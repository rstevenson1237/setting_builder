---
name: block-design
description: How this framework designs a block before its locations are written - step 3d - from layouts, solved and approved by the user, so Locations.md, Connections.md and Blocks.md follow the picture. Use at step 3d, when choosing layouts for a block, when changing an approved design, or when the validator reports a design and its tables disagree.
---

# Block design

A region whose `BRIEF.md` node has a `design` line is designed here, at step 3d, before `Locations.md`.
Without the line, skip this. The design file is `setting/region/[Code]/Design.md`
(`patterns/Region_Schema.md`, `templates/region/Design.md`); the layouts are `layouts/`
(`patterns/Layout_Schema.md`). For what each artgen key does, read the `dungeon-map` skill; this
one repeats none of it.

## Order

1. Read the region's `BRIEF.md` node (`python3 tools/validate_setting.py --brief [Code]`), its `Seed.md` and
   `GENRE.md`. Ask the user only what they leave open, three questions at most.
2. `python3 tools/design.py layouts` lists the library by tag. Write `Design.md` without places: a
   `Design` per block, a `Use` for each layout chosen, a `Bind` for each of its roles, a `Join`
   for each pair of sockets meant to meet, a `Fill` for every other location, a `Void` for ground
   no room takes. `python3 tools/design.py expand [Code]` prints the graph it makes and every fault in the design.
3. `python3 tools/design.py solve [Code] [Block]` packs it over twelve seeds and prints each
   packing's score and where it falls short, and draws the best three on a contact sheet in a
   temporary folder. Show the user the sheet and the table.
4. `python3 tools/design.py accept [Code] [Block] --seed N` for the one they pick. It writes the
   places, ways, seed and score. `approved` is the user's word and nothing else sets it.
5. Steps 3e and 3f, then 4a, write the tables to agree: `python3 tools/design.py check [Code]` says
   what still differs and which step owes it.

## What a design holds

- Codes are `[Code].1` to `[Code].N` across the region, as `Locations.md` will number them; each
  `Bind` and `Fill` gives the type of its locations, one for all or one each, in `BRIEF.md`'s mix.
- A stair into a room of the block pins that room over the level it meets, in the design's frame: state an
  `outline` for such a block. A design with none grows from its centre, and `accept` writes the `hull` it filled.
  Where the levels a stair joins are not yet placed, `solve` and `accept` take `--free` to ignore them, and
  `python3 tools/maps.py pack --again` places them around this level.
- `fill`, `spacing`, `passages` and `detour` come from `BRIEF.md`'s `design` line, then `pack` line, and
  a `Design` line overrides only what it names.
- A SAFE or WILD block is fixed geometry, not solved: write each location's `Place` and each street's
  `Link` yourself, and `check` holds the tables to them.
- An approved design's places are the tables': `python3 tools/maps.py pack` refuses its block.

## When a design changes

Edit the lines, solve and accept again. `accept` clears `approved`, so the user approves it again,
and the validator names each table line that now differs. Re-run step 4b for each write-up whose
directions or neighbours changed.
