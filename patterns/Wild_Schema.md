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
  at string                 // compass point and distance from the region's way in, or how far
                            // north or south of it then east or west: "700 yards north, 50 west"
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
node Hazard {              // ground or weather: it shows itself before it bites
  type Hazard_Type
  damage Damage_Type
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
  at string                 // as a Location's at
  sight string              // what a party finds there and can do
  to location opt           // where a path from it leads, in this region or another: a Route is then a
                            // slice through the region, the stops its way to what lies off it
}
node Way {
  to location
  orientation gloss         // compass point and distance from this end
  one-of Secret opt
}
node Secret {              // the way into a Secret location: what opens it, what shows it is there, and when
  trigger gloss
  tell gloss
  when gloss opt
}

folder Wild type=Wild_Type {
  Locations Location
  Dressing Dressing
  Challenges Encounter Hazard Mystery
  Procedures Procedure
  Stops Stop                                       // a Route's only
  Connections Way
  top Landmark Route  // reached from the region itself, so never joined to one another
  join Hidden Landmark Route  // a type connects only to these within its region
  join Secret Landmark Route gate=Secret  // and the Way into it carries a Secret
}
```
