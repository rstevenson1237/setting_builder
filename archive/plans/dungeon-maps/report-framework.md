# Report 1 - Dungeon maps: what the framework gets wrong or leaves open

Scope: the pipeline from `Dressing`/`Connections` tables to a drawn level, as built for level G
(`tools/pack.py`, `route.py`, `mapcheck.py`, the `pack` step, the validator's packed-block checks).
Analysis first; the recommendations are at the end and are short on purpose.

## What the numbers say

| Level | Rooms | Bounding box (ft) | Room share of box | State |
|---|---|---|---|---|
| C | 4 | 115 x 130 | 37% | unpacked |
| D | 6 | 165 x 105 | 47% | unpacked |
| E | 9 | 300 x 253 | 15% | unpacked |
| F | 13 | 330 x 265 | 16% | unpacked |
| **G** | 19 | 220 x 250 | **49%** (was 13%) | packed, routed |
| H | 13 | 309 x 245 | 19% | unpacked |
| I-L | 5-9 | 130-260 | 18-32% | unpacked |

Packing G takes 30-40 s wall clock (about 2.5 CPU-minutes) on four cores; the validator takes 4.6 s.
The new tools are 268 (`pack`), 240 (`route`) and 228 (`mapcheck`) lines. Nine levels remain.

## Findings

### F1. One fact is stored in three places, and only two are regenerated
A room's position is stated in the tables (`Connection.bearing/distance`), again in each write-up's
`**Exits:**` line, and a third time in free prose ("north to the false tomb (G.9)").
Across C-L: 88 write-ups carry an Exits line, 220 bearing/distance pairs in them, and 51 direction
words sit in prose outside Exits. `maps.py pack` rewrites the first two by regex. The third was fixed
by hand in G.6, G.8 and G.16, and nothing checks it: the validator compares Exits *targets* to
Connections, never the bearing or distance, and never reads prose.
Consequence: every layout change costs edits in as many files as the level has locations, and the
unchecked part is the part a player reads aloud.

### F2. The step order makes the layout arrive after the text that depends on it
`3e` writes `Connections.md` with a bearing and distance per way, before any room has a size.
`4a` writes `Dressing` (sizes). `4b` writes the write-ups. Positions can only be computed after
`4a`, so the `3e` numbers are guesses that `pack` overwrites, and any write-up written before `pack`
is stale on arrival. In this build the write-ups already existed, which is why `pack` has to
rewrite them. The schema still *requires* `bearing` and `distance` on every Dangerous Connection,
so the guess cannot be left out.

### F3. `bearing` and `distance` changed meaning without changing name
For SAFE and WILD they are the vector from the way in. For a packed DANGEROUS block they are now the
wall the way leaves by and the walk to the next room's centre. The schema comment says only "from
this end". The validator's reversal check had to be special-cased for packed rooms (the far side no
longer reverses). A reader of the schema cannot tell which meaning applies without reading code.

### F4. Algorithm output is stored as authored data, and the algorithm is not versioned
`east`, `north`, `footprint`, every bearing and every distance are outputs of `pack`/`route`. The
validator re-runs `route.plan` and compares. Consequences:
- Any change to `route.py` (costs, noise, ordering) or its `SEED` silently invalidates every packed
  level; it surfaces only as errors on every Connection line.
- `pack` is not idempotent: it reads the current bearings as the directions to preserve, then
  overwrites them. Packing an already-packed level from a different checkout gives a different
  result. The authored intent ("the stair is south of the hall") and the derived result share one field.
- Determinism holds per seed, but nothing records which seed or which tool version produced a level.

### F5. Rates live in code, against the framework's own rule
`BRIEF.md` is "every count, mix and rate the build is built to". The packer's rates are constants:
target fill 0.45, door/passage mix 35%, minimum fill 0.30 (validator), wall stroke 2.5, hatch
`full`, label sizes. The door-to-passage mix and the fill are exactly the kind of lever BRIEF.md
carries for other artifacts. A user who wants denser or more winding levels must edit Python.

