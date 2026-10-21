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

node Location {
  name string               // per GENRE.md's Naming, after the rest is decided; named only where
                            // something refers to it again. In whose mouth: border passers,
                            // the departed, or its occupants
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
  layout string
  mark entry Factions list opt   // the faction whose Identity shows here
  left entry History list opt    // the event whose Left mark shows here
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
  wound Wound_Type opt     // a Constitution Test's Wound, required for one; one of BRIEF.md's Procedures wounds
  condition gloss opt      // a Fate Test's Condition, required for one; a name in Procedures.md's Conditions
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
  at string opt             // as a Location's at, and its bearing, distance, north and east
  bearing Compass opt
  distance distance opt
  north distance opt
  east distance opt
  sight string              // what a party finds there and can do
  to location opt           // where a path from it leads, in this region or another: a Route is then a
                            // slice through the region, the stops its way to what lies off it
}
node Way {
  to location
  bearing Compass           // from this end
  distance distance
  orientation gloss opt     // the same in words, for the reader
  one-of Secret opt
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

folder Wild type=Wild_Type {
  Locations Location
  Dressing Dressing
  Challenges Encounter Hazard Mystery
  Procedures Procedure
  Stops Stop                                       // a Route's only
  Connections Way
  Ground Ground Feature At                         // written by code
  top Landmark Route  // reached from the region itself, so never joined to one another
  join Hidden Landmark Route  // a type connects only to these within its region
  join Secret Landmark Route gate=Secret  // and the Way into it carries a Secret
}
```
