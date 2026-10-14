# Region Schema

The nodes every rating's tables share. Each rating's schema adds its own, and may define a
node of the same name to mean what that rating needs. Each rating's `folder` also holds its
`seed`, `setting/region/[Code].md`, written before any location exists and naming none,
and its `brief`, `setting/region/[Code]/Brief.md`, written from the tables alone.

Every seed and brief sentence carries something usable at the table - a name, count,
price, place, distance or ruling; why a place exists or how it feels is cut, and nothing
is said twice. A secret always carries its answer. A Situation is true whether or not the
party engages: what is changing, then two rungs, each with what sets it off. Places is an
index, never a description. A list field writes each item as its own `- ` line.

```kdl
node Location {
  name string               // per GENRE.md's Naming, after the rest is decided; named only where
                            // something refers to it again. In whose mouth: residents (SAFE only),
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
node Encounter {
  one-of Creature NamedCreature Faction
  doing string
  reaction string
  want string opt
  know string opt
  left gloss opt
  far gloss opt
}
node Creature {
  bestiary entry Bestiary
  count number
}
node NamedCreature {
  named entry "Named Creatures"
  presence percent
}
node Faction {
  faction entry Factions
  present number
  members string
}
```
