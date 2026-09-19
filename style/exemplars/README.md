# Exemplars

What a finished artifact reads like, one per class, written to `STYLE.md` and to the class
file its rating and weight names. `STYLE.md` states the register and the budget; these are
that register on a page, and `templates/Location.md` names the matching one in its Context
so a generation step reads it beside the template.

They are also the regression floor: `tools/validate_setting.py` runs the location checks
over `location/` on every invocation, generated setting or not, so a later change to the
Feature grammar shows up here before it reaches any content.

## The files

Each was drawn from its class file exactly as STEPS.md step 4c would draw it, then edited to
the target with `fixtures/control/arm1b-output.md` open. Read the class file beside the
exemplar to see which of its lines each Feature answers.

| File | Class file |
|---|---|
| `location/SAFE-working.md` | `patterns/safe/Settlement.md`, working prominence |
| `location/WILD-landmark.md` | `patterns/wild/Landmark.md`, carrying one Hidden child |
| `location/DANGEROUS-high.md` | `patterns/dangerous/High.md` |
| `location/DANGEROUS-medium.md` | `patterns/dangerous/Medium.md` |
| `location/DANGEROUS-low.md` | `patterns/dangerous/Low.md` |
| `region/DANGEROUS.md` | `patterns/region/Dangerous.md`, a collection at d6 |

Three cases are here because they are the ones a single exemplar per class would otherwise
never show:

- **`DANGEROUS-medium.md` has no lock.** Its class file draws any lock obligation recorded
  against the room at rate `1`, and no registry records one against this room, so the line
  draws nothing. The other two show the opposite case.
- **`DANGEROUS-low.md` takes the one-mundane-exit-plus-a-secret-one case**, where the
  concealed detail is mandatory and its payload is the route. Its hidden way onward is
  nested in the Feature that reveals it and is absent from the Exits line, per
  `templates/Location.md`.
- **`WILD-landmark.md` draws neither a challenge nor a treasure**, both of which its class
  file rates instead of requiring.

## Conventions

- **`X` is a placeholder region code**, not a region. The three DANGEROUS locations sit in
  the region `region/DANGEROUS.md` describes and their codes agree with it; the SAFE and
  WILD ones stand alone.
- **Nothing exists behind the citations.** The locations, Bestiary entries and registry rows
  these files name have no setting under them, so the checks over `location/` skip
  everything cross-file.
- **No proper noun here is drawn from `setting/`.** An exemplar that carried this build's
  nouns would teach them alongside the register.

## Measured

Over the five location exemplars: 18 Features, 3.2 sentences per Feature, 14.9 words per
sentence, longest 20. Every tell in `style/tells.txt` reports zero here, and the validator
holds it there: the exemplars are the good corpus for every tell at once, so a pattern that
fires on them is measuring the wrong thing.
