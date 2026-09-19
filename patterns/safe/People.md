# Safe - People

## Provides
Which individuals from the region's roster appear at this location, and what makes each
worth remembering. The roster itself is the Region Overview's People field; this file turns
a roster line into somebody at a location.

## Spec

```
PERSON
  1     Name, from the region roster - not invented here
  1     The disposition they carry                      (genre: dispositions)
  1     What they are doing when the party arrives      (genre: people-activity)
  1     One thing distinctive enough to be recalled a session later
                                                        (genre: people-distinctive)
  1     What they want, whether or not they are asking for it
                                                        (genre: people-wants)
  30%   A Named Creature row, where they will recur or be heard of first
  20%   An opinion about the region's Situation that is not the common one
```

**Make them a Named Creature** where they will appear at more than one location, the party
will hear of them before meeting them, or they will be a problem later. Stat them per
`patterns/setting/Bestiary.md`, most often at 1-2 AD, with a motivation they act on whether
or not the party returns.

## Constraints

- **Draw from the roster; do not invent a cast.** A location that invents its own people
  produces a settlement of strangers who never meet each other, which is the failure the
  roster exists to prevent. If somebody is needed who is not on the roster, add them to the
  roster.
