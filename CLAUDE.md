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

## Patterns' Constraints sections are earned, not anticipated

Every file in `patterns/*/*.md` ends with a Constraints section that starts empty and fills
only from observed generation failures during an actual build - never from guessing what
might go wrong. If you observe one while generating or reviewing content, add it there in
the same pass, generalized rather than tied to whichever setting produced it.

## Validator posture

`tools/validate_setting.py` (`python3 tools/validate_setting.py`) is strict on format,
relaxed on content, ratios, and prose - it fails CI on unambiguous breakage (unknown codes,
name mismatches, missing files, orphaned nodes, broken citations) and warns on what needs a
human glance but might be intentional. Extend it alongside any new artifact type or
template rule.
</content>
