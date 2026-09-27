# Dangerous - Faction

## Provides
What it means for a DANGEROUS location to be held rather than merely inhabited: a picket
killed at its post is noticed, missed, replaced or avenged, where a beast killed in its den
is only killed. What lives in a room on its own account is `dangerous/Creature.md`'s.

## Spec

```
FACTION PRESENCE
  1     Which faction, and what this position is for                        {POSITION}
  1     Something visible that identifies them without naming them - its Identity from
        setting/Factions.md, repeated on gear, dress or work
  1     What happens elsewhere if this position is lost or alarmed
  50%   A standing order they are following, which the party can read or overhear
  30%   Friction                  {with another faction | with the region | within}
  20%   Someone here who would rather be somewhere else
```

```
POSITION - exactly one
  watch        - to watch something
  way          - to hold a way open or shut
  work         - to work or store something
  keep         - to keep something alive, or contained
  foothold     - a foothold not yet held
```

## Constraints
