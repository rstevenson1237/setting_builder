# Dangerous - Treasure

## Provides
What a DANGEROUS location holds to be taken - which registry or table it comes from, what
conceals it, and what stands between the party and it.

The tables themselves are `setting/Treasure1.md` through `Treasure5.md`; citation format
is in `templates/Location.md`. This is the supply end of a Key or a piece of Lore - the
object found here. The demand end, a lock or a quest target this room holds for
something elsewhere, is drawn by the weight file's own registry lines instead.

## Spec

```
TREASURE
  1     Disposition   {guarded | hidden | discarded} - see Patterns
  1     What it is - exactly one, drawn at these rates rather than freely chosen
        {table roll 55% | key 20% | lore 20% | unique treasure 5%}
                        (patterns/setting/Treasure.md,
                         dangerous/Key.md, dangerous/Lore.md,
                         patterns/setting/UniqueTreasures.md)
  1     Container - what it is in, under, or behind, its own condition, and the search or
        trigger that reaches it
  1     Guarded: what guards it, drawn as an Encounter or a Hazard
                        (dangerous/Encounter.md, dangerous/Hazard.md)
  25%   A lesser thing living on or in the container - small, no match for the party, and
        it does not know what it is sitting on         (dangerous/Creature.md)
  25%   Something set on the container itself, whatever the disposition - mechanism fixed
        to trap         (dangerous/Hazard.md, dangerous/Trap.md)
  30%   Something already tried for it and failed
  20%   A reason it was left rather than taken
```

**This is the reward end of the location - what is here to be taken.** A key found here is
treasure; the *lock* a key elsewhere opens is not, and belongs to the drawing class's
registry block. Lore is the same: a document lying here is a find, and it is drawn here.

**Never name or describe the contents of a table roll.** The cited roll decides them, and
stating an item would contradict whatever comes up. Describe the container, what hides it,
and what it takes to reach it - the same way a hidden exit is handled. This does **not**
apply to a unique treasure, a piece of lore, or a key: those are named, because each is a
stub row in its own registry and the row needs a name to be written against.

**One pull per citation.** A location wanting more takes a second citation elsewhere in its
Features rather than multiplying one.

**The rates exist because an unrated menu collapses to its first option.** A four-way
choice with no weights on it reads as "pick one", and what gets picked is whatever is
easiest to write - which is always the table roll, since it names nothing and owes no
registry a row. Keys and Lore are the two things that make a region a network instead of a
list, and both reach a location only through this line. A DANGEROUS region that finishes
4c having drawn no key at all has not found that keys did not fit; it has skipped the
draw.

**The container is a second object, and it is drawn as one.** What holds a cache decides
most of what reaching it costs - whether it opens, whether it travels, whether it survives
being opened wrong, whether taking it whole is an option the party would rather have. A
cache written with no container is a pile the party picks up.

**A lesser thing is not the guard.** It is small enough to be driven off, and the point of
it is that it is a tell: something has been living undisturbed on this for long enough to
say nobody has been here. Where the disposition is `guarded`, the guard is still drawn - a
rat in the chest does not discharge that line.

**A trap on the container is drawn even where nothing guards the room**, which is why the
line does not read off the disposition. Its clue is the cache itself, per
`dangerous/Hazard.md`, and what it threatens is as often the contents as the party.

**A guard is drawn, not invented.** Where the disposition is `guarded`, the thing guarding
it comes from `dangerous/Encounter.md` or `dangerous/Hazard.md` like any other - which is
what keeps a guardian a real encounter with a sign and a want, rather than a sentence
attached to a chest.

## Design patterns

**Which table**
- **I - Scavenged Loot** - debris that rewards looking without demanding action. Low
  weight, and the default where a find should be a small mercy rather than a payoff.
- **II - Equipment and Armaments** - tied to a person or creature: what a guard carries,
  what a corpse still has, what a work party left behind.
- **III - Gems and Jewelry** - a cache with no owner present. Medium-weight hidden
  treasure, and anything walled up or buried.
- **IV - Luxury and Trade Goods** - bulk with a function. Stores, a cargo, a faction's
  supply, something that was being moved when the region stopped working.
- **V - Treasure Cache** - the payoff. High weight, and the room the rest of the region is
  arranged around.

**Concealment** - under a floor, behind a course of stone, inside something else, in
water, in a corpse, in plain sight and unrecognisable, held by something that will not
let go, in a container whose lock is elsewhere in the region.

**Discarded** - dropped where it fell and left; spilled from a container that gave out;
abandoned in a retreat with no time to gather it; lying in plain sight because nothing
that has passed through since had a reason to want it; indistinguishable from debris
until somebody looks twice.

**Containers** - a chest with its lock on the inside; a coffer banded and too heavy to
carry whole; a jar sealed under pitch; a niche plugged with a single dressed stone; a
course of masonry laid over it; a body, still wearing it; a sack gone to fibre that will
not lift; a cistern, and the water is still in it; a floor void under a flagstone; a beam
hollowed and capped; an animal's cache, sorted the way an animal sorts; something built
around it that would have to come down first.

**A container's own condition** - swollen shut and needing the hinges rather than the lid;
burst already, and the contents spread; opened once and closed again by somebody who left;
fused to the floor by what has grown over it; sound, and that is the strange part in a room
where nothing else is.

**Why it is still here** - whoever hid it died before returning; it is too heavy; it is
guarded; it is cursed and known to be; it is worthless to the current occupants and
valuable to the party; nobody has been this deep since.

**Guard relationships** - a creature that has nested on it without knowing what it is; an
occupant who knows exactly what it is; a trap set by someone long dead; a mystery that
must be answered first; something that will follow whoever takes it.

## Constraints

- **A region's stated table-lean is a draw, not a claim.** When a Region Overview names
  which of the five Treasure tables the region leans on, treat it as a per-location draw
  the same way a class file's own spec lines are drawn, and settle any that never got
  cited at 5c. A lean no room ever cashes out is a fact about the region that reaches no
  player.

- **A container is never a blank noun.** "A chest" states only that there is treasure here,
  which the Feature already said. What it is made of, what shape it is in, and whether it
  can be moved are what a party makes a decision out of.

- **Never write a lesser guard the party must fight.** The moment it is a real threat it is
  the location's encounter, drawn at `dangerous/Encounter.md` with a sign and a want, and
  the cache has quietly been given two guards while the room was scoped for one.
