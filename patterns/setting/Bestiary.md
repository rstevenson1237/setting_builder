# Setting - Bestiary

## Provides
What one Bestiary entry states: what kind of thing it is, how dangerous it is, and what a
party can perceive of it before a fight starts. How many entries the Bestiary holds and how
they divide across type and power is `templates/setting/Bestiary.md`'s. What AD is, and that it is
never read against a faction's or a region's dice, is `setting/Procedures.md`'s Scaling.

## Spec

```
BESTIARY ENTRY
  1     Type                                                              {TYPE}
  1     AD - written Xd6+N - the count, from the band that says what the creature is
                                                                          {AD BAND}
  1     Modifier - -2 to +6, against an average of one third of AD rounded up - how much
        more or less lethal it is than its size says
  1     MA - against an average of one quarter of AD rounded up - how many targets it
        threatens at once, from speed, reach, or more than one attack
  1     Description - what a party sees when it comes into view
  1     Range - where it lives, how many of it the country supports, and what it eats
  1     Sign - what reaches a party before the creature does
                                        {a mark | a track | a sound | a smell}
  1     Disposition - what it does on being met, before anyone decides to fight
  1     Special - what it can do that its dice do not already say, in terms a referee
        can run, or `none`: rare below 4 AD, expected at 4 and above, several at 8 and
        above
```

```
TYPE - exactly one
  Men         - human beings, of any people, trade or allegiance
  Humanoid    - a people that is not human, walking upright, speaking, and making things
  Beast       - an animal, of natural kind or grown past natural size
  Undead      - a dead thing that has not stopped
  Construct   - a made thing, set to a task and holding to it
  Horror      - a thing of no natural kind, whose nature is itself the danger
  Wyrm        - a great reptile of the dragon line
  Fey         - a being of the wild places, bound by rules of its own rather than wants
  Fiend       - a thing from outside the world, come or called into it
  Giant       - a people of human shape at more than twice human size
  Fantasy     - what this setting has that fits none of the above
```

```
AD BAND - exactly one, then the count within it
  1           evenly matched for a normal man
  2-3         a superior man-sized combatant
  4-5         larger than man-sized, and highly dangerous
  6-8         extremely large, carrying some level of supernatural danger
  9-12        a gargantuan terror, often solo
  13-16       mono-type - served by those around it, in control without question, and
              tapped into powers beyond comprehension
  17-18       gargantuan - the pinnacle, a titan
```

## Constraints

- **One stat block is one creature** - or one swarm of things not dangerous on their own,
  counted and fought as a single thing. Never a group rate for something individually a
  threat: two of those are two stat blocks' worth of trouble.

- **Never size a creature's dice up or down.** Action Dice are d6 only; a tougher creature
  gets more of them or a bigger modifier, never a d8.

- **What does not go here.** Unique individuals belong in `setting/NamedCreatures.md`; a
  creature that is also a power in the world carries a `setting/Factions.md` entry as well.
  A one-off variant is described inline at its location. The Bestiary holds only what
  recurs - a proper name on a Bestiary entry is the surest sign it is in the wrong file.

- **Ordinary wildlife is region texture, not a Bestiary entry.** What a country typically
  holds - game, birds, the snake underfoot - belongs to a WILD region's Loot and
  Inhabitants fields. A Beast earns an entry here only by being an unusual combatant a
  location will actually draw.

- **Mundane human threats are a faction's, not a type's.** Who opposes the party and why
  is `setting/Factions.md`'s question, and a human worth naming is
  `setting/NamedCreatures.md`'s. What remains for `Men` is the rank and file a faction
  fields; a separate entry per human occupation is a roster with no faction behind it.

- **Guardian and hazard are roles, never Types.** Either is built from whichever Type
  actually fits, and its Special carries the role. A guardian holds one thing, does not
  range or forage, and states the condition it acts on rather than naming itself a
  guardian. A hazard is a recurring danger with a stat line, cited by name wherever it
  turns up - and not a location's Hazard entry, which is one location's mechanism. Anything
  with a want, a reaction, or somewhere else to be is an ordinary creature of its Type;
  anything that exists in one place only belongs inline at that location.
