# Safe - Quest

## Provides
The giver end of a quest: who asks, what they want, what they offer, and what they leave
out. What earns a Quests row is `patterns/setting/Quests.md`'s.

## Spec

```
QUEST - giver end
  1     Who asks, drawn from the region's People roster
  1     Why they will not go themselves - a real reason, never convenience
  1     What specifically, and which location holds it, by code and name
  1     The terms, in the giver's own words - the payment and the payer in one line
  1     A stub row, or an addition to an existing row, in setting/Quests.md
  40%   Something they have not mentioned, and know they have not           {OMISSION}
  30%   A deadline, and what happens after it
  20%   Somebody else has been asked already
```

```
OMISSION - exactly one
  attempt      - somebody went before, and did not come back
  rival        - somebody else wants it too
  right        - they have no right to what they are asking for
  payment      - what they offer is not theirs to give
```

## Constraints

- **Never a target that is not a real location.** Every location exists as a gazetteer
  stub before any is written, so a giver names one by code.
