---
id: location.decorator.prose
target: location
phase: decorator
writes: [Player Overview, Referee Overview]
dependencies:
  - region:${REGION_CODE}
  - container:${CONTAINER_ID}
  - cell:${CELL}
  - siblings:location:${REGION_CODE}
  - table:T-ARC
  - table:T-LNG
  - table:T-NAM
  - table:T-LOR
  - table:T-RUM
  - config
output_template: templates/location.md
schema_version: 1
---

Step 12. The Decorator writes the Player Overview and the prose of the Referee
Overview, and strikes every architect note the file still carries.

This is the last pass in the project. What it writes is the first thing a
referee reads at the table and the only thing a player ever hears, and it is
written last because it is written against finished content: the fields are
set, the features are written, and the Overview's job is to promise exactly what
is below it and nothing else.

```
python tools/resolve_deps.py --pattern location.decorator.prose --target R0n-L07
python tools/ledger.py done 12 R0n-L07 && python tools/ledger.py decorated R0n-L07
python tools/validate.py --scope R0n
```

## Patterns

**The Player Overview is player register.** It shows and never concludes. It
carries no mechanical token (M24), states no measurement the fields already
carry, and leaves what it implies to the table. Plain nouns and what a thing is
made of. Say the ring is clean; never say the ring is important.

**Every bolded noun is a promise and the feature below is the promise kept**
(M17). The check runs one way only: a feature may have no bolded noun above it,
but a bolded noun with no feature is a thing a referee cannot answer a question
about. Bold to the cell's count and no further, and bold the thing rather than
the sentence.

**Write in the order a party meets things.** For a `WILD` or `DANGEROUS`
location that is the order of the approach: the cue, then what changes on the
way in, then the arrival. For a `SAFE` location it is the walk from the door.
Dimensions and material first where the cell says so, then what is in it, then
the state it is currently in.

**The Referee Overview is plain, bounded and spatially precise.** It states
facts, because that is its job. Measurements and directions stated, in the
region's units. What is true that the Player Overview withholds. The reactions
and their branches. The gate and both prices. What the place costs in the
region's time unit. A referee runs the location from this section without
inventing a fact (J10).

**Both registers, and neither borrows from the other.** Player text that states
a conclusion has done the party's reading for them. Referee text that withholds
a measurement to preserve atmosphere has failed the person it is written for.

**Say what the location does to sound, to light and to the footing**, in its own
words rather than the region's. The region's Overview carries what is true
everywhere; this is the scale where the senses are local, and the difference
between the two is what makes an arrival read as an arrival.

**Both naming layers where the location carries both.** A place with a living
name and a Covenant one is worth naming twice, because the disagreement between
them says who named it and when. Every name decomposes into roots in `T-LNG`
(M18), and a name needing a new root waits for the root.

**Nothing in the Overview is true of the region rather than of here.** The test
is mechanical, run in the other direction from step 8's: name the sentence that
would be equally true standing anywhere else in this region. If one exists, it
belongs in the region's Overview, which is already written, and here it is
repetition.

**Strike every architect note the file still carries.** The location is closed
after this pass and `validate.py` reports any note that survives in a closed
file (M25), then fails on it under `--final`. A note is struck when its content
is absorbed, and a note whose content was never absorbed is unfinished work
rather than a formatting problem.

**Record the file with `python tools/ledger.py decorated <code>` after every
target**, never at the end of the region. That record is what makes M25 apply
to this file and what lets the step survive the end of a conversation.

## Excluded patterns

- **A conclusion.** "The silence is unnerving" states what a player is to feel.
  Write the silence and the distance at which it starts.
- **A mechanical token in player-facing text.** Referee-facing, always, and
  `validate.py` reports it separately at location scale.
- **A bolded noun with no feature.** The one check in the corpus that exists
  because the failure is invisible to the person writing it.
- **A measurement stated twice.** The Overview shows the extent; the fields
  state it. Saying both guarantees they will disagree eventually.
- **An architect note left in.** The pass that closes the file is the pass that
  strikes them.
- **A sentence that is true anywhere in the region.** It is the region's and the
  region already has it.
- **Genre or setting restated.** `GENRE.md` is in every bundle and the setting's
  Style section is written. Where the Overview would repeat either, it says
  nothing.
- **A revision note.** The superseded paragraph is rewritten and git holds the
  history.
- **New content.** This pass writes prose over finished features. A fact that
  appears here for the first time is a step 11 fact arriving a pass late, and it
  is written into the feature it belongs to.

## Design questions

1. **What does a party see, hear, smell and stand on when they arrive here, and
   in what order do they meet it?** That order is the Player Overview.
2. **Which nouns are bolded, and does each have a feature?** Read the Features
   list first and bold from it, rather than bolding and then hoping.
3. **What does this location do to sound and to light that the region does
   not?** If the answer is nothing, say nothing, and do not fill the space.
4. **Which sentence here would be true standing anywhere else in this region?**
   Cut it. The region's Overview already carries it.
5. **Can a referee run this location from the Referee Overview alone?** Read it
   as one. Name the fact they would have to invent.
6. **Which architect notes are still in the file, and was each one's content
   absorbed?** A note whose content was never absorbed is not a formatting
   problem.
