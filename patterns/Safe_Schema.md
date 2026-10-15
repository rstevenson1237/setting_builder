# Safe Schema

A SAFE region's tables: every location reached from the region itself. Its seed and
brief are `patterns/Region_Schema.md`'s.

```kdl
enum Safe_Type Inn Merchant Bank Market Authority

node Location {
  name string               // per GENRE.md's Naming, after the rest is decided; named only where
                            // something refers to it again. In whose mouth: residents,
                            // border passers, the departed, or its occupants
  tags tag list n=3
  type kind
}
node Dressing {
  obvious string
  former gloss opt
  condition tag opt
  ambiance gloss opt
  layout string
}

folder Safe type=Safe_Type {
  Locations Location
  Dressing Dressing
}
```
