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

Medium weight means the location presents **one thing to deal with**, and presents it
plainly. A challenge the party cannot see is not a medium-weight challenge - a room built
on a concealed trap presents as empty, and belongs at low weight with the trap as its
variance. That is why the visibility line is mandatory here and nowhere else: it suppresses
`dangerous/Encounter.md`'s absent-on-arrival option, which is a HIGH and LOW device.

**Mystery is not a MEDIUM challenge.** Per `dangerous/Mystery.md` a mystery costs nothing
until a wrong attempt is made, so it is not one thing to deal with - it is something to
work out. MEDIUM draws only `{encounter | hazard}`.

**At MEDIUM the clue competes with the challenge for attention, and that is the point.**
The room presents one thing plainly, per the visibility line above, and a party dealing
with that thing is not searching. A clue findable only by turning away from the challenge
is fair. A clue that cannot be found at all while the challenge is live is not - it is a
detail the room kept for a second visit the party has no reason to make.

The treasure rates are conditional on the challenge because reward should follow the
fiction: a thing that lives here has accumulated something, a mechanism has not.

**Lore substitutes for the table roll rather than adding to it.** At HIGH lore arrives
alongside the payload; at MEDIUM the find is *either* a document *or* a roll, which is what
keeps a medium room from paying out twice.

## Constraints

- **The Payload is not a second treasure draw.** Where a concealed detail pays out at
  MEDIUM, it is the treasure this room already drew, moved behind the clue - not another
  one stacked on top. A room that pays twice for one challenge has quietly become a HIGH
  location without the challenge to justify it.
