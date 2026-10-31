# Spec - placement

`intake.md` holds how the request was read.

## 1. One space

- **S1. The frame.** x east, y north, z up, in whole feet; west, south and down are negative.
  `BRIEF.md`'s `setting` gains `origin A`, the region whose way in, at its ground, is (0,0,0).
  Each placed thing has a parent: a region's is the setting, a block's its region, a
  location's its block, or its region where it is in none. Each thing has an origin, and its
  place is that origin, given in its parent's frame:
  - a region's origin is its way in, and a DANGEROUS region's is its first block's centre, so
    that block states no place;
  - a block's origin is its centre, and a SAFE or WILD block that states no place lies at its
    region's origin, so every location placed today keeps its meaning;
  - a location's origin is its centre, or its point where it has no outline.

  A point's absolute place is its own place plus each ancestor's.
- **S2. Values,** in `Common_Schema.md`:

  ```kdl
  value point     // "x,y" or "x,y,z": whole feet east, north and up of its frame's origin; z is 0 where unstated
  value outline   // "rect W L", "circle R" or "poly x,y x,y x,y ...": feet round the thing's origin; a poly is simple, with three points or more
  value anchor    // "CODE side": a sibling, then north, east, south, west, above or below
  ```
- **S3. Placing a thing.** A thing is placed in exactly one of these ways:
  - `xyz`, measured from its parent's origin.
  - `against`, optionally with `xyz`. The thing touches sibling CODE on the named side. It starts
    at CODE's origin, shifted by its `xyz` across the side's axis (the slide), then moves out
    along that axis until the two outlines touch without overlapping. Finally, its `xyz` along
    the axis is added as the gap. For `above` and `below`, the solids touch in z: one's floor
    meets the other's roof.
  - A SAFE or WILD location's or Stop's `bearing` and `distance`, or `at="way in"`, which means
    (0,0,0). These authored forms stay.
  - S1's defaults, where a thing states none of the above.

  A SAFE or WILD location whose place gives no z stands on its ground: its `At` height minus
  the `At` height of its region's way in.
- **S4. Outlines and solids.** A thing's outline is its `outline` field where it has one.
  Otherwise it is its width and length, as a circle that wide where its shape is `round`. A poly
  outline's extent equals the width and length where both are stated. A solid is an outline
  standing from its z up by its height:
  - a room's height is its Dressing `height`, else its seed's Conditions `height`;
  - a block's solid runs from its lowest floor to its highest roof;
  - SAFE and WILD locations and regions are flat (height 0) at their z.
- **S5. Fields.** Every field below is `opt drawn`.

  ```kdl
  node Region { xyz point; against anchor; outline outline }     // Regions.md
  node Block { xyz point; against anchor; outline outline }      // every rating; DANGEROUS loses footprint
  node Dressing { xyz point; against anchor; outline outline }   // DANGEROUS, in place of east and north
  node Location { xyz point; against anchor }                    // SAFE and WILD, in place of north and east
  node Stop { xyz point }                                        // in place of north and east
  node Dressing { outline outline }                              // SAFE and WILD
  ```

  The DANGEROUS Block's rule that blocks joined by a climbing way share their centre is
  removed, because each block's place is now stored. `Sheets.md` loses its Area column, since the
  Region's `outline` now states it.

## 2. The dry fire

- **S6. `tools/space.py`.** It resolves every region, block and location and prints one row
  each: code, kind, parent, place in the parent, absolute place, outline and z range. Then it
  lists every problem. It exits 1 on any error. `--only CODE` limits the run to one region and
  whatever joins it. The validator reports each problem at the step that owns the thing.
- **S7. Problems.**
  - *Unplaced:* a thing with no place. For a DANGEROUS block not yet packed, or a region with
    no placed join, this is a warning owed to 4a. For a SAFE or WILD location or stop, it is an
    error owed to 3d, as it was before.
  - *Placed twice:* a thing that states more than one of S3's forms.
  - *Anchor:* an anchor that names no sibling, that loops back through other anchors, or whose
    outlines never meet.
  - *Outline:* an outline that is not well formed, or a poly whose extent disagrees with its
    width and length.
  - *Overlap:* two siblings that overlap, or two locations anywhere in the setting that overlap.
    Touching is not overlapping.
  - *Outside:* a child that is not inside its parent's outline, where the parent states one.
  - *Join:* a Connection or Way whose two ends are placed but whose geometry disagrees with it:
    - When it states a `bearing` and `distance`, the far origin must lie at that bearing and
      distance.
    - When it climbs and states neither, the two outlines must overlap in plan.
    - In both cases, the two floors must differ by the `climb`, or by 0 if none is stated.
    - A way between two blocks or regions that states neither and does not climb is an error.
  - *Sheet:* a region whose `xyz` disagrees with the squares between its way in and that of a
    region it shares a sheet with.
- **S8. Tolerances.**
  - Places are whole feet, so overlap and containment are exact to half a foot.
  - A bearing holds within `maps.py`'s `BEARING_SLACK`.
  - A distance holds within the larger of 10 feet and 10%.
  - A climb is exact.

