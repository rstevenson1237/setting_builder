# Report 2 - artgen: where the dungeon and settlement engines cost their consumers

Observed against artgen-maps 0.11.0 (vendored in `tools/artgen`), driving it from `tools/maps.py`
for packed dungeon levels and for wild regions drawn as settlements. artgen is ours to change
(`plans/sheet-maps/intake.md`), so each finding says what a consumer had to build to work around it.
Findings are from renders and file edits, not from reading the engine's design intent; anything not
isolated is marked.

## Consumer code that exists because of artgen's gaps

| Gap | Consumer workaround | Size |
|---|---|---|
| No layout from a graph | `pack.py` (annealing, repair loop, label spacing, turns, nesting, ground) | 432 lines |
| No obstacle-aware corridor router | `route.py` (lattice A*, wall clearance, sharing, noise, named walls) | 515 lines |
| Geometry not exposed | `mapcheck.py` (rebuilds floor, ports, via, slanted runs, doors) | 284 lines |
| No in-room exit | symbol + note + angle placement in `block_map` | about 40 lines |
| Ports run through the room's anchor (A13) | a hub and lead points per room, written into `via` | about 50 lines |
| Room shapes fixed in cells (A15) | every shape but rect, circle and cave written as a `poly` | about 20 lines |

## Findings

### A1. Adjacent floors merge unless two rooms touch and shared walls are on
A floor union is drawn with a wall only where floor meets rock. Test (three rooms, two touching):
- no connections, setting automatic: one merged floor;
- `style.sharedWalls: true`: a wall along each shared edge, no door;
- one connection, setting automatic: wall plus a door where the connection is.
A corridor laid along a room's wall gets no wall at all: partitions are computed only between two
rooms (`sharedEdges` over room outlines). Consequence: the router had to forbid any corridor cell
against a room except at its own door, costing a 10-ft rock band round every room: G measured 34% room
with touching banned and 43% with it allowed. Option: draw a partition wherever two distinct units (room, corridor) are
adjacent except at a declared opening.

### A2. `sharedWalls` defaults on a side effect
`sharedWallsOn = style.sharedWalls ?? !!(connections.length || blocks.length)`. A map whose ways are
all corridors has no `connections`, so the setting is off; touching rooms then merge, silently.
`check` does not warn. Option: default on; and a `check` warning "rooms X and Y touch and will merge".

### A3. Room labels cannot move and only some labels avoid collisions
A room's number badge and code are drawn at the room's centre (`g.cx, g.cy`). The label placer
(`placeLabels`) treats room labels and symbols as obstacles, but only for overlay notes, and only
when rendering with `--fit` (page scale). Room labels are not placed, not checked, and not reported:
`unplaced` lists only overlay labels. Evidence: two adjacent 10-ft halls had overlapping labels; a
stair mark in a 10 x 20 ft room sat on its own room's label. Option: `rooms[].labelAt` (side or
offset), room labels as placeable items, and `check`/`facts` reporting room-label overlaps.

### A4. No way to say "this room has a stair"
A way out of a map exists only as a corridor to a point with `exit.text`, drawn to the map edge.
A stair inside a room is a free `symbol` plus a separate `label`, each positioned by the consumer, with
`angle` semantics that are undocumented (degrees, 0 = east, clockwise: inferred from a render, not
from the source). Consequence: stairs sat at the map edge until the consumer composed its own.
Option: `rooms[].exits: [{side | at, kind: stairs-up|stairs-down|arrow, text}]`, drawing mark and
note and placing the note clear.

### A5. Corridor geometry and door positions are opaque
`dungeon facts --json` returns each corridor's ends and length, each room's box and doors, overlaps,
and unreached rooms. It does not return the corridor path, the position of each door on its wall,
a floor ownership grid, or which room pairs are adjacent. A consumer that wants to answer "does this
door stand on a wall between two floors?" has to rebuild the floor from the file, as `mapcheck.py`
does, by re-deriving port positions (`sidePort`: `offset` is cells from the room's x or y, snapped
by corridor width when no offset is given). That copy can drift from the engine. Option: `facts`
returns `path`, `doors[{at, wall: [a, b]}]`, `floor` (cell to owner) and `adjacent[{a, b, along}]`.

