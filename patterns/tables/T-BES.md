---
id: table.bestiary
target: table
phase: decorator
writes: [Entries]
dependencies:
  - table:S-TRU
  - table:S-AMB
output_template: templates/table.md
schema_version: 1
---

`T-BES` holds the creatures of the setting as they are described at the table.
It is an artifact table: rows at step 3, and a Decorator pass at step 4 that
rewrites each entry into the order a party actually meets the thing.

**Columns:** `ID | Entry | Mechanics`. `decorate: true`.

## Patterns

**Write the meeting, not the monster manual entry.** What is noticed first, what
it does while it is being watched, and what it does when the party moves. A
creature described by its anatomy is a creature a referee has to translate at
the table; a creature described by its behaviour can be run straight off the
row.

**Behaviour before appearance, and behaviour before statistics.** The most
useful sentence in a row is what it does when it is ignored, when it is
approached, and when it is struck. Two of the three, in the entry, in that
order.

**Every creature has a tell and a way to be avoided.** What warns a party, and
what a party can do about it that is not fighting. A bestiary where every
answer is combat has made the difficulty die the only dial the setting has.

**Mechanics are tokens and they sit in their own column.** `{AD: n, mod}` and
`{TYPE: ...}` on every creature, and `{WOUND: ...}` on anything that can cause
one (M21). Nothing mechanical appears in the entry prose (M24).

**The first fragment of the entry is the creature's name, and it is what
citations resolve against.** `(BESTIARY, Fen-wight)` matches the lead of the
row up to the first stop. Name it plainly, put the name first, and never rename
it afterwards.

**Draw the creatures out of the truths.** What this world does to things that
stay in it is `S-TRU`, and a bestiary that could be lifted into another setting
has not read it. Two or three rows should only make sense here.

**Ten to twelve rows, spread across the types and across the difficulty
range.** Something a lone party can drive off, something that is only survivable
by leaving, and several in between.

## Excluded patterns

- **A named individual.** A creature with a name, a history and a want is
  `T-CRE`.
- **A stat block.** `MECHANICS.md` is the whole interface to the ruleset and the
  tokens are the whole of it here.
- **A description that starts with size and colour.** It is what a party notices
  fourth.
- **A creature whose only behaviour is attacking on sight.** It has no content
  above its tokens.
- **Ecology.** What it eats and how it breeds is worth one clause if a party can
  use it, and nothing if they cannot.
- **A bare mechanical value in prose, in either register.**

## Design questions

1. **What does this world do to a thing that stays in it too long?** Two rows
   should be the answer.
2. **For each creature: what does it do when it is ignored?**
3. **What warns a party, and how far out?**
4. **What can a party do about each one that is not fighting?**
5. **Which one is the region-ender — the thing that means leave now?**
6. **Which of these is a person, and does the party find that out before or
   after?**