## 3. Who writes the numbers

- **S9. Authored.** Any of S3's forms may be written by hand in the step that writes the node:
  3a for a region, 3d for a location, 3e for a block, 4a for a Dressing. No tool overwrites an
  `against`.
- **S10. `maps.py place`.** It writes each sheet region's `outline` (its area). For a region
  that shares a sheet with a placed region, it also writes `xyz`, from the squares between their
  ways in and the ground heights between them.
- **S11. Settling a region.** This places a region that has no place, using a join to a placed
  region:
  - *Before packing,* a region is placed over or under the block that a climbing join without a
    bearing reaches. It takes that block's x and y, and its z from the climb. This keeps today's
    concentric levels, now as stored numbers.
  - *After packing,* a region is placed from a join that states a bearing and distance, so that
    its near end lies where the join puts it.

  The joins are tried in the order of the joining region in the gazetteer. Settling never moves
  a placed region. `space.py settle` settles every region it can, and is idempotent.
- **S12. `maps.py pack`.**
  - It settles the region before packing, and reads stair pins from absolute places.
  - It writes each room's `xyz` and the block's `outline`, then settles the region after packing.
  - A room with an `against` keeps it: the packer moves the room with its anchor, as one body.
- **S13. The validator.** `dungeon.problems` stops checking that rooms lie within the footprint
  and that a stair stands over a stair, because S7 now checks both. It keeps the hall, router,
  fill, route and map-defect checks; fill reads the block's outline area. `maps.offset`,
  `dungeon.placed` and `dungeon.stair` are replaced by `space`.

## 4. Templates and steps

- **S14.** Wording changes:
  - `templates/region/Locations.md` places a location by bearing and distance, by `xyz`, or
    `against` a placed sibling.
  - `templates/region/Connections.md` describes a stair (no bearing or distance, the rooms one
    over the other) and a sloping way (both stated); the shared-centre sentence goes.
  - `templates/region/Tables.md` gives a Dressing an `outline` where the room is irregular.
  - In `STEPS.md`, 3b says `place` writes regions' outlines and places; 3f covers every placed
    location; 4a runs `space.py settle` after each pack.
  - The README lists `space.py` and its commands.

## 5. Found in the work

- **S15. Stairs state a bearing too.** Today every one of the 21 ways that climb between levels
  states a bearing and distance as well as a climb, and the shared centre also puts its far room
  over or under it. That is two statements of where the far room is. Until both ends are placed,
  the dry fire checks both. Once both ends are placed, `pack` takes the bearing and distance off a
  stair, as it does a way within a block, and S7's stair rule then holds alone.
- **S16. A and B's own ways disagree with their locations.** The first dry fire
  (`dryfire-before.txt`) finds three ways in WILD regions, each stated from both ends, that miss
  where the locations' bearings put their far ends:
  - A.2 to A.9: stated as 30 yards south-south-west; A.9 lies 163 feet south-east.
  - B.5 to B.9: stated as 40 yards north-north-west; B.9 lies 417 feet north-north-east.
  - B.5 to B.10: stated as 60 yards west-south-west; B.10 lies 249 feet south-west.

  The dry fire also confirms in height what `intake.md` worked out by hand: H.1 to B.10 climbs
  20 feet, where the floors differ by -10. Which number moves is a design choice for each,
  either the way or the location, and is put to the user before T2 wires the validator.
- **S17. A location's bearing and distance are drawn.** On a SAFE or WILD Location or Stop,
  `bearing` and `distance` are `drawn`, as a Way's already are. A place is shown from the tables
  and written in no write-up, so moving a location does not make its write-up stale.
- **S18. `place` writes outlines already in T2.** Once `Sheets.md` lost its Area column, `place`
  had to write each sheet region's `outline` in T2 rather than T4, and a home sheet is read as
  the finest sheet listing the region. `check_places` keeps only its off-the-sheet check; the
  dry fire owns the rest.
- **S19. The migration is a form-only commit.** Old entries hold `east` and `north`, which the
  new drawn set no longer leaves out, so G's write-ups read as stale. The commit that rewrites
  G into `xyz` and `outline` is listed in `.git-blame-ignore-revs`.
- **S20. The pyramid's tip stands out of the sand.** A trial pack of C (reverted) placed C in
  plan from A.1 to C.1. The dry fire then found C.1, floor -15 and roof +5, rising through
  A.1's flat ground. That is the tip standing from the dunes, inside the statues' ring. Whether
  a flat location may lie over a solid that rises through it is for T6, decided with the user.
- **S21. Anchors as built.** The sweep finds where the two outlines *last* touch along the side,
  so a thing placed west of an L-shaped room ends up wholly west of it; to sit in the L's notch,
  it is placed against the notch's facing side. On a plan side, the thing's z is its anchor's
  plus its own; a SAFE or WILD location that states no z stands on its ground. A Stop takes no
  anchor. Until T4, `pack` leaves an anchored room's line as it is, and the dry fire reports any
  overlap with the rooms packed round it.
