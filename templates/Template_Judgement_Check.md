# Template_Judgement_Check.md

## Purpose
A non-mechanical review pass over `templates/` - confirming, by human or model judgement, things `tools/validate_setting.py` structurally cannot: that each template pulls the right patterns in the right order, and that it still encodes the edge cases this project has previously flagged as failure modes. Saved as `checks/TemplateJudgementCheck.md`.

## Context
Consult when running this check:
- `GENRE.md` - the standard every template's Context section should be sharpening, not drifting from.
- `CLAUDE.md` - the source of truth for how templates, patterns, and setting files relate, and for edge cases already called out explicitly (genre drift, pattern timing, narrow-context rules, and the like).
- `STEPS.md` - the declared build order; a template's Context list should match the artifacts that actually exist by the step it's used in.
- every file in `templates/` and every file in `patterns/` - a template can only be judged against the patterns it claims to use.

## Instructions
For each file in `templates/`, confirm the following. Record each as Confirmed / Needs Fix, with a note on what's wrong if not confirmed.

- **Correct patterns, correct order** - does the template's Context section list every pattern file actually relevant to that artifact, in the order they'd be consulted at generation time (e.g. `GENRE.md` first; unconditional patterns like `Dressing.md` before the rating/weight-specific pattern; element files like `Treasure.md`/`Creature.md`/`Hazard.md`/`Mystery.md` only after a chosen spec line calls for them)? Does it name only files that exist **in the rating folder it is describing** - the three folders do not hold the same set, and `patterns/safe/` in particular is thinner than the others?
- **No context creep** - does the template stick to the narrow Context list CLAUDE.md specifies for it, rather than pulling in setting files wholesale "just in case"? (`templates/Location.md`'s Context is the strictest example - other setting files are for looking up a name already referenced, never more.)
- **Pattern chosen at generation time, not earlier** - for `templates/Location.md`, does it still make clear the pattern is picked now, from the matching `patterns/` file, rather than pinned in the gazetteer stub?
- **Two-phase registries respected** - do templates that can introduce a Lore/Key/Named Creature/Unique Treasure entry (chiefly `templates/Location.md`) still correctly separate step 4c (stub: name and location only, no content) from step 4d (full entry, written later)?
- **Format edge cases preserved** - read `templates/Location.md` (the most format-sensitive template) against the locations actually generated from it, and against the findings in the previous `checks/TemplateJudgementCheck.md`. Is every format rule it states still unambiguous, and has any rule a past pass had to call out gone missing or gone vague? Check it against the template, never against a list kept here - a copy of those rules in this file would drift out of step with the template it is meant to be auditing.
- **Genre drift guardrails** - does the template's Instructions section actively discourage the genre's main failure mode (an authored plot creeping in, magic becoming commonplace, an implied central authority) wherever that template is the kind of place it could creep in (History, Factions, Location Features)?
- **Consistency across templates** - do two templates that touch the same concept (e.g. weight, region rating, units) describe it the same way, rather than drifting into contradictory wording?

## Template
```
# Template Judgement Check - [Date or revision note]

## [templates/File.md]
- Correct patterns, correct order: [Confirmed / Needs Fix - note]
- No context creep: [Confirmed / Needs Fix - note]
- Pattern chosen at generation time, not earlier: [Confirmed / Needs Fix - note, or N/A]
- Two-phase registries respected: [Confirmed / Needs Fix - note, or N/A]
- Format edge cases preserved: [Confirmed / Needs Fix - note, or N/A]
- Genre drift guardrails: [Confirmed / Needs Fix - note]
- Consistency across templates: [Confirmed / Needs Fix - note]

[repeat per template file]

## Open Items
- [Anything flagged Needs Fix, carried forward as an action item]
```
