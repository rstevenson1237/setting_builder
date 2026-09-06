Procedures of [Setting Name]

## Tests and Consequences

A test is called only when failure is interesting - never to ask about something nobody at
the table doubts. The referee states the stakes before the roll, not after; the roll
decides only which consequence tier lands, not whether the situation is worth resolving
with dice. Every consequence sorts into one of three tiers:

- **Nuisance** - costs time, position, or a resource, with no lasting harm. The default
  outcome when a failed test had nothing serious actually at stake.
- **Damaging** - costs hit points, a resource, or standing, recoverable within the scene.
- **Lethal** - can end a character outright. Reserved for tests the fiction already flagged
  as genuinely dangerous - a fall, poison, fire, a blow that actually lands.

A failed test never produces a worse *story* than a passed one - it produces a costlier
one.

## Traps

Every trap resolves to one of the same three impact tiers, fixed when the trap is written
and never rolled for afterward:

- **Nuisance** - noise, a mess, lost time, an alarm. Nothing carried is put at risk.
- **Damaging** - a hit point loss or a condition the party can walk away from.
- **Lethal** - can kill outright, reserved for a trap whose tell was genuinely available to
  a party moving carefully.

A trap's mechanism and tell are written into the trap itself (`patterns/dangerous/Trap.md`,
`patterns/wild/Trap.md`); this file only fixes what each tier is allowed to cost.

## Searching

A stated detail, investigated, is found - no roll. Searching resolves on the fictional
action taken, not on a dice check: a party that says where and how it is looking finds
what is actually there, in that manner, at that spot. Searching never manufactures content
that was not already placed - it only decides whether the party pays the cost to reach what
is already there. That cost differs by rating:

- **SAFE** - free; searching is not time-bound (see Time, below).
- **WILD** - costs one four-hour action, the same as a move, a forage, or making camp.
- **DANGEROUS** - costs a Difficulty roll (see Region Dice, below); failing it does not hide
  what was found, it costs a step on the region's Danger track instead.

## Time

Time is tracked differently by rating, and never converted between them:

- **SAFE** - not time-bound. Hours pass off-page unless a specific Situation or Event
  demands otherwise.
- **WILD** - one action costs four hours: a move between neighbouring Landmarks, a search
  of one Landmark, a forage, a tracking attempt, or making camp.
- **DANGEROUS** - runs on the Danger table's six-step countdown instead of the clock (see
  Region Dice, below).

## Scaling

Four numbers in this framework look alike and measure different things. Never substitute
one for another:

- **Players** carry 1-6 dice of d4-d12, d6 average.
- **Creatures** carry d6 only, count 1-18, with a bonus of -2 to +6 - reading roughly as
  classic Hit Dice.
- **Factions** carry d6 only and **no bonus**; a faction's count means something only
  relative to the other factions in play, never on its own.

Creature AD (Action Dice) is pitched against **party altitude** - what the characters can
actually survive, per `GENRE.md`'s lethality framing - and never against a region's die.
The die and AD sit on unrelated axes; see Region Dice, below.

## Region Dice

A region's die (d4-d12) is a **Difficulty die** - unrelated to Scaling above, and not a
power level. Roll it whenever the outcome of an action within the region is genuinely
uncertain:

- **1** - failure
- **2-3** - complication
- **4 or higher** - success

A *smaller* die is *harder*: **d8 is baseline**; d6 is a tougher region, d10 an easier one,
d4 and d12 are deliberate outliers reserved for a region that means to stand out.

What a failed or complicated roll costs depends on rating:

- **WILD** - rolled on each four-hour action; a failure rolls on the region's d6 Encounter
  table.
- **DANGEROUS** - rolled on each meaningful action; a failure steps the region's d6 Danger
  table down by one, counting from 6 toward 1. Entry 6 is the place noticing; entry 1 is
  the place acting.
- **SAFE** - not rolled per-location; SAFE's own d6 Events table is rolled on entry and
  each week thereafter instead.

Location counts follow from this math rather than convention, and deviating from either is
a deliberate trade with a measurable cost, not an oversight: a WILD region at N locations
expects exactly one encounter per full traverse at every die size, and a DANGEROUS region
at 3x the die expects exactly three of the Danger track's six steps per full clear.
