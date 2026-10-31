# Wild Schema

A WILD region's tables: country reached from the region itself, and what lies off its
tracks. Its seed and brief are `patterns/Region_Schema.md`'s.

```kdl
enum Wild_Type Route Hidden Secret {
  Landmark Lair Ruin Natural
}
enum Hazard_Type {
  Ground "Rockfall/Slide" "Bog/Quicksand" "Cliff/Climb" Thorns
  Water Ford Flood "Thin Ice"
  Weather Storm Fog Cold Heat
}
enum Mystery_Type "Standing Stone" Cairn Spring Pool "Old Tree" Shrine "Carved Rock" Ring

node Seed {
  terrain Terrain
  comes text                // what a party sees crossing in, and what brings anyone
  who entry Bestiary Factions "Named Creatures" list   // who is out here; the tables place them
  changing text             // what is changing, and who is behind it and who is hurt
  crossing time opt         // the best route, end to end
  off time opt              // and off it
}
node Ruling {               // per setting/Procedures.md's Time and Distance; ground is never a location
  on gloss                  // the road, off it, the worst ground, night, fog, a fire
  buys text                 // what an action buys there, what loses a party and what finds the way
}

node Location {
  name string               // per GENRE.md's Naming, after the rest is decided; named only where
                            // something refers to it again. In whose mouth: border passers,
                            // the departed, or its occupants
  tags tag list n=3
  type kind
  at string opt             // "way in" where it stands at the region's way in; else prose for the reader
  bearing Compass opt drawn // from its block's origin - the region's way in, unless the block states xyz - with distance; or xyz
  distance distance opt drawn
  xyz point opt drawn       // its centre from its block's origin; z unset, it stands on its ground
  against anchor opt drawn  // touching another location of its block, its xyz then a slide across the side and a gap along it
}
node Dressing {
  obvious string
  former gloss opt
  condition tag opt
  ambiance gloss opt
  width feet opt            // across, west to east, as the place lies on the map
  length feet opt           // north to south
  outline outline opt drawn // where it is no rectangle: its extent is its width and length
  layout string
  mark entry Factions list opt   // the faction whose Identity shows here
  left entry History list opt    // the event whose Left mark shows here
}
node Block {                // a map of its own: a place's buildings, where its locations stand, on the region's ground
  name string
  locations location list
  xyz point opt drawn       // its centre from its region's way in; unset, it lies there
  against anchor opt drawn  // touching another block of its region, its xyz then a slide and a gap
  outline outline opt drawn
  wall gloss opt            // drawn round the locations where stated; its height and what stands on it
  towers gloss opt          // their shape and where they stand
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
node NamedCreature {
  named entry "Named Creatures"
  presence percent
}
node Faction {
  faction entry Factions
  present number
  members string
}
node Hazard {              // ground or weather: it shows itself before it bites
  type Hazard_Type
  damage Damage_Type
  test Test
  wound Wound_Type opt     // required for a Constitution Test: one of BRIEF.md's Procedures wounds
  condition gloss opt      // required for a Fate Test: a name in Procedures.md's Conditions
  sign gloss
}
node Mystery {
  type Mystery_Type
  effect string
  act gloss                // what sets it off
  tell gloss
}
node Procedure {
  procedure entry "Local Procedures"
}
node Stop {                 // a place of interest on a Route, listed in order from where the route starts
  feature gloss             // the Feature its write-up gives it
  at string opt             // as a Location's at, and its bearing, distance and xyz, from its region's way in
  bearing Compass opt drawn
  distance distance opt drawn
  xyz point opt drawn
  sight string              // what a party finds there and can do
  to location opt           // where a path from it leads, in this region or another: a Route is then a
                            // slice through the region, the stops its way to what lies off it
}
node Way {
  to location
  bearing Compass drawn     // from this end
  distance distance drawn
  orientation gloss opt     // the same in words, for the reader
  one-of Secret opt
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

folder Wild type=Wild_Type {
  Locations Location
  Dressing Dressing
  Challenges Encounter Hazard Mystery
  Procedures Procedure
  Blocks Block opt
  Stops Stop                                       // a Route's only
  Connections Way
  Ground Ground Feature At                         // written by code
  top Landmark Route  // reached from the region itself, so never joined to one another
  join Hidden Landmark Route  // a type connects only to these within its region
  join Secret Landmark Route gate=Secret  // and the Way into it carries a Secret
}
```
