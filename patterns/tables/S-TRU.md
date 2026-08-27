---
id: table.truths
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-HIS
output_template: templates/table.md
schema_version: 1
---

`S-TRU` holds the facts of the world that no in-world source states plainly. It
is the answer sheet: what is actually true underneath what everybody says and
what everybody built.

**Columns:** `ID | Entry | Who could state it`. Referee-facing, and no location
may cite it. A player reaches these by inference and never by being told.

## Patterns

**Each truth is stated flatly, in one sentence, as a fact.** This is the one
table in the corpus written for the referee alone, and hedging it defeats it. If
it is not true, it belongs in `T-RUM` with `True` set to `no`.

**Each truth contradicts something the world believes.** A truth nobody would
be surprised by is background. Say what everybody thinks, then say what is so,
and let the two disagree.

**The `Who could state it` column is the inference route.** It names who in the
world holds this and cannot or will not say it: nobody living, a faction that
gains by silence, people who measure it and call it something else. That column
is what tells a later writer how a player could ever get near it.

**Every truth is reachable, by inference, through at least one T table.** The
route is usually a `T-LOR` entry that half-records it or a `T-RUM` entry that
gets it partly right. Name the carrier while writing the row. A truth with no
carrier is a fact the campaign will never touch.

**Undercut the obvious reading of the history.** `S-HIS` says what was done.
This table says what it was actually for, who agreed to what, and what the
world has misfiled as an accident.

**Eight rows.** Two or three that reframe the fall, two or three about what is
still going on that nobody has noticed, and the rest about what a thing in this
world actually is.

## Excluded patterns

- **A secret with no clue anywhere.** A truth that no `T-LOR`, `T-RUM` or
  location clue ever brushes against is a die roll wearing a costume (J2).
- **A twist.** A truth is a standing fact of the world, not a reveal timed to a
  session. Nothing here is "discovered at the right moment".
- **A rule of the setting dressed as a truth.** "Magic half-works" is genre and
  it is already in `GENRE.md`. A truth is specific and it is about this world.
- **A truth that only matters if a player is told it outright.** If it cannot be
  inferred it cannot be used.
- **Anything a faction would simply say.** That is `S-FAC` or `T-RUM`.

## Design questions

1. **What does everybody in this world have wrong, and what is actually so?**
2. **What was the fallen power's real reason?** `S-HIS` records the act. This
   records the reason, and the reason is usually worse.
3. **Which standing condition is still running that nobody has noticed?**
4. **For each truth, who holds it and why do they not say it?** Silence with a
   motive is better than silence with none.
5. **Which T table carries each one outward, and in what distorted form?**
6. **Which truth would change how a party plays if they inferred it early?**
   That is the one worth the most clue chains.
