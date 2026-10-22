# Dangerous Schema

A DANGEROUS region's tables: rooms behind doors, and what a room hides. Its seed and
brief are `patterns/Region_Schema.md`'s.

```kdl
enum Dangerous_Type High Medium Low
enum Connection_Type Open Archway Broken Crude Wooden Banded Stone Iron Lift Chute   // Lift and Chute: a dwarven machine, with `climb` for the rise
enum Contents_Type "Treasure I" "Treasure II" "Treasure III" "Treasure IV" "Treasure V" Magic Hoards Lore Keys "Unique Treasures" "Magical Tomes"
enum Mystery_Type Altar Statue Fountain Fresco Tapestry Throne "Button/Lever/Switch/Keyhole" Mirror Flooring
enum Hazard_Type {
  Mechanical Pit Spike Dart Hammer Gas
  Magical Runes Field Attack
  Environmental "Fire/Lava" Water Ice "Ravine/Climb" "Broken/Weak Floor"
}

node Seed {
  kind Dangerous_Kind
  comes text                // what a party sees at the way in, and what it comes for
  who entry Bestiary Factions "Named Creatures" list   // who lives here; the tables place them
  changing text             // what is changing; a single holding barely moves the Danger track: what presses instead
}
node Conditions {           // every room, unless a Dressing, Block or Connection says otherwise
  material gloss
  height feet
  width feet                // of a passage
  light gloss
  sound string              // what carries it and what hides it
  footing gloss
  air gloss
  fire string               // what a lit fire does
}

node Location {
  name string               // per GENRE.md's Naming, after the rest is decided; named only where
                            // something refers to it again. In whose mouth: border passers,
                            // the departed, or its occupants
  tags tag list n=3
  type kind
}
node Dressing {
  obvious string
  former gloss opt
  condition tag opt
  ambiance gloss opt
  width feet                // across, west to east as the room lies; a round room's diameter
  length feet               // north to south
  height feet opt           // floor to roof, where it matters at the table
  shape Room_Shape opt      // rect where unset
  layout string
  mark entry Factions list opt   // the faction whose Identity shows here
  left entry History list opt    // the event whose Left mark shows here
}
node Encounter {
  one-of Creature NamedCreature Faction
  doing string
  reaction Reaction
  answers time opt          // how soon it reaches an alarm raised elsewhere in its region; unset, it does not come
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
node Procedure {
  procedure entry "Local Procedures"
}
node Purpose {
  unique string opt
  pressure string opt
  signs location list opt
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
  bearing Compass           // from this end
  distance distance
  climb feet opt            // up, or down where negative, where the way changes level
  orientation gloss opt     // the same in words, for the reader
  width feet opt            // where it differs from its block's; within both rooms' footprints
  height feet opt
  one-of Encounter Hazard Mystery Secret Lock opt
}
node Block {               // one level: a map of its own
  name string
  locations location list
  width feet opt            // of its passages, where they differ from the seed's Conditions
  height feet opt
}
node Secret {              // what sets off or opens the thing it sits on, and what gives it away
  trigger gloss
  tell gloss
  knows gloss opt           // who knows it, or nobody
  fact string opt           // what it hides, where the node it sits on does not say
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
  Procedures Procedure
  Blocks Block
  Connections Connection
}
```
