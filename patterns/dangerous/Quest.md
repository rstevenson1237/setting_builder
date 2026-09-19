# Dangerous - Quest

## Provides
How a DANGEROUS location participates in a Quest - almost always as the target end.
Criteria are `patterns/setting/Quests.md`'s; the registry is `setting/Quests.md`.

## Spec

```
QUEST - target end
  1     What this location can supply that someone elsewhere wants
                                        (genre: quest-supply-underground)
  1     What stands in the way of taking it   (genre: quest-obstacles-underground)
  1     A stub row in setting/Quests.md naming this location as target
  30%   Evidence that someone has already tried and failed
                                        (genre: quest-prior-attempt)
```

**Register supply, do not wait for demand.** Record the stub now, even where no giver
exists yet; givers are drafted from what has been registered. Every location's stub exists
before any location file is written, so a giver in another region can name this one by code
and name at 4c, and what it is actually taking is written at 4d.

## Constraints

- **DANGEROUS locations are where quests end, not where they are offered.** A giver in this
  region needs a reason - a prisoner, a rival expedition, something that bargains.
