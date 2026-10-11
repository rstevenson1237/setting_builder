# Locations.md - DANGEROUS

## Purpose
The location table of one DANGEROUS region, `setting/region/[Region Code]/Locations.md`:
every room as a row - named, tagged and weighted - and the tables of what each room is.

## Context
Read first, every step:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- this region's Overview, `setting/region/[Region Code].md`, and its die in `setting/region/Regions.md`

Then, by step:
- **4a** (names and tags): nothing more.
- **4b** (weights): what each weight guarantees - `patterns/dangerous/High.md`, `patterns/dangerous/Medium.md`, `patterns/dangerous/Low.md`.
- **4f** (the room tables): the stubs of § High, § Medium, § Low and § Dressing; § Location; `patterns/dangerous/Dressing.md` and the three class files above, for their own lines; the rows a Payload row or Foreshadows names.
- **4g** (naming): `patterns/setting/Naming.md`; `setting/Language.md`; every row in the region naming the location, since a name comes after everything else is decided.

## Instructions

**Count and mix**, set against the region die - defaults, which `BRIEF.md` replaces where
it speaks:

```
DANGEROUS
  count   a collection: 3x the die, which across a full clear burns 3 of the Danger
          track's 6 steps at every die size. A single holding: what the home actually
          contains, usually 5-8, never padded to the multiplier
  mix     30% high, 50% medium, and low the rest - the residue, not a quota
  entrances   1-2 at about 12 locations, 2 at about 24, 2-3 at about 36
```

**Weights** - one per room, in the mix above:
- **low** - connective areas, empty rooms, or areas that contain detail but do not demand action.
- **medium** - one major reactive element, such as a trap, a monster, or a puzzle to solve.
- **high** - an area central to the theme of the region, holding one or more major features.

**Tags** - each room gets exactly three, one or two words each, written for it alone
against the setting's and this region's tag lines, the Region Overview and `BRIEF.md`.
They are the spark the room is later written to, so they push it away from the region's
average room: never the room's own name, never a fact every room in the region shares, and
no two rooms in one region carrying the same three.

**The tables**, each in the format `templates/region/Allocation.md` sets, and filled at
the steps named above:
- § Location - Code, Name, Tags, Weight, Block. Written at 4a with Weight empty; Block is
  the block diagram's at 4c.
- § High, § Medium, § Low - the class files' own lines, one row per room of that weight.
- § Dressing - one row per room.
- § Naming - one row per room.

A pass over these tables writes every room in view, which is where the constraints that
range over a block - a purpose not repeated within one, per `patterns/dangerous/Dressing.md`
- are kept.

## Template
```
Locations of [Region Code] [Region Name]

## Location
| Code | Name | Tags | Weight | Block |
|---|---|---|---|---|
| [Region Code].1 | [Location Name] | [tag], [tag], [tag] | [high/medium/low] | [Block Name] |

## High
| Code | [patterns/dangerous/High.md's labels] | Realized |

## Medium
| Code | [patterns/dangerous/Medium.md's labels] | Realized |

## Low
| Code | [patterns/dangerous/Low.md's labels] | Realized |

## Dressing
| Code | [patterns/dangerous/Dressing.md's labels] |

## Naming
| Code | [patterns/setting/Naming.md's labels] |
```
