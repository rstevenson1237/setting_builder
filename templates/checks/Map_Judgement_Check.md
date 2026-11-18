# Map_Judgement_Check.md

## Purpose
A review of every block's map and every sheet by eye, for what `tools/validate_setting.py` and
artgen's `check` cannot see: whether the drawing reads as the place the tables describe.
Saved as `setting/checks/MapJudgementCheck.md`.

## Context
- `GENRE.md`, `STYLE.md` and `BRIEF.md` - each region's `design` line, its `footprint` and its outline.
- each region's seed, `setting/region/[Code]/Seed.md`, its `Design.md`, `Dressing.md`,
  `Connections.md` and `Blocks.md`, and its write-ups.
- the maps, drawn by one command, `python3 tools/maps.py draw --out _maps --fit 1600x1600px`,
  each sheet and each `_maps/[Block].svg` viewed whole; then again with `--fit 110x150mm`, the PDF's size.
- the output of `python3 tools/validate_setting.py`.

## Instructions
Run this once the loop has exited, in a context that drew none of the maps. Read each block's
map for the items below, and each sheet for the last. Record findings only, each with a note
and its likely source: a table line, a `BRIEF.md` line, a design or plan line, a tool
(`tools/maps.py`, `tools/plan.py`), or artgen, sent upstream as the `setting-maps` skill says.
A block with no finding is named in the Confirmed line. A finding a tool could make - a count,
an overlap, a missing citation - is also listed under Owed to a tool.

### Per block

- **It is what its seed says** - the map shows what the seed says is there: streets, a wall,
  the thing the block is named for.
- **Every way reads as itself** - each Connection is a door, arch, passage, street or path
  between the two places it joins and no others; a locked, secret or trapped way is marked; a
  way out is a stair, gate or arrow inside its place, with its note.
- **Floors read apart** - no two places, and no place and way, read as one floor; a hall reads
  as a room, a passage as a passage.
- **What a party walks on is drawn** - between two places a party can reach, the ground it
  crosses is on the map.
- **Labels and marks read** - every code, stair and note can be read at both sizes, none laid
  over another or over a wall.
- **Prose follows the map** - each direction a write-up gives that names no location code (an
  arch east, a stair in the north wall) matches the map. The validator checks those that name one.
- **The block keeps its shape** - its size sits in the sequence `BRIEF.md`'s footprints set,
  its stairs stand over the stairs they meet, and its places lie as its seed and outline say:
  a central hall central, a far tomb far.
- **It plays** - a party meets choices where the seed implies them: loops, a second way to a
  prize, a dead end where one is meant.
- **The drawing reads as the approved design** - the design's layouts can be seen in the map,
  and its voids and the places it sets stand where the design put them.

### Per sheet

- **Its edges keep the genre** - nothing a sheet draws at a region's edge (a forest, a river,
  a road) contradicts `GENRE.md`.

## Template
```
# Map Judgement Check - [Date or revision note]

Confirmed on every item: [every block and sheet not named below]

## Block [Block Code]
- [item]: [note, and its source]

[repeat per block or sheet with a finding]

## Open Items
- [Each finding, as an action, with its source]

## Owed to a tool
- [A finding a tool could make] - [tools/validate_setting.py, tools/metrics.py or tools/space.py]
```
