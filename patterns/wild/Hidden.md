# Wild - Hidden

## Provides
What a Hidden-tier location guarantees, and how it hangs off its parent.

## Read at
**Mode: entry.** Step 4c, after every Landmark in the region exists. A Hidden location
cannot be written before its parent, because its connection is written into the parent's
Exits.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Every line is either an edge - it names a
file in parentheses, the only other file that line requires - or a question the generator
answers here.

```
WILD - HIDDEN

  -- substrate: what this place is
  1     Dressing - what it is, and what weather has done to it       (wild/Dressing.md)
  1     Kind   {ruin | lair | natural feature}      (wild/Ruin.md, wild/Lair.md,
                                                     wild/NaturalFeature.md)
  1     Secrets - whether it conceals anything                       (wild/Secrets.md)

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

  1     Naming, after everything above                               (wild/Naming.md)
```

A Hidden location is not found by roaming. It is found by **stopping at a Landmark and
actually looking** - going behind, under, past, or into something the parent's entry
already described. No trigger, no roll: per `setting/Procedures.md`, a stated detail
investigated is a detail found.

The distinction from a Secret is the whole tier: a Hidden way in is *visible and easy to
miss*; a Secret way in is *concealed until acted on*.

**A Hidden location draws a Kind like any other**, and skips only the position line - per
`wild/Dressing.md`, its position is the parent it hangs off. What it is physically has to
be answered somewhere, and the kind files are where that answer lives.

Its rated lines come to about 0.8 of a Feature against a Landmark's 0.6, and its child
leads are read off the region's `Connections.mmd` the same way - mandatory per child the
graph gives it, absent otherwise. A party that stopped and looked has already paid
something to be standing here, and the rates are where that is paid back.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
