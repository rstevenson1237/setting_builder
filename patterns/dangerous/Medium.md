# Dangerous - Medium

## Provides
One medium-weight DANGEROUS location: a room that presents one thing to deal with, and
presents it plainly.

## Spec

```
DANGEROUS - MEDIUM

  -- substrate: what this room is
  1     Dressing - what it is now, and what it was     (dangerous/Dressing.md)
  40%   Concealed detail, stated as:
          Clue        - visible in this room's own Dressing, never the drawn challenge,
                        and findable by turning away from the challenge
          Trigger     - a stated act on the clue
          Payload     - what changes what the challenge is worth
                        {a way past it | what it is sitting on | what the room is not
                         saying about it}
          Payload row - where the payload is what it is sitting on: the treasure row
                        this room already drew, moved behind the clue

  -- challenge: what opposes the party
  1     Challenge - guaranteed, and present and visible on entry: an encounter itself,
        or a hazard with more in the room than its clue
                        {encounter | hazard}          (dangerous/Encounter.md,
                                                       dangerous/Hazard.md)

  -- reward: what is here to take - reward follows the fiction: a thing that lives here
     has accumulated something, a mechanism has not
  50%   Treasure - where the challenge is an encounter  (dangerous/Treasure.md)
  33%   Treasure - where the challenge is a hazard      (dangerous/Treasure.md)
  20%   Lore instead - where treasure is drawn, it is lore rather than a table roll
                                                       (dangerous/Lore.md)

  -- registry: what ties this room to somewhere else
  25%   Foreshadow - a detail that foreshadows a HIGH location elsewhere in the region
  1     Foreshadows - where a foreshadow was drawn: that HIGH location, by code
  1     Lock - any lock obligation recorded against this room       (dangerous/Lock.md)
  10%   Quest - something here that someone elsewhere would want, registered as supply
                                                     (dangerous/Quest.md)

  1     Naming, after everything above      (patterns/setting/Naming.md)
  30%   Second name - from a different mouth than the first
                                            (patterns/setting/Naming.md)
```

## Constraints

- **An encounter here is never drawn absent.** The challenge is what a MEDIUM room is;
  drawn absent, the room is a LOW room with a rumour in it.

- **The Payload is not a second treasure draw.** Where it pays out, it is the treasure
  this room already drew, moved behind the clue.
