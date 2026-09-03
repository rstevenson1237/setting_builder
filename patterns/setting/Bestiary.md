# Setting - Bestiary

## Decides
What creatures the setting holds, how they are distributed across type and power, and what
each entry must state so the location patterns can use it without reinventing it.

## Read at
Step 2e, after `setting/Outline.md` has fixed the region dice. The Bestiary is written in
one pass rather than grown, so it has to anticipate demands made three steps later.

## Spec

```
TYPE MIX - about 20 entries
  40%   Beast              - natural animals, however large or dangerous
  20%   Man                - bandits, soldiers, cultists, mundane human threats
  15%   Humanoid           - non-human peoples with their own culture and society
  15%   Undead             - death-tainted; the mythic underworld's own population
  10%   Everything else    - Fantasy Creature, Construct, Horror, Wyrm, Fey, Fiend, Giant,
                             combined. Rarely more than two of these types in one setting
```

```
AD SPREAD - anchored to the region dice in setting/Outline.md
  1     At least two entries ABOVE the largest DANGEROUS die
  1     At least three entries within 1 of each region's die
  1     At least four entries at 2d6 or below
  1     No more than a third of entries sharing a single AD value
```

**The AD spread is the part that fails silently.** `dangerous/Creature.md` requires a
high-weight location's creature to sit *above* its region's die; `wild/Creature.md`
requires one at or below. A Bestiary written without the dice in view will cluster in the
middle and leave the high-weight spec unsatisfiable - and that does not surface until
step 4c, when every region is already laid out.

## Patterns

**Entry fields, and which pattern demands each**

- **Description** - appearance and behaviour, 1-3 sentences. Every file.
- **Range** - where it lives, how many the country supports, and what it eats.
  Demanded by `wild/Creature.md` (populations, not individuals), `wild/Lair.md` (what it
  eats and where that comes from), and `dangerous/Creature.md` (household logistics).
- **Sign** - what a party finds before they find the creature. Demanded by both Creature
  files: a creature's signs should reach the party before the creature does, at least once
  per region, and that only works if the signs are decided once here rather than
  improvised per location.
- **Disposition** - what it does on being met, before anyone decides to fight. Demanded by
  `wild/Creature.md`: most things met in open country would rather not fight, and a party
  should be able to be wrong about that.

**Coverage the location patterns will ask for**

- Something that ranges rather than lairs, so a WILD region can meet the same thing twice.
- Something that lairs and cannot leave - young, stores, or a thing it guards.
- Something a party can talk to.
- Something that will not fight and is a problem anyway.
- Something small enough to be a nuisance in numbers.
- Something that eats what a settlement produces, so a SAFE region has a standing grievance.
- Something death-tainted that is a fact of the underworld rather than a villain.
- Something that was made rather than born.

**What does not go here.** Unique individuals belong in `setting/NamedCreatures.md`; a
creature that is also a power in the world carries a `setting/Factions.md` entry as well.
A one-off variant is described inline at its location. The Bestiary holds only what
recurs - if an entry will be used once, it is not a template.

## Constraints
*(Empty. Entries arrive from generation testing, never from anticipation.)*
