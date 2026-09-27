# Wild - Landmark

## Provides
One Landmark-tier WILD location: freely discoverable by roaming, and the leads to whatever
the region's graph hangs off it. Which Landmarks carry children is the region's
`Connections.mmd`'s.

## Spec

```
WILD - LANDMARK

  -- substrate: what this place is
  1     Dressing - what it is, and what weather has done to it       (wild/Dressing.md)
  1     Kind   {ruin | lair | natural feature | crossing}   (wild/Ruin.md, wild/Lair.md,
                                                             wild/NaturalFeature.md,
                                                             wild/Crossing.md)
  20%   A concealed detail, stated as:
          Clue    - {growth | ground | weather | wear}, legible from where a party
                    stopped, since a Landmark has a horizon and a room has four walls
          Trigger - a stated act at a stated spot
          Payload - never a way onward
                    {a cache | a piece of Lore | a Key | a vantage |
                     what this place was actually for}

  -- access: how the party comes to be standing here
  1     Freely discoverable by roaming - no parent, and no lead required to reach it
  1     A reason to stop, visible from outside

  -- challenge: what opposes the party
  35%   Challenge   {creature | hazard | mystery}    (wild/Creature.md, wild/Hazard.md,
                                                      wild/Mystery.md)

  -- reward: what is here to take
  15%   Treasure                                                     (wild/Treasure.md)

  -- registry: what ties this place to somewhere else
  1     A visible detail leading onward to each Hidden child the region's Connections.mmd
        hangs off this Landmark - one per child, and none where it has none
  1     A Clue for each Secret child the graph hangs off this Landmark
                                                                     (wild/Secret.md)
  10%   This location's carrying role in a quest given elsewhere     (wild/Quest.md)

  1     Naming, after everything above                (patterns/setting/Naming.md)
  20%   A second name, from a different mouth than the first
                                                       (patterns/setting/Naming.md)
```

## Constraints

- **A Landmark can be named, revisited and connected to.** A slope, a brook, a field of
  flowers is what the region looks like, and belongs in its Terrain.

- **Never roll for children.** The lead lines are mandatory per child the graph gives this
  Landmark and absent otherwise; a Hidden child whose parent states no lead is
  unreachable.

- **A Crossing is chosen for what going around costs, never for who built or lives
  there.** Where the same object's point is its history or its strangeness, it is a Ruin
  or a Natural Feature and the route through it is incidental.

- **Crossing is a Landmark kind only.** A crossing nobody can find is not doing the only
  job the kind has.

- **A concealed detail never pays out a route.** Ways onward are the child-lead lines; a
  Payload that is a way through invents an edge the graph does not carry.
