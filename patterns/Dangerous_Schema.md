# Dangerous Schema

A DANGEROUS region's tables: rooms behind doors, and what a room hides.

```kdl
enum Dangerous_Type High Medium Low
enum Kind collection "single holding"   // a worked complex in blocks, sized by its die; one occupant's home, sized by what it holds
enum Connection_Type Open Archway Broken Crude Wooden Banded Stone Iron
enum Mystery_Type Altar Statue Fountain Fresco Tapestry Throne "Button/Lever/Switch/Keyhole" Mirror Flooring
enum Hazard_Type {
  Mechanical Pit Spike Dart Hammer Gas
  Magical Runes Field Attack
  Environmental "Fire/Lava" Water Ice "Ravine/Climb" "Broken/Weak Floor"
}

node Purpose {
  unique string opt
  pressure string opt
  signs location list opt
}
node Hazard {
  type Hazard_Type
  damage Damage_Type
  one-of Secret
}
node Mystery {
  type Mystery_Type
  effect string
  one-of Secret
}
node Reward {
  container gloss
  contents pull Contents_Type
  one-of Encounter Hazard Mystery Secret Lock opt
}
node Connection {
  to location
  type Connection_Type
  orientation gloss
  one-of Encounter Hazard Mystery Secret Lock opt
}
node Secret {              // what sets off or opens the thing it sits on, and what gives it away
  trigger gloss
  tell gloss
}
node Lock {
  key entry Keys
}

folder Dangerous type=Dangerous_Type {
  Locations Location
  Purpose Purpose
  Dressing Dressing
  Challenges Encounter Hazard Mystery
  Rewards Reward
  Connections Connection
  seed {
    Kind Kind
    Overview text           // what a party sees at the way in, who lives there, what it comes for
    Approach text           // every entrance: where it opens from, who or what watches it
    Conditions text         // every room unless it says otherwise: material, height and width,
                            // light, what carries sound, footing, air, what a lit fire does
    Situation text          // a single holding barely moves the Danger track: name what presses instead
  }
  brief {
    Places text             // each block, or a single holding's notable rooms: codes, way in, prize, rival
    Inhabitants text        // one sentence: every creature and faction the Encounters hold, how many, where
    Alarm text              // what raises it, who hears first, who comes from where, how many turns later
    Loot text               // the largest prize and what stands over it; treasure tables; who buys it back
    Secrets text            // - the fact - the entry that brings it out
    Leads text              // - each rumour by number, each quest by name
    Tables text             // d6 Danger, 6 noticing to 1 acting, down one per failed Difficulty roll;
                            // d6 rooms for anywhere no location keys
  }
}
```
