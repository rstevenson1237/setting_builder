# Wild - Secret

## Provides
What a Secret-tier location guarantees, and the trigger that reveals it.

## Read at
**Mode: entry.** Step 4c, last of the three tiers, after its parent Landmark or Hidden
location exists.
## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Every line is either an edge - it names a
file in parentheses, the only other file that line requires - or a question the generator
answers here.

```
WILD - SECRET

  -- substrate: what this place is
  1     Dressing - what it is, and what weather has done to it       (wild/Dressing.md)
  1     Kind   {ruin | lair | natural feature}      (wild/Ruin.md, wild/Lair.md,
                                                     wild/NaturalFeature.md)
  1     Secrets - whether it conceals anything                       (wild/Secrets.md)

  -- access: how the party comes to be standing here
  1     Parent location, named
  1     Clue    - already visible in the parent's own Features
  1     Trigger - the specific action at the parent that reveals the way
  1     Payload - the connection to this whole location
  1     A reason it was worth concealing

  -- challenge: what opposes the party
  40%   Challenge   {creature | hazard | mystery}    (wild/Creature.md, wild/Hazard.md,
                                                      wild/Mystery.md)

  -- reward: what is here to take
  40%   Treasure                                                     (wild/Treasure.md)

  -- registry: what ties this place to somewhere else
  20%   This location's carrying role in a quest given elsewhere     (wild/Quest.md)

  1     Naming, after everything above                               (wild/Naming.md)
```

The Clue/Trigger/Payload here is the same shape as a feature-level Secret, scaled up: the
Payload is an Exit to an entire location rather than a detail inside one. Mark the edge
hidden (`-.-`) in the region's `Connections.mmd`.

Unlike a feature-level Secret, this is **mandatory, not rated** - a Secret-tier location
without a stated Clue at its parent is unreachable, and unreachable content is content
that does not exist.

Its rated lines come to one Feature against a Hidden location's 0.8 and a Landmark's 0.6,
and the reward rate is the highest of the three. A place a party had to notice a clue and
act on it to reach is the tier's last chance to pay them for that, and nothing below it
will.

## Constraints

- **A Secret-tier location is the end of a chain, not a link in one.** It carries no
  child of its own, which is why it has no lead line where `wild/Landmark.md` and
  `wild/Hidden.md` have one. Depth in a WILD region runs Landmark to Hidden to Secret and
  stops - a clue at a parent that itself has to be found by acting on a clue is two
  triggers deep and will not be reached. `region/Wild.md`'s topology states the same rule
  on the graph side, where it is enforceable.
