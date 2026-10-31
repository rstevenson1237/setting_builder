# Bestiary.md

## Purpose
Reusable, system-neutral creature templates for the setting.

## Context
```kdl
template scope="setting" writes="setting/Bestiary.md" shape="Bestiary"
read "setting/Setting.md"
read "setting/History.md"
read "setting/Truths.md"
field "Bestiary.Sight" sentences="1"
field "Bestiary.Range" sentences="1-2"
field "Bestiary.Disposition" sentences="1"
field "Bestiary.Description" from="Bestiary.Sight, Bestiary.Range, Bestiary.Sign, Bestiary.Disposition" sentences="2-3"
```

## Instructions
Each entry is one record following its fields in `patterns/Setting_Schema.md`.

Write the entries `BRIEF.md` asks for up front, in its mix and AD spread. The Bestiary then
grows as the build needs it: a location or region seed that needs a creature the Bestiary
lacks adds its entry here first, then cites it.

Write the other fields first, then `Description`: two or three sentences for the referee that
restate them as one read, in the order a party meets the creature - what reaches it first, what
it sees, where it lives and what it eats, what it does on being met - adding nothing the fields
do not say. The site and PDF show `Description` in place of the fields it is written from.

Cut any field the schema does not name.
