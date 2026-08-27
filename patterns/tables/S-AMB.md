---
id: table.ambiance
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-HIS
output_template: templates/table.md
schema_version: 1
---

`S-AMB` is the sensory register of the setting as a whole: what it is like to
stand in this world, in the senses, with nothing happening. Referee-facing. A
location draws on it through a T table and states its own senses in its own
words.

**Columns:** `ID | Entry | Sense`.

## Patterns

**One sense per row, named in its own column, and cover the senses that are not
sight.** Sight is the sense prose reaches for and the one a party is already
using. Smell, hearing, touch and the sense of temperature are what make a place
felt rather than described, and this table exists to make sure the corpus has
them on hand.

**A row states what is there, not what it is like.** "Peat smoke running flat
along the reed tops" is the entry. "An oppressive atmosphere" is a conclusion
and it is exactly what the player registers may not state.

**Each row is true of the setting rather than of a place.** The same
least-common-denominator test as `GENRE.md`: name a region where the row is
false, and if one exists, that row is the region's.

**Prefer the sense that is wrong.** Warm stone in a cold place, water that gives
no sound back, light holding an hour longer than the sky accounts for. A
sensation that contradicts what the eye reports is worth three that agree with
it, and it is the cheapest way a setting tells a party it is not home.

**Write for reuse at speed.** These rows are read aloud between other things, so
they are fragments: fifteen words or fewer, one image, no clause explaining it.

**Twelve rows, spread across at least four senses.** Two or three per sense so a
referee has a choice without hunting.

## Excluded patterns

- **A conclusion, a mood word, or an adjective doing the work.** Ominous,
  eerie, oppressive, unsettling: each of them tells the table what to feel.
- **An event.** Something happening is an Encounter and it belongs in a region's
  referee table.
- **A sensation tied to one place.** Demote it into that place.
- **A creature, a person, or anything with intent.** Ambiance is the room, not
  what is in it.
- **A mechanical token.** Nothing here is tested against. A sensation that
  requires a test is a hazard and it is `T-HAZ`.

## Design questions

1. **What does this world smell of, everywhere?**
2. **What does sound do here that it does not do at home?**
3. **What is the temperature of the built stone, and is it the temperature of
   the air?**
4. **What does the light do, and how long does it hold?**
5. **Which of these sensations contradicts what the eye reports?**
6. **What does a party stop noticing after a week out, and notice again on the
   way back in?**
