# Dangerous - Dressing

## Provides
The physical reality of a DANGEROUS location, how much of it the weight class earns, how
its parts read as one place, and how it sounds on the page.

## Read at
**Mode: second pass.** Step 4c, for every DANGEROUS location without exception - unlike
the element files, this is not conditional on a spec line drawing it. Units, the Exits
line syntax, and the citation formats are in `templates/Location.md`.

## Spec

```
DRESSING - every location
  1     Size and shape
  1     Condition - active use, or former use: abandoned, decayed, ruined, destroyed
  1     Purpose - what it was for
  1     Ambiance - smell and sound, attributable to Condition or Purpose
  1     Every exit typed and positioned
```

## Design patterns

**Condition.** Every room sits somewhere on a line from still in use to gone entirely, and
where it sits is stated before what it was for:

*Active* - still used for its purpose, by whoever is here now.
*Abandoned* - left, not fought over or reclaimed; intact but empty.
*Decayed* - standing, but failing on its own - rot, rust, damp, subsidence, vermin.
*Ruined* - a structural failure has happened - a collapse, a breach, a fire - and the room
reads as an event, not just neglect.
*Destroyed* - the room's original form is no longer legible; what is left is debris,
footprint, or absence.

**Purpose.** Every room was for something, even where Condition means it no longer is. A
former purpose is a source of detail on its own - tool marks, worn grooves, fixtures left in
the wall, a floor sloped to drain somewhere. Draw from the region's Architecture and what
its occupants needed:

*Keeping* - storeroom, larder, cistern, well, granary, vault, armoury, firewood store,
tack room.
*Working* - smithy, kiln, workshop, mill, tannery, dye house, mine face, mushroom bed,
scriptorium, laundry.
*Living* - barracks, bedroom, living quarters, common room, kitchen, dining hall, nursery,
bath, latrine, guano pit.
*Holding* - guardroom, guard chamber, gatehouse, prison cell, slave pen, kennel, cage
room, torture chamber.
*Meeting* - antechamber, great hall, banquet hall, throne room, audience chamber, arena,
court.
*Believing* - chapel, shrine, vestry, chantry, reliquary, oratory.
*Dying* - crypt, ossuary, charnel pit, mortuary, catacomb, barrow chamber.
*Moving* - stair hall, landing, ramp, shaft head, bridge span, dock, culvert.

**Ambiance.** Smell and sound, minimum one, and both **attributable** - caused by Condition
(rot, standing water, settling stone, vermin) or by Purpose (what was made, stored, or done
here), never free-floating mood. A smell or sound equally true of any room in the region
belongs in the Region Overview's own Ambiance field, not here - per this file's Constraints
below. Temperature and footing are real facts but follow from Condition; state them there,
or in a Feature line, when they matter enough to act on.

**Exits.** Every exit gets a type - material, construction, condition - never just "a
door." Every exit gets a position: which wall or corner it opens from.

Two exits of the same type are told apart by their positions and their details, and this
is not housekeeping. **It is what makes a branch a decision rather than a coin flip.** A
party choosing between "a door" and "a door" is guessing. A party choosing between "a low
door, scorched black around the frame" and "a wide arch, its threshold worn smooth" is
deciding. Where the region's graph marks a location a branch or a divide, its exits carry
the weight of that choice and must earn it.

**Integration.** The last pass, and the one that separates a location from a list of
features. Everything in the room was put there by the same history: the same builders, the
same occupant, the same collapse, the same water. Before the entry is done, check that
each feature could plausibly share a room with the others - and where one cannot, change
it rather than explaining it.

**Vocabulary, per `GENRE.md`'s Voice.** Real architectural terms - corbel, lintel,
revetment, spandrel, newel. Real trades and their leavings. Real materials named as
materials.

## Constraints

- **Details already included in the region description are not included here.** A prior
  full build had a Region Overview claim a recurring motif that fewer than a third of the
  region's locations actually carried - the claim existed at the overview level and nowhere
  a party could touch it. Per `GENRE.md`, say a thing once, at the highest level where it is
  true: a location's Dressing states what is specific to it, not what the Region Overview
  already covers for the whole region.

- **Do not reuse a purpose already used in this region.** Repetition is the failure this
  list exists to prevent, and a region with three storerooms has told the party that
  rooms do not matter. A room whose Condition is destroyed enough that Purpose reads as
  illegible is still drawn from this list - state what it was, then let Condition
  explain why it no longer shows.

- **Do not let every room in a region land at the same point on this line.** Variance
  here is what makes "how the place answers intrusion," per the Region Overview's
  Dangers field, something a party reads room to room rather than a claim stated once
  and never felt.
