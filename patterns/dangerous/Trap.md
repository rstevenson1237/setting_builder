# Dangerous - Trap

## Decides
Which trap fits, and whether it states a tell.

## Read at
Step 4c, when a weight file's spec draws a trap. Resolution is not here - it is in
`setting/Procedures.md`.

## Spec

```
TRAP
  1     Mechanism, from the Patterns below
  1     Impact tier, from setting/Procedures.md   {nuisance | damaging | lethal}
  1     Tell, IF this trap is a medium-weight location's challenge
  33%   Treasure, where the trap guards something
```

**The tell requirement follows from the class.** A trap presented as a MEDIUM location's
challenge must state a visible tell, because MEDIUM guarantees an obvious reactive
element. A trap without a tell is not obvious - a room built on one presents as empty, and
belongs at LOW weight as variance. A trap guarding treasure needs no physical tell: the
treasure is the tell, and a party that does not suspect a chest has made a choice.

Write every trap in one format:

`**Name:** tell; tell → effect; effect`

The colon goes **inside** the bold, per `templates/Location.md`'s Feature label format - a trap
is a Feature line like any other, and `tools/validate_setting.py` will not recognise one
written `**Name**:`.

The arrow makes it visible at a glance when a trap has been written with no way to detect
it. Two tells is better than one - one that anyone entering would notice, one available
only to someone already looking.

## Patterns

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

Mechanisms are drawn from what the region is built from and what its occupants can
maintain. A trap needing a machinist has a machinist somewhere, or it does not work.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
