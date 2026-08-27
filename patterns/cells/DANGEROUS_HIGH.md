# DANGEROUS_HIGH

> The region's landmarks.

A `DANGEROUS_HIGH` location is what the level is remembered as: the great
chamber, the thing at the bottom, the gate that gives the place its name, the
room every route eventually reaches. Every region carries at least the floor set
by `region_weights.<weight>.high_min` in `config/weights.yaml`, and in a
`DANGEROUS` region those floors are these rooms.

## What belongs here

- **More than one way in, and they arrive differently.** A landmark reached one
  way only is a corridor with a prize at the end. Two or three approaches, each
  arriving at a different part of the room, each having cost the party something
  different on the way. Say what each approach shows first, because what is seen
  first is what a party plans against.

- **The whole reaction surface.** The type requires reactions branching on named
  player actions, and this is the room where a referee will be asked for four in
  a row. Name the actions a party will actually take here — going in, going
  round, putting the light out, addressing the thing, taking the thing, going
  back for what they left — and answer each in a line.

- **All three layers, at full depth.** Landmark: what arriving and looking
  gives. Hidden: what asking about a named thing or spending turns gives.
  Secret: what a named physical action gives, with at least one clue, and here
  the clue is usually distributed — a `T-LOR` entry, a `T-RUM` line, a `T-KEY`
  pairing set down rooms away.

- **The region's largest gate, with the answer priced.** Both branches costed,
  and both real. Where a bypass is cheaper in time, its price is what the party
  arrives without: unpractised, unmet, or burning light they will want later.
  Where the gate opens to a key, both ends are recorded in `T-KEY`.

- **A reason it is still here.** State it plainly. The way in, the thing
  standing in it, the fact that what was taken out before was taken by people
  who did not come back up. A landmark with no answer to this reads as a prop.

- **The way out as its own content.** What has changed since they came in, what
  is now carrying weight, what was passed on the way and reads differently now,
  and what is between them and the surface. The trip back is half the session
  and this room is where it is priced.

- **Where the reversal lives, if the region has one.** This is the cell that can
  afford it, and it is funded by convention held elsewhere. Name the straight
  instances paying for it, by code, in the Referee Overview.

## Where the boundary falls

- **Down to `DANGEROUS_MEDIUM`** when the consequence stops at the room. A room
  with a hard fight and a good hoard is a working room. A room that changes what
  the rest of the level means is a landmark.

- **Not this cell** when the room is only the biggest. Scale is not content, and
  a hall a hundred feet across with one thing in it is a `LOW` room that has
  been inflated.

- **Not this cell** when the room is the last one and nothing else. Position in
  the map is not a landmark. Something has to come out of it.

## Form

- **Player Overview:** twelve to twenty sentences, written in the order of the
  approach a party is most likely to take, with the other approaches noted in
  the Referee Overview. It shows and never concludes. Bold four to six nouns and
  give every one a feature.
- **Features:** four to seven. One carries the gate. One carries the secret. One
  carries the connection pointer to each route out.
- **Referee Overview:** each approach and what it shows first, then the reaction
  list, then why the place is still here, then the gate and both prices, then
  the departure, then the funding for any reversal, by code.
- **Exits:** every route in and out, each with a cue, and each stating what it
  costs going the other way. A one-way route says what makes it one-way from the
  far side.
- **Tokens:** referee-facing, beside the feature that carries them. Everything
  taken out carries value, weight and quality, and the weight is what makes
  taking it a decision.
- **Tables it leans on:** `T-CRE` and `T-BES` for what is here, `T-KEY` and
  `T-PUZ` for the gate, `T-LOR` and `T-TOM` for what is legible, `T-TRE` and
  `T-HRD` for what comes out, `T-ARC` for the stonework the level has been
  teaching the party to read.

## Worked example

An illustration of the shape and the register. Nothing in it is canon, and the
codes are stand-ins.

**Player Overview.** The stair comes out at a gallery, and the floor of the
chamber is forty feet below it. The chamber is round, a hundred feet across, and
the walls are the only true masonry on the level: courses a foot high, laid
without mortar, running unbroken all the way round. In the centre, on a floor of
the same stone, stands **the frame** — four uprights and a ring, tall enough to
walk under, with nothing hanging in it. **A drift of silt** banks against the
north wall to the height of a man, and things stand up out of it at angles.
Around the base of the wall, at the height of a hand, runs **a cut line**, level
all the way round, and the stone below it is a different colour. The air is dry.
Everything here is dry, and the level above is not.

**Referee Overview.** *Approaches:* the gallery stair shows the frame first and
the silt not at all. The flooded passage from the east comes out at floor level
inside the drift and shows what is standing in it before anything else. The
worked face from the south comes out behind the frame and shows the ring from
below, which is the only angle the ring can be read from. *Reactions:* going
under the ring, addressing the thing in the silt, putting out the light,
touching the cut line, going back up before the frame is worked. *Why it is
still here:* three parties reached it. What came out was carried by the last of
them as far as the gallery, and it is still on the gallery. *Gate:* the ring
takes the clapper and the clapper is two levels up in a socket
(KEYS, T-KEY-04). The answer that is not the key is the cut line, which is a
water mark, and the chamber can be filled from the flooded passage until the
frame floats what is under it {TEST: Sanity} {WOUND: Frost}. That costs the
party the dry floor and everything standing in the silt. Neither is the mistake.
*Departure:* what is taken out weighs what it weighs, and the worked face south
cannot be climbed by anyone carrying it {WT: 30} {QUALITY: Artifact}. *Funding:*
the frames at (ARCHITECTURE AND TERRAIN, T-ARC-02) and the votive shelf at
(ARCHITECTURE AND TERRAIN, T-ARC-03) are both exactly what they appear to be.
This is the one place on the level where the empire's own work is turned against
its purpose. The gallery stair runs back up -> R06-L11.

## Excluded patterns

- **A boss room.** A thing that waits to be fought and does nothing else is a
  statistics block with a floor under it. Whatever is here has a want, a
  territory and a reaction to being left alone.
- **A single approach.** More than one route reaches most places, and every
  route into a landmark costs something different.
- **A finale.** The setting is a standing situation. Nothing here is the end of
  anything, and nothing is written to happen in a particular order.
- **A secret with no clue.** Least of all here. The region's biggest secret
  carries its clue in the tables, placed rooms or miles away.
- **A reversal with nothing funding it.** Name the straight instances by code or
  do not write the reversal.
- **An explanation.** What happened is `S-HIS`, and it reaches a party through
  `T-LOR` and `T-RUM` as fragments. This room states what is physically here and
  withholds what it means.
- **Padding by scale.** A bigger room is not a better one. What makes this cell
  is that something comes out and something changes.
