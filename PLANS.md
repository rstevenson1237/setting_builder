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
- `dangerous/Secrets.md` finished dissolving. Its INCLUSION table set the concealment rate
  by weight and, at LOW, by node role - a rate that varies between the classes drawing it,
  which by this library's own rule is the drawing class's line. `dangerous/Medium.md` now
  draws at 40%, `dangerous/Low.md` at the three node-role rates (100% appears-as-dead-end,
  50% honest dead end, 30% everything else), and `dangerous/High.md` states in prose that
  it draws none and why. The dead-end/appears-as-dead-end reasoning moved to LOW, where
  node role lives, and its prohibition became LOW's first Constraint. The file's mode went
  from `second pass` to `ingredient`, which was the honest description all along once HIGH
  stopped drawing it, and the anomaly the mode pass surfaced is closed. `safe/Secrets.md`
  and `wild/Secrets.md` keep their rates, because a flat 10% and a flat 20% are the same
  for every class that draws them - which is what makes DANGEROUS the odd one rather than
  the three being inconsistent.
- Reach mode declared and validated (the old item 3, then item 1). Every file's `## Read at`
  now opens `**Mode: ...**`, from `second pass`, `kind`, `ingredient`, `conditional`, or
  `entry` for a file a STEPS.md step reads directly and nothing draws. The validator checks
  the declaration is present and valid, and that any file claiming one of the four drawn
  modes is actually cited by some other file's Spec - which is the orphan check SPEC.md had
  been proposing, and what keeps `safe/Naming.md`, `wild/Naming.md`, `wild/Faction.md` and
  `dangerous/Faction.md` from silently reopening. Edges are read from the fenced blocks
  alone. Two corrections the review pass forced: "exactly one of four modes" was not true -
  `safe/People.md` is a Kind and every SAFE location's gate person, and `dangerous/Key.md`
  is drawn from both ends, so both declare `kind, ingredient` - and `Faction` means a
  different mode in each rating rather than one row in the table.
- The earns-patterns test corrected, one commit after the pass that introduced it. The
  demotion pass used reach mode as the test and it does not survive contact with the files:
  it forced `Dressing` to be named a standing exception, and it split the four files drawn
  by `safe/Settlement.md`'s single hook line three-to-one, stripping `safe/Faction.md`
  while `safe/Quest.md`, `Lore.md` and `Key.md` kept theirs off the identical line. The
  test is what a file's output *is* - body content versus a shape applied to a location -
  which gets `Dressing` right with no exception and all four hooks right together, and
  leaves only `Naming` and `Secrets` as shapes. `safe/Faction.md` and `wild/Faction.md`
  have their patterns back and the compile list is thirty-five. Mode stays as coupling
  information; it just does not decide this.
- Items 1 and 2 closed together, since both decided what step 1b rewrites. The neutral
  option menus came out of `## Design patterns` in twenty-eight files - all sixteen
  `setting/*`, all three `region/*`, `dangerous/Low.md`, and the `Naming`, `Secrets` and
  `Faction` files in all three ratings - and into those files' Specs, with five
  forbidden-pathway paragraphs split off into Constraints on the way. `dangerous/Environmental.md`
  and `dangerous/Residual.md` gained the `## Design patterns` they never had, which is what
  had them generating thinner than `dangerous/Trap.md`. Step 1b's compile list was rewritten
  from the reach-mode split - Kind and ingredient files plus the three `Dressing` files,
  thirty-three in all - and `tools/validate_setting.py` now checks that list against the set
  of files carrying the section, in both directions, so the two cannot drift apart again.
  `patterns/SPEC.md`, `README.md` and `CLAUDE.md` track the rule.
- The two small items closed: `setting/Setting.md`'s "Don't default to the last one" was a
  forbidden-pathway warning embedded mid-paragraph in Design patterns, and is now a
  Constraint stated generally - a standing obligation is one option among many and an
  economic instrument is a flavor of that one option, never the setting's engine.
  `setting/Genre.md` now says in its own header that it is an elicitation procedure
  carrying sections the skeleton does not, so its Seed pool, eligibility test, narrowing
  rounds and Q2 axes read as the procedure rather than as a file left unconverted.

## Implementation

Rationale and open questions: `DRAKENHOLD.md`. Phases land in order.

**1. `STEPS.md`**
- [x] Add step ids by suffix; never renumber - every `## Read at` cites them.
- [x] `4c`: in a DANGEROUS region the unit of generation is the block. HIGH region-wide
      first, then block by block, MEDIUM before LOW within each.

