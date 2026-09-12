# Dangerous - Treasure

## Provides
What a DANGEROUS location holds to be taken - which registry or table it comes from, what
conceals it, and what stands between the party and it.

## Read at
**Mode: ingredient.** Step 4c, when a weight file's spec draws treasure. The tables
themselves are `setting/Treasure1.md` through `Treasure5.md`; citation format is in
`templates/Location.md`. This is the supply end of a Key or a piece of Lore - the object
found here. The demand end, a lock or a quest target this room holds for something
elsewhere, is drawn by the weight file's own registry lines instead.

## Spec

```
TREASURE
  1     Disposition   {guarded | hidden | discarded}
  1     What it is    {table roll | unique treasure | lore | key}
                        (patterns/setting/Treasure.md,
                         patterns/setting/UniqueTreasures.md,
                         dangerous/Lore.md, dangerous/Key.md)
  1     What it is in, under, or behind, and the search or trigger that reaches it
  1     Guarded: what guards it, drawn as an Encounter or a Hazard
                        (dangerous/Encounter.md, dangerous/Hazard.md)
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

**Why it is still here** - whoever hid it died before returning; it is too heavy; it is
guarded; it is cursed and known to be; it is worthless to the current occupants and
valuable to the party; nobody has been this deep since.

**Guard relationships** - a creature that has nested on it without knowing what it is; an
occupant who knows exactly what it is; a trap set by someone long dead; a mystery that
must be answered first; something that will follow whoever takes it.

## Constraints

- **A region's stated table-lean, never cited.** A prior full build had a Region Overview
  state which of the five Treasure tables the region leans on, and three of the five tables
  were never cited by any of its locations - the lean was a claim about the region that no
  room ever cashed out. When a Region Overview names a table lean, treat it as a per-location
  draw the same way a class file's own spec lines are drawn, and settle any that never got
  cited at 4e.
