# Common Schema

The values every field is written in, shared by every schema after it; a narrower schema
defining a name used here shadows it.

A field is `Label type`, then `opt`, `list` (comma-separated) or `none` (may be `none`).
An enum field opens with one of its items, and may go on after ` - ` in prose. How many
entries a file holds is `BRIEF.md`'s.

```kdl
value string words=8
value gloss words=4
value tag words=2
value text                    // prose, any length
value number                  // N, or a range N-M; range= bounds it
value dice                    // Nd6 or Nd6+M; count= and bonus= bound it
value percent                 // N%
value location                // a location code
value place                   // location codes first, each one that exists, then any prose after ` - `;
                              // from= names the table node placing the entry, and the codes
                              // are exactly the locations whose entries hold one naming it
value kind                    // an item of the folder's type enum
value entry                   // a title on each table the member names
value pull                    // a roll table's name, or "Table: Title" for an entry table

enum Damage_Type Nuisance Damaging Lethal     // the count of Tests a hazard asks: 1, 2 or 3
enum Wound_Type Piercing Crushing Poison Fire Frost Blast   // each has a Wound table in Procedures.md
// Names. A coined name is recorded in Language.md; only these fields coin. A location's name
// carries no form: it may point at a coinage already recorded, and never coins one.
enum Name_Form common family epithet tongue   // a being's: in the common tongue; a common name, then a family name
                                              // coined in a tongue; a common name, then "the Y", "son of Y" or
                                              // "of Y"; or coined wholly in a tongue
enum Place_Form common tongue                 // the setting's and a region's: in the common tongue, or coined
```
