# Dangerous - Medium

## Provides
What a medium-weight location guarantees.

## Read at
**Mode: entry.** Step 4c, for a location its gazetteer stub marks medium.

## Spec

**Every line below is read the same way:** `1` is mandatory; a percentage is the rate at
which a Feature carrying that content appears. Every line is either an edge - it names a
file in parentheses, the only other file that line requires - or a question the generator
answers here.

```
DANGEROUS - MEDIUM

  -- substrate: what this room is
  1     Dressing - what it is now, and what it was     (dangerous/Dressing.md)
  1     Secrets - whether it conceals anything          (dangerous/Secrets.md)

  -- challenge: what opposes the party
  1     Challenge   {encounter | hazard} - guaranteed, and obvious
                                                      (dangerous/Encounter.md,
                                                       dangerous/Hazard.md)
  1     The challenge is present and visible on entry - at MEDIUM an encounter is
        never drawn absent, and a hazard's clue is never the only thing in the room

  -- reward: what is here to take
  50%   Treasure, where the challenge is an encounter  (dangerous/Treasure.md)
  33%   Treasure, where the challenge is a hazard      (dangerous/Treasure.md)
  20%   Where treasure is drawn, it is lore rather than a table roll

  -- registry: what ties this room to somewhere else
  25%   A detail that foreshadows a HIGH location elsewhere in the region
  10%   A lock, and the key that opens it is elsewhere  (dangerous/Key.md)
  10%   The target of a quest given elsewhere           (dangerous/Quest.md)

  1     Naming, after everything above                  (dangerous/Naming.md)
```

Medium weight means the location presents **one thing to deal with**, and presents it
plainly. A challenge the party cannot see is not a medium-weight challenge - a room built
on a concealed trap presents as empty, and belongs at low weight with the trap as its
variance. That is why the visibility line is mandatory here and nowhere else: it suppresses
`dangerous/Encounter.md`'s absent-on-arrival option, which is a HIGH and LOW device.

**Mystery is not a MEDIUM challenge.** Per `dangerous/Mystery.md` a mystery costs nothing
until a wrong attempt is made, so it is not one thing to deal with - it is something to
work out. MEDIUM draws only `{encounter | hazard}`.

The treasure rates are conditional on the challenge because reward should follow the
fiction: a thing that lives here has accumulated something, a mechanism has not.

**Lore substitutes for the table roll rather than adding to it.** At HIGH lore arrives
alongside the payload; at MEDIUM the find is *either* a document *or* a roll, which is what
keeps a medium room from paying out twice.


## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
