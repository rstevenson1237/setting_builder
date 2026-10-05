# Dangerous - Door

## Provides
What an exit physically is: its kind, what stands in the opening, where it sits, and where
it goes. Which locations connect, and by what kind of edge, is the block diagram's; the
Exits line syntax and units are `templates/region/Location.md`'s.

## Spec

```
DOOR - every exit
  1     Kind, read off the edge the block diagram already drew - never chosen here, and
        made visible by what a party sees rather than by the word
                                         {open | one-way | secret | vertical}
  1     What stands in the opening                                         {OPENING}
  1     Its material, its construction and its condition - named by its parts, as facts
        a party could test by hand
  1     Position - which wall, corner, or direction it opens from, given by the part a
        thing sits on rather than by left and right
  1     Where it goes - the location code, or plain terms for an exit leaving the map
  40%   A gate on passage, stated as what opens it, on the exit line itself    {GATE}
  1     Where warded: what the ward refuses, and what forcing it costs
                        (dangerous/Mystery.md)
  15%   Where a gate was drawn, something set on the way through as well - mechanism
        fixed to trap   (dangerous/Hazard.md, dangerous/Trap.md)
```

```
OPENING - exactly one
  leaf         - a hinged door
  pivot        - a slab turning on a pin
  portcullis   - a grille dropped from above
  grille       - fixed bars, with a gap or a gate in them
  hanging      - a curtain, hide or screen
  arch         - an open, built opening
  breach       - a hole made through what was a wall
  hatch        - a door set in a floor or a ceiling
  climb        - a fixed way up or down between levels
  natural      - an unbuilt gap in rock, root or earth
  sluice       - an opening built to pass water
```

```
GATE - exactly one
  locked       - a lock, and whatever key opens it
  barred       - barred from one side
  stuck        - held by the building rather than by anyone: opened by time, force or a
                 tool, never an answer, and owing setting/Keys.md no row
  fitted       - wanting a fitted object the party does not have: a key, owing a
                 setting/Keys.md row per dangerous/Key.md's demand end
  weight       - wanting weight, power or numbers
  warded       - sorcery, with a maker in setting/History.md
```

## Constraints

- **No written exit description repeats across more than a third of a block's exits.**
  Kind and usually material are fixed from above; two exits of the same kind are told
  apart by their opening, their make and their position.

- **Never move a gate into a Feature.** Written apart from its exit, the exit reads as
  unobstructed and the gate as decoration.
