# Dangerous - Door

## Provides
What an exit physically is: its kind, what it is made of and how well, where it sits, and
where it goes.

Distinct from the region's block diagram, which decides *which* locations connect and by
what kind of edge: this file decides what standing at that connection is like. The Exits
line syntax and units are in `templates/Location.md`.

## Spec

```
DOOR - every exit
  1     Kind, matching the edge the block diagram already drew
        {open | one-way | secret | vertical}
  1     Type - material, construction, condition
  1     Position - which wall, corner, or direction it opens from
  1     Where it goes - the location code, or plain terms for an exit leaving the map
  40%   A gate on passage, stated as the thing that opens it
        {locked | barred | stuck | wanting a fitted object | wanting weight, power or
         numbers | warded}
  1     Warded: what the ward refuses, and what forcing it costs
                        (dangerous/Mystery.md)
  15%   Where a gate was drawn, something set on the way through as well - mechanism
        fixed to trap   (dangerous/Hazard.md, dangerous/Trap.md)
```

**Kind is read, not chosen.** The block diagram written at 4b already typed this edge, and
both its ends agreed. This file states what that kind looks like from inside this room; it
never reclassifies it. A secret exit stays nested inside the feature that conceals it, per
`templates/Location.md`, and its Clue, Trigger and Payload come from the concealment line
that drew it - not from here.

**A gate is not a fifth kind.** It qualifies a kind, and it is stated as what opens it rather
than as the fact of being shut. A door that needs a rod is an open exit with a price.

**A stuck gate has no maker.** Nobody shut it - the building did, and what opens it is
time, force, or a tool rather than an answer. It owes `setting/Keys.md` no row, and it is
the one gate a party can always spend effort on instead of solving.

**A trap on a way through is drawn, not decorated on.** It arrives with the clue, the
trigger and the stated cost every hazard owes, which is what stops a trapped exit being a
sentence that fires when the referee decides it does.

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
bottom course, a bronze grille green with age, plank-and-batten pinned with wooden trenails,
a cast bronze leaf too heavy for its own hinges, iron banding over a core that has rotted
out from behind it, a hurdle of withies, a hide stretched on a frame.

**What is actually in the opening**, where it is not a door at all: a plug of piled rubble;
a portcullis down and silted in; a hatch in a floor with a ring pulled off it; a bulkhead
laid flat over a stair; a hanging heavy enough to stop light; a screen of stacked stone
built dry; nothing, and a drop; nothing, and the opening is the wrong shape for anything
that walks.

**Condition**, following the room's own Condition: hinges seized, the leaf sprung and
never closed since, a bar socket cut out of the jamb by somebody in a hurry, scorching
around the frame, a threshold worn into a trough, a door taken off and used for something
else, fresh timber in an old opening.

**Kind, made visible.** *Open* - an arch, a breach, a doorway whose leaf is long gone.
*One-way* - a drop, a chute, a leaf barred from the far side, a slope that cannot be
climbed back up. *Secret* - a pivot seam in dressed stone, a counterweighted slab, a
passage behind a fitting nobody would move. *Vertical* - a shaft with staples, a ladder
well, a stair spiralling in a chimney, a hole broken through a floor.

**Gates**, where one is drawn: a lock wanting a key held elsewhere, a socket wanting a
fitted object, a mechanism wanting power the level does not currently have, a weight no
single person shifts.

*Barred* - a bar seated from the far side; a brace jammed under the leaf; wedges driven at
the sill; spikes through the jamb, set by somebody keeping something out, or in. *Stuck* -
timber swollen with damp; hinges seized solid; a lintel settled onto the leaf; silt or
spoil banked against the far face; the leaf sprung in its frame and binding at one corner.
*Warded* - a mark cut across the threshold and kept clean when nothing else here is; a
line of fittings buried at the sill; a name cut into the lintel in a tongue from
`setting/Language.md`; an opening that takes some things through and stops others.
*Trapped* - the mechanism comes from `dangerous/Trap.md`, and the tell that it is there
from the frame, the threshold, or what is lying short of it.

**Vocabulary.** An opening's parts already have names, and the name costs less than the
description: jamb, reveal, soffit, threshold-stone, pintle, gudgeon, strap-hinge, hasp,
staple, drawbar, bar-socket, wicket, postern. Where something sits on a door is given in
these rather than in left and right.

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

- **Never write a bare "a door".** An exit's Type line names material, construction and
  condition, or names the thing standing in the opening that is not a door. "A door" states
  only that the block diagram drew an edge here, which the diagram already said, and it
  hands the party nothing to look at, lever, burn, or listen through.

- **A ward is sorcery, and `GENRE.md` prices it.** A region carries at most one warded way,
  it has a maker somewhere in `setting/History.md`, and forcing it costs. Warding the
  ordinary locked doors of a region is the fastest way to make sorcery routine, which is the
  drift this genre is least able to absorb.

- **Never state what an exit means.** Where it goes and what it looks like are facts; that
  it is the way on, the safe route, or the mistake is the party's to find out.
