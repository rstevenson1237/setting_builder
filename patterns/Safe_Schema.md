# Safe Schema

A SAFE region's tables: every location reached from the region itself except a Secret,
what can be bought there and who is found there. Its seed and brief are
`patterns/Region_Schema.md`'s.

```kdl
enum Safe_Type Inn Merchant Bank Market Authority Gate Secret
// Gate: a way across the region's edge, where what stands at the Approach stands. Secret: a
// place or thing kept hidden, reached only by the Way that hangs it from another location.
enum Purchase_Type menu service sale   // food and drink by the portion; a thing done for a party; goods handed over

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

node Purchase {
  type Purchase_Type
  item string
  price gloss               // in Treasure I's coin, and per what
  limit gloss opt           // the stock, hours or terms that cap it
}
node Person {
  name string
  form Name_Form
  role gloss
  personality gloss
  wants string              // of a stranger, and what it offers for it
  knows string              // what a party can learn from them
  quest entry Quests opt    // the quest they give; left empty until Quests.md is written (step 5d)
}

node Way {
  to location
  orientation gloss
  one-of Secret opt
}
node Secret {              // the way into a Secret location: what opens it, what shows it is there, and when
  trigger gloss
  tell gloss
  when gloss opt
}

folder Safe type=Safe_Type {
  Locations Location
  Dressing Dressing
  Purchases Purchase
  People Person
  Connections Way
  top Inn Merchant Bank Market Authority Gate   // reached from the region itself, so never joined to one another
  join Secret Inn Merchant Bank Market Authority Gate gate=Secret   // the only type that connects within its region, and the Way into it carries a Secret
}
```
