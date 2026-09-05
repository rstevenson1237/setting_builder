# Setting - Bestiary

## Decides
Party altitude, and what creatures the setting holds - how they are distributed across type
and power, and what each entry must state so the location patterns can use it without
reinventing it.

## Read at
Step 2e, right after `setting/Setting.md`. Party altitude is fixed here, first, since
nothing before this step needed it. The Bestiary is written in one pass rather than grown,
so it has to anticipate demands made several steps later.

## Spec

```
PARTY ALTITUDE
  1     What the characters are, and what they can expect to survive, stated in dice
```

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
AD SPREAD - anchored to party altitude, fixed above, NOT to the region dice
  1     At least six entries at 1-2 AD      - people, common animals, numbers
  1     At least six entries at 3-4 AD      - the working middle of the setting
  1     At least four entries at 5-8 AD     - fought carefully, or not at all
  1     At least two entries at 9+ AD       - the party should be frightened
  1     At least one entry the party is NOT meant to beat
  1     No more than a third of entries sharing a single AD value
```

**Creature AD is pitched against the party, never against the region die.** A d8 DANGEROUS
region does not want an 8 AD creature - the die is a difficulty die and the AD is a power
count, and they are separate axes. See `setting/Procedures.md`.

**The last line is the important one.** OSR play rewards recognising that three orcs are
worth fighting and the spectre is not, and that judgement is only available if the setting
actually contains a spectre. A Bestiary where everything is beatable has removed the
decision. Write at least one entry that will kill the party if they engage it, and give it
the clearest **Sign** and **Disposition** in the file - those two fields are how a party
learns what it is facing before committing, and they are what turn an unwinnable fight
into a judgement rather than an ambush.

**Numbers are part of the pitch.** State in Range how many the country supports. Six at
2 AD and one at 6 AD are different problems, and the dice alone do not say which one a
location is offering.

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
