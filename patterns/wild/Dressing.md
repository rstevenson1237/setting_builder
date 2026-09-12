# Wild - Dressing

## Provides
The physical reality of a WILD location, where it sits in its region, how its parts read
as one place, and how it sounds on the page.

## Read at
**Mode: second pass.** Step 4c, drawn unconditionally by `wild/Landmark.md`,
`wild/Hidden.md` and `wild/Secret.md`'s substrate blocks - every WILD location without
exception. Units, the Exits syntax and the citation formats are in
`templates/Location.md`.

## Spec

```
DRESSING - every WILD location
  1     Size and shape, in yards
  1     Position within the region - a bearing from the entry or a named Landmark
  1     Condition - what weather, season, and time have done to it since
  1     Purpose - per its kind file (Ruin, Lair, Natural Feature, or Crossing); not
        restated here
  1     Ambiance - smell and sound, attributable to Condition or Purpose
  1     Every exit typed and positioned
```

There is no detail budget in WILD. Every location gets the full treatment, because none of
them is filler - a region holds only about as many as its die, and a landmark written thin
has wasted one of ten slots. Depth comes from attaching children, not from writing some
parents lighter than others.

Hidden and Secret locations skip the position line: their position is defined by the
parent they hang off.

## Design patterns

**Scale in yards.** Outdoor footprints are measured in yards, because feet read as false
precision once there are no walls to measure to. A vertical drop or climb stays in feet
either way - that is a mechanical measurement, not an areal one. Distance between
locations follows the same split: yards for a short hop, miles for a long trek.

**Position.** A cardinal bearing from the region's entry, or a distance and direction from
another named Landmark. In a point crawl this is the only spatial information a party
gets, and it is what lets a referee say where they are when they are between things.

**Condition.** A WILD location is exposed, and what weather, season, and time have done to
it is stated before anything else physical: what it is like in rain, what it is like at
night, what the season is doing to the footing and the cover, what has changed it since it
was last what its kind file says it is - worked, disturbed, reclaimed, damaged by a past
event. This is also where a location earns a second visit - the same place in different
weather is genuinely different.

**Ambiance.** Smell and sound, minimum one, and both **attributable** - caused by Condition
(what the weather, season, or an event have done here) or by Purpose (what grows, lives, or
happens here). Outdoors the reliable registers are what the air smells of and what sound
does across open ground or under canopy; temperature and footing are real but follow from
Condition, and belong there or in a Feature when they matter enough to act on. A fact
equally true of the whole region belongs in the Region Overview's own Ambiance field, not
here.

**Exits.** Every exit gets a type and a position: what indicates the way, and which
direction it leads. Outdoors, position is a compass direction or a relation to something
stated - along the ridge, past the treeline, down the watercourse. Two exits reading
identically is a failure here for the same reason it is underground: it turns a choice
into a guess.

**Integration.** Everything here was shaped by the same ground, the same weather, and the
same tenancy. Before the entry is done, check that its parts could plausibly share a place
- and where one cannot, change it rather than explaining it.

**Vocabulary, per `GENRE.md`'s Voice.** Real terms for landform, watercourse, vegetation and
weather - scree, corrie, holt, spinney, sike, hag, tor, brake. Name the species rather than
"trees."

## Constraints

- **Purpose is supplied by the kind file, not restated here.** `wild/Ruin.md` states
  what a Ruin was, `wild/Lair.md` states why its occupant stays,
  `wild/NaturalFeature.md` states why a party would stop, `wild/Crossing.md` states what
  must be crossed - whichever applies has already answered "what is this for." Dressing
  does not reopen that question; it dresses the answer. Every WILD location draws exactly
  one kind, at all three tiers, so there is never a location with no answer to fall back
  on.

- **No detail budget is not a licence to explain at length**, and WILD is the rating
  most likely to confuse the two. Every location getting the full treatment means every
  location gets its position, its Condition, its Ambiance and its full complement of
  Features - it does not mean any of those may be written out at length. A WILD entry
  runs long in two specific ways: the connective texture that belongs in the Region
  Overview's Terrain field gets written out again here, or a detail is given its causal
  history instead of just being present.
