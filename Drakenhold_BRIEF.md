# Brief

Drakenhold, written as a `BRIEF.md`: a candidate to replace the Thornmarch one, not read by any
step until it is copied over. Everything in the block is the framework's grammar; where the
write-up and the framework disagree, the block follows the framework and says what the
write-up had in a `// was` comment. Below the block: what changed in the framework for it,
how the write-up's inconsistencies were settled, and a proposed next development.

This build's design requests: every count, mix and rate it is built to, and what this one
setting should hold. Templates and schemas set none of their own.
It never overrides a schema's rules or `STYLE.md`.

- `files`, `safe`, `wild` and `dangerous` hold the framework's levers at reasonable
  defaults. Change a value to customise it.
- `setting` holds this setting's outline and what it asks of the setting files.
- `region` holds one region each, in gazetteer order: its rating, die, location count and
  outline, and any target of its own.

A share is `"N%"`, at least that share of entries rounded down to whole entries, or `"<=N%"`,
at most; a count is `N`, a range `"N-M"`, or `"N+"`, at least. A region's target replaces the
rating's only for the values it names. A quoted line is prose, read by the
step that writes what it names. A `target` is measured by `tools/metrics.py`; a `rate` is
how many entries each location of a type holds in a table file; `words` is how long each
field of a region's brief runs, or each item of a list field and each row of a table.
An `architecture` or `construction` line in `setting` is how its SAFE or DANGEROUS regions are
built, so a region states only where it differs.

The maps are asked for here. `setting` holds a `sheet` per terrain map: its name, `square`
(a distance), `extent` (`"W by H unit"`) and `regions`, the codes it holds; a DANGEROUS region
is on none. A region on a sheet may hold one `ground` line, a terrain its area must have, then
prose the writing reads and the solver does not, and `place` lines: another region on a sheet
with it, a compass direction, and a distance or `"N-M unit"` from that region's way in.

