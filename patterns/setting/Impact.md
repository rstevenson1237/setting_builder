# Setting - Impact

## Provides
The three tiers a hazard's cost is pitched at, which one a given hazard gets, and what the
cost is paid in.

## Read at
**Mode: ingredient.** Step 4c, drawn once per hazard, mandatory: `dangerous/Hazard.md`'s
and `wild/Hazard.md`'s Impact tier line, and `safe/Wealth.md`'s `trapped` Protection, which
draws it only in that one case and so cites it in prose rather than on its Kind line. Read
again at 1c and 2h, where `patterns/setting/Procedures.md` cites it for the tier names the
seeded `setting/Procedures.md` has to resolve.

Distinct from `setting/Procedures.md`, the generated artifact, which owns **resolution** -
what a character rolls, what a tier does to them, and what recovering from it costs. This
file owns the **choice**: which of the three a hazard is, and what makes that the honest
answer. A pattern file cites the tier by name and never restates the mechanic.

## Spec

```
IMPACT
  1     Tier - pitched against party altitude per GENRE.md, never against the region die:
          nuisance    costs time, ground, noise, position, or a piece of gear. Nobody is
                      going to die of it, and it is still a cost the party feels
          damaging    costs something the party has to spend to get back - the working
                      default, and where most hazards sit
          lethal      can kill outright, and the party had what they needed to refuse it
  1     What the cost is paid in   {the body | gear | time | the goods | standing}
  1     Frequency across a region - damaging is the default, nuisance is common, and
        lethal is rare enough to be believed: one or two in a region, each one a party
        that read the room could have walked away from
  1     That the tier is legible from the warning the drawing file already owes - a
        hazard whose clue reads nuisance and lands lethal has cheated
  20%   A tier that rises if the hazard is left alone or answered wrongly, stated as the
        second tier and what raises it
```

**The tier is a promise made before it lands.** Every file that draws this one already owes
a clue or a warning - `dangerous/Hazard.md`'s Clue, `wild/Hazard.md`'s warning available to
careful movement, `safe/Wealth.md`'s Protection. The tier is what that warning is a warning
*of*, which is why it is chosen here and not improvised at resolution: a party's decision to
go around, go slow, or go through is only a decision if the size of the cost was on the
table.

**Cost currency is a real choice, not flavor.** A trap that ruins what the cache holds and a
trap that takes a finger are the same tier and different games. Naming the currency is what
lets a rating pitch its hazards without reaching for the body every time - SAFE especially,
where the goods, the time, and a party's standing in a settlement are all things they can
lose and the body usually is not.

**Contract.** A hazard's impact owes: a tier, what the cost is paid in, and a warning
consistent with both. Genre-neutral and permanent - the tier names are fixed across every
setting, and only what each one resolves to is tailored, in `setting/Procedures.md` at 2h.

## Constraints

- **Resolution never lives here.** What a character rolls, what the tier does, and what
  recovery costs are `setting/Procedures.md`'s and are cited by name. This file exists so
  that three drawing files can name a tier instead of each carrying a cost scale, and it
  stops being able to do that the moment it starts holding mechanics.

- **An impact tier is a cost, not a death sentence by default.** The three tiers exist so
  that most hazards are survivable and the lethal ones are rare enough to be believed. A
  region where every hazard is lethal has no tiers, just a tax on entering rooms.

- **Never pitch a tier against the region die.** The die is a difficulty die on a separate
  axis; the tier answers what the party can survive, per `GENRE.md`'s lethality framing.

- **A lethal tier in a SAFE region needs the Situation behind it.** Per `safe/Wealth.md`,
  somebody's strongroom is somebody's work, and a mechanism meant to kill a thief is a
  statement about the settlement that its own Situation has to already support.

- **The tier is not a Feature of its own.** It qualifies the hazard, so it stays on the
  hazard's line per `patterns/SPEC.md` - a location never carries a Feature whose whole
  content is a tier name.
