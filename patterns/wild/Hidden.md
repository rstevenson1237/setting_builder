# Wild - Hidden

## Provides
What a Hidden-tier location guarantees, and how it hangs off its parent.

## Spec

```
WILD - HIDDEN

  -- substrate: what this place is
  1     Dressing - what it is, and what weather has done to it       (wild/Dressing.md)
  1     Kind   {ruin | lair | natural feature}      (wild/Ruin.md, wild/Lair.md,
                                                     wild/NaturalFeature.md)
  20%   A concealed detail, stated as:
          Clue    - in this location's own ground and growth, not the parent's
          Trigger - a stated act at a stated spot
          Payload - never a way onward: a cache, a piece of Lore, a Key, or what the
                    parent only implied, carried one step further

  -- access: how the party comes to be standing here
  1     Parent Landmark, named
  1     The visible detail at the parent that leads here - a mundane Exit, no trigger
  1     Something the parent only implied, now made concrete

  -- challenge: what opposes the party
  40%   Challenge   {creature | hazard | mystery}    (wild/Creature.md, wild/Hazard.md,
                                                      wild/Mystery.md)

  -- reward: what is here to take
  25%   Treasure                                                     (wild/Treasure.md)

  -- registry: what ties this place to somewhere else
  1     A Clue for each Secret child the region's Connections.mmd hangs off this
        location - one per child, and none where it has none         (wild/Secret.md)
  15%   This location's carrying role in a quest given elsewhere     (wild/Quest.md)

  1     Naming, after everything above                (patterns/setting/Naming.md)
```

**A Hidden location draws a Kind like any other**, and skips only the position line - per
`wild/Dressing.md`, its position is the parent it hangs off.

**A party standing here is already looking.** They followed a visible detail from the
parent, so a clue here can sit closer to the edge of notice than a Landmark's can. What it
still cannot do is need a lead of its own to find: a clue reached only by acting on another
clue is two triggers deep, and `region/Wild.md`'s depth rule exists because that second one
never gets reached.

## Constraints

- **A Hidden location's concealed detail never pays out a route.** Ways onward are its
  Secret-child Clue lines, one per child the region's `Connections.mmd` hangs here. A
  Payload that is a way through puts an edge in the prose that the graph does not carry.
