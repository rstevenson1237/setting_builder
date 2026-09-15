# CLAUDE.md

Loaded on every request. It carries only what must be actively re-checked each time;
forgetting one of these mid-task is this framework's most common failure mode. Everything
else is read from the system that owns it - `README.md` maps the repository, `STEPS.md` is
the build log, `patterns/SPEC.md` is the field spec.

## The three tests outrank everything

Every line of every artifact, at every level, must pass GENRE.md's three tests under
**What a line has to earn**: every word is translated (a setting fact must reach players as
something they can see, hear, be told, pick up, or decide about, or it's cut); setting that
is not actionable cannot be played (every fact names its Handle - a truth with no Handle is
a tag, an event with no Left mark is backstory); never make the player's decision for them
(state what's true and visible, never what they'll conclude). A line that fails these is
cut even where a template asks for it, and a template that keeps producing such lines is
the wrong template. **Re-read GENRE.md at every generation step - don't rely on having read
it once.** Two failure modes to watch: genre drift (an authored plot creeping in, magic
becoming common, an implied central authority), and inert prose (mood in place of a handle,
a fact restated downward from the level where it was already true).

## STEPS.md is the authority

`STEPS.md` is the current, authoritative, sequential build log. Where it disagrees with any
other file, including this one, STEPS.md wins.

## Pattern file rules

`patterns/SPEC.md` is the full spec. The rules that get broken without it open:

- **One skeleton, every file**: **Provides / Read at / Spec / Design patterns /
  Constraints**. There is no `## Design questions` heading.
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
- **`## Read at` names the STEPS.md step(s) that read the file** and opens with the file's
  reach mode - `**Mode: ingredient.**`. Both are validated.
- **`## Design patterns` is compiled content**, carried only by the files on STEPS.md step
  1b's compile list. Check that list before adding or removing the section.

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
