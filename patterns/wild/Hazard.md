# Wild - Hazard

## Provides
What in a WILD location acts against the party, whether anybody set it, what warns of it,
and what it costs. What a tier resolves to is `setting/Procedures.md`'s. Distinct from
`wild/Mystery.md`, which costs nothing until a genuinely wrong attempt is made.

## Spec

```
HAZARD
  1     Mechanism   {set | condition of the ground | living} - decide first, they read
        differently        (genre: hazards-set, hazards-ground, hazards-living)
  1     Tier - the first of these that hits, and nothing below it:
          15%   lethal    can kill outright, and the warning already said so
          45%   damaging  costs the party something they have to spend to get back
          1     nuisance  costs time, ground, a piece of gear, or the route they wanted
  1     A warning available to somebody moving carefully   (genre: hazard-warnings)
  1     Trigger - what sets it off, or what crossing it costs
  1     Damage - the expression the tier allows, per setting/Procedures.md
  1     What it was for, and who set it - where the mechanism is `set`
  20%   Something already caught in it
```

**The mechanism is a line here, not a file**, because a WILD hazard's three answer the same
two questions whichever is drawn.

**Lethal sits lower here than at depth**, and so does what it forces: a WILD hazard that
kills is one the party was told about and walked into anyway, so it rarely goes past 2d.

**The mechanism picks the damage type.** `set` delivers Piercing, Crushing or Poison;
`condition of the ground` delivers Crushing from a fall or slide, Frost from water and
exposure, Poison from bad air; `living` delivers Poison, or the Condition its sting or spore
leaves behind.

**In the open a warning is rarely concealed** - it is available and easy to walk past. A
party moving fast should be able to miss what a party moving carefully would catch.

**Set hazards have owners.** A trapline means a trapper; a deadfall on a trail means whoever
uses the trail is not welcome.

## Constraints

- **A living hazard is not an encounter.** Where the thing has a want, a reaction, or
  somewhere else it could be, it is a creature and belongs in `wild/Creature.md`.