### F6. The pyramid is not a constraint anywhere
GENRE/Setting.md: "the pyramid grows wider for five levels and narrower for five more"; level 6 is
"laid out in the shape of level 4". Nothing encodes either. A level's footprint is an output of its
room areas (G came out at 250 ft because its rooms need that), so widening and narrowing are
accidents of room count, and H matching F cannot be checked. Stairs have the same gap: G.19's way
down and H.1's way up are positioned independently; there is no cross-level constraint, and the
packer sees one block at a time. The user's original request ("constraining the dungeon shapes into
the shape of the pyramid") is therefore met only locally, as a square per level.

### F7. The data model has no linear space
G.2 (10 x 80), G.14 (10 x 90) and G.16 (10 x 80) are authored rooms with encounters and a hazard but
are one passage wide. They are indistinguishable from corridors to the packer and router, sit
beside real passages, and were in the label collisions (G.14 with G.16, G.2 with G.1). `Room_Shape` is
rect/round/octagon/cave; there is no "hall". Whether they are rooms or corridors is a content
decision the schema cannot express, so the tools guess from dimensions.

### F8. The structural gate passes while the picture is wrong
Three defect classes were found only by looking at renders: touching rooms merging into one floor,
a corridor laid against a room wall merging with it, and room labels colliding. Each then needed a
new rule after the fact. `mapcheck.py` now covers the geometry, but it reimplements artgen's
port/width/via semantics from the JSON, so it can diverge from what artgen draws (report 2, A5).
There is no review step for maps in `STEPS.md` step 5; the judgement checks cover templates, schemas
and the setting, not maps. Label overlap stays a warning because room labels cannot be moved (report 2, A3).

### F9. Generated JSON is committed, so any tool change rewrites every level
Changing corridor port offsets modified all ten `*.a.json` files although only G's tables changed.
Staleness is checked only for packed blocks. The sync machinery (`origin: "tables"`, hand edits
kept) exists but no hand edit has ever been made. The files are build output stored as source.

### F10. Map logic is spreading into files that are not map files
`validate_setting.py` imports `maps`, `route` and `mapcheck` and now holds `check_packing`
(about 90 lines) beside `check_blocks`. `maps.py`'s `block_map` carries the routed branch (about 120
lines) inside an already long function, and `settlement_map` has `if wild` branches. Each rating's
block drawing should be one module with one entry point, with the validator calling that entry.

### F11. The design reversed three times because the engine's options were not on hand
Touching rooms were banned, then restored once `style.sharedWalls` was found; corridors-against-walls
were noticed only in a render; stair labels were fixed after a collision. `plans/sheet-maps/
brief-engines.md` records which artgen commit is vendored, not what it can do or how its settings
behave (`sharedWalls` is automatic only when the map has a connection; `via`, `offset`, `hatch`,
`wall` appear in the JSON but not in `--help`). The cost was rework in framework code.

## What works, so it is not lost
- Positions in the tables with the route derived from them: one source, checkable.
- A way graph that stays authored: locks, secrets and hazards stay attached to ways.
- Deterministic packing per seed; a repair loop that re-anneals only the ways that found no passage
  (it took G from 280 ft to 250 ft).
- The validator catching a stale map, a wrong Exits distance and a missing way in the same run.

## Recommendations (ordered)
1. Derive, do not restate: generate the position part of every Exits line from `Connections` at
   build time (or keep the tool, and add a validator check that Exits bearing/distance and prose
   direction words agree with Connections). This removes F1.
2. Move layout before the write-ups and make `Connection.bearing/distance` optional until `pack` has
   run; state their packed meaning in the schema (F2, F3).
3. Separate authored intent from derived output: a `facing` hint on a way for the packer to read,
   and record the tool version in `Blocks.md` so a router change is a visible, single event (F4).
4. Put the rates in BRIEF.md (`fill`, passage share, wall) and give each pyramid level a stated
   `footprint` with a validator rule on the sequence; let a neighbour's stair position pin the next
   level (F5, F6).
5. Decide what a hall is in the schema before packing the other nine levels (F7).
6. Add a map judgement check to step 5 with a fixed viewing recipe (thick walls, zoom) and decide
   whether block JSON is committed or built (F8, F9).
7. Keep an `artgen` capabilities note beside `brief-engines.md` (F11); report 2 is its first draft.
