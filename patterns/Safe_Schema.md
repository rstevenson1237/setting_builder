# Safe Schema

A SAFE region's tables: every location reached from the region itself except a Secret,
what can be bought there and who is found there - people, named creatures and the members
of a faction - with a garrison at an Authority. Its seed and brief are
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
  at string opt             // "way in" where it stands at the region's way in; else prose for the reader
  bearing Compass opt       // from the region's way in, with distance; or north and east
  distance distance opt
  north distance opt        // how far north of the way in, south where negative
  east distance opt         // and east, west where negative
}
node Dressing {
  obvious string
  former gloss opt
  condition tag opt
  ambiance gloss opt
  width feet opt            // across, west to east as the room lies; a round room's diameter
  length feet opt           // north to south
  height feet opt           // floor to roof, where it matters at the table
  shape Room_Shape opt      // rect where unset
  layout string
  mark entry Factions list opt   // the faction whose Identity shows here
  left entry History list opt    // the event whose Left mark shows here
}

node Procedure {
  procedure entry "Local Procedures"
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
  member entry Factions opt // the faction they belong to, where they belong to one
  quest entry Quests opt    // the quest they give; left empty until Quests.md is written (step 5d)
}
node NamedCreature {
  named entry "Named Creatures"
  presence percent
}
node Faction {              // members met here in the ordinary run of the place, not under arms
  faction entry Factions
  present number
  members string
}
node Garrison {             // the standing force an Authority commands
  faction entry Factions
  present number            // under arms and within call
  members string            // ranks, arms and posts
  answers string            // what brings it out, and how soon
}

node Way {
  to location
  bearing Compass           // from this end
  distance distance
  orientation gloss opt     // the same in words, for the reader
  one-of Secret opt
}
node Block {               // a map of its own, and the enclosure drawn round its locations
  name string
  locations location list
  wall gloss opt            // its height and what stands on it
  towers gloss opt          // their shape and where they stand
}
node Secret {              // the way into a Secret location: what opens it, what shows it is there, and when
  trigger gloss
  tell gloss
  when gloss opt
}

node Ground {               // written by `tools/maps.py ground`, never by hand: the region as its sheet draws it
  sheet string              // its home sheet
  square string             // its way in on that sheet, as "column,row"
  ground string list        // the terrain its area holds, by share
}
node Feature {              // a river, road, hill or hollow in the region's area
  kind Feature_Kind
  bearing Compass           // from the region's way in, to the nearest of it
  distance distance
  runs Compass opt          // the way a river or road runs, to its far end
  height feet opt           // a hill's or hollow's
}
node At {                   // the ground at a location
  ground Ground_Type
  height feet
  slope Slope
}

folder Safe type=Safe_Type {
  Locations Location
  Dressing Dressing
  Purchases Purchase
  People Person NamedCreature Faction
  Garrison Garrison                                // an Authority's only
  Procedures Procedure
  Blocks Block opt
  Connections Way
  Ground Ground Feature At                         // written by code
  top Inn Merchant Bank Market Authority Gate   // reached from the region itself, so never joined to one another
  join Secret Inn Merchant Bank Market Authority Gate gate=Secret   // the only type that connects within its region, and the Way into it carries a Secret
}
```