### A6. `check` finds some defects and not the ones that matter most
Reported: corridors running through a room, crossing without a junction, labels left unplaced,
overlaps, unreached rooms. Not reported: a door standing in open floor or rock; a corridor along a
room wall (A1); touching rooms with shared walls off (A2); two doors stacked; a way with no passage.
The first and fourth are the "doors in open rooms" class. All of them are properties of data artgen
already holds. Option: add them as `check` warnings with stable ids so consumers can promote them to
errors.

### A7. Corridor routing has hints, not a router
`route` takes `auto | hv | vh | straight | around`, plus `via` waypoints. `around` produced
through-room and crossing warnings that the consumer then patched by dropping `side`/`offset`
(this also left an `offset` without a `side`, a file error, until patched). The consumer wrote an
A* router. Related corridors that merge on purpose (two ways leaving one room) trigger "crosses
corridor with no junction (the floors join there)" although the junction is intended; an endpoint of
the form `{corridor: id}` exists but nothing builds a junction automatically.
A router a consumer would now also need: a door at a named point on a wall, a slanted run from a
curved or diagonal wall onto the grid, ground the route must stay on, and related corridors that
may join and part but not run side by side.
Option: `link --route maze` with clearance, bend cost, share-with-siblings and a seed; and treat
related corridors' overlap as a junction.

### A8. The generator makes layouts, not layouts to a brief
`dungeon gen --layout scatter|dense|blocks` places random rooms. There is no input for "these rooms,
at these sizes, joined as this graph, inside this footprint". `pack.py` supplies that: energy terms
for overlap, touching, face-to-face alignment, door-versus-passage mix, round-room clearance,
label spacing and shared wall between floors; moves that turn, mirror and nest rooms; a repair loop
that re-anneals round ways that found no passage or detour; ground bounded by an outline and keep-out
areas; and a square sized from a target fill. It runs about 30 s in Python on four cores; the same search in the engine would be
faster and shared by every consumer. Option: `dungeon layout --graph g.json --footprint square|poly
--keep-out poly --fill 0.45 --passages 0.35 --seed n`, returning a map file.

### A9. Rock rendering has two modes and neither suits a dense level
`hatch: band` leaves white voids inside a dense map that read as unmapped space; `full` fills the
whole map with the hatch, which is heavy at page scale. The old reference maps use a solid ground
colour with white floors. Option: `style.rock: hatch | solid | none` and a colour setting.

### A10. One wall weight for outlines and partitions
`style.wall` is a single factor. The default reads as a hairline for a partition at fit size; a
factor of 2.5 was needed for shared walls to read, which also thickens outlines. Option: a separate
`partition` weight, or weights that scale with page scale.

### A11. Limits and units push work onto the consumer
`cols` and `rows` are capped at 240 cells; a wild region 2,000 ft across needed 10-ft cells to fit.
Corridor `width` is in cells, so a 10-ft passage is 2 on a 5-ft grid and 1 on a 10-ft grid and the
consumer converts. The settlement overlay rejects a `water` label kind (`name | note | area | street`
only) although `map` accepts it, which a consumer learns from a validation error.

### A12. The settings are discoverable only by reading the bundle
`--help` omits `style.sharedWalls`, `style.wall`, `style.hatch`, `corridor.via`, `offset` as a JSON
key and `exit`. `check` reports errors by path, which helps, but there is no schema export and no
reference. Every one of A1-A3 was found by experiment. Option: `artgen schema dungeon|map|settlement`
(JSON Schema) and one reference page per engine with an example per key.

### A13. A port runs through the room's anchor
A port `{room, side, offset}` starts at the anchor's row or column (`sidePort`: `[along, g.cy]` or
`[g.cx, along]`) and runs out through the wall. `{room}` with no side starts at the anchor itself. A
poly room's anchor (`roomAnchor`) is a point within 1.5 cells of no wall, nearest the box's centre.
In an L, nothing keeps it in the part that sees every wall, so a port to the far arm crosses the
notch and draws a passage over rock. If the path's first point is outside the outline, `exitPoint`
returns null and no door is drawn, with no warning. A `{at: [x, y]}` end can start at the wall,
but it drops the room: `render --room` no longer crops round it and `facts` no longer counts it.
The consumer finds the point that sees every wall, clear of walls by half a passage, and writes
`{room}` with that point and one just inside the door at the head of `via`.
Option: `{room, at: [x, y]}`, a port at a point on the wall that keeps the room link; or
`rooms[].anchor`; and a `check` warning where a port's first point is outside its room.

