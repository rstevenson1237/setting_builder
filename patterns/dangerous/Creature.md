# Dangerous - Creature

## Provides
Which creature fits a DANGEROUS location, how it is here, and at what scale. Scaling is
`patterns/setting/Bestiary.md`'s; an individual the setting keeps consistent is
`patterns/setting/NamedCreatures.md`'s.

## Spec

```
CREATURE
  1     Entry - a setting/Bestiary.md entry, or an inline description where none fits
  1     Shape - how it is here, read off what reaches the party before the species
        does, and off what the Bestiary entry says it does                   {SHAPE}
  1     Number - how many, which the shape has largely already answered; for a swarm,
        what it covers, how fast it spreads, or how long it takes to pass
  1     Scale - against what GENRE.md's Lethality and Player characters answers say the
        party can survive, never against the region die                     {SCALE}
  1     Demeanour - one word for how it carries itself before a fight starts or
        doesn't, for its citation
  25%   Named - a Named Creature, at high weight
```

```
SHAPE - exactly one
  swarm        - many small things moving as one
  pack         - a group that hunts together
  lone hunter  - one, ranging
  patrol       - a group on a route, between places worth patrolling
  sentry       - one or a few on a place or a thing worth standing on
  terrain      - part of the room, until it moves
  searchers    - working the region for something in it
  rivals       - here for what the party came for, which some location here holds
```

```
SCALE - by the weight of the room drawing it
  low          - something the party can walk past or through; often absent
  medium       - a real fight the party is expected to win at some cost
  high         - a fight the party should weigh, and may lose; where its MA sits above
                 its average, how fast the party stops being separate targets
```

## Constraints

- **A shape that contradicts the Bestiary entry is the shape that is wrong.** A solitary
  ambusher drawn as a patrol has been picked for the room rather than read off the
  creature.

- **Never give a swarm a countable number.** A figure turns a condition to get out of into
  a fight won by arithmetic.
