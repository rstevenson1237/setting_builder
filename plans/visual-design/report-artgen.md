# Report to artgen - designing levels, from setting_builder

Status: finished, not sent. It is sent only on the user's word (spec S14), as an issue on
`rstevenson1237/image_tools` labelled `artgen-feedback`.

In reply to image_tools `docs/DUNGEON-DESIGN.md` (`86e957d`), checked against artgen 0.13.0
(`0056fe4`). Everything was built in setting_builder first: a layout library (`layouts/`), a design
file per block (`setting/region/[Code]/Design.md`), and `tools/design.py` to expand a design to a
`dungeon layout` graph, solve it over seeds, score the packings and hold the tables to the result.
One level, region E of this build, was designed that way end to end (`pilot-E.md`). Evidence
files are under `plans/visual-design/` and are named in each request.

## Answers to its open questions

- **Does setting_builder want to emit a brief, or keep calling `layout` with its own graph?** For
  now it keeps calling `layout`. When artgen has a design brief and layouts of its own,
  `design.py` will emit the brief and shrink, as `pack.py` did in 0.12.
- **Who owns the library?** A bundled set in artgen, plus a project folder. setting_builder keeps
  its own `layouts/` and will offer the ones that prove out.
- **Rigid or flexible first?** Flexible, as proposed. Its limits are R2 and R4.

## Corrections to the proposal

- §7 step 8 and §9: issues #46 to #56 are fixed in 0.13.0, so dressing and rigid features no
  longer wait on drawing gaps.
- Two words clash: setting_builder's `BRIEF.md` is a whole build's brief and its Block one level or
  settlement. It calls artgen's block a "split" and the per-dungeon request a "design brief".
  artgen's docs should not assume "brief" means one dungeon.
- setting_builder already has pinned rooms (`over`, from absolute places), voids (`Rock` as
  `keepOut`) and a 3D place for every room (`tools/space.py`).

## Requests

| # | Request | Evidence |
|---|---|---|
| R1 | A layout format and composition in the engine: parts with roles, a count from a parameter, sockets with a bearing and a width, chain by socket, and a check that joined sockets face one another and match in width | `layouts/*.md`; `tools/design.py` (`Expand`); `evidence/E-graph.json`, the graph E expands to |
| R2 | Solver constraints (below) | `evidence/E-seed-1-unpinned.png`, `evidence/six-layouts-joined.png`, `evidence/cell-row-seed-2.png` |
| R3 | Growth from a point, and `over` that does not need a frame | `evidence/E-seed-12-pinned-crossing.png`; unbounded runs below |
| R4 | Rigid layouts stamped as exact geometry, using 0.13's `rings` and door kinds | A ring hub's eight doors cannot be held by the solver (R2) |
| R5 | `dungeon design`: layouts plus a design brief to a graph; N seeds; scoring; a contact sheet. Score what artgen already finds (`doors-stacked`, `door-off-wall`, `outside-bounds`), and two passages leaving one room that cross or run together, which `check` allows and no hub reads as a spoke | `tools/design.py` `solve`; `evidence/E-seed-12-pinned-crossing.png` against `evidence/E-seed-1-unpinned.png` |
| R6 | `dungeon pattern extract` (proposal §4.3) | Grows the library from drawn maps; the six layouts here were written by hand |
| R7 | The measuring half of trace (proposal §4.3) | As the proposal says |
| R8 | A settlement laid out from a graph: streets that run past several buildings, a gate, a wall, and spacing that is a target and not a result | `spike-settlement.md`, `spike-settlement-1.png`, `spike-settlement-2.png` |
| R9 | `style.palette.rock` colours the hatch too, and the `dark` and `blueprint` presets keep walls between touching rooms visible | `looks/dungeon-looks.jpg`: a sand palette leaves the hatch grey, and both presets draw walls in the rock's colour |
| R10 | A settlement drawn `--theme bw` draws its ground in black and white | `looks/settlement-terrain-looks.jpg` |
| R11 | `dungeon layout`'s routes as an input: a file whose rooms are placed and whose passages follow given routes | The tables hold places and ways, so the map redraws each passage and reads as the design in its rooms and not in its passage shapes (`pilot-E.md`) |
| R14 | `layout` with cave and polygon rooms: it joins a room as its box, so a way between two caves is a door on a wall the cave's outline does not reach | `evidence/test-dungeon/designs/Z-Design.md`: 24 of 24 seeds routed, and `check` finds `way-no-passage` on 10 or 11 of the 13 ways |
| R15 | The `dark` preset draws the outside band (title, scale bar, legend) in colours that cannot be read, and a legend of thirty symbols shrinks a square map to a thumbnail | `evidence/test-dungeon/level3.png`; `level2.png` |
| R16 | Carry what a table cannot say into the map: symbols, rings, wavy edges, natural and curved passages, double doors, dashed walls, doors standing in a run | Only door kinds, shapes, widths and stairs came through the tables; the rest was a 30 to 60 line pass for each level (`evidence/test-dungeon/scripts/`) |
| R17 | A passage that ends at a round, octagonal or polygon room goes to its anchor, by a diagonal final leg, and two such passages overlap there; passages that leave one wall of a rect room a cell apart overlap and stack their doors | Seen on the test dungeon's Y.7 and X.1, and on C.4 and G.22 of the pyramid. `check` finds the stacked doors but not the diagonal leg. setting_builder now writes ports and offsets itself (`dungeon.block_map`, `spread_ends`), where `check` agrees |
| R12 | Room places in whole feet: a room an odd number of cells wide has its centre at a half foot, so the packing's place is not one a table can hold | `design.py` sizes rooms in 10 ft steps to avoid it |
| R13 | Routing that holds at 25 rooms and more: seeds that route, or a repair when none do | G at 29 rooms (below): the real graph from the tables routes 1 seed of 12, and a design of the same size 0 of 12, so a level this size needs dozens of seeds |

