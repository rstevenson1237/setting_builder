# Lore.md

## Purpose
A registry of written works discoverable within the setting - books, scrolls, tapestries, notes, correspondence, maps, and the like - that reveal purpose behind a region, connect its History and Truths, and offer adventure hooks. Each entry is written from the table entries naming it.

## Context
```kdl
template scope="setting" writes="setting/Lore.md" shape="Lore"
read "setting/Setting.md"
read "setting/History.md"
read "setting/Truths.md"
read "setting/Rumours.md" once="written"
read "setting/Quests.md" once="written"
read naming="Lore"
```

## Instructions
Write each entry a table names and this file lacks, per `patterns/Setting_Schema.md`, with its
Found at the locations naming it. Once Rumours and Quests are written, bring each entry's Text
in line with them and with History and Truths: a hook, a dating or a contradiction names the
thing it points at, not a stand-in.
