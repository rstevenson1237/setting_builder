# Dangerous - Dressing

## Provides
The physical reality of a DANGEROUS location, how much of it the weight class earns, how
its parts read as one place, and how it sounds on the page.

Units, the Exits line syntax, and the citation formats are in `templates/Location.md`.

## Spec

```
DRESSING - every location
  1     Size and shape
  1     Condition - active use, or former use: abandoned, decayed, ruined, destroyed
  1     Purpose - what it was for: keeping, working, living, holding, meeting,
        believing, dying, or moving something through
  1     Ambiance - smell and sound, attributable to Condition or Purpose
  1     Every exit typed and positioned                 (dangerous/Door.md)
```

**Condition is stated before Purpose**, since where a room sits on the line from still in
use to gone entirely decides how legible Purpose still is - a room destroyed enough reads
as debris, footprint, or absence before it reads as whatever it was for.

**A former purpose is a source of detail on its own** even where Condition means it no
longer is - tool marks, worn grooves, fixtures left in the wall, a floor sloped to drain
somewhere. Draw it from the region's own Architecture and what its occupants needed, never
freely invented.

**Ambiance is attributable, never free-floating mood** - caused by Condition (what decay
sounds and smells like) or by Purpose (what was made, stored, or done here). A smell or
sound equally true of any room in the region belongs in the Region Overview's own Ambiance
field instead, per this file's Constraints below. Temperature and footing are real facts
but follow from Condition; state them there, or in a Feature line, when they matter enough
to act on.

**Integration is the last pass**, and the one that separates a location from a list of
features. Everything in the room was put there by the same history: the same builders, the
same occupant, the same collapse, the same water. Before the entry is done, check that each
feature could plausibly share a room with the others - and where one cannot, change it
rather than explaining it.

**Name real architectural terms, real trades, and real materials rather than describing
them.** A part or a process with a name costs less than the sentence describing it.

## Constraints

- **Details already included in the region description are not included here.** Per
  `GENRE.md`, say a thing once, at the highest level where it is true: a location's
  Dressing states what is specific to it, not what the Region Overview already covers for
  the whole region. The inverse is the failure to watch for - a motif claimed at the
  overview level and carried by only a handful of the region's locations exists nowhere a
  party can touch it.

- **Do not reuse a purpose already used in this region.** A region with three storerooms
  has told the party that rooms do not matter, whatever category each one answers to. A
  room whose Condition is destroyed enough that Purpose reads as illegible still states
  what it was - state that, then let Condition explain why it no longer shows.

- **Do not let every room in a region land at the same point on this line.** Variance
  here is what makes "how the place answers intrusion," per the Region Overview's
  Dangers field, something a party reads room to room rather than a claim stated once
  and never felt.
