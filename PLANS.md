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

## Decision: System B - compile genre into the pattern files, not a runtime lookup

Supersedes Plan 1's and Plan 3's original design (Tags.md as a rich structural vocabulary
- Institution/Condition, Agent/Threat, Site-Type - joined against generic pattern files at
generation time). That design was built and tested (`tags_fantasy.md`, `tags_scifi.md`,
`tags_apoc.md`, `vertical_slice_locations.md` - since removed once the decision below was
made; git history holds them if this record needs to be checked against the actual files
again) and worked, but on review the better direction is the opposite one:

**Tags stay pure theme-director/seed material - a flat, genre-derived pool with no
structural role at all.** The actual genre-specific content (what a trap looks like here,
what kind of place a Ruin is, what a creature's demeanor sounds like) gets written
*directly into the tier-2 pattern files themselves*, once, right after `GENRE.md` exists -
a compile step, not a per-generation join.

**Why, explicitly:** the cons identified for this approach during design (bigger up-front
cost, patterns/ forking away from generic shared infrastructure per build) are being taken
as the argument *for* it, not against it. The site-type/hazard-type tag content built for
the rejected design is the proof: that was the point where the tag pool stopped reading as
decorative and started reading as real setting material, and pushing that same effort into
the pattern files themselves - rather than a lookup table the model has to successfully
join at generation time - is what makes generation read as **situations, not stories**:
procedural output built from a stocked, genre-true parts bin, rather than a lookup table
that has to be re-translated correctly every single time it's consulted. The lookup-join
design is judged to carry more risk of reading like a story-game's recurring, hand-authored
tropes (the same abstract gloss re-interpreted differently each time) than like this
framework's own procedural, non-narrative generation model.

**Scope narrowed:** cross-genre portability (fantasy/sci-fi/post-apoc swapping) is out of
scope for now. `GENRE.md` generation narrows to OSR/fantasy references only - the
contract/example split still earns its keep entirely within that scope, since it's what
lets the pattern files' *examples* vary by chosen reference (Howard/Conan vs. Mörk Borg vs.
Dolmenwood, all "OSR fantasy," very different concrete iconography), not just across
genres.

**The six-point execution plan**, as given, with the file-level specifics decided where the
original phrasing left them open (flagged inline so they're easy to correct):

1. **New step, right after 1a**: generate `setting/Tags.md` - ~25 genre-level thematic
   tags, each with a one-line gloss, drawn from `GENRE.md`'s chosen reference. Flat, not
   split by rating - rating-specific structural content is now the compiled pattern files'
   job, not the tag pool's.
2. **Remove the 3 embedded tags from `Setting.md` and each Region Overview.** Each becomes
   a single tag-line pointing at the relevant `Tags.md` pool rather than inline-authored
   adjectives.
3. **Each region gets its own `Tags.md`** - 25 more tags, same shape as the setting-level
   pool, generated alongside its Region Overview. *File-path decision, flagged*: placed at
   `setting/region/[Code]/Tags.md`, which means a region's folder now gets created at
   step 3 (when its Overview and Tags.md are written) rather than first appearing at 4a -
   4a then just adds `Locations.md` into an already-existing folder.
4. **Each location gazetteer pulls one tag from setting, one from region** - two tags
   total, not three. *Interpretation decision, flagged*: this replaces the location
   header's three freely-invented tags outright (`templates/Location.md`'s
   `*[three, thematic, tags]*` becomes two, deterministically pulled, not
   locally-invented) - the location's own flavor now comes from the compiled pattern
   file's examples, not a third freely-invented tag.
5. **Separate contract from examples in every tier-2 pattern file** - the element files a
   class file's Spec cites in parentheses, not the class files themselves and not the
   unconditional Dressing/Secrets/Naming companions (scoped this narrowly on purpose; see
   Plan 1B below for the exact file list). Each gets an explicit CONTRACT (what it decides,
   genre-neutral, permanent) separated from EXAMPLES (illustrative, meant to be
   genre-compiled per build).
