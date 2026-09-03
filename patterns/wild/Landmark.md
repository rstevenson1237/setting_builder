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

## Patterns

**A reason to stop.** A Landmark that offers nothing is scenery with a name. Something has
to reward the four hours it costs to look:

Shelter from weather or pursuit · a vantage over the region · water, in country that is
short of it · a crossing, or the only crossing · fuel, forage, or materials · a mark left
by someone, meant to be read · a body, or the remains of an event · something obviously
built where nothing should be built · an animal sign that means something · a boundary
between two kinds of country · a thing that is wrong for the place it is in.

**Position.** State where it sits: a cardinal bearing from the region's entry, or a
distance and direction from another named Landmark. A party roaming the region has to be
placeable relative to it, and in a point crawl this is the only spatial information they
get.

**Carrying children.** Where a Landmark leads onward, the parent's own entry states the
detail: a Hidden child is reached through something **visible but easy to miss** and
listed as a mundane Exit; a Secret child is reached through a Clue/Trigger/Payload written
into a Feature, and the edge in `Connections.mmd` is marked hidden.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
