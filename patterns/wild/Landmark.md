# Wild - Landmark

## Provides
What a Landmark-tier location guarantees, and whether it carries children.

## Spec

```
WILD - LANDMARK

  -- substrate: what this place is
  1     Dressing - what it is, and what weather has done to it       (wild/Dressing.md)
  1     Kind   {ruin | lair | natural feature | crossing}   (wild/Ruin.md, wild/Lair.md,
                                                             wild/NaturalFeature.md,
                                                             wild/Crossing.md)
  20%   A concealed detail, stated as:
          Clue    - weather, growth or ground, legible from where a party would stand
          Trigger - a stated act at a stated spot
          Payload - never a way onward: a cache, a piece of Lore, a Key, a vantage, or
                    what this place was actually for

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
```

**A Landmark can be named, revisited, and connected to.** That is the test that separates
one from terrain. A stretch of eroded slope, a brook, a field of flowers belong in the
Region Overview's Terrain field; written as locations they waste a slot the region cannot
spare.

**The deeper the tier, the more the entry pays.** The rated lines here come to about 0.6 of
a Feature, Hidden's to 0.8, Secret's to 1.0. Access is what the gradient is priced against.

**Which children a Landmark carries is read off the graph, not rolled here.** The region's
`Connections.mmd`, written at 4b, already says which Landmarks have children and by which
edge, so the lead lines are mandatory per child and absent otherwise. A Hidden child whose
parent never stated the detail leading to it is unreachable.

**Outdoors a clue is weather and time, not construction**: a hollow that has slumped; a
covering rotted through; a plant growing where the ground was disturbed; frost melting in a
shape; water draining where it should pool; growth younger than the growth around it; a path
worn to nowhere; a mark cut above standing height.

**A party can walk past a whole hillside.** A room has four walls and a party will look at
all of them; a Landmark has a horizon. State the clue against the reason the party stopped
here, so it sits where they are already standing.

## Constraints

- **A Crossing is chosen for what it costs to go around, not for who built or lives
  there.** Its physical form can be a Ruin's, a Natural Feature's, or held like a Lair -
  Kind is exactly one, so pick Crossing when the location's point is that the region's own
  shape forces the party through it.

- **Crossing is a Landmark kind only**, which is why `wild/Hidden.md` and `wild/Secret.md`
  draw three kinds and this file four. A crossing nobody can find is not doing the only job
  the kind has.

- **A Landmark's concealed detail never pays out a route.** Ways onward are its child-lead
  lines, one per child the graph actually hangs here. A Payload that is a way through
  invents an edge the graph does not carry.
