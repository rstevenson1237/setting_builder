---
id: table.tomes
target: table
phase: decorator
writes: [Entries]
dependencies:
  - table:S-TRU
  - table:T-LNG
  - table:T-LOR
output_template: templates/table.md
schema_version: 1
---

`T-TOM` holds magical tomes: the written works that do something, as opposed to
the written works that say something. It is an artifact table — rows at step 3,
and a Decorator pass at step 4 that gives each one its actual words.

**Columns:** `ID | Entry | Mechanics`. `decorate: true`.

## Patterns

**A tome is a device made of writing, and it obeys the device rules.** Magic here
is a found technology nobody understands. A tome half-works, works differently
than it is recorded to work, or works on the wrong thing, and it has a running
cost like anything else.

**Give the words, not the summary.** The line that has to be read, the phrase
that is repeated, the instruction as written. That is the decoration pass, and
it is what lets a referee put the book in front of a player.

**Say what reading costs.** Time, light, being read aloud where something can
hear it, being read in the wrong place, being read by somebody who understands
the older layer. Reading is the action, and an action in this setting has a
price.

**The physical object matters as much as the text.** What it is made of, how it
has survived, what is missing from it, what has been added to it by a later
hand. A tome that is only its contents cannot be handled, hidden, ruined or
carried.

**Half of them should be usable once.** A single reading, a single working, a
page that is spent. That is what keeps them findable treasure rather than
permanent ability.

**Anchor each to `T-LNG` and to `S-TRU`.** These are the works that record what
nobody says plainly, and they mostly record it wrongly. A tome that agrees
entirely with the truths is a handout.

**Eight rows.**

## Excluded patterns

- **A spellbook with a list of spells.** The ruleset is the mold, it is not in
  this repository, and a list of its spells would not survive a swap of
  `MECHANICS.md`.
- **A tome that teaches a permanent ability with no cost.**
- **A tome written in a language a party simply cannot read, with no route in.**
  There is always a route: a translator, a partial record, a diagram, a
  recurring root.
- **A summary of contents.** The Decorator pass deletes it.
- **A book that is only lore.** That is `T-LOR`.
- **A grimoire whose author is a wizard with a name and a tower.** Nobody rules
  here and nothing enchants on request.

## Design questions

1. **What did people here write down that was meant to be operated rather than
   read?**
2. **For each: what are the actual words, and what happens when they are said?**
3. **What does reading it cost, and who else hears?**
4. **What is the object made of, and what is missing from it?**
5. **Which of these is spent by one use?**
6. **Which truth does each one get wrong, and in which direction?**
