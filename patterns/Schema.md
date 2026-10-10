# Schema

What every location table entry is checked against.

```kdl
value string words=8
value gloss words=4
value tag words=2
value number                  // N, or a range N-M
value percent                 // N%
value location                // a location code
value entry                   // a title on the table the member names
value pull                    // a roll table's name, or "Table: Title" for an entry table

table "Treasure I" roll file="setting/Treasure1.md"
table "Treasure II" roll file="setting/Treasure2.md"
table "Treasure III" roll file="setting/Treasure3.md"
table "Treasure IV" roll file="setting/Treasure4.md"
table "Treasure V" roll file="setting/Treasure5.md"
table Magic roll file="setting/Magic.md"
table Bestiary entry file="setting/Bestiary.md"
table Factions entry file="setting/Factions.md"
table "Named Creatures" entry file="setting/NamedCreatures.md"
table Lore entry file="setting/Lore.md"
table Keys entry file="setting/Keys.md"
table "Unique Treasures" entry file="setting/UniqueTreasures.md"
table "Magical Tomes" entry file="setting/MagicalTomes.md"
table Hoards entry file="setting/Hoards.md"

enum Dangerous_Type High Medium Low
enum Connection_Type Open Archway Broken Crude Wooden Banded Stone Iron
enum Damage_Type Nuisance Damaging Lethal
enum Mystery_Type Altar Statue Fountain Fresco Tapestry Throne "Button/Lever/Switch/Keyhole" Mirror Flooring
enum Hazard_Type {
  Mechanical Pit Spike Dart Hammer Gas
  Magical Runes Field Attack
  Environmental "Fire/Lava" Water Ice "Ravine/Climb" "Broken/Weak Floor"
}
enum Contents_Type "Treasure I" "Treasure II" "Treasure III" "Treasure IV" "Treasure V" Magic Hoards Lore Keys "Unique Treasures" "Magical Tomes"

node Location {
  name string
  tags tag list n=3
  type Dangerous_Type
}
node Purpose {
  unique string opt
  pressure string opt
  signs location list opt
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
node Secret {
  trigger gloss
  tell gloss
}
node Lock {
  key entry Keys
}

folder Dangerous {
  Locations Location
  Purpose Purpose
  Dressing Dressing
  Challenges Encounter Hazard Mystery
  Rewards Reward
  Connections Connection
  rate High Purpose=1 Dressing=1 Challenges="1-2" Rewards="1-2"
  rate Medium Dressing=1 Challenges=1 Rewards="50%"
  rate Low Dressing=1 Rewards="25%"
}
```
