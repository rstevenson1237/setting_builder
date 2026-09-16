# Dangerous - Environmental

## Provides
A hazard that is a condition of the place itself, set by nobody and maintained by nothing.

Distinct from `dangerous/Trap.md`, which somebody built and therefore has an owner and
an intent, and from `dangerous/Residual.md`, which something left behind and which is
still acting.

## Spec

```
ENVIRONMENTAL
  1     Kind   {collapse | air | water | footing | heat | cold | growth | dark and sound}
  1     What the place is doing - the physical condition, stated plainly
  1     What it is a consequence of, in the location's own Dressing
  1     Whether it is constant, or worsens while the party is in it
  30%   Somewhere in this location it does not reach, and why
```

**An environmental hazard is Dressing with a cost** - the same fact the Dressing line
already records, read as something the party has to price rather than walk past. It has
no owner, so the only moves are prepare, endure, route around, or leave.

**A kind is drawn against the region, not against the room.** What a region is cut into,
how deep it sits, and what water and air do in it are settled above this file, and they
rule out most of the menu before it is read - a dry region high in rock does not produce a
flooded corridor in one location because the roll came up water. Where the region admits
two kinds, the location's own Dressing picks between them.

**A safe pocket is worth more than a bigger number.** Somewhere the condition does not
reach turns endurance into a decision about how long to stay out of it.

## Design patterns

**Water and footing** - standing water that never drained; a floor slick with what grows
on it; silt that takes a boot and keeps it; ice where a draught crosses water; stone worn
smooth by whatever has been dragged down it; a surface that holds a person and not a
person carrying something.

**Air** - air that will not carry a flame; a heaviness that settles into the lowest part
of the room; dust that hangs where something dropped it; a smell strong enough to be a
fact rather than dressing; what grows on the walls, breathed.

**Temperature** - a cold that comes up through the floor rather than through the air; heat
still in stone long after whatever made it is gone; a draught that takes warmth faster
than still air at the same reading; damp, which makes every other condition here worse.

**Heat at the top of the scale** - stone too hot to put a hand on and getting hotter with
depth; a crust over molten rock that carries a person and not a person running; a vent
that breathes on an interval somebody could have timed; steam where water reaches it, and
the water is coming from somewhere; air that dries a throat faster than it burns anything;
metal in the room that has slumped, which says what this place does at its worst.

**Light, dark, and sound** - dark that swallows a light source's useful radius; glare off
water or pale stone that hides what is under it; a room that carries every sound made in
it somewhere else; a room that carries none, so nothing can be heard coming.

**Collapse, and what is holding** - a ceiling carrying its load on one prop, one pillar, or
one beam, and the party can see which; a fall already down to the waist of a corridor with
a gap over it; a floor eaten thin from below; a fresh fall where the dust has not settled;
a roof that drops grit whenever something heavy moves; a shaft whose collar has gone; a
wall out of plumb far enough to read from the doorway; a working propped by whoever cut it,
in timber that has since been eaten.

**Growth** - a root mass that has opened a wall and is holding what it opened; thorn grown
across the only way through, thick enough to be a job rather than a step; a stand that
closes behind whatever passes through it; something that grips what touches it and does not
choose to; a bloom or a spore bed that answers to being disturbed; a mat over standing water
that reads as floor.

**What the place has become** - growth that has taken the walls and is load-bearing now; a
colony or a nest old enough to be terrain rather than a creature; a room whose original
shape can no longer be made out from inside it.

## Constraints

- **A fall that has finished is Dressing, not a hazard.** What this file draws is a
  condition still able to act: something holding that can stop holding, ground still
  moving, water still rising. Rubble that came down a century ago costs nothing to stand
  in, and writing it here buys a location a hazard it does not have.

- **Growth that acts on its own account is a creature.** Something that reaches, follows,
  wants, or can be driven off belongs at `dangerous/Creature.md` as terrain-shaped. This
  file draws only what has to be got through.

- **An environmental hazard the Dressing does not already account for has an owner, and
  therefore belongs elsewhere.** A condition with no cause in what the room is came from
  somebody building it (`dangerous/Trap.md`) or something leaving it
  (`dangerous/Residual.md`), and filing it here strips it of the maker that made it worth
  finding.

- **Never invent region-scale terrain for one location.** Molten rock, a water table, a
  seam that burns - these are facts about where the region sits, stated above this file. A
  location may reach one; it may not be the only room in the region that has one.
