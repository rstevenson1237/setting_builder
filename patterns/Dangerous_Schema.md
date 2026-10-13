# Dangerous Schema

A DANGEROUS region's tables: rooms behind doors, and what a room hides.

```kdl
enum Dangerous_Type High Medium Low
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
}
```
