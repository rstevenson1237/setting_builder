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
  by the first field naming it, and named by exactly that one; a list field that holds no
  location is left out. How long each field or item runs is `BRIEF.md`'s `words`.
- what is `drawn` from the seed and the tables beside the brief, never written: Conditions,
  Inhabitants, Services, Procedures, Loot, Alarm, Leads, Secrets.
- its `design`, `setting/region/[Code]/Design.md`, for a region whose `BRIEF.md` node has a
  `design` line: what its blocks are to look like, written at step 3d before `Locations.md`.
  Each block is one `Design`, then the lines that state it - in DANGEROUS either a layout engine's
  `Use`, `Bind`, `Fill`, `Join` and `Void`, or a plan's `Layout`, `Room`, `Route` and `Void`; in SAFE
  and WILD `Fill`, `Tie`, `Street` and `Void` - and, once solved, a `Place` for each location and,
  in DANGEROUS, a `Link` for each way inside the block. Once the user approves a design, the tables are written to agree with it.

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
  against anchor opt drawn  // in place of a place from a sheet or join: touching another region, with xyz its slide and gap
  outline outline opt drawn // its area on its home sheet; written by `tools/maps.py place`
}

enum Safe_Kind steading thorp village town seat hold   // a household; a few; trades; a market and authority;
                                                        // a greater power's seat; a garrison with folk under its walls
enum Terrain hills mountains plains forest swamp desert jungle coast underground   // one, or two in combination; underground: a cavern or delving under the surface
enum Dangerous_Kind collection "single holding"   // a worked complex in blocks, sized by its die; one occupant's home, sized by what it holds -
                                                  // a lair or a seat, never a complex of rooms with no master

enum Link_Kind door passage   // a door through a wall two rooms share; a passage between rooms that do not touch
enum Facing north south east west north-east south-east south-west north-west   // the side of its parent a thing keeps to
enum Side n s e w           // the half of that side: w or e on a north or south one, n or s on an east or west one
enum Arrange cluster row column grid spine ring   // how a layout sets its rooms against one another

