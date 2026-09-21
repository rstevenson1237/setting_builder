# Dangerous - Creature

## Provides
Which creature fits a DANGEROUS location, at what scale, and what its presence implies
about the rest of the region.

Scaling is in `patterns/setting/Bestiary.md`; entries are in `setting/Bestiary.md`.
Distinct from `patterns/setting/NamedCreatures.md`, the kind drawn for an individual the
setting keeps consistent across appearances.

## Spec

```
CREATURE
  1     Bestiary entry, or an inline description where none fits
  1     Shape - how it is here, which is what the party reads before they read a species
        {swarm | pack | lone hunter | patrol, on a route | sentry, on a place or a thing
         | part of the terrain, until it moves | searchers, working the region for
         something | rivals, here for what the party came for}
  1     What it is doing when the party arrives - not waiting
  1     Number - how many, which is half the pitch, and which the shape has largely
        already answered
  1     Scale, against party altitude, per GENRE.md - never against the region die:
          low weight     something the party can walk past or through; often absent
          medium weight  a real fight the party is expected to win at some cost
          high weight    a fight the party should weigh, and may lose - and where its MA
                         sits above its average, how fast the party stops being separate targets
  25%   A Named Creature, at high weight
  30%   Something it wants that is not a fight
  25%   Absent when the party arrives - signs of it, and it is elsewhere in the region
```

**The region's die says nothing about what to put here.** It is a difficulty die - 1 =
failure, 2-3 = complication, 4+ = success, so a *smaller* die is *harder* - and AD is a
power count on a separate axis. A d8 DANGEROUS region does not want an 8 AD creature.

**Shape decides the sign, the spacing and the number; the species decides what happens
when it is reached.** A pack seen at distance and a swarm coming down a corridor are the
same Bestiary row met two entirely different ways, and only one of them is a fight in a
room. Draw the shape against what the location is - a patrol wants somewhere to patrol
between, a sentry wants a thing worth standing on, searchers want something in the region
worth being after - and against what the Bestiary entry says the creature actually does.
**A shape is read off what reaches the party before the species does** - a sound or smell
with no front, a spacing pattern, a beaten route, a held position - never a description
of the creature itself.

**Rivals are drawn against the region's own reward.** What they are after is something a
location here holds, so the party can get there first, buy them off, follow them, or let
them spring what is waiting. What they are after is never named as the thing the party is
supposed to lose.

**Presence is rolled apart from description.** A location's occupant is not always at
home. A room written as a den, found empty, with the thing that lives in it somewhere
behind the party, is worth more than the same room with the thing standing in it - and it
is what makes a wandering-monster result mean something. Where it is drawn absent, what a
party notices is its passage, not its presence - what it left rather than what it is.

A creature named directly in its Feature line needs no citation syntax. If no Bestiary
entry fits, describe the creature inline - the Bestiary holds only what recurs. A Demeanor
word for the Bestiary citation format names how it carries itself before a fight starts or
doesn't - a posture read at a glance, distinct from what the species is capable of.

**High weight does not mean beatable.** Some of what a region holds is not meant to be
fought, and the region is not sized to the party. Where a location's creature is one of
those, its Bestiary **Sign** and **Disposition** carry the warning - and they must reach
the party a room early, so the choice to withdraw is a judgement they got to make.

**A region with living occupants has the logistics of living in it**, and they are worth a
location each: where the food is, where the water comes from, where the waste goes, where
the young are, where the dead go. These are the questions that turn a dungeon into
somewhere something lives, and they hand players non-combat leverage - a household's own
wants and relations, drawn against what it eats, what eats it, what it will not go near,
and who it answers to elsewhere in the region, are what make it native to this room rather
than any other.

## Constraints

- **A shape that contradicts the Bestiary entry is the shape that is wrong.** A solitary
  ambusher drawn as a patrol has been picked for the room rather than read off the creature,
  and every later line written from it inherits the error.

- **Rivals belonging to something with a name elsewhere are a faction, not a creature.**
  Draw them at `dangerous/Faction.md`, so what they answer to and what they want are the
  faction's and stay consistent the next time the party meets them.

- **Terrain that only costs is not a creature.** Something that never acts on its own
  account, wants nothing, and can only be endured or routed around is an environmental
  hazard and belongs at `dangerous/Environmental.md`. What makes terrain a creature is that
  it stops being terrain.

- **Never give a swarm a countable number.** Its Number line states what it covers, how
  fast it is spreading, or how long it takes to pass - a figure invites a roster, and a
  roster turns a condition the party has to get out of into a fight they can win by
  arithmetic.
