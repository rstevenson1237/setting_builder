# LocalProcedures.md

## Purpose
A registry of procedures that belong to a place - a forage table, a game played at an inn,
a rule a crossing adds to a standing move. Each extends one move or procedure of the
ruleset and `setting/Procedures.md`, and is never a second way to do what they already
settle. Each entry is written from the table entries naming it.

## Context
Read first:
- `GENRE.md`, `STYLE.md` and `BRIEF.md`, as `python3 tools/validate_setting.py --brief setting` prints it
- `patterns/Common_Schema.md` and `patterns/Setting_Schema.md`
- `setting/Setting.md`, `setting/Procedures.md`
- the seed of each region holding the table entries naming it, `setting/region/[Region Code]/Seed.md`
- every table entry naming it

## Instructions
Write each entry a table names and this file lacks, per `patterns/Setting_Schema.md`, with its
Found at the locations naming it. `Extends` names what it plugs into and the entry adds only
what the place changes. A table's Results are rows `1` to its die; a contest or variant's are
the ruleset's three results, one line each. Stakes and prices are in cn. The Tell is
something a party can see, hear or be told, never an instruction to play.

## Template
```
Local Procedures of [Setting Name]

### [Name]
Kind: [PROC_KIND]
Extends: [EXTENDS]
Found at: [Location Code] [Location Name]
Roll: [Combat, Skill, Magic, Difficulty or d6] - [whose it is, and what it decides]
Stakes: [what a party risks and what it can win, in cn]
Results:
- [row or result]
Tell: [what shows a party it can be done here]
```
