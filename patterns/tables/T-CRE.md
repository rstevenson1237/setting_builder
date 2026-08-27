---
id: table.creatures
target: table
phase: decorator
writes: [Entries]
dependencies:
  - table:S-FAC
  - table:S-HIS
  - table:T-BES
  - table:T-NAM
output_template: templates/table.md
schema_version: 1
---

`T-CRE` holds named creatures: the individuals a party can meet, recognise, and
meet again. It is an artifact table: rows at step 3, and a Decorator pass at
step 4 that gets each one to the point where a referee can play them off the
row.

**Columns:** `ID | Entry | Mechanics`. `decorate: true`.

## Patterns

**One of a kind, and the corpus knows it.** A named creature is not a stronger
example of a `T-BES` row. It is a specific thing with a name, a history, a want
and somewhere it usually is. If it could be met twice in two regions
simultaneously, it belongs in the bestiary.

**A want and a price, like a faction, but a person-sized one.** What it is
trying to get, and what it will do or give for it. That is what makes it
playable rather than an encounter with a name attached.

**Say how it opens.** The first thing it does when a party arrives, before
anybody has decided anything. That single sentence is what a referee needs most
and it is the sentence most often missing.

**Name what would make it leave, and what would make it fight.** Both. Most of
these should be avoidable and several should be negotiable, because a setting
where the named things are all boss fights has no room to be talked to.

**Some of them are people, and being a person is not the same as being safe.**
The setting has no living authority: what stands in its place is orders nobody
can rescind and people still keeping them. Two or three rows should be exactly
that.

**Tie each one to a faction or to a truth.** A named creature loose in the
setting is a set piece. One that wants what a faction wants, or one whose
existence is an `S-TRU` item standing up and walking, is content.

**Eight rows.** These are held in a referee's head across a campaign, and past
eight they stop being individuals.

## Excluded patterns

- **A quest giver.** Nobody is issuing tasks. A named creature wants something
  and a party may decide to be useful to it.
- **A creature that cannot be met.** If it is only ever heard about, it is a
  rumour or a truth.
- **A stat block, or a fight written in advance.** The tokens carry the
  mechanics and the table decides the rest.
- **A name whose roots are not recorded.** `T-LNG` first.
- **A tragic backstory that a party can never learn.** Either it is findable or
  it is not there.
- **An unkillable creature.** Something that cannot be beaten and cannot be
  avoided is a wall with dialogue.

## Design questions

1. **Who is still out here keeping an order nobody can rescind?**
2. **For each: what does it want, and what will it give?**
3. **What does it do in the first ten seconds?**
4. **What makes it leave, and what makes it fight?**
5. **Which one is a `T-BES` creature that became a person, or the reverse?**
6. **Which of these would a party come back for, and what would they bring?**
