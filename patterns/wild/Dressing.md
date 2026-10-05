# Wild - Dressing

## Provides
The physical reality of a WILD location, where it sits in its region, and how its parts
read as one place. Purpose is the kind file's. Units, the Exits syntax and the citation
formats are `templates/region/Location.md`'s.

## Spec

```
DRESSING - every WILD location
  1     Size - in yards, a vertical drop or climb in feet
  1     Shape
  1     Position - a bearing from the region's entry, or a distance and direction from a
        named Landmark; a Hidden or Secret location takes its parent's
  1     Condition - stated before anything else physical: what weather, season and time
        have done to it            {worked | disturbed | reclaimed | damaged}
  1     Weathered - what it is like in rain and at night
  1     Smell - what the air smells of, caused by Condition or Purpose
  1     Sound - what sound does across open ground or under canopy, caused by
        Condition or Purpose
  1     Exits - every exit typed and positioned                     (wild/Exit.md)
```

## Constraints

- **Never give a detail its causal history.** It is present, or it is not.
