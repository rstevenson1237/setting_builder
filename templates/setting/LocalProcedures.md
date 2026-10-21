# LocalProcedures.md

## Purpose
A registry of procedures that belong to a place - a forage table, a game played at an inn,
a rule a crossing adds to a standing move. Each extends one move or procedure of the
ruleset and `setting/Procedures.md`, and is never a second way to do what they already
settle. Each entry is written from the table entries naming it.

## Context
```kdl
template scope="setting" writes="setting/LocalProcedures.md" shape="Local Procedures"
read "setting/Setting.md"
read "setting/Procedures.md"
read "setting/region/[Region Code]/Seed.md" part="each region holding an entry naming it"
read naming="Local Procedures"
```

## Instructions
Write each entry a table names and this file lacks, per `patterns/Setting_Schema.md`, with its
Found at the locations naming it. `Extends` names what it plugs into and the entry adds only
what the place changes. A table's Results are rows `1` to its die; a contest or variant's are
the ruleset's three results, one line each. Stakes and prices are in cn. The Tell is
something a party can see, hear or be told, never an instruction to play.
