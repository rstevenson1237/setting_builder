# Setting - Keys

## Provides
One key entry: a portable object, the lock it opens elsewhere, and why the two are apart.
When a location reaches for a key is its rating's own `Key.md`; a key found before it is
used is distinct from a quest, which is asked before it is fulfilled.

## Spec

```
KEY ENTRY
  1     Form                                                              {FORM}
  1     Unlocks - exactly what it unlocks: a specific feature at a specific location
  1     Found at - where it is found, by location
  1     Apart - why the two are apart                                     {APART}
  1     Connection - what connects it to its lock, where the connection is not obvious - itself a
        discoverable secret                                          {CONNECTION}
```

```
FORM - exactly one
  key          - a key, cut for one lock
  profile      - a rod, pin or bar cut to a profile
  fitting      - a stone or disc fitted to a socket
  seal         - a seal or signet
  token        - a token carried as proof
  bone         - a part of a specific creature
  word         - a phrase or name recorded on something portable
  measure      - a measured length
  fragment     - a piece broken off the lock itself
```

```
APART - exactly one
  deliberate   - keeping them together defeated the point
  transit      - its holder died carrying it
  loot         - it was taken as plunder
  burial       - it went into the ground with someone
  trust        - it was left for safekeeping and never reclaimed
  later        - the lock was built afterwards, around a thing that already existed
```

```
CONNECTION - at least one
  maker        - a shared maker's mark
  material     - the same material
  measure      - a matching measurement
  tongue       - the same tongue
  wear         - matching wear
  inscription  - an inscription naming the lock but not the key
  record       - an entry in setting/Lore.md
```

## Constraints

- **A key that opens nothing is treasure.** Without a lock it belongs on a
  `setting/Treasure[I-V].md` roll or in `setting/UniqueTreasures.md`.

- **A key never gates a single room's own contents.** Gating a room from inside itself is
  a Hazard's or a Mystery's job; a key connects locations.
