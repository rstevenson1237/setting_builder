# Template_Judgement_Check.md

## Purpose
A non-mechanical review pass over `templates/` - confirming, by human or model judgement, things `tools/validate_setting.py` structurally cannot: that each template enters the right pattern files and reads no more than it needs, that its defaults yield to the brief, and that it still encodes the edge cases this project has previously flagged as failure modes. Saved as `setting/checks/TemplateJudgementCheck.md`.

## Context
Consult when running this check:
- `GENRE.md`, `BRIEF.md` and `STYLE.md` - the standards a template's Instructions should be sharpening, not drifting from.
- `STEPS.md` - the declared build order and phase bookkeeping; a template's Context and its pending markers should match the step it is used in.
- every generation template in `templates/` - the three `*_Judgement_Check.md` files are not in scope; they are reviewed by being run.
- `python3 tools/validate_setting.py --read-set` - which pattern files each template's step enters and reaches, in place of reading all of `patterns/`.
- where a build exists, the table rows naming one location of each rating - what `templates/region/Location.md`'s Context actually assembles to.
- the last build's `setting/` and its `setting/checks/SettingJudgementCheck.md` - a template is judged by what it produced, and a default is judged by whether it won against the brief.

## Instructions
Read each generation template against the items below. Record **findings only**: each as
Needs Fix, with the template, the item, what is wrong, and - where the last build shows
it - what it produced. A template with no finding is named once, in the Confirmed line.

Every template:
- **Entry points, not the tree** - does its Context name every pattern file its artifact
  enters from, in the rating folder it describes, and nothing reached only through a Spec
  edge? `--read-set` shows the entries and what they reach.
- **No context creep** - does it read only what its artifact needs? A whole setting file
  read for one name or one column is creep.
- **Consistent with STEPS.md and with the other templates** - does it describe weight,
  rating, units, counts and phases the way STEPS.md and every other template do? A pending
  marker naming the wrong step is a finding here.
- **Genre drift guardrails** - where an authored plot, commonplace magic or a nearer
  authority could creep in (History, Factions, Treasure, Location Features), do its
  Instructions push against it?
- **Defaults yield to the brief** - is every count, mix and coverage rule stated as a
  default `BRIEF.md` replaces, and does its Context read `BRIEF.md`? Where the last build's
  brief contradicted a default, which did the artifact follow?
- **Defaults are neutral** - does any default carry one genre's assumptions (a type share
  justified by what one kind of region is built around, a mechanic one reference has) that
  belongs in a `GENRE.md` answer or a `BRIEF.md` line instead?
- **Every field is used** - is every field it asks for read by a later step, rolled at the
  table, or used by a referee running the artifact?

Only where the item names it:
- **Pattern chosen by weight alone** (`templates/safe/Locations.md`, `templates/wild/Locations.md`,
  `templates/dangerous/Locations.md`) - no gazetteer row pins a pattern beyond its Weight.
- **Two-phase registries** (`templates/region/Allocation.md` and the five registry templates) -
  a stub at 4d carries name and location only; content is 4h's.
- **Format edge cases preserved** (`templates/region/Location.md`, `templates/region/Region.md`) - every
  format rule still unambiguous against the entries generated from it, and against the
  previous pass's findings.
- **Rows match** (`templates/region/Location.md`) - does compile read every row naming its
  location and nothing else? A row no location file realizes, or a Feature no row carries,
  is a finding.

## Template
```
# Template Judgement Check - [Date or revision note]

Confirmed on every item: [templates/..., templates/...]

## Findings
- [templates/[folder]/File.md] - [item]: [what is wrong] - [what the last build shows, if it shows it]

## Open Items
- [Each finding, as an action, with its source: template, template default, or STEPS.md]
```
