# Dangerous - Creature

## Decides
Which creature fits a DANGEROUS location, at what scale, and what its presence implies
about the rest of the region.

## Read at
Step 4c, when a weight file's spec draws a creature. Scaling is in
`setting/Procedures.md`; entries are in `setting/Bestiary.md`.

## Spec

```
CREATURE
  1     Bestiary entry, or an inline description where none fits
  1     What it is doing when the party arrives - not waiting
  1     Number - how many, which is half the pitch
  1     Scale, against party altitude in setting/Bestiary.md - never against the region die:
          low weight     something the party can walk past or through; often absent
          medium weight  a real fight the party is expected to win at some cost
          high weight    a fight the party should weigh, and may lose. MA where it has it
  25%   A Named Creature, at high weight
  30%   Something it wants that is not a fight
  25%   Absent when the party arrives - signs of it, and it is elsewhere in the region
```

**Presence is rolled apart from description.** A location's occupant is not always at
home. A room written as a den, found empty, with the thing that lives in it somewhere
behind the party, is worth more than the same room with the thing standing in it - and it
is what makes a wandering-monster result mean something.

A creature named directly in its Feature line needs no citation syntax. If no Bestiary
entry fits, describe the creature inline - the Bestiary holds only what recurs.

**High weight does not mean beatable.** Some of what a region holds is not meant to be
fought, and the region is not sized to the party. Where a location's creature is one of
those, its Bestiary **Sign** and **Disposition** carry the warning - and they must reach
the party a room early, so the choice to withdraw is a judgement they got to make.

## Patterns

**What it is doing** - eating; sleeping; working at something; moving something heavy;
arguing; grooming or being groomed; tending young; watching a thing that is not the door;
repairing what the last intruders broke; already wounded from something else in the region.

**Household** - a region with living occupants has the logistics of living in it, and they
are worth a location each: where the food is; where the water comes from; where the waste
goes; where the young are; where the dead go. These are the questions that turn a dungeon
into somewhere something lives, and they hand players non-combat leverage - the well, the
stores, the nursery.

**Relations** - what it eats and what eats it; what it will not go near, and why; what it
tolerates that the party would not expect; who it answers to elsewhere in the region; what
it would trade for.

**Presence without encounter** - tracks, spoor, a kill, a shed skin, a territorial mark, a
smell that arrives before the thing does, a sound heard two rooms away. A creature's
signs should reach the party before the creature does, at least once per region.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
