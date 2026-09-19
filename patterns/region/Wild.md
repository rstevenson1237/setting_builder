# Region - Wild

## Provides
What a WILD Region Overview says, how many locations it holds and in what mix of
classifications, and what shape its connection graph takes.

## Spec

```
LOCATION COUNT
  About as many as the die type. A d10 region holds about ten.
  This is the pressure mechanism, not a rule of thumb: N locations at a 1/N failure rate
  means a full traverse expects exactly ONE encounter, at every die, with about a 65%
  chance of at least one. See setting/Procedures.md.
  The die therefore sets texture, not difficulty. A d4 region is four locations that bite
  a quarter of the time - short and spiky. A d12 is twelve at 8.3% - long and smooth.

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
  1     Depth stops at three - a Secret carries no children of its own
  20%   A Landmark that connects onward to a neighbouring region
```

Landmarks do not interconnect. A party roams the region and finds them; depth happens
below a Landmark, not between them.

**This graph is what the parents' lead lines answer to.** Deciding here which parents carry
children is deciding how much of the region's content sits behind something, and a child
whose parent states nothing is unreachable.

The Region Overview's fields, for a WILD region.

```
FIELDS
  1     Overview   - what this stretch of country is, who uses it and for what, and why it
                     has not been settled or cleared. A reason it stays that way is worth
                     stating
  1     Ambiance   - what it looks, sounds and smells like across the whole region, and how
                     weather and season change it
  1     Terrain    - the ground itself, and how hard it is to move through beyond what
                     Layout's distances imply. This field carries the connective texture the
                     referee narrates between points, which is more work than its length
                     suggests
  1     Foraging   - plants, huntable wildlife and geological goods findable here, how rare,
                     and what they are called locally. Anything dangerous enough to be an
                     encounter belongs in Creatures. Healing or magical value stays rare and
                     priced, per GENRE.md
  1     Layout     - no separate type field; Terrain carries that. The region's shape and
                     extent, distances between Landmarks in yards or miles, and roughly
                     where its notable Features and Dangers sit. State that an action costs
                     four hours, and what one buys: a move, a search, a forage, a tracking
                     attempt, or making camp
  1     Features   - what a party interacts with across the region rather than at one point:
                     crossings, weather, footing, what can be seen from high ground, what
                     the region does at night
  1     Dangers    - how the region answers intrusion. Some country is indifferent and
                     merely lethal; some is watched
  1     Creatures  - what lives here, its range, and how it meets a party. Bestiary by name,
                     plus what is specific to this population
  1     Factions   - whether any of the three claim ground here, and how much: a held
                     Landmark, a route kept open or shut, a stretch worked for what it
                     yields. Name which; none where the region is genuinely unclaimed
  1     Secrets    - what the region hides, and roughly where. Enough that the Secret-tier
                     locations have somewhere to come from
  1     Treasure   - what rewards exploration here, and which tables the region leans on
  1     Tables     - a d6 Encounter table, rolled on each failed Difficulty roll
```

## Constraints
