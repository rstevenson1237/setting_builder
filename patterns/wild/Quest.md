# Wild - Quest

## Provides
The carrying end of a quest: where it is travelled through, obstructed, or offered by
somebody living rough. What earns a Quests row is `patterns/setting/Quests.md`'s.

## Spec

```
QUEST - carrying end
  1     Role                                                                 {ROLE}
  1     Quests row - a stub row, or an addition to an existing row, in setting/Quests.md
  30%   Others - evidence of somebody else on the same errand, ahead or behind
                                        {a camp | a marker cut twice | a party}
```

```
ROLE - exactly one
  waypoint     - a stop on the way
  obstacle     - what stands in the way, en route: the crossing that is out, the
                 country that must be gone around, the thing that holds the only path
  supply       - something only found here
  giver        - somebody with a reason to be out here, and an ask too small and
                 personal for a settlement, rarely paid in coin
```

## Constraints
