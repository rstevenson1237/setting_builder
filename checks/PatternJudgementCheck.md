# Pattern Judgement Check - 2026-09-04, first full pass after the Brackvaen build

Run against all forty-eight files in `patterns/` with `GENRE.md` and `templates/Location.md`
in view, following `templates/Pattern_Judgement_Check.md` - including its inversion, that
**two restatements which read the same are a finding rather than a convenience.**

The library is in good shape. The specific/discoverable/interactive/not-generic tests pass
almost everywhere, and the deliberate restatement across the three rating folders has done
what it was supposed to do: a trap in SAFE, WILD and DANGEROUS are three different objects
written three different ways, and so are secrets, dressing, lore, quests and keys. Four
things need attention, and one of them is structural.

---

## Cross-pattern

- **No overlap or contradiction: Needs Attention.** Two items, one of them the inverted
  duplication check.

  *Restatement that has collapsed.* `patterns/setting/Keys.md`, `safe/Key.md`,
  `wild/Key.md` and `dangerous/Key.md` all state the same sentence: "a key that opens
  nothing is treasure." `safe/Key.md` and `wild/Key.md` state it identically, word for
  word, including the follow-on: "Cite a table and move on." That is a *criterion* - what
  earns a row - and by the inversion it belongs in `patterns/setting/Keys.md` alone, which
  already carries it. Delete it from the three rating files. The rest of those three files
  is genuinely differentiated and should stay: in SAFE the key has a holder and the holder
  is the obstacle, in WILD it is the tier where key and lock got separated, at depth it is
  held by something that will not give it up. That differentiation is the good version of
  what this library is for; the shared sentence is the drift it costs.

  *A boundary that is stated well and one that is not.* `wild/Secret.md` (a whole Secret-
  tier location) against `wild/Secrets.md` (a detail concealed inside one location) is
  distinguished explicitly in both files and will not be blurred. `Mystery.md` against
  `Trap.md` is likewise clean in both WILD and DANGEROUS - a trap fires on contact, a
  mystery fires only on a failed attempt to use it, and both files say so. But
  `templates/Location.md` carries a full **Puzzles** bullet with its own rules (at least
  two physical details, an explicit trigger, a stated cost for a genuinely wrong attempt)
  and there is no `Puzzles.md` in any folder. `dangerous/Mystery.md` is plainly the file
  meant to serve it - it carries exactly those requirements - and `dangerous/High.md` even
  says "a puzzle set-piece... see `dangerous/Mystery.md`". The relationship is correct in
  substance and unnamed in the library, which is why `templates/Pattern_Judgement_Check.md`
  is still asking about a file that does not exist.

