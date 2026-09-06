# Dangerous - Medium

## Decides
What a medium-weight location guarantees.

## Read at
Step 4c, for a location its gazetteer stub marks medium.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Where a line names a file in parentheses,
that is the only other file this line requires.

```
DANGEROUS - MEDIUM
  1     Dressing and Secrets, unconditional           (dangerous/Dressing.md,
                                                        dangerous/Secrets.md)
  1     Challenge - guaranteed, and obvious   {creature | trap}
                                                       (dangerous/Creature.md,
                                                        dangerous/Trap.md)
  50%   Treasure, if the challenge is a creature       (dangerous/Treasure.md)
  33%   Treasure, if the challenge is a trap           (dangerous/Treasure.md)
  25%   A detail that foreshadows a HIGH location elsewhere in the region
  20%   Lore, in place of treasure rather than alongside it   (dangerous/Lore.md)
```

Medium weight means the location presents **one thing to deal with**, and presents it
plainly. A challenge the party cannot see is not a medium-weight challenge - a room built
on a concealed trap presents as empty, and belongs at low weight with the trap as its
variance.

The treasure rates are conditional on the challenge because reward should follow the
fiction: a thing that lives here has accumulated something, a mechanism has not.
