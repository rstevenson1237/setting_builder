# Wild - Landmark

## Provides
What a Landmark-tier location guarantees, and whether it carries children.

## Read at
Step 4c, for a WILD location its stub marks landmark. Generate all Landmarks before any
Hidden or Secret location, since each child's connection is written into its parent.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Where a line names a file in parentheses,
that is the only other file this line requires.

```
WILD - LANDMARK
  1     Dressing and Secrets, unconditional              (wild/Dressing.md, wild/Secrets.md)
  1     Kind                        {Ruin | Lair | Natural Feature | Crossing}
                                                        (wild/Ruin.md, wild/Lair.md,
                                                        wild/NaturalFeature.md,
                                                        wild/Crossing.md)
  1     Position within the region - a bearing from the entry or another named Landmark
  1     A reason to stop, visible from outside
  40%   A visible detail leading onward to a Hidden child
  50%   Creature, treasure, trap, or mystery - one      (wild/Creature.md, wild/Trap.md,
                                                        wild/Treasure.md, wild/Mystery.md)
  20%   Lore, Key, or Quest involvement                 (wild/Lore.md, wild/Key.md,
                                                        wild/Quest.md)
```

**A Landmark can be named, revisited, and connected to.** That is the test, and it is what
separates a Landmark from terrain. A stretch of eroded slope, a brook, a field of flowers
- these are what the region looks like, they belong in the Region Overview's Terrain
field, and writing them as locations wastes a slot the region cannot spare.

Every Landmark is freely discoverable by roaming the region. None of them is hidden behind
another, and none requires being led there.

## Constraints

- **A Crossing is chosen for what it costs to go around, not for who built or lives
  there.** Its physical form can be a Ruin's (a bridge, a causeway), a Natural Feature's
  (a ford, a pass), or held like a Lair - Kind is exactly one, so pick Crossing when the
  location's point is that the region's own shape forces the party through it; pick Ruin
  or Natural Feature instead when the same object's point is its history or its
  strangeness and the route through it is incidental.
