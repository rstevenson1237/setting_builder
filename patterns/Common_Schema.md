# Common Schema

The values every field is written in, shared by every schema after it; a narrower schema
defining a name used here shadows it.

A field is `Label type`, then `opt`, `list` (comma-separated) or `none` (may be `none`), and
`n=N`: exactly N items, or N paragraphs of prose. How a field is set down is its `out=`, else
its value's, else `tag` for an enum and `line` for any other.
A folder's line is a file and the nodes it holds, then `opt` where a region may leave it out.
An enum field opens with one of its items, and may go on after ` - ` in prose. How many
entries a file holds is `BRIEF.md`'s.

```kdl
enum Out line prose bullets table tag readaloud   // one value on a line; paragraphs; a `- ` line each; a d6 table; a short word
                                                   // set by a title; prose read aloud to the players, set apart from the referee's
value string words=8
value gloss words=4
value tag words=2
value text out=prose          // prose, any length
value number                  // N, or a range N-M; range= bounds it
value dice                    // Nd6 or Nd6+M; count= and bonus= bound it
value percent                 // N%
value feet                    // a whole number of feet, negative where a climb goes down
value distance                // a number then a Distance_Unit: 40 feet, 1.5 miles
value point                   // "x,y" or "x,y,z": whole feet east, north and up of its frame's origin; west, south
                              // and down where negative; z is 0 where unstated
value anchor                  // "CODE side": a sibling - a region, block or location under the same parent - then
                              // north, east, south, west, above or below
value outline                 // "rect W L", "circle R" or "poly x,y x,y x,y ...": feet round the thing's origin; a
                              // poly is simple, with three points or more
value finds                   // finds split by "; ", each prose then "(N cn, N wt)"
value coin                    // N cn or N-M cn, low to high; or pennies
value time                    // N or N-M, then a Time_Unit: 2 turns, 1 watch
value location                // a location code
value region                  // a region code
value place                   // location codes first, each one that exists, then any prose after ` - `;
                              // from= names the table node placing the entry, and the codes
                              // are exactly the locations whose entries hold one naming it
value kind                    // an item of the folder's type enum
value entry                   // a title on each table the member names
value pull                    // a roll table's name, or "Table: Title" for an entry table
value relation out=bullets    // lines "- [Faction] - [Relation]", then any prose: one line for each other faction

enum Room_Shape rect round octagon hexagon cave hall   // in its width and length; a hexagon walled flat north and south;
                                                       // hall: one passage wide and at least twice as long, a DANGEROUS room's only
enum Compass north north-north-east north-east east-north-east east east-south-east south-east south-south-east south south-south-west south-west west-south-west west west-north-west north-west north-north-west
enum Distance_Unit feet yards miles
enum Ground_Type deep water marsh sand desert grass scrub forest rock snow   // the terrains a sheet draws
enum Time_Unit Round turn hour watch day week
enum Slope flat gentle steep cliff
enum Feature_Kind river road hill hollow
enum Damage_Type Nuisance Damaging Lethal     // the count of Tests a hazard asks: 1, 2 or 3
enum Reaction Hostile Wary Fearful Neutral Friendly
enum Test Constitution Fate Sanity
enum Wound_Type Piercing Crushing Poison Fire Frost Blast   // each has a Wound table in Procedures.md

// Names. A coined name is recorded in Language.md; only these fields coin. A location's name
// carries no form: it may point at a coinage already recorded, and never coins one.
enum Name_Form common family epithet tongue   // a being's: in the common tongue; a common name, then a family name
                                              // coined in a tongue; a common name, then "the Y", "son of Y" or
                                              // "of Y"; or coined wholly in a tongue
enum Place_Form common tongue                 // the setting's and a region's: in the common tongue, or coined
```
