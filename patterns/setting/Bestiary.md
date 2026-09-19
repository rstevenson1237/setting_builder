# Setting - Bestiary

## Provides
What creatures the setting holds - how they are distributed across type and power, and what
each entry must state so the location patterns can use it without reinventing it. Written in
one pass rather than grown, so it anticipates demands made several steps later.

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

```
ENTRY - every row
  1     Description - appearance and behaviour, 1-3 sentences
  1     AD, in d6 only, written with its modifier (4d6+2). The modifier runs -2 to +6 and
        averages one third of AD, rounded up; the deviation is the information
  1     MA - how many targets it can engage at once. Averages one quarter of AD, rounded
        up; the deviation reads the same way
  1     Range - where it lives, how many the country supports, and what it eats
  1     Sign - what a party finds before they find the creature
  1     Disposition - what it does on being met, before anyone decides to fight
                                                        (genre: demeanours)
  1     Special - what it can do that its AD does not already say; `none` where it has
        none, per GENRE.md's state-the-nil. More often at 4 AD and above, and expected in
        several at 8 and above
```

```
COVERAGE - what the location patterns will ask for
  1     Something that ranges rather than lairs
  1     Something that lairs and cannot leave
  1     Something a party can talk to
  1     Something that will not fight and is a problem anyway
  1     Something small enough to be a nuisance in numbers
  1     Something that eats what a settlement produces
  1     Something death-tainted that is a fact of the underworld rather than a villain
  1     Something that was made rather than born
```

**One stat block is one creature** - or one swarm of creatures that are not dangerous on
their own, counted and fought as a single thing. A stat block is never a group rate for
something individually a threat.

## Constraints

- **The Bestiary holds only what recurs.** Unique individuals belong in
  `setting/NamedCreatures.md`; a one-off variant is described inline at its location. A
  proper name on a Bestiary entry is the surest sign the entry is in the wrong file.

- **Ordinary wildlife is region texture, not an entry.** What a country typically holds
  belongs to a WILD region's Foraging and Creatures fields. A Beast earns a template here
  only by being an unusual combatant.

- **Mundane human threats are a faction's, not a type's.** What remains for `Man` is the
  rank and file a faction fields, and one or two templates cover every faction in a setting.

- **A Guardian holds one thing and does nothing else.** It does not range, forage, or want
  anything, and its Special states the condition it acts on. Per `GENRE.md` most guardians
  need no stat line at all.

- **A `Hazard` entry is not `dangerous/Hazard.md`.** That file is the per-location
  mechanism; this type is a recurring living danger with a stat line. If it exists in one
  place only, it belongs inline at that location.
