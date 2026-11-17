# Spec - map contents

Nothing changes until a line is ticked. `intake.md` holds the prototype each line rests on.

- [x] **M1. A symbol for each Mystery, Hazard and Reward, by its type, in a slot chosen by rule.** `tools/maps.py`
  adds `overlay.symbols` to a DANGEROUS block's map as the prototype does. The type-to-symbol table sits beside
  `BUILDING` in `maps.py`; a type with no symbol draws none. No field is added and no step changes.
- [ ] **M2. Where an entry stands, stated once, in the words a referee reads out.** Approved; the vocabulary
  below awaits confirmation. Two optional members on Mystery, Hazard and Reward:

  ```kdl
  enum Part centre north north-east east south-east south south-west west north-west
  enum Side north north-east east south-east south south-west west north-west
  at Part opt        // the part of the room it stands in, set in from the walls
  against Side opt   // the wall it stands against, found as Connection's `wall` finds one; with `at`, toward that end
  ```

  Each position has one spelling, and step 4b's "where it sits" uses its phrase:

  | Stated | Read out |
  |---|---|
  | `at=centre` | in the centre of the room |
  | `at=south-west` | in the south-west part of the room |
  | `against=north` | against the north wall |
  | `against=north at=west` | against the west end of the north wall |
  | `against=north-west` | in the north-west corner (on a wall that runs north-west, against it) |

  With `against` on a side, `at` is one of the two points along that wall; with `against` on a corner, `at` is
  unstated. Stated, the symbol takes that place and the validator finds the phrase in the write-up, as it finds a
  Hazard's Test; unstated, M1's rule chooses and the prose is free. Today 553 Features state position mostly as
  "on the wall", "in the middle" or beside another thing; those stay prose.
- [x] **M3. A trap on a way is drawn at its door, and a block's Rock as rock.** Restores what plan maps lost.
- [x] **M4. The legend is drawn**, outside the map with the scale bar.
- [ ] **M5. A players' map**: the same file rendered without what is secret, linked from the region page.
  Not one flag: artgen's dungeon layers are rock, floors, grid, doors, symbols, numbers, labels, title, scale and
  compass, none of them "secret", so `maps.py` writes a second file per block. It turns each secret door to wall,
  drops the rooms reached only through one (E.14, G.14) with their corridors, keeps a symbol unless its entry holds
  a Secret (a pool or an altar is in plain view), and leaves room codes unlinked, since each links to the referee's
  write-up. It doubles the block renders (10 dungeons; all 12 blocks render in about 11 s and 416 KB of inline
  SVG), adds a figure the site, PDF and `map_labels` must each carry, and a file `validate_setting.py` must check.
  It also hands players the whole level, which play exists to map; a handout of what a party has seen is per room,
  and waits on the paused location cuts.

Not proposed: placing furniture from a Dressing's `layout`, symbols for Encounters, a thing placed beside another
thing, or any size or rotation.