```kdl
// -- Framework levers ----------------------------------------------------------

files {
  Treasure rolls=20 provenance="20%" ceiling=100 {   // ceiling: no result above 100x its table's mean
    average I="0-500"                                // a table's mean, in the standard coin
    quality table=II poor="10%" normal="50%" fine="30%" masterwork="5%" cursed="5%"
    price normal=100 fine="3-10x" masterwork="10-100x"   // Table II, against a normal item
    effect fine="33%"                                // share of each quality carrying an effect
    spread "Result 1 sits well below the table's average; results 2 and 3 are each slightly below it, or about double the average weight for their value."
  }
  Magic rolls=12
  Rumours die=12 T=4 P=3 F=3 U=2
  Bestiary specials-from=4                           // AD below which a Special is rare
  Factions count=6 marks=2                           // the write-up's six
  Quests count=7                                     // was 5: the write-up's hooks need seven
  History events=13                                  // the write-up's thirteen
  Truths count=9                                     // the write-up's nine
  Language affixes="3-5" roots="15-20" clues=4       // per tongue; clues: Lore entries that teach the runic script
  Procedures wounds="Piercing Crushing Poison Fire Blast" madness=6   // Blast: rune detonations and a dragon's breath
}

safe {
  rate Inn Dressing=1 Purchases="2-4" People="2-3"
  rate Merchant Dressing=1 Purchases="2-4" People="1-2"
  rate Bank Market Dressing=1 Purchases="1-3" People="1-2"
  rate Authority Dressing=1 Purchases="0-2" People="1-3" Garrison="0-1"
  rate Gate Dressing=1 Purchases="0-1" People="1-2"
  rate Secret Dressing=1 Purchases="0-1" People="0-1"
  words Overview=120 View=90 Approach=90 Law=70 Arrival=50 Plan=90 Places=35 Tables=25
}

wild {
  rate Lair Dressing=1 Challenges=1
  rate Ruin Natural Hidden Secret Dressing=1 Challenges="0-1"
  rate Route Dressing=1 Challenges="0-1" Stops="3-6"
  words Overview=120 Approach=80 Terrain=110 Ways=120 Landmarks=40 Places=40 Tables=25
}

dangerous {
  rate High Purpose=1 Dressing=1 Challenges="1-2" Rewards="1-2"
  rate Medium Dressing=1 Challenges=1 Rewards="0-1"
  rate Low Dressing=1 Rewards="0-1"
  words Overview=100 Approach=70 Conditions=70 Entrances=60 Prizes=50 Places=35 Tables=25
  target Location.type High="17%" Medium="50%" Low="33%"
  target Hazard.damage Nuisance="40%" Damaging="40%" Lethal="20%"
  target Reward.contents Keys="20%" Lore="20%"       // was 10% and 15%: rods, tiles and names are keys, and runes are lore
}

// -- This setting --------------------------------------------------------------

setting {
  // Frontier is the approach; Hold is the Outer City and the Skybridge among the three peaks;
  // Village is Thornhaven. Distances on the approach are assumed, not in the write-up.
  sheet Frontier square="200 yards" extent="22 by 10 miles" regions="A B C D E"
  sheet Hold square="20 yards" extent="1.6 by 1.2 miles" regions="E I"
  sheet Village square="10 feet" extent="200 by 150 yards" regions="A"
  test "Drakenhold in play, not in text: a party outfits at a dwindling river village, walks the Ironwood to a ruined dwarf-hold, and chooses a way in - the broken Trade Hall doors, the Skybridge, a servants' passage - then climbs and descends three peaks of halls where the right rod, tile or spoken name opens what force cannot. A sleeping dragon that no party can fight lies in the second peak's heart, and the way to ruin him lies in a tomb on the third. Every location type, procedure kind and registry the framework has is used at least once."
  outline "One mountain hold of three peaks, a day from the last village: Thornhaven at the river and the Ironwood's edge; the wood trail, the goblin camps and the river crossing between it and the hold; the ruined Outer City below the peaks; and fifteen levels of halls, vaults, crypts and lost caverns, where runes, rods, tiles and names are the locks and the dwarves' machines are the roads."
  pressure "Something under Drakenhold is stirring again. Evil comes up from the lost caverns, the kobolds still carry tribute to a dragon that has slept for ten years, and Thornhaven feels it first: strays gone from the wood's edge, a witch who blames the village, and a rougher class drifting in on a rumour of hoards. Nobody there knows what wakes Vermakith, and nobody knows where the stolen artifact went."
  history "The hold's founders carved three halls into three peaks and found the caverns under them; it was dwarven work for twelve centuries."
  history "Dragons assaulted the peaks three centuries ago and were beaten with ancient magic, and the Runemasters were given the Third Peak for it."
  history "The Breaking, thirty-two years ago, ended the dwarven kingdom: its king killed, its clans at war, its last loyalists dead in the Armory."
  history "Vermakith came thirty years ago, took the second peak, and has slept there for ten."
  truth "The runic script of the hold's first inhabitants states its basic features, runs through every puzzle and trap, is the Runemasters' tool for wards and incantations, and carries clues that help a reader translate it."
  truth "Complex carved stone tiles, fitted to their receptacles, open ways in the hold."
  truth "Rods of precious metal carved with runes, not keys, open the hold's secured portals: some open many, and the highest security wants several specific rods, one lock after another."
  truth "The dwarves invented complex machinery and earth-powered magic: traps, ritual sites, and marvellous ways of moving people and things."
  truth "Seven sat the council: two of the trade guilds, two Runemasters, the Steward of Drakenhold, the leader of the guard, and the King."
  truth "Names hold power: speaking a name from the dwarven past opens secret doors, wakes magical effects and lets a speaker talk with the wraiths of long-dead dwarves."
  truth "The dragon's name is Vermakith. The last King is divisive and his name is stricken from many places and kept in others; the Dwarven Knight's name is written nowhere officially and survives in graffiti and private writings."
  truth "Beneath the Runemasters, guilds and royals lived an underclass of servants, staff and slaves, and a few survivors hide in the servants' passages deep in the hold."
  truth "In the Knight's burial tomb lies a magical lance that may bring ruin on the dragon."
  procedures "Hazards are Tests of Constitution and Fate, and a Test of Sanity only where the harrowing's evil has touched the stone: the Sanctuary and the lost caverns. Poison is Lethal at least once, in a hazard or a creature's Special. Machines deal Crushing and Piercing; runes deal Blast."
  architecture "Thornhaven is a river village built for a larger trade than it keeps: timber-framed houses on stone footings with slate and thatch patched, a landing on black piles, and two stone buildings from its better days, now put to rougher use."
  construction "Dwarven cut grey granite throughout: passages eight feet wide and twelve high, halls to forty; rune-lamps long dark; sound carries down straight halls and stone doors muffle it; footing is paved and worn at the stairs; the air is dry and cold, warmer toward the forge; a lit fire draws on the old flues."
  tongue "the common tongue of Thornhaven and the river trade - Law's"
  tongue "the rough cant of the wood and the road, spoken by goblins, hobgoblins, kobolds, transients and anyone who looks after themselves - Neutrality's"
  tongue "the dead tongue of the hold's makers, spoken only by wraiths and survivors and cut in runes across every wall - Law's"
  tongue "the wyrm-speech of the lizardmen and of Vermakith, heard in his servants' mouths - Chaos's"
  bestiary Wolf Automaton "Living Statue" "Skeletal Warrior" Shadow "Dwarven Wraith" "Ancient Wyrm" "Minor Wyrm" Ooze Kobold "Kobold Warrior" "Kobold Chieftain" Goblin "Goblin Chieftain" Hobgoblin "Lizard Man" Owlbear "Dwarven Survivor" "Giant Spider" "Wood Sprite"   // up front; the rest added as a location needs them
  bestiary-note "Vermakith is a Named Creature, not a Bestiary entry. A Minor Wyrm is a weaker subtype of the Ancient Wyrm. Men are the rank and file a faction fields, never one entry per human occupation. No two tribes' creatures share both an AD and a Special; the kobold and goblin chieftains differ in their Special, and so does the Living Statue from either."
  faction "the Dragon: AD 6d6, Vermakith, a great red dragon from the north, asleep in the second peak"
  faction "the kobolds: AD 2d6, both drawn to and fearful of the dragon and the lizardmen"
  faction "the lizardmen: AD 3d6, Vermakith's direct servants, who exist to do his bidding and strike fear in his name, especially on intruders and kobolds"
  faction "the dwarven survivors: AD 1d6, small groups of the underclass hiding in fear in the servants' quarters of the hold"
  faction "the goblins: AD 1d6, decrepit bandits making a living in small camps throughout the Ironwood"
  faction "the hobgoblins: AD 2d6, raiders and scavengers round the hold who send parties into the ruined city and the hold and sometimes terrorise Thornhaven"
  relations "Vermakith holds the lizardmen Friendly, the kobolds Tolerated and every other faction Antipathy; the lizardmen hold the kobolds Antipathy and everyone else Hatred."
  relations "The kobolds hold Vermakith and the lizardmen Tolerated (fear), the goblins Neutral and the hobgoblins and survivors Antipathy; the goblins and the hobgoblins hold each other Antipathy."
  relations "The survivors hold Vermakith and the lizardmen Hatred (fear). Every pair not named is Neutral."
  rumours "Twelve, each pointing at a place or person: the haunted basement and its relics, the witch, the goblins' offer, the hobgoblin bridge, the silent dragon, the rods, the names, the lance, the survivors, the kobold chieftain's defection, the Skybridge, and the lost caverns. At least one is true and sounds false, and each P names which place, count or person is wrong."
  quest "a reeve's and neighbours' bounty to lay the haunted farmstead's relics to rest, given at Thornhaven"
  quest "the witch's demand: keep the village back from the wood's edge, or find who is taking the strays"
  quest "a factor's offer for proof the northern road is open again, given at the river landing"
  quest "a survivor's plea to carry word to kin in the servants' passages and learn the Knight's name"
  quest "the Guildmaster's master rod, wanted by a transients' leader and by the factor"
  quest "the Knight's lance, sought by the survivors and by anyone who has heard Vermakith can be ruined"
  quest "the stolen artifact, found and sealed or destroyed, wanted by a survivor who remembers the Breaking"
}

// ---- The approach ------------------------------------------------------------

region A rating=SAFE die=d6 locations=11 people=14 {
  ground grass "a river meadow at the Ironwood's western edge, the river landing on the south side and the trail leaving east into the wood"
  outline "Thornhaven: a small river village past its best - a trail gate toward the Ironwood and a landing gate on the river, two inns, one a doss house for transients, two merchants, a factor's counting house at the landing, a market, the reeve's house and the chapel, and one hidden thing: the basement of a farmstead on the edge, over a cemetery that once lay under it, whose dead walk at night when the relics are disturbed. Natives and transients dislike each other; a witch at the wood's edge holds the village to blame. Joins the Ironwood Trail."
  target Location.type Gate=2 Inn=2 Merchant=2 Bank=1 Market=1 Authority=2 Secret=1
  procedure "Selling what a party carries home, at the factor's counting house."
}

region B rating=WILD die=d10 locations=7 {
  ground forest "the Ironwood, dark and close, the trail a narrow ride through it"
  place A east "0.25-0.5 miles"
  outline "The Ironwood Trail: the northernmost passable way from the west, dark and encroached by the wood - giant spiders in the thickets, wood sprites that move trail markers and mimic voices, goblin bandits at the narrow places. A burned wayhouse, a hanging tree, a spider thicket, a sprite glade, and the witch's hut at the margin. Joins Thornhaven, the goblin camps and the river crossing."
  target Location.type Route=1 Landmark=2 Lair=2 Hidden=1 Ruin=1
  procedure "Forage and hunt in the wood."
}

region C rating=WILD die=d6 locations=8 {
  ground forest "dense wood north of the trail broken by scrub and hollows"
  place B north "2-3 miles"
  outline "The Goblin Camps: three hidden camps of a tribe that lives on banditry and scavenging, willing to ally with a party, and an owlbear's new nest nearby that the goblins cannot clear. A track joins the camps; a parley hollow sits between. Joins the trail and the river crossing."
  target Location.type Lair=4 Route=1 Landmark=2 Hidden=1
}

region D rating=WILD die=d8 locations=6 {
  ground scrub "scrub above a river gorge, a stone bridge below"
  place B east "5-7 miles"
  outline "The River Crossing: an old outpost on an overlook with a hidden cache of supplies and the first sight of Drakenhold and the dragon's ruin; below it an ancient stone bridge with a guard booth at each end, the far one held by hobgoblins who take a toll or rob; a rough road, once a paved highway, climbs to the Outer City. Joins the trail, the goblin camps and the Outer City."
  target Location.type Landmark=2 Ruin=1 Hidden=1 Lair=1 Route=1
  procedure "Paying or fighting the toll at the far booth."
}

region E rating=WILD die=d8 locations=30 {
  ground scrub "three wide hills of broken ground below the peaks, the Ironwood to the west and south"
  place D east "1-2 miles"
  outline "The Outer City: three hills of streets, a town square, barracks, a guard wall and abandoned homes with the small marks of those who lived in them - wolves at night, kobolds scavenging, decaying buildings that fall. The hold's great doors, cracked open with the left one fallen, stand at the head of the square. Thirty keyed highlights, not every building. Joins the river crossing, the Skybridge and the Trade Hall."
  target Location.type Ruin=16 Landmark=6 Lair=4 Hidden=2 Secret=1 Route=1
  procedure "Searching a ruined house."
}

// ---- Peak 1: the Trade Peak --------------------------------------------------

region FA rating=DANGEROUS die=d10 locations=40 {
  outline "Peak 1, main level - the Trade Hall: three hundred feet of hall hung with faded tapestries, its stone doors cracked open and the left one fallen; signs of battle and a stillness; kitchens and supporting rooms that fed the hold; servants' passages deep within that link all three peaks, and receiving and transport rooms for the guilds' staff; a ramp circling down to the granaries and up into the peak. The Processional of the Living runs to the Judgement Hall. No single route: hallways branch into clusters. Joins the Outer City, the Granaries, the Workshop and the Judgement Hall, and by the servants' passages the Celebration Hall."
  target Location.type High=7 Medium=20 Low=13
  target Reward.contents Keys=8 Lore=8
  procedure "Speaking a dwarven name at a ward."
}

region FB rating=WILD die=d8 locations=18 {   // WILD: the referee moves it to SAFE or DANGEROUS with what a party does here
  outline "Peak 1, under level - the Granaries: the kobold tribe's home. Granaries and water tanks round a central receiving room, a chimney that once drew gas from the deep earth to the forge, meandering storerooms. Lizardmen watch the tribe. Joins the Trade Hall and, by the chimney, the Lost Caverns."
  target Location.type Lair=4 Ruin=8 Landmark=3 Natural=1 Route=1 Hidden=1
}

region FC rating=DANGEROUS die=d10 locations=20 {
  outline "Peak 1, level 2 - the Workshop: the administrative rooms that directed and measured the flow of goods, and the high-end work areas where the hold's craftsmen worked. Joins the Trade Hall and the Forge."
  target Location.type High=3 Medium=10 Low=7
  target Reward.contents Keys=4 Lore=4
}

region FD rating=DANGEROUS die=d10 locations=22 {
  outline "Peak 1, level 3 - the Forge: automatons, the Forge Master's residence, training halls and student dorms. The forge runs on vents from the deep earth, and lifts carry loads between its floors. Joins the Workshop, the Guildmaster Manse and the Lost Caverns."
  target Location.type High=4 Medium=11 Low=7
  target Reward.contents Keys=4 Lore=4
  procedure "Riding the forge lifts."
}

region FE rating=DANGEROUS die=d8 locations=20 {
  outline "Peak 1, level 4 - the Guildmaster Manse: four large open rooms, each ringed by a close branching of small chambers and quarters. Joins the Forge and the Skybridge."
  target Location.type High=4 Medium=10 Low=6
  target Reward.contents Keys=5 Lore=3
}

// ---- Peak 2: the Peak of Judgement ------------------------------------------

region GA rating=DANGEROUS die=d10 locations=24 {
  outline "Peak 2, main level - the Judgement Hall: a hundred-foot circle where seven stone chairs face a carved stone table; Living Statues hold the room. A gathering area round a black obelisk is where the Processional of the Living, from the Trade Hall, and the Processional of the Dead, from the Celebration Hall, meet before the hall. On the far side the corridor splits three ways: ramps up and down, and servants' halls of administrative quarters. Joins the Trade Hall, the Celebration Hall, the Prison and the Throne of the King."
  target Location.type High=4 Medium=12 Low=8
  target Reward.contents Keys=5 Lore=5
  procedure "Speaking a dwarven name at the stone chairs."
}

region GB rating=DANGEROUS die=d10 locations=28 {
  outline "Peak 2, under level - the Prison and Barracks: housing and training for the militia on one half and cells for malcontents on the other. A sandy arena with stone benches anchors the barracks, with administration, armoury and planning rooms round it, and soldiers' quarters further out. The prison is branching corridors of tight cells, and hidden beyond them the more dangerous. The last loyalists fell in the Armory. Joins the Judgement Hall and the Lost Caverns."
  target Location.type High=5 Medium=14 Low=9
  target Reward.contents Keys=6 Lore=4
  procedure "Fighting in the barracks arena."
}

region GC rating=DANGEROUS die=d8 locations=18 {
  outline "Peak 2, level 2 - the Throne of the King: defiled, burned and broken. Administrative chambers hold clues to the Breaking. The throne room opens on a large balcony with views of the dwarven kingdom. Joins the Judgement Hall and the Treasure Vaults."
  target Location.type High=3 Medium=9 Low=6
  target Reward.contents Keys=4 Lore=6
}

region GD rating=DANGEROUS die=d8 locations=14 {
  outline "Peak 2, level 3 - the Treasure Vaults: claimed by the dragon, his hoard now lies here, and kobolds bring treasure up as tribute under lizardmen's eyes. The main vault is sundered; others hold, sealed by powerful magic. Joins the Throne of the King and the King's Holding."
  target Location.type High=3 Medium=7 Low=4
  target Reward.contents Hoards=4 Keys=3 "Unique Treasures"=1
}

region GE rating=DANGEROUS die=d4 locations=10 {
  outline "Peak 2, level 4 - the King's Holding: ruin and destruction, Vermakith's lair, where he sleeps. A stately corridor with the King's retinue at one end and the Queen's at the other, with servants' quarters, sitting rooms and private places off it; the King's chambers are destroyed and a crater opens the holding to the sky. Joins the Treasure Vaults and the Skybridge."
  target Location.type High=2 Medium=5 Low=3
  target Reward.contents Hoards=1 Lore=3
}

// ---- Peak 3: the Runemasters' Peak ------------------------------------------

region HA rating=DANGEROUS die=d8 locations=22 {
  outline "Peak 3, main level - the Celebration Hall: a two-hundred-foot oval, much like the Judgement Hall, with fewer signs of the Breaking's fighting than of luxury gone to rot - furniture and tapestry among the debris. The Processional of the Dead leaves from one side to the Judgement Hall; on the other the way splits three ways, up, down and into the servants' halls, kitchens and room-servants' quarters. Joins the Judgement Hall, the Crypts and the Chapel, and by the servants' passages the Trade Hall."
  target Location.type High=4 Medium=11 Low=7
  target Reward.contents Keys=4 Lore=4
}

region HB rating=DANGEROUS die=d6 locations=20 {
  outline "Peak 3, under level - the Crypts: undead and haunted spirits, and trapped secrets hiding the wealth of the ancestors, among them the tomb of an earlier Knight of Drakenhold, a title the people grant, and the lance in it. Joins the Celebration Hall and the Lost Caverns."
  target Location.type High=3 Medium=10 Low=7
  target Reward.contents "Unique Treasures"=2 Lore=3 Keys=3
}

region HC rating=DANGEROUS die=d8 locations=14 {
  outline "Peak 3, level 2 - the Chapel of the Runemasters: now the kobold chieftain's, who left his tribe, lured by whispers from the Sanctuary above. Joins the Celebration Hall and the Temple of Stone."
  target Location.type High=2 Medium=7 Low=5
  target Reward.contents Lore=3 Keys=2
}

region HD rating=DANGEROUS die=d6 locations=16 {
  outline "Peak 3, level 3 - the Temple of Stone: ordained paths that guard the Runemasters' secrets and punish the unfaithful. A receiving room opens on a circular route of trials; at its centre, the secret rooms where the leaders set the trials and watched. Joins the Chapel and the Sanctuary."
  target Location.type High=3 Medium=8 Low=5
  target Reward.contents Keys=4 Lore=4
  procedure "Walking the trials."
}

region HE rating=DANGEROUS die=d4 locations=12 {
  outline "Peak 3, level 4 - the Runemaster Sanctuary: corrupted by the harrowing, the evil let loose when the artifact was used, haunted, and untouched by the dragon. A Test of Sanity is called for here. The artifact lies here, and what it opens a way to. Joins the Temple of Stone and the Skybridge."
  target Location.type High=3 Medium=6 Low=3
  target Reward.contents Lore=4 "Magical Tomes"=1 Keys=2
}

// ---- Above and below ----------------------------------------------------------

region I rating=WILD die=d6 locations=8 {
  ground rock "bare rock and sheer faces between the three peaks"
  place E east "0.5-1 miles"
  outline "The Skybridge: spans joining the three peaks' fourth levels, trails to watchtowers and defensive points in varied repair, and a way into the King's Holding by its crater. A party that reaches it skips the halls below. Joins the Outer City, the Guildmaster Manse, the King's Holding and the Sanctuary."
  target Location.type Route=2 Landmark=3 Ruin=2 Hidden=1
}

region J rating=DANGEROUS die=d8 locations=24 {
  outline "The Lost Caverns: secret pathways and subterranean places, ancient inhabitants, hidden uses by the dwarven lords, mined gems and metals, and an evil that comes up toward the hold. Ancient and Minor Wyrms lurk in the heated depths. A Test of Sanity is called for here. Joins the Granaries by the gas chimney, the Forge by its vents, the Prison and the Crypts."
  target Location.type High=4 Medium=12 Low=8
  target Reward.contents Hoards=2 "Unique Treasures"=1 Keys=3 Lore=3
}
```

