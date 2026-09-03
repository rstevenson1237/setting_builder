# Outline.md

## Purpose
The setting's shape, fixed before any of its content exists: how many regions, of what
ratings, at what dice, and what altitude the party plays at.

## Context
Consult when drafting:
- `GENRE.md` - the only fixed input; this is the first generated artifact.
- `patterns/setting/Outline.md` - the region mixes, what a die means, and how to state altitude.
- `setting/Procedures.md` - the Difficulty roll and what the location counts derive from.

## Instructions
Fix the region count, the rating mix, a die per region, and party altitude. Everything
downstream scales against this file, most sharply `setting/Bestiary.md`, whose AD spread is
anchored to party altitude.

Start every region at **d8** and move off it for a reason. The die is a difficulty die, not
a power level - see `setting/Procedures.md`.

## Template
```
Outline of [Setting Name]

Regions: [count, and the code range]
[Code] - [SAFE/WILD/DANGEROUS], d[N] - [one clause on what it is for]

Party altitude: [what the characters are, in dice - what they can face, what they must avoid]

Shortest loop: [the one SAFE, one WILD, one DANGEROUS a party can actually run]
```
