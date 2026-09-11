# Wild - Landmark

## Provides
What a Landmark-tier location guarantees, and whether it carries children.

## Read at
Step 4c, for a WILD location its stub marks landmark. Generate all Landmarks before any
Hidden or Secret location, since each child's connection is written into its parent.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Every line is either an edge - it names a
file in parentheses, the only other file that line requires - or a question the generator
answers here.

```
WILD - LANDMARK

  -- substrate: what this place is
  1     Dressing - what it is, and what weather has done to it       (wild/Dressing.md)
  1     Kind   {ruin | lair | natural feature | crossing}   (wild/Ruin.md, wild/Lair.md,
                                                             wild/NaturalFeature.md,
                                                             wild/Crossing.md)
  1     Secrets - whether it conceals anything                       (wild/Secrets.md)

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

  1     Naming, after everything above                               (wild/Naming.md)
```

**The blocks are what the entry is**, and WILD carries one DANGEROUS does not. Substrate
says what the place is, challenge what opposes the party, reward what is here to take,
registry what ties it to somewhere else - the same four. **Access** is WILD's own: at
depth, how a room is reached is the connection graph, written at 4b and needing no words
in the entry; out here it is content, written into the parent's Features, and it is the
whole distinction between this tier and the two below it.

**A Landmark can be named, revisited, and connected to.** That is the test, and it is what
separates a Landmark from terrain. A stretch of eroded slope, a brook, a field of flowers
- these are what the region looks like, they belong in the Region Overview's Terrain
field, and writing them as locations wastes a slot the region cannot spare.

**The deeper the tier, the more the entry pays.** The rated lines here come to about
0.6 of a Feature, Hidden's to 0.8, Secret's to 1.0. Access is what the gradient is priced
against: a Landmark costs nothing to reach, so most of them are allowed to be a place and
nothing more, while a location a party spent an action looking for and a clue acting on
owes them something for it.

**Which children a Landmark carries is read off the graph, not rolled here.** Per
`region/Wild.md` the region's `Connections.mmd`, written at 4b, already says which
Landmarks have children and by which edge - a normal edge to a Hidden child, a hidden
(`-.-`) edge to a Secret one. So the lead lines are mandatory *per child the graph gives
this Landmark* and absent otherwise; they are not a rate, the same way
`dangerous/Low.md`'s node role is read off the graph rather than chosen. A Hidden child
whose parent never stated the detail leading to it is unreachable.

**Naming comes last because a place is named for what turned out to be there.** It is the
one pass that gets cheaper by running after everything else is decided.

**Position is Dressing's, not this file's.** `wild/Dressing.md` already states a bearing
from the region's entry or another named Landmark for every WILD location that has one;
the line was written twice and is answered there.

## Constraints

- **A Crossing is chosen for what it costs to go around, not for who built or lives
  there.** Its physical form can be a Ruin's (a bridge, a causeway), a Natural Feature's
  (a ford, a pass), or held like a Lair - Kind is exactly one, so pick Crossing when the
  location's point is that the region's own shape forces the party through it; pick Ruin
  or Natural Feature instead when the same object's point is its history or its
  strangeness and the route through it is incidental.

- **Crossing is a Landmark kind only**, which is why `wild/Hidden.md` and
  `wild/Secret.md` draw three kinds and this file four. A crossing exists because going
  around it is expensive, so the country itself advertises it; one nobody can find is
  not doing the only job the kind has.
