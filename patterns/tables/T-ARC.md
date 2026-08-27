---
id: table.architecture
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-HIS
  - table:T-LNG
  - config
output_template: templates/table.md
schema_version: 1
---

`T-ARC` holds recurring construction and ground: the stonework, the earthwork
and the terrain a party meets in more than one region. Its whole value is that
the same construction appears in a safe region and a dangerous one, because
recognition is cheaper than explanation.

**Columns:** `ID | Entry | Types`. A parameter table, and one of the most cited
in the corpus.

## Patterns

**Not split by region type.** The `Types` column marks which region types an
entry suits, and an entry may suit all three. Splitting the table by type would
destroy the recognition that makes it worth having: a party that learns what a
bell frame is on a safe road should meet the same frame in the dangerous one and
know what they are looking at.

**Describe by construction and by what it does.** How it is made, what it is
made of, what it was for. A referee reads this to place it and to answer the
first question a party asks about it, and both answers are physical.

**Every entry is a thing a party can stand next to.** A slab, a frame, a shelf,
a channel, a course of stone, a doorway squared to the compass. Not a style and
not a period.

**Recognition earns a second reading.** Write at least three entries whose
meaning changes once a party has met them twice: the construction that is always
sound, so the one that is not stands out; the fitting that is always empty here.
That is trope used as free structure, and the budget it saves goes into the
detail that could only be this instance.

**Terrain counts as architecture when it is shared.** Ground that recurs across
regions is here for the same reason stonework is. Ground that belongs to one
region is that region's Fields.

**Ten to twelve rows, and the `Types` column is genuinely used.** If every row
suits all three types, the column is decoration and the regions are not
different enough.

## Excluded patterns

- **A specific building in a specific place.** That is a location.
- **A style label.** "Cyclopean masonry" names a category. "Slabs fitted without
  mortar, each course a hand thicker than the one above" names a thing.
- **A trap or a mechanism.** `T-PUZ`, or local.
- **A hazard.** `T-HAZ`, and a construction may carry one by reference.
- **A row whose only content is that it is old and ruined.** Everything here is.
- **A measurement carried as a mechanical value.** Feet, yards and hands are
  fiction and they are welcome. Anything a ruleset would recognise is not.

## Design questions

1. **What is the most common built thing in this setting, and what was it for?**
2. **Which three constructions should a party learn to read?**
3. **What does each look like when it has failed, and how is that different from
   how it looks when it is sound?**
4. **Which ground recurs across regions, and at what rate is it crossed?**
5. **Which construction means something different in a dangerous region than in
   a safe one?**
6. **What did the fallen power build that nobody has worked out the purpose of?**
