# Dangerous - Encounter

## Provides
What the party meets in a DANGEROUS location, what it is doing, and what reaches them
before it does.

## Read at
**Mode: ingredient.** Step 4c, when a weight file's spec draws a challenge and the
challenge is an encounter, or when `dangerous/Treasure.md` draws a guard. Which *kind*
of encounter is decided here; the kind file supplies what fills it. Distinct from
`dangerous/Hazard.md`: an encounter has something that can act on its own account, a
hazard only reacts.
## Spec

```
ENCOUNTER
  1     Kind    {creature | named creature | faction}
                        (dangerous/Creature.md, patterns/setting/NamedCreatures.md,
                         dangerous/Faction.md)
  1     What it is doing when the party arrives - not waiting
  1     Number, and scale against party altitude per GENRE.md - never the region die
  1     A sign of it readable before the encounter itself is met
  30%   Something it wants that is not a fight
  25%   Absent when the party arrives - its signs, and where it is instead
```

**The sign is the line that makes an encounter survivable.** A party that meets a thing
with no warning has had a choice taken from them. Per `GENRE.md`'s lethality framing the
region is not sized to the party, so something a party cannot beat has to announce itself
a room early - and the sign line is where that happens, whichever kind was drawn.

**Presence is decided apart from description.** A location's occupant is not always at
home. A room written as a den, found empty, with the thing that lives in it somewhere
behind the party, is worth more than the same room with the thing standing in it.

**Scale is against what the characters can survive, never against the region die.** The
die is a difficulty die; AD is a power count on a separate axis.

## Constraints

- **Kind is exactly one.** A faction picket that is also a named creature is a faction
  encounter whose leader carries a `setting/NamedCreatures.md` row, not two encounters
  stacked in one Feature.
