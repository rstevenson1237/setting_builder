---
id: table.treasure2
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-HIS
  - table:T-TR1
output_template: templates/table.md
schema_version: 1
---

Treasure Table II: goods. Things made to be used by somebody, kept because they
were worth keeping, and left where their owner left them.

**Columns:** `ID | Entry | Mechanics`. A parameter table. Base band: roughly
`{VALUE: 100 cn}` to `{VALUE: 400 cn}` a piece.

## Patterns

**A good has an owner in it.** The band above salvage is the band where a party
starts finding possessions rather than material. Whose it was, what they used it
for, and how recently, is the content that separates this table from the one
below it.

**Usable now, by this party.** Rope that still holds, a lamp that still seals, a
coat that still turns water. A party that can use a find on the way out feels
the band change without being told.

**Trade goods count.** Salt, wax, oil, thread, ink, seed, cut peat. Portable,
divisible, priced everywhere, and the reason somebody was out here in the first
place.

**Quality is the dial and it is stated.** `{QUALITY: Poor}` through
`{QUALITY: Fine}` across the band, with weight and value on every row. Fine work
at this level is unremarkable in a lit place and remarkable four days out.

**One or two rows are from the fallen power and still work.** Not magic: made
better than anything made since. That is the bridge to the bands above, and it
is where a party first realises what they are walking on top of.

**Eight rows.**

## Excluded patterns

- **Anything that does something a party could not do without it.** That is a
  device and it is a higher band.
- **A weapon or armour as a treasure row.** Equipment a ruleset prices is the
  ruleset's, and the ruleset is not in this repository. A distinctive piece with
  a history is `T-TRE`.
- **A named item.**
- **A row with no owner implied.**
- **A quality of `{QUALITY: Artifact}`.** Not in this band.

## Design questions

1. **What were people doing out here, and what did they carry to do it?**
2. **Which of these can a party use on the way out?**
3. **What is the trade good this setting runs on?**
4. **Whose things are these, and how long ago did they stop needing them?**
5. **Which row is the fallen power's ordinary work, and how does a party tell?**
