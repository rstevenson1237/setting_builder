# The pattern file spec

What every file in `patterns/*/*.md` is made of, and why. `README.md` says what the
patterns are *for* within the build; this file says what one looks like and how to tell a
correct one from a broken one. `CLAUDE.md` carries the short version.

Status: the field model and the tier split below are settled and implemented. The **reach
mode** section is settled as a model but **not yet implemented** - the "Known divergences"
section at the end names exactly where the current files differ from it.

## The governing distinction

Two things are true of a pattern file's content, and they are independent:

- **Neutral and permanent** - true of this framework in any setting, any genre. Written
  once, never rewritten by a build.
- **Specific and compiled** - true of *this* setting only. Rewritten at STEPS.md step 1b
  from the chosen genre reference.

Almost every rule below follows from keeping those two apart. The generator answers
neutral questions; the specific content exists to stop those answers coming out flat. A
file that blurs the two cannot be recompiled for a new setting without hand-editing, which
is the failure this separation prevents.

**Prefer a question to a pattern wherever the verbiage can carry it.** Patterns are an
intentional, budgeted insertion of highly specific content, not the default home for
anything that happens to be a list. A question that can be stated neutrally belongs in
Design questions even when it reads like a menu.

## The five fields

Every file carries these, in this order. Nothing else is a section.

### `## Provides`
What exists after this file is read, in a sentence. Names the output, not the activity -
the test is whether a reader can tell what artifact or feature the file is responsible
for. Neutral and permanent.

### `## Read at`
When the file is reached, by which STEPS.md step, and **by what**. This is the coupling
record: for an element file it names the classifier and the spec line that draws it, and
for a classifier the step that reads it. It also carries the boundary against any sibling
file that could be confused for this one. Neutral and permanent.

The step ids here are validated against STEPS.md. `## Read at` is the only record of how a
file is reached, which is why it is prose that has to stay honest rather than decoration.

### `## Spec` *(classifiers only)*
The contract: which features the thing gets, and at what rate, as a fenced block. `1` is
mandatory; a percentage is the rate at which a feature carrying that content appears; a
file named in parentheses is the only other file that line requires. Neutral and
permanent.

### `## Design questions` *(elements only)*
The open-ended slots the generator must answer to fill the contract its classifier already
stated. Same fenced-block grammar as a Spec, and percentages are allowed - the difference
is not format but ownership: a Spec states a contract, Design questions fill one.
**Neutral and permanent** - step 1b never rewrites this section.

### `## Design patterns` *(either tier, but budgeted)*
The deliberate injection of highly specific content that keeps generated output from
reading flat. **Specific and compiled** - rewritten at step 1b from the chosen genre
reference. A section here is a claim that this file's output would be too generic without
it; see "Which files earn patterns" below.

### `## Constraints`
Every prohibition: what belongs in another file, what this file must never do, a named
failure mode. Blank when a file is created. Fills as the patterns are refined and negative
patterns are identified, and from failures observed during an actual build. Entries are
written generalized, never tied to the setting that produced them.

A positive rule phrased contrastively ("the pressure mechanism, not a rule of thumb") is
not a prohibition and stays where it is.

## The two tiers

A file's section names say which tier it is.

**Classifier** - states a contract, in a `## Spec`. One per thing generated:
`region/*`, `setting/*`, plus the location classes `dangerous/High|Medium|Low`,
`wild/Landmark|Hidden|Secret`, and `safe/Settlement`.

**Element** - fills a contract some classifier already stated, so it has no Spec of its
own and carries `## Design questions` instead. Everything else.

A contract lives in the file it describes. A classifier names a Kind or draws a feature
and cites the element file; it does not carry that element's contract inline. (It used to:
`wild/Landmark.md` held four KIND blocks and `dangerous/High.md` held the MYSTERY block,
which left five element files with no questions of their own.)

`patterns/setting/Genre.md` is in neither tier. It is an interactive elicitation procedure
and its extra sections are that procedure.

## Reach modes

Every element file is reached in exactly one of four modes, and the mode is what a
classifier's spec line already encodes. Mode predicts what a file needs.

| mode | reached | example |
|---|---|---|
| **second pass** | every output, unconditionally, after the fact | `Dressing`, `Secrets`, `Naming` |
| **kind** | exactly one of N, mutually exclusive | `safe/Commerce.md`, `wild/Ruin.md` |
| **ingredient** | drawn at a stated rate | `Creature`, `Trap`, `Treasure`, `Mystery`, `Lore`, `Key`, `Quest` |
| **conditional** | triggered by content already generated | `Faction` |

**Every element file is reached by a classifier, in the mode it claims.** A file reachable
only through its own `## Read at`, or only from inside another element file, is orphaned
from the spec graph: nothing draws it, so nothing guarantees it is ever read.

### Which files earn patterns

Mode answers this. **Kind** and **ingredient** files fill a location's body and are where
flatness shows, so they are where specific content is spent. **Second pass** and
**conditional** files are mostly structural - a Clue/Trigger/Payload shape, a naming
procedure - and a `## Design patterns` section in one is a claim that needs justifying.
`Dressing` is the standing exception: it is second pass and genuinely needs both.

A classifier's own content is neutral by definition, so a classifier carrying
`## Design patterns` is worth a second look - its option menus are usually answering a
question rather than injecting specificity.

## Citation format

A citation from one `patterns/*/*.md` file to another is always `folder/File.md`, bare,
with no `patterns/` prefix - except a reference to a `patterns/setting/*.md` file, which
always keeps the prefix, since a bare `setting/File.md` means the *generated* file of that
name rather than the pattern that produces it.

## What the validator enforces

Today: citation format; the five fields present per tier; a classifier carrying no
`## Design questions` and an element carrying no `## Spec`; `## Read at` step ids resolving
against STEPS.md.

Proposed, once reach modes are implemented: that every element file is reached by some
classifier in the mode it claims, which turns the orphans below into errors rather than
silence.

## Known divergences

Real, current, and deliberately not yet fixed:

1. **Four orphaned element files.** `safe/Naming.md` and `wild/Naming.md` say "for every
   location, after Dressing" but no `safe/` or `wild/` classifier cites them - only the
   three `dangerous/` classifiers cite their Naming file. `dangerous/Faction.md` and
   `wild/Faction.md` are cited by no classifier at all; `wild/Faction.md` is reached only
   from inside `wild/Ruin.md`, another element.
2. **Twenty classifiers carry `## Design patterns`**, sixteen of them `setting/*`. Their
   content is neutral option menus - `setting/Keys.md`'s "Forms", `setting/Truths.md`'s
   "Kinds of truth" - which by the neutrality test are Design questions, not patterns.
3. **STEPS.md step 1b's compile list names 18 files** but says "every other tier-2 element
   file". Twenty-one element files carrying patterns are not on the list. Splitting them
   by reach mode is what decides which belong there - not all of them do.

Resolving 2 and 3 changes what step 1b rewrites, so they are held together rather than
fixed piecemeal.
