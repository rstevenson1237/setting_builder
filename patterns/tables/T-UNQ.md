---
id: table.questions
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-TRU
  - table:S-HIS
output_template: templates/table.md
schema_version: 1
---

`T-UNQ` holds the deliberate in-fiction open threads: the things this setting
does not answer, on purpose, and will not answer later. It is the only register
of open questions in the repository, and it is in-fiction by construction.

**Columns:** `ID | Entry | What an answer would cost`.

## Patterns

**A row here is a decision to leave something open, not a note that it is
undecided.** There is no open-questions register in this project. A build-time
question is asked in a step's question batch and answered before generation. A
row in this table is the opposite: an answer deliberately withheld from the
world, which the referee may keep withheld or may settle at their own table.

**Each question is anchored in something a party can find.** The thing is
present; the explanation is not. A question with no anchor is not open, it is
absent, and nobody will ever ask it.

**The second column prices the answer.** What a party would have to do, go, or
give up to settle it — and, where the honest answer is that nothing in the
setting settles it, say that plainly so a referee knows they are free to decide.
This is what stops the table becoming a list of loose ends.

**Ask what a referee will actually be asked.** The good rows are the questions a
player asks in the first session: what happened to the people, why is it warm,
who tied the rope. Those need an answer prepared or a stated absence, and this
table is where the absence is stated.

**Some of these are answered in `S-TRU` and the world still does not say so.**
That is a legitimate row: the question is open in the fiction and closed on the
referee's page. Say which truth answers it, so the referee is not left guessing
what they are holding.

**Eight rows.** More than that and the setting reads as evasive rather than
withholding.

## Excluded patterns

- **A question the project has not decided.** That belongs in a step's question
  batch, or in `EXTERNAL.md` if it depends on something outside the repository.
- **A mystery with a hidden answer nobody has written.** Either the answer is in
  `S-TRU` or the row says the setting does not settle it. A third option is a
  gap that will be filled by whoever notices it last.
- **A rhetorical question.** "What really lies beneath?" is a tagline.
- **A question about the ruleset or the mechanics.** The ruleset is not in this
  repository.
- **A question whose answer would invalidate the tables.** Leaving the founding
  of the world open is fine. Leaving open whether the fall happened is not.

## Design questions

1. **What will a player ask in the first session that the setting should not
   answer?**
2. **For each, what is the physical anchor a party can stand in front of?**
3. **Which of these does `S-TRU` actually answer, and should the world keep
   quiet about it anyway?**
4. **What would settling each one cost, and is that cost payable?**
5. **Which question, if answered, would make the setting smaller?** That is the
   one to protect.
