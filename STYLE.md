# Style

The positive target: what a line in this repository should *read* like. `GENRE.md`'s three
tests outrank this file and decide whether a line lives at all; this file decides how the
surviving line is written. `templates/` owns the shape a referee sees - the header, the
labels, the tables, the citation forms - and this file owns the sentences inside it.

**Re-read this at every generation step, beside `GENRE.md`.**

## The four sources

Three published modules and one endorsed output. Each contributes a shape, never its wording.

- **The Hole in the Oak** - the branch form. A bold label, then each branch as its own short
  sentence: `Pried: the grate lifts free. Struck: the frame splits and the shaft floods.`
  Two branches are two sentences, never one comma-welded clause.
- **Arden Vul** - the cross-reference. An entry names another location by its code and a
  registry entry by its name, and stops. What a thing means, what it opens and what it is
  worth sit where they are defined, so the room stays a container.
- **B4 The Lost City** - the referee's voice on the page. Room name, a line of dimensions and
  fixtures, what is obvious in a sentence or two, mechanics stated where they are needed, and
  a plain aside to the referee about running the room.
- **`fixtures/control/arm1b-output.md`** - the register itself. The user endorsed this output,
  and `style/exemplars/` is written to match it. Read a page of it before writing a location.

What the four share is the form the templates already have, and none of them bans the full
stop.

## One register: the referee's

Almost every line is written to a referee reading the page mid-session. Plain nouns,
dimensions, materials, and the verbs of making and decay. A specialist term stands unglossed,
since the referee is looking at the word.

The **Player Summary** is the one line spoken aloud. One to three sentences of what a party
perceives on arriving, in words a referee can say without stumbling. Every bolded noun is a
promise that the thing appears as a Feature below. It says what is there, never what it means.

## Which referee asides stay

An aside addressed to the referee *about running the room* stays: `Do not prompt them.`
`Let them argue about it.` `Roll this where they can see it.` It changes a ruling, so it has
travelled the whole way and earned its place.

Two go, wherever they appear:

- **What the players will feel, conclude, or remember.** The facts are the page's business;
  the reading is theirs.
- **A claim nobody at the table could witness** - reach across time or space, exclusivity,
  what has or has not happened elsewhere. State the observable and stop.

## The sentence budget

Measured off the endorsed baseline, which runs about fourteen words to the sentence.

- A **Feature** is one to four sentences of about fifteen words each. Past twenty words a
  sentence is long; past four sentences the Feature is two Features, or it is carrying
  content a registry owns.
- A **Player Summary** is one to three sentences, same lengths.
- **Referee Notes** are the same sentences, with no separate allowance.
- **Full stops are free.** Length is the constraint, not punctuation. Where a fact wants a
  second sentence it gets one.
- **No trailing explanatory clause.** A clause hung off the end to say why the thing is there,
  what it used to be for, or what it shows is cut rather than shortened. Its usual joints are
  `rather than`, `which is why`, and `meaning that`.

One Feature and one Player Summary from the same entry, to shape:

> A bare stone room, fifteen feet square, holding nothing but its own **floor** - one slab of
> it, wall to wall, without a seam. Something beneath it creaks as the first boot lands.

> **Weighted Floor:** One slab spans the room, pivoting on an iron rod set east wall to west.
> Weight past the centre of either half tips it and slides everything down into a pit ten feet
> below (Test of Fate, Condition). Crossed from both sides at once, it holds level. A pole set
> down on it draws the creak before it tips.

## The tells

A tell is the textual signature of a class of failure - a candidate to read, not an error.
`style/tells.txt` is the list, and `python3 tools/metrics.py --tells [PATH]` reports it over
any markdown; until that file exists, the tells in force are the four `tools/metrics.py`
carries. **Clear a tell by rewriting the line.** Swapping a word or dropping in a comma to
satisfy the pattern leaves the failure in place and costs the measurement as well.
