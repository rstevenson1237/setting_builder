# Wild - Landmark

## Decides
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
  1     Kind                        {Ruin | Lair | Natural Feature} - see the KIND blocks
                                                        below
  1     Position within the region - a bearing from the entry or another named Landmark
  1     A reason to stop, visible from outside
  40%   A visible detail leading onward to a Hidden child
  50%   Creature, treasure, trap, or mystery - one      (wild/Creature.md, wild/Trap.md,
                                                        wild/Treasure.md, wild/Mystery.md)
  20%   Lore, Key, or Quest involvement                 (wild/Lore.md, wild/Key.md,
                                                        wild/Quest.md)
```

```
KIND: RUIN                                        (content in wild/Ruin.md)
  1     What it was, and roughly when
  1     What state it is in now, and what did that to it
  1     Whether anything holds it now
  40%   A second occupancy between the builders and now
  30%   Something the builders did that nobody does any more
  20%   A name in an older tongue, per wild/Naming.md
```

```
KIND: LAIR                                        (content in wild/Lair.md)
  1     What lives here, from setting/Bestiary.md
  1     The territory it claims, and how far that reaches
  1     A sign of it readable before the lair itself is reached
  1     What it eats, and where that comes from
  40%   Young, stores, or dependants - a reason it cannot simply leave
  30%   Absent when the party arrives, and elsewhere in the region
  30%   A child location: the den proper, the midden, the larder, the killing ground
```

```
KIND: NATURAL FEATURE                             (content in wild/NaturalFeature.md)
  1     What it physically is, and its scale in yards
  1     Why a party would stop - shelter, water, vantage, materials, or a crossing
  1     One way it is not like the country around it
  30%   Something mysterious about it, priced or dangerous to use, per GENRE.md
  30%   A resource findable here, tied to the region's Foraging field
  20%   A hazard that is simply part of the place
```

**A Landmark can be named, revisited, and connected to.** That is the test, and it is what
separates a Landmark from terrain. A stretch of eroded slope, a brook, a field of flowers
- these are what the region looks like, they belong in the Region Overview's Terrain
field, and writing them as locations wastes a slot the region cannot spare.

Every Landmark is freely discoverable by roaming the region. None of them is hidden behind
another, and none requires being led there.

**Ruin condition is the storytelling.** A tower thrown down is a different story from a
tower abandoned, which is different from a tower still roofed and empty. State what
happened to it, not just that it is ruined.

**A Lair is the tier's natural place to carry depth.** Complexity comes from attaching
children rather than from writing the parent heavier - a lair decomposes into children more
readily than any other kind, because a thing that lives somewhere lives across several
spaces. **Territory is what makes a lair matter to the region**: a den nobody can find is a
room; a den whose owner ranges three landmarks in every direction is a fact about the whole
region.

**A Natural Feature is the hardest kind to write well** - it has no builder and no
occupant, so unlike a Ruin or a Lair it has to earn its slot on what it *does* alone.
