# Bestiary.md

## Purpose
Reusable, system-neutral creature templates for the setting.

## Context
```kdl
template scope="setting" writes="setting/Bestiary.md" shape="Bestiary"
read "setting/Setting.md"
read "setting/History.md"
read "setting/Truths.md"
field "Bestiary.Description" sentences="1"
field "Bestiary.Range" sentences="1-2"
field "Bestiary.Disposition" sentences="1"
```

## Instructions
Each entry is one record following its fields in `patterns/Setting_Schema.md`.

Write the entries `BRIEF.md` asks for up front, in its mix and AD spread. The Bestiary then
grows as the build needs it: a location or region seed that needs a creature the Bestiary
lacks adds its entry here first, then cites it.

The site and PDF set the fields the schema's `flow=` names as sentences under the first
one's label, so write each after the first as a clause that reads when joined by semicolons.
Each field's length is its `field` line's.

Cut any field the schema does not name.
