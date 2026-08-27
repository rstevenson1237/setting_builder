---
id: table.lore
target: table
phase: decorator
writes: [Entries]
dependencies:
  - table:S-HIS
  - table:S-TRU
  - table:T-LNG
output_template: templates/table.md
schema_version: 1
---

`T-LOR` holds written works, statues and art as the thing itself. It is an
artifact table: the Builder writes the rows at step 3 and the Decorator raises
each entry at step 4 until a referee can read it to a player exactly as it
stands.

**Columns:** `ID | Entry | Form`. `decorate: true`.

## Patterns

**The entry is the text, not a description of the text.** "A ledger recording
the ringing order" is a stub. The line as it is cut into the stone is the row.
This is the whole reason the table is decorated (J9).

**The `Form` column is where the object lives.** What it is written on or carved
into, and how a party comes to be looking at it: upside down to a walker,
legible only from inside looking out, waxed and folded into a socket, half of it
below the present waterline. That column carries the physical gate, and it is
where the discovery is designed.

**This is the main distributed clue route.** An `S-TRU` item reaches a player
through a `T-LOR` entry that half-records it, or through one that records it
confidently and wrongly. Write at least three rows that are the far end of a
clue chain, and know which truth each one serves.

**A record is written by somebody with a reason.** An order, a tally, a
complaint, a last instruction, a boast, an account rendered. Each has a voice
and each leaves something out. Nothing here is a neutral history, because
nothing anybody actually writes is.

**Some of it is wrong.** Not most of it: a corpus where every record lies
teaches a party to read nothing. Two rows in ten that are confidently wrong,
with the error traceable, are worth more than ten that are reliable.

**Ten to twelve rows, in mixed forms.** Cut letters, a page, a relief, a
statue, a tally, a mark. A table of documents leaves a referee with nothing to
show a party who cannot read.

## Excluded patterns

- **A summary.** "It describes the fall of the Covenant" is what the Decorator
  pass exists to delete.
- **An entry too long to read aloud.** A cut inscription is a line or two. A
  page is a paragraph. Anything longer is a location's content.
- **A modern editorial voice.** Nobody in this world is writing for a reader
  outside it, and no entry explains its own significance.
- **A name whose roots are not recorded.** M18 does not scan table prose, and
  the corpus still has to hold together.
- **A row that states an `S-TRU` item plainly.** A truth stated outright in a
  findable document is not a truth, it is a handout.

## Design questions

1. **Which three truths does this table carry outward, and in what form?**
2. **What did people here write on, and what survives the conditions?**
3. **Who wrote each of these, and what were they leaving out?**
4. **Which entry is confidently wrong, and what would let a party catch it?**
5. **What is here for a party who cannot read?** A relief, a statue, a worn
   place, a tally.
6. **Which entry is the one a referee will read aloud most often?** Write that
   one first and hold the rest to it.
