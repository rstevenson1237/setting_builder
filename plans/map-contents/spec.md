# Spec - map contents

Nothing changes until a line is ticked. `intake.md` holds the prototype each line rests on.

- [ ] **M1. A symbol for each Mystery, Hazard and Reward, by its type, in a slot chosen by rule.** `tools/maps.py`
  adds `overlay.symbols` to a DANGEROUS block's map as the prototype does. The type-to-symbol table sits beside
  `BUILDING` in `maps.py`; a type with no symbol draws none. No field is added and no step changes.
- [ ] **M2. `at` on an entry, where the prose places it.** One optional member on Mystery, Hazard and Reward:
  `at Slot opt`, with `enum Slot centre north north-east east south-east south south-west west north-west`. Stated,
  it takes that slot; unstated, the rule chooses. The validator holds a write-up that names a wall for the Feature
  to the entry's `at`. Without M2 the rule's slot and such prose can disagree.
- [ ] **M3. A trap on a way is drawn at its door, and a block's Rock as rock.** Restores what plan maps lost.
- [ ] **M4. The legend is drawn**, outside the map with the scale bar.
- [ ] **M5. A players' map**: the same file rendered without secret doors, traps and Reward symbols, linked from
  the region page. One flag on `maps.py draw`.

Not proposed: placing furniture from a Dressing's `layout`, symbols for Encounters, or any size or rotation.
