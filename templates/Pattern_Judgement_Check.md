# Pattern_Judgement_Check.md

## Purpose
A non-mechanical review pass over `patterns/` - confirming, by human or model judgement, that the pattern library is internally consistent, produces content worth putting in front of players, and actually covers what the setting needs. Saved as `checks/PatternJudgementCheck.md`.

## Context
Consult when running this check:
- `GENRE.md` - the standard a pattern's content is measured against (specific, dangerous, low-magic, points-of-light - not generic fantasy dressing).
- every file in `patterns/`.
- `templates/Location.md` (and any other template that consumes a pattern) - to see how a pattern's output actually gets used, since a pattern can only be judged generic or specific, discoverable or not, by how it lands on the page.
- prior conversation/requests from the user calling for specific content, to check against the "gaps" and "doesn't fit anywhere" items below.

## Instructions
For each pattern file, and for the set of pattern files as a whole, confirm the following. Record each as Confirmed / Needs Attention, with a note.

- **No overlap or contradiction** - does one pattern's instructions duplicate or conflict with another's (e.g. two patterns both claiming the same trigger-and-effect shape, or giving incompatible guidance for the same situation)? Where two patterns legitimately share a boundary (e.g. `Trap.md` vs. `Mystery.md`, `Secrets.md` layered on top of any other pattern, `wild/Secret.md`'s location-level Clue/Trigger/Payload vs. `wild/Secrets.md`'s feature-level one), is the distinction stated clearly enough that a generator won't blur them?
- **Specific** - does the pattern push toward named, particular content (a specific mechanism, a specific creature, a specific object) rather than a reskinnable placeholder?
- **Discoverable** - does using the pattern require the players to notice, investigate, or search for something, rather than handing content to them automatically?
- **Interactive** - does the pattern give players something to act on (examine, trigger, disarm, solve, take) rather than pure read-aloud flavor?
- **Not overly generic** - could the pattern's output, as written, be dropped unchanged into any generic fantasy dungeon without a rewrite? If so, it needs sharper genre-specific hooks.
- **Gaps** - is there a location type, weight, or region rating with no pattern coverage, or a pattern file that's thin relative to how often it'll be drawn on?
- **Missing relevant features** - within an existing pattern, is there a feature type clearly relevant to that pattern's scope that isn't currently included (e.g. a common DANGEROUS-location situation the low/medium/high files don't address)?
- **Unhoused content** - has the user asked for specific content (a mechanic, a theme, a recurring element) that doesn't fit into any current pattern file? Flag it explicitly rather than force-fitting it into an unrelated pattern, so it can become a new pattern file or an addition to an existing one.

## Deliberate restatement
`patterns/` deliberately restates the same concept in each rating folder - a trap in SAFE is
a swindle, in WILD a snare, in DANGEROUS a deadfall - so that each is written for its own
context with no cross-rating branching in view. That trade buys sharpness and costs drift.

**So the duplication check is inverted here: two restatements that read the same are a
finding, not a convenience.** Where `safe/Trap.md`, `wild/Trap.md` and `dangerous/Trap.md`
converge on the same guidance, either differentiate them or establish that the shared part
is a *mechanic* and move it to `setting/Procedures.md`, or *format* and move it to
`templates/`. The pairs most at risk are the hook files, which exist in all three folders:
`Quest.md`, `Key.md` and `Lore.md`, plus each folder's version against its
`patterns/setting/` counterpart, which holds criteria rather than selection.

## Template
```
# Pattern Judgement Check - [Date or revision note]

## Cross-pattern
- No overlap or contradiction: [Confirmed / Needs Attention - note]
- Gaps in coverage: [Confirmed / Needs Attention - note]
- Unhoused user-requested content: [Confirmed / Needs Attention - note]

## [patterns/<folder>/File.md]
- Specific: [Confirmed / Needs Attention - note]
- Discoverable: [Confirmed / Needs Attention - note]
- Interactive: [Confirmed / Needs Attention - note]
- Not overly generic: [Confirmed / Needs Attention - note]
- Missing relevant features: [Confirmed / Needs Attention - note]

[repeat per pattern file]

## Open Items
- [Anything flagged Needs Attention, carried forward as an action item]
```
