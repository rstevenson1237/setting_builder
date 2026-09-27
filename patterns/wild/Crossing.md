# Wild - Crossing

## Provides
What a Landmark defined by the cost of going around it guarantees, and what currently
controls passing through it: the region's own shape makes going through cheaper than
going around, whoever built or holds it.

## Spec

```
KIND: CROSSING
  1     What must be crossed, and why the country will not simply be gone around
                                                                       {CROSSING}
  1     What controls or complicates the crossing today
                                             {season | toll | hazard | guardian}
  1     What waits on the far side, visible before the party commits - a territory's
        edge, a sign of who holds that ground, or nothing at all
  40%   Something else caught here, mid-crossing, when the party arrives
                              {waiting out a season | staffing a post | wreckage}
  30%   A toll, custom, or right-of-way someone here enforces
  30%   What controls it is a faction from setting/Factions.md        (wild/Faction.md)
```

```
CROSSING - exactly one
  ford         - water crossable at one place
  bridge       - a built way over
  gate         - a built way through
  pass         - a way through high ground, open only part of the year
  exposure     - open ground with nothing to hide behind
```

## Constraints
