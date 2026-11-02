# Implementation - artgen 0.12 into the framework

artgen 0.12.0 (image_tools PR #43, merged as `98ac9cb`) builds what `plans/dungeon-maps/report-artgen.md` asked of
the engine. Its plan, and what was built, is image_tools' `docs/DUNGEON-PLAN.md`; every key of a dungeon file is in
`docs/DUNGEON.md` there and in `node tools/artgen/artgen-maps.js schema dungeon --keys`. This plan moves the framework onto
it and retires the code report 2 lists. Commits cite tasks as `artgen-0.12 T1`. Each task ends with
`python3 tools/validate_setting.py` clean of errors, both `--check` builds passing, and commits on its own.

| Task | What | Files |
|---|---|---|
| T0 | Prerequisites and baseline (below) | `metrics-before.txt` |
| T1 | Install 0.12; CLAUDE.md; re-check what the framework writes | `tools/artgen/`, `.claude/`, `CLAUDE.md`, `plans/sheet-maps/artgen-capabilities.md` |
| T2 | `pack` lays a block out with `artgen dungeon layout`; `pack.py` and the packing half of `route.py` retired | `tools/dungeon.py`, `tools/maps.py`, `tools/pack.py`, `tools/route.py` |
| T3 | A block's map routes its passages in the engine (`route: "maze"`); `route.py` retired | `tools/dungeon.py`, `tools/route.py` |
| T4 | `mapcheck.py` retired: the validator reads `dungeon check` and `dungeon facts` | `tools/dungeon.py`, `tools/mapcheck.py`, `tools/validate_setting.py` |
| T5 | Stairs as room exits; shapes in the engine's terms; Rock as areas; the block's outline as bounds | `tools/dungeon.py` |
| T6 | Docs, skill and metrics | `README.md`, `.claude/skills/setting-maps/SKILL.md`, `STEPS.md`, `metrics-after.txt`, this folder |

## T0 - prerequisites and baseline

- **The release tag.** `artgen-v0.12.0` (`98ac9cb`) and `artgen-dist-v0.12.0` (`9ae8487`) are in image_tools, so T1 can pin
  `#artgen-dist-v0.12.0`.
- **The build.** `git ls-remote https://github.com/rstevenson1237/image_tools refs/heads/artgen-dist`, then
  `artgen-dist` `maps/VERSION` must read `0.12.0`. The artgen-dist workflow publishes it from the merge; if its run failed, fix
  that in image_tools first.
- **Baseline.** `python3 tools/metrics.py > plans/artgen-0.12/metrics-before.txt`; keep the validator's output and a site build
  (`build_site.py --out <scratch>/before`) and block maps (`maps.py draw --out <scratch>/maps-before`) to diff against after
  T1. Scratch does not outlive the session; a later one rebuilds them from T0's commit.

## T1 - install 0.12

- `npx -y github:rstevenson1237/image_tools#artgen-dist update --notes <scratch>/notes.md`. The installer now writes
  `artgen-maps.js` into the core commands of a maps-only repo, so the files 0.11 installed are replaced. It keeps this repo's
  CLAUDE.md section, which was edited by hand.
- **CLAUDE.md.** 0.12 has a section written for this case: a maps-only repo with no `art/` that names its files with `--file`.
  Move the first line of the current section ("Maps are built from the tables …") above the markers, into the framework's own
  part. Then run `update --force` so the installer writes its section and tracks it again, and drop the second line ("artgen's CLI
  here is …"), which the installed section now says correctly.
- **What changes in the drawing, and is expected.** The block files are still format 1, read as format 2 by migration and drawn as
  before, except where 0.12 changes the drawing whatever the format. Room labels move off symbols and other labels. Doors are set
  along the wall where a passage meets it at a slant. Diff the site build against T0's and look at each changed map.
- **`plans/sheet-maps/artgen-capabilities.md`.** Most of its "observed" lines are now fixed or documented (A1-A16). Cut it to
  what the framework writes and why, and point at `schema dungeon --keys` and image_tools' `docs/DUNGEON.md` for how each key behaves.

## T2 - `pack` lays a block out in the engine

`plans/artgen-0.12/prototype/export_graphs.py` builds each block's graph from the tables, as `pack_region` builds its inputs
for `pack.py`. In image_tools, all ten blocks lay out from these graphs at BRIEF.md's footprints: every way routed, none past its
detour, `check` clean, 1.4 to 9.6 s a block. That is image_tools' fixture `setting-builder/layout`.

- In `pack_region`, write the graph (rooms in 5 ft cells; ways with the bearing to keep and the wall named; `fill`, `passages`,
  `detour`, `footprint` from BRIEF.md). Then run
  `node tools/artgen/artgen-maps.js dungeon layout --file <tmp> --graph <g.json> --seed N --json --force` and read its `report`
  (`left`, `detours`) and the rooms it placed.
- **What the prototype leaves out and T2 adds.** Rooms placed `against` another become `rooms[].against` (`glued`'s feet east and
  south become cells). A stair's room over another level's becomes `rooms[].over`, a box in the footprint's frame (`pins`). Rock
  becomes `keepOut` polygons in the footprint's frame (as `ground()` frames them). A poly `outline` becomes `footprint`.
- **Back to the tables.** Each room's `xyz` comes from the block's centre: x is `(room.x + w/2 - margin) * 5 - side/2` feet east
  and y is `side/2 - (room.y + h/2 - margin) * 5` feet north (margin 2 cells, side in feet). A turned room's `width`, `length`
  and `outline` come from what the file wrote. Ways inside the block lose their `bearing` and `distance`, as now.
- **Retire** `tools/pack.py` and everything `pack_region` calls in it. `ground()`, `frame_of()` and `route.LATTICE` go when T3
  retires `route.py`.
- The engine routes with clearance 0: a passage may run along a wall, which format 2 draws. H.a packs only with that (`pack.py`
  never found it a passage within its detour).

## T3 - passages routed in the engine

- `block_map` writes `"version": 2` and lets `style.sharedWalls` default (walls wherever two floors meet). For each way inside a
  block: a `connection` where its rooms touch (as now), else a corridor with `route: "maze"` and `width: 2` (10 ft on 5 ft cells),
  its ends `{room, side}` or `{room, port}` where the Connection names a wall. Write the corridors shortest first, as `layout`
  routes them, so the map draws the passages `pack` measured.
- `walks()` (each way's wall and walk, for Ground and the dry fire) reads `dungeon facts`: each corridor's `path` and its doors.
  `route.detours` becomes the validator's own sum over `path`.
- Blocks' `router` (Dangerous_Schema line 129) records the `tools/route.py` version. Either record the mapgen version that packed
  the block (`artgen-maps.js --version`) or drop the field. **The user's call.**
- **Retire** `tools/route.py`.

## T4 - `mapcheck.py` retired

`defects()` becomes `dungeon check --file F --json --errors door-off-wall,through-room,corridors-cross,way-no-passage,reenters-room,port-outside-room,rooms-overlap,in-keep-out,outside-bounds,maze-no-route`
plus two comparisons against the tables:

| mapcheck finding | 0.12 |
|---|---|
| rooms overlapping | `rooms-overlap` |
| touching with no shared walls | `rooms-merge` (only with walls off) |
| corridor through a room, or running into it past its wall | `through-room`, `reenters-room`, `port-outside-room` |
| corridors touching that share no room | `corridors-cross` (corridors from one room may join) |
| a door not on a wall between two floors; doors stacked | `door-off-wall`, `doors-stacked` (`facts.doors[].on`) |
| a room reached by no way | `facts.unreached` |
| ways the tables name that the map lacks, and the reverse | compare the tables' ways with `facts.rooms[].doors` and `connections` |
| exits the tables take vs marks drawn | compare with `facts.rooms[].exits` (after T5) |
| labels laid over one another | `label-overlap` (stays a warning) |

**Retire** `tools/mapcheck.py`.

## T5 - stairs, shapes, ground

- **Stairs.** The ~40 lines of stair spots, insets and angles in `block_map` become `rooms[].exits`:
  `[{kind: stairs-up|stairs-down|arrow, side: <facing(…) of the way>, text: "Up to F.2"}]`. The engine places the mark a cell in
  from that wall, turns it toward the wall, puts the note beside it, and moves the room's label clear.
- **Shapes.** `DRAWN` maps `octagon` to `octagon` with `cut: 0.2929` (`1/(2+√2)`, regular, as `route.py` drew it) and `hexagon` to
  `hexagon`. Only `poly` outlines stay polygons.
- **Ground.** A block's own poly outline becomes `bounds`. Each Rock becomes `areas: [{points, kind: rock, label: <what>}]` in
  place of an overlay note. Consider `style.rock: solid` (report A9: the reference maps use solid ground); **the user's call**.
  `style.partition` can replace `wall: 2.5` if only the walls between floors need the weight.

## T6 - docs, skill, metrics

`README.md`'s `tools/` list loses `pack.py`, `route.py` and `mapcheck.py`, and says what `dungeon.py` hands the engine. The
`setting-maps` skill names `dungeon layout`, `check` ids and `facts`. STEPS 4a's `pack` sentence stays true; check its wording.
`python3 tools/metrics.py > plans/artgen-0.12/metrics-after.txt`. Anything the engine still does wrong goes upstream with
`artgen-maps.js report --file … --made-by "python3 tools/maps.py draw" --note "…"` (the `setting-maps` skill says how).

## Open decisions for the user

1. Blocks' `router` field: record the mapgen version, or drop it (T3).
2. Solid rock or hatching for packed levels (T5).
3. With the engine reaching about 55% fill at the smallest square BRIEF.md's `fill` allows, whether to lower BRIEF.md's pack footprints.
   That is a design change to the setting, not part of this move.

## Risks

- **The map moves.** T2 repacks every block, so positions, Ground and the dry fire change. Run `space.py settle` and
  `maps.py ground` after it, as STEPS 4a says. Diff the write-ups' Exits and Ground lines.
- **Slower packs on G and H.** 8 to 10 s each at 12 tries on one core; `--tries` lowers it, at a cost to how short the ways walk.
- **The layout and the draw disagree.** T3 routes again at draw time. If a block draws a passage `pack` did not measure, write the
  layout's `via` into a cache keyed by the block's tables, rather than letting the two drift.
