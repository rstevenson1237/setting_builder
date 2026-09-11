# CLAUDE.md

This file is loaded into context on every request, so it stays short by design. Full repo
orientation - directory structure, the generation workflow, scaling/dice, location format,
regions and weights, units and time, and validation - lives in `README.md`, read once per
session via the SessionStart hook in `.claude/settings.json`. Don't re-derive any of that
here; this file exists only for what must be actively re-checked on every single request,
because forgetting one of these mid-task is this framework's most common failure mode.

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

`STEPS.md` is the current, authoritative, sequential build log. Where it disagrees with
`README.md`'s summary of the workflow (or with this file), STEPS.md wins.

## Party altitude vs. the region die

The single most common category error this framework produces: creature AD is pitched
against **party altitude** - what the characters can survive, per `GENRE.md`'s lethality
framing - never against a region's die. The die is a difficulty die (1 = failure, 2-3 =
complication, 4+ = success, so a *smaller* die is *harder*); AD is a power count on a
completely separate axis. A d8 DANGEROUS region does not want an 8 AD creature.

## The two pattern tiers, and where a prohibition goes

Every file in `patterns/*/*.md` is one of two tiers, and its section names say which.
A **classifier** states a contract - which features a thing gets and at what rate - in a
`## Spec` block: `region/*`, `setting/*`, plus `dangerous/High|Medium|Low`,
`wild/Landmark|Hidden|Secret`, and `safe/Settlement`. An **element** fills a contract some
classifier already stated, so it has no Spec of its own: it carries `## Design questions`
instead. Both may carry `## Design patterns`, the constrained examples. Full skeleton:
**Provides / Read at / Spec-or-Design questions / Design patterns / Constraints**.
`patterns/setting/Genre.md` is in neither tier - it is an elicitation procedure, and its
extra sections are that procedure.

**Constraints is where every prohibition lives** - anything that closes a pathway: what
belongs in another file, what this file must never do, a named failure mode. It is blank
when a file is first created; it fills as the patterns are refined and negative patterns
get identified, and from failures observed during an actual build. Write entries
generalized rather than tied to whichever setting produced them. A positive rule phrased
contrastively ("the pressure mechanism, not a rule of thumb") is not a prohibition and
stays where it is.

`## Read at` names the `STEPS.md` step(s) that read the file, and the validator checks
those step ids against STEPS.md - a phase-2 renumber once left eight `setting/` patterns
pointing one step too far down, three at a step that no longer existed.

## Validator posture

`tools/validate_setting.py` (`python3 tools/validate_setting.py`) checks `patterns/*/*.md`
itself (citation format, section structure per tier, `## Read at` step ids)
unconditionally, plus generated `setting/` content against the templates. Strict on
format, relaxed on content, ratios, and prose - it fails CI on unambiguous breakage in
content that *exists* (unknown codes, name mismatches, orphaned nodes, broken citations)
and warns on what needs a human glance but might be intentional. **A file that is simply
missing is a warning, not an error** - partial, in-progress work is expected to push and
be reviewed before every file exists. Extend it alongside any new artifact type or
template rule.

## Pattern citation format

A citation from one `patterns/*/*.md` file to another is always `folder/File.md`, bare, no
`patterns/` prefix - except a reference to a `patterns/setting/*.md` file, which always
keeps the `patterns/` prefix, since a bare `setting/File.md` means the *generated* file of
that name, not the pattern that produces it. `tools/validate_setting.py` enforces this.
</content>
