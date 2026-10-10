# Tables - DANGEROUS

## Purpose
The table files of one DANGEROUS region, `setting/region/[Region Code]/[Table].md`: one
file per table `patterns/Schema.md`'s Dangerous folder names, each holding entries.

## Context
Read first, for every table:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md`
- `patterns/Schema.md`
- this region's Overview, `setting/region/[Region Code].md`

Then, by table:
- **Locations**: this region's die in `setting/region/Regions.md`, `patterns/setting/Naming.md` and `setting/Language.md`.
- **Purpose**: this region's `Locations.md` and `Connections.mmd`.
- **Every other table**: this region's `Locations.md`, `Connections.mmd` and `Purpose.md`, and the setting files `patterns/Schema.md` names for this table's values.

## Instructions
- **Locations** - count and mix, against the region die - defaults, which `BRIEF.md` or
  the user's own request replaces:
  ```
  count   3x the die
  mix     20% High, 50% Medium, Low the rest
  ```
- **Purpose** - a room's other entries are written toward its Purpose, and a room its
  `signs` names carries a sign of it.
- **Every other table** - each room gets the entries its type's `rate` line gives; a
  percentage is rolled per room.
- **Connections** - one entry per side of every edge in `Connections.mmd`.

## Template
````
# [Table] of [Region Code] [Region Name]

```kdl
[Node] [Location Code] [member]=[value] { [Child] [member]=[value] }
```
````
