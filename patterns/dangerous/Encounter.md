# Dangerous - Encounter

## Provides
Which kind of thing the party meets in a DANGEROUS location; the kind file supplies what
fills it. Distinct from `dangerous/Hazard.md`: an encounter has something that can act on
its own account, a hazard only reacts.

## Spec

```
ENCOUNTER
  1     Kind    {creature | named creature | faction}
                        (dangerous/Creature.md, patterns/setting/NamedCreatures.md,
                         dangerous/Faction.md)
  1     What it is doing when the party arrives - not waiting  (genre: creature-activity)
  1     Number, and scale - stated by the kind file that was drawn
  1     A sign of it readable before the encounter itself is met  (genre: creature-sign)
  30%   Something it wants that is not a fight                   (genre: creature-wants)
  25%   Absent when the party arrives - its signs, and where it is instead
```

**The sign is the line that makes an encounter survivable.** Per `GENRE.md`'s lethality
framing the region is not sized to the party, so something they cannot beat announces
itself a room early.

## Constraints

- **Kind is exactly one.** A faction picket that is also a named creature is a faction
  encounter whose leader carries a `setting/NamedCreatures.md` row, not two encounters
  stacked in one Feature.
