# Wild - Hidden

## Provides
One Hidden-tier WILD location: found by stopping at its parent and looking, not by
roaming. Its parent is the region's `Connections.mmd`'s.

## Spec

```
WILD - HIDDEN

  -- substrate: what this place is
  1     Dressing - what it is, and what weather has done to it       (wild/Dressing.md)
  1     Kind   {ruin | lair | natural feature}      (wild/Ruin.md, wild/Lair.md,
                                                     wild/NaturalFeature.md)
  20%   A concealed detail, stated as:
          Clue    - {growth | ground | weather | wear}, in this location's own ground,
                    not the parent's, and free to sit closer to the edge of notice since
                    the party arrived already looking
          Trigger - a stated act at a stated spot
          Payload - never a way onward
                    {a cache | a piece of Lore | a Key |
                     what the parent only implied, carried one step further}

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
  20%   A second name, from a different mouth than the first
                                                       (patterns/setting/Naming.md)
```

## Constraints

- **A Hidden way in is visible and easy to miss; a Secret way in is concealed until acted
  on.** Writing one as the other moves the location to the wrong tier.
