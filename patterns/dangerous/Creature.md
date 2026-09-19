# Dangerous - Creature

## Provides
Which creature fits a DANGEROUS location, at what scale, and what its presence implies
about the rest of the region. Scaling is `patterns/setting/Bestiary.md`'s; an individual
the setting keeps consistent across appearances is `patterns/setting/NamedCreatures.md`'s.

## Spec

```
CREATURE
  1     Bestiary entry, or an inline description where none fits, and the demeanour it
        carries here                                            (genre: demeanours)
  1     Shape - how it is here, which is what the party reads before they read a species
                                                                (genre: creature-shapes)
  1     What it is doing when the party arrives - not waiting  (genre: creature-activity)
  1     Number - how many; a swarm takes no count, and states what it covers and how fast
        it is spreading
  1     Scale, against party altitude, per GENRE.md - never against the region die:
          low weight     something the party can walk past or through; often absent
          medium weight  a real fight the party is expected to win at some cost
          high weight    a fight the party should weigh, and may lose - and where its MA
                         sits above its average, how fast the party stops being separate targets
  25%   A Named Creature, at high weight
  30%   Something it wants that is not a fight                   (genre: creature-wants)
  25%   Absent when the party arrives - its signs, and it is elsewhere in the region
                                                                  (genre: creature-sign)
```

**The region's die says nothing about what to put here.** It is a difficulty die - a
*smaller* die is *harder* - and AD is a power count on a separate axis.

**Draw the shape against the location, then against the entry.** A patrol wants somewhere
to patrol between, a sentry a thing worth standing on, searchers something in the region
worth being after.

**High weight does not mean beatable.** Where the creature is not meant to be fought, its
Bestiary Sign and Disposition carry the warning, a room early.

## Constraints

- **A shape that contradicts the Bestiary entry is the shape that is wrong.** It has been
  picked for the room rather than read off the creature, and every later line written from
  it inherits the error.

- **Rivals belonging to something named elsewhere are a faction.** Draw them at
  `dangerous/Faction.md`, so what they answer to stays consistent the next time the party
  meets them. What they are after is never the thing the party is supposed to lose.

- **Terrain that only costs is not a creature.** Something that wants nothing and can only
  be endured or routed around is `dangerous/Environmental.md`'s. What makes terrain a
  creature is that it stops being terrain.
