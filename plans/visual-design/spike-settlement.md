# Spike - can a SAFE or WILD block be solved like a level?

Question (implementation T6): design a settlement block with locations as building footprints and
ways as streets, solve it with `dungeon layout`, and see whether the picture is one a referee
would use. Done in a scratch folder on region A's block `A.a` (WILD, nine locations); nothing in
the setting changed.

## What was done

- A graph from `A.a`: each location a room at its `Dressing` width and length, on the 5 ft grid
  (A.5 is 120 by 25, A.4 90 by 70, A.9 20 by 15), and eight ways as streets, each with the bearing
  the table gives (the statues A.1 as the hub; the temple A.6 to the scouts' camp A.7; the house
  A.2 to the cellar A.9; the dry canal A.8 west of the hub).
- `dungeon layout --graph` over seed 1, twelve packings, `fill` and `detour` set, `passages` 1.0.
- The result turned into a settlement file the way `maps.settlement_map` does: rooms as buildings,
  each passage's `port`, `via` and `port` as a street, the canal as a wide street. It passes
  `artgen settlement check` and renders.

## What worked

- The graph is the one `design.py expand` already writes; no change to the engine call.
- The solver routed every way (`left` empty) and the footprint, `fill`, `detour` and seed all
  applied.
- The file is a valid settlement and renders in the house look.

## What did not

| | Run 1: footprints as given | Run 2: each grown by one street width, drawn inset |
|---|---|---|
| Streets | 2 of 8 ways are passages; the other 6 are "doors through a shared wall", which a building has no use for | 3 of 8; the rest are rooms that happen to touch |
| Spacing | buildings wall to wall | a street-width gap, but between touching pairs only |
| Spread | all nine within a 300 ft square | within 430 ft |
| `passages` 1.0 | ignored (2 of 8) | ignored (3 of 8) |

- **The table says otherwise.** A.a places its locations 120 to 330 yards from the statues, 360 to
  1000 ft. A solver that packs rooms close in a footprint cannot hold that; asking for it means a
  footprint of 1200 ft and a fill of two percent, where the annealer has nothing to pull the rooms
  together or apart.
- **A street is not a way.** The engine routes a passage between two rooms and draws a corridor.
  A settlement's streets run past many buildings, bend, end at a gate; the graph has no road, no
  gate and no wall. The canal, a Route, came out a long room laid across the hub.
- **What a settlement block needs, `maps.enclosure` and `settlement_map` already derive from
  places**: the wall round the buildings, the gates, the market's yard, the water. A solver that
  moved the places would move them with it, and none of it is in the graph.
- **There is no SAFE region in this build.** Both settlements are WILD ruins whose landmarks are
  placed by bearing and distance across open ground.

## Picture

`spike-settlement-1.png` (footprints as given) and `spike-settlement-2.png` (grown by a street
width). Both are `A.a` at seed 1 in the colour theme.

## Recommendation

**(b) SAFE and WILD designs state fixed geometry and are not solved.** The design for such a block
lists each location's place (`Place`), its streets as ways, and its voids; `design.py` has no
`solve` for them, the user's pick is the geometry itself, and the validator still holds the tables
to it. Reasons: the solver compresses what the tables spread; a street is not a way the engine
knows; and nothing in the pilot needs it. A settlement solver is a request to artgen (report R8:
a settlement laid out from a graph, with roads, gates and a wall), after which (a) can be taken
up.
