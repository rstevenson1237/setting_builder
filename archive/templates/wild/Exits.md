# Exits.md - WILD

## Purpose
What each way between two locations of one WILD region physically is,
`setting/region/[Region Code]/Exits.md`: one row per edge of the region's diagrams.

## Context
Read first:
- `GENRE.md`
- `STYLE.md`
- `BRIEF.md` - this build's design requests, which replace this template's defaults where they speak
- this region's Overview, `setting/region/[Region Code].md`, and its Connections.mmd
- `patterns/wild/Exit.md`
- this file's stub rows, and `Locations.md`'s § Location and § Dressing rows for both ends of each - where an exit sits is a fact about both rooms

## Instructions
- One row per diagram edge, created at allocation with its Kind read off the edge and its
  gate decided once for the edge, so each way through is drawn once rather than once from
  each side. The format is `templates/region/Allocation.md`'s.
- An exit is connected: it is written once both its ends have their rooms' tables filled,
  which for an edge into another region means once that region is too.
- Write every empty cell; never re-decide a tag allocation settled.
- Every exit of one location is written in view of the others, which is where a pattern
  constraint ranging over a location's or a block's exits is kept.

## Template
```
# Exits of [Region Code] [Region Name]

## Exit
| ID | From | To | [patterns/wild/Exit.md's labels] | Realized |
|---|---|---|---|---|
| EX1 | [Location Code] | [Location Code, or plain terms] | [tag] | |
```
