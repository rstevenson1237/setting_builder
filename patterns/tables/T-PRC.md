---
id: table.procedures
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-AMB
  - table:T-HAZ
output_template: templates/table.md
schema_version: 1
---

`T-PRC` is the one place in the corpus where a die roll may gate a result.
Everywhere else, content never writes a discovery as roll-gated and what a roll
adjudicates is what the time costs. Here, a procedure states the roll and states
all three outcomes.

**Columns:** `ID | Procedure | Roll | Outcomes`. A parameter table: its rows are
data a referee reads and they stop at Builder.

## Patterns

**Three outcomes, always, in the same order.** `{OUTCOME: Success}`,
`{OUTCOME: Complication}`, `{OUTCOME: Failure}`, each on its own line, each
written out. A procedure with two outcomes is a pass-fail check and the reason
this table exists is that pass-fail checks eat sessions.

**Complication is the load-bearing outcome.** It is not failure with a smaller
number: the thing is done and it costs something the party will feel later. A
second watch spent, a soaking, a noise made, a route now known to something
else. Write it before writing the other two.

**Failure costs something other than the attempt.** Not "nothing happens" and
not "try again". Something is lost, spent, dropped, heard or closed.

**A procedure is a thing a party chooses to do.** Crossing, sounding, hauling,
prising, wading, counting, camping. It is the sequence of play at its smallest,
and it exists because the party decided to spend the time.

**The `Roll` column says who rolls and how often.** One test per crosser, one
for the party, one per watch. That is the single most common thing a referee
has to decide at the table and this is where it is decided in advance.

**Nothing in this table gates a discovery.** A procedure adjudicates what an
action costs, never whether a secret is found. Time spent searching is a
separate matter and its cost is what a roll settles.

**Eight rows, covering movement, handling, sound, light and rest.** The
procedures a party runs repeatedly, because those are the ones worth writing
once.

## Excluded patterns

- **A search or a perception procedure.** Whether a thing is found is never
  rolled for. What the looking costs may be.
- **A social procedure that decides what somebody thinks.** Reactions belong to
  locations and they branch on named player actions.
- **A combat procedure.** The ruleset is the mold and it is not in this
  repository.
- **An outcome that says "as the referee decides".** All three lines are
  written.
- **A procedure that can only be attempted once, ever.** That is a location's
  gate.
- **A bare mechanical value in the `Roll` column.** Say who rolls and how often,
  not what they roll.

## Design questions

1. **What does a party do repeatedly out here?**
2. **For each: who rolls, and how often?**
3. **What is the complication — the thing that costs them later?**
4. **What does failure spend, if it does not spend the attempt?**
5. **Which procedure is the one that makes a party turn back on time?**
6. **Which of these has a hazard behind it, and is the hazard's token stated
   where the outcome needs it?**
