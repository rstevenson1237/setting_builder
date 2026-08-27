---
id: setting.builder.tables
target: setting
phase: builder
writes: [Tables]
dependencies:
  - config
output_template: templates/table.md
schema_version: 1
---

Step 3. The Builder writes every row of all twenty-four tables. This pattern is
the discipline that binds across them; each table's own pattern under
`patterns/tables/` carries what that table is for, what its columns are and what
a good row in it looks like. A writer reads both.

The tables are the setting's whole shared substance. Everything a region or a
location shares with another region or location passes through one of them, so a
thin table at step 3 is a thin setting at Milestone 6, and no later step can
recover it.

## Patterns

**Write in dependency order.** A table is written after every table it draws on.
The order that satisfies the catalogue is: `S-HIS`, `S-TRU`, `S-FAC`, `S-AMB`,
then `T-LNG`, `T-ARC`, `T-NAM`, `T-LOR`, `T-RUM`, `T-UNQ`, `T-HAZ`, `T-BES`,
`T-CRE`, `T-PUZ`, `T-PRC`, `T-TR1` through `T-TR5`, `T-TRE`, `T-TOM`, `T-HRD`,
and `T-KEY` last. Writing out of order means guessing at a dependency that was
about to be written, and the guess becomes canon.

**`T-LNG` is written before any table that carries a proper name.** It is the
root registry, not a flavour table. A name coined before its roots are recorded
is a name that cannot be decomposed and `validate.py` will say so (M18).

**S content reaches a player through a T table and never directly.** The four S
tables are referee-facing and no location may cite one (M14). That boundary is
what the `draws_on` column records: a T table names the S tables it carries
outward, and the T row is where the S fact becomes something a player can find.
An S fact that no T table carries is a fact the table will never reach.

**Entry register.** A row is a sentence fragment, fifteen words or fewer where
the table's job allows it, written to be read aloud from the table at speed.
Not a description of a thing: the thing. Longer rows are legitimate where the
table's own pattern says so, and they are still fragments rather than
paragraphs.

**Rows are numbered from 01 in the order written, and a number is never
reused.** Locations cite rows by ID (M16). Renumbering a table after step 10
silently repoints every citation into it.

**Eight to twelve rows is the standard depth.** Enough that a table does not
repeat inside one campaign, short enough that every row has to earn its place.
Three tables sit outside it on purpose: `T-LNG` is a registry and runs as deep
as the setting's names require, `S-FAC` runs shorter because a faction is an
entity rather than a roll result, and `T-KEY` is written at step 10 because a
gate and its key are two locations that do not exist yet.

**Every row is different in kind, not only in detail.** Two rows that differ
only in which stone they name are one row. Before writing a row, say what a
referee would do with it that they could not do with any other row in the table.

**Carry mechanics as tokens and never as values.** `MECHANICS.md` holds the
vocabulary and `validate.py` checks every token against it (M21) and reports any
bare mechanical value found in prose (M24). `T-PRC` is the one table where a die
roll may gate a result, and it states all three outcomes every time.

**A parameter table is finished at the end of this step.** Seventeen of the
twenty-four stop here, and their rows are the form a referee reads. The seven
artifact tables are written here as complete rows too, and step 4 raises the
entry itself to the thing a referee can read aloud. Neither is a licence to
stub: "the lost journal of a noble" is not a row a Decorator can rescue.

**Strike the architect note when the rows land.** The stub carries `[[ ... ]]`
naming this step. Its content is absorbed the moment the table has rows, so it
goes then, and the table's guidance paragraph takes its place.

## Excluded patterns

- **A row that names a specific location.** The test for a table is that its
  content is shared between locations or is created before it is placed.
  Anything true of one location is that location's, and it is written there.
- **A row that is a category.** "A weapon" is a category. "A cutter's hook,
  ground back to nothing on one side" is a row.
- **Padding to a count.** A table of nine strong rows beats a table of twelve
  where three are filler, and the count in this pattern is a band rather than a
  quota.
- **An S code in a `sources` list on a location.** Mechanically refused
  (M14), and the reason it is refused is the whole S boundary.
- **A discovery written as roll-gated.** Outside `T-PRC`, nothing in the corpus
  says a thing is found on a roll. What a roll adjudicates is what the time
  costs.
- **Its own revision history.** A superseded row is rewritten in place.

## Design questions

1. **Which S facts have to reach a player, and through which T table?** Name the
   carrier for each. An S row with no carrier is a row the setting will never
   use.
2. **What is the setting's shared substance?** Which recurring stonework, which
   creatures, which procedures does a referee expect to meet in more than one
   region?
3. **Which roots does the whole corpus need?** Every name in every table and
   every region on the roster decomposes into them.
4. **Which rows are the clue chains?** A distributed clue is a `T-LOR` row
   reinforcing an `S-HIS` item. Name at least three chains before writing, so
   the tables hold together rather than each standing alone.
5. **What is the treasure ladder?** Five tables of ascending kind and base
   value. What separates each band from the one below it, and what is the
   silver-standard value at each?
6. **What does this setting not have?** `GENRE.md` names the absences. Which
   table would a reader expect to hold the missing thing, and what stands in
   its place there instead?
