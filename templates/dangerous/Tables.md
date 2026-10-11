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
- this region's seed, `setting/region/[Region Code].md`

Then, by step:
- **4a, Locations**: this region's die in `setting/region/Regions.md`, `patterns/setting/Naming.md` and `setting/Language.md`.
- **4c, the stubs**: this region's `Locations.md` and `Connections.mmd`.
- **5a**: this region's `Locations.md`, `Connections.mmd` and `Purpose.md`, the table being filled, and the setting files `patterns/Schema.md` names for its values.

## Instructions
- **4a, Locations** - count and mix, against the region die - defaults, which `BRIEF.md`
  or the user's own request replaces:
  ```
  count   3x the die
  mix     20% High, 50% Medium, Low the rest
  ```
- **4c, the stubs** - every other table, its entries bare: `[Node] [Location Code]`.
  Each room gets the entries its type's `rate` line gives, choosing within a range for a
  reason its tags give. Connections get one entry per side of every edge in
  `Connections.mmd`, with `to` set. A member or child is written now only where the
  design already fixes it.
- **5a, filling** - Purpose first; then each table in one pass, every stub in view. Write
  every member a stub lacks, toward its room's Purpose; a room a Purpose's `signs` names
  carries a sign of it. A stub that will not fit its room is a finding for 5c, never moved
  or dropped here.

## Template
````
# [Table] of [Region Code] [Region Name]

```kdl
[Node] [Location Code] [member]=[value] { [Child] [member]=[value] }
```
````
