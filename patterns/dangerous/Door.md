# Dangerous - Door

## Provides
What an exit physically is: its kind, what it is made of and how well, where it sits, and
where it goes.

## Read at
**Mode: second pass.** Step 4c, for every exit of every DANGEROUS location without
exception, drawn by `dangerous/Dressing.md`'s exit line. Distinct from the region's block
diagram, which decides *which* locations connect and by what kind of edge: this file decides
what standing at that connection is like. The Exits line syntax and units are in
`templates/Location.md`.

## Spec

```
DOOR - every exit
  1     Kind, matching the edge the block diagram already drew
        {open | one-way | secret | vertical}
  1     Type - material, construction, condition
  1     Position - which wall, corner, or direction it opens from
  1     Where it goes - the location code, or plain terms for an exit leaving the map
  40%   A gate on passage, stated as the thing that opens it
```

**Kind is read, not chosen.** The block diagram written at 4b already typed this edge, and
both its ends agreed. This file states what that kind looks like from inside this room; it
never reclassifies it. A secret exit stays nested inside the feature that conceals it, per
`templates/Location.md`, and its Clue, Trigger and Payload come from the concealment line
that drew it - not from here.

**A gate is not a fifth kind.** It qualifies a kind, and it is stated as what opens it rather
than as the fact of being shut. A door that needs a rod is an open exit with a price.

**A gate is stated on the exit line, not moved into a Feature.** What opens a way through
belongs where the party reads what the way through is; written as a Feature instead, the
exit reads as unobstructed and the gate reads as decoration, and the two facts have to be
reassembled at the table. Where the gate wants a portable object the party does not
already have, that object is a key: record a `setting/Keys.md` row for it here, per
`dangerous/Key.md`'s demand end, rather than leaving a socket in the wall that nothing in
the setting fills.

## Design patterns

**Material and construction.** Real materials named as materials, and real joinery: banded
oak, bronze-shod, iron-strapped, a slab of dressed limestone pivoting on a socket, a lintel
of a single stone, a curtain of hide over a hacked opening, mud brick gone soft at the
bottom course, a bronze grille green with age.

**Condition**, following the room's own Condition: hinges seized, the leaf sprung and
never closed since, a bar socket cut out of the jamb by somebody in a hurry, scorching
around the frame, a threshold worn into a trough, a door taken off and used for something
else, fresh timber in an old opening.

**Kind, made visible.** *Open* - an arch, a breach, a doorway whose leaf is long gone.
*One-way* - a drop, a chute, a leaf barred from the far side, a slope that cannot be
climbed back up. *Secret* - a pivot seam in dressed stone, a counterweighted slab, a
passage behind a fitting nobody would move. *Vertical* - a shaft with staples, a ladder
well, a stair spiralling in a chimney, a hole broken through a floor.

**Gates**, where one is drawn: a lock wanting a key held elsewhere, a bar seated from the
far side, a socket wanting a fitted object, a mechanism wanting power the level does not
currently have, a weight no single person shifts.

## Constraints

- **No written exit description repeats across more than a third of a block's exits.**
  Kind comes from the diagram and material usually comes from the region's Architecture, so
  neither is free to vary - in a single-material region most exits will honestly read "open
  archway - basalt", and demanding otherwise would ask a file to contradict the region above
  it. What has to vary is the rest of the line: the construction and the condition, which
  this file's Design patterns stock for exactly that reason. A block whose exits are mostly
  one repeated phrase has written the diagram out in words rather than described anything,
  and the rule below cannot be met by compass direction alone.

- **Two exits of the same kind are told apart by their type and their position, and this is
  not housekeeping.** It is what makes a choice a decision rather than a coin flip. A party
  choosing between "a door" and "a door" is guessing; a party choosing between "a low door,
  scorched black around the frame" and "a wide arch, its threshold worn smooth" is deciding.
  A location with three or more exits carries the weight of that choice and its exits must
  earn it.

- **Never reclassify an edge here.** Kind comes from the block diagram, where both ends of
  the connection agreed on it. An exit written as open at one end and secret at the other is
  the same map contradicting itself.

- **Where an exit commits the party, the room says so.** An exit into a wing the party
  cannot cross back from without retracing states that consequence where they are standing,
  not only in the graph. A consequence the players cannot see coming makes their decision
  for them.

- **Never state what an exit means.** Where it goes and what it looks like are facts; that
  it is the way on, the safe route, or the mistake is the party's to find out.
