# The pattern file spec

What every pattern file in `patterns/` is made of, and how to tell a correct one from a
broken one. `patterns/Schema.md` is not a pattern file: it is what every location table is
checked against, and nothing here governs it.

**This file is a standard, not an input.** No generation step reads it: a pattern file has
to be followable on its own, from its own notation - rates in the left margin, `{…}` for a
draw, `(folder/File.md)` for an edge, a block name in capitals for a block further down
the same file. This file is what the library is tested against, by
`tools/validate_setting.py` and at STEPS.md step 5b.

## The division of labour

A **pattern** generates. A **template** frames: it names what is read before generating
(its Context), how many units the artifact holds and how they are spread (its
Instructions), and the exact shape the output is cut down to (its Template block).

So a pattern file specifies **one unit** - one entry, one event - and never
how many of them a file holds or in what mix. A count, a distribution or a coverage list
in a pattern file is the template's; per-unit content in a template is the pattern's.

## The root

The library is one tree, rooted at `patterns/Genre.md`. Its GENRE block is the set of
questions `GENRE.md` answers; its other blocks are edges to every file a build enters
from. A template names the node its step expands, and that node must be reachable from the
root.

## The governing rule

Everything in a pattern file is **neutral and permanent** - true of this framework in any
setting, any genre, written once and never rewritten by a build. There is no second,
compiled channel for specificity: a field that would otherwise read flat earns its
precision from how the question itself is written, not from a worked example attached to
it.

**A question earns the line by naming the axis an answer has to move along, not just the
topic.** Where a field still reads thin once its axis is named, the fix is a sharper
question, never a list of instances to draw from.

**Question or draw is a design decision, made per line.** A question produces the answer
that best fits everything already in context - the average, done well. A draw forces the
answer into a set chosen for being worth meeting, at the cost of fit. Reach for a draw
where questions alone have been seen to produce the plain case every time.

**A draw is not a list of instances.** A draw's items are the whole set of categories an
answer may fall in, closed and exhaustive; a list of instances is a sample of answers,
which the generator copies. An item may carry a **definition** - what the category is - or
a **condition** - when it is the right pick. It never carries an **example** - a member of
the category - because an example is an instance with a label on it.

## The three fields

Every file carries these, in this order. Nothing else is a section.

### `## Provides`
What exists after this file is read, in a sentence. Names the output, not the activity -
the test is whether a reader can tell what artifact or feature the file is responsible
for. Neutral and permanent.

It also carries the **boundary** against any sibling file that could be confused for this
one, and a pointer to the authority for anything adjacent that this file does not decide -
a rate that belongs to the drawing line, a resolution that belongs to
`setting/Procedures.md`, a citation format that belongs to `templates/region/Location.md`.

**It never says when or by what the file is reached.** That is the read-set graph's, and
the graph runs one way: a STEPS.md step names its template, a template names the pattern
files its artifact requires, and a Spec line names what it draws. A file restating where
it sits in that graph is a second copy of an edge something upstream already owns, and the
second copy is what drifts.

### `## Spec`
What this file decides, as a fenced block. Every line is one of exactly three things:

- **an edge** - it points to another pattern file, named in parentheses, which is the only
  other file that line requires;
- **a question** - it states something the generator must answer, and cites nothing; or
- **a draw** - it names a closed set and the generator selects from it: exactly one
  unless the line says otherwise, at the rates the line gives where it gives any. A short
  set sits inline, `{a | b | c}`. A long one, or one whose items need definitions, is named
  on the line in capitals, `{TYPE}`, and listed as its own fenced block of that name
  further down the same Spec, one item per line: `item - definition or condition`.

**A draw or an edge is decided by what the pick opens.** Where picking an item only sets
a value - nothing else in the unit changes shape - it is a draw, and its items live in
this file. Where picking an item opens lines of its own to answer, each item is a unit and
gets a file, and the line is an edge: the parentheses go on the line, one file per item.

