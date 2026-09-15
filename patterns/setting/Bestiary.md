# Setting - Bestiary

## Provides
What creatures the setting holds - how they are distributed across type and power, and
what each entry must state so the location patterns can use it without reinventing it.

The Bestiary is written in one pass rather than grown, so it has to anticipate demands
made several steps later.

## Spec

```
TYPE MIX - about 20 entries
  20%   Beast              - unusual combatants only, never the region's ordinary wildlife
  10%   Man                - the rank and file a faction fields
  15%   Humanoid           - non-human peoples with their own culture and society
  15%   Undead             - death-tainted; the mythic underworld's own population
  15%   Guardian           - made or bound to hold one thing, and does nothing else
  10%   Hazard             - a living or persisting danger that is a fact of a place
  15%   Everything else    - Fantasy Creature, Construct, Horror, Wyrm, Fey, Fiend, Giant,
                             combined. Rarely more than two of these types in one setting
```

```
AD LADDER - what a count means, in absolute terms
  1       Evenly matched for a normal man
  2-3     A superior man-sized combatant
  4-5     Larger than man-sized, and highly dangerous
  6-8     Extremely large, carrying some level of supernatural danger
  9-12    A gargantuan terror - often solo, and still a fight rarely worth taking
  13-16   Mono-type: expects to be served by those around it, controls without
          question, and is tapped into powers beyond comprehension
  17-18   Gargantuan, the pinnacle, a titan
```

```
AD SPREAD - anchored to what GENRE.md's lethality establishes the party can survive,
NOT to the region dice
  1     At least six entries at 1-3 AD    - people, numbers, the things underfoot
  1     At least six entries at 4-8 AD    - the working middle of the setting
  1     At least two entries at 9-12 AD
  1     At least one entry at 13+
  1     At least one entry the party is NOT meant to beat
  1     No more than a third of entries sharing a single AD value
```

**One stat block is one creature** - or one swarm of creatures that are not dangerous on
their own, counted and fought as a single thing. A stat block is never a group rate for
something that is individually a threat: two of those are two stat blocks' worth of
trouble, and the referee needs to be able to say so.

**AD.** Action Dice are d6 only, counted 1 to 18, and never sized up or down the way a
player's dice are: a tougher creature gets more d6s or a bigger bonus, never a d8. Read
the count against the ladder above, which is absolute - what the creature *is* - and not
against the region's die, which is a difficulty die and says nothing about power.

**The modifier carries the information the count cannot.** It runs `-2` to `+6` and is
written after the dice count (`4d6+2`). **Its average is one third of AD, rounded up** -
so a 4 AD creature averages `+2`, a 9 AD creature `+3`, an 18 AD creature `+6`. Write it
on every entry. The point is the deviation: a creature above its average is more lethal
than its size suggests, one below is less, and a referee reads that difference straight
off the line. An entry that sits on the average every time has thrown the field away.

**MA is the ability to attack multiple targets at once** - from speed, from size, from
having more than one attack to make. **Its average is one quarter of AD, rounded up**, and
it reads the same way the modifier does: deviation is the information. A thing with one
mouth and no reach sits below its average however large it is; a thing that is fast, or
long, or many-limbed sits above it.

**A creature may have a special ability.** More often at 4 AD and above, and an entry at
8 AD and above is expected to carry several. Below 4 it is rare, and a 1 AD creature with
one is making a claim the rest of its line has to support. State what the ability does in
terms a referee can run, never as a name alone.

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
- **Special** - what it can do that its Action Dice do not already say, where the AD band
  calls for one. `none` where it has none, per GENRE.md's state-the-nil. Demanded by
  `dangerous/Creature.md` and `dangerous/Encounter.md`: a guardian's condition, a hazard's
  mechanism and a horror's reach are the whole of what makes them worth citing, and a
  referee improvising them at the table is improvising the entry.

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
recurs - if an entry will be used once, it is not a template. A proper name on a Bestiary
entry is the surest sign the entry is in the wrong file.

**Ordinary wildlife is region texture, not a Bestiary entry.** What a country typically
holds - the game a party can hunt, the birds overhead, the snake underfoot - belongs to a
WILD region's **Foraging** and **Creatures** fields, which already demand real named
animals. A Beast earns a template here only by being an *unusual* combatant: something a
location will actually draw and a party will actually have to deal with. Filling the type
with the fauna a region would have anyway spends the setting's smallest artifact on
scenery, and leaves the referee looking for the dangerous things among the sparrows.

**Mundane human threats are a faction's, not a type's.** Who opposes the party and why is
`setting/Factions.md`'s question, and a human worth naming is `setting/NamedCreatures.md`'s.
What remains for `Man` is the rank and file a faction fields - the line a party actually
fights - and one or two templates cover every faction in a setting. A separate entry per
human occupation is a roster with no faction behind it.

**A Guardian type does not contradict "a guardian is more often a condition than a
monster."** Per GENRE.md the condition is still the default, and most guardians in a
setting should never need a stat line at all. This type is for the recurring condition
that *is* tested - a thing that will not touch anyone wearing the right mark, until
somebody arrives without one. What makes it a Guardian rather than a Beast or an Undead is
that it holds one thing and does nothing else: it does not range, does not forage, does
not want anything, and its **Special** states the condition it acts on.

**A `Hazard` entry is not `dangerous/Hazard.md`.** That file is the per-location
mechanism - trap, environmental, residual - and it owns clue, trigger and impact for the
one place it is drawn into. A Hazard-type Bestiary entry is a recurring living or
persisting danger with a stat line, cited by name from wherever it turns up rather than
reinvented per room. If it has a want, a reaction, or somewhere else to be, it is a
creature and not a hazard; if it exists in one place only, it belongs inline at that
location.
