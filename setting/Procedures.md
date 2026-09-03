Procedures of [Setting Name]

## Tests and Consequences

A TEST is called for only when failure costs something and success is not certain. Roll
against the relevant characteristic; the referee says what failure costs before the roll.

- **TEST OF CONSTITUTION** - one character is exposed to lethal harm: they triggered it,
  or they are the one it is aimed at.
- **TEST OF FATE** - the whole party is exposed at once. Roll to see who among those in
  the affected area is actually caught, then resolve each of them separately.

Failure produces one of two consequences, chosen to fit the fiction:

- **WOUND** - a lasting injury. It does not heal on its own within a session.
- **CONDITION** - a freeform state: poisoned, bloodied, blinded, deafened, lamed, marked.
  It states its own end - what removes it, or how long it lasts.

## Traps

Every trap carries one of three impact tiers.

- **Nuisance** - no lasting harm. An inconvenience, a delay, a complication. Resolved
  narratively; no test.
- **Damaging** - ordinary damage to whoever triggers it, resolved like any other hit.
  No test.
- **Lethal** - severe enough to demand a test. TEST OF CONSTITUTION for a single target,
  TEST OF FATE for an area. Failure produces a WOUND or a CONDITION.

A single location does not lean on the same tier twice.

## Searching

Finding is a matter of doing the right thing in the right place, not of rolling well.

- **A stated detail needs no roll.** If a location's Features name a visible detail and the
  party investigates it, they find what it leads to. This is how Hidden locations are
  reached.
- **A Clue needs its Trigger.** A Secret is found by acting on the clue as stated - no
  roll. If the party has not found the clue, no amount of searching substitutes.
- **A general search of a space costs one action and finds something on 1 in 6.** This
  covers looking for what has not been hinted at. In DANGEROUS regions the search also
  advances the Danger countdown.
- **Searching is declared against a thing, not a room.** "We search the room" gets the
  1-in-6. "We look behind the tapestry" gets what is behind the tapestry.

## Time

Time is tracked at the scale the region's rating sets, stated in each Region Overview.

- **SAFE** - not time-bound. Do not track hours unless something specific demands it.
- **WILD** - 4 hours per action. Travel between landmarks, tracking, foraging, searching a
  landmark, and setting a camp each cost one slot. Four slots to a day.
- **DANGEROUS** - the Danger table's countdown replaces real time. It counts down from 6
  on each failed Difficulty roll, and on each action taken that the region would notice.

## Scaling

Three different things carry Action Dice, and they are **three different scales**. They are
not interchangeable, and comparing one to another directly is a category error.

**Players** - 1 to 6 dice, of any size from d4 to d12. A d6 is average. Six d12 is the
theoretical ceiling and not something an ordinary character reaches.

**Creatures** - d6 only, never any other size. The die *count* runs 1 to 18, and a flavour
bonus of -2 to +6 tunes an entry within its band. Creature AD reads roughly as classic
Hit Dice, which is the useful reference for pitching a new entry:

| AD | Reads as |
|---|---|
| 1-2 | A person. A common animal. Most of what a settlement contains |
| 3-4 | A big animal, a tough humanoid, an ogre |
| 5-8 | A serious monster. A party fights this carefully, or not at all |
| 9-12 | An adult dragon and its equals. A party should be frightened |
| 13-18 | Legendary. Not meant to be fought by an ordinary party, ever |

**Factions** - d6 only, and **no bonus**. A faction's die count has no absolute meaning: it
is set purely relative to the other factions in the setting, to resolve Faction Turns
against each other. Do not compare a faction's dice to a creature's or a party's.

**Number and scarcity are part of the pitch.** Three creatures at 2 AD is a different
proposition from one at 6, and neither is captured by the dice alone. State how many, and
how often the party is likely to meet them.

**There is no balance to hit.** A location is not sized to what the party can beat. Some
things in the setting will kill them, and the skill the game rewards is recognising which
- that three orcs are worth fighting and the spectre is not. This is what
`setting/Bestiary.md`'s **Sign** and **Disposition** fields are for: they are how a party
learns what it is facing *before* committing, and they are what make the choice a judgement
rather than a gamble.

## Region Dice

A region's die (d4 to d12) is a **difficulty die**, not a power level. It is rolled to
determine whether the region's Events, Encounter, or Danger table comes up, and a smaller
die fails more often. So the scale runs opposite to intuition:

| Die | Means |
|---|---|
| d4 | Outlier. Punishing. Rare, and deliberate |
| d6 | Slightly tougher than typical |
| **d8** | **Baseline. Typical for a region of this rating** |
| d10 | Slightly easier than typical, and still common |
| d12 | Outlier. Mild. Rare, and deliberate |

**The die is not a creature benchmark.** A d8 DANGEROUS region does not want an 8 AD
creature; it wants creatures pitched against the party. Difficulty and power are separate
axes.

### The Difficulty roll

Roll the region's die:

- **1** - failure. The region's Encounter or Danger table fires.
- **2-3** - complication. The attempt works, but not cleanly.
- **4 or higher** - success.

| Die | Failure | Complication | Success |
|---|---|---|---|
| d4 | 25% | **50%** | 25% |
| d6 | 16.7% | 33.3% | 50% |
| **d8** | **12.5%** | **25%** | **62.5%** |
| d10 | 10% | 20% | 70% |
| d12 | 8.3% | 16.7% | 75% |

**Complication is the most common non-success at every die**, and at d4 it is the most
common result of all. A punishing region is not one where you fail often - it is one where
you rarely get away clean. Region tables fire on failure, so complications are narrated
from the region's own material: its Terrain and Foraging in WILD, its Architecture and
Features in DANGEROUS.

### Why the location counts are what they are

Location count is not a heuristic. It is the mechanism, and it produces the same pressure
curve at every die.

**WILD - about as many locations as the die.** Traversing the whole region rolls the die
about N times at a 1/N failure rate:

> Expected encounters per full traverse = **exactly 1**, at every die.
> Chance of at least one = **about 65%**, at every die (it converges on 1 - 1/e).

**DANGEROUS - about three times the die.** Clearing the whole region rolls about 3N times
at 1/N, against a Danger track that counts down from 6:

> Expected countdown steps per full clear = **exactly 3** - half the track, at every die.
> Chance of burning the whole track = **8.4%**, at every die.

So a full clear leaves the party at 3 of 6 on average. The place is clearable, and anything
inefficient - backtracking, searching, retreating and returning - eats into a half-track
that was never generous. That is the pressure to get in and get out, and it is built into
the sizing rather than imposed by the referee.

**The die changes pacing and variance, never expected friction.** A d4 WILD region is four
locations with a 25% bite each - short and spiky. A d12 is twelve locations at 8.3% - long
and smooth. Both average one encounter. Choose the die for the *texture* of the region, not
for how hard it is.

**Deviating from the count is a deliberate trade, and now a measurable one.** Half the
locations is half the pressure. A five-room lair written as its own DANGEROUS region at d8
expects 0.6 countdown steps across a full clear - effectively none - so its tension has to
come from what is in it, not from the track.
