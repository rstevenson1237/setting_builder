# Tables

## Purpose
The table files of one region, `setting/region/[Region Code]/[Table].md`: one file per
table its rating's schema, `patterns/[Rating]_Schema.md`, names, each holding entries.

## Context
Read first, for every table:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md`
- `patterns/Common_Schema.md`, `patterns/Setting_Schema.md` and this region's rating schema
- this region's seed, `setting/region/[Region Code].md`

Then, by step:
- **4a, Locations**: this region's die in `setting/region/Regions.md`, the rating schema's Location and `setting/Language.md`.
- **4c, the stubs**: this region's `Locations.md`, and its `Connections.mmd` where it has one.
- **5a**: this region's `Locations.md`, `Connections.mmd` and `Purpose.md` where it has them, the table being filled, and the setting files `patterns/Setting_Schema.md` names for its values.
- **5d, placing**: this region's table files and `Connections.mmd`, and the setting entries `python3 tools/validate_setting.py --pending` owes to 5d.

## Instructions
- **4a, Locations** - the count `BRIEF.md` sets for the region, in its targets' type mix.
  A name is written with its `form`: `common`, `family`, `epithet` or `tongue`, per
  `patterns/Common_Schema.md`. A tongue or family name is recorded in `setting/Language.md`
  first. The same holds for a Person's name at 5a.
- **4c, the stubs** - every other table, its entries bare: `[Node] [Location Code]`.
  Each room gets the entries its type's `rate` line in `BRIEF.md` gives, choosing within a range for a
  reason its tags give, and toward `BRIEF.md`'s targets. The occupants the seed's Overview
  names are placed as Encounters. Connections get one entry per
  side of every edge in `Connections.mmd`, with `to` set, and a gate the folder's `join`
  line names on the way into a gated location. A member or child is written now only where the
  design already fixes it.
- **5a, filling** - Purpose first, where the folder has one; then each table in one pass, every stub in view. Write
  every member a stub lacks, toward its room's Purpose and `BRIEF.md`'s targets; a room a
  Purpose's `signs` names carries a sign of it. A stub that will not fit its room is a finding for 5c, never moved
  or dropped here.
- **5d, placing** - a lock goes where the design wants a gate: a `Lock` on a Connection or
  a Reward, naming its key. A setting entry is placed where its Found at or Appears at
  names a location whose tables do not yet hold it - a key as a Reward pulling
  `Keys: [name]`. A placed entry holds only what placement fixes; the next 5a fills the rest.

## Template
````
# [Table] of [Region Code] [Region Name]

```kdl
[Node] [Location Code] [member]=[value] { [Child] [member]=[value] }
```
````
