# Plans

Live working notes for architectural changes under discussion but not yet built. Unlike
`STEPS.md` (a record of what *was* done), this file is a record of what we've *decided to
build and why*, kept in one place because these four plans touch each other - a decision
made executing one changes an assumption in another, and this file is where that gets
caught and updated in the same pass rather than discovered later as drift.

Each plan below is independent enough to execute on its own, but references the others
where they share a mechanism. When executing a plan surfaces a change to another plan's
assumptions, **update that plan's section immediately, in the same pass** - this file is
only useful if it stays current.

## Cross-cutting decisions

Ground rules every plan below has to honor. These came out of specific concerns raised
before any of this was built, and they're binding on all four plans, not just the one that
prompted each.

### Pre-assignment sits under the probability layer, never replaces it

Every class file's Spec (`dangerous/High.md`, `wild/Landmark.md`, etc.) decides **whether**
and **how many** - `1` mandatory, a percentage a roll - and that machinery is untouched by
anything in this file. Where a plan below talks about pre-assigning a specific creature,
faction, or named entry to a location, it means exactly this: *if and when* the class
file's own roll at 4c lands on that category, a region-wide pre-pass has already suggested
which specific entry to reach for, so the model isn't inventing/picking blind at the moment
of writing. It never forces a category to fire, never adds a category the Spec doesn't
already call for, and an unused suggestion (the roll went to trap instead) simply isn't
spent - Bestiary/Faction entries are reusable by design, so nothing is wasted.

### Kind and Tag are two different axes, not one

- **Kind** selects the machine: which pattern file's inclusion spec governs this location.
  Small, closed, load-bearing set (3-5 per rating). Adding a Kind means adding a new file
  with its own Spec block - a structural change, same weight as adding `safe/Wealth.md` was.
- **Tag** colors what the machine produced: a flavor/index layer on the finished location,
  read by the referee for a quick handle and (once `setting/Tags.md` exists) drawn from a
  described, closed pool. Tags never gate which Spec runs and never carry their own
  percentage/inclusion math.

Never fold one into the other. A tag bank entry that starts effectively selecting behavior
has become a Kind and should be named one.

### A Kind's function is genre-neutral; its name and flavor are genre-derived, from Tags

Refines the rule above rather than relaxing it. Checked against the actual Spec content:
SAFE's Commerce/Authority/Social/People/Wealth and WILD's Ruin/Lair/NaturalFeature are
already **functions** under the hood (trade, governance, dwelling, storage; built-and-
abandoned, inhabited-by-something, environmental) - every mandatory/percentage line in
their Specs works identically for a fantasy tower, a derelict ship, or a quarantine ward.
What isn't genre-neutral is the English word chosen for each ("Ruin," "Lair") and the
illustrative Patterns-section prose under it - and that prose is already this framework's
own stated convention for "an illustration to be varied from," not binding spec.

So: **a Kind's Spec math (what it guarantees, mandatory/percentage lines) is written once,
genre-neutral, and never changes per setting. A Kind's display name and descriptive flavor
are genre-derived, sourced from `setting/Tags.md`'s Hazard/Room-Type facet (Plan 1), and
get filled in at generation time - never hard-coded into the pattern file as a fantasy
noun.** This is the same principle `patterns/setting/Genre.md` already states for the
Mythic Underworld itself ("a post-apocalyptic reference's underworld may be a buried
machine... the *function* is the constant across references; its dressing is not") -
Plan 1 and Plan 3 are threading a principle the framework already committed to at the
genre level down into Kind labeling, where it was never actually carried before.

This does not move Tag into Kind's job: Tag still never decides which Spec file governs a
location. It supplies the vocabulary Kind's *label* borrows once that decision is made.

### Weight leads for DANGEROUS; Kind composes under it, not beside it

DANGEROUS is the one rating mapping room-by-room, so weight (High/Medium/Low) is the
signal that keeps a room players spend an hour on legible against a room that's
deliberately unclear whether it's empty. That primacy doesn't move. SAFE and WILD don't
carry the same constraint - SAFE's low end is the referee narrating procedurally, not a
written room; SAFE and WILD's high end is closer to the Region Overview itself - which is
why they don't need (and shouldn't get) the same weight-first structure.