### R2: constraints, by layout

| Layout | Needed | Seen |
|---|---|---|
| `cell-row` | cells held against the hall's two long sides, mirrored | Held as a row on a small design; on E three rows came out loosely grouped, a cell a hall's length away |
| `spine-ring-hub` | a socket's bearing held, sockets that are opposite held opposite, a round hub with its doors at the compass points | A socket asked north gave a room south on one seed; E.2's write-up needs four opposite pairs |
| `axis-of-halls` | halls on a line | Scored (`straight`), not held |
| `suite` | a sub-room against one wall of its main room | Left to the bearing |
| `stair-vestibule` | a room pinned over the level it meets | Works as `over`, in the footprint's frame (R3) |
| `secret-bypass` | a way that is not drawn as a passage | A Secret on a way is the tables', not the layout's |

### R3: how growth and pins behaved

- Unbounded (no footprint), six rooms: the least square was 90 ft at 54% fill, every way routed.
- Bounded, nine rooms in a 300 ft footprint (`evidence/six-layouts-joined.png`): 4.5% fill, the rooms packed
  in a corner. A footprint far larger than the rooms gives no spread.
- A stair into a room pins it over a room of the next level, in the footprint's frame, so an unbounded
  design with a stair cannot be solved: the side is not known until the solve. `design.py` asks for an outline.
- Solved beside two placed levels, E's two stair rooms were pinned: several seeds failed to route
  and the cleanest packing still had two passages crossing. Solved with the pins off, all sixty seeds
  routed and the best scored 96. The level beside has to be placed after, from this one (`--free`).

### More cases (scratch designs, `evidence/scratch-designs/`)

Run in a copy of the repo, not committed. Routed means every way routed.

| Case | Setup | Result |
|---|---|---|
| G, 29 rooms | five layouts, 33 ways, 240 ft ground | 0 of 12 routed pinned at 240 and at 300 ft, 0 of 12 unpinned, 0 of 24 unpinned with the fill floor at 25%; 2 of 12 at 300 ft, scoring 63 and 0; 1 of 12 unbounded in 286 s, scoring 0 |
| G, baseline | the real graph from the tables, 34 ways with a bearing each | 1 of 12 routed in 72 s: the engine is slow at this size, not the design |
| G, bearings | the design with bearings off, with rooms free to turn | 0 of 12 at 240 and 300 ft: bearings are not the cause |
| I, 14 rooms, unbounded, unpinned | ring hub, cell row, suite, secret bypass, two fill | 24 of 24 routed, best 95, hull of about 110 by 120 ft (`evidence/I-unbounded-14-rooms.png`) |
| J then K, in order | J designed unpinned and its tables written; K solved pinned under J.6 | K.1 lands under J.6 (same plan place, 20 ft down); pinned K 24 of 24 routed, best 95; unpinned K 24 of 24, best 100 |
| K, small ring | a 20 ft hub with four 10 ft passages | 0 to 4 of 24 routed, scoring 27 or less at 100 ft and 80 ft; the same design with a 40 ft ring routed 24 of 24 |

What they add:

- **Layouts need relations between parameters.** A ring hub's size has to grow with the passages that leave
  it. A layout cannot say so, and a design that picks `ring=20` fails on every seed. R1 should allow a
  parameter's minimum to depend on the sockets joined.
- **Spacing stayed a hint.** The median gap between joined rooms came out 0 ft in I and J against a wanted 10 to 30
  (R5).
- **Pins cost little when the design is sound.** Pinned K scored 5 below unpinned. What failed was
  the design's sizes, which the score shows and the pins do not explain.
- **A role's rooms share one type.** A `Bind` gives every room of a role one type, so a role whose rooms differ
  in type (I.6 Low, I.7 Medium) cannot be bound. This is setting_builder's to fix, not artgen's.

### The test dungeon (`evidence/test-dungeon/`)

