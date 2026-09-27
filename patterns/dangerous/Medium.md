# Dangerous - Medium

## Provides
One medium-weight DANGEROUS location: a room that presents one thing to deal with, and
presents it plainly.

## Spec

```
DANGEROUS - MEDIUM

  -- substrate: what this room is
  1     Dressing - what it is now, and what it was     (dangerous/Dressing.md)
  40%   A concealed detail, stated as:
          Clue    - visible in this room's own Dressing, never the drawn challenge, and
                    findable by turning away from the challenge
          Trigger - a stated act on the clue
          Payload - what changes what the challenge is worth
                    {a way past it | what it is sitting on | what the room is not saying
                     about it}

  -- challenge: what opposes the party
  1     Challenge   {encounter | hazard} - guaranteed, and obvious
                                                      (dangerous/Encounter.md,
                                                       dangerous/Hazard.md)
  1     The challenge is present and visible on entry - an encounter here is never drawn
        absent, and a hazard's clue is never the only thing in the room

  -- reward: what is here to take - reward follows the fiction: a thing that lives here
     has accumulated something, a mechanism has not
  50%   Treasure, where the challenge is an encounter  (dangerous/Treasure.md)
  33%   Treasure, where the challenge is a hazard      (dangerous/Treasure.md)
  20%   Where treasure is drawn, it is lore instead of a table roll
                                                       (dangerous/Lore.md)

  -- registry: what ties this room to somewhere else
  25%   A detail that foreshadows a HIGH location elsewhere in the region
  1     Any lock obligation recorded against this room       (dangerous/Key.md)
  10%   Something here that someone elsewhere would want, registered as supply
                                                     (dangerous/Quest.md)

  1     Naming, after everything above      (patterns/setting/Naming.md)
  30%   A second name, from a different mouth than the first
                                            (patterns/setting/Naming.md)
```

## Constraints

- **A challenge the party cannot see is not a MEDIUM challenge.** A room built on a
  concealed trap presents as empty, and belongs at LOW.

- **Mystery is not a MEDIUM challenge.** It costs nothing until a wrong attempt, so it is
  something to work out rather than one thing to deal with.

- **The Payload is not a second treasure draw.** Where it pays out, it is the treasure
  this room already drew, moved behind the clue.
