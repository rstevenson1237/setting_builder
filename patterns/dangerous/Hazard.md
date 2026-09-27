# Dangerous - Hazard

## Provides
What in a DANGEROUS location acts against the party without anything choosing to, what
warns of it, and what it costs. Which mechanism is decided here; the mechanism file
supplies the rest. What a tier resolves to is `setting/Procedures.md`'s. A mystery costs
nothing until a genuinely wrong attempt; a hazard acts on contact or condition.

## Spec

```
HAZARD
  1     Mechanism   {trap | environmental | residual}
                        (dangerous/Trap.md, dangerous/Environmental.md,
                         dangerous/Residual.md)
  1     Clue - perceivable before the hazard acts, and not itself the hazard: one anyone
        entering would notice, and where it can, a second only a searcher finds; a
        hazard guarding treasure takes the treasure as its clue
  1     Tier, rolled before going down - it fixes what the mechanism file may pick and
        what the hazard may force                                            {TIER}
  20%   Something already caught in it
```

```
TIER - the first of these that hits, and nothing below it
  lethal       - 20%; can kill outright, and the clue already said so
  damaging     - 40%; costs the party something they have to spend to get back
  nuisance     - otherwise; costs time, ground, noise, position, or a piece of gear
```

## Constraints

- **The whole hazard is one Feature, never two.** The clue is how the hazard is seen
  before it acts, not a second object.

- **Never raise a tier because the room feels important.** That is how a region ends up
  with no tiers, only a tax on entering rooms.
