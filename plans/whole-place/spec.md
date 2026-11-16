# Spec - the whole place

Tick a line to approve it. V1 and V2 add no stored data; V3 and V5 each add one member.

- [ ] **V1. Passages are solids.** `space.py` reads each approved plan's passages from its solve
  (`plan.solved`), each a run of squares at its Design's `width` and its Conditions' `height`, and tests them with
  the rooms. Nothing new is written: the plan is the source.
- [ ] **V2. A way between two placed ends is a segment, and is tested.** From one end's point to the other's,
  against every room and passage it does not join. It also reports the way's slope: steeper than one in one is
  a shaft or ladder, which its entry must say (`type`, or its `orientation`), else a warning owed to step 3f.
- [ ] **V3. An underground region has a roof.** A WILD Seed whose `terrain` is underground states `height`, in
  feet. The region is then a volume, and a block of another region inside it is reported unless a way joins
  the two there.
- [ ] **V4. A side elevation.** `python3 tools/space.py section` draws every block as a band, floor to roof,
  across its extent east to west, each stair and sloping way a line between its ends, each region labelled. The
  site's home page and the PDF's front matter embed it. It is the picture that shows V1 to V3's findings at once.
- [ ] **V5. One datum.** `maps.py ground` writes each `At` height from the region's way in, in the shared
  space's feet, in place of the sheet's own.

## What approval reports at once

The six rows of `intake.md`, as warnings. Each is then settled in the tables or the text: move B.10 or say where
it is; give the cavern a height and place it clear of the pyramid, or write the pyramid as standing in it.

## Asked

1. Is the lake city meant to lie beside the pyramid's lower levels, or round them?
2. V4 alone can be built first, on what `space.py` holds today. Should it be?
