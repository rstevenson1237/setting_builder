# Template_Judgement_Check.md

## Purpose
A non-mechanical review pass over `templates/` - confirming, by human or model judgement, things `tools/validate_setting.py` structurally cannot: that each template reads the right schemas and no more than it needs, that it leaves every count, mix and rate to the brief, and that it still encodes the edge cases this project has previously flagged as failure modes. Saved as `setting/checks/TemplateJudgementCheck.md`.

## Context
Consult when running this check:
- `GENRE.md`, `BRIEF.md` and `STYLE.md` - the standards a template's Instructions should be sharpening, not drifting from.
- `STEPS.md` - the declared build order and phase bookkeeping; a template's Context and its pending markers should match the step it is used in.
- every generation template in `templates/` - the three `*_Judgement_Check.md` files are not in scope; they are reviewed by being run.
- `python3 tools/validate_setting.py --read-set` - which templates and schemas each step reads.
- where a build exists, the table rows naming one location of each rating - what `templates/region/Location.md`'s Context actually assembles to.
- the last build's `setting/`, its `setting/checks/SettingJudgementCheck.md`, and the findings its `setting/checks/Review.md` sent to the framework - a template is judged by what it produced.

## Instructions
Read each generation template against the items below. Record **findings only**: each as
Needs Fix, with the template, the item, what is wrong, and - where the last build shows
it - what it produced. A template with no finding is named once, in the Confirmed line.

Every template:
- **The right schemas** - does its Context name the schemas its artifact is checked
  against, its own rating's and no other? `--read-set` shows them.
- **No context creep** - does it read only what its artifact needs? A whole setting file
  read for one name or one column is creep.
- **Consistent with STEPS.md and with the other templates** - does it describe weight,
  rating, units, counts and phases the way STEPS.md and every other template do? A pending
  marker naming the wrong step is a finding here.
- **Genre drift guardrails** - where an authored plot, commonplace magic or a nearer
  authority could creep in (History, Factions, Treasure, Location Features), do its
  Instructions push against it?
- **No defaults** - does it state a count, mix or rate itself, or fall back on one where
  `BRIEF.md` is silent? Each belongs in `BRIEF.md`, which the template reads.
- **Every field is used** - is every field it asks for read by a later step, rolled at the
  table, or used by a referee running the artifact?

Only where the item names it:
- **Format edge cases preserved** (`templates/region/Location.md`, `templates/region/Region.md`) - every
  format rule still unambiguous against the entries generated from it, and against the
  previous pass's findings.
- **Entries match** (`templates/region/Location.md`) - does each write-up carry every entry
  `--location` prints for it and nothing else? An entry no Feature carries, or a Feature no
  entry carries, is a finding.

## Template
```
# Template Judgement Check - [Date or revision note]

Confirmed on every item: [templates/..., templates/...]

## Findings
- [templates/[folder]/File.md] - [item]: [what is wrong] - [what the last build shows, if it shows it]

## Open Items
- [Each finding, as an action, with its source: template or STEPS.md]
```
