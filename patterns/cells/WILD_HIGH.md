# WILD_HIGH

> The arrival, and the thing worth leaving it for.

A `WILD_HIGH` location is why the road exists. It is the place a party walks
watches to reach, reads, takes something out of, and leaves while the walk back
still costs less than the thing is worth. Every region carries at least the
floor set by `region_weights.<weight>.high_min` in `config/weights.yaml`, and in
a `WILD` region those floors are the arrivals.

## What belongs here

- **An approach written as its own passage.** The non-visual cue first, at a
  stated distance, then what changes on the way in, then the arrival. A landmark
  that begins at the door has thrown away the best ground in the cell. State
  what turning back costs at each stage, and make the earliest stage cheap.

- **Something extractable, and it is not always an object.** A route, a name, a
  working device, a way in, a measurement, a person willing to be led out. Name
  what it is, what it weighs a party down by, and what it is worth to somebody
  in a lit place.

- **A reason it has not already been emptied.** The walk, the gate, the thing
  standing in the water, the fact that nobody who knows the way says so. State
  it plainly in the Referee Overview, because a landmark with no answer to this
  question reads as a prop.

- **Layers, all three of them.** The landmark layer is what is seen on arrival.
  The hidden layer is opened by asking about a thing named in the Overview or by
  spending time on it. The secret layer is inside a feature and gated on a named
  physical action — standing somewhere, clearing something, speaking a name,
  looking back. Every secret carries at least one clue.

- **A gate with a priced answer.** The characteristic shape of this cell is one
  gate, two ways through, and neither of them free. Where the gate opens to a
  key, both ends go in `T-KEY`. Where the bypass is cheaper in time, its cost is
  what the party arrives without: unpractised, unmet, or burning light they will
  want later.

- **Terrain that stops being the region's.** The ground here is not the road's
  ground, and the difference is the arrival. State the new rate, the new
  footing, and what the old units no longer measure.

- **A departure that is not the arrival reversed.** What is different on the way
  out: what has been spent, what is now carrying weight, what was passed on the
  way in and reads differently now, and what waits between the party and the
  road.

## Where the boundary falls

- **Down to `WILD_MEDIUM`** when this is a hard piece of route rather than a
  destination. Ask what a party carries away. If the answer is only that they
  are past it, it is a crossing.

- **Down to `WILD_LOW`** never directly. A landmark that turns out to be thin is
  a `MEDIUM` and the region needs its landmark written somewhere else.

- **Not this cell** when the place is hunted rather than reached — when the
  content is what lives here rather than what is here. That is a `DANGEROUS`
  region, and mislabelling it puts a party on a road with no Dangers table
  behind it.

## Form

- **Player Overview:** ten to sixteen sentences, in the order of the approach.
  Bold four or five nouns and give every one a feature. It shows and never
  concludes: it says the ring is clean and never that the ring is important.
- **Features:** four to six. One carries the gate, one carries the secret, one
  carries the connection pointer back to the route.
- **Referee Overview:** approach cue and distance, then terrain and rate, then
  why it is still here, then the gate and both prices, then the departure. Then
  the straight instances funding any reversal, by code.
- **Exits:** two or more where the fiction allows it. A landmark reachable one
  way only states why, and states what the one way costs in both directions.
- **Tokens:** referee-facing, beside the feature that carries them. Treasure
  carries value, weight and quality. Nothing carries a token in the Player
  Overview.
- **Tables it leans on:** `T-ARC` and `T-HAZ` for the ground, `T-KEY` for the
  gate, `T-LOR` for what is legible here, `T-TRE` and `T-HRD` for what comes
  out, `T-BES` and `T-CRE` for whatever stands in it, `T-PRC` for the way in.

## Worked example

An illustration of the shape and the register. Nothing in it is canon, and the
codes are stand-ins.

**Player Overview.** The water shallows over a floor that is not the fen's:
dressed slabs, laid true, holding at a depth of a hand for thirty yards in every
direction. At the near edge, standing clear of the water, is **a votive shelf**,
its outer lip cut with slots. Beyond it the roof of **the inner cell** breaks the
surface like the back of something lying down, and its lintel is square and
whole. **A bronze ring** is set into the shelf where a hand would fall.
Everything here is green with age. The ring is not. The reeds stop thirty yards
out on every side and do not begin again.

**Referee Overview.** *Approach:* the sound goes first. A party coming east
along the span stops hearing its own wading a hundred yards short of the shelf.
There is a full watch of open span behind them at that point and turning back
costs only the watch. *Terrain:* dressed slab under a hand of still water,
walked at the road rate and no slower. Off the dressed floor it is open mere with
no bottom found. *Why it is still here:* the way in is a gate and the key is a
mile back up the road in a socket nobody has a reason to reach into. *The gate:*
the shelf's centre slot takes the clapper and lifts the door slab; that costs the
party the clapper, which stays in the slot while the slab is up. The answer that
is not the key is the fallen east wall, which is longer, underwater the whole
way, and dark {TEST: Constitution} {WOUND: Frost}. Neither is the mistake.
*Departure:* what stood in the shallows and let them pass inward puts itself
between them and the span when they turn to leave. The span runs back west to
the road -> R04-L03.

## Excluded patterns

- **A landmark that is only large.** Scale is not content. What is here has to
  be readable, handleable and leavable.
- **An arrival with no cue.** The type requires a non-visual approach cue at a
  distance a party can still turn back from. A landmark that is first noticed on
  reaching it is an ambush.
- **A gate with one answer.** Two routes, both priced, and the text never names
  the mistake.
- **A secret found by searching.** Secrets are gated on named physical actions.
  What time spent searching costs is a separate matter and it is `T-PRC`.
- **A reversal with nothing funding it.** A landmark that is not what it appears
  names the straight instances paying for it, by code, in the Referee Overview.
- **A dungeon.** Depth, rooms, turns and a Dangers table belong to a
  `DANGEROUS` region. This cell is a place on the surface, reached across
  distance, and it is counted in watches.
