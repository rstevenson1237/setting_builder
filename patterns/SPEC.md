# The pattern file spec

What every file in `patterns/` is made of, and how to tell a correct one from a broken
one. `CLAUDE.md` carries the short version.

**This file is a standard, not an input.** No generation step reads it: a pattern file has
to be followable on its own, from its own notation - rates in the left margin, `{…}` for a
draw, `(folder/File.md)` for an edge, a block name in capitals for a block further down
the same file. This file is what the library is tested against, by
`tools/validate_setting.py` and at STEPS.md step 5b.

## The division of labour

A **pattern** generates. A **template** frames: it names what is read before generating
(its Context), how many units the artifact holds and how they are spread (its
Instructions), and the exact shape the output is cut down to (its Template block).

So a pattern file specifies **one unit** - one entry, one event, one location - and never
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
topic.** "Condition" alone invites a generic answer; `Condition, stated before Purpose -
how far the room sits from still in use to gone` names the axis, and the draw beside it,
`{active | abandoned | decayed | ruined | destroyed}`, marks five points on it. Both are as
true of any setting as "size and shape" is - which is what keeps them a question and a
draw rather than an example. Where a field still reads thin once its axis is named,
the fix is a sharper question, never a list of instances to draw from.

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
all of them belongs in the file it cites. (`dangerous/High.md` requires an architecture
detail because HIGH announces itself, so that line is HIGH's; `dangerous/Dressing.md`'s
five baseline lines are constant, so they are Dressing's.) This is the same test
`setting/Procedures.md` applies one level up.

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

A classifier may cite a file that is itself a classifier - `Encounter` drawing
`{creature | named creature | faction}`, `Hazard` drawing a mechanism - which is how a
category earns a middle level instead of being a rename. A middle file is worth adding only
when the kind beneath it is a real choice of two or more.

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
  reached is the connection graph, written at 4c and needing no words in the entry; out in
  the country it is content, written into the parent's Features, and it is the whole
  distinction between Landmark, Hidden and Secret.
- **SAFE** has no challenge - a settlement opposes nobody - and a **gate** in the same
  slot: the person standing between the party and what this place has, and their terms.
  Its reward block is a **transaction**: what is obtainable here and what is not.

A rating renaming or adding a block is a claim that the rating genuinely works differently,
and the classifier says why in the prose under its Spec. A rating *dropping* one is a
different matter: `dangerous/Low.md` carries a challenge block that says "none", and the
reason, rather than omitting the heading, because the absence is the class's defining fact.

## How a Spec becomes tables

A region's content is held as tables before it is written as locations, and the tables are
read off the Spec, never designed beside it. Three rules place everything:

1. **A line that is not an edge is a column** - a question, a draw, or a sub-line nested
   under another line - of the table of the file it is written in. A draw's cell is the
   item drawn; a question's is the answer; a rated line not taken is `none`.
2. **A pattern file is exactly one table**, in exactly one file, holding a row for each
   unit that drew it. A file drawn as a kind holds rows only for the units that picked it.
3. **A table's file is the block of the class-file line it descends from**: substrate,
   gate and transaction go to the location table; challenge, reward and registry each to
   their own file; and anything on an edge, being shared by two locations, to the exits
   file. The file names and their columns' shape are the templates'.

**One unit, one home.** A file reached from more than one line lives where its first draw
puts it - the shallowest, then the topmost line of the class file - and every other drawer
names its row. A file drawn from two homes at once is two files, or one of its draws is
really a value and becomes a line.

**Every line opens with its column label**: a word or two before ` - `, unique within its
table and among the tables its rows join - a kind's table and its classifier's, or any
table keyed by the same location. **A line answered by more than one value is more than
one line**: where a single draw item or a short phrase cannot answer it, it is asking
several things, and splits - most often a draw that also asks for the thing it
categorises, which is a tag column and a gloss column. **A line with nothing to answer is
not a Spec line**: a rule about another line belongs on that line, in Constraints, or in
Provides.

**Kinds fold into their classifier only when they answer the same lines.** Kind files
become one table - items of a draw on the classifier - when the union of their lines
leaves no kind with a column it never asks. A `none` from a rate is fine; a `none` because
a kind has no such question means the kinds are different units and stay separate files.

## How a file is reached

Read off the graph, never declared. Five shapes recur often enough to be worth naming, and
the names are a way of talking about a file rather than anything a file states about
itself:

| shape | reached |
|---|---|
| **entry** | named by a template, so a STEPS.md step reads it directly |
| **second pass** | every output, unconditionally, after the fact |
| **kind** | exactly one of N, mutually exclusive |
| **ingredient** | drawn at a stated rate |
| **conditional** | triggered by content already generated |

Nothing validates these, because nothing can: `kind` and `ingredient` are not separable by
line shape. `wild/Hidden.md` draws `1 Kind {ruin | lair | natural feature}` and
`dangerous/High.md` draws `1 Challenge {encounter | hazard | mystery}` - identical shape,
three alternatives, three citations - and the first draws three kinds while the second
draws three ingredients. The difference is that a Kind decides what the location *is* and a
challenge is something *in* it, which is semantic and not on the line. Any check would be
checking a label against itself, and the generator branches on the drawing Spec line
regardless.

`Faction` is the one name that means a different mode in each rating, and must not be read
as one thing: `safe/Faction.md` is one of four hooks in
`safe/Settlement.md`'s registry line, so it is an ingredient exactly like its three
siblings; `dangerous/Faction.md` is a Kind of `dangerous/Encounter.md`; only
`wild/Faction.md` is conditional, drawn from inside each of the four WILD kind files at a
rate the Kind sets, because whether a faction is possible here depends on what the place
already turned out to be.

**Every element file is reached by a classifier.** One reachable only from inside another
element file is orphaned: nothing draws it, so nothing reads it, and the content it
describes is never generated. `tools/validate_setting.py` warns on it, and step 5b judges it.

**A file drawn two genuinely different ways is a signal, not a feature.** Prefer
splitting it to carrying both, by **How a Spec becomes tables**' one-home rule.

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

**No hard word ceiling, anywhere.** A per-Feature cap measures prominence, while the
thing that actually varies is complexity - contracts run from two mandatory lines
(`wild/Quest.md`) to six (`wild/Mystery.md`). Decomposition does the work a cap would be
standing in for.

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