6. **Demeanor becomes `dangerous/Creature.md` and `wild/Creature.md`'s examples;
   personality becomes `safe/People.md` and `wild/Creature.md`'s own People pattern's
   examples.** Replaces `GENRE.md`'s old People/Creatures tag categories outright, which
   get removed as redundant once this exists.

See **Plan 1B** below for the concrete file-by-file breakdown. Plan 2 (region-level field
review) is unaffected by this pivot. Plan 4 (pre-assignment pass) loses its dependency on
an Agent/Threat tag facet, since that facet no longer exists - it reverts closer to its
original, Tags-independent conception (pre-assign a specific Bestiary/Faction entry
straight from the region's own established roster) and is noted as such in its own
section.

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
are genre-derived, sourced from `setting/Tags.md`'s Site-Type facet (Plan 1), and
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

Any Kind axis added to DANGEROUS attaches the same way WILD's Kind already works *inside*
`wild/Landmark.md` - a KIND block nested under the class file's own top-level spec,
supplying additional guaranteed/percentage lines, never a second axis competing with
weight for which file governs the room's budget. Currently inert: Plan 3 reviewed adding
one and resolved without it (`dangerous/Dressing.md`'s existing Purpose field covers the
room-kind-variety problem this would have solved) - this rule stays as the constraint to
honour if a DANGEROUS Kind axis is ever proposed again, not a description of one that
exists.

---

## Plan 1 - SUPERSEDED by System B, see the Decision section above

Kept in full below as the historical record of the design that was built, tested, and
then deliberately rejected in favor of compiling genre content into the pattern files
instead of joining a lookup table at generation time. `tags_fantasy.md`,
`tags_scifi.md`, `tags_apoc.md`, and `vertical_slice_locations.md` served as the evidence
for that decision and have since been removed from the repo as no longer needed - this
section, and the Decision section above, are the durable record of what they showed.
**Plan 1B, after Plan 4 below, is the current plan for the tag mechanism.**

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
- **Three facets per rating**, revised up from two after auditing the proof-of-concept
  content itself and finding the original "Thematic" facet was secretly doing two
  different jobs (evidence: fantasy DANGEROUS's own Thematic list mixed *Elder Sorcery* -
  an institutional/historical fact - with *Serpent Cult* - an active present threat -
  under one label):
  - **Institution/Condition** - what social, political, or organizational fact is
    standing here (governance, custom, debt, history). Larger and described, the
    surviving half of the original "Thematic" axis.
  - **Agent/Threat** - new. Who or what actively opposes or endangers here - a flavor of
    danger, never a specific Bestiary/Faction assignment (that stays Plan 4's job). The
    other half of the original "Thematic" axis, split out because an institution and an
    active threat are different kinds of fact even when both read as "flavor."
  - **Site-Type** - what physical place or space this is. Renamed from "Hazard/Room-Type"
    on the same audit: WILD's own entries (a Ford, a Denning Ground) were never literally
    rooms, so the label shouldn't imply one. What reinforces genre at the structural
    level, not just the descriptive one, and what Plan 3's Kind naming draws from (see
    the cross-cutting decision on function vs. flavor above).
  - Cross-categorized within each facet, not flat, so combination space (not list length)
    buys variety per the token-cost analysis - a location's tags draw one per facet.
  - Considered and rejected: a fourth Naming/Vocabulary facet (`Language.md` already owns
    this - would duplicate an existing living artifact) and a fourth Sensory/Ambiance
    facet (unclear it's distinct from Site-Type rather than the same content restated;
    holding off until the 3-facet version has been run for real).
- Each tag carries a one-line gloss, short and specific, never decorative.
- **Read once per region, at 4a** (low cardinality) when gazetteer stubs are minted. The
  drawn tags' glosses get copied straight into the stub. **4c never opens `Tags.md`** -
  everything it needs is already sitting in its own stub, matching `Location.md`'s existing
  narrow-context design. Marginal cost at the highest-cardinality step: zero.

**Integration.**
- This *is* the mechanism for what was called "seed a hook at stub time" in the prior
  discussion - no separate system needed, minting a stub's tags from this pool is the hook.
- Feeds Plan 3 directly: a Kind's Spec math stays genre-neutral and fixed; its display name
  and flavor text are pulled from this plan's Site-Type facet at generation time.
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
- Exact facet list and count per rating (Institution/Condition + Agent/Threat + Site-Type
  is the current floor, not necessarily the ceiling - Sensory/Ambiance stays a candidate).
- Whether GENRE.md's existing Safe/Wild/Dangerous bank gets absorbed into `Tags.md` and
  removed from GENRE.md, or GENRE.md keeps a small fixed subset and `Tags.md` is additive.
  Leaning toward absorption - GENRE.md paying for an unused bank at every step is exactly
  the token-cost problem this plan is fixing; leaving a duplicate copy behind reopens it.
- How reuse/exhaustion is tracked across a large region (60+ locations pulling from one
  region's Tags.md) - simple round-robin, or explicit "spent" tracking on `Regions.md`.
- Whether Site-Type (and now Agent/Threat) tags, once assigned to a stub, are binding on
  4c (this location *will* reflect this Agent/Threat tag) or advisory like Plan 4's
  pre-assignments (a preference the class file's own roll may or may not land on).
  Leaning advisory, for the same reason Plan 4 stays advisory - the probability layer is
  cross-cutting and shouldn't be overridden twice by two different plans. This question
  sharpens now that Agent/Threat exists as its own facet: an Agent/Threat tag reads a lot
  like a preview of a Plan 4 pre-assignment, and the boundary between "a tag suggesting a
  flavor of danger" and "a pre-assignment naming a specific Bestiary/Faction entry" needs
  to stay clean when both plans are built.

**Status.** Proof-of-concept built and then revised once, in the same pass, after an
honest audit of the first draft's own content: `tags_fantasy.md` (Robert E. Howard/Conan,
reusing this repo's own `GENRE.md` reference as a control), `tags_scifi.md` (Mothership
1e), and `tags_apoc.md` (Fallout) - three full tag pools, now in the three-facet shape
above, ~121-125 tags each.

The first draft (two facets - Thematic + Hazard/Room-Type) passed the cross-genre overlap
check, but auditing its own content before moving on found "Thematic" was quietly doing
two jobs (see the Mechanic section above) and "Room-Type" was mislabeled for WILD. Revised
in place rather than treated as done. Re-checked after the revision: diffing tag names
across all three files, **1-4 overlapping tags per pair out of ~121-125 each, every
overlap a universal behavioral primitive** (Territorial, Frenzied, Calculating, Silent,
Superstitious), same result as the first draft - **zero overlap in Institution/Condition,
Agent/Threat, or Site-Type specifically**, so splitting the facet didn't reintroduce
mushiness. This is the result the plan needed to see before building the real mechanism:
the structure holds a genre's own vocabulary rather than producing generic fill-in-the-blank
output, at three facets as well as two.

Not done before the System B pivot superseded this plan: wiring these into an actual
generation step (they were standalone target files at repo root, not `setting/Tags.md`
outputs produced by a template/pattern), the seed-pool broadening noted above (Mothership
and Fallout were hand-picked for this test, not run through the actual Round 1-3 narrowing
flow), and the open questions below.

**Vertical slice built:** `vertical_slice_locations.md` (since removed, see the note at
the end of this Status section) - one SAFE, one WILD, one
DANGEROUS location per genre (nine total), hand-drawing one tag per facet per location and
writing the full entry against the real `templates/Location.md` + class pattern files
(`safe/Settlement.md`+`Commerce.md`, `wild/Landmark.md`+`Ruin.md`,
`dangerous/High.md`), in clean-room isolation from the real Carrdun setting (no Region
Overview, Bestiary, or People roster - see that file's own Method section for exactly what
was skipped and why). Result: all three facets did real structural work in every one of
the nine (Institution/Condition shaped organizational history, Agent/Threat became the
actual mechanical challenge, Site-Type was the room), genre register held with no bleed
between the three sets, and re-reading the finished prose confirms the tag-name overlap
check's result at the prose level, not just the vocabulary-list level.

One finding that changes Plan 4: **Agent/Threat doesn't map 1:1 onto the Creature slot.**
Apoc DANGEROUS's *Automated Defense Grid* tag resolved as a **trap** (using
`dangerous/Trap.md`'s tell format), not a creature. Plan 4's pre-assignment pass can't
assume an Agent/Threat tag always feeds a Bestiary/creature pre-assignment - it has to stay
agnostic across creature/trap/mystery the same way the class file's own Challenge line is,
and resolve only once 4c's roll lands on a category.

Two real spec misses were left uncorrected on purpose, as data rather than embarrassment:
`wild/Dressing.md`'s Position line (a bearing from the entry or another Landmark) got
conflated with the Size line in two of the three WILD entries; `safe/Commerce.md`'s "where
it sends them instead" clause was only half-satisfied in two of the three SAFE entries.
Both are the kind of miss `tools/validate_setting.py` or `checks/SettingJudgementCheck.md`
should be positioned to catch in real generation, not something to quietly patch after the
fact in a prototype.

`tags_fantasy.md`, `tags_scifi.md`, `tags_apoc.md`, and `vertical_slice_locations.md` have
since been removed from the repo now that System B (Plan 1B) is the live plan - this
Status section and the findings above are what they were kept around long enough to
produce, not a description of files still present.

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

**Open questions.**
- **SAFE's tier-1 wrapper, raised reviewing Plan 3.** `safe/Settlement.md` is SAFE's only
  class file - unlike WILD's 3 and DANGEROUS's 3 - and inside it, SETTLEMENT TYPE
  (steading/thorp/village/town/seat) and PROMINENCE (liner note/working/central) both sit
  above Kind (Commerce/Authority/Social/People/Wealth), which is nested a level deeper
  still. Decide whether that wrapper stays as-is (Prominence leads, Kind composes under
  it - already the pattern, and already consistent with the cross-cutting decision that
  DANGEROUS's weight leads the same way) or whether Kind should be promoted out from under
  it - and if promoted, whether SETTLEMENT TYPE folds into Kind or stays a separate axis
  Kind sits beside. Settled here, not as a side effect of Plan 3, since Plan 3's scope is
  DANGEROUS and WILD only (see its Status).

**Status.** Not started.

---

## Plan 3 - Kind axes: DANGEROUS resolved without a new axis; WILD widened - EXECUTED

**Resolution (review before execution).** Reviewed against the actual DANGEROUS and WILD
pattern files before building anything, three decisions came out of that review:

1. **DANGEROUS gets no new Kind axis.** The room-type variety this plan was chasing
   already exists, unstructured, in `dangerous/Dressing.md`'s Purpose field (Keeping /
   Working / Living / Holding / Meeting / Believing / Dying / Moving, with its own "do not
   reuse a purpose already used in this region" rule). A second mechanical axis alongside
   Weight - Spec math per Kind, gated per weight tier - was judged more structure than the
   problem needs; Purpose already answers "what kind of room" without competing with
   Weight for which file governs the room's budget. **What DANGEROUS actually lacks isn't
   room-kind variety, it's locations that function as a group** - the way a WILD Landmark
   and its Hidden/Secret children read as one place. DANGEROUS's dense, node-role graph
   (`patterns/region/Dangerous.md`) doesn't have an obvious equivalent to
   parent-and-children, so multi-location functional blocks are a real, separate design
   problem - tracked below as an open item, not attempted in this pass.
2. **WILD widening executed.** Added one new Kind, **Crossing**, to `wild/Landmark.md`'s
   Kind line and KIND blocks, with its own `wild/Crossing.md` content file (Decides / Read
   at / Examples / Constraints, matching `Ruin.md`/`Lair.md`/`NaturalFeature.md`'s shape
   exactly) and wired into the step-1b compile list in `STEPS.md`. Function: a Landmark
   defined by what it costs to go around, not by who built or lives there - built, natural,
   or held, chosen when the region's own shape forces the party through a specific point
   rather than around it.
   - The plan's other candidate, a mobile/inhabited-but-not-a-lair Kind, was considered and
     **rejected on review**: `wild/Lair.md`'s own Examples already cover this ground
     directly ("a camp of somebody who moves seasonally" under Kinds of holding; "a hunting
     camp... a work party too far out to return nightly" under Occupied by people), and a
     separate Kind built on the same ground risked being a flavor fork of Lair rather than
     a genuinely distinct function-with-its-own-Spec-math - the exact failure mode the
     Kind-vs-Tag cross-cutting decision warns against. Not added; revisit only if real
     generation shows Lair's "why it stays / territory" contract genuinely doesn't fit a
     transient occupant.
   - Not a 4th WILD *classification* (Landmark/Hidden/Secret stays 3) - this is a 4th Kind
     nested under Landmark, same tier as Ruin/Lair/NaturalFeature, no change to
     `patterns/region/Wild.md`'s counts or topology.
3. **The WILD/SAFE retrofit note (pulling existing Kind display names from a Tags.md
   facet) is now moot**, not just deprioritized - per the System B decision, genre flavor
   for every tier-2 file comes from its own compiled EXAMPLES block (step 1b), not a
   generation-time Tags.md lookup. `wild/Ruin.md`/`Lair.md`/`NaturalFeature.md` already work
   this way; `Crossing.md` was built the same way from the start, so there is no retrofit
   left to do.

**Problem (historical).** "Class" conflated two different axes. Kind (what a location
fundamentally *is*) and Weight/Prominence (how much attention/budget it gets) are cleanly
split for SAFE (5 Kinds x 3 Prominence levels) and WILD (now 4 Kinds nested under Landmark
x 3 classifications), but DANGEROUS only has the Weight axis - resolved above as
intentional, not a gap, given Purpose already does this job.

**Integration.**
- DANGEROUS's Purpose field (`dangerous/Dressing.md`) remains what Plan 4's pre-assignment
  pass and Plan 2's region-field review should read for "what kind of room" signal - see
  Plan 4's Integration section, corrected to match.
- `wild/Crossing.md` follows Plan 1B's compile mechanism exactly like its three siblings -
  no dependency on Plan 1's superseded Tags.md Site-Type facet.

**Open questions.**
- **DANGEROUS multi-location blocks** (item 1 above) - a real, separate problem: whether
  and how a set of DANGEROUS rooms can read as one functional unit the way a WILD Landmark
  and its children do, given the region's graph is a dense node-role web rather than a
  forest of trees. Needs its own design pass before any DANGEROUS structural change is
  attempted again - not scoped further here.
- Whether `wild/Crossing.md`'s Examples produce content genuinely distinct from
  `wild/Ruin.md`'s own "Passage" subheading (bridges, fords, causeways already appear
  there too) once run against a real region - the two are meant to answer different
  questions (history vs. present-tense cost of the route) but that needs checking against
  generated output, not just the pattern text.

**Status.** DANGEROUS portion resolved without new files (see Resolution above). WILD
portion executed: `patterns/wild/Landmark.md` updated, `patterns/wild/Crossing.md` created,
`STEPS.md` step 1b's compile list updated. Not yet run against a real region.

---

## Plan 4 - Region-wide pre-assignment pass (which, not whether)

**Note (post System-B decision):** unaffected in mechanic, but its dependency below on
"Plan 1's tag-gloss copy-into-stub step" is stale now that Plan 1 is superseded and tags
carry no structural content - this plan now draws straight from the region's own
established Bestiary/Faction/Named-Creature roster (per Plan 2), not from any tag. Simpler
than before, not blocked by anything in Plan 1B.

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
  real material to distribute) and benefits from `dangerous/Dressing.md`'s existing Purpose
  field (storeroom vs. audience chamber narrows which roster entries make sense there) -
  corrected from an earlier draft that expected this from a DANGEROUS Kind axis; Plan 3
  resolved without adding one (see its Status), so Purpose is the only "what kind of room"
  signal this pass has to read, not a substitute waiting to arrive.
- Shares its "resolve once, region-wide, cheaply; consume for free at 4c" shape with
  Plan 1B's per-build compile step, but the two are independent mechanisms now - one
  pre-assigns specific registry entries per location, the other compiles genre-general
  examples into the pattern files themselves.

**Open questions.**
- Exact file/field the suggestion lives in - a new column on `Locations.md`, or a sidecar
  file per region.
- Whether Faction-involvement suggestions need the same "not overused" distribution
  guarantee that node roles already have for LOW locations (60%+ non-default), or whether
  3 factions is small enough that simple round-robin suffices.

**Status.** Not started.

---

## Plan 1B - Compile genre content into the tier-2 pattern files (current tag-mechanism plan)

**Problem.** Superseding Plan 1's design (see the Decision section at the top of this
file for the full rationale). Summary: a lookup-table join at generation time is a live
risk (the model may not translate a generic example into the setting's own genre under
word-budget pressure) and produces no durable, setting-wide consistency (every location
independently re-translates the same generic category). Compiling genre-specific content
directly into the pattern files, once, removes both problems at the cost of `patterns/`
no longer staying generic shared infrastructure across builds - accepted deliberately,
not as an oversight.

**Mechanic.**
- `setting/Tags.md`: ~25 flat, genre-derived thematic tags with one-line glosses,
  generated in a new step right after 1a. Pure seed/color, no structural role, not split
  by rating.
- `setting/region/[Code]/Tags.md`: 25 more, same shape, generated alongside each Region
  Overview (moves that region's folder creation up from 4a to step 3).
- `setting/Setting.md` and each Region Overview drop their 3 embedded, freely-invented
  tags in favor of a single tag-line pointing at the relevant `Tags.md`.
- A location's gazetteer stub carries exactly two tags - one pulled from `setting/Tags.md`,
  one from its region's `Tags.md` - replacing the old three freely-invented ones outright.
- Every tier-2 element file (the ones a class file's Spec cites in parentheses - not the
  class files themselves, not the unconditional Dressing/Secrets/Naming companions) gets
  restructured with an explicit CONTRACT section (what it decides, genre-neutral,
  permanent) separated from an EXAMPLES section (illustrative, swapped per build):
  - SAFE: `Commerce.md`, `Authority.md`, `Social.md`, `People.md`, `Wealth.md`,
    `Situation.md`
  - WILD: `Ruin.md`, `Lair.md`, `NaturalFeature.md`, `Creature.md`, `Trap.md`,
    `Treasure.md`, `Mystery.md`
  - DANGEROUS: `Creature.md`, `Trap.md`, `Treasure.md`, `Mystery.md`
- Demeanor examples compiled into `dangerous/Creature.md` and `wild/Creature.md`;
  personality examples compiled into `safe/People.md` and `wild/Creature.md`'s own People
  pattern - replacing `GENRE.md`'s old People/Creatures tag categories, which are removed
  as redundant.
- `GENRE.md`'s Safe/Wild/Dangerous/People/Creatures tag bank is removed outright - fully
  absorbed by the new `Tags.md` pools and the compiled pattern-file examples.
- Scope narrowed to OSR/fantasy: the seed-pool-broadening task from the superseded Plan 1
  is dropped, not carried forward.

**Integration.**
- Plan 2 (region field review) still applies and is now slightly sharper: a Region
  Overview that commits specific names is exactly the material the region's own `Tags.md`
  and Plan 4's pre-assignment pass should stay consistent with.
- Plan 3 depends on this plan for any new Kind's genre-true naming (see Plan 3's note).
- Plan 4 no longer depends on this plan at all (see Plan 4's note) - it draws straight
  from the registries.

**Open questions.**
- Whether the compile step is a single step (1b) that touches every tier-2 file for every
  rating at once, or split per-rating and deferred until a rating is first used at 3c/4c.
  Leaning toward all-at-once for simplicity, revisit if it proves too large a single step.
- Whether `dangerous/Trap.md`'s existing interleaved design guidance (e.g. "a trap needing
  a machinist has a machinist somewhere") survives the CONTRACT/EXAMPLES split intact, or
  needs rewording once separated from its examples.
- File-path and folder-timing decisions for region-level `Tags.md` (see the Decision
  section above) - flagged as an interpretation, not confirmed with a fresh pair of eyes.

**Status.** Executing now.
