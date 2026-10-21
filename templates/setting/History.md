# History.md

## Purpose
Records the major events that have shaped the setting, oldest to newest.

## Context
```kdl
template scope="setting" writes="setting/History.md" shape="History"
read "setting/Setting.md"
read naming="History" once="written"
run "--location [Location Code]" once="written"
```

## Instructions
List the events `BRIEF.md` asks for, each following its fields in `patterns/Setting_Schema.md`,
oldest to newest, one record each. A later step adds an event only where it needs one to
account for something it wrote. With none asked for, the file is its header line.

An event's Codes are the locations whose Dressing names it in `left`, each showing its Left mark.
