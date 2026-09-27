# Setting - Named Creatures

## Provides
One named individual the setting keeps consistent across every appearance. A creature met
once, however memorable, is a Bestiary entry named in its Feature line instead.

## Spec

```
NAMED CREATURE ENTRY
  1     A name, per GENRE.md's Naming answer
  1     A stat line, on the same scale as any creature    (patterns/setting/Bestiary.md)
  1     Why it earns a row                                                {ROLE}
  1     Motivation - pursued whether or not the party ever shows up      {MOTIVE}
  1     Every location it appears at
  1     How it reaches a party before it is met - a rumour, a piece of lore, or a
        survivor
  1     What it remembers of those it meets                               {MEMORY}
  1     Something it wants
```

```
ROLE - exactly one
  set piece    - a region's defining threat
  ranging      - it moves across more than one region
  situation    - a settlement's Situation turns on it
  survivor     - it will live through an encounter and remember it
  leader       - its faction will outlast it
  unkillable   - the party is likely to fail to kill it
```

```
MOTIVE - exactly one
  feeding      - it is feeding something
  holding      - it is holding a boundary
  searching    - it is looking for something it lost
  collecting   - it is owed, and collecting
  protecting   - it is protecting young
  expanding    - it is taking ground it did not hold last season
  waiting      - it is waiting for a condition to be met
```

```
MEMORY - at least one
  hurt         - who hurt it
  fed          - who fed it
  fled         - who ran
  scent        - a smell
  name         - a name
  promise      - a promise
```

## Constraints

- **A motivation is a standing goal, not a scripted arc.** It can be stated without
  mentioning the party.

- **Never let a second meeting play like the first.** What it remembers is the reason it
  has a row.
