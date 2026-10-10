# Pattern_Judgement_Check.md

## Purpose
A non-mechanical review pass over `patterns/` - confirming, by human or model judgement, that the pattern library is internally consistent, produces content worth putting in front of players, and actually covers what the setting needs. Saved as `setting/checks/PatternJudgementCheck.md`.

## Context
Consult when running this check:
- `patterns/SPEC.md` - the standard every pattern file's shape is tested against.
- `GENRE.md` and `STYLE.md` - the standards a pattern's content is measured against; `STYLE.md` outranks every pattern.
- every file in `patterns/`.
- `templates/region/Location.md` (and any other template that consumes a pattern) - to see how a pattern's output actually lands on the page.
- where a build exists, the table files of a sample of regions - at least one per rating - to see what a class file's rates and draws actually allocated.
- where a build exists, this pass's `setting/checks/SettingJudgementCheck.md`: run this check after it, and start from its findings traced to a pattern, which are this pass's best evidence.
- `BRIEF.md`, and the user's requests in the session or pull request that asked for this pass - for the unhoused-content item.

## Instructions
Record **findings only**, each as Needs Attention with the file, the item and a note. A
file with no finding is covered by the Confirmed line; do not write a block per file.

Across the library:
- **No overlap or contradiction** - does one pattern duplicate or conflict with another?
  Where two share a boundary (`Hazard.md` and `Mystery.md`; a Secret location's access
  triple and its inner one), is the distinction stated where a generator will see it?
- **The three tiers are supplied, and each drawing class states its own triple** - per
  `templates/region/Location.md`'s three tiers, does each class file draw something obvious,
  something at the trigger tier, and - at its own rate - a concealed detail whose Clue,
  Trigger and Payload that file states itself?
- **Rates compound sensibly** - read the sampled resolutions together: a per-exit rate
  that gates nearly every room, rates that between them fire in almost every room, a rate
  so low a region this size never meets it. Record the rate and what it compounds to.
- **Nothing contradicts STYLE.md** - does any line require what a standing consequence
  forbids, or forbid what one requires?
- **Wiring** - `tools/validate_setting.py` warns on any file the root or no template
  reaches; judge whether each should be wired in or go, and whether a reached file is
  drawn at a rate this setting's size will ever meet.
- **Gaps** - a location type, weight, rating, or a thing a region needs (the space its
  entrances open onto, the ordinary finds `GENRE.md` names) that no pattern produces.
- **Unhoused content** - anything the brief or the user asked for that fits no current
  pattern. Flag it rather than force-fitting it.

Per node of `patterns/Schema.md`, which is what a location draws; a `setting/` or
`region/` pattern is judged by the library items above and by what its artifact produced:
- **Specific** - pushes toward named, particular content rather than a reskinnable
  placeholder.
- **Discoverable** - what it adds has to be noticed, investigated or searched for.
- **Interactive** - it gives players something to act on, not read-aloud.
- **Not overly generic** - its output could not be dropped unchanged into any fantasy
  dungeon.
- **Missing relevant features** - a feature clearly within its scope that it never draws.

## Template
```
# Pattern Judgement Check - [Date or revision note]

Evidence: [the Setting Judgement Check this pass started from, and the locations resolved]

Confirmed on every item: [every file not named below]

## Across the library
- [item]: [Needs Attention - note, naming the files]

## Findings by file
- [patterns/<folder>/File.md] - [item]: [note]

## Open Items
- [Each finding, as an action, with its source: pattern line, rate, notation, or gap]
```
