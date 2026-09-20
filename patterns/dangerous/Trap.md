# Dangerous - Trap

## Provides
Which mechanism a built hazard uses, what springs it, what it forces, and who set it.

What an expression resolves to is not here - it is in `setting/Procedures.md`. Distinct from
`dangerous/Environmental.md` and `dangerous/Residual.md`: a trap was built for this, by
somebody, and still does that job.

## Spec

```
TRAP
  1     Mechanism - what physically does it, from the list below for the tier
        `dangerous/Hazard.md` rolled
  1     Trigger - the action that springs it
  1     Damage - the expression the tier allows, per setting/Procedures.md
  1     Who set it, and whether anyone is still here to maintain it
```

**The clue and the tier are Hazard's; everything else a trap owes is here.** A trap is the
mechanism whose defining fact is that **somebody built it for this**, and its trigger
follows from that: a built trap has a deliberate one, a discrete act on the thing itself,
which is what `dangerous/Environmental.md` and `dangerous/Residual.md` do not have and why
the trigger is drawn at this level rather than up. The same goes for the maker -
`dangerous/Environmental.md` has none and `dangerous/Residual.md`'s is gone. Mechanisms
below are sorted by the tier already rolled, so the selection cannot quietly outrun it.

**A mechanism has to be maintainable by whoever is here.** Mechanisms are drawn from what
the region is built from and what its occupants can keep working - a trap needing a
machinist has a machinist somewhere in the region, or it does not work. This is the line
that keeps trap selection tied to the region instead of to a list.

**A trap's damage type is whatever the mechanism can actually deliver**, and the mechanism
is picked first: Piercing from a dart, needle, spear or spike; Crushing from a deadfall, a
weight, a fall, or walls; Poison from a coated edge or a released gas; Fire from oil or a
flame kept lit; Blast from anything stored under pressure. A Test of Sanity is a trap's only
where what springing it exposes is itself the harm. Picking the type before the mechanism is
how a region ends up with a frost trap nobody could have built.

Write every trap in one format:

`**Name:** tell; tell -> effect (expression)`

The colon goes **inside** the bold, per `templates/Location.md`'s Feature label format - a
trap is a Feature line like any other, and `tools/validate_setting.py` will not recognise
one written `**Name**:`. The tell is the clue `dangerous/Hazard.md` drew, on this same line
and not a Feature of its own.

The arrow makes it visible at a glance when a trap has been written with no way to detect
it; the expression does the same for one written with no stated cost.

## Design patterns

**Nuisance mechanisms** - an alarm, bell, or released creature that alerts something
elsewhere; a marking trap - dye, scent, residue - that draws attention later; a snare or
net; a trap that ruins a resource rather than a person; a lid weighted to hold something
shut from the inside; a container that destroys its contents when opened wrong; a
mechanism so rusted it half-works and is worse for it.

**Damaging mechanisms** - a covered pit, shallow; a dart or needle from a wall; a spear
trap at chest height; a hanging weight on a trip line; choking gas, spores or dust; a
chest that gasses, sprays, or fouls what it holds; a fixture whose ornament is wired to
its base; a turning trapdoor mounted on an axis.

**Lethal mechanisms** - a spiked pit, deep, with a beam across it; a deadfall or
collapsing floor; a floor that gives onto something living below; a swinging blade, scythe
or pendulum; a small catapult loaded with a ball-and-chain; a flooding chamber; a
rockslide or cave-in; boiling oil from a heated cauldron; walls that close.

**The same mechanism can sit a tier lower** - a pit is the plain case: shallow and empty
it is damaging, deep and spiked it is lethal. Where a tier's list is thin for the region's
materials, drop a mechanism from the tier above and take out what makes it worse, rather
than reaching up for one the tier cannot afford.

**Vocabulary.** Name the working parts instead of describing them: springe, gin, deadfall,
treadle, detent, sear, tumbler, counterweight, trip-line, quarrel, scythe-beam, pitfall lid.
A mechanism with a name is a mechanism a referee can rule on without inventing how it works.

## Constraints

- **Never pick a damage type the mechanism cannot produce.** The type follows the thing that
  does it. A type chosen first drags in a mechanism the region has no way to build or
  maintain, which is the same failure as a mechanism needing a machinist who is not here.