### A14. A door is set square to the path, not to the wall
A door takes the angle of the path segment that crosses the outline (`exitPoint`). On a straight
wall the routes cross square, so this holds; on a round or octagonal wall, a door is flush only
where the path crosses along the radius. The consumer arranges that, running the last stretch from
the room's hub to the first cell of the grid. Option: set a door along the outline's tangent at the
crossing.

### A15. Room shapes are fixed in cells, and the dungeon has no hexagon
An octagon's cut is `round(min(w, h) * 0.3 * 2) / 2` cells, so its walls move with `perCell` and
snap to half cells, and a consumer routing in feet cannot predict them. `rooms[].shape` takes `rect`,
`circle`, `octagon`, `cave` and `poly`; a hexagon exists only through `block add`, as a poly. The
consumer draws every other shape as a `poly` of its own outline in feet. Option: shapes defined in
map units with stated proportions (an octagon's cut as a ratio), `hexagon` with an orientation in
`rooms[]`, and the formulas in the reference (A12).

### A16. A level has no outline and no keep-out areas
A dungeon map has no polygon for the ground a level occupies, nor for rock within it (a shaft, a
collapse). Rock is hatched everywhere outside the floor, so a level's outline is not drawn, and a
keep-out area shows only as an overlay note at its centre. Option: `bounds` (a polygon the hatch and
grid are clipped to, its edge drawn) and `areas: [{points, kind: rock | void, label}]`.

### A17. Not isolated
- Whether `dungeon sync` preserves stale fields when an entry's end changes from a side port to a
  waypointed one: files were deleted and regenerated instead of tested.
- Whether a missing partition between touching rooms (seen once, between rooms meeting at a partial
  overlap, in a layout that was not kept) is an engine fault or a consequence of corner meetings.
  A fresh test of partial overlaps drew complete walls.
- Whether a door wider than its wall is drawn whole. One pack failed the consumer's door test where
  a 10-ft passage met the end of a 6-ft hall, and the layout was not kept to retest.
- Whether a poly's winding matters. A mirrored L drew a broken wall at its inner corner; the cause
  was the consumer's port through that corner (A13). The consumer writes every poly clockwise
  anyway, and artgen with an anticlockwise poly was not tested on its own.

## What worked and should be kept
- `corridor.via` and port `offset`: enough to draw any orthogonal route exactly.
- A slanted first segment from `{room}`: a door off the grid, on a round or octagonal wall, comes out
  flush when the segment runs along the radius.
- `poly` rooms with `sharedWalls`: walls and openings along a shared straight edge, as for rects.
- Two corridors that share cells draw as one floor, so a junction can be laid by overlap.
- `style.sharedWalls: true` once set: clean walls and doors through shared edges.
- `facts` overlaps and unreached rooms; `render --json` `unplaced`.
- `perCell` freedom and the `underlay` option for settlements over a terrain sheet.
- Deterministic output given a seed; the render cache keyed on file, engine version and arguments.

## Priorities (by consumer cost removed per unit of engine work)
1. A5 + A6: expose geometry in `facts`, add door/adjacency/touching checks. Retires most of `mapcheck.py`.
2. A1 + A2: partition between any two adjacent units; `sharedWalls` default on. Removes the 10-ft
   rock rule and recovers density.
3. A13 + A14: a port at a point on the wall, and doors along the wall. Small, and it retires the hub
   and lead points the consumer writes into every `via`.
4. A3: movable, checked room labels.
5. A12: schema export and a reference page; cheap, and it prevents the rework in report 1, F11.
6. A8 + A7: layout from a graph and a corridor router. The largest piece, and the one that removes
   `pack.py` and `route.py` from the framework.
7. A4, A9, A10, A11, A15, A16: smaller drawing options.
