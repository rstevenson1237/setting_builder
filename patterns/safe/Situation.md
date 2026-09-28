# Safe - Situation

## Provides
How the region's standing Situation shows at this location, and what its next rung looks
like from here. The Situation itself is the Region Overview's.

## Spec

```
SITUATION - as seen from this location
  1     What is visibly different here because of it
  1     Who here is worse off, by name
  1     Which rung it is on, from the region's Situation field, and what the next rung
        looks like from here if nobody does anything
  40%   Somebody here who benefits, and would rather it continued
                                                     {profit | cover | a rival's loss}
  30%   What this location's people are doing about it, which is usually not enough
  20%   A way the party makes it worse by helping                          {WORSE}
```

```
WORSE - exactly one
  escalation   - helping pushes it up a rung
  tolerance    - helping removes the reason a faction was tolerating this place
  departure    - the party leaves, and the consequences stay
```

## Constraints
