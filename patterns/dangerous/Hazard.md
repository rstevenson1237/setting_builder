# Dangerous - Hazard

## Provides
What in a DANGEROUS location acts against the party without anything choosing to, what
warns of it, and what it costs.

## Read at
**Mode: ingredient.** Step 4c, when a weight file's spec draws a challenge and the
challenge is a hazard, or when `dangerous/Treasure.md` draws a guard. Which *mechanism*
is decided here; the mechanism file supplies what fills it. The tier it carries is
`patterns/setting/Impact.md`'s, and resolution is `setting/Procedures.md`'s. Distinct
from `dangerous/Mystery.md`, which is the neutral case: a mystery costs nothing until a
genuinely wrong attempt is made, a hazard acts on contact or condition.

## Spec

```
HAZARD
  1     Mechanism   {trap | environmental | residual}
                        (dangerous/Trap.md, dangerous/Environmental.md,
                         dangerous/Residual.md)
  1     Clue - perceivable before the hazard acts, and not itself the hazard
  1     Trigger - the specific action or condition that sets it off
  1     Impact tier   {nuisance | damaging | lethal}   (patterns/setting/Impact.md)
  20%   Something already caught in it
```

**Clue, Trigger, Impact is the same triple a concealed thing uses**, with the payload fixed
negative. That is the whole shape: something perceivable, an action or condition acting on
it, an outcome. A hazard missing its clue is not hidden, it is unfair - the party never had
the information the choice needed.

**Two clues is better than one** - one that anyone entering would notice, one available
only to somebody already looking. The first makes the room readable; the second rewards the
search.

**A hazard guarding treasure needs no separate clue**: the treasure is the clue, and a
party that does not suspect a cache has made a choice.

## Constraints

- **The tier is not restated here.** What the three tiers cost, how often a lethal one is
  honest, and what the cost is paid in are `patterns/setting/Impact.md`'s; this file draws
  a tier and owes the clue that makes it legible.
