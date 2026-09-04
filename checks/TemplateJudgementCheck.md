# Template Judgement Check - 2026-09-04, first full pass after the Brackvaen build

Run against `templates/` with `GENRE.md`, `CLAUDE.md`, `STEPS.md` and every file in
`patterns/` in view, following `templates/Template_Judgement_Check.md`. Twenty-four
template files. Seven are Needs Fix; the rest are Confirmed.

The pass has one theme. The templates were written before the five-folder `patterns/`
migration and before the framework settled that **creature AD is pitched against party
altitude, never against the region die** - and in four places they still carry the older
wording. Nothing in the generated setting followed the stale wording, so the cost so far is
zero; the cost of leaving it is that the next build has two sources of truth.

---

## templates/Outline.md
- Correct patterns, correct order: Confirmed - GENRE.md, then `patterns/setting/Outline.md`, then `setting/Procedures.md` for the Difficulty roll. Correct order and nothing extra.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - states the d8 default and that the die is a difficulty die, not a power level.
- Genre drift guardrails: Confirmed - party altitude is stated as "treasure hunters barely above commoners" by reference to GENRE.md.
- Consistency across templates: Confirmed.

## templates/Setting.md
- Correct patterns, correct order: **Needs Fix** - Context lists only `GENRE.md` and calls this "the first document, so it is the only fixed input". It is not: `STEPS.md` 2a puts `setting/Outline.md` before it, and `patterns/setting/Setting.md` exists and is not cited. The Context should read GENRE.md, `setting/Outline.md`, `patterns/setting/Setting.md`.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - name, three tags, two-or-three-sentence referee outline.
- Genre drift guardrails: Needs Fix, as above - the "name the pressure, not the plot" and "tags must constrain" discipline lives only in the uncited pattern file. `setting/Setting.md` happens to honour both, but the template does not ask for them.
- Consistency across templates: Confirmed.

## templates/History.md
- Correct patterns, correct order: **Needs Fix** - `patterns/setting/History.md` is not cited, and it carries the count (3-7 events), the inside/outside living memory requirement, the still-resolving requirement and the depth-layering rule that every DANGEROUS region depends on. The template asks only for "1 or more major events".
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - "[x] years ago" backward dating.
- Genre drift guardrails: Confirmed - "an event is a fact of the past, not a ticking clock aimed at the party" is stated in the Context line itself, which is the right place for it.
- Consistency across templates: Confirmed.

## templates/Truths.md
- Correct patterns, correct order: **Needs Fix** - same omission: `patterns/setting/Truths.md` is not cited, and it holds the count (3-6), the class-not-instance rule, the discoverable-by-acting requirement and the costs-somebody-something requirement.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - the class-not-object distinction survives in the Instructions, which is the one piece of the pattern that did make it across.
- Genre drift guardrails: Confirmed - "should sharpen the genre's stated constraints, not contradict or override them".
- Consistency across templates: Confirmed.

## templates/Rumours.md
- Correct patterns, correct order: **Needs Fix** - `patterns/setting/Rumours.md` is not cited, and it carries the T/P/F proportions (~40/~40/~20), the "at least two true and sounding false" line and the "partially true is the productive band" guidance. Without it the template asks for twenty rumours and no distribution.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - twenty numbered rows, T/P/F marked and not shared with players.
- Genre drift guardrails: Confirmed - "a lead the party can choose to chase, not a chapter in a story already written", and the explicit prohibitions on assuming a speaker or stating what to do with it.
- Consistency across templates: Confirmed.

## templates/Bestiary.md
- Correct patterns, correct order: Confirmed - GENRE.md, `patterns/setting/Bestiary.md`, `setting/Outline.md`, then the setting artifacts.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: Confirmed - unique individuals routed to `setting/NamedCreatures.md`, one-off variants inline, "the Bestiary holds only what recurs".
- Format edge cases preserved: Confirmed - the four lines, and Range/Sign/Disposition each a clause, exist "because the location patterns cite them rather than reinventing them per location".
- Genre drift guardrails: Confirmed - "low magic means most threats should be mundane, natural, or death-tainted rather than arcane".
- Consistency across templates: **Needs Fix, and this is the one that matters.** The Context line reads: "`setting/Outline.md` - the region dice. The AD spread is anchored to them, and a Bestiary written without them will not cover its own regions." That is the exact category error the rest of the framework exists to prevent. `CLAUDE.md`, `STEPS.md` 2f, `setting/Procedures.md` and `patterns/setting/Bestiary.md` all state that AD is anchored to **party altitude** and never to the region die - `patterns/setting/Bestiary.md` says so in bold. The template's own Instructions then send the reader to that pattern file, so a generator following the template gets contradicted one line later. Fix: "`setting/Outline.md` - **party altitude**. The AD spread is anchored to it and never to the region dice, which are a separate axis."

