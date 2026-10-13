# Setting Schema

The values every entry is written in, and every setting file: its fields, under the
`table` line naming it. `patterns/Region_Schema.md` and each rating's schema build on it; a
name a narrower schema defines shadows the same name here.

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
value place                   // location codes first, or "nowhere on this map", or "the referee's"
value kind                    // an item of the folder's type enum
value entry                   // a title on each table the member names
value pull                    // a roll table's name, or "Table: Title" for an entry table

enum Damage_Type Nuisance Damaging Lethal
enum Contents_Type "Treasure I" "Treasure II" "Treasure III" "Treasure IV" "Treasure V" Magic Hoards Lore Keys "Unique Treasures" "Magical Tomes"

// -- Setting.md: its name, a tag line no other setting of its genre fits, and an outline
//    of two or three sentences: what the party does here, a pressure already going wrong
//    that is not aimed at them, and what this setting has that a generic one lacks.

// -- Procedures.md: the mechanics every level cites, each resolving in one roll or none;
//    nothing that varies by rating or belongs to one place. Tailoring adjusts, never replaces.

// -- Tongues. Every coinage is registered under its tongue's "Coined here", decomposed
//    into roots, and glossed wherever it is reused; only setting and region steps coin.
enum Speakers present departed arrived side non-people jargon liturgy
table Language doc file="setting/Language.md" heading=2 step=2g {
  "Spoken by" Speakers
  Consonants text             // an inventory no other tongue shares
  Vowels text
  Syllable text               // open or closed, unlike the others'
  Affixes text                // each marks one thing: place, water, smallness, plural, belonging, age, direction, negation, title
  Roots text                  // "- root - gloss" lines naming ground, water, growth, weather, colour,
                              // body, making, exchange, light, the dead, number, direction - never abstractions
  "Coined here" text opt      // "- Noun = root + root - where it appears"
}

// -- Creatures. One stat block is one creature, or one swarm fought as a single thing.
//    AD is d6 only; a tougher creature gets more dice or a bigger bonus. A proper name
//    means a Named Creature; ordinary wildlife is a WILD region's Terrain, not an entry.
// Men human; Humanoid a non-human people; Giant a people over twice human size; Beast an
// animal, natural or grown past it; Wyrm a great reptile; Undead a dead thing not stopped;
// Construct a made thing; Horror no natural kind; Fey bound by its own rules; Fiend from
// outside the world; Fantasy this setting's own.
enum Bestiary_Type Men Humanoid Giant Beast Wyrm Undead Construct Horror Fey Fiend Fantasy
enum Sign "a mark" "a track" "a sound" "a smell"
table Bestiary entry file="setting/Bestiary.md" step=2d {
  Type Bestiary_Type
  AD dice count="1-18" bonus="-2..6"   // 1 a man's match; 2-3 superior; 4-5 larger, highly dangerous;
                                       // 6-8 supernatural; 9-12 gargantuan; 13-16 served; 17-18 a titan
  MA number range="1-6"                // targets threatened at once, about AD/4
  Description text                     // what a party sees when it comes into view
  Range text                           // where it lives, how many the land supports, what it eats
  Sign Sign                            // what reaches a party before it does
  Disposition text                     // what it does on being met, before anyone fights
  Special text                         // what its dice do not say, or `none`
}

enum Role "set piece" ranging situation survivor leader unkillable
enum Motive feeding holding searching collecting protecting expanding waiting
enum Reach "a rumour" "a piece of lore" "a survivor"
enum Memory "who hurt it" "who fed it" "who ran" "a smell" "a name" "a promise"
table "Named Creatures" entry file="setting/NamedCreatures.md" step=5a {
  Type Bestiary_Type
  AD dice count="1-18" bonus="-2..6"
  MA number range="1-6"
  "Appears at" place
  Role Role
  Motivation Motive           // a standing goal, stated without the party
  "Reaches by" Reach
  Remembers Memory list       // why a second meeting never plays like the first
  Wants text
  Description text
  Special text
}

// -- Factions. AD is set against other factions' dice and nothing else; a goal is a
//    condition acted on every turn, never a countdown.
enum Want route resource person cleared sealed legitimacy debt rival knowing hiding
table Factions entry file="setting/Factions.md" step=2e {
  AD dice bonus="0..0"
  Want Want                   // concrete enough to be interfered with
  Identity text               // repeated identically everywhere: colour, device, habit, arms, mark, phrase, tongue
  Resources text
  Knowledge text              // what makes it worth dealing with rather than only fighting
  Tactics text
  Reactions text              // noticed, crossed, injured
  Goals text
  Fields entry Bestiary list none
}

