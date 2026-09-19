# Dangerous - Mystery

## Provides
What the strange thing is, how it is engaged, and what engaging it wrongly costs.

Distinct from `dangerous/Hazard.md`, which is the costly case: a mystery is neutral
until a genuinely wrong attempt is made. Distinct from a concealed detail, whose rate and
triple the weight file draws: a Mystery is content and may be in plain sight; a concealed
detail is a discovery structure and by definition is not.

## Spec

```
MYSTERY
  1     Fixture, built or placed with purpose, never found debris
        {ward | water - fountain, pool, basin | altar | statue or effigy | illusion
         | machinery}
  2     Physical details it can be reasoned from - the floor, not the target: one detail is
        guessed at, three is reasoned out
  1     Trigger, stated explicitly
  1     What the correct trigger accomplishes
  1     What a genuinely wrong attempt costs
  40%   A third detail, where the trigger is more than one step
```

**The fixture decides what the details are made of.** Machinery is reasoned from wear,
travel and what it is connected to; water from level, flow and what is in it; a statue from
pose, gaze and what is worn smooth; an altar from its fittings, its channels and its stains;
a ward from what is kept clean, what stops short of it, and what is lying on the far side;
an illusion from what disagrees - sound, draught, dust, or a floor that keeps going where
the wall says it stops. Pick the fixture first and the details are already half-written;
pick the details first and the fixture ends up a label on them.

**A Mystery left uninvestigated is neutral.** Inspection, theorising, and a wrong guess
that stops short of a real attempt all cost nothing - this is what separates a Mystery from
a Trap: a trap fires on contact or presence, a mystery fires only on a failed attempt to
use it.

## Design patterns

**Fixtures** - a statue whose pose or gaze means something; an altar with a fitting, a
channel, or a stain; a fountain, basin or cistern that still runs or conspicuously does
not; a door with no handle and a made surface; a mechanism part-visible in a wall; a floor
laid in a pattern that is not decoration; a mural that disagrees with the room it is in.

**Machinery** - a mechanism whose linkage runs into the wall and out somewhere else in the
region; a drum, capstan or windlass with its rope gone; a shaft that turns and does nothing
visible; a counterweight hanging at the wrong height; a thing wanting power the region no
longer produces; a fitting worn only on one side, which says which way it was worked; a
housing with the part taken out of it, and the part is somewhere.

**Wards** - a mark cut across a threshold and kept clean where nothing else here is; a line
of fittings buried at a sill, one of them missing; a name cut into a lintel in a tongue from
`setting/Language.md`; a ring of something laid down that has not been disturbed by anything
that walks; a doorway that takes some things through and stops others; what is lying just
short of the line, and how long it has been there.

**Water** - a fountain still running where nothing else in the region does; a pool that
takes what is dropped in it and does not give it back; a basin whose level does not answer
to the weather; standing water clear over a floor that should have silted; a cistern with a
channel cut to somewhere; water that is warm, or is not, and what that says about what it
came through.

**Illusions** - a wall a draught crosses; a floor that carries sound from further than it
goes; a room that shows itself furnished in a region where nothing else has survived; a
figure that does not turn; a way on that dust does not settle in; a thing that is only
wrong from one side of the room.

**Standing effects** - a space where a sense does not work; a cold that has a boundary; a
sound with no source that changes with position; light that falls wrong; a thing that does
not decay in a room where everything else has; water that will not mix.

**Sealed ways** - a door held by something other than a lock; a way barred from the side
the party is on; an opening that admits some things and not others; a threshold with a
condition written on it in a tongue from `setting/Language.md`.

**Triggers** - an object placed, fitted, or returned; a phrase spoken in the right tongue;
a sequence pressed, turned, or lit; weight applied or removed; a specific person or thing
brought near; something given up.

## Constraints

- **Ward and illusion are sorcery, and `GENRE.md` prices it.** Each has a maker traceable
  to an event in `setting/History.md`, and a region carries at most one of them - the same
  one a warded exit drawn at `dangerous/Door.md` spends, since both reach a ward through
  this file. The other four fixtures are things people built, and a region that reaches for
  the two rare ones twice has made sorcery the ordinary case.

- **A fixture whose answer is elsewhere in the region is a lock.** It owes a
  `setting/Keys.md` row through `dangerous/Key.md`'s demand end, or the party arrives at a
  socket that nothing in the setting fills.

- **A fixture that costs on contact is a hazard.** A mystery is neutral until a real
  attempt fails; anything that acts on entry, on touch, or on presence is drawn at
  `dangerous/Hazard.md` and stops competing with this file for the same room.
