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

## Plan 1 - `setting/Tags.md`: a closed, described tag pool

**Problem.** Location stub tags (the "*three, thematic, tags*" on every gazetteer entry)
are currently invented fresh per location with no fixed pool, no description, and no
tracking - confirmed against real output (`setting/region/B/Locations.md`): tags like
*Ancient, Crossing, Exposed* barely overlap `GENRE.md`'s own Safe/Wild/Dangerous tag bank.
GENRE.md's Tags section is read wholesale at nearly every step but is only actually
consumed by name in one place (the Bestiary citation's demeanor tag) - paid for everywhere,
used almost nowhere.

**Mechanic.**
- New setting-level artifact, `setting/Tags.md`, seeded generic alongside the framework
  seeds (`Procedures.md`, `Language.md`) and tailored per setting, same living-artifact
  treatment.
- Larger pool than GENRE.md's flat 10-per-category, and **cross-categorized rather than
  flat** - split each rating into 2-3 facets (e.g. Danger / Physical / History for
  DANGEROUS) so a location's three tags draw one from each facet. Combination space, not
  list length, is what buys variety: three 15-tag facets is ~3,000 combinations, not 45.
- Each tag carries a one-line gloss - short, mechanically or texturally specific, not
  decorative ("Submerged - half-flooded, walkable only at low water," not "watery").
- **Read once per region, at 4a** (low cardinality) when gazetteer stubs are minted. The
  three tags' glosses get copied straight into the stub. **4c never opens `Tags.md`** -
  everything it needs is already sitting in its own stub, matching `Location.md`'s existing
  narrow-context design. Marginal cost at the highest-cardinality step: zero.

**Integration.**
- This *is* the mechanism for what was called "seed a hook at stub time" in the prior
  discussion - no separate system needed, minting a stub's tags from this pool is the hook.
- Feeds Plan 4's pre-assignment pass: a location's tag glosses are cheap, already-resolved
  material a region-wide pass can lean on when distributing creature/faction preferences
  (a location tagged *Denning* is an obvious creature-slot candidate; a pass shouldn't
  ignore what's already been decided at 4a).
- Does **not** replace Kind (see cross-cutting decision above). A tag can describe a
  DANGEROUS room's texture; it never determines which pattern file governs its contents.

**Open questions.**
- Exact facet split per rating (Danger/Physical/History was illustrative, not decided).
- Whether GENRE.md's existing Safe/Wild/Dangerous bank gets absorbed into `Tags.md` and
  removed from GENRE.md, or GENRE.md keeps a small fixed subset and `Tags.md` is additive.
  Leaning toward absorption - GENRE.md paying for an unused bank at every step is exactly
  the token-cost problem this plan is fixing; leaving a duplicate copy behind reopens it.
- How reuse/exhaustion is tracked across a large region (60+ locations pulling from one
  region's Tags.md) - simple round-robin, or explicit "spent" tracking on `Regions.md`.

**Status.** Not started.

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

## Plan 3 - Kind axes: give DANGEROUS one, widen WILD's

**Problem.** "Class" currently conflates two different axes. Kind (what a location
fundamentally *is*) and Weight/Prominence (how much attention/budget it gets) are cleanly
split for SAFE (5 Kinds x 3 Prominence levels) and WILD (3 Kinds nested under Landmark x 3
classifications), but DANGEROUS only has the Weight axis (High/Medium/Low) - a room's
"kind" (crypt, vault, shrine, barracks...) currently lives as free prose inside
`dangerous/Dressing.md`'s Purpose field rather than a structured, filed menu.

**Mechanic.**
- **DANGEROUS Kind axis**: add a KIND block set (candidates: Crypt, Vault, Shrine,
  Barracks, Workshop, Cistern - not decided) nested under each weight file
  (`High.md`/`Medium.md`/`Low.md`), exactly the way `wild/Landmark.md` nests
  Ruin/Lair/NaturalFeature under its own top-level spec. Per the cross-cutting decision
  above, this composes under weight - it supplies extra guaranteed/percentage lines for
  "what kind of room," weight still governs the room's overall budget and inclusion rate.
- **WILD Kind widening**: WILD currently has only 3 Kinds under Landmark
  (Ruin/Lair/NaturalFeature). Cheap to add a 4th/5th (candidates: a Camp/Holding - inhabited
  but mobile; a Crossing/Shrine) the same way `safe/Wealth.md` was added as a 5th SAFE Kind.
- Explicitly **not** proposing to add a 4th DANGEROUS weight tier or a 4th WILD
  classification - those are calibrated against location-count math, the Danger countdown,
  and node-role distribution rules (per the cross-cutting decision above); widening them
  means re-deriving that math, not just writing a new file.

**Integration.**
- A DANGEROUS Kind, once it exists, is exactly the kind of already-resolved fact Plan 4's
  pre-assignment pass should read before suggesting a creature/faction - a Vault-kind room
  suggests a different creature than a Barracks-kind room.
- Interacts with Plan 1: once `Tags.md` exists, check whether a new Kind's own vocabulary
  overlaps with a tag facet enough to collapse (per the Kind-vs-Tag delineation above, if a
  candidate Kind starts reading like a flavor descriptor rather than a content-selector, it
  belongs in `Tags.md` instead, not as a new Kind file).

**Open questions.**
- Final DANGEROUS Kind list - needs the same "what does each guarantee" spec work every
  existing class file went through, not just a name list.
- Whether every weight tier needs every Kind, or some Kinds are weight-restricted (a Vault
  might only make sense at Medium/High, never Low).

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
