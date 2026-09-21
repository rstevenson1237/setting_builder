# Safe - People

## Provides
Which individuals from the region's roster appear at this location, and what makes each
worth remembering.

Both draws want the same fields, which is why there is one file. The roster itself is
the Region Overview's People field; this file turns a roster line into somebody at a
location.

## Spec

```
PERSON
  1     Name, from the region roster - not invented here
  1     What they are doing when the party arrives - not idle
  1     One thing distinctive enough to be recalled a session later - a mark, a
        habit, a possession, a fear, a competence, or a disposition, never a
        physical description in full
  1     What they want, whether or not they are asking for it
  30%   A Named Creature row, where they will recur or be heard of first
  20%   An opinion about the region's Situation that is not the common one
```

**Recall beats description.** A party remembers one concrete thing - a scar, a habit, a
grudge, a way of speaking, a thing they carry - and forgets three sentences of appearance.
Write the one thing.

**They will appear at more than one location, or the party will hear of them before
meeting them, or they will be a problem later.** That is when to make them a Named
Creature - stat them per `patterns/setting/Bestiary.md`, most often at 1-2 AD, and give
them a motivation they act on whether or not the party ever returns.

## Constraints

- **Draw from the roster; do not invent a cast.** The region's People field lists who is
  here. A location that invents its own people produces a settlement of strangers who
  never meet each other, which is the failure the roster exists to prevent. If somebody
  is needed who is not on the roster, add them to the roster.
