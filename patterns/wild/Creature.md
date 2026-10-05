# Wild - Creature

## Provides
What lives in or ranges through a WILD location, and how it meets a party. Scaling is
`patterns/setting/Bestiary.md`'s. What holds or works a place is `wild/Faction.md`'s; a
living thing with nowhere else to be and nothing it wants is `wild/Hazard.md`'s.

## Spec

```
CREATURE
  1     Entry - a setting/Bestiary.md entry, or an inline description where none fits
  1     Number - how many the country supports, from the entry's Range, and where the
        rest are when they are not here
  1     Scale - against what GENRE.md's Lethality and Player characters answers say the
        party can survive, never the region die: usually something to handle or avoid,
        occasionally something that must be read and left
  1     Doing - what it is doing                                            {DOING}
  1     Noticed - whether it has noticed the party first                {yes | no}
  1     Reaction - on being met, before anyone decides to fight: most things in the
        open would rather not, and a party that assumes otherwise can be wrong
  1     Limit kind - what it will not cross        {ground | depth | light | distance}
  1     Limit - that limit, marked by a warning or display before it commits
  1     Demeanour - one word for how it carries itself before a fight starts or
        doesn't, for its citation
  40%   Range - it is not only here, and the party may meet it elsewhere in the region
  30%   Absent - absent, with signs of it, and elsewhere in the region right now
```

```
DOING - exactly one
  distant      - seen at a distance
  heard        - heard and not seen
  following    - following the party
  fleeing      - fleeing something else
  between      - already between the party and where they were going
```

## Constraints

- **Never a lone individual in open country.** A single creature written as the only one
  of its kind belongs in a lair, not a landmark.