## templates/Factions.md
- Correct patterns, correct order: **Needs Fix** - `patterns/setting/Factions.md` is not cited, which loses the visual-identity requirement. The template's own Template block has no Identity field either, yet all three Brackvaen factions carry one and it is the field the pattern calls "the field this framework kept missing". Add the pattern to Context and an `- Identity:` line to the Template block.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - d6 only, no bonus, relative-only meaning, and the creature-that-is-also-a-power double entry are all stated well.
- Genre drift guardrails: Confirmed - "a Goal should be a standing condition the faction acts on turn to turn, not a countdown toward a scripted climax; points of light means no faction defaults to overarching authority."
- Consistency across templates: Confirmed - the faction/creature/party dice separation matches `setting/Procedures.md` exactly.

## templates/Treasure.md
- Correct patterns, correct order: **Needs Fix** - `patterns/setting/Treasure.md` is not cited. The template carries the table shapes but not the pattern's "anchor value to party altitude" instruction, which is what produced the wage line at the head of each generated table.
- No context creep: Confirmed, and stated unusually well - the explicit "do not consult location, region, or faction files" paragraph is the clearest no-creep statement in `templates/`.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - result 1 below average, results 2-3 varied, 4-20 randomised, the Quality/Effect percentages, cursed presenting as fine or masterwork, and the 100 cn per wt relationship as an average rather than a conversion.
- Genre drift guardrails: Confirmed - "Low Magic means the exceptional item should be rare and feel earned".
- Consistency across templates: Confirmed.

## templates/Procedures.md
- Correct patterns, correct order: Confirmed - GENRE.md, `patterns/setting/Procedures.md`, and the 2i-only additions.
- No context creep: Confirmed - the 2i-only qualifier on `setting/Setting.md`/`Truths.md` is exactly right.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: **Needs Fix** - "Sections, in order: Tests and Consequences, Traps, Searching, Time, Scaling." That is five. `patterns/setting/Procedures.md` requires six, the sixth being "Region dice - the Difficulty roll and what the counts derive from", and the generated `setting/Procedures.md` correctly carries it as a seventh section along with Local Conditions. The template is behind both the pattern and the artifact.
- Genre drift guardrails: Confirmed - "a procedure that needs a subsystem to run is the wrong procedure for this genre", and "tailoring is adjustment, not replacement".
- Consistency across templates: Confirmed.

## templates/Language.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed - the "at 2i / at 4d" split on which files to read for coinages is precise.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: Confirmed in spirit - this is the one continuously-appended artifact and the template says so in bold.
- Format edge cases preserved: Confirmed - "this file is appended to, never rewritten", and a name that cannot be decomposed is either wrong or a marked loan word.
- Genre drift guardrails: Confirmed - constructed language over real-world borrowing, per GENRE.md.
- Consistency across templates: Confirmed.

## templates/Region_Gazetteer.md
- Correct patterns, correct order: Confirmed - GENRE.md then `setting/Setting.md`. No pattern file exists for this artifact and none is needed; the ratings and dice come from `setting/Outline.md`, which `STEPS.md` 3a names.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - plain A-Z codes, doubling past 26, and the note that a DANGEROUS region may sit inside a WILD one. Brackvaen uses that last provision for C inside B.
- Genre drift guardrails: Confirmed - "regions should read as isolated and unevenly known, not as tiles in a fully-mapped, fully-governed world".
- Consistency across templates: Confirmed.

## templates/Connections.mmd
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - existence only, no type or quantity, which is what distinguishes it from `Region_Connections.mmd`.
- Genre drift guardrails: Confirmed - "connections should reflect isolation between settlements, not an implied network of control".
- Consistency across templates: Confirmed.

