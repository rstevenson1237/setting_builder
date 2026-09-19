# Safe - Faction

## Provides
How a power in `setting/Factions.md` shows itself inside a settlement, where it cannot
simply take what it wants. Distinct from `dangerous/Faction.md`: a held position at depth
is a garrison; in a settlement it is influence, and influence is visible in different
things.

## Spec

```
FACTION PRESENCE - in a settlement
  1     Which faction, and what it wants from this place
                                                (genre: faction-wants-settlement)
  1     Something visible that identifies them without naming them
                                                (genre: faction-signs)
  1     Who here is theirs, and whether the settlement knows
                                                (genre: faction-agents)
  1     What the settlement gets in return for tolerating it
                                                (genre: faction-payoff)
  40%   A rival's presence, and how the two avoid open trouble
                                                (genre: faction-friction)
  30%   Something they are doing here that they would rather not be seen doing
  20%   Somebody who used to be theirs
```

## Constraints

- **A faction in a settlement is never the settlement's own authority.** What it holds here
  is leverage over somebody who is, and that somebody is named.
