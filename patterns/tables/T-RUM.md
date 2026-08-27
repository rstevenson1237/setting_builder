---
id: table.rumours
target: table
phase: decorator
writes: [Entries]
dependencies:
  - table:S-HIS
  - table:S-FAC
  - table:S-TRU
output_template: templates/table.md
schema_version: 1
---

`T-RUM` holds rumours as spoken, in the words a player would actually hear. It
is an artifact table: rows at step 3, and a Decorator pass at step 4 that puts
each one into a mouth.

**Columns:** `ID | Entry | True | Source faction`. `decorate: true`.

## Patterns

**Write the sentence, not the report of it.** "Rumours say the fen is
dangerous" is a stub. "A man who takes nothing out of the fen can cross it
twice. Only twice, mind" is a rumour, and the Decorator pass is what gets from
the first to the second.

**The `True` column takes three values and the middle one is the useful one.**
`yes`, `partly` and `no`. A table of true rumours is a briefing; a table of
false ones teaches a party to ignore the table. `partly` is where the work is:
the fact is right and the reason is wrong, or the thing is real and the
location is not.

**Every rumour is somebody's.** The `Source faction` column names who says it,
and the phrasing follows: a cutter counts, a remnant of the fallen power
recites, a trader prices. Two rumours about the same thing from two factions
should be recognisably different sentences.

**A rumour is heard before it is understood.** It names a thing a party has not
seen yet in terms that will make sense afterwards. That is what makes a rumour
land at the table two sessions later.

**Cover the map and the truths.** Some rumours point at regions, some at what is
in them, and two or three are the near end of a clue chain running back to
`S-TRU`. A rumour that carries no truth and points at no place is atmosphere.

**Ten to twelve rows.** The table is drawn from repeatedly in a `SAFE` region,
so it needs enough that a party asking twice does not hear the same thing.

## Excluded patterns

- **A quest hook.** "They say a wizard in the tower needs help" is a plot. A
  rumour states a fact about the world and the party decides whether it is
  worth anything.
- **A rumour with no speaker.** "It is said" is nobody. The `Source faction`
  column is not optional.
- **A rumour that resolves itself.** If the sentence contains its own answer, it
  is lore.
- **Mechanical values.** No numbers a ruleset would recognise, in any register.
- **A `no` row that is obviously false.** A lie a party can spot from the
  phrasing costs nothing to ignore. The false ones are the ones that sound
  exactly like the true ones.

## Design questions

1. **What does each faction say about the others?**
2. **Which two rumours describe the same thing from opposite ends?**
3. **Which rumour is right about the fact and wrong about the reason?**
4. **What would somebody warn a party about for their own reasons?**
5. **Which `S-TRU` item is at the far end of a rumour here?**
6. **What does the setting sound like in a mouth?** Register carries: a cutter
   and a remnant do not build the same sentence.
