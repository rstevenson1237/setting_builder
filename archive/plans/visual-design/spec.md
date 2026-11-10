# Spec - visual design

What this change makes true, and why. The task plan is `implementation.md`; the request and the
answers that shaped it are `intake.md`.

## Words

Two words mean different things here and in artgen. This plan keeps them apart.

| Word | Here | In artgen |
|---|---|---|
| Block | one map of a region: a DANGEROUS level or a SAFE/WILD settlement (`Blocks.md`) | a shape split into rooms that share walls (`dungeon block`) |
| Brief | `BRIEF.md`, the build's counts and outline | the proposed `brief.json`, one dungeon's design request |

In this plan an artgen block is called a **split**, and the per-block request is called the
**design brief**. A **layout** is a named motif that expands to rooms and ways. A **design** is
one block's committed design file.

## Review of `DUNGEON-DESIGN.md`

Checked against image_tools at `0056fe4` (artgen 0.13.0) and this repo at `7f3d6cd`.

| Claim | Verdict | Evidence |
|---|---|---|
| Two published maps were recreated at about 0.90 floor overlap | Not checked here; taken as reported | The work is in image_tools. `scripts/dungeon-compare.mjs` exists. |
| `dungeon gen` scatters rooms and joins them with a spanning tree plus loops | True | `dungeon/generate.ts`, lines 2-3 and 59-67 (Prim, then `loops`) |
| Random layouts are `scatter`, `dense` and `blocks` | True | `generate.ts`, lines 33-34 and 128-197 |
| Splits take rect, octagon, circle, hexagon or polygon, and join with `link` | True | `dungeon/blocks.ts`, header |
| `dungeon layout --graph` takes named rooms, ways with bearing and wall, a footprint or polygon, `keepOut`, `fill`, `passages`, `detour`, `over`, `against` and a seed | True | `dungeon/graph.ts`, `GraphRoom`, `GraphWay` and `Graph` |
| `layout` is a port of this repo's `pack.py` | True | `plans/artgen-0.12/implementation.md` T2; image_tools `docs/DUNGEON-PLAN.md` line 24 |
| This repo builds graphs from its own tables | True | `tools/dungeon.py` `graph_of` |
| The drawing gaps #46 to #56 are open, and steps 5 and 8 wait on them | **Out of date** | artgen 0.13.0 fixes all of them, and #44 and #45. Its changelog lists double doors, plain and keyed numbers, palettes and presets, wall weights, dashed walls, `rings`, wavy edges and new symbols. Nothing in steps 5 or 8 now waits on a drawing gap. |
| The concept-to-brief work belongs with this repo | True, with two corrections | The words above clash. Pins (`over`, `xyz`), voids (`Rock` becomes `keepOut`) and 3D places (`tools/space.py`) already exist here, so the design step builds on them. |
| An unset footprint lets the solver grow the level | Partly | `Graph.footprint` unset means "the least square `fill` allows". That is compact, not grown from a point. True growth is an engine feature (see the report). |

The proposal's split of work holds, but the order changes: everything is built here first
(`intake.md`). What the prototype and the pilot show belongs in the engine is written into
`report-artgen.md` as the work goes, and sent only when the user agrees. Once artgen ships it, the
framework upgrades and moves onto it (S14).

## S1. A design step, optional per region

- A region's `BRIEF.md` node may hold one `design` line. With it, the region's blocks are
  designed at a new step **3d**, after its seed (3c) and before `Locations.md`. Without it, the
  region is built as today.
- The steps after it are renumbered, as the user asked: `Locations.md` becomes 3e,
  `Connections.md` 3f, and the second `maps.py ground` 3g. Every citation moves with them
  (implementation T4 lists them). "3d" is also a count of Tests in the content (`Test of
  Constitution, 3d, Piercing`), and those are not step ids.
- 3d writes `setting/region/[Code]/Design.md`, following `templates/region/Design.md`. Steps 3e
  and 3f read it when it exists and write the tables to agree with it.
- A designed DANGEROUS block is not packed at 4a: its places come from the design. `maps.py pack`
  refuses a designed block and names 3d.

## S2. The design file

`Design.md` holds one `Design` node for each block of the region, in KDL like the tables, read by
`tools/kdl.py`. Its schema sits in `patterns/Region_Schema.md`, since every rating can have one.

A design holds:

- the block's code, its `xyz`, and its `outline` where it is bounded (S5);
- its settings: `fill`, `spacing`, `passages`, `detour` (S5);
- its voids (S6);
- each layout it uses, by id, with values for its parameters, and each role bound to location
  codes;
