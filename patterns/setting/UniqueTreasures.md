# Setting - Unique Treasures

## Provides
One treasure with a name and a history of its own, rather than a roll on a table. A find that
is a table roll is `patterns/setting/Treasure.md`'s.

## Spec

```
UNIQUE TREASURE ENTRY
  1     Name - per GENRE.md's Naming answer
  1     Does - stated plainly enough to adjudicate                           {DOES}
  1     Cost - at what GENRE.md's Magic level says power costs              {COST}
  1     Origin - where it came from: an entry in setting/History.md, setting/Truths.md,
        setting/Factions.md or setting/NamedCreatures.md that accounts for it
                                                                          {ORIGIN}
  1     Found at - the location it is found at
```

```
DOES - exactly one
  once         - it works once
  class        - it works on one class of thing
  adjacent     - it does something next to what a party wants
  solution     - it makes one specific problem soluble that otherwise is not
  knowledge    - it grants knowledge rather than force
  passage      - it opens or closes
  ward         - it protects against one named thing
```

```
COST - at least one, or none where GENRE.md's Magic level lets power be free
  toll         - it takes something from the bearer each time it is used
  noticed      - it works, and something notices
  bound        - it cannot be put down
  desperate    - it works better the worse the bearer's situation
  foreign      - it was made for someone else, and knows it
  sought       - somebody is looking for it
  forbidden    - using it is something the setting's Truths punish
```

```
ORIGIN - exactly one
  event        - made for an event in setting/History.md
  truth        - a consequence of a truth in setting/Truths.md
  lost         - a faction's property, lost
  reclaimed    - a Named Creature's, and they want it back
  grave        - grave goods
  unlikely     - made by somebody who should not have been able to
  unmade       - not made at all
```

## Constraints

- **Never an invented origin.** An artifact nothing established can account for is
  disconnected from the setting by construction, and should not exist.
