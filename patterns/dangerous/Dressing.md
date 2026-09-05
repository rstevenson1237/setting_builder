# Dangerous - Dressing

## Decides
The physical reality of a DANGEROUS location, how much of it the weight class earns, how
its parts read as one place, and how it sounds on the page.

## Read at
Step 4c, for every DANGEROUS location without exception - unlike the element files, this
is not conditional on a spec line drawing it. Units, the Exits line syntax, and the
citation formats are in `templates/Location.md`.

## Spec

```
DRESSING - every location
  1     Size and shape
  1     Purpose - what it was for, and whether that use still holds
  1     One sensory fact beyond the visual
  1     Every exit typed and positioned
```

Detail beyond that baseline is what the weight class buys:

```
DETAIL BUDGET
  low weight     baseline only. Nothing should read as unusual or invite a second look
  medium weight  one detail out of spec - an irregular shape, an incongruous former use,
                 a second sensory fact, or a notable exit. Still dressing, still in the
                 Referee Notes or the Exits line
  high weight    dressing becomes exploration material. Several details out of spec, and
                 where one gives players something to act on, it is promoted to its own
                 Feature line
```

```
WORD BUDGET - the whole entry, excluding the header line and the Exits line
  low weight     ~140 words
  medium weight  ~220 words
  high weight    ~320 words
```

**The budget is diagnostic, not a target.** The detail budget above governs how many things a
room holds; nothing governed how many words each thing got, and that is the gap this closes.
A room over budget is almost never a room holding too much - it is a room whose contents have
been explained. Per `templates/Location.md`, find the sentence that says why a detail is
there, what it means, or what the party will conclude from it, and delete that before
touching a fact.

The ratio is the point as much as the numbers: a low-weight room should read as a fraction of
a high-weight one, and if low and high are within a third of each other on the page then the
weight classes are not doing any work no matter what the spec says they contain.

## Patterns

**Purpose.** Every room was for something, even if it has stopped being for it. A former
purpose is a source of detail on its own - tool marks, worn grooves, fixtures left in the
wall, a floor sloped to drain somewhere. Draw from the region's Architecture and what its
occupants needed:

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
*Failing* - debris room, collapsed section, mined-through wall, flooded room, burned room,
a space whose purpose is no longer legible at all.

**Do not reuse a purpose already used in this region.** Repetition is the failure this
list exists to prevent, and a region with three storerooms has told the party that rooms
do not matter.

**Sensory.** One fact beyond the visual, minimum, and it must be **attributable** - caused
by something already stated about the room: its purpose, its occupant, its decay, its
materials, what is on the other side of its walls. A smell that would be equally true of
any room in the region is not a detail. Reach for temperature, air movement, what the
floor does underfoot, what sound does in the space, and what the room smells of, before
reaching for a noise with no source.

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

**Voice.** Per `GENRE.md`: specific vocabulary before general. Real architectural terms -
corbel, lintel, revetment, spandrel, newel. Real trades and their leavings. Real materials
named as materials. Where a plainer word would also do, the precise one is the one to use.

## Constraints

- **Brackvaen, C.15 Peluath.** First full build ran low-weight rooms at 341 words, medium at
  422 and high at 609 - a spread of under 2x across classes whose whole distinction is how
  much they present. C.15's five Features held roughly 130 words of fact and 320 of
  explanation, and the room stated the answer to its own problem (stand off the groove)
  three separate times, twice in the entry and once in the Region Overview. The detail
  budget above was being honoured and the entry was still four times too long, because
  nothing budgeted the words each detail got. Hence the word budget, and hence
  `templates/Location.md`'s rule that every sentence be a thing, an action, or an effect.

- **Budget calibration, clean-room test.** The first figures set were 120/180/260 and all
  three were about 20% too tight. Writing one room per class from scratch against `GENRE.md`
  and this folder alone - drawing the spec rates honestly, and at or just under each class's
  *expected* number of content items - landed at 132/212/311 after a full pass cutting
  commentary. Further cuts would have removed facts, which rule 3 forbids. Raised to
  140/220/320, which holds the ~2.3x low-to-high ratio that is the point of the budget and
  is still roughly a 55% cut from the first build's measured 341/422/609. The lesson for
  anyone re-tuning these: a class's budget has to be set against what its spec actually
  mandates at an average draw, and HIGH mandates the most, so it needs the most headroom
  rather than a proportional share.

- **A region-wide motif that stops at the Region Overview.** A prior full build had a
  Region Overview state a recurring architectural or material motif running through a
  region, and fewer than a third of that region's locations actually carried it - the motif
  existed at the overview level and nowhere a party could touch it. Per `GENRE.md`, a
  region-level claim is only real if it's cited by the rooms underneath it; when drafting
  a location, check whether its Region Overview asserts a running motif and, if so, either
  carry it into a Feature or the sensory line, or flag it at 4e for the overview to cut.
