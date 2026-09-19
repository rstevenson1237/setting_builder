# Feedback

The intake for every reaction to generated content - the user's, a judgement check's, a
playtest's, or a reading of the corpus. **Classify before editing anything.** An item names
a failure. What it does not name is which file should have prevented it, and choosing that
file is what this procedure does.

The routes are tried in order, and the first one that can carry the item is the one taken.
The order is cost, not priority. R1 changes one entry. R2 widens what a draw can land on,
and every later draw is wider for it. A rule can only narrow, it is charged against every
build that would have been fine without it, and it is charged in a context window that is
read at every step. So the rule routes are last, and taking one is an admission that
nothing below could hold the item.

## The routes

**R1 Content.** The item is about one location, one field, one entry. Fix it in `setting/`
and change nothing else. The test is whether the same observation would be true of the next
location generated: where it would not, the item ends here. Most items are R1.

**R2 List.** The output was the average - a door that is a door, a container that is "a
chest", a demeanour anyone would have written. The draw landed where every draw lands,
because the list behind that Spec line is short or crowded at one end. Add entries to the
list the line draws from: `genre/<pack>/lists/<name>.md` once P3.1 has moved them, and
until then the `## Design patterns` section of the pattern file whose Spec line drew the
field. Entries are written generalized, per `patterns/SPEC.md`, and enough of them go in
that the crowded end is no longer where the draw falls. **This is the route most items
past R1 belong on.**

**R3 Exemplar.** The item is about how a line reads, and no list is the problem: the shape
it wants is shown nowhere. Edit the entry in `style/exemplars/` that should have shown it,
or add one - `style/exemplars/README.md` holds what the set covers. An exemplar is read at
generation and checked on every run, so it carries where a sentence about the same shape
does not.

**R4 Tell.** A class of failure that recurs and has a textual signature. One line in
`style/tells.txt` and one known-bad entry under `fixtures/bad/` the line fires on, plus the
near miss under `fixtures/good/` where the signature is loose enough to need one. A tell
buys a measurement, not a prohibition - it reports a candidate and never an error, per
`STYLE.md` - which is why it sits above both rule routes.

**R5 Rule.** A class with no signature and no list behind it. One sentence in `STYLE.md`,
or one `GENRE.md` standing consequence, and only where the item names the
`templates/*_Judgement_Check.md` item that will look for it. A rule nothing reads back is a
preference. Consequences are capped at twelve: at the cap, merge two before adding one.

**R6 Constraint.** The item is about one pattern file's output and no other. One entry in
that file's `## Constraints`, to `patterns/SPEC.md`'s rules. Last resort. Every route above
points a draw somewhere; a Constraint closes a pathway for every build this framework will
ever run, including the ones where that pathway was the right one.

**R7 Rules project.** A mechanic the citation grammar cannot cite. Log it and stop. The
rules are not in this tree, `templates/` owns how a line cites them, and a mechanic that
has no citation is owed to the rules document instead of to a file here.

**R0 Playtest.** An observation from the table. Logged as a line and left there until
`checks/Playtest.md` exists. It becomes an item on the second session that reports it, or
on a re-read that finds the chain it describes actually broken. One table on one night is a
sample of one.

### The toll on a rule

R5 and R6 are taken only after the routes above have been tried, and the log entry names
what was tried: the list entry, the exemplar, or the tell that went in first. An entry
naming none of them is a rule written against a single output.

### What is not an item

A boundary between two pattern files - what belongs in the sibling, which file owns a kind
- is authored with the file and stays out of this log. It arrives by reading the tree, not
by reading output, and `patterns/SPEC.md` already decides where it lives.

## The log

One line per item: the date, the item in the words it arrived in, the route, and the commit
that lands it. An unstruck line is owed. Strike it in the commit that lands it and leave it
struck, because the struck line is what says which route a rule came from when the rule is
next questioned.

Format: `` `date` - "the item" - route - `commit` ``. Items arriving together are
classified in one table instead, as the worked example below is.

### Retro-classified, as the worked example

The rule additions in the three pull requests before this file predate the routes. Each
item is stated as the pull request recorded it; none arrived in writing, so none is a
quote.

| Item | Route | Where it landed |
| --- | --- | --- |
| The model wrote the average door - "a door" | R2 | `d15f10e` - material and opening lists, plus a Constraint the lists make redundant |
| The average container - "a chest" | R2 | `d15f10e` - a named-object Spec line, plus a Constraint |
| The average swarm, given a countable number | R2 | `d15f10e` - a Shape menu with per-shape tells, plus a Constraint |
| Region-scale terrain invented for one room | R2 | `d15f10e` - a Kind menu drawn against the region, plus a Constraint |
| A gate or a fixture with nothing to draw from | R2 | `d15f10e` - the gate and fixture menus, correctly |
| A Feature drawn from a mechanism file had no lexicon and described itself in a relative clause | R2 | `ae492fa` - vocabulary lists in Trap, Door, Residual, Environmental, correctly |
| A trailing clause in 70% of Features, "rather than" in 61 of 206 | R4 | `ae492fa` - a closed punctuation grammar and a mechanical check; the signature was computed by hand and nothing kept computing it |
| A specialist term followed by its own gloss | R4 then R5 | `ae492fa` - one sentence in instruction 5, naming the judgement-check item; the toll was paid |
| Claims nobody at the table could witness | R5 | `ae492fa` - one consequence, naming the two check rows; the toll was paid |
| A hazard's cost was fiction, with nothing rolled | R7 | `a239d81` - a notation in `templates/` and `setting/Procedures.md` instead |
| One hazard written as two Features | R6 | `a239d81` - correctly |
| "Never write what the fixture is for above the details it is reasoned from" | none | `d15f10e` - `GENRE.md`'s third test, restated one file down; a cut candidate for P2.3 |

Six of the twelve land on R2, and four of those six landed as a list **and** a prohibition
against the average the list had just made unlikely. Three findings the classification
turned up:

- **Most of `d15f10e`'s twenty-one Constraints are not items at all.** Fourteen state a
  boundary against a sibling file - a fall that has finished is Dressing, a growth that
  acts is a creature - and were authored with the file. They never came through this door.
- **R7 is a route the framework has not taken.** `a239d81` read as feedback about a
  mechanic and was answered with a notation, a Conditions list, and a format check in this
  tree. It stands as a test case the rules may absorb, not as a precedent.
- **The toll was paid twice.** Two rule additions named the judgement-check item that would
  read them back - the gloss and the unwitnessable claim - and both are in `ae492fa`, the
  last of the three.
