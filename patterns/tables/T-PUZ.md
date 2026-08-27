---
id: table.puzzles
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-HIS
  - table:T-LNG
  - table:T-ARC
output_template: templates/table.md
schema_version: 1
---

`T-PUZ` holds puzzles that recur or are built before they are placed: the
constructions a party meets in more than one location, and the shapes a writer
reaches for when a location needs one.

**Columns:** `ID | Entry | Answer | Clue`.

## Patterns

**A puzzle is a construction with a state, an answer and a way to learn the
answer.** All three columns are filled. A puzzle whose answer is not written
down is not a puzzle, it is a referee improvising under pressure while four
people watch.

**Nothing here resolves on a roll.** The answer is reached by doing a named
physical thing or by knowing something findable. What a roll adjudicates is what
the time costs, never whether the thing is solved (SPEC.md section 10.2).

**The `Clue` column is proximate or distributed and says which.** A proximate
clue sits in the same location and needs nothing outside the room. A distributed
clue is a `T-LOR` entry, a rumour, or the same construction met earlier and
working normally. Recurring puzzles are the natural home of the second kind:
the third time a party meets the mechanism, the first two were the clue.

**A puzzle is made of what this world builds.** Draw the mechanism from `T-ARC`,
the words from `T-LNG`, and the reason it exists from `S-HIS`. A puzzle that
could stand in any setting is a puzzle that teaches a party nothing about this
one.

**Every puzzle has a way past that is not the answer, and it is priced.**
Breaking it, going around it, or paying somebody. The content never says which
is the mistake. Where a puzzle is opened by a physical key, both ends belong in
`T-KEY` and that pairing is written at step 10.

**Eight rows, of at least three kinds.** Sequence, substitution, physical
manipulation, language, observation. A table of one kind is one puzzle with
eight skins.

## Excluded patterns

- **A riddle in verse.** It resolves on whether one player has heard it before.
- **A puzzle requiring a player to know the setting's language.** The
  vocabulary is in `T-LNG` for the referee, and a party reaches it through
  findable records, never through study.
- **A puzzle with one solution and no way past.** That is a wall.
- **A puzzle that is a lock waiting for a key.** That is `T-KEY`.
- **A puzzle whose failure state is a death with no warning.** Failure costs
  time, light, position or noise.
- **A puzzle specific to one location.** Local puzzles are written at the point
  of use, by the location patterns.

## Design questions

1. **What did the fallen power build that needed operating, and what happens
   when it is operated wrongly now?**
2. **Which mechanism recurs often enough that meeting it twice teaches the
   party how it works?**
3. **For each puzzle: what is the answer, and where is it findable?**
4. **What is the way past that is not the answer, and what does it cost?**
5. **What does failure cost, in time, light or noise?**
6. **Which puzzle would a party solve by talking to somebody instead?**
