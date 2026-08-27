---
id: table.history
target: table
phase: builder
writes: [Entries]
dependencies: []
output_template: templates/table.md
schema_version: 1
---

`S-HIS` is what happened, in order, and what it left behind. It is the root of
the corpus: it draws on nothing, and four of the five tables written after it
draw on it.

**Columns:** `ID | Entry | Left behind`. Referee-facing, and no location may
cite it (M14). Its content reaches a player through a T table.

## Patterns

**One event per row, in order, and each one leaves something a party can walk
into.** The `Left behind` column is what makes this table the root rather than
a chronology. An event that left nothing is an event no later table can carry
outward, and the setting is only ever met through what is still standing.

**Write the fall, not the golden age.** What the world was is background. What
it did, in what order, and what broke is the material later tables cut up. Two
or three rows on what was built, one on what it was built for, and the rest on
how it ended and what happened after.

**End before the present.** The last row stops short of what a party walks into
now: that is the standing situation, and `GENRE.md` and the setting Overview
carry it. A history that runs up to this morning has written the plot.

**Leave the causes underneath.** Why the fall happened is `S-TRU`, because it is
the thing no in-world source states plainly. This table says what was done and
what it left. The two read differently on purpose, and the gap between them is
where a party's inference lives.

**Number the rows so the order is readable.** `S-HIS-01` is the earliest.
Nothing else in the corpus depends on that, and a referee reading the table
cold does.

**Eight rows.** Enough to hold a rise, a fall and an aftermath. Fewer and the
aftermath is a single beat; more and the middle rows stop being distinguishable
events.

## Excluded patterns

- **A date, a regnal year, or a calendar.** Nobody out here counts them, and a
  date is a fact a player cannot use. "Four years" and "one season" are
  durations and they are usable.
- **A named individual.** People are `S-FAC` when they are a power and `T-CRE`
  when a party can meet them. A history naming a person has written a character
  no pattern owns.
- **A prophecy, or anything still to come.** The setting is a standing
  situation.
- **A row whose `Left behind` is "ruins".** Name the ruin. A doorway squared to
  the compass is a thing; a ruin is a category.
- **The reason.** That is `S-TRU`.

## Design questions

1. **What did the fallen power build, and what did it build it for?** The answer
   is the most common built thing in the setting and every region carries some
   of it.
2. **How did it end?** In one season or across four years? By something arriving
   or by something being dug into?
3. **What happened after, and who was still here to do it?** The aftermath rows
   are the ones a party meets the residue of.
4. **For each row, what is still standing?** If the answer is nothing, cut the
   row or find the residue.
5. **Which of these events does an in-world source get wrong?** That
   disagreement is `T-LOR` and `T-RUM` material, and it is worth deciding here.