## Notes

Not read by any step; delete when the block is adopted.

### Region codes

The write-up's codes stand. A code is one or two letters, ascending; a first letter holds one
region (`A`) or a group (`FA`-`FE`). So the first letter is the part: F is Peak 1, G Peak 2,
H Peak 3, and the surface, the Skybridge and the Lost Caverns are single letters. Twenty-two
regions, about 390 locations, four times Thornmarch's 94; the surface is 70 of them. Dice are
per type, so a SAFE die is the settlement's size, a WILD die is the ground, rolled every four
hours, and a DANGEROUS die is the hostility, rolled each move or ten minutes; nothing in the
write-up's dice is out of line.

### Framework changes made

- **Codes `AA`-`ZZ`**, sorted within the first letter (`tools/tables.py`,
  `patterns/Region_Schema.md`). The validator's "plain A-Z progression" is now "ascending, and
  a first letter is a region or a group, not both".
- **`Lift` and `Chute`** as Connection types (`patterns/Dangerous_Schema.md`), drawn without a
  door.
- **`translation`** as a Lore value (`patterns/Setting_Schema.md`) and a `Language` lever
  `clues=N`, measured against the Lore that teaches the script.
- **`architecture`** (SAFE) and **`construction`** (DANGEROUS) lines in `setting`, passed to
  each region's slice and read by `templates/region/Region.md`. Conditions are still written
  per region; they now start from the line and state only what the level changes.

