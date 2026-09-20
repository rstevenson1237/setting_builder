# Setting - Treasure

## Provides
What the five d20 tables hold, how value is distributed within each, and what money means
to a party at this setting's altitude.

Reads `GENRE.md` for party altitude - what the characters can survive - since value is
only meaningful relative to what they have.

## Spec

```
TABLE SHAPE - each of the five
  1     Result 1 is significantly below the table's average value
  2-3   Each either slightly below average, or about double the average weight for its value
  4-20  The remaining spread, in randomised order - never ascending or descending
  1     No result describes how it is stored, found, or carried
```

```
TABLE II - quality
  10%   poor
  50%   normal
  30%   fine          - 30% of these carry an effect
  3%    masterwork    - always carries a positive effect
  5%    cursed        - always carries a negative effect, and presents as fine or masterwork
```

**Result 1 exists so the roll can disappoint**, and the randomised order exists so it cannot
be read for the best outcome. Both are anti-optimisation, and both matter more than the
contents.

**Anchor value to party altitude.** A find is interesting because of what it buys these
characters. State what a week's ordinary wage is at the head of Table I, and point back to
it from each of the others, so every number in every table has a scale - treasure hunters
barely above commoners, per `GENRE.md`, means most finds should be *useful*, and a
table-topping result should change what the party can attempt next.

**What one wt is.** `wt` is bulk and weight together - what it takes to move the thing,
not what it weighs on a scale:

```
WEIGHT
  0 wt   Pocketed and forgotten about - no call on anyone's hands
  1 wt   One hand, or about 100 coins
  2 wt   Both hands
  3+ wt  More than one person to carry, and more still the higher it goes
```

**Encumbrance is the lever value pushes off of.** About 100 coins - or a comparable
volume of anything else - per wt is the average relationship, which is what makes a find a
decision rather than an addition. A hoard is heavy *because* it is worth something: a
chest of coin worth 4000 cn is roughly 40 wt and several trips, and writing it at 6 wt to
keep the number tidy deletes the only interesting thing about finding it. State the wt the
haul actually costs, however large that gets.

**A small but incredibly valuable item earns its value by rising an order of magnitude
against that average**, not by escaping it. A gem at 1 wt and 1000 cn is the shape - ten
times the average, small enough to run with, and the reason a party takes it over the
plate. Two orders is a table-topping result and rare; anything past that is a Unique
Treasure and belongs in `setting/UniqueTreasures.md`. Mundane bulk runs the other way, as
low as 5 cn per wt for a sack of copper pennies.

**Table I - Scavenged Loot.** Everyday debris, minor coin, tools, scraps. Average under
500 cn. This is what most finds are, and it should mostly be *useful* rather than valuable -
rope, oil, a whetstone, someone's boots in the party's size.

**Table II - Equipment and Armaments.** Weapons, armour, adventuring gear, with Quality and
Effect columns per the spec above. Normal is 100 cn; fine runs 3-10x, masterwork 10-100x.
Cursed items are valued and described as what they present as - the curse is the trap, not
a label.

**Table III - Gems and Jewelry.** Value-dense and weightless, which makes it the band where
carrying capacity stops being a constraint. Give some pieces a provenance a party could
trace; a ring with a device on it, per `setting/Factions.md`, is worth more than its stones
to the right person and dangerous to sell to the wrong one.

**Table IV - Luxury and Trade Goods.** Bulk with a function - the band where weight is the
whole problem. Bolts, casks, ingots, hides, spices, salt. A party that finds this has to
decide what to leave, which is the most interesting decision treasure can produce.

**Table V - Treasure Cache.** The payoff, and the only table where a single result should
be able to change a party's plans. A mix of coinage - not only standard silver, include
other denominations or foreign/exotic coin - plate, a hoard's worth of one thing.

This is also the table where the weight scale bites hardest, and it should. A result here
is usually more than a party can carry out in one trip, and saying so in the `wt` column
is what turns the payoff into the problem it ought to be: what to take first, what to
cache, what to come back for, and who is still here when they do. A cache that fits in a
backpack is a number, not a haul.

**Materials and coinage** should come from `setting/History.md` and `setting/Truths.md` -
what was minted here, by whom, and whether it is still accepted. Coin from a fallen realm
is a find and a problem at once.

## Constraints

- **Never decide the container.** These tables are reusable everywhere and tied to no
  place. What holds a find, what conceals it, and what it takes to reach it are the
  location's job - see each rating's `Treasure.md`.
