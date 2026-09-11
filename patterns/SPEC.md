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
anything that happens to be a list. A question that can be stated neutrally belongs in the
Spec even when it reads like a menu.

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

### `## Spec`
What this file decides, as a fenced block. Every line is one of exactly two things:

- **an edge** - it points to another pattern file, named in parentheses, which is the only
  other file that line requires; or
- **a question** - it states something the generator must answer, and cites nothing.

`1` is mandatory; a percentage is the rate at which a feature carrying that content
appears. Neutral and permanent - step 1b never rewrites a Spec.

That two-way rule is what makes the library a single tree. A file whose Spec has outgoing
edges is a classifier; a file whose Spec is all questions is a leaf. Neither is declared
anywhere - it is read off the citations, so it cannot fall out of step with itself.

**Where a line lives** follows from whether it varies: a line that differs between the
classes that draw it belongs in the drawing class's Spec, and a line that is the same for
all of them belongs in the file it cites. (`dangerous/High.md` requires an architecture
detail because HIGH announces itself, so that line is HIGH's; `dangerous/Dressing.md`'s
five baseline lines are constant, so they are Dressing's.) This is the same test
`setting/Procedures.md` applies one level up.

### `## Design patterns` *(optional, and budgeted)*
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

## Classifiers and leaves

A file's Spec says which it is, without asserting anything: outgoing edges make it a
**classifier**, an all-questions Spec makes it a **leaf**. Depth is a fact about the tree,
not a property a file declares.

A contract lives in the file it describes. A classifier names a Kind or draws a feature and
cites the file; it does not carry that file's contract inline. (It used to:
`wild/Landmark.md` held four KIND blocks and `dangerous/High.md` held the MYSTERY block,
which left five files with no Spec of their own.)

A classifier may cite a file that is itself a classifier - `Encounter` drawing
`{creature | named creature | faction}`, `Hazard` drawing a mechanism - which is how a
category earns a middle level instead of being a rename. A middle file is worth adding only
when the kind beneath it is a real choice of two or more.

`patterns/setting/Genre.md` carries extra sections beyond the skeleton. It is an
interactive elicitation procedure and those sections are that procedure.

## The blocks a classifier's Spec is grouped into

A classifier states its lines under named blocks, and the blocks answer the same four
questions in every rating:

| block | asks |
|---|---|
| **substrate** | what this place is |
| **challenge** | what stands between the party and what they want |
| **reward** | what is here to take |
| **registry** | what ties this place to somewhere else, in either direction |

The point of the blocks is that a line failing to belong to any of them is almost always a
line belonging to a different class - which is a test that runs while the Spec is being
written, not afterwards.

Each rating fills the four its own way, and one adds a fifth:

- **DANGEROUS** is the plain case: challenge is what opposes the party, reward what is in
  the room.
- **WILD** adds **access**, between substrate and challenge. At depth, how a room is
  reached is the connection graph, written at 4b and needing no words in the entry; out in
  the country it is content, written into the parent's Features, and it is the whole
  distinction between Landmark, Hidden and Secret.
- **SAFE** has no challenge - a settlement opposes nobody - and a **gate** in the same
  slot: the person standing between the party and what this place has, and their terms.
  Its reward block is a **transaction**: what is obtainable here and what is not.

A rating renaming or adding a block is a claim that the rating genuinely works differently,
and the classifier says why in the prose under its Spec. A rating *dropping* one is a
different matter: `dangerous/Low.md` carries a challenge block that says "none", and the
reason, rather than omitting the heading, because the absence is the class's defining fact.

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

## What a spec line owes

A spec line says which feature appears and at what rate. What it does **not** say, and
must not, is how many words the generated feature gets.

**The unit of generated content is the Feature, not the word.** A drawn element's contract
is satisfied across as many Features as it takes: where a contract line names something the
players can address as its own object - looked at, acted on, taken, fought, opened - that
line becomes its own Feature. Treasure hidden in a pillar and guarded by a beast is three
Features, not one complex one. A contract line that only *qualifies* another thing - its
condition, its position, how it is reached - stays on that thing's line.

This is what keeps entries terse without a cap. One Feature states one thing, so it is
naturally short; the generator never has to compress a complex feature into a word count
that cannot hold it, and never has connective prose to write, because Features are listed
rather than joined. An entry's length is therefore the number of Features the classifier
drew - a decision already made, in the Spec - and not a budget anyone sets afterwards.

Corollaries:

- **Never fill a gap with prose.** Every clause traces to a drawn contract line. A clause
  with no line behind it is cut, which is a structural test rather than a stylistic one.
- **Complexity decomposes, it does not expand.** A feature that will not fit a short line
  is usually several features.
- **Word counts are diagnostic at most.** An over-long Feature means something is being
  explained rather than stated; an over-long entry means too many Features were drawn,
  which is the classifier's problem and not the line's.

Hard word ceilings were tried and removed. `templates/Location.md` carried a per-Feature
cap keyed to position - 15 words for the first Feature, 8-12 for the rest - which measured
prominence while the thing that actually varies is complexity: contracts run from two
mandatory lines (`wild/Quest.md`) to six (`wild/Mystery.md`), and both got the same
allowance. `safe/Dressing.md` and `wild/Dressing.md` carried whole-entry word budgets that
were, by their own admission, provisional figures carried across by analogy from a
DANGEROUS calibration that is not recorded anywhere - and `dangerous/Dressing.md`, the
rating they were taken from, carries no budget at all. Decomposition does the work all
three were standing in for.

## Citation format

A citation from one `patterns/*/*.md` file to another is always `folder/File.md`, bare,
with no `patterns/` prefix - except a reference to a `patterns/setting/*.md` file, which
always keeps the prefix, since a bare `setting/File.md` means the *generated* file of that
name rather than the pattern that produces it.

## What the validator enforces

Today: citation format; `## Provides`, `## Read at`, `## Spec` and `## Constraints`
present on every file; no leftover `## Design questions` heading; `## Read at` step ids
resolving against STEPS.md.

Proposed, once reach modes are implemented: that every element file is reached by some
classifier in the mode it claims, which turns the orphans below into errors rather than
silence.

## Known divergences

Real, current, and deliberately not yet fixed:

1. **Twenty classifiers carry `## Design patterns`**, sixteen of them `setting/*`. Their
   content is neutral option menus - `setting/Keys.md`'s "Forms", `setting/Truths.md`'s
   "Kinds of truth" - which by the neutrality test are Spec questions, not patterns.
2. **STEPS.md step 1b's compile list names 18 files** but says "every other tier-2 element
   file". Twenty-one element files carrying patterns are not on the list. Splitting them
   by reach mode is what decides which belong there - not all of them do.

Both change what step 1b rewrites, so they are held together rather than fixed piecemeal.

The orphaned element files this section used to list are closed. `safe/Naming.md` and
`wild/Naming.md` are drawn as the last line of their classifiers, `wild/Faction.md` by a
Spec line in each of the four WILD kind files, and `dangerous/Faction.md` by
`dangerous/Encounter.md`.
