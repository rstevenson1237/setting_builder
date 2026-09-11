# Wild - Hazard

## Provides
What in a WILD location acts against the party, whether anybody set it, what warns of it,
and what it costs.

## Read at
Step 4c, when a classifier's spec line draws a challenge and the challenge is a hazard -
`wild/Landmark.md`, `wild/Hidden.md`, or `wild/Secret.md`. Impact tiers and resolution are
in `setting/Procedures.md`. Distinct from `wild/Mystery.md`, which is the neutral case: a
mystery costs nothing until a genuinely wrong attempt is made, a hazard acts on contact or
condition.

## Spec

```
HAZARD
  1     Mechanism   {set | condition of the ground | living} - decide first, they read
        differently
  1     Impact tier, per setting/Procedures.md   {nuisance | damaging | lethal}
  1     A warning available to somebody moving carefully
  1     What it was for, and who set it - where the mechanism is `set`
  20%   Something already caught in it
```

**The mechanism is a line here, not a file.** `dangerous/Hazard.md` splits its three
mechanisms across `Trap`, `Environmental` and `Residual` because each carries a contract of
its own - a maker still here, a condition with a cause in the Dressing, a maker gone. A
WILD hazard's three answer the same two questions whichever is drawn, so the choice fits on
one line and earns no middle tier.

**In the open, almost everything gives warning.** A dungeon can hide a pressure plate in a
worked floor; broken ground announces itself to anyone reading it. So a WILD hazard's
warning is rarely concealed - it is *available and easy to walk past*, which is a
different failure and a better one. A party moving fast should be able to miss what a
party moving carefully would catch, and the cost of moving carefully is the four-hour
action they spend on it.

**Set hazards have owners.** Somebody put it here for something, and that somebody is a
fact about the region - a trapline means a trapper, a deadfall on a trail means whoever
uses the trail is not welcome.

**Contract.** A WILD hazard owes: its mechanism, an impact tier, a warning available to
careful movement, and (where it was set) what it was for. Genre-neutral and permanent.
Which mechanisms fill that contract is not - the Design patterns below are this build's
compile of it, from this setting's chosen genre reference.

## Design patterns

**Set by people** - a snare or spring-noose on a game trail; a pit with a covered mouth; a
deadfall log or stone; a spiked pit at a gap in a wall; a line strung at ankle or throat
height; an alarm - stones on string, a bell, a pile that falls; a poisoned water source; a
gate or barrier rigged to fall; a bait pile with something waiting near it; a marked
crossing that has been re-marked wrongly.

**Conditions of the ground** - a bog or quaking ground; ice over water; a scree slope that
runs; an undercut bank; a rotten log bridge; loose footing above a drop; a sinkhole under
turf; a tide, flood, or seasonal channel; a cave with bad air; a hollow that pools cold.

**Living hazards** - a plant that stings, blisters, or blinds; a plant easily mistaken for
one worth gathering; a nest that defends itself; something that hunts by ambush from
below; something that hunts by ambush from above.

**Warnings** - disturbed ground; a path that goes around; older remains of previous
victims; the absence of animal sign where there should be some; cut ends on vegetation;
something tied, and recently; the way the water moves; a smell.

## Constraints

- **A living hazard is not an encounter.** What makes it a hazard is that nothing chooses
  to act on the party - the plant is where it is, the ambusher takes whatever passes.
  Where the thing has a want, a reaction, or somewhere else it could be, it is a creature
  and belongs in `wild/Creature.md`, which asks what it is doing and what avoiding it
  costs.
