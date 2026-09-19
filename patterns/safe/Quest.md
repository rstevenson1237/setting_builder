# Safe - Quest

## Provides
How a SAFE location gives a quest: who asks, what they want, what they offer, and what they
leave out. SAFE **gives** - this is the giver end. Criteria are in
`patterns/setting/Quests.md`; the registry is `setting/Quests.md`.

## Spec

```
QUEST - giver end
  1     Who asks, drawn from the region's People roster
  1     Why they will not go themselves - and it must be a real reason
                                                        (genre: quest-refusals)
  1     What specifically, and which location holds it, by code and name
                                                        (genre: quest-objects)
  1     The terms, stated in the giver's own words       (genre: quest-terms)
  1     A stub row or an addition to an existing row in setting/Quests.md
  40%   Something they have not mentioned, and know they have not
                                                        (genre: quest-omissions)
  30%   A deadline, and what happens after it            (genre: quest-deadlines)
  20%   Somebody else has been asked already
```

**Deadlines are what make a party choose between two hooks**, which is the point of having
more than one.

## Constraints

- **An omission is something the giver knows and is withholding, never an error.** A giver
  who is simply mistaken has no leverage and nothing to be confronted with later.
