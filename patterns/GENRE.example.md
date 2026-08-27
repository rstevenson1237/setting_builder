---
id: setting.genre
target: setting
phase: architect
writes: [Premise, Register, Play, Constants, Absences, Naming, Influences]
dependencies: []
output_template: templates/genre.md
schema_version: 1
---

`GENRE.md` is the thematic inspiration for the whole setting, and it is the one
file every bundle carries. This pattern writes it.

It runs in the main session and takes no bundle, because the file it writes is
the file `resolve_deps.py` injects: there is no genre to inject while the genre
is being written. Answer the design questions below as one batch, write the
file to the output template, then freeze it. Editing `GENRE.md` after Milestone
2 is a step re-run of everything downstream.

## Patterns

**Least common denominators only.** A line belongs here when it is true in
every region of the setting. A line true of one region is demoted into that
region, and a line true of one location is demoted into that location. The test
is mechanical: name a region where the line is false. If one exists, the line
is not genre.

**Write the situation, not the history.** History is `S-HIS` and it is written
at step 3. What belongs here is the standing condition a party walks into: what
the world is doing now, in every part of it.

**State the register by demonstrating it.** A sentence describing a voice is
worth less than a sentence written in that voice. Carry one worked line of each
register that binds everywhere, and keep it short enough to be read as a
sample rather than as content.

**Name the play, not the plot.** The setting supports a kind of session. Say
what a party spends its time doing, what the setting rewards, and what it
costs. A plot names events that have to happen, and events that have to happen
are the thing this system is built to avoid generating.

**Absences are checkable and preferences are not.** "No gods answer" is an
absence a writer can hold a draft against. "A sombre tone" is a preference and
a writer can satisfy it while writing anything at all. Every absence names what
stands in its place, so the writer is not left with a hole.

**Influences state a quality, in one clause each.** Name the work and name what
is taken from it: a pace, a discipline, a way of withholding. Never a scene,
never a character, never a plot. This is the only file in the repository
permitted to name a work outside the content tree, and it names them as a
statement of the kind of play the setting supports.

**Stay under the cap and expect to be cut.** `config/weights.yaml` holds
`genre.max_words`, and `resolve_deps.py` fails above it. The cap is not
arbitrary: this file enters every subagent call, so every hundred words here is
a hundred words taxed on every generation for the rest of the build. Aim well
under it. The first draft that reaches the cap is carrying region content.

**Neutrality holds here too.** Prose never states a mechanical value. `GENRE.md`
carries no tokens either, because a token belongs beside the feature it
qualifies and there are no features in this file.

## Excluded patterns

- **A named place, faction, person or event.** Those are `S-HIS`, `S-FAC`,
  `S-TRU` and the regions. A genre file naming a place has already decided
  something a later step exists to decide.
- **A metaplot, a timeline, or a thing that is about to happen.** The setting
  is a standing situation. What happens is what a party does.
- **A statement about what the players will feel, notice or conclude.** Write
  what is there. A conclusion stated in advance is a conclusion the table is
  denied.
- **Mechanical values, dice, statistics or the name of a ruleset.** The ruleset
  is the mold and is not in this repository. `MECHANICS.md` is the whole
  interface to it.
- **Imitation of a named work.** An influence names a quality that is taken. It
  never licenses generated content that reproduces a named work's places,
  characters or scenes.
- **Instructions to a referee about how to run a table.** That is the finished
  playbook's job, and the referee-facing registers carry it.
- **Its own revision history.** A superseded line is rewritten, not annotated.

## Design questions

Asked as one batch, before anything is written. Genuine alternatives, not only
the conservative option.

1. **What is the standing situation?** In two or three sentences: what has
   happened to this world, what state it is in now, and what a party walks
   into. Name the one condition true in every region.
2. **What does the world sound like on the page?** Plain and measured, or
   heightened? What does the prose state outright, and what does it refuse to
   state? Which units does it count distance and time in?
3. **What kind of session does this setting support?** Exploration and
   extraction, negotiation between powers, survival against attrition, or
   investigation of something the world will not explain? What does it reward,
   and what does it cost?
4. **What are the three to six constants?** Each one sentence, each true in
   every region. Name a region where each would be false; if you can, it is not
   a constant.
5. **What is absent from this world that a reader would expect?** For each
   absence, what stands in its place?
6. **What does a name sound like here?** What is a name built from, and what
   does the shape of a name tell a referee? Which roots does this open with,
   for the `T-LNG` registry?
7. **Which outside works state the kind of play this supports?** Three to six,
   each with the one quality taken from it. What is deliberately not taken?
8. **What must never appear?** The absences of question 5 are things the world
   lacks. This asks what the writing must not do.
