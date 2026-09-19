# Dangerous - Door

## Provides
What an exit physically is: its kind, what it is made of and how well, where it sits, and
where it goes. Which locations connect, and by what edge, is the block diagram's; the Exits
line syntax and units are `templates/Location.md`'s.

## Spec

```
DOOR - every exit
  1     Kind, matching the edge the block diagram already drew
        {open | one-way | secret | vertical}, and what that kind looks like from inside
        this room                                                 (genre: door-kinds)
  1     Type - material and construction               (genre: doors)
  1     Condition                                      (genre: door-condition)
  1     Position - which wall, corner, or direction it opens from
  1     Where it goes - the location code, or plain terms for an exit leaving the map
  40%   A gate on passage, stated as the thing that opens it      (genre: gates)
  1     Warded: what the ward refuses, and what forcing it costs
                        (dangerous/Mystery.md)
  15%   Where a gate was drawn, something set on the way through as well - mechanism
        fixed to trap   (dangerous/Hazard.md, dangerous/Trap.md)
```

**Kind is read, not chosen.** The block diagram typed this edge at 4b and both ends agreed.
A secret exit stays nested inside the feature that conceals it, per `templates/Location.md`,
and its Clue, Trigger and Payload come from the concealment line that drew it.

**A stuck gate has no maker**, so it owes `setting/Keys.md` no row: what opens it is time,
force or a tool rather than an answer. Where a gate instead wants a portable object the
party does not have, that object is a key, recorded here per `dangerous/Key.md`'s demand end.

## Constraints

- **A gate is stated on the exit line, never moved into a Feature.** Written as a Feature,
  the exit reads as unobstructed and the gate as decoration, and the two have to be
  reassembled at the table.

- **Two exits of the same kind are told apart by their type and their position.** A party
  choosing between "a door" and "a door" is guessing. Kind comes from the diagram and
  material usually from the region's Architecture, so what has to vary is the construction
  and the condition. No exit description repeats across more than a third of a block's
  exits, and compass direction alone does not meet that.

- **Where an exit commits the party, the room says so.** A consequence the players cannot
  see coming makes their decision for them.
