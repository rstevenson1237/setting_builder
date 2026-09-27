# Safe - People

## Provides
Somebody from the region's roster, at this location, and what makes them worth
remembering. The roster itself is the Region Overview's People field.

## Spec

```
PERSON
  1     Name, from the region roster - never invented here
  1     What they are doing when the party arrives - never idle
  1     One thing distinctive enough to be recalled a session later - never a physical
        description in full          {a mark | a habit | a possession | a fear |
                                      a competence | a disposition}
  1     What they want, whether or not they are asking for it
  20%   An opinion about the region's Situation that is not the common one
```

## Constraints

- **Never invent a cast.** A location that invents its own people produces a settlement of
  strangers who never meet; somebody needed and not on the roster is added to the roster.
