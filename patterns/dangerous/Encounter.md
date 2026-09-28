# Dangerous - Encounter

## Provides
What the party meets in a DANGEROUS location, what it is doing, and what reaches them
before it does. Which kind is decided here; the kind file supplies what fills it. An
encounter can act on its own account, where `dangerous/Hazard.md` only reacts.

## Spec

```
ENCOUNTER
  1     Kind    {creature | named creature | faction}
                        (dangerous/Creature.md, patterns/setting/NamedCreatures.md,
                         dangerous/Faction.md)
  1     What it is doing when the party arrives - never waiting
  1     Number, and scale - stated by the kind file that was drawn
  1     A sign of it readable before the encounter itself is met - a room early where
        GENRE.md's Lethality answer means it could kill them
  30%   Something it wants that is not a fight
  25%   Absent when the party arrives - its signs, and where it is instead
```

## Constraints
