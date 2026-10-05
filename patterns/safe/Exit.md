# Safe - Exit

## Provides
One way in or out of a SAFE location: how it goes, where it sits at each end, and who may
use it. Which locations connect, and by what kind of edge, is the region's
`Connections.mmd`'s; the Exits line syntax and units are `templates/region/Location.md`'s.

## Spec

```
EXIT - every exit
  1     Kind - read off the edge the region's Connections.mmd already drew, never chosen
        here                                         {normal | hidden | one-way}
  1     Way - what a party passes through, named by its make
  1     Position from - which wall, side or direction it opens from, at this end
  1     Position to - the same, at the far end
  1     To - where it goes: the location code, or plain terms for an exit leaving the map
  1     Who may use - access here is social as often as physical: who is let through,
        and who is turned back
```

## Constraints
