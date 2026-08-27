---
id: table.treasure1
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-HIS
output_template: templates/table.md
schema_version: 1
---

Treasure Table I: salvage. The bottom rung of the ladder and the one a party
meets most often — what is stripped off what is left, carried out because it is
worth more than the space it takes.

**Columns:** `ID | Entry | Mechanics`. A parameter table. Base band: roughly
`{VALUE: 10 cn}` to `{VALUE: 80 cn}` a piece, silver standard.

## Patterns

**Salvage is material, not craft.** Metal, glass, cloth, cord, fuel, fittings.
Its value is what it is made of and what it would cost to replace out here, and
that is exactly why a party carries it: the weight-to-value question is the
whole content of this table.

**Every row states weight.** `{WT: n}` on every entry, where a hundred coins is
one slot. This is the band where load actually decides what comes home, so a
row with no weight is a row that cannot be played.

**Half of it should be awkward.** Long, bulky, sharp, wet, or in pieces. A table
of neat purses teaches a party that carrying is free, and the trip back is
where this setting does its arithmetic.

**Salvage says who was here.** A stripped fitting says somebody stripped it. A
tool ground back to nothing on one side says how long it was used and for what.
Write the wear.

**Nothing here is magical and nothing here is fine.** `{QUALITY: Poor}` and
plain work. The one exception worth writing is a `{QUALITY: Cursed}` piece
indistinguishable from the rest, and one is the limit.

**Eight rows.** Enough that a hoard composed from this band is not the same
hoard twice.

## Excluded patterns

- **Coin.** Coin is counted, not rolled for.
- **Anything a party would keep rather than sell.** That is a higher band.
- **A named item.** `T-TRE`.
- **A row with no weight.**
- **Generic bulk.** "A sack of goods" is not a row.
- **A bare mechanical value in the entry prose.** Tokens carry it.

## Design questions

1. **What is worth stripping out here, and what is it worth in a lit place?**
2. **Which of these is awkward to carry, and how awkward?**
3. **What does the wear on each piece say about who used it?**
4. **What is abundant enough that a party stops taking it after the first
   trip?**
5. **Which piece is worth more to one faction than to a buyer?**
