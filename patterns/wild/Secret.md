# Wild - Secret

## Decides
What a Secret-tier location guarantees, and the trigger that reveals it.

## Read at
Step 4c, last of the three tiers, after its parent Landmark or Hidden location exists.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Where a line names a file in parentheses,
that is the only other file this line requires.

```
WILD - SECRET
  1     Dressing and Secrets, unconditional              (wild/Dressing.md, wild/Secrets.md)
  1     Parent location, named
  1     Clue    - already visible in the parent's own Features
  1     Trigger - the specific action at the parent that reveals the way
  1     Payload - the connection to this whole location
  1     A reason it was worth concealing
  70%   Creature, treasure, trap, or mystery - one      (wild/Creature.md, wild/Trap.md,
                                                        wild/Treasure.md, wild/Mystery.md)
  40%   Lore, Key, or Quest involvement                 (wild/Lore.md, wild/Key.md,
                                                        wild/Quest.md)
```

The Clue/Trigger/Payload here is the same shape as a feature-level Secret, scaled up: the
Payload is an Exit to an entire location rather than a detail inside one. Mark the edge
hidden (`-.-`) in the region's `Connections.mmd`.

Unlike a feature-level Secret, this is **mandatory, not rated** - a Secret-tier location
without a stated Clue at its parent is unreachable, and unreachable content is content
that does not exist.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
