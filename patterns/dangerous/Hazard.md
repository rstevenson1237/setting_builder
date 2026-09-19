# Dangerous - Hazard

## Provides
What in a DANGEROUS location acts against the party without anything choosing to, what
warns of it, and what it costs. What a tier resolves to is `setting/Procedures.md`'s.
Distinct from `dangerous/Mystery.md`, which costs nothing until a genuinely wrong attempt
is made.

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

**Only the Clue is drawn here.** What sets the hazard off and what it then forces differ
by mechanism and are drawn with it. A hazard missing its clue is not hidden, it is unfair.

**Roll the tier before going down.** The mechanism file draws against it twice: it picks
the mechanism, and it fixes which expressions the hazard may force.

**Two clues is better than one** - one anyone entering would notice, one available only to
somebody already looking. A hazard guarding treasure needs no separate clue: the treasure
is the clue.

## Constraints

- **The whole triple is one Feature, never two.** The clue is not a second object; it is
  how the hazard is seen before it acts.

- **A tier is a cost, not a death sentence by default.** Raising a room's tier because the
  room feels important is how a region ends up with no tiers at all, just a tax on entering
  rooms.
