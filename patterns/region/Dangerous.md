# Region - Dangerous

## Decides
What a DANGEROUS Region Overview says, how many locations the region holds and in what
mix, and what shape its connection graph takes.

## Read at
Step 3c, drafting `setting/region/[Code].md` for a DANGEROUS region, alongside `GENRE.md`,
`setting/region/Regions.md`, and the setting-level artifacts the region draws on. Read
again at 4a and 4b, which take their counts and graph shape from here.

## Spec

Location count is set here, not by a fixed multiplier. Pick the region's kind first:

```
REGION KIND
  {collection | single holding}

  collection      - a worked complex: a dungeon, a mine, a barrow field, a sunken quarter.
                    Count defaults to 3x the die.
  single holding  - one inhabitant's lair realized as a region. Count is what the holding
                    actually contains, usually 5-8, and padding it to a multiplier is
                    the failure this option exists to prevent.
```

**The 3x rule is the pressure mechanism, not a rule of thumb.** Per
`setting/Procedures.md`, 3x the die across a full clear burns **exactly 3 of the Danger
track's 6 steps**, at every die size - so a clean sweep leaves the party half-spent and
anything inefficient costs real ground.

A **single holding** deviates from that deliberately and pays for it: five rooms at d8
expects 0.6 steps across a full clear, which is effectively no countdown at all. Its
tension has to come from what is in it - one thing that cannot be fought, a way in that is
not a way out, something that wakes - because the track will not supply any.

Class distribution, scaled by count:

The die is a **difficulty die**, not a power level - d8 baseline, d6 tougher, d10 easier,
per `setting/Procedures.md`. It sets the class mix below through the location count only;
it is not a benchmark for creature AD.

```
CLASS MIX
  ~12 locations    1-2 entrances    15% HIGH    40% MEDIUM    45% LOW
  ~24 locations      2 entrances    10% HIGH    35% MEDIUM    55% LOW
  ~36 locations    2-3 entrances     8% HIGH    32% MEDIUM    60% LOW
```

LOW is the largest class and grows fastest with size. A dungeon with no unremarkable rooms
has nothing to make its remarkable ones legible, and connective space is where the
region's decisions get made rather than where its filler goes.

Connection graph:

```
TOPOLOGY - dense, few entrances
  1     Every location reachable from an entrance
  1     At least one loop - a path that returns without backtracking
  1     At least one divide - a choice that does not reconverge
  60%   A dead end, per 12 locations
  30%   A one-way connection
```

## Patterns

The Region Overview's fields, for a DANGEROUS region.

- **Overview** - what this place was, who broke it, and what is in it now. Three
  occupancies is the target: builder, later occupier, current squatter. Not all three need
  still be present.
- **Ambiance** - sensory only: smell, sound carrying through the whole place, temperature,
  humidity. Material and construction belong to Architecture.
- **Architecture** - what it is built from and how well. One motif that repeats throughout
  and ties the rooms together as one work - an arch shape, a carved mark, a masonry
  pattern, a way of cutting stairs. Typical ceiling height and passage width, so rooms
  default to them unless their own notes say otherwise.
- **Layout** - the shape of the complex, its entrances, and how deep it runs. State that
  time runs on the Danger countdown rather than in hours.
- **Features** - the environmental facts that apply throughout: water, air, light, footing,
  what carries sound, what a fire does here.
- **Dangers** - how the place answers intrusion. Some places sleep and some are awake to
  it. State which, and what wakes it.
- **Creatures** - who lives here, what they eat, where their water comes from, where their
  waste goes, and where their young are. Reference the Bestiary by name; add what is
  specific to this group - what they guard, carry, or know.
- **Secrets** - what may be revealed about the setting's past, and what hidden ways exist.
- **Treasure** - what rewards exploration, and which of the five tables the region leans on.
- **Tables** - a d6 Danger table, counting down from 6 with each failed Difficulty roll.
  Entry 6 is the place noticing; entry 1 is the place acting.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
