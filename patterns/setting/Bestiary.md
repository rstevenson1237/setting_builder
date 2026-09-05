# Setting - Bestiary

## Decides
What creatures the setting holds - how they are distributed across type and power, and
what each entry must state so the location patterns can use it without reinventing it.

## Read at
Step 2e, right after `setting/Setting.md`. The Bestiary is written in one pass rather than
grown, so it has to anticipate demands made several steps later.

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
AD SPREAD - anchored to what GENRE.md's lethality establishes the party can survive, NOT
to the region dice
  1     At least six entries at 1-2 AD      - people, common animals, numbers
  1     At least six entries at 3-4 AD      - the working middle of the setting
  1     At least four entries at 5-8 AD     - fought carefully, or not at all
  1     At least two entries at 9+ AD       - the party should be frightened
  1     At least one entry the party is NOT meant to beat
  1     No more than a third of entries sharing a single AD value
```

**AD, bonus, and MA.** A creature's Action Dice are d6 only, counted 1 to 18 - the count
reads roughly like classic Hit Dice, and it is never sized up or down the way a player's
dice are: a tougher creature gets more d6s or a bigger bonus, never a d8. The bonus runs
-2 to +6 and is written after the dice count (`4d6+2`); most entries carry none at all. MA
(Movement Allowance) is optional and stated only when a creature's speed materially
matters - something that outpaces the party, or can't be outrun - as a single number, 1-6,
read against a person's own walking pace of 3; most entries omit it.

## Patterns

**Entry fields, and which pattern demands each**

- **Description** - appearance and behaviour, 1-3 sentences. Every file.
- **Range** - where it lives, how many the country supports, and what it eats.
  Demanded by `wild/Creature.md` (populations, not individuals), `wild/Lair.md` (what it
  eats and where that comes from), and `dangerous/Creature.md` (household logistics).
- **Sign** - what a party finds before they find the creature: marks or tracks left, a
  sound, or a smell that can be detected before the creature itself is seen. Demanded by
  both Creature files: a creature's signs should reach the party before the creature does,
  at least once per region, and that only works if the signs are decided once here rather
  than improvised per location.
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

## Constraints

**What does not go here.** Unique individuals belong in `setting/NamedCreatures.md`; a
creature that is also a power in the world carries a `setting/Factions.md` entry as well.
A one-off variant is described inline at its location. The Bestiary holds only what
recurs - if an entry will be used once, it is not a template.