## templates/Region.md
- Correct patterns, correct order: Confirmed - GENRE.md, the setting artifacts, `setting/region/Regions.md`, the one matching `patterns/region/` file, then `setting/Procedures.md`. "read only the one that matches" is stated explicitly.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed and thorough - the five rating-specific fields are named and gated, Ambiance narrows to sensory-only for DANGEROUS because Architecture takes the rest, units split yards/miles, and the time assumption is stated per rating.
- Genre drift guardrails: Confirmed - the Situation field carries "it is a condition, not a plot, per GENRE.md" and distinguishes itself from the Events table in the same breath.
- Consistency across templates: Confirmed - matches `patterns/region/Safe.md`/`Wild.md`/`Dangerous.md` field for field.

## templates/Location_Gazetteer.md
- Correct patterns, correct order: Confirmed - GENRE.md and the Region Overview, with counts and class mix explicitly deferred to `patterns/region/`.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: Confirmed, and stated as strongly as it needs to be: "no Pattern and no descriptive sentence... pattern selection and content happen later, per location".
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - DANGEROUS weight, WILD classification, SAFE neither; the landmark/hidden/secret proportions; and the counts stated as a measurable trade rather than a rule of thumb.
- Genre drift guardrails: Confirmed - "DANGEROUS-region locations should read as ruin and chaos, not a designed conspiracy".
- Consistency across templates: **Needs Fix (minor)** - SAFE carries neither weight nor classification, which is correct, but `patterns/safe/Settlement.md` requires prominence (liner note / working / central) to be "decided per location, before anything is written", and `CLAUDE.md` repeats that it "is decided before anything is written and is deliberately *not* derived from size". Nothing records it. The Brackvaen gazetteer for A gives ten names and tags; the prominence spread turned out well (three locations at two features, four at three or four, three at five) but that is invisible to the gazetteer, to `tools/validate_setting.py`, and to anyone reviewing the region. Either the gazetteer should carry it as SAFE's third column or `patterns/safe/Settlement.md` should stop calling it a decision made first.

## templates/Region_Connections.mmd
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed - this region's `Locations.md` only.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - the three edge types are given with their meanings, which is what lets the validator distinguish a hidden edge from a missing one.
- Genre drift guardrails: Confirmed - "layout should read as decayed and found, not architected as a puzzle box aimed at the party".
- Consistency across templates: **Needs Fix (minor)** - `STEPS.md` 4b requires node roles (empty, dead end, branch, loop leg, divide) to be assigned here for DANGEROUS regions, and `patterns/dangerous/Low.md` reads them from here. The template says nothing about node roles and shows no place to put them. The Brackvaen build improvised a table under the graph in `setting/region/C/Connections.mmd`, which works well and should be promoted into this template.

