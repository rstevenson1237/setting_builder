# Setting - Bestiary

## Provides
What one Bestiary entry must state - its type, its Action Dice and what they mean, and
what a party can perceive of it before a fight starts. How many entries the Bestiary holds
and how they divide across type and power is `templates/Bestiary.md`'s Instructions, not
this file's.

## Spec

```
BESTIARY ENTRY
  1     A Type - Men, Humanoid, Beast, Fantasy, Undead, Construct, Horror, Wyrm, Fey,
        Fiend, or Giant. No other Type exists; a creature that does not fit one of these
        is a sign the roster, not the taxonomy, needs to change.
  1     AD, written Xd6+N, read against the ladder below
  1     A modifier, -2 to +6, averaging one third of AD (rounded up)
  1     An MA, averaging one quarter of AD (rounded up)
  1     A Description of 1-3 sentences
  1     A Special where the AD band calls for one, or `none`
```

```
TYPES
  Men         - ordinary mortal humans: bandits, soldiers, cultists, mundane human threats
  Humanoid    - non-human, human-shaped peoples with their own culture and society
              (goblins, orcs)
  Beast       - natural animals, however large or dangerous, with no magical or
              supernatural nature (wolves, giant spiders, bears)
  Fantasy     - catch-all for setting-flavor creatures that aren't natural animals and
              don't fit a sharper category below (griffons, will-o'-wisps)
  Undead      - anything animated by death-tainted or necrotic energy (skeletons,
              ghosts, wraiths)
  Construct   - artificial, non-living bodies, usually magically animated (golems,
              animated armor)
  Horror      - alien or sanity-bending things that sit outside normal nature and magic
              entirely
  Wyrm        - dragons and their draconic kin specifically
  Fey         - otherworldly, fae-touched beings bound by strange rules or bargains
  Fiend       - extraplanar, malevolent entities of infernal or abyssal origin
  Giant       - oversized humanoid-adjacent brutes: giants, ogres, trolls
```

**Guardian and hazard are roles, not Types.** Neither appears in the TYPES list above.
Any Type can be built to fill either role through its Special - see Constraints below for
what each role requires.

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

**Description.** Appearance, behaviour, range, population, diet, sign, and disposition are
all optional points of inclusion - none is mandatory on every entry. Write whichever the
entry actually needs; a Beast that ranges widely might spend its sentences on population
and diet, an entry built as a guardian and fixed at one threshold might spend them
entirely on what it does when approached. Which downstream pattern wants which point:

- **Range** - where it lives, how many the country supports, and what it eats. Wanted by
  `wild/Creature.md` (populations, not individuals), `wild/Lair.md` (what it eats and
  where that comes from), and `dangerous/Creature.md` (household logistics).
- **Sign** - what a party finds before they find the creature: marks or tracks left, a
  sound, or a smell detectable before the creature itself is seen. Wanted by both
  Creature files: a creature's signs should reach the party before the creature does, at
  least once per region, and that only works if the signs are decided once here rather
  than improvised per location.
- **Disposition** - what it does on being met, before anyone decides to fight. Wanted by
  `wild/Creature.md`: most things met in open country would rather not fight, and a party
  should be able to be wrong about that.

**Special** - what it can do that its Action Dice do not already say, where the AD band
calls for one. `none` where it has none, per GENRE.md's state-the-nil. Demanded by
`dangerous/Creature.md` and `dangerous/Encounter.md`: a guardian's condition, a hazard's
mechanism and a horror's reach are the whole of what makes them worth citing, and a
referee improvising them at the table is improvising the entry.

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
What remains for `Men` is the rank and file a faction fields - the line a party actually
fights - and one or two templates cover every faction in a setting. A separate entry per
human occupation is a roster with no faction behind it.

**A guardian is a role any Type can carry, not a Type of its own.** Per GENRE.md a
guardian is more often a condition than a monster, and most guardians in a setting should
never need a stat line at all. Where one does, build it from whichever Type actually fits
- an Undead bound to a tomb, a Construct set at a threshold, even a Beast that is
territorial rather than hungry - and let its **Special** carry the role: it holds one
thing and does nothing else, does not range, does not forage, does not want anything
beyond that, and states the condition it acts on rather than naming it a guardian.

**A hazard is a role any Type can carry, not a Type of its own, and it is not
`dangerous/Hazard.md`.** That file is the per-location mechanism - trap, environmental,
residual - and it owns the clue, the trigger, and what is forced, for the one place it is
drawn into. An entry built as a hazard is a recurring living or persisting danger with a
stat line, cited by name from wherever it turns up rather than reinvented per room - most
naturally a Horror, a Beast, or an Undead. If it has a want, a reaction, or somewhere else
to be, it is an ordinary creature of its Type and not a hazard; if it exists in one place
only, it belongs inline at that location, not here.
