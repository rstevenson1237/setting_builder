# Wild - Hidden

## Decides
What a Hidden-tier location guarantees, and how it hangs off its parent.

## Read at
Step 4c, after every Landmark in the region exists. A Hidden location cannot be written
before its parent, because its connection is written into the parent's Exits.

## Spec

```
WILD - HIDDEN
  1     Parent Landmark, named
  1     The visible detail at the parent that leads here - a mundane Exit, no trigger
  1     Something the parent only implied, now made concrete
  60%   Creature, treasure, trap, or mystery - one, from the element files
  30%   Lore, Key, or Quest involvement
  20%   A further child of its own - a Secret below this one
```

A Hidden location is not found by roaming. It is found by **stopping at a Landmark and
actually looking** - going behind, under, past, or into something the parent's entry
already described. No trigger, no roll: per `setting/Procedures.md`, a stated detail
investigated is a detail found.

The distinction from a Secret is the whole tier: a Hidden way in is *visible and easy to
miss*; a Secret way in is *concealed until acted on*.