- **Gaps in coverage: Needs Attention.** Five element files are missing, and one folder is
  missing its inclusion spec.

  `patterns/safe/` has no `Trap.md`, `Creature.md`, `Treasure.md` or `Mystery.md`.
  `patterns/wild/` has no `Faction.md`. `templates/Location.md` names all five in its
  Context list as though they existed, and `wild/Ruin.md` works around the missing one by
  sending the reader to `patterns/dangerous/Faction.md` - a cross-folder reference that
  breaks `CLAUDE.md`'s rule that a generation step reads only the folder matching what it
  is building, and that hands a WILD ruin guidance written for a garrison at depth.

  The SAFE gaps are not academic. A settlement contains swindles, cutpurses, penned and
  working animals, goods for sale and things nobody can explain, and the region overview
  for A asks for all of them - `patterns/region/Safe.md` gives Treasure a field ("what is
  *for sale or in stock* rather than found") and Creatures a field ("Man, overwhelmingly...
  Anything else here is either working, penned, or a problem"). Those two fields are doing
  the work four missing files should be doing, at region scale, where they cannot be
  location-specific.

  The structural half of this is worse. `patterns/safe/Settlement.md` is SAFE's class file,
  and `templates/Location.md` says a class file "carries the **inclusion spec**: which
  lines are mandatory, which are a stated percentage, and what each draws from."
  `Settlement.md` carries no such spec. It has SETTLEMENT TYPE and PROMINENCE, both
  excellent and neither an inclusion spec - so it never says at what rate a SAFE location
  draws Commerce, Authority, Social, People, Situation, Faction, Quest, Key or Lore.
  `dangerous/High.md`, `Medium.md` and `Low.md` all do this; so do `wild/Landmark.md`,
  `Hidden.md` and `Secret.md`. SAFE is the only rating where step 1 of the reading order
  produces nothing to read, which is very likely why nobody noticed the four missing
  element files: no spec line ever drew them.

- **Unhoused user-requested content: Confirmed.** Nothing the user has asked for is
  sitting outside the library. The Brackvaen-specific mechanics that generation produced -
  the Gorm track, salt-debt, cured things, Old Rede letters - all correctly landed in
  `setting/Procedures.md` under Local Conditions rather than being force-fitted into a
  pattern, which is exactly the routing `patterns/setting/Procedures.md` prescribes.

- **A fourth item, not on the checklist but worth recording: every Constraints section in
  all forty-eight files is still empty.** The section exists to fill "only from observed
  generation failures, never from anticipation", and a complete generation run has now
  happened and produced observable failures - a coined proper noun that never reached
  `setting/Language.md`, a region-wide motif that was stated at region level and then
  carried by under a third of the locations that needed it, three of five treasure tables
  never cited. Those are precisely the entries the section was built for. The mechanism is
  sound and has not yet been used once.

---

## patterns/setting/

Fifteen files. All fifteen are Confirmed on every criterion; notes below are on what each
does particularly well or where a line is thin, not findings.

- **Outline.md** - Specific/Discoverable/Interactive/Not overly generic: Confirmed. The
  rating mixes are named as four distinct shapes with a reason each, and "start every
  region at d8 and move off it only for a reason" is a real constraint rather than advice.
  Missing relevant features: Confirmed.
- **Setting.md** - Confirmed throughout. "Tags constrain or they are wasted", with
  *dark, mysterious, dangerous* against *timber, debt, boundary*, is the single most
  useful worked example in the library. Missing relevant features: Confirmed.
- **History.md** - Confirmed. "Every event leaves a mark or it did not happen" is what
  makes this file discoverable rather than a backstory generator, and the depth-layering
  note (builder, taker, squatter) is authored here so no DANGEROUS region has to invent it.
- **Truths.md** - Confirmed. The class-not-instance rule is stated with an example on each
  side of the line, and "where truths pay off" names the three rating folders a truth must
  be visible in, which is what stops a Truth being a location feature in costume.
- **Rumours.md** - Confirmed. "Partially true is the productive band" with eight named
  ways to be partially true is the most immediately usable list here.
- **Bestiary.md** - Confirmed. The AD spread is anchored to party altitude in bold and
  restated in prose, and the "at least one entry the party is NOT meant to beat" line, with
  its requirement that that entry carry the clearest Sign and Disposition in the file, is
  where this library states its whole theory of OSR play.
- **Factions.md** - Confirmed. Visual identity is correctly identified as "the field this
  framework kept missing", and "ignorance is its own relation" gives factions something to
  do that is not conflict.
- **Treasure.md** - Confirmed. "Result 1 exists so the roll can disappoint" and the
  randomised order are correctly named as anti-optimisation rather than flavour.
- **Lore.md** - Confirmed. "Lore is an object, never spoken exposition", with rumour and
  creature knowledge routed elsewhere, is the boundary this file most needed to draw.
- **Keys.md** - Confirmed on all five criteria. See the cross-pattern note: this file
  holds the criterion three rating files are also holding.
- **Quests.md** - Confirmed. "Supply is registered by targets, not requested by givers" is
  the line that makes the whole two-ended mechanism work at 4c, and it is not obvious.
- **NamedCreatures.md** - Confirmed on the five criteria. One tension worth recording for
  the Setting check rather than as a finding here: "a slot here is earned by recurrence"
  and "heard of before met" are two different entry criteria, and the file states the first
  as the rule and the second as the best use. Five of the six Brackvaen entries earn their
  row on the second and fail the first. See `checks/SettingJudgementCheck.md`.
- **UniqueTreasures.md** - Confirmed. "Low Magic means the price is the entry" is the
  strongest anti-drift statement in the library, and **Restraint** correctly says most
  high-weight rooms are better served by a Table V citation.
- **Procedures.md** - Confirmed. "A rule belongs here if it does not change between SAFE,
  WILD and DANGEROUS" is a clean test and it held through a full build.
- **Language.md** - Confirmed. "Make them sound unlike each other" with the specific
  contrast (open running syllables against strict closed ones, five vowels against three)
  is what makes the three Brackvaen tongues audibly distinct.

## patterns/region/

Three files, one per rating, and splitting by rating rather than by tier was right - the
three overviews they produce are materially different documents.

- **Safe.md** - Specific: Confirmed. Discoverable: Confirmed. Interactive: Confirmed.
  Not overly generic: Confirmed - "a SAFE region is safe from the wilderness, not from its
  own people" reframes the whole rating. Missing relevant features: Confirmed. The People
  field's insistence that **absence is the interesting half** is the best line in the file
  and it produced Torsgaard's missing smith, healer and priest.
- **Wild.md** - Confirmed on all five. The location-count spec is stated as a pressure
  mechanism with the arithmetic shown (N locations at 1/N means exactly one expected
  encounter at every die), which converts a convention into a decision. "Depth is how a
  WILD region carries weight... a Landmark that matters more gets children" is the file's
  central idea and it is stated three times, correctly.
- **Dangerous.md** - Confirmed on all five, and the REGION KIND fork (collection against
  single holding) is the one place in the library that lets a generator deviate from a
  count and states exactly what the deviation costs - 0.6 countdown steps across a full
  clear at five rooms, "effectively no countdown at all". That is how a constraint should
  be written.

## patterns/safe/

Thirteen files. The nine that exist are strong; the four that do not are the gap above.

- **Settlement.md** - Specific: Confirmed. Discoverable: N/A, this is a class file.
  Interactive: Confirmed. Not overly generic: Confirmed - the five settlement types with
  what each can and cannot hold, and "the gate is what a type cannot hold", is a real
  constraint. **Missing relevant features: Needs Attention** - no inclusion spec, per the
  cross-pattern note. This is the library's one structural hole.
- **Commerce.md** - Specific: Confirmed. Discoverable: Confirmed. Interactive: Confirmed.
  Not overly generic: Confirmed - "the gap is more useful than the stock", and prices
  stated in cn rather than implied. Missing relevant features: Confirmed.
- **Authority.md** - Confirmed on all five. "State the edge - it is the most useful fact
  in the entry, and it is where a party's leverage lives" is the Points of Light constraint
  made mechanical.
- **Social.md** - Confirmed on all five. "Nobody is waiting for the party" and "a rumour is
  repeated, not delivered" between them prevent the two commonest failures of a tavern
  scene.
- **Situation.md** - Confirmed on all five. The six-rung worked ladder for an armed-men
  situation is the clearest escalation example in the library, and "state the next rung...
  because that is what makes a party's inaction a choice" is exactly the condition-not-plot
  distinction GENRE.md asks for.
- **People.md** - Confirmed on all five. "Draw from the roster; do not invent a cast" is
  the right rule and it names the failure it prevents. See the Setting check - the
  Brackvaen build inverted it.
- **Faction.md** - Confirmed on all five. "A faction in a settlement trades rather than
  holds... a faction present with no exchange is an occupation, and that is a Situation,
  not a presence" is a genuinely different proposition from `dangerous/Faction.md`, which
  is what the restatement is for.
- **Quest.md** - Confirmed on all five. "Terms in the giver's own words... the *generous*
  one is taking a double share, the *fair* one is taking half" is a two-line lesson in
  characterising through terms, and "what they leave out is the quest" is the file's centre.
- **Key.md** - Specific/Discoverable/Interactive/Not overly generic: Confirmed. "In SAFE a
  key has a holder, and the holder is the obstacle" is the correct tier distinction.
  Missing relevant features: Needs Attention - see the cross-pattern restatement note.
- **Lore.md** - Confirmed on all five. "SAFE lore is obtainable rather than discovered...
  the entry is about the *access*, not the finding" differentiates it cleanly from the
  other two.
- **Dressing.md** - Confirmed on all five. **Signs of use** is correctly identified as the
  SAFE-specific line ("a dungeon room records what happened to it; a settlement building
  records what happens in it, daily"), and the detail budget tied to prominence is the
  right mechanism. The vernacular paragraph is what makes a settlement read as one place.
- **Secrets.md** - Confirmed on all five. The 10% rate is the lowest of the three and the
  reasoning is given ("a settlement where every building has a hidden compartment is not a
  settlement, it is a dungeon with a market"). **Consequence** - somebody notices the party
  knows - is a payload half the other two ratings do not have and should not.
- **Naming.md** - Specific/Discoverable/Interactive: Confirmed. **Not overly generic:
  Needs Attention**, but for the opposite reason to usual - it is too *specific*, to the
  wrong thing. "The occasional **Old Rede** name marks something the settlement inherited
  and did not build" names one of Brackvaen's three tongues inside a reusable pattern file.
  See the Open Items. Missing relevant features: Confirmed - "SAFE is the only rating whose
  namers are present" and the official/actual two-layer name are both right.

## patterns/wild/

Sixteen files.

- **Landmark.md** - Confirmed on all five. "A Landmark can be named, revisited, and
  connected to. That is the test" is the line that keeps terrain out of the location list,
  and the eleven-item "reason to stop" list is concrete enough to pick from.
- **Hidden.md** - Confirmed on all five. "A Hidden location that could have been a Landmark
  has been misclassified" is the tier's whole self-test, and "it should answer something
  the parent raised" gives it a purpose beyond geography.
- **Secret.md** - Confirmed on all five. Correctly makes the Clue mandatory rather than
  rated, with the reason stated: "unreachable content is content that does not exist."
  "Clues that survive weather" is the right list for the tier.
- **Ruin.md** - Specific/Discoverable/Interactive/Not overly generic: Confirmed - the six
  kinds with their sub-lists are excellent, and "condition is the storytelling" is the
  file's key idea. **Missing relevant features: Needs Attention** - the "what holds it now"
  list points at "`wild/Faction` guidance in `patterns/dangerous/Faction.md`", which is a
  file that does not exist referred to via one in the wrong folder.
- **Lair.md** - Confirmed on all five. "Territory is what makes a lair matter to the
  region" and the observation that a lair decomposes into children more readily than any
  other kind are both doing real work for the depth mechanism.
- **NaturalFeature.md** - Confirmed on all five, and this is the hardest of the three kinds
  to write well - the file says so and then earns it. "Terrain is not a Landmark" repeats
  the Landmark test where it is most needed.
- **Creature.md** - Confirmed on all five. "A WILD creature is usually avoidable, and that
  is the point... state what it costs to go around" is the clean distinction from
  `dangerous/Creature.md`. "Populations, not individuals" is the second.
- **Trap.md** - Confirmed on all five. "In the open, almost everything gives warning" -
  and the reframing of that as *available and easy to walk past* rather than concealed -
  is a genuinely different hazard from a dungeon's, which is the restatement working.
- **Treasure.md** - Confirmed on all five. "Weather is the difference... a pristine find in
  open country needs a reason", and the note that Table V is rare in WILD and always
  attached to a Secret-tier location or a long tenancy.
- **Mystery.md** - Confirmed on all five. "Outdoors, a mystery has been exposed to weather
  and to other people. Both leave marks" gives the tier its own detail source.
- **Quest.md** - Confirmed on all five. WILD as the **carrying** end, with obstacle stated
  en route rather than at the target, is the right third role and it completes the
  give/carry/target triangle.
- **Key.md** - Specific/Discoverable/Interactive/Not overly generic: Confirmed - "WILD is
  where a key gets separated from its lock" is the correct tier role. Missing relevant
  features: Needs Attention - the shared sentence, per the cross-pattern note.
- **Lore.md** - Confirmed on all five. "Outdoors, lore is cut, not written... monumental,
  public, and meant to be read by strangers", and "a boundary stone is an argument, not a
  fact", are the sharpest lines in the three Lore files.
- **Dressing.md** - Confirmed on all five. "There is no detail budget in WILD" with its
  reason (a region holds only as many locations as its die, so none of them is filler) is
  the right departure from the other two Dressing files. Weather-and-season as the thing
  that earns a location a second visit is a good idea stated once and clearly.
- **Secrets.md** - Confirmed on all five. The 20% rate with its reason - WILD's concealment
  budget is mostly spent on the Secret tier itself - is well argued, and "clues that
  weather leaves" is a different list from the masonry cues in the DANGEROUS file.
- **Naming.md** - Specific/Discoverable/Interactive: Confirmed. **Not overly generic:
  Needs Attention** - same contamination as `safe/Naming.md`, worse. It names **Marchspeech**
  and **Old Rede** as two of its three naming registers, and describes what each is in
  Brackvaen terms. Missing relevant features: Confirmed - "who names wild country... people
  who pass through and need to talk about it afterwards" is a real insight, and the
  restraint note about a Hidden child doing better with a descriptive label than a coinage
  is correct.

## patterns/dangerous/

Fourteen files. The most complete folder, and the only one whose class files all carry a
proper inclusion spec.

- **High.md** - Confirmed on all five. The mandatory architecture line, with its reason -
  "before a party knows what is in the room, the room has to look like somewhere that
  matters" - is the right thing to make mandatory at this weight.
- **Medium.md** - Confirmed on all five. "A challenge the party cannot see is not a
  medium-weight challenge - a room built on a concealed trap presents as empty, and belongs
  at low weight with the trap as its variance" is the cleanest weight boundary in the
  library, and the treasure rates conditional on the challenge type follow the fiction.
- **Low.md** - Confirmed on all five, and this is the best file in `patterns/`. "What makes
  it low is that **it looks like nothing**", the argument for why that is the class's whole
  value, and the five node roles each stated as the player's *question* rather than as a
  content list, are why Brackvaen's thirteen low-weight rooms are not filler.
- **Creature.md** - Confirmed on all five. "Presence is rolled apart from description" -
  the room written as a den and found empty, with the thing behind the party - is worth the
  file on its own. The **Household** paragraph (food, water, waste, young, dead) hands
  players non-combat leverage and is the strongest single idea here.
- **Trap.md** - Confirmed on all five. The one-line format `tell; tell → effect; effect`,
  with the reason given - "the arrow makes it visible at a glance when a trap has been
  written with no way to detect it" - is a format that enforces its own rule.
- **Mystery.md** - Confirmed on all five. "Two details is the floor, not the target. A
  mystery with one detail is guessed at; a mystery with three is reasoned out."
- **Treasure.md** - Confirmed on all five. "Never name or describe the item" is stated
  first and given its reason, and the which-table list ties each of the five to a weight
  and a fictional situation.
- **Faction.md** - Confirmed on all five. "The difference between a lair and a held
  position is **off-site consequence**" is the whole reason this file is separate from
  `Creature.md`, and it says so.
- **Quest.md** - Confirmed on all five. "Register supply, do not wait for demand" is the
  mechanism that lets 4c work, restated here from `patterns/setting/Quests.md` in the tier's
  own terms rather than duplicated.
- **Key.md** - Specific/Discoverable/Interactive/Not overly generic: Confirmed. The Key/
  Quest opposite-ends framing is stated here better than anywhere else. Missing relevant
  features: Needs Attention - the shared sentence, per the cross-pattern note.
- **Lore.md** - Confirmed on all five. The substitutes-at-low-and-medium / sits-alongside-
  at-high rule is a genuinely useful weight interaction the other two Lore files do not
  need.
- **Dressing.md** - Confirmed on all five. The nine-category purpose list with "do not
  reuse a purpose already used in this region" is the file's main contribution, and the
  exits paragraph - "a party choosing between 'a door' and 'a door' is guessing" - states
  why position matters better than the template does.
- **Secrets.md** - Confirmed on all five. The rate table by weight and node role, and the
  argument for why the dead-end rate is 50% rather than 0% or 100% ("half is the number
  that keeps the question live"), is the most carefully reasoned number in the library.
- **Naming.md** - Specific/Discoverable/Interactive: Confirmed. **Not overly generic:
  Needs Attention** - the worst of the three. It names **Old Rede**, **Marchspeech** *and*
  **Ghaunt**, and gives a worked example in Brackvaen's own vocabulary: "Ghaunt names
  describe use, not history: the wet place, the deep den, the cold." Missing relevant
  features: Confirmed - the three-register idea and "the gap between the three registers is
  free storytelling" are exactly right and are what should survive the fix.

---

## Open Items

1. **`patterns/safe/Settlement.md` has no inclusion spec.** SAFE is the only rating whose
   class file does not say which element lines are mandatory, which are rated, and what
   each draws from - which makes step 1 of `templates/Location.md`'s reading order produce
   nothing for SAFE, and is the likeliest reason the four missing SAFE element files went
   unnoticed. Add a spec in the shape of `dangerous/Medium.md`'s or `wild/Landmark.md`'s,
   parameterised by prominence the way `Low.md` is parameterised by node role.

2. **Write the five missing element files**: `patterns/safe/Trap.md`, `Creature.md`,
   `Treasure.md`, `Mystery.md`, and `patterns/wild/Faction.md`. A SAFE trap is a swindle, a
   rigged scale, a debt written wrong; a SAFE creature is working, penned, or a problem; a
   SAFE treasure is in stock rather than found; a SAFE mystery is something the settlement
   has always done and cannot explain. A WILD faction presence is a patrol, a picket, or a
   claim on country nobody lives in - between `safe/Faction.md`'s influence and
   `dangerous/Faction.md`'s garrison. Until they exist, `templates/Location.md` names files
   that are not there and `wild/Ruin.md` sends a WILD generator into the DANGEROUS folder.

3. **All three `Naming.md` files carry Brackvaen's tongues.** `safe/Naming.md` names Old
   Rede; `wild/Naming.md` names Marchspeech and Old Rede as two of its three registers;
   `dangerous/Naming.md` names all three and gives a worked example in Ghaunt. `patterns/`
   is the reusable framework and `setting/` is the generated content, so the next setting
   built with this library inherits Brackvaen's languages by name. The underlying ideas are
   good and should be kept in the abstract - "the settlement's own tongue", "an older tongue
   found only on stone", "the occupants' tongue" - with the concrete names moved into
   `setting/Language.md`, which already carries all of them under its "Who speaks what"
   heading.

4. **The "a key that opens nothing is treasure" criterion is stated four times.** Keep it
   in `patterns/setting/Keys.md`; delete it from `safe/Key.md`, `wild/Key.md` and
   `dangerous/Key.md`. Per the inversion, two restatements reading identically - which
   `safe/Key.md` and `wild/Key.md` do, word for word - is a finding.

5. **Name the Puzzle relationship.** `templates/Location.md` has a Puzzles bullet, no
   `Puzzles.md` exists, and `dangerous/Mystery.md` is plainly the file that serves it.
   Either say so in `templates/Location.md` and in `templates/Pattern_Judgement_Check.md`,
   or split a `Puzzles.md` out of `Mystery.md`. The current state is a content type the
   template rules on and the library does not name.

6. **Every Constraints section is empty after a full build.** They fill "only from observed
   generation failures", a build has now happened, and the Setting check below records
   several. At minimum: `dangerous/Dressing.md` should carry a constraint about carrying a
   region-wide architectural motif into individual entries; all three `Naming.md` files
   should carry one about the write-back to `setting/Language.md`; `dangerous/Treasure.md`
   should carry one about a region's stated table lean actually being cited by its rooms.
