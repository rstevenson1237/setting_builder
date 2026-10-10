# Tables - DANGEROUS

## Purpose
The table files of one DANGEROUS region, `setting/region/[Region Code]/[Table].md`: one
file per table `patterns/Schema.md`'s Dangerous folder names, each holding entries.

## Context
Read first, for every table:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- `patterns/Schema.md`
- this region's Overview, `setting/region/[Region Code].md`

Then, by table:
- **Locations**: this region's die in `setting/region/Regions.md`, `patterns/setting/Naming.md` and `setting/Language.md`.
- **Purpose**: this region's `Locations.md` and `Connections.mmd`.
- **Every other table**: this region's `Locations.md`, `Connections.mmd` and `Purpose.md`, and the setting files `patterns/Schema.md` names for this table's values.

## Instructions
- **Locations** - count and mix, against the region die:
  ```
  count   3x the die
  mix     20% High, 50% Medium, Low the rest
  ```
  Each room's three tags push it away from the region's average room: never its own name,
  never a fact every room in the region shares, and no two rooms carrying the same three.
- **Purpose** - every other table's entries at a High room are written toward it, and a
  room its `signs` names carries that sign in its own Dressing or Challenges.
- **Every other table** - each room gets the entries its type's `rate` line gives. A
  percentage is rolled per room, never chosen.
- **Connections** - one entry per side of every edge in `Connections.mmd`; the two sides of
  one edge share a type.

## Template
````
# [Table] of [Region Code] [Region Name]

```kdl
[Node] [Location Code] [member]=[value] { [Child] [member]=[value] }
```
````
