---
id: region.decorator.prose
target: region
phase: decorator
writes: [Overview]
dependencies:
  - container:${CONTAINER_ID}
  - table:S-AMB
  - table:T-ARC
  - table:T-LNG
  - table:T-NAM
  - config
output_template: templates/region.md
schema_version: 1
---

Step 8. The Decorator writes the region's Overview: what a person standing
anywhere in this region sees, hears and is walking on.

This is the last region-scale pass, and it is the one a referee reads first at
the table. It is also the last chance to demote. The Fields are written, the
tables are written, and reading them back is how the sentences that are really
about one location get found and pushed down into the locations step 9 is about
to stub.

## Patterns

**The Overview is player register.** It shows and never concludes. It carries no
mechanical token (M24), states no measurement a `Fields` line already carries,
and leaves what it implies to the table. Three or four paragraphs.

**Every noun in it is true everywhere in the region.** The same
least-common-denominator rule that binds `GENRE.md` and the setting Overview,
one scale down. The test is mechanical: name a place inside this region where
the sentence is false. If one exists, the sentence belongs in that place, and
step 9 is about to stub it.

**Demote before writing, not after.** Split each field into clauses, name a
destination for each clause that is about one place, and carry the destination
forward as a location the region needs (J1). A region Overview that describes
its landmark has spent the landmark's best material a scale too high, and the
location will read as a repetition when it arrives.

**Write from the ground, in the order a person meets things.** What is underfoot,
then what is at eye level, then what is at the horizon, then what does not
behave the way the other three suggest. A region that is entered from one
direction is described from that direction.

**Say what the region sounds like and what it does to sound.** The setting's
Style section states the register; the region states its own acoustics, its own
smell, its own light and its own temperature. `S-AMB` is where the setting's
sensory register lives and this is the scale that spends it.

**Both naming layers appear where the region carries both.** A place with a
living name and an older one is worth naming twice, because the disagreement
between the two says who named it and when. Every name decomposes into roots in
`T-LNG` (M18), and a name that needs a new root waits for the root rather than
coining it.

**The Overview and the region's type agree without stating it.** A `SAFE`
region reads as somewhere people are, a `WILD` region as ground between places,
a `DANGEROUS` region as somewhere that was built and is now occupied. The
Overview never names the type, the difficulty or the weight: it is the thing
those dials describe.

**Strike every architect note this pass closes**, and record the region with
`python tools/ledger.py decorated <code>`. After this step `validate.py` reports
any note that survives in a decorated file (M25).

## Excluded patterns

- **A conclusion.** "The silence is unnerving" states what a player is to feel.
  Write the silence and the distance at which it starts.
- **A named location.** The roster is step 9 and the description is step 12. A
  region Overview that names its landmark has written the landmark.
- **A mechanical token, a die, or a stated difficulty.** Referee-facing, and
  this section is not.
- **A measurement the Fields already carry.** The Overview shows the extent; the
  Fields state it. Saying it twice guarantees the two will disagree eventually.
- **Genre restated.** `GENRE.md` is in every bundle already. Where the Overview
  would say the same thing, it says nothing.
- **A sentence that is false anywhere in the region.** It is a location, and it
  is written as one.
- **A revision note.** The superseded paragraph is rewritten and git holds the
  history.

## Design questions

1. **What does a person see, hear, smell and stand on anywhere in this region?**
   Every noun survives the "name a place where this is false" test.
2. **Which direction is this region entered from, and what is met first?** The
   Overview is written in that order.
3. **What does this region do to sound and to light?** Two of the four senses
   the setting's ambiance carries, spent at the scale where they are local.
4. **Which sentences turned out to be about one place?** Name the location each
   becomes, and hand the list to step 9.
5. **Which names here carry two layers, and what do the two disagree about?**
   That disagreement is content and belongs in the Overview.
6. **What would a referee expect from a region of this type that this one does
   not have?** Name the absence, and let the Overview show what stands in its
   place.
