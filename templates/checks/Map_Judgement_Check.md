# Map_Judgement_Check.md

## Purpose
A review of each DANGEROUS block's map by eye, for what `tools/validate_setting.py` and
`tools/mapcheck.py` cannot see: whether the drawing reads as the place the tables describe.
Saved as `setting/checks/MapJudgementCheck.md`.

## Context
- `GENRE.md`, `STYLE.md` and `BRIEF.md` - its `pack` lines and each region's outline.
- each DANGEROUS region's seed, `setting/region/[Code]/Seed.md`, its `Dressing.md`,
  `Connections.md` and `Blocks.md`, and its write-ups.
- the maps, drawn by one command, `python3 tools/maps.py draw --out _maps --fit 1600x1600px`,
  each `_maps/[Block].svg` viewed whole; then again with `--fit 110x150mm`, the PDF's size.
- the output of `python3 tools/validate_setting.py`.

## Instructions
Run this once the loop has exited, in a context that drew none of the maps. Record each item
per block as Confirmed or Needs Attention, with a note, in the order below; the Template block
lists the same items in the same order. Every Needs Attention names its likely source: a table
line, a `BRIEF.md` line, a tool (`tools/pack.py`, `tools/route.py`, `tools/dungeon.py`), or
artgen, in the terms of `plans/dungeon-maps/report-artgen.md`.

### Per block

- **Every way reads as itself** - each Connection is a door, arch or passage between the two
  rooms it joins and no others; a locked, secret or trapped way is marked; a way out is a stair
  or arrow inside its room, with its note.
- **Floors read apart** - no two rooms, and no room and passage, read as one floor; a hall reads
  as a room, a passage as a passage.
- **Labels and marks read** - every code, stair and note can be read at both sizes, none laid
  over another or over a wall.
- **Prose follows the map** - each direction a write-up gives that names no location code (an
  arch east, a stair in the north wall) matches the map. The validator checks those that name one.
- **The level keeps its shape** - its square sits in the sequence `BRIEF.md`'s footprints set,
  its stairs stand over the stairs they meet, and its rooms lie as its seed and outline say:
  a central hall central, a far tomb far.
- **It plays** - a party meets choices where the seed implies them: loops, a second way to a
  prize, a dead end where one is meant.

## Template
```
# Map Judgement Check - [Date or revision note]

## Block [Block Code]
- Every way reads as itself: [Confirmed / Needs Attention - way, and its source]
- Floors read apart: [Confirmed / Needs Attention - rooms, and its source]
- Labels and marks read: [Confirmed / Needs Attention - labels, and its source]
- Prose follows the map: [Confirmed / Needs Attention - location, and its source]
- The level keeps its shape: [Confirmed / Needs Attention - note, and its source]
- It plays: [Confirmed / Needs Attention - note, and its source]

[repeat per block]

## Open Items
- [Anything flagged Needs Attention, carried forward as an action item, with its source]
```