- each socket join, between two layouts or from a layout to a way out of the block;
- after approval, the solved place of every location (`xyz`, `outline`, `shape`), every way (door
  or passage), the seed, the candidate's score, and `approved`. Only the user's word sets
  `approved`.

Location codes are given at design time (`G.1` to `G.29`), so the tables can follow. A role
carries the location `type` it asks for (`High`, `Medium`, `Low`, or a WILD/SAFE type).

## S3. Agreement: the validator holds tables to the design

For each block with an approved design, the validator reports an **error** when:

- the design's location codes are not exactly the block's `locations`;
- a location's `xyz`, `outline` or `shape` in the tables differs from the design's;
- a way inside the block is in the design and not in `Connections.md` (both sides), or the other
  way round, or its door or passage kind differs;
- a role's `type` differs from the location's `type`;
- a design void has no matching `Rock` (DANGEROUS) or `Void` (SAFE/WILD) entry, or the other way
  round.

It reports a **warning**, owed by 3d, for a region whose `BRIEF.md` node has `design` but has no
approved design. `--pending` lists it. Each error names the step that fixes it: 3d when the
design is wrong, 3e or 3f when the tables are.

`tools/space.py` reads design places through the same code as table places, so the dry fire
covers designs.

## S4. Layouts

- The library is `layouts/`, one KDL-in-markdown file per layout, read by `tools/kdl.py`. Its
  format is `patterns/Layout_Schema.md`.
- A layout holds `id`, `tags`, `params` (each a range), `parts` (rooms and passages, each with a
  role, a size or shape, and an optional place relative to another part), `ways`, `sockets` (a
  part, a bearing and a width), `constraints` (for now advisory: `mirror`, `straight`), and
  `source` (`drawn` with an origin, or `written`).
- Layouts are **flexible**: they expand to rooms and ways that the existing `dungeon layout` places.
  Rigid stamping waits for the engine (`report-artgen.md`).
- Several layouts make one block. They chain socket to socket; a socket left unjoined is closed.
  The rooms a block needs beyond its layouts are **fill**: plain rooms placed by the solver.
- The first library, from the maps the proposal studied and this build's own levels:
  `cell-row`, `spine-ring-hub`, `axis-of-halls`, `suite`, `stair-vestibule`, `secret-bypass`.
  "Dressed focal room" is a role tag (`focal`), not a layout.

## S5. Filling a shape, or growing from a point

- **Bounded** (the design states an `outline`): the solver's footprint is the outline and `fill`
  is the share of it the rooms cover.
- **Unbounded** (no `outline`): the footprint is left unset, which gives the least square that
  `fill` allows, centred on the block's `xyz`. After the solve, the block's outline is written as
  the hull of what it holds. True growth from a point is an engine request.
- `spacing` is the corridor length wanted between joined locations, as a range in feet. It is
  scored, and it sets `passages` and `detour` for the solver where the design leaves them unset.
- Defaults come from the `dangerous` `pack` line in `BRIEF.md`. A `design` line or a design
  overrides only the values it names.

## S6. Voids

- A void is an outline, with an `xyz`, inside a block that no location or way takes.
- In a DANGEROUS block it is the existing `Rock` node, which is passed to the solver as `keepOut`.
- SAFE and WILD gain a `Void` node with the same fields (`what`, `outline`, `xyz`). It is drawn as
  open ground, and a location placed in it is an error.

## S7. Solving, scoring, choosing

`tools/design.py`:

- `layouts`: lists the library with tags and parameters.
- `expand CODE`: turns a design into the `dungeon layout` graph (rooms, ways, footprint,
  `keepOut`, pins from `over`) and prints it.
- `solve CODE [--seeds N] [--keep K]`: runs the solver over N seeds and scores each result against
  the design brief: location count, fill, every way routed, dead-end share, spacing, symmetry
  where asked. It renders the best K to PNG with a contact sheet in a scratch folder, and prints a
  table of scores and what each one trades off.
- `accept CODE --seed S`: writes that candidate's places into `Design.md`, with `approved` left
  for the user's word.
- `check`: the agreement in S3, called by the validator.

For SAFE/WILD blocks, a spike decides the solver first (implementation T6). Either the same
`dungeon layout` call packs building footprints and routes streets, or those designs use fixed
geometry stated in the layout.

## S8. The design skill

`.claude/skills/block-design/SKILL.md`, this repo's, beside `setting-maps`. It runs 3d:

