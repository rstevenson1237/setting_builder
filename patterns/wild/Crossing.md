# Wild - Crossing

## Provides
What a Landmark defined by the cost of going around it guarantees, and what currently
controls passing through it: the region's own shape makes going through cheaper than
going around, whoever built or holds it.

## Spec

```
KIND: CROSSING
  1     Crossing - what must be crossed                                     {CROSSING}
  1     Why - why the country will not simply be gone around
  1     Control - what controls or complicates the crossing today
                                             {season | toll | hazard | guardian}
  1     Far side - what waits on the far side, visible before the party commits: a
        territory's edge, a sign of who holds that ground, or nothing at all
  40%   Caught - something else caught here, mid-crossing, when the party arrives
                              {waiting out a season | staffing a post | wreckage}
  30%   Toll - a toll, custom, or right-of-way someone here enforces
  30%   Faction - what controls it is a faction from setting/Factions.md
                                                                  (wild/Faction.md)
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
