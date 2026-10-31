# Region Schema

What `setting/region/` holds: the gazetteer, `Regions.md`, one `Region` node a region, then for
each region, by rating, beside its tables:

- its `seed`, the nodes of `setting/region/[Code]/Seed.md`, written before any location
  exists and naming none, each opening with the region code. A `seed` line names its
  nodes in order, each `=N`, exactly N, or `="1+"`; a node its rating's schema defines is
  that rating's own.
- its `brief`, `setting/region/[Code].md`, written from the seed and the tables and stale
  when they change: the seed's fields as prose, then one list field per `holds=`, each
  item opening with the codes it is about. `holds=` names location types, `entrance`
  (a location joined to a region that is not DANGEROUS) or `rest`; each location is held
  by the first field naming it, and named by exactly that one. How long each field or item
  runs is `BRIEF.md`'s `words`.
- what is `drawn` from the tables beside the brief, never written: Inhabitants, Services,
  Procedures, Loot, Alarm, Leads, Secrets.

Every brief sentence carries something usable at the table - a name, count, price, place,
distance or ruling; why a place exists or how it feels is cut. A brief is read beside the
region's maps, `Ground.md` and what is drawn: it says what they cannot, what a party
notices and hears, and restates no place, size, height, person or price they show.

```kdl
enum Rating SAFE WILD DANGEROUS
enum Region_Die d4 d6 d8 d10 d12
node Region file="setting/region/Regions.md" {   // opens with the region's code; one or two capital letters, ascending; a first letter holds one region or a group (FA, FB), never both
  name string               // per GENRE.md's Naming
  form Place_Form           // of the name
  gloss gloss               // what a tongue name means; `none` where the name is plain
  rating Rating
  die Region_Die            // BRIEF.md's, per Procedures.md
  joins region list         // every region it borders, and the WILD region a DANGEROUS one opens from; a join is mutual
  tag string                // one phrase, the region one step past its name
  xyz point opt drawn       // its origin - its way in, a DANGEROUS region's first block's centre - from the setting's,
                            // BRIEF.md's origin region's way in; unset, placed from a sheet or join it shares with a placed region
  outline outline opt drawn // its area on its home sheet; written by `tools/maps.py place`
}

enum Safe_Kind steading thorp village town seat hold   // a household; a few; trades; a market and authority;
                                                        // a greater power's seat; a garrison with folk under its walls
enum Terrain hills mountains plains forest swamp desert jungle coast   // one, or two in combination
enum Dangerous_Kind collection "single holding"   // a worked complex in blocks, sized by its die; one occupant's home, sized by what it holds

node Rung {                 // what the situation does next, true whether or not a party engages
  if string                 // what sets it off
  then text                 // what follows
}
node Entry {                // a way in
  name gloss
  from string opt           // where it opens from
  stands text               // who or what stands at it or watches it
  takes text opt            // what passing takes
  refused text opt          // what befalls the turned away
}

region Safe {
  seed Seed=1 View=1 Rung=2 Entry="1+" Law="1+"
  brief {
    Overview text           // the Seed and both Rungs, each with what sets it off
    View text
    Approach text           // every Entry
    Law text                // every Law
    Arrival text list out=bullets holds=Gate    // what a party meets there that the Approach does not say
    Plan text               // how the locations sit, what is reached through what
    Places text list out=bullets holds=rest     // what each holds and what a party goes there for, what is noticed
                                    // or heard there, a secret shown only as what a party can notice
    Tables text out=table   // d6 Events
  }
  drawn Inhabitants Services Leads Secrets
}

region Wild {
  seed Seed=1 Rung=2 Entry="1+" Ruling="1+"
  brief {
    Overview text           // the Seed and both Rungs, each with what sets it off
    Approach text           // every Entry, and the crossing on and off the best route
    Terrain text            // the Seed's terrain, then every Ruling
    Ways text list out=bullets holds=Route      // how long it takes, its stops in order and where each leads
    Landmarks text list out=bullets holds=Landmark   // what shows of it and from how far, how it is reached from a Way
    Places text list out=bullets holds=rest     // what is noticed or heard there, a secret shown only as what a party can notice
    Tables text out=table   // d6 Encounter
  }
  drawn Inhabitants Procedures Leads Secrets
}

region Dangerous {
  seed Seed=1 Rung=2 Entry="1+" Conditions=1
  brief {
    Overview text           // the Seed and both Rungs, each with what sets it off
    Approach text           // every Entry
    Conditions text
    Entrances text list out=bullets holds=entrance   // how it shows from outside
    Prizes text list out=bullets holds=High     // what holds it, and its prize
    Places text list out=bullets holds=rest     // what is noticed or heard there, a secret shown only as what a party can notice
    Tables text out=table   // Danger, 6 noticing to 1 acting
  }
  drawn Inhabitants Loot Alarm Procedures Leads Secrets
}
```
