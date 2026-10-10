# Setting - Magical Tomes

## Provides
One book that teaches magic, with a title and a writer of its own. A written work that
teaches nothing is `patterns/setting/Lore.md`'s.

## Spec

```
MAGICAL TOME ENTRY
  1     Title - per GENRE.md's Naming answer
  1     Teaches - what a reader able to use it learns, stated plainly enough to adjudicate
  1     Reading - what learning from it takes                            {READING}
  1     Writer - an entry in setting/History.md, setting/Factions.md or
        setting/NamedCreatures.md that accounts for it
  1     Found at - the location it is found at
```

```
READING - exactly one
  time         - days of study, stated
  tongue       - a tongue from setting/Language.md the reader must know
  rite         - an act done while reading
  cost         - something the reader gives up to finish it
```

## Constraints

- **A tome is learned, never discharged.** What it grants passes to the reader; the book
  itself does nothing when used.
