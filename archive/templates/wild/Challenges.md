# Challenges.md - WILD

## Purpose
Everything in one WILD region that stands between a party and what it wants,
`setting/region/[Region Code]/Challenges.md`: every creature, hazard and mystery its places
hold, one row each.

## Context
Read first:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- this region's Overview, `setting/region/[Region Code].md` - its Inhabitants and Terrain
- the `setting/Bestiary.md` entries the stubs name
- `setting/Procedures.md` - the forced-damage tiers a hazard's Damage cell names
- `patterns/wild/Creature.md`, `patterns/wild/Hazard.md`, `patterns/wild/Mystery.md`
- this file's stub rows

A row's place is its `Location` code and that location's § Location row - name,
classification, tags. Nothing else of the place is read.

## Instructions
- Which places get a row, and every tag on it, was settled at allocation, so this pass
  writes every empty cell of every stub no composition has claimed, and never re-decides
  a tag. The format is `templates/region/Allocation.md`'s.
- Every row of a table is written in view of the others. Across the region the creature
  rows add up to the Overview's Inhabitants, and no two hazards share a Mechanism and a
  Warning.

## Template
```
# Challenges of [Region Code] [Region Name]

## Creature
| ID | Location | [patterns/wild/Creature.md's labels] | Realized |

## Hazard
| ID | Location | [patterns/wild/Hazard.md's labels] | Realized |

## Mystery
| ID | Location | [patterns/wild/Mystery.md's labels] | Realized |
```
