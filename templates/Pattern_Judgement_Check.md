# Pattern_Judgement_Check.md

## Purpose
A non-mechanical review pass over `patterns/` - confirming, by human or model judgement, that the pattern library is internally consistent, produces content worth putting in front of players, and actually covers what the setting needs. Saved as `setting/checks/PatternJudgementCheck.md`.

## Context
Consult when running this check:
- `GENRE.md` - the standard a pattern's content is measured against (specific, dangerous, low-magic, points-of-light - not generic fantasy dressing).
- every file in `patterns/`.
- `templates/Location.md` (and any other template that consumes a pattern) - to see how a pattern's output actually gets used, since a pattern can only be judged generic or specific, discoverable or not, by how it lands on the page.
- prior conversation/requests from the user calling for specific content, to check against the "gaps" and "doesn't fit anywhere" items below.

## Instructions
For each pattern file, and for the set of pattern files as a whole, confirm the following. Record each as Confirmed / Needs Attention, with a note.

- **No overlap or contradiction** - does one pattern's instructions duplicate or conflict with another's (e.g. two patterns both claiming the same trigger-and-effect shape, or giving incompatible guidance for the same situation)? Where two patterns legitimately share a boundary (e.g. `Hazard.md` vs. `Mystery.md`, `patterns/wild/Secret.md`'s location-level Clue/Trigger/Payload vs. the feature-level concealed detail its own substrate block also draws), is the distinction stated clearly enough that a generator won't blur them?
- **The three tiers are supplied, and each drawing class states its own triple** - per `templates/Location.md` a location displays information at three tiers, and the pattern library is what fills them. For each class file, does its Spec draw something **obvious** (Dressing, a visible challenge, a reason to stop), something at the **trigger** tier that rewards acting on what is obvious, and - at whatever rate it sets - a **secret**: a concealed detail whose Clue, Trigger and Payload that file states itself? A class drawing a concealed detail without stating its own triple has lost the customization the distribution was for, and a class whose Spec reaches only one tier will produce flat entries however sharply its questions are phrased. Check the element files against the same three: a file supplying only read-aloud sits at one tier and is the **Interactive** finding below.
- **Specific** - does the pattern push toward named, particular content (a specific mechanism, a specific creature, a specific object) rather than a reskinnable placeholder?
- **Discoverable** - does using the pattern require the players to notice, investigate, or search for something, rather than handing content to them automatically?
- **Interactive** - does the pattern give players something to act on (examine, trigger, disarm, solve, take) rather than pure read-aloud flavor?
- **Not overly generic** - could the pattern's output, as written, be dropped unchanged into any generic fantasy dungeon without a rewrite? If so, it needs sharper genre-specific hooks.
- **Wiring** - is every pattern file actually reached? `tools/validate_setting.py` warns on
  any file no generation template can reach, walking STEPS.md to `templates/` to each
  template's named pattern files and out along Spec edges. An unreachable file is never
  read, so the content it describes is never generated - which is silent under-generation
  rather than a broken file, and the judgement here is whether the file should be wired in
  or should go. Check the reverse too: a file reached at a rate so low it will not fire in a
  setting of this size is wired but not funded.
- **Gaps** - is there a location type, weight, or region rating with no pattern coverage, or a pattern file that's thin relative to how often it'll be drawn on?
- **Missing relevant features** - within an existing pattern, is there a feature type clearly relevant to that pattern's scope that isn't currently included (e.g. a common DANGEROUS-location situation the low/medium/high files don't address)?
- **Unhoused content** - has the user asked for specific content (a mechanic, a theme, a recurring element) that doesn't fit into any current pattern file? Flag it explicitly rather than force-fitting it into an unrelated pattern, so it can become a new pattern file or an addition to an existing one.

## Deliberate restatement
`patterns/` deliberately restates the same concept in each rating folder - a trap in SAFE is
a swindle, in WILD a snare, in DANGEROUS a deadfall - so that each is written for its own
context with no cross-rating branching in view. That trade buys sharpness and costs drift.

**So the duplication check is inverted here: two restatements that read the same are a
finding, not a convenience.** Where `patterns/wild/Hazard.md` and `patterns/dangerous/Hazard.md`
converge on the same guidance, either differentiate them or establish that the shared part
is a *mechanic* and move it to `setting/Procedures.md`, or *format* and move it to
`templates/`. The pairs most at risk are the hook files, which exist in all three folders:
`Quest.md`, `Key.md` and `Lore.md`, plus each folder's version against its
`patterns/setting/` counterpart, which holds criteria rather than selection.

**The concealment triples are the same trade, and the same risk.** Each class that draws a
concealed detail states its own Clue, Trigger and Payload, so that what a clue is made of,
what a trigger is, and what a payload may be are written for what *that* class conceals -
construction underground, weather and time outdoors, people and mismatches in a settlement.
Two of those triples that have converged on the same wording are a finding here, exactly as
two Hazard files would be: either differentiate them, or establish that the shared part is
a *mechanic* and belongs in `setting/Procedures.md`, or a *rule* and belongs in `GENRE.md`,
which already owns the two that are genuinely constant.

## Template
```
# Pattern Judgement Check - [Date or revision note]

## Cross-pattern
- No overlap or contradiction: [Confirmed / Needs Attention - note]
- Three tiers supplied across the class files: [Confirmed / Needs Attention - note]
- Concealment triples stated per class, and not converged: [Confirmed / Needs Attention - note]
- Gaps in coverage: [Confirmed / Needs Attention - note]
- Unhoused user-requested content: [Confirmed / Needs Attention - note]

## [patterns/<folder>/File.md]
- Tier coverage - obvious / trigger / secret: [Confirmed / Needs Attention - note]
- Specific: [Confirmed / Needs Attention - note]
- Discoverable: [Confirmed / Needs Attention - note]
- Interactive: [Confirmed / Needs Attention - note]
- Not overly generic: [Confirmed / Needs Attention - note]
- Missing relevant features: [Confirmed / Needs Attention - note]

[repeat per pattern file]

## Open Items
- [Anything flagged Needs Attention, carried forward as an action item]
```
