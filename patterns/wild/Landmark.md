# Wild - Landmark

## Provides
One Landmark-tier WILD location: freely discoverable by roaming, with no parent and no lead
required to reach it. Which Landmarks carry children is the region's `Connections.mmd`'s;
the lead each child shows here is that child's own line, in `wild/Hidden.md` or
`wild/Secret.md`.

## Spec

```
WILD - LANDMARK

  -- substrate: what this place is
  1     Dressing - what it is, and what weather has done to it       (wild/Dressing.md)
  1     Kind   {ruin | lair | natural feature | crossing}   (wild/Ruin.md, wild/Lair.md,
                                                             wild/NaturalFeature.md,
                                                             wild/Crossing.md)
  20%   Concealed detail, stated as:
          Clue kind   - {growth | ground | weather | wear}
          Clue        - legible from where a party stopped, since a Landmark has a
                        horizon and a room has four walls
          Trigger     - a stated act at a stated spot
          Payload     - never a way onward
                        {a cache | a piece of Lore | a Key | a vantage |
                         what this place was actually for}
          Payload row - where a cache, a piece of Lore or a Key: the treasure row it is,
                        its disposition hidden

  -- access: how the party comes to be standing here
  1     Reason to stop - visible from outside

  -- challenge: what opposes the party
  35%   Challenge   {creature | hazard | mystery}    (wild/Creature.md, wild/Hazard.md,
                                                      wild/Mystery.md)

  -- reward: what is here to take
  15%   Treasure                                                     (wild/Treasure.md)

  -- registry: what ties this place to somewhere else
  10%   Quest - this location's carrying role in a quest given elsewhere (wild/Quest.md)

  1     Naming, after everything above                (patterns/setting/Naming.md)
  20%   Second name - from a different mouth than the first
                                                       (patterns/setting/Naming.md)
```

## Constraints

- **A Landmark can be named, revisited and connected to.** A slope, a brook, a field of
  flowers is what the region looks like, and belongs in its Terrain.