Not made: an alarm crossing regions (the referee rules it), a lock with several keys (a
chain of locks does it), registration between level maps.

### Write-up inconsistencies, settled

- **The Knight** is a title the people grant, and also a person: the lance is in an earlier
  Knight's tomb in the Crypts, and the young Knight held the title by acclaim.
- **Wyrms.** Vermakith is from the north and no kin of the cavern Wyrms; the Ancient Wyrm is
  its own older line, and a Minor Wyrm is a weaker subtype of it.
- **Processionals.** The Living joins the Trade Hall to the Judgement Hall; the Dead joins the
  Celebration Hall to it; both meet at the obelisk, then enter the hall.
- **The doors** at the head of the Outer City's square are the Trade Hall's.
- **The harrowing** is the evil let loose when the artifact was used, and the intrusions that
  followed; the Breaking is the King's death and the war. The term stays.
- **The dragon sleeps**, in the King's Holding, and has for ten years. What wakes him is a
  Rung.
- **Homes.** Lizardmen in the Granaries, the Vaults and the Holding; hobgoblins at the bridge
  and in the Outer City; survivors in the servants' passages of the Trade, Judgement and
  Celebration Halls; the witch's hut on the Trail.
- **The artifact** is in the Sanctuary; the Lost Caverns' evil is what it opens a way to.
- **Bestiary shapes.** Vermakith is a Named Creature; types are singular (`Beast`, `Wyrm`,
  `Fantasy`); the Automaton's MA 1 is omitted; Hobgoblin and Lizard Man are added; the Ooze
  is a Horror; the two chieftains and the Living Statue share 3d6+1, so their Specials
  differ.
