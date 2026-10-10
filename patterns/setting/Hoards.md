# Setting - Hoards

## Provides
One hoard: a bespoke list of treasure gathered at one location by one owner. A single
find is a table roll; one item with a history of its own is
`patterns/setting/UniqueTreasures.md`'s.

## Spec

```
HOARD ENTRY
  1     Name - what its owner calls it, per GENRE.md's Naming answer
  1     Owner - who gathered it: an entry in setting/Bestiary.md, setting/Factions.md
        or setting/NamedCreatures.md
  1     Items - each a treasure result                (patterns/setting/Treasure.md)
  1     Total - value and wt, summed
  1     Found at - the one location holding it
```

## Constraints

- **Never more than one location.** Treasure spread across rooms is several entries.
