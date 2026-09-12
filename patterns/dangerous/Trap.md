# Dangerous - Trap

## Provides
Which mechanism a built hazard uses, and who set it.

## Read at
**Mode: kind.** Step 4c, when `dangerous/Hazard.md` draws Mechanism: trap. Resolution is
not here - it is in `setting/Procedures.md`. Distinct from `dangerous/Environmental.md`
and `dangerous/Residual.md`: a trap was built for this, by somebody, and still does that
job.

## Spec

```
TRAP
  1     Mechanism - what physically does it, from the Design patterns below
  1     Who set it, and whether anyone is still here to maintain it
```

**Everything else a trap owes is Hazard's.** The clue, the trigger, and the impact tier are
mandatory lines on `dangerous/Hazard.md` and are answered there for every mechanism; this
file states only what is true of a trap specifically. A trap is the mechanism whose defining
fact is that **somebody built it for this**, which is why the maker line is here and not up
a level - `dangerous/Environmental.md` has no maker and `dangerous/Residual.md`'s maker is
gone.

**A mechanism has to be maintainable by whoever is here.** Mechanisms are drawn from what
the region is built from and what its occupants can keep working - a trap needing a
machinist has a machinist somewhere in the region, or it does not work. This is the line
that keeps trap selection tied to the region instead of to a list.

Write every trap in one format:

`**Name:** tell; tell -> effect; effect`

The colon goes **inside** the bold, per `templates/Location.md`'s Feature label format - a
trap is a Feature line like any other, and `tools/validate_setting.py` will not recognise
one written `**Name**:`.

The arrow makes it visible at a glance when a trap has been written with no way to detect
it.

## Design patterns

**Falling and footing** - deadfall or collapsing floor; covered pit, shallow or deep;
spiked pit with a beam across it; turning trapdoor mounted on an axis; a floor that gives
onto something living below.

**Striking** - swinging blade, scythe or pendulum; spear trap at chest height; dart or
needle from a wall; a hanging weight on a trip line; a small catapult loaded with a
ball-and-chain.

**Area** - choking gas, spores or dust; flooding chamber; rockslide or cave-in; boiling
oil from a heated cauldron; walls that close.

**Guarding an object** - a chest that gasses, sprays, or fouls what it holds; a fixture
whose ornament is wired to its base; a container that destroys its contents when opened
wrong; a lid weighted to hold something shut from the inside.

**Consequence without damage** - an alarm, bell, or released creature that alerts
something elsewhere; a marking trap - dye, scent, residue - that draws attention later; a
snare or net; a trap that ruins a resource rather than a person; a mechanism so rusted it
half-works and is worse for it.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
