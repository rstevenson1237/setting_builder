# Wild - Landmark

## Decides
What a Landmark-tier location guarantees, and whether it carries children.

## Read at
Step 4c, for a WILD location its stub marks landmark. Generate all Landmarks before any
Hidden or Secret location, since each child's connection is written into its parent.

## Spec

```
WILD - LANDMARK
  1     Kind, from Ruin.md, Lair.md, or NaturalFeature.md
  1     Position within the region - a bearing from the entry or another named Landmark
  1     A reason to stop, visible from outside
  40%   A visible detail leading onward to a Hidden child
  20%   A Clue that a Secret is here, per wild/Secrets.md
  50%   Creature, treasure, trap, or mystery - one, from the element files
  20%   Lore, Key, or Quest involvement
```

**A Landmark can be named, revisited, and connected to.** That is the test, and it is what
separates a Landmark from terrain. A stretch of eroded slope, a brook, a field of flowers
- these are what the region looks like, they belong in the Region Overview's Terrain
field, and writing them as locations wastes a slot the region cannot spare.

Every Landmark is freely discoverable by roaming the region. None of them is hidden behind
another, and none requires being led there.
