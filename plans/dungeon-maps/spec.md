# Spec - dungeon maps

Each proposal names the findings it closes. `intake.md` holds how they were read.

## 1. A way's position is said once (F1)

- **S1. Exits carry no position.** `templates/region/Location.md`'s exits line becomes
  `"[make and condition] -> [Location Code] [Location Name]"`. The site and PDF add the
  position from the tables: the wall a way leaves by and its walk to the next room where both
  rooms are placed (S3), else the Connection's `bearing` and `distance`. The validator rejects
  an Exits line that states a position. Its check for two exits described alike compares them
  with their positions added.
- **S2. Prose directions are checked.** A compass word in a write-up line, followed in the same
  clause by a cited location code that a Connection from this location reaches, must lie
  within 45 degrees of that way's position. A mismatch is a warning owed to 4b. A direction
  that cites no code is the map check's to judge (S9).

## 2. Positions are stored once, as authored or as placed (F2, F3, F4)

- **S3. One meaning for bearing and distance.** In `Dangerous_Schema.md`:

  ```kdl
  node Dressing {
    east feet opt             // where its centre lies east of its block's centre, west where negative; written by `tools/maps.py pack`
    north feet opt            // and north of it, south where negative; a block states both for every room or for none
  }
  node Connection {
    bearing Compass opt       // where the far end lies from this one, as designed: it places the rooms of a block not yet packed, and pack keeps it
    distance distance opt     // with bearing; a way between two rooms that state east and north states neither
  }
  node Block {
    footprint feet opt        // the side of the square, centred on the block's centre, its rooms are packed in
    router number opt         // the version of tools/route.py its passages were routed by
  }
  ```

  A block's centre is shared by every block a climbing way joins it to, so a stair's two ends
  lie one over the other (S6).
- **S4. `pack` writes positions only.** It reads the direction to keep for each way from the
  rooms' positions where they are placed, else from the way's bearing, else keeps none. It
  writes each room's `east` and `north`, the block's `footprint` and `router`, and
  removes `bearing` and `distance` from the ways inside the block. It touches no write-up. On a
  packed block whose ways all route under the current router it changes nothing but `router`;
  `--again` repacks.
- **S5. Checks.** A way inside a packed block states no bearing or distance. A packed block
  states `router`, equal to `route.VERSION`. Every room lies inside the footprint square
  centred on the block's centre. The bearing-reversal check skips ways inside packed blocks.
  No seed is recorded: the positions it produced are stored, and nothing derives them again.

## 3. The build's rates and the pyramid's shape (F5, F6)

- **S6. `pack` lines in `BRIEF.md`.**

  ```kdl
  dangerous {
    pack fill="30-45%" passages="35%"   // fill: share of the square its rooms cover; the packer starts at the top, the validator holds the bottom
  }
  region G ... {
    pack footprint="250 feet"           // a region's own: the side of its block's square
  }
  ```

  A region's `pack` replaces its rating's only for the values it names. `pack` packs into a
  stated footprint exactly, else from the top of `fill` upward. The validator holds a packed
  block's footprint to the brief's and its rooms to the bottom of `fill`. Every pyramid level
  states a footprint, widening to G and narrowing after, with H's equal to F's.
- **S7. Stairs stand over stairs.** A way that climbs between two packed blocks joins rooms
  whose footprints overlap in plan; the validator holds it. Packing a block whose room climbs
  to a room of a packed block pulls it over that room.

## 4. Halls (F7)

- **S8.** `Room_Shape` gains `hall`: a room one passage wide and at least twice as long as it
  is wide. A Dressing in a block whose narrower side is no wider than its block's passages and
  whose longer side is at least twice it is a `hall`, and a `hall` is such a room; the
  validator holds both ways. A hall is drawn as a rectangle showing its code alone, and the
  packer spaces its label as such.

## 5. Review and build (F8, F9)

- **S9. A map judgement check.** `templates/checks/Map_Judgement_Check.md`, step 5d, writing
  `setting/checks/MapJudgementCheck.md`. Its viewing recipe is one command,
  `python3 tools/maps.py draw --out _maps --fit 1600x1600px`, and its items are what no rule
  sees: every way reads as the way it is, floors read apart, labels and marks read, a
  direction in prose that cites no code matches the map, and the level reads as its seed.
- **S10. Block maps are built.** `maps.py draw`, the site and the PDF build each block's map
  from its tables when they need it; `setting/region/*/*.json` is ignored by git. artgen's
  `sync`, the stale-map check and the hand-edit handling for blocks go. The terrain sheets stay
  committed under D7.

## 6. Where the code lives (F10, F11)

- **S11. `tools/dungeon.py`.** A DANGEROUS block's map (`block_map`), its routes (`plan`),
  the `pack` command and every check on a block (`problems`) move out of `maps.py` and the
  validator. `maps.block_file` dispatches by rating; the validator calls `dungeon.problems`.
- **S12. `plans/sheet-maps/artgen-capabilities.md`.** The keys the framework writes into a
  dungeon and settlement file, what each does as observed, the defaults that bite, and where
  report 2 holds the gaps. README's artgen line cites it.
