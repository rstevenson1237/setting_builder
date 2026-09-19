# Dangerous - Trap

## Provides
Which mechanism a built hazard uses, what springs it, what it forces, and who set it. What
an expression resolves to is `setting/Procedures.md`'s. Distinct from
`dangerous/Environmental.md` and `dangerous/Residual.md`: a trap was built for this, by
somebody, and still does that job.

## Spec

```
TRAP
  1     Mechanism - what physically does it, filtered by the tier dangerous/Hazard.md
        rolled            (genre: mechanisms-nuisance, mechanisms-damaging,
                           mechanisms-lethal)
  1     Trigger - the action that springs it, a discrete act on the thing itself
  1     Damage - the expression the tier allows, per setting/Procedures.md
  1     Who set it, and whether anyone is still here to maintain it
  1     Terms for the working parts, named rather than described
                                                        (genre: vocabulary-underground)
```

**A mechanism has to be maintainable by whoever is here.** A trap needing a machinist has a
machinist somewhere in the region, or it does not work. Where a tier's list is thin for the
region's materials, drop a mechanism from the tier above and take out what makes it worse.

**The mechanism is picked first, and it decides the damage type**: Piercing from a dart,
needle, spear or spike; Crushing from a deadfall, a weight, a fall or walls; Poison from a
coated edge or a released gas; Fire from oil or a flame kept lit; Blast from anything stored
under pressure.

Write every trap as `**Name:** tell; tell -> effect (expression)`, colon inside the bold per
`templates/Location.md`. The tell is the clue `dangerous/Hazard.md` drew, on this line and
not a Feature of its own.

## Constraints

- **Never pick a damage type the mechanism cannot produce.** A type chosen first drags in a
  mechanism the region has no way to build or maintain, which is how a region ends up with
  a frost trap nobody could have built.
