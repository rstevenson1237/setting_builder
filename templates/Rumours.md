# Rumours.md

## Purpose
A referee-facing table of 20 rumours of varying truth that serve as adventure hooks into the setting.

## Context
Read first:
- `GENRE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- `patterns/setting/Rumours.md`
- `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`

## Instructions
Create a table numbered 1-20 of rumours, each following `patterns/setting/Rumours.md`'s
Spec. The collection as a whole must hold this shape:

```
RUMOURS - a d20 table
  ~35%  True
  ~35%  Partially true
  ~20%  False
  ~10%  Unverified - no answer held; the referee's to settle
  1     At least three pointing at a region, not a detail
  1     At least two that are true and sound false
  1     At least one that is false and sounds unmistakably true
```

**Settled at** names where a party finds out - the Location Code, or codes, holding what
confirms, denies, or corrects this rumour. It is written in two phases like every other
registry: left as `[pending 5c]` while the table is authored at 2d, since no location
exists yet, and filled at step 5c against the locations actually built. For a `P` entry it
also names **which half is false**, in a clause, because "partially true" without that is
a mark the referee cannot act on.

A rumour that points off the map says so - `Settled at: nowhere on this map` - which per
STYLE.md's state-the-nil is a decision on the page. Without it, a deliberate lead beyond
the edge of the setting and a dangling reference to something nobody ever wrote read
exactly alike.

This column is referee-side, exactly as the truth mark is, and is never shared. It records
where the truth is, not what the party should do about it - per
`patterns/setting/Rumours.md`, a rumour is a lead and not an instruction.

## Template
```
Rumours of [Setting Name]

| # | Rumour | T/P/F/U | Settled at |
|---|--------|-------|------------|
| 1 | [A rumour the players might encounter] | [T/P/F/U] | [Location Code(s), and for P which half is false; for U, the referee's, and where a party would look] |
| 2 | [A rumour the players might encounter] | [T/P/F/U] | [...] |
| ... | ... | ... | ... |
| 20 | [A rumour the players might encounter] | [T/P/F/U] | [...] |
```