- **Six factions, nine truths, thirteen events**, as written. Thornhaven's natives and
  transients are its People, the witch a Named Creature, and the dead, the Runemasters'
  spirits and the sprites Bestiary creatures.

### GENRE.md

GENRE.md is fixed and not edited here. This setting answers six of its ten differently:
Reference (a lost hold, not a fortified outpost); Magic level (dwarven earth-magic is
everywhere in the hold, scarce outside it); Authority (none past Thornhaven); Population
density (one village, then a ruin); Decay (high: the realm that held it is gone); and Player
characters (a dwarf's kin are among the survivors). A Drakenhold build starts by writing
those answers.

### Proposed development

**Build order.** Writing twenty-two regions at once is the cost, so build a vertical slice
first: the setting files (steps 2a-2g), the surface A-E and I, then one route through the
hold - the Trade Hall (FA), the Judgement Hall (GA) and the King's Holding (GE) - with every
registry each touches. That is the loop 4a-4d on a path that includes a lock, its rod, the
sleeping dragon and the first graffiti name. The remaining levels follow, a peak at a time.

**The key economy.** Decide it before any room is written, as a table: about ten rods
(master, Steward, Guildmaster, Runemaster, Royal, vault-specific), eight tiles, twelve names,
each with where it is found, what it opens, and which is behind which. A lock has one key,
so the highest security is a chain: the rod that opens the vault door lies behind another
lock. A rod behind its own lock is the validator's one hard error; a chain of three is the
dungeon's spine.

**The dragon.** Vermakith is a Named Creature asleep in the Holding, with his hoard in the
Vaults below and the Skybridge a way round. Two Rungs: what wakes him (a hoard taken, a
name spoken in the Holding) and what he does next (hunts the Outer City, burns
Thornhaven). The lance is the one `solution`; a party that never finds it can still carry a
hoard out past a sleeping dragon.

**Named Creatures first.** Vermakith, the kobold chieftain at the Chapel, the goblin chief,
the witch, the Steward's and the Guard Leader's wraiths, the Forge Master's last automaton,
and the voice in the caverns. Each is a place for a hook to land.

**Thornhaven as the pressure's face.** The haunted basement, the witch's feud and the
native-transient split are three quests that never enter the hold; keep them cheap and
specific so the surface earns the climb. The river factor is what makes the road worth
reopening.

**Language before names.** Dwarvish needs roots for forge, vault, throne, crypt, rod, tile,
oath, king, knight, servant, and the thirty or so names the wraiths, graffiti and survivors
will use, and four Lore entries (`clues=4`) that teach the script. Write them at 1b, since a
name found in a room must already be coined.

**The Granaries.** `FB` is WILD with rooms in it. It is a good test of the referee's
promotion: if play makes it a lair worth clearing, rewrite it as DANGEROUS; if a party
befriends the kobolds, as SAFE.