There is no fourth form. A list trailing a line without braces is either meant to be
exhaustive, and is a draw, or illustrates, and is cut in favour of a sharper question.

**What makes a citation an edge is that the generator must go and read that file.**
Anything already in context at this step is not an edge and takes no parentheses: state it
as part of the question, naming the generated artifact it is actually read from (`from
setting/Bestiary.md`) rather than the pattern that produced it. A Dressing line the
classifier already drew one level up, an event already written into `setting/History.md`,
the register a line files its stub in - all questions. A decorative citation is not
harmless: it makes a leaf read as a classifier.

**And the converse: an edge belongs in the fenced block.** Edges are read from the block
only, so a draw stated in the prose underneath is invisible to the tree even when both
ends know about it. If a line requires another pattern file, the parentheses go on the
line.

`1` is mandatory; a percentage is the rate at which a feature carrying that content
appears. Neutral and permanent.

That two-way rule is what makes the library a single tree. A file whose Spec has outgoing
edges is a classifier; a file whose Spec is all questions and draws is a leaf. Neither is declared
anywhere - it is read off the citations, so it cannot fall out of step with itself.

**Where a line lives** follows from whether it varies: a line that differs between the
classes that draw it belongs in the drawing class's Spec, and a line that is the same for
all of them belongs in the file it cites.

### `## Constraints`
Every prohibition: what belongs in another file, what this file must never do, a named
failure mode. Blank when a file is created. Fills as the patterns are refined and negative
patterns are identified, and from failures observed during an actual build. Entries are
written generalized, never tied to the setting that produced them.

A positive rule phrased contrastively ("the pressure mechanism, not a rule of thumb") is
not a prohibition and stays where it is.

## Classifiers and leaves

A file's Spec says which it is, without asserting anything: outgoing edges make it a
**classifier**, a Spec of questions and draws only makes it a **leaf**. Depth is a fact about the tree,
not a property a file declares.

A contract lives in the file it describes. A classifier names a Kind or draws a feature and
cites the file; it does not carry that file's contract inline.

A classifier may cite a file that is itself a classifier, which is how a category earns a
middle level instead of being a rename. A middle file is worth adding only
when the kind beneath it is a real choice of two or more.

## What prose owes

Prose in any field points to where something is. It never restates what is there.

- **Never state a count that can be derived from a list.** Name the list.
- **Never enumerate the files** that carry a line or a section. The tree carries
  that, `tools/validate_setting.py` computes it, and the pattern reference renders it.
- **Never restate a rule another file owns.** Cite it.
- **Never restate the fenced block** in the prose beneath it. The block is the contract.

Every copy drifts from its original, and the copy is the one a reader trusts, because it
is the one in front of them. `tools/validate_setting.py` warns when a sentence of nine
words or more appears in three or more files.

## Citation format

A citation from one `patterns/*/*.md` file to another is always `folder/File.md`, bare,
with no `patterns/` prefix - except a reference to a `patterns/setting/*.md` file, which
always keeps the prefix, since a bare `setting/File.md` means the *generated* file of that
name rather than the pattern that produces it.

## What the validator enforces

Run `python3 tools/validate_setting.py` to see it; the script is the list. This section
states only what the checks *mean*, which is not readable off them.

**Reachability is checked, and it is the one graph question worth a machine.** The
validator walks Spec edges out from `patterns/Genre.md` and warns on anything the root
cannot reach, and separately on anything no generation template enters. A phase-5 template
is not a generation template: a review pass cites pattern files as examples, and counting
those would let an orphan hide behind a mention in a judgement check. It warns rather than errors
because unreachable content cannot corrupt a build - it means content expected to be
generated silently is not, which is a thinness judgement and belongs to step 5b.

**Edges are read from the Spec's fenced blocks only.** The prose under the block cites
pattern files freely - `setting/Truths.md` names three - and counting those would make half
the leaves in the library read as classifiers.

`--read-set [STEP]` prints what any step reads, entry points separated from Spec expansion.
