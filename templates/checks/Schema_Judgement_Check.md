# Schema_Judgement_Check.md

## Purpose
A non-mechanical review pass over `patterns/*_Schema.md` - confirming, by human or model judgement, that the schemas are consistent, push toward content worth putting in front of players, and cover what the setting needs. Saved as `setting/checks/SchemaJudgementCheck.md`.

## Context
Consult when running this check:
- `GENRE.md` and `STYLE.md` - the standards a pattern's content is measured against; `STYLE.md` outranks every pattern.
- every schema in `patterns/`.
- `templates/region/Location.md` (and any other template that consumes a pattern) - to see how a pattern's output actually lands on the page.
- where a build exists, the table files of a sample of regions - at least one per rating - to see what the schemas' fields and nodes actually hold.
- where a build exists, this pass's `setting/checks/SettingJudgementCheck.md`: run this check after it, and start from its findings traced to a schema, which are this pass's best evidence.
- `BRIEF.md`, and the user's requests in the session or pull request that asked for this pass - for the unhoused-content item.

## Instructions
Record **findings only**, each as Needs Attention with the file, the item and a note. A
schema with no finding is covered by the Confirmed line. `tools/validate_setting.py`
enforces every field, enum and range; this check judges what they ask for.

Across the schemas:
- **No overlap or contradiction** - do two nodes or fields say the same thing, or conflict?
  Where a rating redefines a shared name, is the difference the rating's own?
- **Nothing contradicts STYLE.md** - does any comment require what `STYLE.md` forbids?
- **Gaps** - a location type, rating, or a thing a region needs (the ordinary finds
  `GENRE.md` names, the space its entrances open onto) that no field or node produces.
- **Unhoused content** - anything the brief or the user asked for that fits no field.

Per field, node and enum:
- **Specific** - it pushes toward named, particular content, not a reskinnable placeholder.
- **Discoverable** - what it adds has to be noticed, investigated or searched for.
- **Interactive** - it gives players something to act on, not read-aloud.
- **Not overly generic** - its output could not drop unchanged into any fantasy setting.
- **Enforceable** - a free-text field whose answers fall into a closed set is an enum or
  range not yet written.

## Template
```
# Schema Judgement Check - [Date or revision note]

Evidence: [the Setting Judgement Check this pass started from, and the locations resolved]

Confirmed on every item: [every file not named below]

## Across the schemas
- [item]: [Needs Attention - note, naming the files]

## Findings by file
- [patterns/[Name]_Schema.md] [node or field] - [item]: [note]

## Open Items
- [Each finding, as an action, with its source: field, enum, range, comment, or gap]
```
