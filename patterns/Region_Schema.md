# Region Schema

What `setting/region/` holds for each region, by rating: its `seed`,
`setting/region/[Code].md`, written before any location exists and naming none, and its
`brief`, `setting/region/[Code]/Brief.md`, written from the tables alone. The tables
themselves are the rating's own schema.

Every seed and brief sentence carries something usable at the table - a name, count,
price, place, distance or ruling; why a place exists or how it feels is cut, and nothing
is said twice. A secret always carries its answer. A situation is true whether or not the
party engages: what is changing, then two rungs, each with what sets it off. Places is an
index, never a description. A list field writes each item as its own `- ` line, and
paragraphs are separated by a blank line.

```kdl
enum Safe_Kind steading thorp village town seat hold   // a household; a few; trades; a market and authority;
                                                        // a greater power's seat; a garrison with folk under its walls
enum Terrain hills mountains plains forest swamp desert jungle coast   // one, or two in combination
enum Dangerous_Kind collection "single holding"   // a worked complex in blocks, sized by its die; one occupant's home, sized by what it holds

region Safe {
  seed {
    Kind Safe_Kind
    Overview text           // what a party comes to do; then its situation: who is behind it, and who is hurt
    Approach text           // every way in: what stands at it, what passing takes, what befalls the turned away
    Law text                // what gets a stranger fined, locked up or put out; who enforces; what each costs
  }
  brief {
    Layout text n=3         // every location by code: the view from afar, then the seed's Approach folded
                            // in at each way in; the plan - its blocks or main ways, and the compass point
                            // and distance between them; what each location holds and what a party goes
                            // there for, a secret or rule shown only as what a party can notice
    Inhabitants text        // every Person, Named Creature, Faction and Garrison the People and Garrison
                            // tables hold, where and what they are about, a faction's members for what
                            // its Identity shows
    Services text           // one sentence on the economy; then what is sold, done and bought from a
                            // party, at what price and where, and what cannot be had
    Secrets text            // - the fact - who knows it; the entry that brings it out
    Leads text
    Tables text             // d6 Events
  }
}

region Wild {
  seed {
    Overview text           // what a party sees crossing in, who is out here, what brings anyone
    Approach text           // where it is entered, and how long a crossing takes on the best route and off it
    Terrain Terrain         // then rulings per setting/Procedures.md's Time and Distance: what an action buys on a road,
                            // off it, through the worst; what loses a party and finds the way; weather,
                            // night, a fire. Ground is never a location.
    Situation text
  }
  brief {
    Layout text             // the region as a plan: its routes, each way in, and the compass point and distance from the way in to each landmark, by location code
    Places text             // every Landmark: what shows from a distance, what a party goes for
    Inhabitants text        // one sentence: every creature and faction the Encounters hold, how many, where
    Loot text               // forage and game by local name, what the nearest SAFE region pays; treasure
                            // tables. Anything dangerous enough to meet is an Encounter, never game.
    Secrets text
    Leads text
    Tables text             // d6 Encounter
  }
}

region Dangerous {
  seed {
    Kind Dangerous_Kind
    Overview text           // what a party sees at the way in, who lives there, what it comes for
    Approach text           // every entrance: where it opens from, who or what watches it
    Conditions text         // every room unless it says otherwise: material, height and width,
                            // light, what carries sound, footing, air, what a lit fire does
    Situation text          // a single holding barely moves the Danger track: name what presses instead
  }
  brief {
    Layout text             // the region as a plan: its blocks and main passages, each entrance, and the compass point and distance between them, by location code
    Places text             // each block, or a single holding's notable rooms: codes, way in, prize, rival
    Inhabitants text        // one sentence: every creature and faction the Encounters hold, how many, where
    Alarm text              // what raises it, who hears first, who comes from where, how many turns later
    Loot text               // the largest prize and what stands over it; treasure tables; who buys it back
    Secrets text            // - the fact - the entry that brings it out
    Leads text              // - each rumour by number, each quest by name
    Tables text             // Danger, 6 noticing to 1 acting
  }
}
```
