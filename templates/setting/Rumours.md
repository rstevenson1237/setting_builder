# Rumours.md

## Purpose
A referee-facing table of rumours of varying truth that serve as adventure hooks into the setting.

## Context
Read first:
- `GENRE.md`, `STYLE.md` and `BRIEF.md`, as `python3 tools/validate_setting.py --brief setting` prints it
- `patterns/Common_Schema.md` and `patterns/Setting_Schema.md`
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`
- each region's seed, `setting/region/[Region Code].md`
- the location entries and write-ups each rumour is settled at

## Instructions
Create a table of rumours, numbered to the die `BRIEF.md` sets, each following
its fields in `patterns/Setting_Schema.md`, marked T, P, F or U in the shares `BRIEF.md` sets.

**Settled at** names where a party finds out - the Location Code, or codes, holding what
confirms, denies, or corrects this rumour, filled from what that location holds. For a `P` entry it
also names **which half is false**, in a clause, because "partially true" without that is
a mark the referee cannot act on.

A rumour that points off the map says so - `Settled at: none` - a decision on
the page. Without it, a deliberate lead beyond
the edge of the setting and a dangling reference to something nobody ever wrote read
exactly alike.

This column is referee-side, exactly as the truth mark is, and is never shared. It records
where the truth is, not what the party should do about it - per
`patterns/Setting_Schema.md`, a rumour is a lead and not an instruction.

## Template
```
Rumours of [Setting Name]

| # | Rumour | T/P/F/U | Settled at |
|---|--------|-------|------------|
| 1 | [A rumour the players might encounter] | [T/P/F/U] | [Location Code(s), and for P which half is false; for U, none, and where a party would look] |
| 2 | [A rumour the players might encounter] | [T/P/F/U] | [...] |
| ... | ... | ... | ... |
| [N] | [A rumour the players might encounter] | [T/P/F/U] | [...] |
```
