# Truths.md

## Purpose
Establishes the unique truths that separate this setting from a generic instance of its genre.

## Context
```kdl
template scope="setting" writes="setting/Truths.md" shape="Truths"
read "setting/Setting.md"
read "setting/History.md"
run "--location [Location Code]" once="written"
field "Truths.Codes" from="Truths.Handle"
```

## Instructions
List the truths `BRIEF.md` asks for, each following its fields in `patterns/Setting_Schema.md`.
With none asked for, the file is its header line.

A standing mystery or a gap left for the referee may be listed here whether or not the
file is otherwise asked for; it is the place such a decision is written down.

A truth's Codes are the locations that deliver it.