1. Read the region's `BRIEF.md` node, its seed and `GENRE.md`. Ask the user only what they leave
   open, in at most three questions.
2. Choose layouts by tag, bind roles to codes, chain sockets, and write `Design.md` without
   places.
3. Run `design.py solve`. Show the user the contact sheet and the score table.
4. Run `design.py accept` for the user's pick. Set `approved` only on their word.
5. Hand over to 3e and 3f.

It names the existing `dungeon-map` skill for the meaning of every artgen key, and repeats none
of it.

## S9. One place from another

`python3 tools/space.py from CODE to CODE` prints the distance, the compass bearing and the climb
between any two regions, blocks or locations, from their absolute places.

## S10. artgen 0.13

Install `artgen-dist-v0.13.0` as the `setting-maps` skill says. Remove any workaround in
`tools/dungeon.py` or `tools/maps.py` that 0.13 makes unneeded. Add the new check ids that apply
to `dungeon.FAULTS`. Bring `plans/sheet-maps/artgen-capabilities.md` up to date.

## S11. The house look

- `BRIEF.md`'s framework levers gain a `maps` node with one `look` line per map kind, written at
  the default the user picks and changed there like any other lever:

  ```kdl
  maps {
    look dungeon hatch=none rock=solid wall=1.5 numbers=plain doors=square rock-color="#a9824c" floor="#f6ecd6" ink="#3a2a18" grid="#c9b48c" wall-color="#3a2a18"
    look settlement theme=color
    look terrain theme=color
  }
  ```

  (the values shown are option B below). A dungeon `look` may also name `preset=dark|blueprint`,
  whose values fill what the line leaves unset. A key left out keeps today's drawing, so a
  `BRIEF.md` with no `maps` node draws every map as it does now.
- `tables.Brief` reads it; `tools/dungeon.py` and `tools/maps.py` apply it in place of today's
  fixed values (`dungeon.py`'s `style`, `ROUTED_WALL`; `maps.py`'s `--theme color`). The validator
  rejects an unknown key, preset or theme, and a colour that is not `#rrggbb`.
- The options, rendered with artgen 0.13 on level 5 (`G.a`), the Drifted Streets (`A.a`) and the
  Sands sheet, are in `looks/`:

  | Option | Dungeon | Note |
  |---|---|---|
  | A. Classic | today's grey hatched rock, black walls, with plain numerals and square doors | prints anywhere |
  | B. Sand | solid ochre rock, cream floors, dark brown ink and walls | the Lost City's colours; prints as mid-grey rock in black and white |
  | C. Sand on hatch | cream floors and brown ink over today's hatch | the hatch stays grey: `palette.rock` does not colour it |
  | D. `dark` or `blueprint` preset | solid dark or blue rock, white floors | the walls take the rock's colour, so walls between touching rooms vanish and rooms run together; usable only with `wall-color` set to the ink |

  Settlements and terrain keep `color` (today) or take `bw`. In 0.13 a settlement drawn `bw`
  still has coloured ground, which goes in the report.

## S12. Claude Code settings

`.claude/settings.json` allows the commands every step runs without a prompt: this repo's own
`python3 tools/*.py` commands and the artgen CLI (already allowed). It asks before anything that
reaches outside the repo: `artgen ... report --issue`, the `npx` installer, and `git push`.
The rule syntax is checked against the current Claude Code documentation before it is written.

## S13. What else changes

- `CLAUDE.md`: the maps line says that a designed block's tables follow its approved design, and
  that drawn maps are still built from the tables.
- `README.md`: `layouts/`, `tools/design.py`, the `block-design` skill and `Design.md`.
- `STEPS.md`: the new step 3d, the renumbered 3e to 3g, and 4a for designed regions.
- `templates/region/Locations.md` and `Connections.md` read `Design.md` where it exists.
- `templates/checks/Map_Judgement_Check.md`: one item per designed block, "the drawing reads as
  the approved design".

## S14. Moving onto artgen once it has the engine half

Built here first, the prototype decides what artgen should take. When the user is satisfied with
the prototype and the pilot:

1. The report (`report-artgen.md`) is finished from what the work showed and sent on the user's
   word.
2. image_tools builds what it takes, and releases it.
3. The framework upgrades to that release, as the `setting-maps` skill says, and moves each piece
   onto the engine: `design.py` shrinks to what is framework-specific, `layouts/` moves or stays as
   the report settles, and every design solves to the same places it did before the move (or the
   user approves the difference).

That last phase is a plan of its own, written when the release exists.
