# Brief.md

## Purpose
A region's brief, `setting/region/[Region Code].md`: its run sheet, written once its
locations exist and rewritten when its seed or tables change. A referee holding it, with
what the site draws beside it, can run an excursion into the region without opening a
location.

## Context
Read first:
- `GENRE.md`, `STYLE.md` and `BRIEF.md`, as `python3 tools/validate_setting.py --brief [Region Code]` prints it
- `patterns/Common_Schema.md`, and `patterns/Region_Schema.md` - this region's rating's `brief` and `drawn`
- this region's seed, `setting/region/[Region Code]/Seed.md`
- this region's table files and its `Ground.md`

## Instructions
Write every field of the rating's `brief`, in its order, from the seed and the tables
alone. The seed's fields are its nodes as prose, each member once. A list field opens one
`- ` item for each location its `holds=` gives it, in code order, with that code; the
validator names any it holds and lacks. What `drawn` names is never written here.

Every fact about a location names it by code. A fact no entry holds is an entry to add to
the tables, not a line here. A setting entry is cited as `(Named Creature: Name)`,
`(Faction: Name)` or `(Local Procedure: Name)`.

## Template
```
[Region Code] [Region Name]

[Field]: [prose, short]

[List field]:
- [Location Code] - [...]

Tables:
[die, if rolled] [table name]
1. [...]
...
6. [...]
```
