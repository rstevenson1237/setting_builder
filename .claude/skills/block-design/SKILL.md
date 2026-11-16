---
name: block-design
description: How this framework designs a block before its tables are written - step 3e - from its locations, laid out, drawn and approved by the user, so Connections.md, Blocks.md and Dressing.md follow the picture. Use at step 3e, when designing a SAFE or WILD block as a settlement, when changing an approved design, or when the validator reports a design and its tables disagree. A DANGEROUS block's lines are the block-plan skill's.
---

# Block design

Every DANGEROUS region, and any other region whose `BRIEF.md` node has a `design` line, is designed here, at
step 3e, once its `Locations.md` stands. The design file is `setting/region/[Code]/Design.md`
(`patterns/Region_Schema.md`, `templates/region/Design.md`). A DANGEROUS block is a plan: the `block-plan` skill
says how its lines are written and solved. A SAFE or WILD block is a settlement, below.

## Order

1. Read the region's `BRIEF.md` node (`python3 tools/validate_setting.py --brief [Code]`), its `Seed.md`, its
   `Locations.md` and `GENRE.md`. Ask the user only what they leave open, three questions at most.
2. Write `Design.md` without places: a `Design` per block, then the lines that state it.
3. `python3 tools/design.py solve [Code] [Block]` lays it out and draws it. Show the user the drawing and what
   the solve reports.
4. `python3 tools/design.py accept [Code] [Block]` (`--seed N` for a settlement) for the one they pick. It writes
   the places, ways, seed and score. `approved` is the user's word and nothing else sets it.
5. `python3 tools/design.py apply [Code]` writes an approved design's places into the tables: a SAFE or WILD
   location's into `Locations.md` now, a DANGEROUS room's into `Dressing.md` at step 4a. Steps 3f and 4a write
   the rest to agree: `python3 tools/design.py check [Code]` says what still differs and which step owes it.

## A settlement

- A `Fill` for each location's footprint, a `Tie` for each place a bearing and distance from another, a `Street`
  for each street with the buildings it runs past; its first location stands at the block's centre. Each
  building is the kind its location's type gives.
- `solve` lays it out over twelve seeds (`artgen settlement layout`) and scores each on the faults the engine
  reports and how far each tie strays; the contact sheet shows the best three.
- Where every place is already tied, as in a ruin field, the solve gives back the ties: it is worth it for a town
  with streets.

## When a design changes

Edit the lines, solve and accept again. `accept` clears `approved`, so the user approves it again,
and the validator names each table line that now differs. Re-run step 4b for each write-up whose
directions or neighbours changed.
