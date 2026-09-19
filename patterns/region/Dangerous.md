# Region - Dangerous

## Provides
What a DANGEROUS Region Overview says, how many locations the region holds and in what
mix, and what shape its connection graph takes.

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
`setting/Procedures.md`, 3x the die across a full clear burns exactly 3 of the Danger
track's 6 steps at every die size, so a clean sweep leaves the party half-spent.

A **single holding** deviates deliberately and pays for it: five rooms at d8 expects 0.6
steps across a full clear, which is no countdown at all. Its tension has to come from what
is in it - one thing that cannot be fought, a way in that is not a way out, something that
wakes.

The die is a **difficulty die**, not a power level - d8 baseline, d6 tougher, d10 easier. It
sets the entrance count through the location count only.

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

**MEDIUM is the largest class, and the mix does not slide with size.** It is the only
class that guarantees the party something to act on, so a region that is half LOW is half
rooms with nothing in them to address. LOW is the residue of the count rather than a target
to fill - a room or two either side of 20% has failed nothing; half LOW has.

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

Edges are typed at 4b and `dangerous/Door.md` reads that type rather than choosing one, so
the mix is decided here: left to per-edge judgement every edge comes out open, because open
is the type that needs no reason.

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

**The family names what the quarter is for, not what every room in it was.** A block's rooms
take whichever purposes *serve* its family: a Believing quarter has its chapel and its vestry
and also the passage the procession walked, the archive its rite was recorded in, and the pit
its offerings went into. What the family rules out is a room serving some other quarter's
question - a barracks in a temple block belongs to the block that is about holding people, or
the region has one block too few. The quarter is also the scale at which
`dangerous/Dressing.md`'s bar on reusing a purpose can actually be met.

**LOW distribution.** LOW is the class most likely to be drawn as plain corridor, so it is
the one the graph has to argue with:

```
LOW SHAPE MIX - of a region's LOW-weight locations, measured on the assembled graph
  60%+  A degree other than 2 - not a plain through-connection
  1     No single degree class - 1, 2, 3, 4+ - accounts for more than a third
```

Degree is a coarse instrument and the rule is a warning rather than a bar - a location on a
loop has degree 2 and reads here as a corridor. A region where every dead end, branch and
divide landed on a HIGH or MEDIUM location while every LOW location sat between two
neighbours satisfies the graph-wide counts above and still fails this rule, which is what it
is for.

The Region Overview's fields, for a DANGEROUS region.

```
FIELDS
  1     Overview     - what this place was, who broke it, and what is in it now. Three
                       occupancies is the target: builder, later occupier, current squatter
  1     Ambiance     - sensory only: smell, sound carrying through the whole place,
                       temperature, humidity
  1     Architecture - what it is built from and how well; one motif repeating throughout;
                       typical ceiling height and passage width, so rooms default to them
  1     Layout       - the region's kind first, then the shape of the complex, its
                       entrances, how deep it runs, and roughly where its notable Features
                       and Dangers sit. State that time runs on the Danger countdown
  1     Features     - the environmental facts that apply throughout: water, air, light,
                       footing, what carries sound, what a fire does here
  1     Dangers      - how the place answers intrusion: whether it sleeps or is awake to
                       it, and what wakes it
  1     Creatures    - who lives here, what they eat, where their water comes from, where
                       their waste goes, where their young are. Bestiary by name, plus what
                       is specific to this group
  1     Factions     - whether any of the three hold part of this place as a position,
                       distinct from living here; which rooms or sections; none if nothing
                       here answers to an outside power
  1     Secrets      - what may be revealed about the setting's past, and what hidden ways
                       exist
  1     Treasure     - what rewards exploration, and which of the five tables the region
                       leans on
  1     Tables       - a d6 Danger table counting down from 6 with each failed Difficulty
                       roll. Entry 6 is the place noticing; entry 1 is the place acting
```

## Constraints