Any Kind axis added to DANGEROUS (Plan 3) attaches the same way WILD's Kind already works
*inside* `wild/Landmark.md` - a KIND block nested under the class file's own top-level
spec, supplying additional guaranteed/percentage lines, never a second axis competing with
weight for which file governs the room's budget.

---

## Plan 1 - `setting/Tags.md`: a closed, described, genre-derived tag pool

**Problem.** Location stub tags (the "*three, thematic, tags*" on every gazetteer entry)
are currently invented fresh per location with no fixed pool, no description, and no
tracking - confirmed against real output (`setting/region/B/Locations.md`): tags like
*Ancient, Crossing, Exposed* barely overlap `GENRE.md`'s own Safe/Wild/Dangerous tag bank.
GENRE.md's Tags section is read wholesale at nearly every step but is only actually
consumed by name in one place (the Bestiary citation's demeanor tag) - paid for everywhere,
used almost nowhere.

Separately, but discovered while scoping this plan: `patterns/setting/Genre.md` already
requires its own tag bank to be genre-derived ("draw every tag from the chosen reference's
own concrete iconography first"), and already states that a Mythic Underworld's *function*
is genre-constant while its *dressing* is not (a post-apoc reference's underworld is a
buried machine, not a dungeon). Neither principle currently reaches past GENRE.md - the
Kind labels in `wild/Landmark.md` (Ruin/Lair/NaturalFeature) and any new DANGEROUS Kind
(Plan 3) are still fixed English dungeon nouns regardless of which reference GENRE.md
names. A setting built from a modern-horror, gritty-sci-fi, or post-apocalyptic reference
would inherit "pit traps and throne rooms" it has no business generating. This plan is
where that gets fixed, since it's the plan already building a genre-facing described pool.

**Mechanic.**
- New setting-level artifact, `setting/Tags.md`, generated once, early - right after
  GENRE.md exists (step 1a's successor, before any region exists) - by extending the same
  "draw from the chosen reference's concrete iconography first" rule `patterns/setting/
  Genre.md` already uses for its own tag bank. Tailored, not seeded-generic: unlike
  `Procedures.md`/`Language.md`, there's no genre-neutral default worth seeding, since the
  whole point is that its content is derived from GENRE.md's specific chosen reference.
- **At least two facets per rating**, not decided beyond that count:
  - **Thematic** - the existing color/flavor axis, larger and described (per the prior
    discussion, "keeping at least one axis of tags that way still makes sense" -
    preserved, not replaced).
  - **Hazard/Room-Type** - new. What kinds of dangers and room-functions exist *in this
    specific genre* - for a modern-horror reference: Quarantine Ward, Contaminated,
    Surveillance, Ritual Site, Feral; for post-apocalyptic: Radiation Pocket, Scavenged,
    Collapsed, Cache, Territorial Marker; for gritty sci-fi: Vacuum Breach, Malfunctioning,
    Airlock, Cargo Hold, Server Core. This facet is what reinforces genre at the structural
    level, not just the descriptive one, and is what Plan 3's Kind naming draws from (see
    the cross-cutting decision on function vs. flavor above).
  - Cross-categorized within each facet, not flat, so combination space (not list length)
    buys variety per the token-cost analysis - a location's tags draw one per facet.
- Each tag carries a one-line gloss, short and specific, never decorative.
- **Read once per region, at 4a** (low cardinality) when gazetteer stubs are minted. The
  drawn tags' glosses get copied straight into the stub. **4c never opens `Tags.md`** -
  everything it needs is already sitting in its own stub, matching `Location.md`'s existing
  narrow-context design. Marginal cost at the highest-cardinality step: zero.

**Integration.**
- This *is* the mechanism for what was called "seed a hook at stub time" in the prior
  discussion - no separate system needed, minting a stub's tags from this pool is the hook.
- Feeds Plan 3 directly: a Kind's Spec math stays genre-neutral and fixed; its display name
  and flavor text are pulled from this plan's Hazard/Room-Type facet at generation time.
  Plan 3 cannot be genre-portable without this plan existing first.
- Feeds Plan 4's pre-assignment pass: a location's tag glosses are cheap, already-resolved
  material a region-wide pass can lean on when distributing creature/faction preferences
  (a location tagged *Denning* is an obvious creature-slot candidate; a pass shouldn't
  ignore what's already been decided at 4a).
- Does **not** replace Kind (see cross-cutting decisions above). A tag can describe a
  DANGEROUS room's texture, or supply a Kind's genre-flavored name; it never itself
  determines which pattern file governs a location's contents.

**Separate, smaller, related task - not part of this plan but blocking a real test of it.**
`patterns/setting/Genre.md`'s 20-30-reference seed pool is currently 100% fantasy (Howard,
Erikson, Mörk Borg, etc.) despite the mechanism explicitly supporting a freehand
non-fantasy reference. Nobody has run a horror/sci-fi/post-apoc setting through this
framework yet, so this plan's genre-portability claims are untested against real output.
Worth broadening the seed pool (add real references - SCP Foundation, Jeff VanderMeer's
Southern Reach, Alien, Mothership, Delta Green, The Last of Us, Fallout - as their own
corners in Round 1) before or alongside building `Tags.md`, so there's an actual non-fantasy
setting to generate and check this against. Cheap (it's additive entries in one list), but
tracked separately since it's a `patterns/setting/Genre.md` change, not a Tags.md one.

**Open questions.**
- Exact facet list and count per rating (Thematic + Hazard/Room-Type is the floor, not
  necessarily the ceiling).
- Whether GENRE.md's existing Safe/Wild/Dangerous bank gets absorbed into `Tags.md` and
  removed from GENRE.md, or GENRE.md keeps a small fixed subset and `Tags.md` is additive.
  Leaning toward absorption - GENRE.md paying for an unused bank at every step is exactly
  the token-cost problem this plan is fixing; leaving a duplicate copy behind reopens it.
- How reuse/exhaustion is tracked across a large region (60+ locations pulling from one
  region's Tags.md) - simple round-robin, or explicit "spent" tracking on `Regions.md`.
- Whether Hazard/Room-Type tags, once assigned to a stub, are binding on 4c (this location
  *will* reflect Contaminated) or advisory like Plan 4's pre-assignments (a preference the
  class file's own roll may or may not land on). Leaning advisory, for the same reason
  Plan 4 stays advisory - the probability layer is cross-cutting and shouldn't be overridden
  twice by two different plans.

**Status.** Proof-of-concept built: `tags_fantasy.md` (Robert E. Howard/Conan, reusing this
repo's own `GENRE.md` reference as a control), `tags_scifi.md` (Mothership 1e), and
`tags_apoc.md` (Fallout) - three full tag pools in the shape this plan proposes (Thematic +
Hazard/Room-Type per rating, plus People/Creatures), ~95-98 tags each, built before touching
any generation mechanism, specifically to test whether the facet structure produces
genre-distinct vocabulary or just reskinned fantasy.

Checked by diffing tag names across all three files: **1-4 overlapping tags per pair out of
~95-98 each, and every overlap is a universal behavioral primitive** (Territorial, Frenzied,
Calculating, Silent, Superstitious - legitimately cross-genre creature/personality traits).
Zero overlap in either Thematic or Hazard/Room-Type facets specifically - no fantasy
institution or room-type leaked into the sci-fi or post-apoc pools. This is the result the
plan needed to see before building the real mechanism: the structure holds a genre's own
vocabulary rather than producing generic fill-in-the-blank output.

Not yet done: wiring these into an actual generation step (they're standalone target files
at repo root, not `setting/Tags.md` outputs produced by a template/pattern), the seed-pool
broadening noted above (Mothership and Fallout were hand-picked for this test, not run
through the actual Round 1-3 narrowing flow), and the open questions below.

---

## Plan 2 - Region-level field review (Overview vs. gazetteer stub)

**Problem.** `templates/Region.md`'s fields haven't been reassessed since the five-folder
pattern migration. Real output (`setting/region/A.md`) is already reasonably specific
(names "Border Raider," "Garrison Deserter," the quartermaster) but that reads as
generation instinct, not a stated rule - nothing in `patterns/region/*.md` currently
requires committing named, specific material at 3c the way this plan would formalize.
There's also a live question of what belongs at the Overview level (shared, read by every
location in the region) versus the gazetteer stub level (committed once, per location, at
4a) - Plan 1 already answers this for tags specifically; this plan is the general pass.

**Mechanic.**
- Read `templates/Region.md`, all three `patterns/region/*.md` files, and several real
  Region Overviews + their `Locations.md` gazetteers side by side.
- For each field (Ambiance, Creatures, Dangers, Secrets, Treasure, Features, the
  rating-specific ones), decide: does this field currently commit *named, specific*
  material, or does it stay abstract and leave specificity to 4c? Where it's abstract,
  either tighten the pattern file's instruction to require 2-3 committed names/signs per
  field, or explicitly declare that field's specificity belongs downstream instead.
- Cross-check against `checks/SettingJudgementCheck.md`'s existing claim-auditing rule
  ("a claim made here is a promise the locations have to keep") - a field tightened to
  require named commitments raises the bar that check already enforces; make sure the two
  stay aligned rather than the check silently doing double duty.

**Integration.**
- Directly upstream of Plan 4: a Region Overview that already commits specific named
  creatures/factions is exactly the roster a region-wide pre-assignment pass draws from.
  Doing this review first makes Plan 4 easier to execute correctly.
- Shares the stub-vs-overview line with Plan 1 (tags are the one field already resolved by
  this review, in advance).

**Open questions.** None yet - this is a review pass, findings will populate this section.

**Status.** Not started.

---

## Plan 3 - Kind axes: give DANGEROUS one, widen WILD's, name all of them by function

**Problem.** "Class" currently conflates two different axes. Kind (what a location
fundamentally *is*) and Weight/Prominence (how much attention/budget it gets) are cleanly
split for SAFE (5 Kinds x 3 Prominence levels) and WILD (3 Kinds nested under Landmark x 3
classifications), but DANGEROUS only has the Weight axis (High/Medium/Low) - a room's
"kind" currently lives as free prose inside `dangerous/Dressing.md`'s Purpose field rather
than a structured, filed menu. Separately: every existing Kind name (Ruin, Lair,
Commerce, Wealth) is a genre-neutral function wearing a fantasy-flavored English label,
which is fine as long as every setting is fantasy and breaks the moment one isn't (see the
cross-cutting decision on function vs. flavor above, added after this plan's first draft
named fantasy-dungeon nouns - Crypt, Vault, Shrine, Barracks - as DANGEROUS Kind
candidates and got called on it).

**Mechanic.**
- **DANGEROUS Kind axis, named by function, not noun.** Candidates, restated abstractly:
  - **Sanctum** - built around a purpose, ritual, or authority (fantasy: shrine/throne
    room; sci-fi: command deck/bridge; horror: ritual chamber; post-apoc: command bunker).
  - **Cache** - built to store or protect something (vault/treasury; cargo hold/armory;
    evidence locker; supply cache).
  - **Habitation** - built for something to live, work, or rest (barracks/quarters; crew
    quarters; living quarters; den/shelter).
  - **Passage** - connective space that still counts as a room, not mere corridor
    (gallery/antechamber; airlock/junction; hallway/stairwell; choke point).
  Each gets a KIND block nested under each weight file (`High.md`/`Medium.md`/`Low.md`),
  exactly the way `wild/Landmark.md` nests its Kinds under its own top-level spec. The
  block's Spec math (what it guarantees) is written once, genre-neutral, using the
  abstract function name (Sanctum, Cache, ...) as the file/section identifier. **The
  genre-flavored display name and descriptive vocabulary shown in the generated location
  come from Plan 1's `Tags.md` Hazard/Room-Type facet at generation time, never from the
  pattern file itself.** Per the cross-cutting decision on weight, this composes under
  weight - it supplies extra lines for "what kind of room," weight still governs the room's
  overall budget and inclusion rate.
- **WILD Kind widening**: WILD currently has only 3 Kinds under Landmark
  (Ruin/Lair/NaturalFeature - already functions: built-and-abandoned, inhabited-by-
  something, environmental). Cheap to add a 4th/5th function (candidates: a mobile/
  inhabited-but-not-a-lair Kind; a pure-Passage/crossing Kind) the same way
  `safe/Wealth.md` was added as a 5th SAFE Kind - and, per the same principle, any new
  WILD Kind's file-level name should be function-first too.
- **Retrofit note, not urgent**: WILD's and SAFE's *existing* Kind file names (Ruin, Lair,
  Commerce, Wealth...) stay as the internal/file identifiers - renaming files is unwarranted
  churn - but the generation step should treat those names as function labels internally
  and pull the genre-flavored display name from `Tags.md` the same way a new DANGEROUS Kind
  would, once Plan 1 exists. Lower priority than getting DANGEROUS's axis built correctly
  from the start, but tracked here so it isn't forgotten.
- Explicitly **not** proposing to add a 4th DANGEROUS weight tier or a 4th WILD
  classification - those are calibrated against location-count math, the Danger countdown,
  and node-role distribution rules (per the cross-cutting decision above); widening them
  means re-deriving that math, not just writing a new file.

**Integration.**
- **Depends on Plan 1** for genre-portability - this plan cannot produce a genre-true
  Kind name without `Tags.md`'s Hazard/Room-Type facet to draw from. Building Plan 3 before
  Plan 1 means hard-coding fantasy nouns again, the exact mistake this revision fixes.
- A DANGEROUS Kind, once it exists, is exactly the kind of already-resolved fact Plan 4's
  pre-assignment pass should read before suggesting a creature/faction - a Cache-kind room
  suggests a different creature than a Habitation-kind room.
- Function names (Sanctum/Cache/Habitation/Passage) are deliberately abstract enough that
  none of them should ever collapse into a Tag (per the Kind-vs-Tag delineation) - if a
  candidate Kind starts reading like a flavor descriptor rather than a content-selector
  with its own Spec math, it belongs in `Tags.md` instead, not as a new Kind file.

**Open questions.**
- Final DANGEROUS Kind list and their Spec math - the four functions above are a starting
  shape, not a decided spec; needs the same "what does each guarantee" work every existing
  class file went through.
- Whether every weight tier needs every Kind, or some Kinds are weight-restricted (a Cache
  might only make sense at Medium/High, never Low).
- Whether the WILD/SAFE retrofit (function-first naming pulled from Tags.md) happens as
  part of this plan or is spun into its own smaller follow-on once Plan 1 ships.

**Status.** Not started.

---

## Plan 4 - Region-wide pre-assignment pass (which, not whether)

**Problem.** DANGEROUS node roles are already decided once at 4b, region-wide, with the
whole graph visible, and 4c "reads the assignment rather than inventing it" (`STEPS.md`
4b). Nothing else works that way: which *specific* Bestiary entry, Faction, or Named
Creature fills a location's creature/faction-involvement line is left to that location's
own 4c pass, decided blind to what every sibling location in the region already chose,
under a 15-/8-12-word Feature budget. Independent, budget-pressured, blind-to-siblings
decisions are exactly the conditions that produce convergent, samey choices.

**Mechanic** (see the cross-cutting decision above - this never touches the probability
layer, only pre-stocks it):
- New pass at 4b (or a 4b.5), region-wide, after node roles are assigned and before 4c
  starts writing. Walk the region's gazetteer stubs and, for every location whose class
  file's Spec includes a citation-bearing line (Creature, Faction, Named Creature - **not**
  Dressing/Ambiance, which stay freshly invented per room by design), attach a non-binding
  suggestion: *if this location's roll lands on that category, prefer this specific,
  already-established entry.*
- The pass's job is explicitly to **distribute across the region's existing roster**
  (Bestiary entries, the 3 Factions, already-coined Named Creatures) rather than
  independently gravitate to the same 1-2 memorable entries - round-robin or
  usage-weighted, not random per location.
- Implementation is one added line per relevant stub, e.g. `A.3: Creature = Steppe Wolf`,
  not a new file.
- At 4c, the class file's own Spec still runs unchanged - if it rolls a creature, check the
  stub's suggestion first; if it rolls trap/mystery instead, the suggestion goes unused and
  remains available for another location.

**Integration.**
- Depends on Plan 2 (a Region Overview that already commits specific names gives this pass
  real material to distribute) and benefits from Plan 3 (a location's Kind, once it exists
  for DANGEROUS, narrows which roster entries actually make sense there).
- Shares mechanism with Plan 1's tag-gloss copy-into-stub step - both are "resolve once,
  region-wide, cheaply; consume for free at 4c."

**Open questions.**
- Exact file/field the suggestion lives in - a new column on `Locations.md`, or a sidecar
  file per region.
- Whether Faction-involvement suggestions need the same "not overused" distribution
  guarantee that node roles already have for LOW locations (60%+ non-default), or whether
  3 factions is small enough that simple round-robin suffices.

**Status.** Not started.
