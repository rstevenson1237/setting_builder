---
name: block-design
description: How this framework designs a block before its locations are written - step 3d - from layouts, laid out by artgen's engine and approved by the user, so Locations.md, Connections.md and Blocks.md follow the picture. Use at step 3d, when choosing layouts for a block, when changing an approved design, when adding a layout to layouts/, or when the validator reports a design and its tables disagree.
---

# Block design

A region whose `BRIEF.md` node has a `design` line is designed here, at step 3d, before `Locations.md`.
Without the line, skip this. A DANGEROUS block whose shape is known well enough to state - its layouts, rooms and
routes - is designed as a plan instead: the `block-plan` skill. The design file is `setting/region/[Code]/Design.md`
(`patterns/Region_Schema.md`, `templates/region/Design.md`). artgen's **dungeon-design** skill says how layouts,
designs, seeds and scores behave; this one says only how this repo drives them. Its project steps (`art/`,
`--sheet art/...`) do not apply: `tools/design.py` writes artgen's design from `Design.md` and runs the engine.

## Order

1. Read the region's `BRIEF.md` node (`python3 tools/validate_setting.py --brief [Code]`), its `Seed.md` and
   `GENRE.md`. Ask the user only what they leave open, three questions at most.
2. `python3 tools/design.py layouts` lists the layouts: artgen's bundled ones, and this repo's `layouts/` in place
   of any of the same id. Write `Design.md` without places: a `Design` per block, a `Use` for each layout chosen, a
   `Bind` for each of its roles, a `Join` for each socket meant to meet a socket or a location, a `Fill` for every
   other location, a `Void` for ground no room takes. `python3 tools/design.py expand [Code]` prints the design as
   artgen's and the graph the engine expands it to, or every fault in it.
3. `python3 tools/design.py solve [Code] [Block]` lays it out over twelve seeds and prints each one's score,
   where it falls short, and the contact sheet of the best three. Show the user the sheet and the table.
4. `python3 tools/design.py accept [Code] [Block] --seed N` for the one they pick. It writes the
   places, ways, seed and score. `approved` is the user's word and nothing else sets it.
5. Steps 3e and 3f, then 4a, write the tables to agree: `python3 tools/design.py check [Code]` says
   what still differs and which step owes it.

## What a design holds

- Codes are `[Code].1` to `[Code].N` across the region, as `Locations.md` will number them; each
  `Bind` and `Fill` gives the type of its locations, one for all or one each, in `BRIEF.md`'s mix.
- A `Use`'s params are in its layout's own terms: counts, or sizes in 5 ft cells. Every other size is in feet.
- A room too small for the ways it holds is grown by the engine, so `accept` can write a size the layout did
  not state. Give a part `"grow": false` in a layout of `layouts/` to hold it.
- A stair into a room of the block pins that room over the level it meets, in the design's frame: state an
  `outline` for such a block. A design with none grows from its centre, and `accept` writes the `hull` it filled.
  Design the levels a stair joins in order: the first with `--free` on `solve` and `accept`, which ignores the
  stairs' places, then `python3 tools/maps.py pack --again` places its neighbours round it, and each next
  level is solved pinned to the last.
- `fill`, `spacing`, `passages`, `detour` and `pad` start from `BRIEF.md`'s `design` line, then its `pack` line;
  a `Design` line overrides what it names. `pad` keeps rooms apart so a passage runs between them; `spacing`'s
  most is how far joined rooms may stand. The engine scores what `dungeon check` finds, ways left unrouted,
  bearings strayed and detours; `solve` adds a note where fill falls outside the design's.
- A `Fill` may state a `shape`, or a `poly` `outline` where no shape draws the room.
- A SAFE or WILD block is a settlement, laid out by `settlement layout`: a `Fill` per location, a `Tie` for
  each place a bearing and distance from another, a `Street` for each street with the buildings it runs past;
  its first location stands at the block's centre. `solve` and `accept` work as for a level. Where every place
  is already tied, as in a ruin field, the solve gives back the ties: it is worth it for a town with streets.
- An approved design's places are the tables': `python3 tools/maps.py pack` refuses its block.

## A layout of this repo's own

`layouts/[id].json`, in artgen's layout format (`node tools/artgen/artgen-maps.js schema layout --keys`). Add one
only where no bundled layout gives the shape; one of a bundled id replaces it for every design here. The
validator runs the folder through the engine, which names the first file it rejects.

## When a design changes

Edit the lines, solve and accept again. `accept` clears `approved`, so the user approves it again,
and the validator names each table line that now differs. Re-run step 4b for each write-up whose
directions or neighbours changed.
