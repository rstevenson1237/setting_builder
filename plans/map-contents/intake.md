# Intake - map contents: what a room holds, drawn in it

## The request, verbatim

> Currently the design struggles with routing rooms let alone room contents, do we think precise placement is
> reasonable for 4?

## How it is read

The review proposed drawing a symbol for what a room holds, and an optional `at` on an entry. The question is
whether that needs each thing placed precisely, by a solver that already has trouble with rooms and routes.

## The answer

No, and it needs no solver. `prototype/symbols.py` reads a block's map file and its Challenges and Rewards and
gives each Mystery, Hazard and Reward the artgen symbol its type names, in one of nine slots in its room -
the centre and the eight compass points, set in from the walls - by three rules: a Mystery takes the centre, a
Hazard the slot nearest the room's first door, a Reward the free slot farthest from every door. A room one
passage wide uses the three slots along it.

| Block | Symbols | `dungeon check` errors |
|---|---|---|
| C.a | 4 | 0 |
| E.a | 11 | 0 |
| G.a | 24 | 0 |

`prototype/E.a.png` and `prototype/G.a.png` are the drawings: coffins in the tombs, the altar in the rites hall,
a pit at the chapel's door, chests away from the doors. Nothing in the tables changed and nothing was placed by
hand. Routing is untouched: the symbols are laid over a map that is already solved.

## What the rule cannot do

- Say where the prose says. A write-up naming a wall ("a casket set in the north wall") can disagree with a
  slot chosen by rule. A search for a named wall, end, side or corner finds 7 of 407 Features placing their thing by compass.
- Draw what has no symbol: a Mirror, a Fresco, a Tapestry, a Button or Lever, Flooring, and every Encounter.
- Draw furniture a Dressing's `layout` describes in words.

## Found in the work

A plan's map draws no trap on a way and no Rock: the map file the retired `dungeon.block_map` wrote held both,
and `plan.dungeon_file` writes an empty `overlay` and no `areas`.