node Design {               // a block's design, opening with its id: layouts, chained, round the rooms they leave to the solver
  locations location list   // every location of the block; Locations.md holds exactly these
  xyz point opt             // its centre from its region's origin, as Blocks.md's
  outline outline opt       // the ground its rooms fill; unset, they grow out from xyz and the outline is the hull of what they hold
  fill string opt           // the share of the outline the rooms cover, "N-M%"; unset, BRIEF.md's pack
  spacing string opt        // the passage wanted between joined rooms, "N-M feet"; sets passages and detour where they are unset, and its most is how far joined rooms may stand apart
  pad string opt            // "N feet" kept clear round each room, so joined rooms stand twice it apart, a passage between
  passages percent opt      // the share of ways run as passages; unset, BRIEF.md's pack
  detour distance opt       // the most a way may walk beyond the straight line; unset, BRIEF.md's pack
  hull outline opt drawn    // where it states no outline, the ground the solved rooms and ways hold, which Blocks.md draws
  seed number opt drawn     // the solver's seed for the places below
  score string opt drawn    // the engine's score for that seed, out of 100
  approved string opt       // the date the user approved it; only their word sets it
  facing Facing opt         // a plan: the side of the region it keeps to, where it states no xyz
  side Side opt
  width feet opt            // a plan: its passages' width, 5 or 10; 10 where unset
}
node Layout {               // a plan: a group of rooms set against one another, placed in the block as one, opening with the block's id
  id tag                    // its name, which a Room and a Route cite
  arrange Arrange opt       // cluster where unset; a spine's or ring's first room (or entry) is its hall or hub
  gap feet opt              // between its rooms; 0, sharing walls, where unset
  xyz point opt             // its centre from the block's; unset, where its routes run best
  facing Facing opt         // unset xyz: the side of the block it keeps to
  side Side opt
  entry location opt        // the room a route to the layout reaches, and a spine's hall or a ring's hub
  links string opt          // auto: the arrangement joins its rooms; none: only routes join its locations
  cols number opt           // a grid's rooms a row
  align Side opt            // a row's or column's rooms lined up on one side; centred where unset
  door string opt           // the door between its rooms: a door kind; door where unset
}
node Room {                 // a plan: one location, opening with its code, or rooms no location holds, opening with the block's id
  layout tag opt            // the layout it is part of; the block's own where unset
  width feet opt            // across and along, in 10 ft steps; 20 where unset
  length feet opt
  shape string opt          // a Room_Shape, or diamond: a square turned on its point; rect where unset
  xyz point opt             // its centre from its layout's, or the block's
  facing Facing opt         // unset xyz: the side of its parent it keeps to; in a ring, the hub's side it stands on
  side Side opt
  count number opt          // opening with the block's id: how many such rooms
  label string opt          // a name for a room no location holds
}
node Route {                // a plan: a way between two or more ends, opening with the block's id; every goal it states gives way to a route that works
  ends text                 // "end, end, ...": each a location, a layout, this block (its edge) or a location of another block, then
                            // ":facing" - the wall it leaves by, a layout's or block's outermost on that side - then ":side", its half
  length string opt         // short (where unset), long (as long as fits), or N 10 ft squares, or "N feet"; of its first two ends
  kind Link_Kind opt        // door: through a wall the first two ends share, set against one another; passage where unset
  door string opt           // the door at each end, one kind or one an end: door, secret, locked, portcullis, arch, double, open, none
  width feet opt            // 5 or 10; the Design's where unset
  stair string opt          // up or down: a way out of the block drawn as a stair in its room; a block over or under is one unasked
  style string opt          // natural: rough walls; built where unset
  line string opt           // straight: a cleft from one edge of the block to another, laid before the rooms, which keep off it
                            // and passages cross; up to 20 ft wide
  label string opt          // a note; a cleft's, at each edge
}
node Use {                  // a layout in the block, opening with the block's id
  id tag                    // its name in the block, which a Bind and a Join cite
  layout string             // a layout's id, as `tools/design.py layouts` lists them
  params string opt         // "name=N" pairs, in the layout's own terms and range (sizes in 5 ft cells)
}
node Bind {                 // a role of a Use given its locations
  use tag
  role tag
  locations location list
  type kind list            // one type for every location of the role, or one for each, in order
  pad string opt            // "N feet", in place of the design's for these rooms
}
node Fill {                 // locations no layout binds: plain rooms the solver places
  locations location list
  type kind list            // as a Bind's
  width feet opt            // each room's across and along; unset, the solver's size for the type
  length feet opt
  pad string opt            // as a Bind's
  shape Room_Shape opt      // rect where unset
  outline outline opt       // a "poly" where no shape draws the room: its extent is its width and length
}
node Tie {                  // SAFE and WILD: one location a bearing and distance from another, which the solver holds
  from location
  to location
  bearing Compass
  distance distance
}
node Street {               // SAFE and WILD: a street, the buildings it runs past in order from its start
  past location list
  kind gloss opt            // a road kind; a street where unset
}
node Join {                 // a way between two ends: a Use's socket, or a location code
  from string               // "use.socket", or a location code
  to string                 // as from; a location of another block is a way out of this one
}
node Void {                 // ground within the block that no location or way takes; in DANGEROUS the block's Rock
  what gloss                // what fills it, written on its map
  outline outline           // feet round its xyz
  xyz point opt             // its centre from its block's; the block's centre where unstated
}
node Place {                // opening with a location code: where the solver put it; written by `tools/design.py accept`
  xyz point drawn
  outline outline opt drawn // a "poly" where no shape draws the room
  shape Room_Shape opt drawn
}
node Link {                 // opening with a location code: a way to another location of the block; written by `accept`
  to location drawn
  kind Link_Kind drawn
}

node Rung {                 // what the situation does next, true whether or not a party engages
  if string                 // what sets it off
  then text                 // what follows
}
node Entry {                // a way in
  name gloss
  from string opt           // where it opens from
  stands text               // who or what stands at it or watches it
  takes text opt            // what passing takes; a word, key or token it takes is a Lock on the
                            // way's Connection, naming a Key that says where it is found
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
    Entrances text list out=bullets holds=entrance   // how it shows from outside
    Prizes text list out=bullets holds=High     // what holds it, and its prize
    Places text list out=bullets holds=rest     // what is noticed or heard there, a secret shown only as what a party can notice
    Tables text out=table   // d6 Danger: its rows numbered 6 (noticing) down to 1 (acting), in that order
  }
  drawn Conditions Inhabitants Loot Alarm Procedures Leads Secrets
}
```
