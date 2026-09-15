# The pattern file spec

What every file in `patterns/*/*.md` is made of, and why. `README.md` says what the
patterns are *for* within the build; this file says what one looks like and how to tell a
correct one from a broken one. `CLAUDE.md` carries the short version.

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

## The four fields

Every file carries these, in this order. Nothing else is a section.

### `## Provides`
What exists after this file is read, in a sentence. Names the output, not the activity -
the test is whether a reader can tell what artifact or feature the file is responsible
for. Neutral and permanent.

It also carries the **boundary** against any sibling file that could be confused for this
one, and a pointer to the authority for anything adjacent that this file does not decide -
a rate that belongs to the drawing line, a resolution that belongs to
`setting/Procedures.md`, a citation format that belongs to `templates/Location.md`.

**It never says when or by what the file is reached.** That is the read-set graph's, and
the graph runs one way: a STEPS.md step names its template, a template names the pattern
files its artifact requires, and a Spec line names what it draws. A file restating where
it sits in that graph is a second copy of an edge something upstream already owns, and the
second copy is what drifts.

### `## Spec`
What this file decides, as a fenced block. Every line is one of exactly two things:

- **an edge** - it points to another pattern file, named in parentheses, which is the only
  other file that line requires; or
- **a question** - it states something the generator must answer, and cites nothing.

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
it; which files can make that claim is settled by what the file's output is, in "Which
files earn patterns" below. The files that carry one are exactly STEPS.md step 1b's compile list -
the two sets are checked against each other by `tools/validate_setting.py`.

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
cites the file; it does not carry that file's contract inline.

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
describes is never generated. `tools/validate_setting.py` warns on any file no generation
template reaches, and step 5b judges it.

**A file drawn two genuinely different ways is a signal, not a feature.** Two are:
`safe/People.md`, both a Kind where the location *is* a household and the mandatory person
in every SAFE location's gate block; and `dangerous/Key.md`, drawn as a Kind under
`dangerous/Treasure.md` for the key lying here and as a rated line on each weight file for
the lock a key elsewhere opens. Each is a candidate for being two files, and the second
already is: its demand end is moving out. Prefer splitting to carrying both.

### Which files earn patterns

**What the file's output is** answers this, and mode does not. A file that fills a
location's body - its Dressing, its Kind, an ingredient drawn into it, a hook hanging off
it - is where flat output would show, so that is where specific content is spent: those
files carry `## Design patterns`, and they are step 1b's compile list. A file that supplies
a *shape applied to* a location carries none, because a shape reads the same whatever
reference was chosen. Only two things are shapes: `Naming`, a procedure, and `Secrets`, a
Clue/Trigger/Payload discovery structure that can sit on top of any feature a location
already has.

**How a file is reached does not decide this**, and reasoning from it gets `Dressing` and
the four SAFE hooks wrong.

A rating classifier's own content is neutral by definition, so **no rating classifier
carries `## Design patterns`**, and neither does a `setting/` or `region/` file. Their
option menus answer a question rather than inject specificity, so they are Spec lines.

A **middle-tier** classifier is decided by body-versus-shape like anything else, and they
split both ways: one whose output is the dispatch, with the Kind beneath filling the body,
carries none; one that names what a hoard actually holds is filling the body itself, and
carries patterns. Being a classifier is not by itself the test. This is the library's most persistent drift: an option
menu reads like content, and filing it as compiled content licenses step 1b to rewrite it
for the next setting - an *edge* included.

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

The compile-list check holds STEPS.md and the tree to the same answer; it does not decide
the answer. Whether a given file *earns* patterns is the body-versus-shape judgement above
and stays a human call.

**Reachability is checked, and it is the one graph question worth a machine.** The
validator walks STEPS.md to `templates/` to each template's named pattern files and out
along Spec edges, and warns on anything it cannot reach. A phase-5 template is excluded
from the root set: a review pass cites pattern files as examples, and counting those would
let an orphan hide behind a mention in a judgement check. It warns rather than errors
because unreachable content cannot corrupt a build - it means content expected to be
generated silently is not, which is a thinness judgement and belongs to step 5b.

**Edges are read from the Spec's fenced blocks only.** The prose under the block cites
pattern files freely - `setting/Truths.md` names three - and counting those would make half
the leaves in the library read as classifiers.

`--read-set [STEP]` prints what any step reads, entry points separated from Spec expansion.