## templates/Location.md
- Correct patterns, correct order: **Needs Fix** - the three-step ordering is right and clearly stated (class file for the inclusion spec, then the element files its spec drew, then `Dressing.md`/`Secrets.md`/`Naming.md` unconditionally). The fault is in step 2: it lists the element files as "`Trap.md`, `Creature.md`, `Treasure.md`, `Mystery.md`, `Faction.md`, `Quest.md`, `Key.md`, `Lore.md`, and (SAFE) `Commerce.md`..." as though the first eight exist in all three folders. `patterns/safe/` has no `Trap.md`, `Creature.md`, `Treasure.md` or `Mystery.md`; `patterns/wild/` has no `Faction.md`. Either the template names files that do not exist, or the pattern library has five gaps - see `checks/PatternJudgementCheck.md`, which treats it as the latter.
- No context creep: Confirmed, and this is the strictest and best-stated Context in the set. The closing paragraph - consult the other setting files "only to look up a name the stub or region overview already references, never to pull in new material wholesale" - is doing real work, and the Brackvaen location files visibly respect it.
- Pattern chosen at generation time, not earlier: Confirmed - the class file is selected from the stub's weight or classification at 4c, and nothing is pinned in the gazetteer.
- Two-phase registries respected: Confirmed - the 4c stub / 4d content split is stated in the Context list, restated under the Lore/Keys/Quests bullet with the exact citation syntax, and restated a third time in the closing "A note on completeness". Three statements is not too many for the rule most likely to be broken.
- Format edge cases preserved: Confirmed on every item the checklist names - header line, Player Summary bolding, Referee Notes italics, Feature labels without a leading article, trigger-gated exits belonging in Features, treasure cited as a single d20 pull and never named, feet/yards split with vertical drops always in feet, Features and Exits stating position and Features their own dimension where spatially significant, and the WILD landmark-then-hidden-then-secret generation order.
- Genre drift guardrails: Confirmed - "a Feature is something to react to on the spot, not a beat in a larger scripted arc".
- Consistency across templates: **Needs Fix (minor)** - the Exits syntax is `[what indicates the exit, and where it sits] -> [Code] [Location Name]`, with no form for an exit that leaves the map. Region B needed one three times (B.1's causeway running west out of the region into open water, B.2's four miles of unstaked wading east toward the flats, B.3's "no fixed way leads on from here"). All three are good writing and correct for a point crawl; all three are outside the stated format and invisible to the validator. The template should give them a form.

## templates/Lore.md
- Correct patterns, correct order: Confirmed - and the per-step Context split (2i needs nothing, 4c needs GENRE.md and the calling Feature, 4d needs the setting artifacts and the location file) is the clearest expression of the two-phase idea in `templates/`.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: Confirmed.
- Format edge cases preserved: Confirmed - form named in italics, location by code and name, content deferred to 4d.
- Genre drift guardrails: Confirmed by reference to `patterns/setting/Lore.md`, which carries "lore is an object, never spoken exposition" and the primary-source requirement.
- Consistency across templates: Confirmed.

## templates/Keys.md
- Correct patterns, correct order: Confirmed - including the nice touch of reading the location it unlocks at 4d "if it already exists".
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: Confirmed.
- Format edge cases preserved: Confirmed.
- Genre drift guardrails: Confirmed.
- Consistency across templates: Confirmed - the Key/Quest opposite-ends relationship is stated in `patterns/setting/Quests.md` and `patterns/dangerous/Key.md` and does not contradict anything here.

## templates/Quests.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: Confirmed - "at 4c record only the name and the two location codes".
- Format edge cases preserved: Confirmed - two-ended by definition, both ends named by code, Wants/Object/Obstacle/Terms with the obstacle called out as the one that matters, and Terms in the giver's own words.
- Genre drift guardrails: Confirmed - "a quest is work offered, not a plot the party is expected to complete".
- Consistency across templates: Confirmed.

## templates/NamedCreatures.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: Confirmed - and it handles the second-location case explicitly ("add that location to its existing row rather than duplicating it"), which is the case most likely to go wrong.
- Format edge cases preserved: **Needs Fix (minor)** - the Template block has Motivation and Description but no line for the two fields `patterns/setting/NamedCreatures.md` requires: "something it remembers, and something it wants". The Brackvaen entries all carry a `Remembers: ... Wants: ...` line, invented at 4d because the pattern demanded it and the template had nowhere to put it. Promote it into the Template block.
- Genre drift guardrails: Confirmed by reference - "a motivation is a standing goal, not a scripted arc".
- Consistency across templates: Confirmed - AD notation matches `templates/Bestiary.md` and `setting/Procedures.md`.

## templates/UniqueTreasures.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: Confirmed.
- Format edge cases preserved: Confirmed - "what it is, what it does, and what it costs", with the cost carried into the Template block's own Description line so it cannot be quietly dropped.
- Genre drift guardrails: Confirmed - the pattern's "Low Magic means the price is the entry" is the strongest single anti-drift line in the framework, and the template routes to it.
- Consistency across templates: Confirmed.

## templates/Template_Judgement_Check.md
- Correct patterns, correct order: Confirmed - GENRE.md, CLAUDE.md, STEPS.md, then all of `templates/` and `patterns/`.
- No context creep: Confirmed - a check is one of the two places a broad read is correct.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: Confirmed - it asks after the 4c/4d split explicitly.
- Format edge cases preserved: **Needs Fix** - the "correct patterns, correct order" bullet names `Creatures.md`, `Traps.md`, `Puzzles.md` and `Dangerous_High.md`. None of those files exists. The first three are pre-migration plurals (`Creature.md`, `Trap.md`) or absent entirely (`Puzzles.md`), and `Dangerous_High.md` is the pre-migration name for `patterns/dangerous/High.md`. A checklist that names files the library does not contain will generate false findings on every future run.
- Genre drift guardrails: Confirmed - it asks after the three named failure modes by name.
- Consistency across templates: Needs Fix, as above.

## templates/Pattern_Judgement_Check.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: **Needs Fix** - same stale names. The "no overlap or contradiction" bullet cites "`Traps.md` vs. `Puzzles.md`" and "`Wild_Secret.md`'s location-level Clue/Trigger/Payload vs. `Secrets.md`'s feature-level one". The live files are `patterns/wild/Secret.md` and `patterns/wild/Secrets.md`, and there is no `Puzzles.md` anywhere. The boundary the bullet is pointing at is real and worth checking - see the Pattern check - but it is named wrongly.
- Genre drift guardrails: Confirmed.
- Consistency across templates: Confirmed on the substance - the **Deliberate restatement** section is correct, well-argued, and is the reason the Pattern check found what it found.

## templates/Setting_Judgement_Check.md
- Correct patterns, correct order: Confirmed.
- No context creep: Confirmed - and it says why the breadth is licensed here, which is the right way to make an exception to `templates/Location.md`'s narrowness.
- Pattern chosen at generation time, not earlier: N/A.
- Two-phase registries respected: N/A.
- Format edge cases preserved: Confirmed - it asks after the WILD classification split, the parent-link requirement for hidden and secret locations, and the Position guidance from each rating's `Dressing.md`.
- Genre drift guardrails: Confirmed - "an implied central authority, commonplace magic, an authored plot rather than a situation".
- Consistency across templates: Confirmed.

---

## Open Items

1. **`templates/Bestiary.md` anchors the AD spread to the region dice.** Direct contradiction of `CLAUDE.md`, `STEPS.md` 2f, `setting/Procedures.md` and `patterns/setting/Bestiary.md`. Highest priority of the seven, because it is the one that would produce a wrong artifact rather than a thin one. Rewrite the Context line to anchor to party altitude and state that the dice are a separate axis.

2. **Six setting-level templates do not cite their `patterns/setting/` counterpart.** `Setting.md`, `History.md`, `Truths.md`, `Rumours.md`, `Factions.md` and `Treasure.md`. Every one of those pattern files holds the counts, proportions and hard requirements the template omits, so a generator following the template alone produces a legal but underspecified artifact. `templates/Bestiary.md`, `Outline.md`, `Procedures.md` and `Language.md` cite theirs correctly and are the model to copy. Add the pattern file to each Context list, and add an `- Identity:` line to `templates/Factions.md`'s Template block.

3. **`templates/Location.md` names five element files that do not exist**: `patterns/safe/Trap.md`, `Creature.md`, `Treasure.md`, `Mystery.md`, and `patterns/wild/Faction.md`. Resolve alongside the Pattern check's gap finding rather than separately - if the files are written, the template is already correct; if they are not, the template must qualify the list by folder.

4. **Both judgement-check templates cite pre-migration pattern filenames**: `Creatures.md`, `Traps.md`, `Puzzles.md`, `Dangerous_High.md`, `Wild_Secret.md`. Update to `Creature.md`, `Trap.md`, `patterns/dangerous/High.md`, `patterns/wild/Secret.md`, and decide what `Puzzles.md` should now point at - `templates/Location.md` still carries a full **Puzzles** bullet with its own rules and the pattern library has no file for it, only `Mystery.md`.

5. **`templates/Procedures.md` lists five sections where the pattern requires six.** Add Region Dice to the stated section list; the generated `setting/Procedures.md` already has it.

6. **`templates/NamedCreatures.md`'s Template block is missing `Remembers:` / `Wants:`.** The pattern requires both and the generated entries carry both; only the template is short.

7. **Two recording gaps.** SAFE prominence is required to be decided first and has nowhere to be written (`templates/Location_Gazetteer.md`); DANGEROUS node roles are required to be assigned at 4b and the template shows no place for them (`templates/Region_Connections.mmd`). The Brackvaen build solved the second with a table under the graph in `setting/region/C/Connections.mmd` - promote that into the template. The first is still open.

8. **`templates/Location.md`'s Exits syntax has no form for an exit that leaves the map.** Region B needed one three times. Add a form, and decide whether `tools/validate_setting.py` should recognise it or continue to ignore it.

9. **Not a template, but found while checking them: `README.md` is stale.** It describes the pre-migration `patterns/Safe.md` / `Wild.md` / `Dangerous_Low.md` layout, states that each `Locations.md` stub "pins a Pattern" - which `templates/Location_Gazetteer.md` explicitly forbids and this check's own criterion tests against - and omits `Outline.md`, `Procedures.md`, `Language.md`, `Quests.md` and the Treasure tables from its setting file list. It is the repository's front door and it currently contradicts `CLAUDE.md`.
