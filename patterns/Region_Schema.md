# Region Schema

What `setting/region/` holds for each region, by rating: its `seed`,
`setting/region/[Code].md`, written before any location exists and naming none, and its
`brief`, `setting/region/[Code]/Brief.md`, written from the tables alone. The tables
themselves are the rating's own schema.

Every seed and brief sentence carries something usable at the table - a name, count,
price, place, distance or ruling; why a place exists or how it feels is cut, and nothing
is said twice. A secret always carries its answer. A situation is true whether or not the
party engages: what is changing, then two rungs, each with what sets it off. A Layout is enough to draw from: an artist given it alone
draws the region's plan and its view without a guess, every measure agreeing with every
other and with each location's `at`. A list field writes each item as its own `- ` line,
and paragraphs are separated by a blank line.

```kdl
enum Safe_Kind steading thorp village town seat hold   // a household; a few; trades; a market and authority;
                                                        // a greater power's seat; a garrison with folk under its walls
enum Terrain hills mountains plains forest swamp desert jungle coast   // one, or two in combination
enum Dangerous_Kind collection "single holding"   // a worked complex in blocks, sized by its die; one occupant's home, sized by what it holds

region Safe {
  seed {
    Kind Safe_Kind
    Overview text           // what a party comes to do; then its situation: who is behind it, and who is hurt
    View text               // from where and how far off it is first seen; its outline and size; its walls or
                            // edges, their height and material; the ground under it; roofs, colours, devices, lights
    Approach text           // every way in: what stands at it, what passing takes, what befalls the turned away
    Law text                // what gets a stranger fined, locked up or put out; who enforces; what each costs
  }
  brief {
    Layout text n=3         // every location by code: the seed's View, then its Approach at each way in;
                            // the plan - its outline, blocks and main ways, and every location at its `at`,
                            // with its footprint; what each location holds and what a party goes there
                            // for, a secret or rule shown only as what a party can notice
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
    Overview text           // what a party sees crossing in, who is out here, what brings anyone; then its situation
    Approach text           // where it is entered, and how long a crossing takes on the best route and off it
    Terrain Terrain         // then rulings per setting/Procedures.md's Time and Distance: what an action buys on a road,
                            // off it, through the worst; what loses a party and finds the way; weather,
                            // night, a fire. Ground is never a location.
  }
  brief {
    Layout text n=3         // every location by code: each way in and each Route - where it runs, how long, the
                            // seed's Approach folded in; each Landmark at its `at` - what shows of it and from
                            // how far, and how it is reached from the route; the rest at its `at`, in prose,
                            // a secret or rule shown only as what a party can notice
    Inhabitants text        // every creature and faction the Encounters hold, how many, where and what they are about
    Loot text               // one sentence on what the land yields; then forage and game by local name, what the
                            // nearest SAFE region pays, and treasure, where. Anything dangerous enough to meet is
                            // an Encounter, never game.
    Secrets text
    Leads text
    Tables text             // d6 Encounter
  }
}

region Dangerous {
  seed {
    Kind Dangerous_Kind
    Overview text           // what a party sees at the way in, who lives there, what it comes for; then its
                            // situation - a single holding barely moves the Danger track: name what presses instead
    Approach text           // every entrance: where it opens from, who or what watches it
    Conditions text         // every room unless it says otherwise: material, height and width,
                            // light, what carries sound, footing, air, what a lit fire does
  }
  brief {
    Layout text n=3         // every location by code: each entrance - how it shows from outside, the seed's
                            // Approach and Conditions folded in; each High location - where it lies from the
                            // entrance, its size, what holds it, its prize; the rest in prose, each room at the
                            // compass point and distance from the room it opens off, a secret or rule shown only
                            // as what a party can notice
    Inhabitants text        // every creature and faction the Encounters hold, how many, where and what they are about
    Alarm text              // what raises it, who hears first, who comes from where, how many turns later
    Loot text               // one sentence on the region's wealth; then the largest prize and what stands over it,
                            // treasure, where, and who buys it back
    Secrets text            // - the fact - the entry that brings it out
    Leads text              // - each rumour by number, each quest by name
    Tables text             // Danger, 6 noticing to 1 acting
  }
}
```
