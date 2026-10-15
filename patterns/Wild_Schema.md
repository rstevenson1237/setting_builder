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
  form Name_Form
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

folder Wild type=Wild_Type {
  Locations Location
  Dressing Dressing
  Challenges Encounter Hazard Mystery
  Connections Way
  top Landmark Route  // reached from the region itself, so never joined to one another
  join Hidden Landmark Route  // a type connects only to these within its region
  join Secret Landmark Route gate=Secret  // and the Way into it carries a Secret
}
```
