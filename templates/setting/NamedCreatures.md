# NamedCreatures.md

## Purpose
A registry of specific, named creatures that may appear in multiple locations and act on their own motivation, distinct from the reusable templates in `setting/Bestiary.md`. Each entry is written from the table entries naming it.

## Context
Read first:
- `GENRE.md`, `STYLE.md` and `BRIEF.md`, as `python3 tools/validate_setting.py --brief setting` prints it
- `patterns/Common_Schema.md` and `patterns/Setting_Schema.md`
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`
- `setting/Bestiary.md`, `setting/Factions.md`
- every table entry naming it

## Instructions
Write each entry a table names and this file lacks, per `patterns/Setting_Schema.md`, with its
Appears at the locations naming it.

## Template
```
Named Creatures of [Setting Name]

### [Creature Name]
Form: [NAME_FORM, of the name]
Type: [Type]
AD: [Xd6+N]
Special: [what it can do that its Action Dice do not already say, or `none`]
MA: [Y, omitted at 1]
Appears at: [Location Code(s)]
Reacts: [what it does on meeting a party]
Wants: [the standing goal driving this creature]
Knows: [what a party can get from it, if anything]
Description: [1-3 sentences, same style as a Bestiary entry]
```
