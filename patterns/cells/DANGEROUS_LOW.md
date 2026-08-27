# DANGEROUS_LOW

> The bulk of the module, carried by format.

A `DANGEROUS_LOW` location is a room that holds the map together. It is the
corridor, the landing, the flooded stair, the store with its shelves gone. There
are more of these than of anything else in the region, and the cell succeeds when
a referee can run twenty of them in an hour without the level going slack. That
is a format problem before it is a writing problem, and this file is mostly
about format.

## What belongs here

- **Exits with sensory cues, always.** The type requires them and this cell is
  where they do the work. Every exit says what is noticed from inside this room
  looking that way: colder air, a draught that moves the light, water sound, a
  smell, a slope underfoot. Navigation in a `DANGEROUS` region is the play, and a
  room whose exits are "north, east" is a room that has removed it.

- **Dimensions and material, in the first line.** Feet indoors. What it is cut
  from, what is underfoot, how high the ceiling is, and what the light does. A
  referee reads that line aloud and has run the room.

- **One thing to notice, and it is honest.** Not a hook, not a treasure, not a
  trap. Wear on one side of a threshold. A door that swings shut. A course of
  stone that is older than the rest. A room reads as questionable rather than
  settled because something in it does not match, and most of the time the
  mismatch is exactly what it looks like.

- **A reaction to one named action.** The type requires reactions branching on
  named player actions. In this cell there is usually one: what happens if the
  door is closed, if the water is entered, if the party stops here for a turn.
  One line, and the branch is stated.

- **Emptiness that is stated as emptiness.** A field may be empty. Write `None`
  with a brief reason. A room with nothing in it says so and says why, and that
  is not the same room as a room somebody forgot to fill.

- **What time it costs.** A `DANGEROUS` region counts in turns, six to an hour.
  If the room costs a turn to cross, or two to search, or none, say so.

## Where the boundary falls

- **Up to `DANGEROUS_MEDIUM`** the moment there is something to do here rather
  than something to notice: a hazard with a test, a mechanism, a hoard to
  compose, a thing that holds territory. Doing is `MEDIUM`. Passing through is
  `LOW`.

- **Not a location at all** when it has no exit worth a cue, nothing to notice
  and no reaction. Fold it into the neighbouring room's description and put the
  edge in `connections.md`. A level with fewer, better rooms is a better level,
  and the count band in `config/weights.yaml` is a band rather than a quota.

- **Sideways** when the room is doing nothing but is doing it beautifully. Keep
  it. A level made only of consequential rooms has no rhythm and no place to be
  afraid in.

## Form

- **Player Overview:** two to five sentences. Dimensions, material, light, then
  the one thing to notice. Bold one noun, or none.
- **Features:** zero to two. Zero is a legal and common answer in this cell, and
  the room then lives entirely in its Overviews and its Exits.
- **Referee Overview:** what is true that the Overview does not say, the
  reaction and its branch, the cost in turns, and the nil where there is one.
  Three or four lines. This cell is written short on purpose.
- **Exits:** every one carries a cue. Where an exit is one-way, say what makes
  it one-way from the far side.
- **Tokens:** rare here. A room with three tokens in it is a `MEDIUM`.
- **Tables it leans on:** `T-ARC` above all, because recognition is cheaper than
  explanation and the same stonework recurring is what makes a level legible.
  Then `T-HAZ` for what the building does on its own, and `T-PRC` for what
  crossing or searching costs.

## Worked example

An illustration of the shape and the register. Nothing in it is canon, and the
codes are stand-ins.

**Player Overview.** Twenty feet by twelve, cut from the rock and faced on three
walls only. The fourth wall is bare stone and the facing stops in a straight
vertical line, as though the work was called off between one course and the
next. The floor slopes a foot toward the far corner, where the water stands two
inches deep and does not drain. **A bracket** on the faced wall holds nothing.

**Referee Overview.** *Cost:* one turn to cross, two to search, and there is
nothing to find. *What is true:* the facing stopped because the rock behind it
is not the rock the rest of the level is cut from. It is warmer than the faced
walls by enough to feel with a hand held flat. Nothing else here is warm.
*Reaction:* the standing water is skinned and holds a footprint for a turn.
Anything that has crossed since the party entered the level has left a mark
readable from the doorway. *Treasure:* None. The brackets were stripped, and the
sockets show the tool marks of the stripping.

**Exits.** *West, low arch:* the draught goes this way and takes a flame with
it. *North, doorless:* the slope runs up and the floor is dry within ten feet.
*Down, in the wet corner:* a grating a foot square, and the water above it does
not move -> R06-L18.

## Excluded patterns

- **A room that exists to be counted.** If it has no cue, no notice and no
  reaction, delete it and widen its neighbour.
- **An empty room with no reason to be empty.** Emptiness is stated and its
  reason is given. Silence is what a forgotten room looks like.
- **A monster keyed here to fill space.** Living things in a `DANGEROUS` region
  reach a party through the Dangers table and through the rooms that hold
  territory. A `LOW` room is where they are heard rather than where they are.
- **A trap with no tell.** The tell is in the Player Overview and it is
  physical. Traps are local content and are written by the trap pattern, not
  drawn from a table.
- **A treasure worth stopping for.** Something worth carrying out is what makes
  a `MEDIUM`.
- **Exits stated as compass directions alone.** The cue is the requirement. A
  bearing is not a cue.
- **A description that concludes.** Say the wall is warm. Never say the wall is
  wrong.
