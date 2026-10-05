# Dangerous - Quest

## Provides
The target end of a quest in a DANGEROUS location: what it holds that someone elsewhere
wants. What earns a Quests row is `patterns/setting/Quests.md`'s.

## Spec

```
QUEST - target end
  1     Supplies - what this location can supply that someone elsewhere wants
                        {a substance | a body, or proof of one | an object |
                         a name or word recorded nowhere else | a person |
                         a confirmation that something is true}
  1     Obstacle - what stands in the way of taking it
                        {it lives | it is guarded | taking it breaks it |
                         taking it is noticed | someone else is already here for it}
  1     Quests row - a stub row in setting/Quests.md naming this location as target,
        whether or not a giver exists yet
  30%   Tried - evidence that someone has already tried and failed: what they left
        behind, still findable
```

## Constraints

- **Never a giver here without a reason to be here.** A prisoner, a rival expedition,
  something that bargains; DANGEROUS locations are where quests end.
