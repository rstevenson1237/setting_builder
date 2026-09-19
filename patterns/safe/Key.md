# Safe - Key

## Provides
How a settlement comes to be holding an object that opens something somewhere else.
Criteria are in `patterns/setting/Keys.md`.

## Spec

```
KEY
  1     The object, and what it physically is           (genre: key-forms)
  1     What it opens, named by location code and feature
  1     How it got here                                 (genre: key-provenance-settlement)
  1     Who has it here, and whether they know what it is
                                                        (genre: key-holders-settlement)
  1     What it takes to get it                         (genre: key-price)
  30%   A clue connecting object to lock                (genre: key-clues)
  20%   Somebody else wants it, and is closer to getting it
                                                        (genre: key-rivals)
```

**State how close the rival is**, so delay has a price.

## Constraints

- **A key held in a settlement is a transaction, not a find.** Somebody owns it, and what
  it takes to get it is stated in their terms. A key lying unattended in a settlement has
  been written as a dungeon cache in a town.
