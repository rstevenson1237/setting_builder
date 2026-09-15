# Region - Dangerous

## Provides
What a DANGEROUS Region Overview says, how many locations the region holds and in what
mix, and what shape its connection graph takes.

## Read at
**Mode: entry.** Step 3c, drafting `setting/region/[Code].md` for a DANGEROUS region,
alongside `GENRE.md`, `setting/region/Regions.md`, and the setting-level artifacts the
region draws on. Read again at 4a and 4b, which take their counts and graph shape from
here.

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

Class distribution, and entrances scaled by count:

The die is a **difficulty die**, not a power level - d8 baseline, d6 tougher, d10 easier,
per `setting/Procedures.md`. It sets the entrance count below through the location count
only; it is not a benchmark for creature AD.

```
CLASS MIX
  30%   HIGH
  50%   MEDIUM
        LOW - the rest, and not a quota of its own

ENTRANCES - by location count
  ~12 locations    1-2 entrances
  ~24 locations      2 entrances
  ~36 locations    2-3 entrances
```

**MEDIUM is the largest class, and the mix does not slide with size.** A region is
mostly rooms that present one thing to deal with and present it plainly, because that
is the only class that guarantees the party something to act on -
`dangerous/Low.md` draws no challenge at all by definition, so a region that is half
LOW is half rooms with nothing in them to address.

LOW is what is left over rather than a target to fill. It still earns its place: a
dungeon with no unremarkable rooms has nothing to make its remarkable ones legible,
and a room that looks like nothing is what makes attention a real cost. But it is the
residue of the count, so a region that comes out a room or two either side of 20% LOW
has not failed anything - a region that comes out half LOW has.

Connection graph:

```
TOPOLOGY - dense, few entrances
  1     Every location reachable from an entrance
  1     At least one loop (3+ locations) - a path that returns without backtracking
  1     At least one divide - a choice that does not reconverge
  1     At least one branch (many), per 12 locations - a choice of three or more exits
  60%   A dead end, per 12 locations
  40%   Of those dead ends: appears as dead end instead - a hidden (-.-) edge is the real
        exit, cashing out the dead-end Secret rate in `dangerous/Low.md` as a route
        rather than a cache
```

Edges are typed when the diagram is drawn at 4b, and `dangerous/Door.md` reads that type
rather than choosing one. The mix is therefore decided here, and it has to be decided
here: left to per-edge judgement every edge comes out open, because open is the type that
needs no reason.

```
EDGE KIND MIX - over a region's location-tier edges
  60%   open        (---)
  15%   secret      (-.-)
  15%   vertical    (---|vertical|)
  10%   one-way     (-->)
```

**Blocks - a DANGEROUS region is generated one block at a time**, per STEPS.md 4c:

```
BLOCKS
  1     Every location belongs to exactly one block
  1     Each block is one functional quarter - its locations share a purpose family
        from dangerous/Dressing.md
  1     No two blocks in a region share a purpose family
  12-20 locations per block; a region of 12 or fewer is a single block
```

The quarter is what holds a block together and what sharpens it: a barracks range, a
kitchen and its stores, a run of private cells are each answering a different question about
the same place. It is also the scale at which `dangerous/Dressing.md`'s bar on reusing a
purpose can actually be met - the Purpose list holds 63 nouns, which no hundred-location
region could spread across itself.

**LOW distribution - this is where the graph's shape has to actually show up.** LOW is
the class most likely to be drawn as plain corridor, so it is the one the graph has to
argue with:

```
LOW SHAPE MIX - of a region's LOW-weight locations, measured on the assembled graph
  60%+  A degree other than 2 - not a plain through-connection
  1     No single degree class - 1, 2, 3, 4+ - accounts for more than a third
```

Degree is a coarse instrument and the rule is a warning rather than a bar: a location on a
loop has degree 2 and reads here as a corridor, so a loop-heavy region will look flatter
than it plays. Read a failure as a question, not a verdict.

A region where every dead end, branch and divide landed on a HIGH or MEDIUM location while
every LOW location sat between two neighbours has technically satisfied the graph-wide counts
above while failing this rule - the counts are necessary, not sufficient, and this is the
check that catches it.

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
- **Layout** - state the region's **kind** first (collection or single holding, per the
  REGION KIND spec above) - the same decision that already sets its location count, now
  written where the referee can read it. Then the shape of the complex, its entrances, and
  how deep it runs. Name roughly where its most notable Features or Dangers (below)
  actually sit, so a referee can place them, not just know they exist. State that time runs
  on the Danger countdown rather than in hours.
- **Features** - the environmental facts that apply throughout: water, air, light, footing,
  what carries sound, what a fire does here.
- **Dangers** - how the place answers intrusion. Some places sleep and some are awake to
  it. State which, and what wakes it.
- **Creatures** - who lives here, what they eat, where their water comes from, where their
  waste goes, and where their young are. Reference the Bestiary by name; add what is
  specific to this group - what they guard, carry, or know.
- **Factions** - whether any of the three hold part of this place as a position, distinct
  from merely living here (per `dangerous/Faction.md`'s off-site-consequence test). Name
  which rooms or sections, if any - a faction is often exactly the "current squatter" the
  Overview's three-occupancy structure above already gestures at. State none if nothing
  here answers to an outside power.
- **Secrets** - what may be revealed about the setting's past, and what hidden ways exist.
- **Treasure** - what rewards exploration, and which of the five tables the region leans on.
- **Tables** - a d6 Danger table, counting down from 6 with each failed Difficulty roll.
  Entry 6 is the place noticing; entry 1 is the place acting.

## Constraints
