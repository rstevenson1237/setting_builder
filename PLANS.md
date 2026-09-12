# Plans

Live working notes: what the pattern library's architecture now is, and what is still open.
Unlike `STEPS.md` (the authoritative record of the *build* workflow) and `patterns/SPEC.md`
(the authoritative field spec), this file is the running state of architectural work - what
was decided, what it replaced, and what has not been done yet.

The previous contents of this file - four interlocking plans covering the tag mechanism,
region-level field review, Kind axes, pre-assignment, and citation format - were all either
executed or superseded, and are preserved in git history. The design history for the tag
decision (System B: compile genre content into the pattern files rather than joining a
lookup table at generation time) lives there; that decision still holds and is described in
`README.md` and `STEPS.md` step 1b.

## Where the architecture landed

**One skeleton, on every `patterns/*/*.md` file.** `Provides / Read at / Spec /
Design patterns / Constraints`. `patterns/SPEC.md` is the full spec.

**One governing distinction.** A pattern file's content is either *neutral and permanent*
(true in any setting, written once) or *specific and compiled* (rewritten at step 1b from
the chosen genre reference). Spec is the first; Design patterns is the second. Every other
rule follows from keeping them apart. Prefer a question to a pattern wherever the verbiage
can carry it - patterns are a budgeted insertion against flat output, not the default home
for any list.

**Every Spec line is an edge or a question.** An edge names another pattern file in
parentheses, the only other file that line requires. A question states something the
generator answers and cites nothing. That makes the library one tree: a file whose Spec has
outgoing edges is a classifier, a file whose Spec is all questions is a leaf, and neither is
declared anywhere - it is read off the citations, so the structure cannot fall out of step
with itself. A classifier may cite another classifier, which is how a category earns a
middle level rather than being a rename.

**Where a line lives follows from whether it varies.** A line that differs between the
classes drawing it belongs in the drawing class's Spec; a line that is the same for all of
them belongs in the file it cites. Same test `setting/Procedures.md` applies one level up.

**Constraints holds every prohibition** - what belongs in another file, what this file must
never do, a named failure mode. Blank at creation; filled as patterns are refined and
negative patterns are identified, and from failures observed during a build.

**The unit of generated content is the Feature, not the word.** Where a contract line names
something the players can address as its own object, it becomes its own Feature - treasure
hidden in a pillar and guarded by a beast is three Features, not one complex one. Entries
are terse because one Feature states one thing, not because a cap says so. All word budgets
were removed.

**Every classifier's Spec is grouped into blocks:** substrate (what this place is),
challenge (what stands between the party and what they want), reward (what is here to
take), registry (what ties this place to somewhere else, in either direction). All three
ratings are on it. WILD adds a fifth, **access**, because out in the country how a place is
reached is content rather than the connection graph. SAFE has no challenge - a settlement
opposes nobody - and a **gate** in the slot instead, the person and their terms, with
**transaction** as its reward. `patterns/SPEC.md` carries the table.

**DANGEROUS has a middle tier; WILD does not, and did not need one.** `dangerous/Encounter`
draws `{creature | named creature | faction}` and `dangerous/Hazard` draws
`{trap | environmental | residual}`, both classifiers in their own right, because each
mechanism carries a contract of its own. `wild/Hazard`'s three mechanisms answer the same
two questions whichever is drawn, so the choice is one line. WILD's kind files - `Ruin`,
`Lair`, `NaturalFeature`, `Crossing` - sit where the middle tier sits in DANGEROUS, and are
drawn at all three tiers rather than at Landmark alone.

**The reach gradient is priced against access, not weight.** WILD's rated lines come to
about 0.6 of a Feature at Landmark, 0.8 at Hidden, 1.0 at Secret: a place that costs
nothing to reach is allowed to be a place and nothing more, and one a party spent an action
looking for owes them something. Which parents carry children is read off the region's
`Connections.mmd` at 4b, so the lead lines are mandatory per child and not a rate.

## Completed

- Field vocabulary aligned across all 65 files: `Decides` to `Provides`; `Patterns` and
  `Examples` - one slot under two names - merged to `Design patterns`.
- 33 closed-pathway paragraphs moved from Spec/Patterns prose into `Constraints` across 25
  files. Positive rules phrased contrastively stayed put.
- `Read at` corrected against `STEPS.md`: a phase-2 renumber had left eight `setting/`
  patterns pointing one step too far down, three at a step `2i` that no longer existed. The
  same dead step was in seven `templates/` files.
- `Read at` added to `setting/Keys.md`, `Quests.md`, `NamedCreatures.md`,
  `UniqueTreasures.md` - four of the five two-phase stub files were silent about a
  lifecycle the fifth documented.
- Element contracts moved out of their classifiers: `wild/Landmark.md` held four KIND blocks
  and `dangerous/High.md` held the MYSTERY block, leaving five files with no Spec of their
  own.
- `Design questions` folded into `Spec` - both were neutral and permanent, so they sat on
  the same side of the governing distinction and the split was a fact about tree position
  rather than content.
