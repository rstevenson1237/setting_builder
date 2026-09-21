# Wild - Treasure

## Provides
What a WILD location holds to be taken - which registry or table it comes from, why it is
still out here, and what reaching it costs.

Tables are `setting/Treasure1.md`-`5.md`. This is the supply end of a Key or a piece of
Lore: the object found here. The demand end - a lock whose key is out here, or a quest
given elsewhere that this place carries - is drawn by the classifier's own registry
lines instead.

## Spec

```
TREASURE
  1     What it is - exactly one, drawn at these rates rather than freely chosen
        {table roll 45% | key 30% | lore 20% | unique treasure 5%}
                        (patterns/setting/Treasure.md,
                         wild/Key.md, wild/Lore.md,
                         patterns/setting/UniqueTreasures.md)
  1     Why it is still here after weathering
  1     What reaching it costs - climb, dig, wade, carry, or wait
  30%   Something that has a claim on it - an animal that nested in it, whoever
        buried it, a faction that considers this country theirs, or whoever is
        coming back for it
```

**The key rate is highest here, and that is the point.** Per `wild/Key.md`, open country
is where a key gets separated from its lock - a key found in the wild points a party at a
dungeon they may not have heard of yet, which is the one thing a WILD region can do that
neither of the others can. An unrated menu would never produce it: the table roll is
always the cheapest option to write, so it wins every draw that does not weight against
it.

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

## Constraints
