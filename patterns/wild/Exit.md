# Wild - Exit

## Provides
One way out of a WILD location: how it goes and where it sits at each end. Which
locations connect, and by what kind of edge, is the region's `Connections.mmd`'s; the
Exits line syntax and units are `templates/region/Location.md`'s.

## Spec

```
EXIT - every exit
  1     Kind - read off the edge the region's Connections.mmd already drew, never chosen
        here                                         {normal | hidden | one-way}
  1     Way - what a party follows to leave by it, named as country rather than as a
        direction
  1     Position from - a compass direction or a relation to something already stated,
        at this end
  1     Position to - the same, at the far end
  1     To - where it goes: the location code, or plain terms for an exit leaving the map
```

## Constraints

- **Never two exits of one location reading identically.** Two ways out told apart by
  nothing send the party down the wrong one with no way to have known.