- Word budgets removed (`templates/Location.md`'s per-Feature cap; `safe/Dressing.md`'s and
  `wild/Dressing.md`'s whole-entry budgets, which were provisional figures carried by
  analogy from a DANGEROUS calibration recorded nowhere) and replaced with feature
  decomposition.
- `dangerous/High.md`, `Medium.md` and `Low.md` restructured onto the four blocks;
  `Encounter.md`, `Hazard.md`, `Environmental.md` and `Residual.md` created; `Treasure.md`
  absorbed the reward end of Lore and Keys; `dangerous/Trap.md` slimmed to what is true of
  a trap alone once Hazard owns clue, trigger and impact.
- `wild/Landmark.md`, `Hidden.md` and `Secret.md` restructured onto the blocks plus access;
  `wild/Trap.md` renamed `wild/Hazard.md`, since its own first line already read "set by
  somebody, or a condition of the ground" and Trap named one of three mechanisms in it;
  `wild/Treasure.md` absorbed Lore and Keys as things a find can be; all three tiers draw a
  Kind, where only Landmark did; child leads became graph-determined; Landmark stopped
  restating `wild/Dressing.md`'s position line; the four kind files took `wild/Faction.md`
  out of Design patterns, where step 1b could have recompiled the edge away, and into their
  Specs.
- `safe/Settlement.md` restructured onto substrate / gate / transaction / registry. The
  gate line was being asked three times, once each in `safe/Authority.md`, `Social.md` and
  `Commerce.md`; it is one line on the classifier now, and the Kind files keep the menu of
  answers. The duplicated 10% Secrets rate went the same way `dangerous/Medium.md`'s did.
- Two resolvable-but-wrong citations fixed: `dangerous/High.md` and `safe/Wealth.md` both
  routed a Unique Treasure stub through `patterns/setting/Keys.md`.
- `tools/validate_setting.py` extended: the five sections present, no leftover
  `Design questions` heading, and `Read at` step ids resolved against `STEPS.md`.
  `build_site.py` and `patterns.js` track the field changes. Clean run is 0 errors,
  0 warnings.
- `patterns/SPEC.md` written.
- The two small items closed: `setting/Setting.md`'s "Don't default to the last one" was a
  forbidden-pathway warning embedded mid-paragraph in Design patterns, and is now a
  Constraint stated generally - a standing obligation is one option among many and an
  economic instrument is a flavor of that one option, never the setting's engine.
  `setting/Genre.md` now says in its own header that it is an elicitation procedure
  carrying sections the skeleton does not, so its Seed pool, eligibility test, narrowing
  rounds and Q2 axes read as the procedure rather than as a file left unconverted.

## Open

**1. Twenty classifiers carry `Design patterns` that are neutral option menus** - sixteen of
them `setting/*`, e.g. `setting/Keys.md`'s "Forms", `setting/Truths.md`'s "Kinds of truth".
By the neutrality test these are Spec questions, not compiled content. Held together with
item 2, because both change what step 1b rewrites.

**2. `STEPS.md` step 1b's compile list is wrong in two directions.** It names 18 files while
saying "every other tier-2 element file", so 21 element files carrying patterns are not on
it; and `Encounter`, `Hazard`, `Environmental` and `Residual` are new and not on it either.
`Environmental.md` and `Residual.md` have no `Design patterns` at all and will generate
thinner than `dangerous/Trap.md` until they do. Splitting the list by reach mode is what decides which
files belong on it - not all of them do.

**3. Reach modes are modelled but not implemented.** `patterns/SPEC.md` records four ways an
element is reached - second pass, kind, ingredient, conditional - read off the classifiers'
spec lines. Making the mode explicit and validated is what would keep the orphans the last
two passes closed - `safe/Naming.md`, `wild/Naming.md`, `wild/Faction.md` and
`dangerous/Faction.md` - from silently reopening. The table in SPEC.md is a reading of the
spec lines, not something the files declare, and is worth a review pass before it gets
encoded.

**4. `dangerous/Secrets.md` is half dissolved.** HIGH no longer draws it - concealment there
is a hidden Treasure disposition or a Hazard's or Mystery's own clue. LOW and MEDIUM still
do, and at LOW it is load-bearing (its rate is set by node role, the only place node role
feeds content). Finishing the dissolution means rehoming that inclusion table into the class
Specs.

**5. `wild/Hazard.md` and `wild/Creature.md` share a boundary that is stated in only one
direction.** Hazard's Constraint says a living hazard with a want, a reaction, or somewhere
else to be is a creature; `wild/Creature.md` does not say the converse. Per `STEPS.md` step
5b the duplication check is inverted for `patterns/`, so this is the kind of thing a
Pattern Judgement Check should settle against a real build rather than by anticipation.

**Closed, deliberately.** Steps `3a`, `3b` and `5a`-`5c` have no pattern file. These are
user-led steps and their defaults have held up; no pattern is planned.
