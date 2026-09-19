# Dangerous - Dressing

## Provides
The physical reality of a DANGEROUS location, and how its parts read as one place. Units,
the Exits line syntax and the citation formats are in `templates/Location.md`.

## Spec

```
DRESSING - every location
  1     Size and shape
  1     Condition                                       (genre: room-condition)
  1     Purpose - what it was for, stated even where Condition means it no longer is
                                                        (genre: purposes)
  1     Ambiance - smell and sound, attributable to Condition or Purpose
  1     Terms for what is here, named rather than described  (genre: vocabulary-underground)
  1     Every exit typed and positioned                 (dangerous/Door.md)
```

**Condition is stated before Purpose**, because it decides how much of the purpose still
shows: tool marks, worn grooves, fixtures left in the wall, a floor sloped to drain
somewhere.

## Constraints

- **Details the region description already carries are not repeated here.** A smell or
  sound equally true of every room in the region belongs in the Region Overview's Ambiance
  field. The inverse is the failure to watch for - a motif claimed at the overview level
  and carried by only a handful of rooms exists nowhere a party can touch it.

- **Do not reuse a purpose already used in this region.** A region with three storerooms
  has told the party that rooms do not matter.

- **Do not let every room land at the same point on the Condition line.** Variance here is
  what makes the Region Overview's Dangers field something a party reads room to room
  rather than a claim stated once.

- **Everything in the room was put there by the same history.** Before the entry is done,
  check that each feature could plausibly share a room with the others - and where one
  cannot, change it rather than explaining it.
