# Wild Schema

A WILD region's tables: country reached from the region itself, and what lies off its
tracks.

```kdl
enum Wild_Type Route Hidden Secret {
  Landmark Lair Ruin Natural
}
enum Terrain hills mountains plains forest swamp desert jungle coast   // one, or two in combination
enum Hazard_Type {
  Ground "Rockfall/Slide" "Bog/Quicksand" "Cliff/Climb" Thorns
  Water Ford Flood "Thin Ice"
  Weather Storm Fog Cold Heat
}
enum Mystery_Type "Standing Stone" Cairn Spring Pool "Old Tree" Shrine "Carved Rock" Ring

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
  seed {
    Overview text           // what a party sees crossing in, who is out here, what brings anyone
    Approach text           // where it is entered, and how long a crossing takes on the best route and off it
    Terrain Terrain         // then rulings per setting/Procedures.md's Time: what an action buys on a road,
                            // off it, through the worst; what loses a party and finds the way; weather,
                            // night, a fire. Ground is never a location.
    Situation text
  }
  brief {
    Places text             // every Landmark: what shows from a distance, what a party goes for
    Inhabitants text        // one sentence: every creature and faction the Encounters hold, how many, where
    Loot text               // forage and game by local name, what the nearest SAFE region pays; treasure
                            // tables. Anything dangerous enough to meet is an Encounter, never game.
    Secrets text
    Leads text
    Tables text             // d6 Encounter per failed Difficulty roll; d6 things met between Landmarks
  }
}
```
