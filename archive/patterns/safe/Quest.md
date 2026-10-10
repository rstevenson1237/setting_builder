# Safe - Quest

## Provides
The giver end of a quest: who asks, what they want, what they offer, and what they leave
out. What earns a Quests row is `patterns/setting/Quests.md`'s.

## Spec

```
QUEST - giver end
  1     Giver - who asks, drawn from the region's People roster
  1     Reluctance - why they will not go themselves: a real reason, never convenience
  1     Object - what specifically they want
  1     Target - which location holds it, by code
  1     Terms - in the giver's own words: the payment and the payer in one line
  1     Quests row - a stub row, or an addition to an existing row, in setting/Quests.md
  40%   Omission - something they have not mentioned, and know they have not
                                                                        {OMISSION}
  30%   Deadline - a deadline, and what happens after it
  20%   Asked already - somebody else has been asked already
```

```
OMISSION - exactly one
  attempt      - somebody went before, and did not come back
  rival        - somebody else wants it too
  right        - they have no right to what they are asking for
  payment      - what they offer is not theirs to give
```

## Constraints