// -- The past and the rules. An event is a fact, never a clock aimed at the party, stated
//    in two sentences at most. A truth is a class, shows at more than one rating, sharpens
//    GENRE.md and never overrides it; a mystery or open truth says it is one.
enum Event_Kind founding withdrawal arrival discovery collapse war blight betrayal boundary working sealing
table History entry file="setting/History.md" step=5d {
  When text                   // years ago, vaguer the older it is
  Kind Event_Kind
  Event text
  Left text                   // the physical mark findable now
  Codes place
}
enum Truth_Kind land object custom standing limit price border "the dead" idea mystery open
table Truths entry file="setting/Truths.md" step=5d {
  Truth text                  // the rule in one sentence, not its mood
  Kind Truth_Kind
  Handle text                 // an act a referee could adjudicate
  Codes place
}

// -- Rumours: no speaker built in, and never what the players should do. A P names its
//    false half (elsewhere, count, taken, person, creature, cause, age, survivor); U is
//    the referee's by design. Each points at a region, location, person, creature,
//    treasure, event, truth, faction, route or price.
enum Truth_Mark T P F U
table Rumours roll file="setting/Rumours.md" step=5d {
  "#" number
  Rumour text
  "T/P/F/U" Truth_Mark
  "Settled at" place
}

// -- Finds. A result is the thing itself, tied to no place or container. Value is in
//    Table I's coins at about 100 per wt; wt 0 is pocketed, 1 one hand, 2 both, 3+ more
//    than one carrier, and is never shrunk to keep a number tidy.
table "Treasure I" roll file="setting/Treasure1.md" step=2f {
  "#" number
  Item text
  Value number
  Wt number
}
enum Quality poor normal fine masterwork cursed   // masterwork always has an effect; cursed presents as fine or masterwork
table "Treasure II" roll file="setting/Treasure2.md" step=2f {
  "#" number
  Item text
  Quality Quality
  Effect text                 // or -
  Value number
  Wt number
}
table "Treasure III" roll file="setting/Treasure3.md" step=2f as="Treasure I"
table "Treasure IV" roll file="setting/Treasure4.md" step=2f as="Treasure I"
table "Treasure V" roll file="setting/Treasure5.md" step=2f as="Treasure I"
enum Lasts once charges lasting
table Magic roll file="setting/Magic.md" step=2f {
  "#" number
  Item text
  Does text                   // plainly enough to adjudicate, at GENRE.md's Magic level
  Lasts Lasts
  Tell text                   // what shows it is magic before use
  Value number
  Wt number
}
table Hoards entry file="setting/Hoards.md" step=5a {   // one owner, one location
  "Found at" place
  Owner entry Bestiary Factions "Named Creatures"
  Items text
  Total text                  // value and wt, summed
}
enum Does once class adjacent solution knowledge passage ward
enum Cost toll noticed bound desperate foreign sought forbidden
enum Origin event truth lost reclaimed grave unlikely unmade   // never one nothing established accounts for
table "Unique Treasures" entry file="setting/UniqueTreasures.md" step=5a {
  "Found at" place
  Does Does
  Cost Cost list none
  Origin Origin
  Description text
}
enum Reading time tongue rite cost
table "Magical Tomes" entry file="setting/MagicalTomes.md" step=5a {   // learned, never discharged
  "Found at" place
  Teaches text
  Reading Reading
  Writer entry History Factions "Named Creatures"
}

// -- Lore is a made thing with an author inside the setting, wrong or partial (unknowing,
//    lying, secondhand, late, interested, unfinished); never spoken, never omniscient.
enum Lore_Form written cut woven drawn arranged
enum Lore_Does purpose connection hook naming dating contradiction
table Lore entry file="setting/Lore.md" step=5a {
  Form Lore_Form
  "Found at" place
  Voice text
  Does Lore_Does list
  Text text                   // read aloud in under a minute
}

// -- A key opens a lock at another location; one that opens nothing is treasure, and
//    none gates its own room.
enum Key_Form key profile fitting seal token bone word measure fragment
enum Apart deliberate transit loot burial trust later
enum Key_Link maker material measure tongue wear inscription record
table Keys entry file="setting/Keys.md" step=5a {
  Name text
  Form Key_Form
  "Found at" place
  Opens place
  Feature text
  Apart Apart
  Connection Key_Link list
}

// -- A quest points one way, and says where, even when that is nowhere on this map.
enum Ask retrieve find deliver destroy verify take collect recover message
enum Reluctance unable burned shamed needed "turned back"
enum Obstacle living guarded fragile watched contested misplaced misdescribed
table Quests entry file="setting/Quests.md" step=5d {
  Name text
  Ask Ask
  Giver text                  // who wants it, and how a party hears of it
  Reluctance Reluctance
  Object text
  Obstacle Obstacle
  Terms text                  // the giver's own words: a fee, share, favour, loan, or bait
  "Points to" place
}
```
