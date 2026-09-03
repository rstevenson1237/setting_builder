# Region - Wild

## Decides
What a WILD Region Overview says, how many locations it holds and in what mix of
classifications, and what shape its connection graph takes.

## Read at
Step 3c, drafting `setting/region/[Code].md` for a WILD region. Read again at 4a and 4b,
which take their counts and graph shape from here.

## Spec

```
LOCATION COUNT
  About as many as the die type. A d10 region holds about ten.
  The die is a difficulty die - d8 baseline, d6 tougher, d10 easier. A tougher region is
  therefore smaller and more concentrated, which is a coupling worth using.

CLASSIFICATION MIX
  50-60%   Landmark   - freely discoverable anywhere in the region
  30-40%   Hidden     - reached from a specific parent Landmark's visible detail
  10-20%   Secret     - reached only through a Clue/Trigger/Payload at a parent
```

Depth is how a WILD region carries weight. Every Landmark sits at the same baseline; a
Landmark that matters more does not get written heavier, it gets **children**. A region
where every Landmark is a bare leaf is flat no matter how well each one is written.

Connection graph:

```
TOPOLOGY - a forest of trees
  1     Every Landmark reachable from the region's entry, independently of the others
  1     At least two Landmarks carrying children
  1     Hidden children connect to their parent with a normal edge
  1     Secret children connect to their parent with a hidden (-.-) edge
  20%   A Landmark that connects onward to a neighbouring region
```

Landmarks do not interconnect. A party roams the region and finds them; depth happens
below a Landmark, not between them.

## Patterns

The Region Overview's fields, for a WILD region.

- **Overview** - what this stretch of country is, who uses it and for what, and why it has
  not been settled or cleared. Points of Light: unoccupied is the default, and a reason it
  stays that way is worth stating.
- **Ambiance** - what the place looks, sounds and smells like across the whole region, and
  how weather and season change it. Architectural style and materials where anything built
  recurs here.
- **Terrain** - the ground itself: a single descriptor or a specific combination. How hard
  it actually is to move through, beyond what Layout's distances imply. **This field
  carries the connective texture the referee narrates between points** - it is doing more
  work than its length suggests, because in a point crawl everything between two landmarks
  comes from here.
- **Foraging** - plants, animals, and geological goods findable here; whether they are rare
  or abundant; what they are called locally. Any purported healing or magical value stays
  rare and priced, per GENRE.md.
- **Layout** - the region's overall shape and extent, distances between Landmarks in yards
  or miles. State that an action costs four hours, and what one action buys: a move
  between neighbouring Landmarks, a search of one Landmark, a forage, a tracking attempt,
  or making camp.
- **Features** - what a party interacts with across the region rather than at one point:
  crossings, weather, footing, what can be seen from high ground, what the region does at
  night.
- **Dangers** - how the region answers intrusion. Some country is indifferent and merely
  lethal; some is watched.
- **Creatures** - what lives here, its range, and how it meets a party - hunting, watching,
  avoiding, following. Reference the Bestiary by name and add what is specific to this
  population.
- **Secrets** - what the region hides, and roughly where. Enough that the Secret-tier
  locations have somewhere to come from.
- **Treasure** - what rewards exploration here, and which tables the region leans on.
- **Tables** - a d6 Encounter table, rolled on each failed Difficulty roll.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
