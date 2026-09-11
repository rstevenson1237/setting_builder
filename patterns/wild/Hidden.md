# Wild - Hidden

## Provides
What a Hidden-tier location guarantees, and how it hangs off its parent.

## Read at
Step 4c, after every Landmark in the region exists. A Hidden location cannot be written
before its parent, because its connection is written into the parent's Exits.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Where a line names a file in parentheses,
that is the only other file this line requires.

```
WILD - HIDDEN
  1     Dressing and Secrets, unconditional              (wild/Dressing.md, wild/Secrets.md)
  1     Parent Landmark, named
  1     The visible detail at the parent that leads here - a mundane Exit, no trigger
  1     Something the parent only implied, now made concrete
  60%   Creature, treasure, trap, or mystery - one      (wild/Creature.md, wild/Trap.md,
                                                        wild/Treasure.md, wild/Mystery.md)
  30%   Lore, Key, or Quest involvement                 (wild/Lore.md, wild/Key.md,
                                                        wild/Quest.md)
  20%   A further child of its own - a Secret below this one   (wild/Secret.md)
```

A Hidden location is not found by roaming. It is found by **stopping at a Landmark and
actually looking** - going behind, under, past, or into something the parent's entry
already described. No trigger, no roll: per `setting/Procedures.md`, a stated detail
investigated is a detail found.

The distinction from a Secret is the whole tier: a Hidden way in is *visible and easy to
miss*; a Secret way in is *concealed until acted on*.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
