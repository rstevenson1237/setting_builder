# Wild - Hazard

## Provides
What in a WILD location acts against the party, whether anybody set it, what warns of it,
and what it costs. What a tier resolves to is `setting/Procedures.md`'s. A mystery costs
nothing until a genuinely wrong attempt; a hazard acts on contact or condition.

## Spec

```
HAZARD
  1     Mechanism - decided first                                       {MECHANISM}
  1     Tier                                                                 {TIER}
  1     Warning kind - available to somebody moving carefully           {WARNING}
  1     Warning - that warning as it shows: rarely concealed, and easy to walk past
  1     Trigger - what sets it off, or what crossing it costs
  1     Damage - the expression the tier allows, per setting/Procedures.md, of a type
        the mechanism can deliver
  1     Set for - where the mechanism is set: what it was for, and who set it
  20%   Caught - something already caught in it
```

```
MECHANISM - exactly one
  set          - something somebody placed, and delivers Piercing, Crushing or Poison
  ground       - a condition of the ground itself, and delivers Crushing from a fall or
                 slide, Frost from water and exposure, or Poison from bad air
  living       - a living thing that acts on whatever passes and wants nothing else, and
                 delivers Poison or the Condition its sting or spore leaves
```

```
TIER - the first of these that hits, and nothing below it
  lethal       - 15%; can kill outright, the warning already said so, and rarely past 2d
  damaging     - 45%; costs the party something they have to spend to get back
  nuisance     - otherwise; costs time, ground, a piece of gear, or the route they wanted
```

```
WARNING - at least one
  disturbed    - ground disturbed
  detour       - a path that goes around
  remains      - older remains
  absence      - a sign an animal would leave, missing
  fresh        - something set or tied recently
```

## Constraints

- **Never a set hazard without an owner.** Somebody put it here for something, and that
  somebody is a fact about the region.
