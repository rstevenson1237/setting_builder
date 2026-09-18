# Arm 2: the registry rows 4c wrote

Per `STEPS.md` 4c, a Feature calling for Lore, a Key, a Quest, a Named Creature or a Unique
Treasure adds a **stub row** (name and location) to the matching `setting/` file; the full
entry is written at 4d, with every location that cites it in view. Those rows are held here
rather than written into `setting/`, so the control run does not alter the corpus
`tools/validate_setting.py` and `checks/` are tuned against.

Coinage recorded back into `setting/Language.md` is listed last, per 4c.

## setting/Lore.md

- The Third Winter's Register (*register leaf*) - found at F.3 The Register Room
- The Usher's Tally (*tally*) - found at F.6 The Presence Antechamber
- The Last Sworn Roll (*roll*) - found at F.8 The Sworn Seat
- The Closed Court's Record (*record*) - found at F.12 The Closed Court

## setting/Keys.md

- The Closed Court Token (*token*) - found at F.4 The Gift-Store (unlocks F.12 The Closed
  Court)

## setting/Quests.md

- Who Last Sat - given at (no giver yet), target F.8 The Sworn Seat

## setting/NamedCreatures.md

- Ranik - appears at F.2 The Robing Wreck

## setting/UniqueTreasures.md

*None. No location in this region drew the 5% unique-treasure disposition.*

## setting/Language.md

- Sarnar = sarn (oath, a sworn word) + ar (place, holding) - the old crown seat's own name,
  Marchspeech, in `setting/region/Regions.md`
- Ranik - Marchspeech, (C)V(C) throughout, the Nine Wagons stone-agent at F.2

## setting/region/Regions.md

The gazetteer row this region needs at 3a:

```
F Sarnar (oath-place) - DANGEROUS, d4
Tags: see setting/region/F/Tags.md
Sarnar is the crown seat the unified crown ruled the road from a century and a half ago,
standing empty on its hill above the old approach road since the succession broke
twenty-eight years ago; its lower courses were quarried out of Daghash and carted a week
west, and all three kingdoms watch the hill from a distance without holding it.
```

The die is **d4**, which `setting/Procedures.md` calls a deliberate outlier. It is not a
free choice here: the map fixes the count at twelve, `patterns/region/Dangerous.md` sets a
collection's count at 3x the die, and twelve rooms at d4 burns exactly three of the Danger
track's six steps across a full clear, which is the pressure the 3x rule exists to produce.
