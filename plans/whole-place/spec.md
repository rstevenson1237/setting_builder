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
- [x] **V4. A side elevation.** Built: `python3 tools/space.py section` draws every block as a band, floor to
  roof, each location within it, a SAFE or WILD region as its floor, and each way between two blocks or regions as
  a line between its ends. The site's home page and the PDF embed it, and both `--check`s fail a build without it.
- [ ] **V5. One datum.** `maps.py ground` writes each `At` height from the region's way in, in the shared
  space's feet, in place of the sheet's own.

## What approval reports at once

The open rows of `intake.md`, as warnings: the tunnel across level 5's outer passage, the stair through level 6's,
and a stair's head with no roof to stand in.

## Asked

1. V3 needs the cavern's height. How high is the lake city's roof?
