# Bestiary.md

## Purpose
Reusable, system-neutral creature templates for the setting.

## Context
```kdl
template scope="setting" writes="setting/Bestiary.md" shape="Bestiary"
read "setting/Setting.md"
read "setting/History.md"
read "setting/Truths.md"
field "Bestiary.Description" sentences="3-4"
```

## Instructions
Each entry is one record following its fields in `patterns/Setting_Schema.md`.

Write the entries `BRIEF.md` asks for up front, in its mix and AD spread. The Bestiary then
grows as the build needs it: a location or region seed that needs a creature the Bestiary
lacks adds its entry here first, then cites it.

Write `Description` as one paragraph for the referee, in this order: what reaches a party before the
creature does, what they see, where it lives and what it eats, what it does on being met. It
leaves `Numbers`, `AD` and `Special` to their own fields.

Cut any field the schema does not name.
