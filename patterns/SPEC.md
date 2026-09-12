# The pattern file spec

What every file in `patterns/*/*.md` is made of, and why. `README.md` says what the
patterns are *for* within the build; this file says what one looks like and how to tell a
correct one from a broken one. `CLAUDE.md` carries the short version.

Status: the field model and the tier split below are settled and implemented, and so is
the one consequence of reach mode that had teeth - which files carry `## Design patterns`.
The modes themselves are still a reading of the spec lines rather than something the files
declare; the "Known divergences" section at the end says what that leaves open.

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
it; which files can make that claim is settled by reach mode, in "Which files earn
patterns" below. Thirty-three files carry one, and they are exactly STEPS.md step 1b's
compile list - the two sets are checked against each other by
`tools/validate_setting.py`.

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

How a file is arrived at. Every file **declares its mode**, as the first thing in its
`## Read at`: `**Mode: ingredient.**`. Four modes are drawn by another file's Spec, and
`entry` is the fifth - a file a STEPS.md step reads directly, which nothing draws. The
declaration is validated, so what a file claims and what the graph does cannot drift apart
silently.

| mode | reached | example |
|---|---|---|
| **entry** | read directly by a STEPS.md step; nothing draws it | every `setting/` and `region/` file, and the rating classifiers |
| **second pass** | every output, unconditionally, after the fact | `Dressing`, `Secrets`, `Naming` |
| **kind** | exactly one of N, mutually exclusive | `safe/Commerce.md`, `wild/Ruin.md`, `dangerous/Trap.md`, and WILD's and DANGEROUS's `Lore` and `Key` under `Treasure`'s "what it is" |
| **ingredient** | drawn at a stated rate | `Creature`, `Hazard`, `Treasure`, `Mystery`, `Quest`, and SAFE's `Lore`, `Key`, `Quest` and `Faction` hooks |
| **conditional** | triggered by content already generated | `wild/Faction.md` |

`Faction` is the one name that means a different mode in each rating, and reading it as one
thing is a mistake this table used to make: `safe/Faction.md` is one of four hooks in
`safe/Settlement.md`'s registry line, so it is an ingredient exactly like its three
siblings; `dangerous/Faction.md` is a Kind of `dangerous/Encounter.md`; only
`wild/Faction.md` is conditional, drawn from inside each of the four WILD kind files at a
rate the Kind sets, because whether a faction is possible here depends on what the place
already turned out to be.

**Every element file is reached by a classifier, in the mode it claims.** A file reachable
only through its own `## Read at`, or only from inside another element file, is orphaned
from the spec graph: nothing draws it, so nothing guarantees it is ever read. A file
declaring any of the four drawn modes and cited by nobody's Spec is now an error, which is
what keeps the four orphans two passes closed - `safe/Naming.md`, `wild/Naming.md`,
`wild/Faction.md` and `dangerous/Faction.md` - from silently reopening.

**A file may declare two modes, and two do.** "Exactly one of four" was the original claim
and it is not true of the library: `safe/People.md` is both a Kind, where the location *is*
a household, and the mandatory person in every SAFE location's gate block; `dangerous/Key.md`
is drawn from both ends, as a Kind under `dangerous/Treasure.md` for the key lying here and
as a rated line on each weight file for the lock that a key elsewhere opens. Both declare
`kind, ingredient`. Declare two only where the draws are genuinely different in kind and
both primary - an extra rated draw on top of a primary one (`wild/Naming.md`'s second name
in an older tongue) is prose in `## Read at`, not a second mode.

**Edges are read from the Spec's fenced blocks only.** The prose under the block cites
pattern files freely - `setting/Truths.md` names three - and counting those would make half
the leaves in the library read as classifiers.

### Which files earn patterns

**What the file's output is** answers this, and mode does not. A file that fills a
location's body - its Dressing, its Kind, an ingredient drawn into it, a hook hanging off
it - is where flat output would show, so that is where specific content is spent: those
files carry `## Design patterns`, and they are step 1b's compile list. A file that supplies
a *shape applied to* a location carries none, because a shape reads the same whatever
reference was chosen. Only two things are shapes: `Naming`, a procedure, and `Secrets`, a
Clue/Trigger/Payload discovery structure that can sit on top of any feature a location
already has.

Mode was tried as the test here and does not survive contact with the files. It predicted
that second-pass and conditional files carry no patterns, which forced `Dressing` to be
named a standing exception - and an exception that exists only to save a rule is a sign the
rule is cutting in the wrong place. It also split the four files drawn by
`safe/Settlement.md`'s single hook line three-to-one, stripping `safe/Faction.md` while its
identically-drawn siblings kept theirs. Body-versus-shape gets `Dressing` right with no
exception and all four hooks right together. Mode stays, because how a file is reached is
real coupling information worth declaring - it just does not decide this.

A classifier's own content is neutral by definition, so **no classifier carries
`## Design patterns`** - not a rating classifier, not a middle-tier one, and not a
`setting/` or `region/` file. Their option menus answer a question rather than inject
specificity, so they are Spec lines. This was the library's most persistent drift: an
option menu reads like content, and filing it as compiled content means step 1b is
licensed to rewrite it for the next setting - including, in one case caught during the
WILD restructure, rewriting an *edge* away.

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
resolving against STEPS.md; a valid `**Mode:**` declaration opening every `## Read at`, and
every file claiming a drawn mode actually drawn by some other file's Spec; and step 1b's
compile list against the set of files carrying
`## Design patterns`, in both directions - a listed file with no section to compile into,
and a file carrying one that no step recompiles, are both errors.

That last check holds STEPS.md and the tree to the same answer; it does not decide the
answer. Whether a given file *earns* patterns is the reach-mode judgement above and stays
a human call.

Still proposed: checking that a file is drawn *in the mode it claims*, not merely drawn at
all. That needs the drawing line's own shape read - a `{a | b | c}` choice for a kind, a
rate for an ingredient - and the fenced blocks carry enough false positives (a rate table
naming a classifier it explicitly does *not* draw, in `dangerous/Secrets.md`) that it would
want a pass of its own.

## Known divergences

Real, current, and deliberately not yet fixed:

1. **A declared mode is checked for being drawn, not for being drawn that way.** Every
   file states its mode and the orphan check is live, but nothing yet verifies that a file
   claiming `kind` is drawn by a choice line rather than a rate. See "What the validator
   enforces" above for why that wants its own pass.

The two divergences about `## Design patterns` that this section used to carry are closed:
twenty-eight files' neutral option menus moved into their Specs, and step 1b's compile list
was rewritten from the reach-mode split and is now validated.

The orphaned element files this section used to list are closed. `safe/Naming.md` and
`wild/Naming.md` are drawn as the last line of their classifiers, `wild/Faction.md` by a
Spec line in each of the four WILD kind files, and `dangerous/Faction.md` by
`dangerous/Encounter.md`.
