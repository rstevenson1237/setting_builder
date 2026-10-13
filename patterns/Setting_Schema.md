# Setting Schema

The values every table entry is written in, and the setting files an entry names or pulls
from. `patterns/Region_Schema.md` and each rating's schema build on it; a name a narrower
schema defines shadows the same name here.

```kdl
value string words=8
value gloss words=4
value tag words=2
value number                  // N, or a range N-M
value percent                 // N%
value location                // a location code
value kind                    // an item of the folder's type enum
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

enum Damage_Type Nuisance Damaging Lethal
enum Contents_Type "Treasure I" "Treasure II" "Treasure III" "Treasure IV" "Treasure V" Magic Hoards Lore Keys "Unique Treasures" "Magical Tomes"
```
