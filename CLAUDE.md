# CLAUDE.md

Loaded on every request. It carries only what must be actively re-checked each time;
forgetting one of these mid-task is this framework's most common failure mode. Everything
else is read from the system that owns it - `README.md` maps the repository, `STEPS.md` is
the build log, `patterns/SPEC.md` is the field spec.

## The three tests outrank everything

Every line of every artifact, at every level, must pass STYLE.md's three tests under
**What a line has to earn**: every word is translated (a setting fact must reach players as
something they can see, hear, be told, pick up, or decide about, or it's cut); setting that
is not actionable cannot be played (every fact names its Handle - a truth with no Handle is
a tag, an event with no Left mark is backstory); never make the player's decision for them
(state what's true and visible, never what they'll conclude). A line that fails these is
cut even where a template asks for it, and a template that keeps producing such lines is
the wrong template. **Re-read GENRE.md and STYLE.md at every generation step - don't rely
on having read them once.** Two failure modes to watch: genre drift (an authored plot
creeping in, magic becoming common, an implied central authority), and inert prose (mood in
place of a handle, a fact restated downward from the level where it was already true).

## STEPS.md is the authority

`STEPS.md` is the current, authoritative, sequential build log. Where it disagrees with any
other file, including this one, STEPS.md wins.

## Documentation says where, not how

Prose about a system states **where it lives and what it does**. It never restates **how it
works** - to understand a system, read the system. A one-line gloss naming a subsystem is
fine; a paragraph reproducing its rules is a second copy that nothing keeps current, and it
will drift into contradicting the thing it describes. This binds `README.md`, this file,
and every explanatory passage in `templates/` and `patterns/`.

So, when writing or editing any of them:

- Name the authority and stop. If a rule is spec'd in `STEPS.md`, `patterns/SPEC.md`,
  `setting/Procedures.md`, a template, or the validator, cite that file rather than
  summarizing it.
- Keep only what lives nowhere else - operational facts (commands, one-time setup) and
  rules that must be in context before the authority is opened.
- **Never update documentation to match a change.** If a passage has gone stale, that is
  evidence it was restating rather than pointing: cut it back to a pointer instead of
  refreshing it.
- Cut history on sight. Rationale, superseded approaches and what a rule replaced belong in
  commit messages, not in a file loaded on every read.

## Pattern file rules

`patterns/SPEC.md` is the full spec. The rules that get broken without it open:

- **One skeleton, every file**: **Provides / Spec / Constraints**. There is no `## Read at`
  and no `## Design questions` heading, and no `## Design patterns` heading - every field
  is a neutral, permanent question or edge; a field that reads flat gets a sharper
  question, never a list of examples to draw from.
- **Every Spec line is an edge or a question.** An edge names another pattern file in
  parentheses and belongs in the fenced block, never in the prose under it. A question
  cites nothing. A citation is an edge only where the generator must go and read that file;
  anything already in context is stated as part of the question.
- **A line that varies between the classes drawing it belongs in the drawing class's Spec;
  a line that is the same for all of them belongs in the file it cites.** Same test
  `setting/Procedures.md` applies one level up.
- **Constraints is where every prohibition lives** - anything that closes a pathway. Write
  entries generalized rather than tied to whichever setting produced them. A positive rule
  phrased contrastively is not a prohibition and stays where it is.
- **A pattern file never says when or by what it is reached.** The read-set graph runs one
  way - a STEPS.md step names its template, a template names the pattern files its artifact
  requires, a Spec line names what it draws - and a file restating its own position is a
  second copy of an edge something upstream owns. `## Provides` carries the boundary against
  a sibling file and a pointer to the authority for anything adjacent; nothing else.

## Pattern citation format

A citation from one `patterns/*/*.md` file to another is always `folder/File.md`, bare, no
`patterns/` prefix - except a reference to a `patterns/setting/*.md` file, which always
keeps the `patterns/` prefix, since a bare `setting/File.md` means the *generated* file of
that name, not the pattern that produces it.

## Validator

`python3 tools/validate_setting.py`. Strict on format, relaxed on content, ratios and
prose. A file that is simply missing is a warning, not an error - partial work is expected
to push and be reviewed before every file exists. Extend it alongside any new artifact type
or template rule.
