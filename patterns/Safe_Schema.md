# Safe Schema

A SAFE region's tables: every location reached from the region itself except a Secret,
what can be bought and stolen there and who is found there - people, named creatures and the
members of a faction - with a garrison at an Authority, and what guards a Secret. Its seed and brief are
`patterns/Region_Schema.md`'s.

```kdl
enum Safe_Type Inn Merchant Bank Market Authority Gate Secret
// Gate: a way across the region's edge, where what stands at the Approach stands. Secret: a
// place or thing kept hidden, reached only by the Way that hangs it from another location.
enum Purchase_Type menu service sale   // food and drink by the portion; a thing done for a party; goods handed over
enum Contents_Type "Treasure I" "Treasure II" "Treasure III" "Treasure IV" "Treasure V" Magic Hoards Lore Keys "Unique Treasures" "Magical Tomes"
enum Hazard_Type {
  Mechanical Pit Spike Dart Hammer Gas
  Magical Runes Field Attack
  Environmental "Fire/Lava" Water Ice "Ravine/Climb" "Broken/Weak Floor"
}
enum Mystery_Type Altar Statue Fountain Fresco Tapestry Throne "Button/Lever/Switch/Keyhole" Mirror Flooring

node Seed {
  kind Safe_Kind
  comes text                // what a party comes to do
  who entry Bestiary Factions "Named Creatures" list   // who lives here; the tables place them
  changing text             // what is changing, and who is behind it and who is hurt
}
node View {                 // where it is first seen from
  from string
  distance distance
  outline text              // its outline and size; its walls or edges, their height and material; the ground under it
  shows text                // roofs, colours, devices, lights
}
node Law {                  // what gets a stranger fined, locked up or put out
  offence string
  cost text
  enforcer gloss
}

node Location {
  name string               // per GENRE.md's Naming, after the rest is decided; named only where
                            // something refers to it again. In whose mouth: residents,
                            // border passers, the departed, or its occupants
  tags tag list n=3
  type kind
  at string opt             // "way in" where it stands at the region's way in; else prose for the reader
  bearing Compass opt drawn // from its block's origin - the region's way in, unless the block states xyz - with distance; or xyz
  distance distance opt drawn
  xyz point opt drawn       // its centre from its block's origin, x,y,z
  against anchor opt drawn  // touching another location of its block, its xyz then a slide across the side and a gap along it
}
node Dressing {
  obvious string
  former gloss opt
  condition tag opt
  ambiance gloss opt
  width feet opt            // across, west to east as the room lies; a round room's diameter
  length feet opt           // north to south
  height feet opt           // floor to roof, where it matters at the table
  outline outline opt drawn // where it is no rectangle: its extent is its width and length
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
  price price
  per gloss opt             // what one price buys: "a night", "each"
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
  quest entry Quests opt    // the quest they give; left empty until Quests.md is written (step 4d)
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
node Reward {              // what is there to be stolen: the vault, the treasury
  container gloss
  contents pull Contents_Type
  one-of Secret opt
}
node Encounter {
  one-of Creature NamedCreature Faction
  doing string
  reaction Reaction
  want string opt
  know string opt
  left gloss opt
  far gloss opt
}
node Creature {
  bestiary entry Bestiary
  count number
}
node Hazard {
  type Hazard_Type
  damage Damage_Type
  test Test
  wound Wound_Type opt      // required for a Constitution Test: one of BRIEF.md's Procedures wounds
  condition gloss opt       // required for a Fate Test: a name in Procedures.md's Conditions
  one-of Secret
}
node Mystery {
  type Mystery_Type
  effect string
  test Test opt             // where it asks one; then a Hazard's damage, wound and condition rules hold
  damage Damage_Type opt
  wound Wound_Type opt
  condition gloss opt
  one-of Secret
}
node Garrison {             // the standing force an Authority commands
  faction entry Factions
  present number            // under arms and within call
  members string            // ranks, arms and posts
  call gloss                // what brings it out
  within time               // how soon
}

node Way {
  to location
  bearing Compass drawn     // from this end
  distance distance drawn
  orientation gloss opt     // the same in words, for the reader
  one-of Secret opt
}
node Block {               // a map of its own, and the enclosure drawn round its locations
  name string
  locations location list
  xyz point opt drawn       // its centre from its region's way in, x,y,z
  against anchor opt drawn  // touching another block of its region, its xyz then a slide and a gap
  outline outline opt drawn
  wall gloss opt            // its height and what stands on it
  towers gloss opt          // their shape and where they stand
}
node Secret {              // the way into a Secret location: what opens it, what shows it is there, and when
  trigger gloss
  tell gloss
  knows gloss opt           // who knows it, or nobody
  fact string opt           // what it hides, where the node it sits on does not say
  when gloss opt
}

node Ground {               // written by `tools/maps.py ground`, never by hand: the region as its sheet draws it
  sheet string              // its home sheet
  square string             // its way in on that sheet, as "column,row"
  height feet               // the ground at its way in, above the sea
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
  Rewards Reward opt
  Challenges Encounter Hazard Mystery opt          // a Secret's only
  Procedures Procedure
  Blocks Block Void opt                            // Void: ground in a Block that no location takes, drawn as open ground
  Connections Way
  Ground Ground Feature At                         // written by code
  Design Design Fill Tie Street Fabric Void Place opt
  top Inn Merchant Bank Market Authority Gate   // reached from the region itself, so never joined to one another
  join Secret Inn Merchant Bank Market Authority Gate gate=Secret   // the only type that connects within its region, and the Way into it carries a Secret
}
```
