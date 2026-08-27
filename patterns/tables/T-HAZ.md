---
id: table.hazards
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-AMB
  - table:T-ARC
output_template: templates/table.md
schema_version: 1
---

`T-HAZ` holds the environmental dangers a location places by reference: the
ground, the water, the air and the structure, where they can hurt somebody who
does nothing wrong. A parameter table. Its rows are data a referee reads, and
they stop at Builder.

**Columns:** `ID | Entry | Mechanics`.

## Patterns

**A hazard is a condition, not an event.** It is there whether or not anybody
is looking, and it does not act. Something with intent is `T-BES`. Something
built to catch a party is a trap, and traps are local and written at the point
of use.

**Every hazard is visible before it is suffered, at some cost.** Name what shows
it: the camber, the colour of the water, the sound underfoot, the absence of
reeds. A hazard with no tell is a tax, and a party that cannot read the ground
stops reading anything.

**Carry the mechanic as a token and keep the fiction free of numbers.** The
`Mechanics` column takes `{TEST: ...}`, `{WOUND: ...}` and `{CONDITION: name /
effect / duration}` as `MECHANICS.md` defines them (M21). The Entry column says
what happens in the world, and it says it without a value (M24).

**A condition costs something a party is spending.** Rate, light, load, footing,
watches. A condition that only reduces a number is a number; a condition that
halves the stated rate has just changed how far they can get before dark.

**Reusable across region types.** The same hazard should be placeable in more
than one region, which is what earns it a table row rather than a paragraph in
one location. Where a hazard suits only one region type, say so in the entry.

**Ten to twelve rows, covering ground, water, air, structure and cold.** A
table that is all footing leaves a referee inventing everything else.

## Excluded patterns

- **A trap.** Built, aimed, and almost always local. Traps live in
  `patterns/location/traps.md`.
- **A creature.** `T-BES`.
- **A hazard that kills without warning.** The tell is the content.
- **A bare mechanical value in the Entry column.** Tokens carry it, and M24
  reports the rest.
- **A hazard that is only a delay.** Time is a real cost; a hazard that costs
  only time and never anything else is a terrain note and belongs in a region's
  Fields.
- **A saving throw by name, or any ruleset vocabulary.** The ruleset is the
  mold and is not in this repository.

## Design questions

1. **What does the ground do here that a party will not expect?**
2. **What is the water like, and at what depth does it stop being an
   inconvenience?**
3. **What is in the air, and does it move?**
4. **What does the fallen power's construction do when it fails?**
5. **For each hazard: what shows it, and how far out?**
6. **Which condition here changes how far a party can travel before dark?**
