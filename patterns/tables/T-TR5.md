---
id: table.treasure5
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-HIS
  - table:T-TR4
  - table:T-NAM
output_template: templates/table.md
schema_version: 1
---

Treasure Table V: regalia. The top of the rolled ladder — what the fallen power
made for its own offices, buried with its own dead, or hung where everyone could
see it. A party who comes back with one of these has taken something that was
never meant to be portable.

**Columns:** `ID | Entry | Mechanics`. A parameter table. Base band: roughly
`{VALUE: 8000 cn}` upward.

## Patterns

**Regalia is recognised, and that is its problem.** Everything in this band is
identifiable by anyone who knows the setting's history. Carrying it changes how
people react, who will buy it, and who wants it back. State who recognises it
and what they do about it.

**Its value is not its material.** It is worth what it is because of what it
was, which means a buyer must be someone who cares what it was. Name the kind of
buyer, and expect most of them to be a faction rather than a merchant.

**Weight is real at this band.** A hung bell, a door plate, a standard, a chair.
`{WT: n}` is the whole content of several of these rows: it can be taken, and
taking it is an expedition.

**Some of it is still in use.** An office nobody living was appointed to, an
order nobody can rescind, and someone still keeping it. Taking that piece is not
theft from the dead.

**This is the last rolled band, not the unique one.** Named singletons with a
history of their own are `T-TRE`. A row here is a kind of object the fallen
power made more than one of, and any one of them is a campaign-changing find.

**Eight rows.** Value, weight and quality on every one, and
`{QUALITY: Artifact}` used sparingly and never for something that is only
expensive.

## Excluded patterns

- **A unique named item.** `T-TRE`.
- **A piece that can be sold anonymously.** If nobody recognises it, it is band
  three or four.
- **A crown that makes its wearer a king.** Nothing rules here.
- **A piece with no weight problem and no recognition problem.** Then it is not
  in this band.
- **A device.** Band four, unless the device is also regalia, in which case say
  which half of it is the problem.

## Design questions

1. **What did the fallen power hang, plate, or set up where it could be seen?**
2. **Who recognises each of these, and what do they do about it?**
3. **What would it take to move it, and how many people?**
4. **Which of these is still in use, and by whom?**
5. **Who would buy it, and what would they pay in that is not coin?**
