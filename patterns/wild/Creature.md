# Wild - Creature

## Provides
What lives in or ranges through a WILD location, and how it meets a party. Scaling is in
`patterns/setting/Bestiary.md`. Distinct from `wild/Faction.md`, what a place is held or
worked by, and from `wild/Hazard.md`'s living mechanisms, which want nothing.

## Spec

```
CREATURE
  1     Bestiary entry, or an inline description where none fits, and the demeanour it
        carries here                                    (genre: demeanours)
  1     Number - how many the country supports, from the entry's Range
  1     Scale - pitched against party altitude, not the region die. Usually something a
        party can handle or avoid; occasionally something they cannot, and must read
  1     How it meets the party, and whether it has noticed them first
                                                (genre: creature-encounter-outdoors)
  1     Reaction - most things met in the open would rather not fight, and a party that
        assumes otherwise should be able to be wrong  (genre: creature-signalling)
  1     Its limit - the ground, depth, light, or distance it will not cross
  40%   Range - it is not only here, and the party may meet it elsewhere in the region
  30%   Absent, with signs of it, and elsewhere in the region right now
                                                        (genre: creature-sign)
  25%   People rather than wildlife, and the disposition they carry
                                                (genre: travellers, dispositions)
```

**A WILD creature is usually avoidable, and that is the point.** State the limit and stop:
where a thing will not go is a fact about the thing, and what going around costs is the
party's to find out. Per `GENRE.md`, a line saying the way around is free has made their
decision for them.

## Constraints

- **A WILD region holds a population, not an individual.** State how many the country
  supports and where they go when they are not here. A single creature written as though it
  were the only one of its kind belongs in a lair, not a landmark.