**2. Templates and `STEPS.md` 4b**
- [x] `STEPS.md` `4b`: drop the node-role assignment. A DANGEROUS region produces a
      block-existence diagram plus one typed diagram per block; SAFE and WILD keep a single
      region diagram. Confirm and match an existing cross-block edge before writing one.
- [x] `Connections.mmd`: existence only, and the group-tier rule stated. `Region_Connections.mmd`
      splits by rating - typed location graph for SAFE and WILD, block-existence for DANGEROUS.
      *Plan correction: the item read "existence only" for both, which is wrong for SAFE and
      WILD, where the region diagram is the location tier.*
- [x] `Region_Connections.mmd`: node-role table and "every location gets one" deleted.
- [x] New `Block_Connections.mmd`: one diagram per block. Header carries block name, purpose
      family, region, room budget. Location-tier edges carry type. A cross-block edge is
      declared in both files, identical in existence, type and direction. Locations connect
      only to locations.
- [x] `Location.md`: `setting/Truths.md` in the consult list, availability not a quota.
- [x] `Setting_Judgement_Check.md`: Room to Grow also names reinforcement candidates -
      elements thin enough on the ground that a later pass could thicken them. Recommendation
      only; 5c authors nothing.

**3. `patterns/`**
- [x] New `dangerous/Door.md`: `Mode: second pass`; kinds open, one-way, secret, vertical;
      carries `## Design patterns`. Add it to `STEPS.md` step 1b's compile list in the same
      change - the validator checks that list against the tree in both directions, so the
      list entry errors until the file carrying the section exists.
- [x] `dangerous/Dressing.md`: `1  Every exit typed and positioned` becomes an edge citing
      `dangerous/Door.md`.
- [x] `dangerous/Low.md`: restate the three concealment rates against the location's exits.
- [x] `dangerous/High.md`, `Medium.md`, `Low.md`: demand-side Key line replaced by an
      obligation draw at rate `1`. *The Quest line is reworded, not deleted - DANGEROUS
      registers supply, so the line stays rated.*
- [x] `dangerous/Key.md`: the supply-side line records a `setting/Keys.md` stub; `Unlocks` is
      written at 4d.
- [x] Weight files: reword "the target of a quest given elsewhere" to supply-side
      registration, per `dangerous/Quest.md`.
- [x] `setting/Secrets.md`: rate varies by rating and, in DANGEROUS, by weight and by the
      location's exits.
- [x] `wild/Landmark.md`: drop the node-role analogy.
- [x] `region/Dangerous.md`: LOW SHAPE MIX replaces LOW NODE ROLE MIX; the per-location
      NODE ROLE block is deleted. *Also added the BLOCKS spec, which phase 1's 4c cites for
      the block definition and which the plan did not list.*

**4. `GENRE.md`**
- [x] House rules added to the fixed block in both `GENRE.md` and `templates/Genre.md`,
      stated as standing consequences rather than a fourth test, with the tests winning any
      disagreement. *The predecessor's "the clue lives outside the location holding the
      secret" is reconciled rather than copied: it contradicts `patterns/setting/Secrets.md`,
      whose Clue is local and visible by ordinary observation. The rule is split - the clue
      is local, the answer more often comes from elsewhere.*

**5. `tools/validate_setting.py`**
- [ ] `EDGE_RE`: match labelled edges.
- [ ] Cross-block edges: symmetry over existence, type and direction.
- [ ] Location-tier files: no bare region nodes.
- [ ] Every region-tier edge realized by at least one location-tier edge; no cross-region
      location edge without one.
- [ ] Unconsumed `setting/Keys.md` obligations at the close of 4c: error.
- [ ] A block whose induced subgraph is disconnected: warning.
- [ ] A purpose repeated within a block: warning.
- [ ] LOW node mix, per region: 60%+ of LOW-weight locations have degree != 2, and no single
      degree class (1, 2, 3, 4+) exceeds a third. Warning. Dedupe cross-block edges declared
      in both files before computing degree. Blind spot to state in the message: a loop leg
      is degree 2 and reads as a corridor.
- [ ] `--pending <block>`: list inbound edges declared against a block.

## Open

**1. `wild/Hazard.md` and `wild/Creature.md` share a boundary that is stated in only one
direction.** Hazard's Constraint says a living hazard with a want, a reaction, or somewhere
else to be is a creature; `wild/Creature.md` does not say the converse. Per `STEPS.md` step
5b the duplication check is inverted for `patterns/`, so this is the kind of thing a
Pattern Judgement Check should settle against a real build rather than by anticipation.

**Closed, deliberately.** Steps `3a`, `3b` and `5a`-`5c` have no pattern file. These are
user-led steps and their defaults have held up; no pattern is planned.
