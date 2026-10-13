# Region Schema

The nodes every rating's tables share. Each rating's schema adds its own, and may define a
node of the same name to mean what that rating needs.

```kdl
node Location {
  name string
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
