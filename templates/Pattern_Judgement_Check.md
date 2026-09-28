# Pattern_Judgement_Check.md

## Purpose
A non-mechanical review pass over `patterns/` - confirming, by human or model judgement, that the pattern library is internally consistent, produces content worth putting in front of players, and actually covers what the setting needs. Saved as `setting/checks/PatternJudgementCheck.md`.

## Context
Consult when running this check:
- `patterns/SPEC.md` - the standard every pattern file's shape is tested against.
- `GENRE.md` and `STYLE.md` - the standards a pattern's content is measured against; `STYLE.md` outranks every pattern.
- every file in `patterns/`.
- `templates/Location.md` (and any other template that consumes a pattern) - to see how a pattern's output actually lands on the page.
- `python3 tools/context.py 4c CODE` over a sample of locations - at least one per class file - to see what a class file's rates and draws actually resolve to.
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
  `templates/Location.md`'s three tiers, does each class file draw something obvious,
  something at the trigger tier, and - at its own rate - a concealed detail whose Clue,
  Trigger and Payload that file states itself?
- **Rates compound sensibly** - read the sampled resolutions together: a per-exit rate
  that gates nearly every room, rates that between them fire in almost every room, a rate
  so low a region this size never meets it. Record the rate and what it compounds to.
- **Nothing contradicts STYLE.md** - does any line require what a standing consequence
  forbids, or forbid what one requires?
- **Neutral and permanent** - does any Spec line, draw item or Constraint carry one
  genre's assumptions rather than a question `GENRE.md` answers?
- **Wiring** - `tools/validate_setting.py` warns on any file the root or no template
  reaches; judge whether each should be wired in or go, and whether a reached file is
  drawn at a rate this setting's size will ever meet.
- **Gaps** - a location type, weight, rating, or a thing a region needs (the space its
  entrances open onto, the ordinary finds `GENRE.md` names) that no pattern produces.
- **Unhoused content** - anything the brief or the user asked for that fits no current
  pattern. Flag it rather than force-fitting it.

Per file, applied only to the class and element files a location draws (the files under
`safe/`, `wild/` and `dangerous/`); a `setting/` or `region/` pattern is judged by the
library items above and by what its artifact produced:
- **Specific** - pushes toward named, particular content rather than a reskinnable
  placeholder.
- **Discoverable** - what it adds has to be noticed, investigated or searched for.
- **Interactive** - it gives players something to act on, not read-aloud.
- **Not overly generic** - its output could not be dropped unchanged into any fantasy
  dungeon.
- **Missing relevant features** - a feature clearly within its scope that it never draws.

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
a *mechanic* and belongs in `setting/Procedures.md`, or a *rule* and belongs in `STYLE.md`,
which already owns the two that are genuinely constant.

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
