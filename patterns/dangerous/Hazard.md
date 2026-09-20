# Dangerous - Hazard

## Provides
What in a DANGEROUS location acts against the party without anything choosing to, what
warns of it, and what it costs.

Which *mechanism* is decided here; the mechanism file supplies what fills it, tier by
tier. What a tier resolves to - what is rolled, and what it does - is
`setting/Procedures.md`'s. Distinct from `dangerous/Mystery.md`, which is the neutral
case: a mystery costs nothing until a genuinely wrong attempt is made, a hazard acts on
contact or condition.

## Spec

```
HAZARD
  1     Mechanism   {trap | environmental | residual}
                        (dangerous/Trap.md, dangerous/Environmental.md,
                         dangerous/Residual.md)
  1     Clue - perceivable before the hazard acts, and not itself the hazard
  1     Tier - the first of these that hits, and nothing below it:
          20%   lethal    can kill outright, and the clue already said so
          40%   damaging  costs the party something they have to spend to get back
          1     nuisance  costs time, ground, noise, position, or a piece of gear
  20%   Something already caught in it
```

**Clue, Trigger, cost is the same triple a concealed thing uses**, with the payload fixed
negative: something perceivable, an action or condition acting on it, an outcome. Only the
Clue is drawn here. What sets the hazard off and what it then forces differ by mechanism and
are drawn with it; the Clue does not, which is why it sits at this level. A hazard missing
its clue is not hidden, it is unfair - the party never had the information the choice
needed.

**The tier is what the mechanism file draws against**, twice over: it picks the mechanism
from that file's list, and it fixes which expressions the hazard may force, per
`setting/Procedures.md`. Roll it before going down.

**Two clues is better than one** - one that anyone entering would notice, one available
only to somebody already looking. The first makes the room readable; the second rewards the
search.

**A hazard guarding treasure needs no separate clue**: the treasure is the clue, and a
party that does not suspect a cache has made a choice.

## Constraints

- **The whole triple is one Feature, never two.** A hazard written as a clue Feature and
  a separate mechanism Feature has split one thing the party addresses across two lines,
  against `templates/Location.md`'s rule that a Feature is one addressable thing. The clue
  is not a second object; it is how the hazard is seen before it acts.

- **A tier is a cost, not a death sentence by default.** The ladder is why: most
  hazards come out survivable and the lethal ones stay rare enough to be believed. Raising
  a room's tier because the room feels important is how a region ends up with no tiers at
  all, just a tax on entering rooms.
