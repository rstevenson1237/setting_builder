# Wild - Treasure

## Provides
What a WILD location holds to be taken - which registry or table it comes from, why it is
still out here, and what reaching it costs.

## Read at
Step 4c, when a classifier's spec line draws the reward block - `wild/Landmark.md`,
`wild/Hidden.md`, or `wild/Secret.md`. Tables are `setting/Treasure1.md`-`5.md`. This is
the supply end of a Key or a piece of Lore: the object found here. The demand end - a lock
whose key is out here, or a quest given elsewhere that this place carries - is drawn by
the classifier's own registry lines instead.

## Spec

```
TREASURE
  1     What it is    {table roll | unique treasure | lore | key}
                        (patterns/setting/Treasure.md,
                         patterns/setting/UniqueTreasures.md,
                         wild/Lore.md, wild/Key.md)
  1     Why it is still here after weathering
  1     What reaching it costs - climb, dig, wade, carry, or wait
  30%   Something that has a claim on it
```

**Lore and a Key are things a WILD location holds, not hooks it hands out.** Both are
objects found in the open and carried away, which is the reward block's definition, so
both are drawn here rather than as registry lines of their own - the same split
`dangerous/Treasure.md` makes. What stays in registry is the quest a place carries, which
is not an object and cannot be picked up.

**Never name or describe the contents of a table roll.** The cited roll decides them.
Describe what it is in, what has weathered it, and what reaching it costs. This does
**not** apply to a unique treasure, a piece of lore, or a key: each is a stub row in its
own registry, and the row needs a name to be written against.

**Weather is the difference.** A dungeon hoard sits in the dark; a wilderness find has
been rained on. State what condition it is in and why anything survived - buried, sealed,
submerged, sheltered, or recent. A pristine find in open country needs a reason.

**Carrying is a real cost out here.** Four hours per action, distances in miles, and a
party already loaded. Bulk that would be trivial in a dungeon is a decision in the field.

**Contract.** A WILD treasure find owes: what it is, why it survived weathering, and what
reaching it costs. Genre-neutral and permanent. What it actually is and who
might claim it is not - the Examples below are this build's compile of it, from this
setting's chosen genre reference.

## Design patterns

**Which table**
- **I - Scavenged Loot** - the default. What washes up, what is dropped, what is left at a
  camp, what is worth stooping for and not worth a detour.
- **II - Equipment and Armaments** - a body and what it still carries; a cache left by
  somebody who meant to come back; what a predator dragged home with its meal.
- **III - Gems and Jewelry** - grave goods; a purse buried at a boundary; something that
  came out of the ground with the spoil and was never noticed.
- **IV - Luxury and Trade Goods** - a load that never arrived. A wreck, an overturned cart,
  a pack animal's burden, a caravan's abandoned surplus.
- **V - Treasure Cache** - rare in WILD, and always attached to a Secret-tier location or
  a lair with a long tenancy.

**Why it survived** - buried and only now exposed; under water and preserved by cold; in a
sealed container; sheltered by the thing that fell on it; too heavy to have been carried
off; guarded until recently; nobody has come this way since; taken by an animal that does
not know what it is.

**Claims on it** - the animal that nested in it; the people who buried it and mark the
spot; a faction that considers this country theirs; whoever is coming back for it, and how
soon; the person it was taken from, still findable.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
