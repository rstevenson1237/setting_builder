# Dangerous - Medium

## Provides
What a medium-weight location guarantees.

## Spec

```
DANGEROUS - MEDIUM

  -- substrate: what this room is
  1     Dressing - what it is now, and what it was     (dangerous/Dressing.md)
  40%   A concealed detail, stated as:
          Clue    - visible in this room's own Dressing, and never the drawn challenge
          Trigger - a stated act on the clue
          Payload - something that changes what the challenge is worth: a way past it,
                    what it is sitting on, or what the room is not saying about it

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
  1     Any lock obligation recorded against this room       (dangerous/Key.md)
  10%   Something here that someone elsewhere would want, registered as supply
                                                     (dangerous/Quest.md)

  1     Naming, after everything above      (patterns/setting/Naming.md)
```

Medium weight means the location presents **one thing to deal with**, plainly. A room built
on a concealed trap presents as empty and belongs at low weight with the trap as its
variance - which is why the visibility line is mandatory here and nowhere else.

**Mystery is not a MEDIUM challenge.** It costs nothing until a wrong attempt is made, so
it is not one thing to deal with; MEDIUM draws only `{encounter | hazard}`.

**The clue competes with the challenge for attention, and that is the point.** A clue
findable only by turning away from the challenge is fair; one that cannot be found at all
while the challenge is live is a detail kept for a second visit the party has no reason to
make.

The treasure rates follow the fiction: a thing that lives here has accumulated something, a
mechanism has not.

## Constraints

- **Lore substitutes for the table roll rather than adding to it.** At MEDIUM the find is
  *either* a document *or* a roll, which is what keeps a medium room from paying out twice.

- **The Payload is not a second treasure draw.** It is the treasure this room already drew,
  moved behind the clue. A room that pays twice for one challenge has quietly become a HIGH
  location without the challenge to justify it.
