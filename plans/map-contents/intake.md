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

## What the history holds

| Commit | What it decided | Here |
|---|---|---|
| a50ec14 | Every Feature states "where in the room it sits": the referee had "no way to place a Feature or exit at the table". `templates/region/Location.md` still asks it. | Position is written today, in prose, at step 4b, after the tables. |
| `archive/plans/sheet-maps/brief-symbols.md` (A6) | "Every mark a player or referee must tell apart has its own symbol in the key." | The symbols this plan uses were asked of artgen for that reason. |
| 6b64172 (#92) | Region maps and location cuts were paused, "to restore later". | A location's page has no map of its room. |
| e8b67ef (#107) | The scale, compass and legend stand outside the map; a code labels each room and links to it. | M4 follows it. |
| 8902787 (#116) | Levels became plans. | When the trap and Rock marks stopped being drawn. |

## What the rule cannot do

- Follow the prose. 152 of 407 Features say where their thing sits - under the banner, against three walls, at
  the gate - and 18 of those by compass. A slot chosen by rule is blind to all of it, and the prose is written
  after the tables, so today nothing upstream holds a position for a rule to read.
- Draw what has no symbol: a Mirror, a Fresco, a Tapestry, a Button or Lever, Flooring, and every Encounter.
- Draw furniture a Dressing's `layout` describes in words.

## Found in the work

A plan's map draws no trap on a way and no Rock: the map file the retired `dungeon.block_map` wrote held both,
and `plan.dungeon_file` writes an empty `overlay` and no `areas`.
