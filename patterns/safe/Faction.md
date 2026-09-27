# Safe - Faction

## Provides
How a power in `setting/Factions.md` shows itself inside a settlement, where it cannot
simply take what it wants. A held position at depth is `dangerous/Faction.md`'s; in a
settlement it is influence, and influence shows in different things.

## Spec

```
FACTION PRESENCE - in a settlement
  1     Which faction, and what it wants from this place                       {WANT}
  1     Something visible that identifies it without naming it - its Identity from
        setting/Factions.md, repeated on dress, goods or work rather than stated
  1     Who here is theirs, and whether the settlement knows       {openly | hidden}
  1     What the settlement gets in return for tolerating it
                             {coin | protection | a market | news | a rival kept off}
  40%   A rival's presence, and how the two avoid open trouble
                          {an unstated agreement | a line neither crosses | a bidding war}
  30%   Something they are doing here that they would rather not be seen doing
  20%   Somebody who used to be theirs
```

```
WANT - exactly one
  route        - a way through
  supply       - something the settlement produces
  recruits     - people
  watched      - a person kept under watch
  knowledge    - what the settlement knows
  legitimacy   - the settlement's acknowledgement
  exclusion    - a rival kept out
```

## Constraints

- **Never a presence with no exchange.** A faction here that gives the settlement nothing
  for tolerating it is an occupation, and that is a Situation.
