---
id: table.language
target: table
phase: builder
writes: [Entries]
dependencies:
  - table:S-HIS
  - table:S-TRU
  - config
output_template: templates/table.md
schema_version: 1
---

`T-LNG` is the root registry. Every proper name in the setting decomposes into
roots recorded here, and `validate.py` checks that it does (M18). It is written
before any table that carries a name.

**Columns:** `ID | Root | Meaning`. Above the table, the file states the phoneme
set, the compounding rules and the register that separates the naming layers.
`draws_on` names the S tables the vocabulary is built out of.

## Patterns

**A registry, not a roll table.** Nothing draws on this randomly. It runs as
deep as the setting's names require and it is the one table with no row band:
thirty roots is a working registry for a setting of six regions, and it grows
whenever a step's question batch proposes a new one.

**A root is coined in a question batch and never in passing.** That is the rule
the whole naming layer rests on. A writer who needs a root they do not have
stops and asks. An invented root becomes canon silently and M18 will pass it,
because M18 checks decomposition against this file and this file is whatever it
says it is.

**State the rules above the table and keep them mechanical.** The phoneme set,
what may cluster and where, how two roots join, whether a compound may run to
three, how plurals are formed. A referee coining a name at the table follows
these and lands in register. Rules that cannot be followed without taste are not
rules and belong in the setting's Style section.

**Two layers, and the register separates them.** A living layer of plain
compounds naming what a thing is or does, and an older layer built from the
recorded vocabulary that is often wrong about what the place is now. Say in this
file which roots belong to which layer, or which orderings mark a name as
belonging to one. Where a place carries a name in both layers the two rarely
agree, and that disagreement is content.

**A meaning is a definition and a piece of history.** "Below the waterline, and
lost, but whole" does two jobs: it defines the root and it states a fact of the
world. That second job is what makes the registry worth reading.

**Mind the segmenter.** `config` carries `naming.min_root_length` and
`naming.stop_words`. A root shorter than the minimum cannot be matched, and a
name built only of stop words decomposes into nothing. Compounding roots that
never stand alone are recorded anyway and marked as such.

## Excluded patterns

- **A root coined to fit a name that is already written.** Backfilling makes the
  registry a record of what has been done rather than a constraint on what may
  be done.
- **A conlang.** Grammar, cases, verbs and syntax are not needed by anything in
  the pipeline and nobody will read them. Roots, meanings, and how they join.
- **A root with no meaning, or a meaning that is only a translation.** The
  meaning column carries what the word tells a referee.
- **Two roots that mean the same thing.** They will be used interchangeably and
  the layers will stop separating.
- **Names.** Names are `T-NAM`. This table is what names are made of.

## Design questions

1. **What is the phoneme set, and what may cluster where?**
2. **How do two roots join, and may a compound run to three?**
3. **What separates the two naming layers — which roots, or which ordering?**
4. **Which roots does the roster already need?** Every region name, every
   container name and the setting's own name decomposes into this file.
5. **Which roots does the world need that no name uses yet?** Water, stone,
   depth, direction, light, the fallen power's own word for itself.
6. **Which root carries a fact a party could use?** Those are the ones worth
   putting into names of places a party will visit.
