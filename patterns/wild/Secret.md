# Wild - Secret

## Provides
What a Secret-tier location guarantees, and the trigger that reveals it.

## Spec

```
WILD - SECRET

  -- substrate: what this place is
  1     Dressing - what it is, and what weather has done to it       (wild/Dressing.md)
  1     Kind   {ruin | lair | natural feature}      (wild/Ruin.md, wild/Lair.md,
                                                     wild/NaturalFeature.md)
  20%   A concealed detail inside this location - a second triple, not the access one
        below:
          Clue    - in this location's own Dressing, never the parent's
          Trigger - a stated act here
          Payload - never another location: a cache, a piece of Lore, a Key, or why this
                    place was worth concealing

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

  1     Naming, after everything above                (patterns/setting/Naming.md)
```

**This file carries two Clue/Trigger/Payload triples and they do different work.** The
access triple is the location itself: its Clue sits in the *parent's* Features, and its
Payload is an Exit to this whole place. Mark that edge hidden (`-.-`) in the region's
`Connections.mmd`. The rated triple in the substrate block is an ordinary concealed detail,
wholly inside this location. Writing one where the other belongs is how a Secret location
ends up either unreachable or reached twice.

Unlike a feature-level Secret, the access triple is **mandatory, not rated**. Its rated
lines come to one Feature against a Hidden location's 0.8 and a Landmark's 0.6, and the
reward rate is the highest of the three: a place a party had to notice a clue and act on it
to reach is the tier's last chance to pay them for that.

## Constraints

- **A Secret-tier location is the end of a chain, not a link in one.** It carries no child
  of its own, which is why it has no lead line where `wild/Landmark.md` and
  `wild/Hidden.md` have one. A clue at a parent that itself has to be found by acting on a
  clue is two triggers deep and will not be reached.
