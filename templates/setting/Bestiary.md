# Bestiary.md

## Purpose
Reusable, system-neutral creature templates for the setting.

## Context
Read first:
- `GENRE.md`, `STYLE.md` and `BRIEF.md`, as `python3 tools/validate_setting.py --brief setting` prints it
- `patterns/Common_Schema.md` and `patterns/Setting_Schema.md`
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`

## Instructions
Each entry is one record following its fields in `patterns/Setting_Schema.md`.

Write the entries `BRIEF.md` asks for up front, in its mix and AD spread. The Bestiary then
grows as the build needs it: a location or region seed that needs a creature the Bestiary
lacks adds its entry here first, then cites it.

Cut any field that does not fit the template block below.

## Template
```
Bestiary of [Setting Name]

### [Creature Name]
Type: [Type]
AD: [Xd6+N]
Special: [... or `none` - one Special line per ability]
MA: [Y, omitted at 1]
Description: [...]
Range: [...]
Sign: [...]
Disposition: [...]
```
