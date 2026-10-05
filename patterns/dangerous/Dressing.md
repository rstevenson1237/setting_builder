# Dangerous - Dressing

## Provides
The physical reality of a DANGEROUS location, and how its parts read as one place. Units,
the Exits line syntax and the citation formats are `templates/region/Location.md`'s.

## Spec

```
DRESSING - every location
  1     Size
  1     Shape
  1     Condition - stated before Purpose: how far the room sits from still in use to
        gone, which decides how legible its Purpose still is, and its temperature and
        footing
                                {active | abandoned | decayed | ruined | destroyed}
  1     Family - the purpose family the room served                (dangerous/Block.md)
  1     Use - the room's own use within its family, drawn from the region's Conditions
        and its occupants' needs
  1     Left - what that use left in the fabric of the room
  1     Smell - caused by Condition or Purpose
  1     Sound - caused by Condition or Purpose
  1     Exits - every exit typed and positioned                 (dangerous/Door.md)
```

## Constraints

- **Do not reuse a purpose already used in this block.** A block with three storerooms has
  told the party that rooms do not matter. A room destroyed past legibility still states
  what it was, and lets Condition explain why it no longer shows.