Three independent DANGEROUS regions, X (d10), Y (d8) and Z (d6), in a scratch copy with the pyramid's regions
removed, designed in order so each level's stair pinned the next, each carried to a map from its tables and then
given every engine feature the tables cannot state. The brief was: level 1 two intertwined loops with secret
ways, side branches and a stair at the far end of the right loop; level 2 three routes to a wide hall of statues
and a fountain (the middle one a wide trapped lane), a gate room that branches again into two looping routes round a
dense core, one core room descending; level 3 a natural spiral to a final chamber.

| Level | Design | Solve | Map from the tables |
|---|---|---|---|
| X, 22 rooms, 25 ways | a figure of eight (new layout) with stair end, spurs, secret rooms; unbounded, unpinned | unpadded: 24 of 24 routed, but 20% of the ways were passages against 100% asked, median gap 0, 198 s. Pad 5 ft: 24 of 24, three seeds at 100, 72 s. Pad 10 ft: 24 of 24, one at 100, 204 s | pad 5: all 25 ways drawn as passages, 11 artgen findings (stacked doors, doors off walls, 2 no route, 1 outside the bounds). Pad 10: 5 findings |
| Y, 27 rooms, 29 ways | three-routes, twin-loop and dense-block layouts (new), polygon, round, hexagon and octagon rooms, a dense core with pad 0 and the rest at pad 10; pinned under X's stair | 0 of 24 at 240 ft; 0 of 12 unpinned at 240 and at 320 ft; 7 of 24 at 320 ft pinned, best 85 with one crossing; 240 s | 22 passages, 7 doors in the core's shared walls, no findings |
| Z, 14 rooms, 13 ways | a square spiral of caves (new layout), pinned under Y's stair | 24 of 24 routed, but a serpentine of long straight passages with the final room off to one side, not a spiral; `check` flagged `way-no-passage` (R14) | The spiral was stated by hand (fixed geometry, `Place` and `Link` lines): 14 caves, 13 passages, no findings |

What the feature pass drew without error, over the three maps: all seven door kinds (door, locked, secret, portcullis,
arch, double, open), doors standing in a run, solid, dashed and weighted walls, rect, octagon, hexagon, circle, polygon
and cave rooms, wavy edges, natural passages curved through their bends, rings, twenty-seven of the thirty-three symbol kinds
(the stairs came from exits, and `stairs` was drawn in a probe), a legend, the classic, sand and dark looks, and (on a copy of level 2) walls with towers, voids, rock areas, split
blocks, exits with a fade, a passage joining a passage, diagonal passages, pointy hexagons, octagon cuts, fills, links and
stretched symbols: seventeen probes, seventeen passes, two with `check` findings
(`through-room` and `doors-stacked`).

What it adds:

- **Corridors have to be asked for another way.** `passages="100%"` gave 20% and `spacing` a median gap of 0.
  Growing each room by a pad in the solve and drawing the real rooms from the tables made every way a passage
  and cut a 22-room level's solve from 198 s to 72 s. The engine should take a minimum gap between rooms (R5).
- **Pad size matters.** A 10 ft gap leaves a corridor too short for the doors at its two ends (stacked doors,
  doors off walls); 20 ft halved the findings (11 to 5).
- **A spiral, and any shape that is a path, is not held** (R2). The solver keeps its bearings softly and gives
  the shortest packing; a hand-stated spiral drew correctly through the same pipeline.
- **Dense levels route rarely.** Y at 27 rooms routed 29% of seeds on a ground 40% larger than its fill needed;
  X at 22 rooms with a pad routed all of them (R13).
- **A level designed first cannot pin the next.** A stair pin was read from a room's own Connections, which a level
  not yet written lacks; `space.py` now reads the connection into it, and the region's place where the room has none.
  The same pin failed for a polygon partner. Both are fixed here; the engine's `over` has the frame problem of R3.
- **Mixed shapes need per-room choices.** A layout part has one shape, so polygon and round rooms came from `Fill`s
  and left no layout to hold them; a role of rooms with differing types could not be bound until `Bind` took a type
  for each.

## What `design.py` does that the engine should

`expand` (a design to a graph, with sockets, ties and fill), the socket check (R1), `solve` over seeds
in parallel, the score (R5), the convex hull of what a packing holds for an unbounded level's outline,
and the contact sheet. A graph with named parts and sockets is the part to move; the rest is a loop around
`layout` and `check`.

## What stays framework-specific

`Design.md` as a table file and its agreement rules with `Locations.md`, `Dressing.md`,
`Connections.md` and `Blocks.md`; the steps (3d, then 3e and 3f) and the user's approval; the house look
as a `BRIEF.md` lever; the type mix; prose that states a constraint the design must keep (E.2's
opposite arches); and the staleness of a write-up, which is git time.

## What will be sent as fixtures

`layouts/`, `setting/region/E/Design.md`, and `evidence/`, through
`artgen report --file ... --made-by "python3 tools/design.py expand E --free"` for a graph or a map.
