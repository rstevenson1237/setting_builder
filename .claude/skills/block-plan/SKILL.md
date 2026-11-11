---
name: block-plan
description: Write a DANGEROUS block's design as a plan - the block's ground, its layouts, its rooms and the routes between them, stated in KDL and laid out by tools/plan.py - when a level's shape is known well enough to state, rather than left to the layout engine. Use at step 3d for a complex or hand-shaped level (a hub with spokes, an axis of halls, wings joined by long passages, levels joined by stairs), when a plan leaves a way unrouted or misses a goal, or when changing an approved plan.
---

# Block plans

A plan is one of a DANGEROUS block's two designs at step 3d (`patterns/Region_Schema.md`; the other, layouts chosen
from artgen's library, is the `block-design` skill). Its lines go in `setting/region/[Code]/Design.md`: the block's
`Design` line, then `Layout`, `Room`, `Route` and `Void` lines. `tools/design.py solve` and `accept` hand a planned
block to `tools/plan.py`; everything else in the `block-design` skill holds - the user's word sets `approved`, the
tables then follow the accepted places, and the map is built from the plan.

Every place, facing, side and length is a goal. The solver keeps a plan that routes every way over one that meets
a goal, and says each goal it missed: read the report before showing the map. A way that finds no path first gives up
its own walls, then joins a passage from its other end where that joins no room the way does not (never at a door
or on a spoke), then is routed first and every way again; only then does the whole plan set its goals aside - sides,
facings, lengths, then a larger block, then passages that cross. A level of many rooms wants a block no larger than
its fill asks: spare ground spreads the areas to the edges and lengthens every passage.

## The lines

All sizes and places are feet; x east, y north of the parent's centre. Rooms stand on the map's 10 ft squares.

- `Design` - the block: `xyz` its place in the region (z its floor), `outline` its ground (`rect W L`, `circle R`,
  `poly …`), `fill` the share the rooms should cover, `facing`/`side` where it keeps to, `width` its passages (5 or 10).
- `Layout` - rooms set against one another and placed as one, by `arrange`:
  - row, column, grid (`cols`): in line; `gap` between them (0 shares walls, with doors).
  - spine: a hall with its rooms down both sides. ring: a hub with its rooms on its eight points; a diagonal room
    of a curved or cornered hub and shape is reached by a straight spoke.
  - split: a dense block, its `width` by `length` cut into rooms of every size sharing walls, a door to each and
    `loops` of the rest. court: rooms round a yard, `depth` deep, a door from each to the next all the way round.
    split and court size their own rooms (each a rect).
  - radial: rooms spread evenly round a hub over `sweep` degrees about `bearing`, each on its own straight spoke.
  - cluster (where unset): each room set against one already placed.
  `entry` is the room a route to the layout reaches, and a spine's hall or a ring's or radial's hub.
- `Room` - a location, opening with its code; or rooms no location holds, opening with the block's id, with `count`.
  Each of those is a part of the location it opens off - the nearest reached through such rooms - labelled with that
  code and a letter (M.53a), written by `accept` as a `Part` line and by step 4b as a Feature of that location's
  write-up. No route names a part: only its location's own doors lead to it.
  `layout`, `width`, `length`, and `xyz` or `facing`/`side` within its parent. `shape`: rect, hall, round, oval,
  octagon, hexagon, diamond, cave or organic (rough and smooth irregular), apse (rounded at the end away from its
  facing), ell, cross or irregular (cut back at its corners, the same way each time for the same room). A door
  stands only on a straight stretch of wall: a curved room shares no wall with another, and is met near a side's middle.
- `Route` - a way with two or more `ends`. An end is a location, a layout, the block itself (a way off the map at
  its edge) or a location of another block (a passage toward it, or a stair where its floor is higher or lower).
  `:facing` after an end is the wall it leaves by - a layout's or block's outermost on that side - and `:side` the
  half of it. `length` is short, long, a count of 10 ft squares, or `"N feet"`, of the first two ends; a further end
  branches off the passage. `kind=door` sets the first two ends against one another, a door in their shared wall.
  `door` gives each end's door, one kind or one an end. `style=natural` gives it rough walls. `line=straight` between
  two edges of the block is a cleft, laid before any room: rooms keep off it and passages cross it.
- `Void` - ground no room or passage takes.

Passages run on the 10 ft squares, straight or on the diagonal where that is shorter, never cutting a room's
corner; `diagonals=no` on the Design, or `diagonal=no` on a Route, keeps them to straight runs.

The examples in `examples/` are each solved by the validator: start from the one closest to the level.

## Order

1. Write the plan from the region's brief node and `Seed.md`; `python3 tools/plan.py draft [Code]` writes a first
   one from tables that already stand. `python3 tools/plan.py solve --file F.md` tries a
   plan outside the setting; `python3 tools/design.py solve [Code]` solves the region's and draws it.
2. Read the report: `UNROUTED` and `goal missed` lines say what to change - a larger outline, a facing that
   fights another, a length the ground cannot give. A note says which goals were set aside to route every way.
3. Show the user the drawing; `python3 tools/design.py accept [Code]` writes the `Place`, `Link` and `Part` lines.
   Once approved the plan is solved again exactly as accepted, and `python3 tools/plan.py apply [Code]` writes its
   places into the tables at 4a.
4. A stair's room is held over the room it meets on a placed level. Plan the first level of a chain with `--free`,
   then place its neighbours from it.
