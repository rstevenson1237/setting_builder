---
id: table.treasures
target: table
phase: decorator
writes: [Entries]
dependencies:
  - table:S-HIS
  - table:S-TRU
  - table:T-NAM
  - table:T-TR5
output_template: templates/table.md
schema_version: 1
---

`T-TRE` holds unique treasures: the named singletons, one of each, never
restocked and never rolled up twice. It is an artifact table — rows at step 3,
and a Decorator pass at step 4 that makes each row the thing itself rather than
a description of it.

**Columns:** `ID | Entry | Mechanics`. `decorate: true`.

## Patterns

**Each one is a named object with a history and one owner at a time.** The name
decomposes into recorded roots. The history is short, specific, and findable
somewhere else in the corpus. If nothing else in the setting knows this object
exists, it is a band-five find with a nicer sentence.

**The entry is what a party sees when they are holding it.** Not a catalogue
line. What it is made of, what has happened to it, what is worn, what is
missing, what has been repaired badly. The Decorator pass exists to get to that
sentence.

**Every unique treasure is wanted by somebody who is still here.** A faction, a
named creature, or an order nobody can rescind. That want is what makes it
different from money: taking it means having taken it from someone.

**It carries a cost, not a drawback.** Nothing here is a cursed item with a
trick ending. It weighs something, it is recognised, it is owed, it does not
work the way its records say, or it only works where it came from. State which.

**One clue chain per treasure, at minimum.** A `T-LOR` entry, a rumour, a
mention in a record, a matching fitting in `T-ARC`. A unique treasure nobody in
the setting has ever mentioned cannot be sought, only stumbled on.

**Eight rows.** These are the objects a campaign is remembered by, and eight is
already generous for a setting of six regions.

## Excluded patterns

- **A generic magic item with a name attached.** The history is the content.
- **An item that scales with its owner, levels up, or grows.** It is finished.
  It was finished before anybody now alive was born.
- **A set with pieces to collect.** A pair with one half missing is fine and it
  is one object with a hook. A set of seven is a plot.
- **A treasure whose only property is a value.** Then it is `T-TR5`.
- **An item that makes a whole region trivial.**
- **An item nobody wants back.**

## Design questions

1. **Which eight objects should this campaign be remembered by?**
2. **For each: what is its name, and what does the name decompose into?**
3. **Who wants it back, and how far will they go?**
4. **What does carrying it cost, in weight, recognition, or obligation?**
5. **Where in the corpus is the clue that this thing exists?**
6. **What does it do that its own records get wrong?**
