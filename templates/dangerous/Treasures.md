# Treasures.md - DANGEROUS

## Purpose
What one DANGEROUS region holds to be taken, `setting/region/[Region Code]/Treasures.md`:
every treasure, and every key and piece of lore lying in it, one row each.

## Context
Read first:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- this region's Overview, `setting/region/[Region Code].md` - its Loot
- the headings of `setting/Treasure1.md`-`setting/Treasure5.md`, for what each table holds
- `patterns/dangerous/Treasure.md`, and the files it draws
- this file's stub rows, and the `Challenges.md` rows a Guard names

A row's place is its `Location` code and that location's § Location row. Nothing else of
the place is read.

## Instructions
- Which places get a row, and every tag on it, was settled at allocation, so this pass
  writes every empty cell of every stub no composition has claimed, and never re-decides
  a tag. The format is `templates/region/Allocation.md`'s.
- A row naming a registry entry - its Keys row, Lore row or Unique - cites the stub
  allocation wrote; what the entry means is written into the registry later, not here.
- Every row is written in view of the others. Across the region, the treasure rows lean
  on the tables the Overview's Loot says they do.

## Template
```
# Treasures of [Region Code] [Region Name]

## Treasure
| ID | Location | [patterns/dangerous/Treasure.md's labels] | Realized |

## Key
| ID | [patterns/dangerous/Key.md's labels] |

## Lore
| ID | [patterns/dangerous/Lore.md's labels] |
```
