# Report to artgen - designing levels, from setting_builder (draft)

Status: draft, not sent. Everything is built in setting_builder first. This report gathers
what the prototype and the pilot show belongs in artgen; T10 of `implementation.md` finishes it,
and it is sent only on the user's word. Once artgen releases what it takes, setting_builder
upgrades and moves onto it (spec S14).

In reply to image_tools `docs/DUNGEON-DESIGN.md` (`86e957d`), checked against artgen 0.13.0
(`0056fe4`).

## Answers to its open questions

- **Does setting_builder want to emit a brief, or keep calling `layout` with its own graph?** For
  now it keeps calling `layout`. A prototype in setting_builder (`tools/design.py`, `layouts/`) turns
  a per-block design into the graph. When artgen has a design brief and layouts of its own, the
  prototype will emit the brief instead and shrink, as `pack.py` did in 0.12.
- **Who owns the library?** A bundled set in artgen, plus a project folder. setting_builder keeps
  its own `layouts/` and will offer the ones that prove out.
- **Rigid or flexible first?** setting_builder started with flexible layouts.

## Corrections to the proposal

- §7 step 8 and §9: issues #46 to #56 are fixed in 0.13.0, so dressing and rigid features no
  longer wait on drawing gaps.
- Two words clash with setting_builder's: its `BRIEF.md` is a whole build's brief, and its Block is
  one level or settlement. setting_builder calls artgen's block a "split" and the per-dungeon request a
  "design brief". A rename on either side is not needed, but artgen's docs should not assume
  "brief" means one dungeon.
- setting_builder already has pinned rooms (`over`, from its absolute `xyz`), voids (`Rock`
  passed as `keepOut`) and 3D places for every room (`tools/space.py`).

## Requests

| # | Request | Why |
|---|---|---|
| R1 | A layout format and composition in the engine: parts with roles, sockets with bearing and width, chain, nest, repeat, mirror (proposal §4) | The prototype's expander does this in Python; it belongs beside the solver |
| R2 | Solver constraints: mirror pairs, a straight spine, 45° ways, a part held at a place relative to another | A flexible layout's shape is lost when the annealer packs its rooms as a cluster |
| R3 | Growth from a point: no footprint, an origin, a `spacing` target for passage length, and the hull written as bounds | An unset footprint gives the least square, not a level grown outward from where it starts |
| R4 | Rigid layouts stamped as exact geometry, using 0.13's `rings` and door kinds | A ring hub with its door marks needs no solver |
| R5 | `dungeon design`: a design brief plus layouts become a graph; N seeds; scoring (count, fill, routing, dead ends, spacing, symmetry); a contact sheet | setting_builder's `design.py solve` is the prototype |
| R6 | `dungeon pattern extract` (proposal §4.3) | Grows the library from drawn maps |
| R7 | The measuring half of trace (proposal §4.3) | As the proposal says |
| R8 | (pending T6) a settlement laid out from a graph, or a statement that `dungeon layout` is the way to do it | setting_builder wants SAFE/WILD blocks designed the same way |
| R9 | `style.palette.rock` colours the hatch too, and the `dark` and `blueprint` presets keep walls between touching rooms visible | Found choosing a house look: a sand palette leaves the hatch grey, and both presets draw walls in the rock's colour, so touching rooms run together |
| R10 | A settlement drawn `--theme bw` draws its ground in black and white | In 0.13 its ground stays coloured |

## What the prototype has shown so far

- T5, `tools/design.py expand`. Each of the six layouts expanded and `dungeon layout` routed every
  way, bounded and unbounded. A cell row with a bearing on each way (cells north and south of the hall)
  came out as a row; a spine and ring hub did not keep its ring: the hub's eight door points are
  sockets the solver does not see (R2, R4). The expander checks that joined sockets face one
  another and match in width, which the engine should (R1).
- A stair into a room (`over`) is placed in the footprint's frame, so an unbounded design that
  has one cannot be expressed: the least square is not known before the solve. R3 should let `over` be
  given from the origin, or the engine report the side it will use.

## What setting_builder will send as fixtures

Its layouts, the designs for its pilot level (E) and for C, and the graphs `design.py expand`
writes for them, through `artgen report --file ... --made-by "python3 tools/design.py expand E"`.
