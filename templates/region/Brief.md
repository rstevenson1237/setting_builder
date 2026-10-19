# Brief.md

## Purpose
A region's brief, `setting/region/[Region Code]/Brief.md`: a run sheet written once the
region's locations exist. A referee holding it and the seed can run an excursion into the
region without opening a location.

## Context
Read first:
- `GENRE.md`, `STYLE.md` and `BRIEF.md`, as `python3 tools/validate_setting.py --brief [Region Code]` prints it
- `patterns/Common_Schema.md`, and `patterns/Region_Schema.md` - this region's rating's `brief`
- this region's seed, `setting/region/[Region Code].md`
- this region's table files, and each location's referee notes for its size
- `setting/Rumours.md` and `setting/Quests.md`

## Instructions
Write every field of the rating's `brief`, in its order, from the tables alone, and a location's
size from its referee notes. A setting
entry is cited as `(Named Creature: Name)`, `(Faction: Name)` or `(Local Procedure: Name)`.
Every fact about a location names it by code; a count is summed from the entries. Layout
is read from the Locations' `at` and the Connections' `orientation`. A fact no entry holds
is an entry to add to the tables, not a line here. Nothing the seed says is repeated, unless a field folds it in.

## Template
```
[Field]: [prose, short]

[Paragraph field]: [first paragraph]

[next paragraph]

[List field]:
- [Code or codes, Rumour N or Quest Name] - [...]

Tables:
[die, if rolled] [table name]
1. [...]
...
6. [...]
[die] [what is met where nothing is keyed]
1. [...]
...
6. [...]
```
