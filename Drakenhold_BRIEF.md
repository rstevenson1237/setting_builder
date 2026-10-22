# Brief

Drakenhold, written as a `BRIEF.md`: a candidate to replace the Thornmarch one, not read by any
step until it is copied over. Everything in the block is the framework's grammar; where the
write-up and the framework disagree, the block follows the framework and says what the
write-up had in a `// was` comment. Below the block: the framework features this setting
needs, the inconsistencies in the write-up, and a proposed next development.

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
  Factions count=11 marks=2                          // marks: identity marks each shows
  Quests count=7                                     // was 5: the write-up's hooks need seven
  History events=13                                  // was 4: the write-up dates thirteen
  Truths count=5                                     // was 4: the write-up's nine, sorted (see Notes)
  Language affixes="3-5" roots="15-20"               // per tongue
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
  sheet Hold square="20 yards" extent="1.6 by 1.2 miles" regions="E F"
  sheet Village square="10 feet" extent="200 by 150 yards" regions="A"
  test "Drakenhold in play, not in text: a party outfits at a dwindling river village, walks the Ironwood to a ruined dwarf-hold, and chooses a way in - the broken Trade Hall doors, the Skybridge, a servants' passage - then climbs and descends three peaks of halls where the right rod, tile or spoken name opens what force cannot. A dragon that no party can fight owns the second peak's heart, and the way to ruin it lies in a tomb on the third. Every location type, procedure kind and registry the framework has is used at least once."
  outline "One mountain hold of three peaks, a day from the last village: Thornhaven at the river and the Ironwood's edge; the wood trail, the goblin camps and the river crossing between it and the hold; the ruined Outer City below the peaks; and fifteen levels of halls, vaults, crypts and lost caverns, where runes, rods, tiles and names are the locks and the dwarves' machines are the roads."
  pressure "Something under Drakenhold is waking again. Evil comes up from the lost caverns, the kobolds' tribute to the dragon has not stopped in thirty years, and Thornhaven feels it first: strays gone from the wood's edge, a witch who blames the village, and a rougher class drifting in on a rumour of hoards. Nobody there knows whether Vermakith sleeps, hunts or is dead, and nobody knows where the stolen artifact went."
  history "The hold's founders carved three halls into three peaks and found the caverns under them; it was dwarven work for twelve centuries."
  history "Dragons assaulted the peaks three centuries ago and were beaten with ancient magic, and the Runemasters were given the Third Peak for it."
  history "The Breaking, thirty-two years ago, ended the dwarven kingdom: its king killed, its clans at war, its last loyalists dead in the Armory."
  history "Vermakith came thirty years ago and has not left."
  truth "Nothing in Drakenhold opens to force alone: a portal wants its rod, a receptacle its tile, a secret door its spoken name."
  truth "The runes teach: every ward, trap and puzzle carries a clue to reading the next, and a party that copies them can learn the script."
  truth "The dwarves' machines are the hold's roads, and they work wherever the old earth-magic still holds."
  truth "A name spoken from the dwarven past has power: it opens, wakes, and brings the dead to parley."
  truth "The hold's lowest remember: the survivors in the servants' passages know the hold as it was, and know what the stone says to those who forget."
  procedures "Hazards are Tests of Constitution and Fate, and a Test of Sanity only where the artifact's evil has touched the stone: the Sanctuary and the lost caverns. Poison is Lethal at least once, in a hazard or a creature's Special. Machines deal Crushing and Piercing; runes deal Blast."
  tongue "the common tongue of Thornhaven and the river trade - Law's"
  tongue "the rough cant of the wood and the road, spoken by goblins, hobgoblins, kobolds, transients and anyone who looks after themselves - Neutrality's"
  tongue "the dead tongue of the hold's makers, spoken only by wraiths and survivors and cut in runes across every wall - Law's"
  tongue "the wyrm-speech of the lizardmen and of Vermakith, heard in his servants' mouths - Chaos's"
  bestiary Wolf "Giant Spider" "Wood Sprite" Owlbear Kobold "Kobold Warrior" "Kobold Chieftain" Goblin "Goblin Chieftain" Hobgoblin "Lizard Man" "Dwarven Survivor" Automaton "Living Statue" "Skeletal Warrior" Shadow "Dwarven Wraith" "Ancient Wyrm" Ooze   // up front; the rest added as a location needs them
  bestiary-note "Vermakith is a Named Creature, not a Bestiary entry. Men are the rank and file a faction fields, never one entry per human occupation. No two tribes' creatures share both an AD and a Special; the kobold and goblin chieftains differ in their Special, and the Living Statue is not a chieftain's match."
  faction "Thornhaven's natives: farmers, boatmen and the reeve, longtime residents who want the village kept as it was"
  faction "the transients: the rougher class drifting in on rumours of hoards, prospectors, sell-swords and chancers who want a share"
  faction "the witch of the wood's edge and her wood sprites, who hold the Ironwood's margin against the village's encroachment"
  faction "the goblins of the camps: secretive bandits and scavengers, open to an alliance, under attack from an owlbear"
  faction "the hobgoblin raiders: they hold the bridge's far booth, take tolls, and send parties into the ruin and sometimes against Thornhaven"
  faction "the kobolds of the Granaries: many and cowardly, tribute-payers to the dragon and fearful of the lizardmen, split by a chieftain who left for the Chapel"
  faction "the lizardmen: Vermakith's direct servants, who enforce his will on intruders and kobolds in his name"
  faction "Vermakith, the great red dragon who owns the second peak's vaults and holding, and wants nothing taken from his hoard"
  faction "the dwarven survivors: servants and staff who outlived the Breaking, hiding in the servants' passages, wanting only to be left alone"
  faction "the hold's dead: oath-bound wraiths, the Armory's skeletal warriors and the shades of the crypts, who guard what they died holding"
  faction "the Runemasters' remnant: spirits and the corrupted in the Third Peak's upper levels, who keep the Sanctuary and the artifact's trace"
  relations "Vermakith holds the lizardmen Friendly, the kobolds Tolerated and every other faction Antipathy; the lizardmen hold the kobolds Antipathy, the survivors Hatred and every intruder's side Hatred."
  relations "The kobolds hold Vermakith and the lizardmen Tolerated (fear), the survivors Neutral and everyone else Antipathy; the goblins hold the kobolds Neutral, the hobgoblins Antipathy and the natives Antipathy."
  relations "The hobgoblins hold the natives and the transients Hatred, the goblins Antipathy and the dead Neutral; the natives and the transients hold each other Antipathy; the witch holds the natives Antipathy and the transients Hatred, and they hold her Antipathy."
  relations "The survivors hold the dead Tolerated, Vermakith and the lizardmen Hatred (fear), and the Runemasters' remnant Hatred; the dead hold every living faction Hatred except the survivors Tolerated, and the remnant Antipathy; the remnant holds Vermakith Hatred and the survivors Antipathy. Every pair not named is Neutral."
  rumours "Twelve, each pointing at a place or person: the haunted basement and its relics, the witch, the goblins' offer, the hobgoblin bridge, the silent dragon, the rods, the names, the lance, the survivors, the kobold chieftain's defection, the Skybridge, and the lost caverns. At least one is true and sounds false, and each P names which place, count or person is wrong."
  quest "a reeve's and neighbours' bounty to lay the haunted farmstead's relics to rest, given at Thornhaven"
  quest "the witch's demand: keep the village back from the wood's edge, or find who is taking the strays"
  quest "a factor's offer for proof the northern road is open again, given at the river landing"
  quest "a survivor's plea to carry word to kin in the servants' passages and learn the Knight's name, given by a dwarven PC's kin or a Thornhaven exile"
  quest "the Guildmaster's master rod, wanted by the transients' leader and by the factor"
  quest "the Knight's lance, sought by the survivors and by anyone who has heard Vermakith can be ruined"
  quest "the stolen artifact, found and sealed or destroyed, wanted by a survivor who remembers the Breaking"
}

// ---- The approach ------------------------------------------------------------

region A rating=SAFE die=d8 locations=11 people=14 {   // was d6: a village is not harder than the trail
  ground grass "a river meadow at the Ironwood's western edge, the river landing on the south side and the trail leaving east into the wood"
  outline "Thornhaven: a small river village past its best - a trail gate toward the Ironwood and a landing gate on the river, two inns, one a doss house for transients, two merchants, a factor's counting house at the landing, a market, the reeve's house and the chapel, and one hidden thing: the basement of a farmstead on the edge, over a cemetery that once lay under it. Natives and transients dislike each other; a witch at the wood's edge holds the village to blame. Reached from the realm by river from the south and the western road."
  target Location.type Gate=2 Inn=2 Merchant=2 Bank=1 Market=1 Authority=2 Secret=1
  procedure "Selling what a party carries home, at the factor's counting house."
}

region B rating=WILD die=d8 locations=7 {   // was d10: spiders and bandits make the trail harder than the Wild default
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
  outline "The Outer City: three hills of streets, a town square, barracks, a guard wall and abandoned homes with the small marks of those who lived in them - wolves at night, kobolds scavenging, decaying buildings that fall. The hold's great doors lie broken open at the head of the square. Thirty keyed highlights, not every building. Joins the river crossing, the Skybridge and the Trade Hall."
  target Location.type Ruin=16 Landmark=6 Lair=4 Hidden=2 Secret=1 Route=1
  procedure "Searching a ruined house."
}

region F rating=WILD die=d6 locations=8 {
  ground rock "bare rock and sheer faces between the three peaks"
  place E east "0.5-1 miles"
  outline "The Skybridge: spans joining the three peaks' fourth levels, trails to watchtowers and defensive points in varied repair, and a way into the King's Holding by its crater. A party that reaches it skips the halls below. Joins the Outer City, the Guildmaster Manse, the King's Holding and the Sanctuary."
  target Location.type Route=2 Landmark=3 Ruin=2 Hidden=1
}

// ---- Peak 1: the Trade Peak --------------------------------------------------

region G rating=DANGEROUS die=d10 locations=40 {   // was FA Peak 1 Main Level
  outline "Peak 1, main level - the Trade Hall: three hundred feet of hall hung with faded tapestries, its stone doors cracked open and the left one fallen; signs of battle and a stillness; kitchens and supporting rooms that fed the hold; servants' passages deep within that link all three peaks, and receiving and transport rooms for the guilds' staff; a ramp circling down to the granaries and up into the peak. The Processional of the Living leads off toward the other peaks. No single route: hallways branch into clusters. Joins the Outer City, the Granaries, the Workshop, the Judgement Hall and, by the servants' passages, the Celebration Hall."
  target Location.type High=7 Medium=20 Low=13
  target Reward.contents Keys=8 Lore=8
  procedure "Speaking a dwarven name at a ward."
}

region H rating=DANGEROUS die=d8 locations=18 {   // was FB, rated WILD
  outline "Peak 1, under level - the Granaries: the kobold tribe's home. Granaries and water tanks round a central receiving room, a chimney that once drew gas from the deep earth to the forge, meandering storerooms. Lizardmen watch the tribe. Joins the Trade Hall and, by the chimney, the Lost Caverns."
  target Location.type High=3 Medium=9 Low=6
  target Reward.contents Hoards=2 Lore=3
}

region I rating=DANGEROUS die=d10 locations=20 {   // was FC
  outline "Peak 1, level 2 - the Workshop: the administrative rooms that directed and measured the flow of goods, and the high-end work areas where the hold's craftsmen worked. Joins the Trade Hall and the Forge."
  target Location.type High=3 Medium=10 Low=7
  target Reward.contents Keys=4 Lore=4
}

region J rating=DANGEROUS die=d10 locations=22 {   // was FD
  outline "Peak 1, level 3 - the Forge: automatons, the Forge Master's residence, training halls and student dorms. The forge runs on vents from the deep earth. Joins the Workshop, the Guildmaster Manse and the Lost Caverns."
  target Location.type High=4 Medium=11 Low=7
  target Reward.contents Keys=4 Lore=4
  procedure "Riding the forge lifts."
}

region K rating=DANGEROUS die=d8 locations=20 {   // was FE
  outline "Peak 1, level 4 - the Guildmaster Manse: four large open rooms, each ringed by a close branching of small chambers and quarters. Joins the Forge and the Skybridge."
  target Location.type High=4 Medium=10 Low=6
  target Reward.contents Keys=5 Lore=3
}

// ---- Peak 2: the Peak of Judgement ------------------------------------------

region L rating=DANGEROUS die=d10 locations=24 {   // was GA
  outline "Peak 2, main level - the Judgement Hall: a hundred-foot circle where seven stone chairs face a carved stone table; Living Statues hold the room. A gathering area round a black obelisk marks where the Processional of the Living meets the Processional of the Dead. On the far side the corridor splits three ways: ramps up and down, and servants' halls of administrative quarters. Joins the Trade Hall, the Celebration Hall, the Prison, the Throne of the King and the Crypts."
  target Location.type High=4 Medium=12 Low=8
  target Reward.contents Keys=5 Lore=5
  procedure "Speaking a dwarven name at the stone chairs."
}

region M rating=DANGEROUS die=d10 locations=28 {   // was GB
  outline "Peak 2, under level - the Prison and Barracks: housing and training for the militia on one half and cells for malcontents on the other. A sandy arena with stone benches anchors the barracks, with administration, armoury and planning rooms round it, and soldiers' quarters further out. The prison is branching corridors of tight cells, and hidden beyond them the more dangerous. The last loyalists fell in the Armory. Joins the Judgement Hall and the Lost Caverns."
  target Location.type High=5 Medium=14 Low=9
  target Reward.contents Keys=6 Lore=4
  procedure "Fighting in the barracks arena."
}

region N rating=DANGEROUS die=d8 locations=18 {   // was GC
  outline "Peak 2, level 2 - the Throne of the King: defiled, burned and broken. Administrative chambers hold clues to the Breaking. The throne room opens on a large balcony with views of the dwarven kingdom. Joins the Judgement Hall and the Treasure Vaults."
  target Location.type High=3 Medium=9 Low=6
  target Reward.contents Keys=4 Lore=6
}

region O rating=DANGEROUS die=d8 locations=14 {   // was GD
  outline "Peak 2, level 3 - the Treasure Vaults: claimed by the dragon, his hoard now lies here, and kobolds bring treasure up as tribute under lizardmen's eyes. The main vault is sundered; others hold, sealed by powerful magic. Joins the Throne of the King and the King's Holding."
  target Location.type High=3 Medium=7 Low=4
  target Reward.contents Hoards=4 Keys=3 "Unique Treasures"=1
}

region P rating=DANGEROUS die=d4 locations=10 {   // was GE
  outline "Peak 2, level 4 - the King's Holding: ruin and destruction, Vermakith's lair. A stately corridor with the King's retinue at one end and the Queen's at the other, with servants' quarters, sitting rooms and private places off it; the King's chambers are destroyed and a crater opens the holding to the sky. Joins the Treasure Vaults and the Skybridge."
  target Location.type High=2 Medium=5 Low=3
  target Reward.contents Hoards=1 Lore=3
}

// ---- Peak 3: the Runemasters' Peak ------------------------------------------

region Q rating=DANGEROUS die=d8 locations=22 {   // was HA
  outline "Peak 3, main level - the Celebration Hall: a two-hundred-foot oval, much like the Judgement Hall, with fewer signs of the Breaking's fighting than of luxury gone to rot - furniture and tapestry among the debris. A Processional of the Living on one side; on the other the way splits three ways, up, down and into the servants' halls, kitchens and room-servants' quarters. Joins the Judgement Hall, the Crypts and the Chapel."
  target Location.type High=4 Medium=11 Low=7
  target Reward.contents Keys=4 Lore=4
}

region R rating=DANGEROUS die=d6 locations=20 {   // was HB
  outline "Peak 3, under level - the Crypts: undead and haunted spirits, and trapped secrets hiding the wealth of the ancestors, among them the Knight's tomb and the lance in it. Joins the Celebration Hall, the Judgement Hall by the Processional of the Dead, and the Lost Caverns."
  target Location.type High=3 Medium=10 Low=7
  target Reward.contents "Unique Treasures"=2 Lore=3 Keys=3
}

region S rating=DANGEROUS die=d8 locations=14 {   // was HC
  outline "Peak 3, level 2 - the Chapel of the Runemasters: now the kobold chieftain's, who left his tribe, lured by whispers from the Sanctuary above. Joins the Celebration Hall and the Temple of Stone."
  target Location.type High=2 Medium=7 Low=5
  target Reward.contents Lore=3 Keys=2
}

region T rating=DANGEROUS die=d6 locations=16 {   // was HD
  outline "Peak 3, level 3 - the Temple of Stone: ordained paths that guard the Runemasters' secrets and punish the unfaithful. A receiving room opens on a circular route of trials; at its centre, the secret rooms where the leaders set the trials and watched. Joins the Chapel and the Sanctuary."
  target Location.type High=3 Medium=8 Low=5
  target Reward.contents Keys=4 Lore=4
  procedure "Walking the trials."
}

region U rating=DANGEROUS die=d4 locations=12 {   // was HE
  outline "Peak 3, level 4 - the Runemaster Sanctuary: corrupted by evil let loose when the artifact was used, haunted, and untouched by the dragon. A Test of Sanity is called for here. Joins the Temple of Stone and the Skybridge."
  target Location.type High=3 Medium=6 Low=3
  target Reward.contents Lore=4 "Magical Tomes"=1 Keys=2
}

// ---- Below -------------------------------------------------------------------

region V rating=DANGEROUS die=d6 locations=24 {   // was J Lost Caverns, d8
  outline "The Lost Caverns: secret pathways and subterranean places, ancient inhabitants, hidden uses by the dwarven lords, mined gems and metals, and an evil that comes up toward the hold. Ancient Wyrms lurk in the heated depths. A Test of Sanity is called for here. Joins the Granaries by the gas chimney, the Forge by its vents, the Prison and the Crypts."
  target Location.type High=4 Medium=12 Low=8
  target Reward.contents Hoards=2 "Unique Treasures"=1 Keys=3 Lore=3
}
```

## Notes

Not read by any step; delete when the block is adopted.

### Region codes

The write-up's codes are the block's, remapped to the gazetteer's A-Z progression:

| Write-up | Block | | Write-up | Block |
|---|---|---|---|---|
| A-E | A-E | | GC / GD / GE | N / O / P |
| I Skybridge | F | | HA / HB / HC | Q / R / S |
| FA / FB / FC | G / H / I | | HD / HE | T / U |
| FD / FE | J / K | | J Lost Caverns | V |
| GA / GB | L / M | | | |

Twenty-two regions, about 390 locations, four times Thornmarch's 94. The surface is 70 of them.

### Features the setting needs

The framework can hold the setting as written only with these. In order of how much the
write-up leans on each:

1. **Regions that group.** Fifteen DANGEROUS regions are three peaks of five levels, and the
   site and PDF list them flat. A `Region` member naming its part (`site "Peak 1"`), read by
   both builders, keeps the peaks together. Today the part lives in each outline.
2. **Alarm across regions.** `Encounter.answers` is "how soon it reaches an alarm raised
   elsewhere in its region". With one level a region, a shout in the Trade Hall cannot reach
   the dragon two levels up, and the Alarm view stops at each floor. It needs an alarm that
   names a joined region and a cost per level.
3. **A lock with several keys.** `Lock` holds one `key`. The write-up's highest security
   wants multiple specific rods. `key entry Keys list`, every one required, with the
   validator's "no key behind its own lock" check applied to each. A rod that opens many
   portals already works: `Keys.Opens` is a place list.
4. **Conditions said once.** Every DANGEROUS region writes a `Conditions` node, and fifteen
   levels of dwarven stonework repeat it. A setting-level default, with a region naming only
   what differs, keeps STYLE's "said once".
5. **Vertical registration.** A stair or lift joins a level's room to the next level's room
   at the same plan position, and `draw` renders each block alone. A `stack` request (this
   region sits under that one, offset) lets the drawn maps align and the validator compare a
   Connection's `climb` and bearing from both ends.
6. **Machine Connections.** `Connection_Type` runs Open to Iron. The write-up's lifts, carts
   and chutes want `Lift` and `Chute`, with `climb` for the rise.
7. **Reading the script.** Runes are a mechanic: clues "to assist translation". `Lore_Does`
   has nothing for it. A `translation` value, and a `Language` count (`clues=N`) the
   validator checks against the Lore that carries them, would make decipherment buildable
   instead of narrated.

Not needed: names as keys (`Key_Form word` and `Key_Link tongue` exist), tiles
(`fitting`), rods (`key`), the council and the underclass (History and Factions), and the
dragon as something not to fight (a Named Creature, two Rungs, and a lance that is a
Unique Treasure with `Does solution`).

The fallback with none of these: three regions, one a peak, each a collection with five
Blocks. Alarm, Conditions and stacking work inside a peak, and the grouping falls out. It
loses a die and a brief per level, and puts about a hundred locations in each region.

### Inconsistencies in the write-up

Fixed in the block:

- **Codes** `FA` to `HE` are two letters and break the progression; `FB` is rated WILD
  though its rooms are behind doors, so it is DANGEROUS here.
- **Dice read backwards.** A higher die is easier. Thornhaven d6 sat below the Ironwood
  Trail's d10, and the Lost Caverns, with a demon-touched evil and Ancient Wyrms, sat at d8.
  Now d8, d8 and d6.
- **Bestiary shapes.** `Vermakith` is a proper name, so a Named Creature; types are
  singular (`Beast`, `Wyrm`, `Fantasy`); the Automaton's MA 1 is out of range (omitted at 1);
  Hobgoblin and Lizard Man were missing; the two chieftains and the Living Statue share
  3d6+1; the Ooze is a Horror, not "Fantasy". Specials, ranges and numbers are written at
  step 2d.
- **Counts.** Six factions, nine truths and thirteen events against levers of 11, 4 and 4.
  The nine truths sort to five; the rest are facts: the Council is History, the lance a
  Unique Treasure, the survivors a faction, the tiles and rods Keys.
- **The Council of seven** was stated twice; it is History and the Judgement Hall's
  Dressing.

Open, for you to decide:

1. **The Knight.** A young knight casts off his sword and vanishes 31 years ago; the lance
   is in the "burial tomb of the Knight of Drakenhold". Either the Knight is an office
   (a champion buried in the Crypts, whose lance the young Knight left behind) or the young
   Knight died after the Dragon. Recommended: the office. It also explains the
   unwritten name.
2. **The Dragon and the Wyrms.** Vermakith is "from the north", the Wyrms in the caverns are
   "kin of the same bloodline", and dragons were driven off 311 years ago. Recommended:
   Vermakith is an outsider; the Wyrms are a separate, older line; the 311-year dragons
   were his kind. Rename "Minor Wyrms" (973) and "Ancient Wyrm" to one name.
3. **Processional of the Living.** The Trade Hall says it joins the Celebration Hall; the
   Celebration Hall says it ends outside the Judgement Hall; the Judgement Hall says Living
   and Dead meet at its obelisk. Recommended: Living runs Trade Hall, Judgement Hall,
   Celebration Hall; the Dead runs from the obelisk down to the Crypts. The block's
   outlines say so.
4. **The doors.** The Outer City says the hold's great doors are broken open; the Trade
   Hall says one door has fallen and the doorway is cracked. Recommended: they are the
   same doors, and the Outer City outline points at them.
5. **Breaking and harrowing.** "The harrowing" corrupts the Sanctuary and is not dated.
   Recommended: it is the evil of the 35-year intrusions, before the Breaking, and the
   artifact's use at 40.
6. **Dragon asleep or awake.** Sightings stopped ten years ago, yet kobolds bring tribute
   and lizardmen still serve. Recommended: awake and in the Holding, and not leaving; make
   what wakes him or sends him out a Rung.
7. **Homes.** Lizardmen, hobgoblins (a toll booth only), survivors and the witch had no
   region. Placed: lizardmen in the Granaries, the Vaults and the Holding; hobgoblins at the
   bridge and in the Outer City; survivors in the servants' passages of the Trade Hall,
   Judgement Hall and Celebration Hall; the witch's hut in the Trail.
8. **Where the artifact is.** Stolen at 33 years, never found. Left open: it is the
   framework's open truth. Recommended: the Sanctuary, and the lost caverns' demon is what
   it opens a way to.
9. **Naming.** GENRE answers coined names for the old, and the levels' names are plain
   English. Recommended: plain for the signs a party reads, coined for anything the
   dwarves called their own works (the Processionals, the Sanctuary).

### GENRE.md

GENRE.md is fixed and not edited here. This setting answers six of its ten differently:
Reference (a lost hold, not a fortified outpost); Magic level (dwarven earth-magic is
everywhere in the hold, scarce outside it); Authority (none past Thornhaven); Population
density (one village, then a ruin); Decay (high: the realm that held it is gone); and
Player characters (a dwarf's kin are among the survivors). A Drakenhold build starts by
writing those answers.

### Proposed development

**Build order.** Writing fifteen levels at once is the cost, so build a vertical slice
first: the setting files (steps 2a-2g), the surface A-F, then one route through the hold -
the Trade Hall (G), the Judgement Hall (L) and the King's Holding (P) - with every
registry each touches. That is the loop 4a-4d on a path that includes a lock, its rod, the
dragon and the first graffiti name. The remaining levels follow, a peak at a time.

**The key economy.** Decide it before any room is written, as a table: about ten rods
(master, Steward, Guildmaster, Runemaster, Royal, vault-specific), eight tiles, twelve
names, each with where it is found, what it opens, and which is behind which. A rod
behind its own lock is the validator's one hard error; a chain of three is the dungeon's
spine. The Judgement Hall's stone chairs and the Armory's last stand are the obvious
first locks.

**The Dragon.** Treat Vermakith as a clock the table can read: the Holding is the lair,
the Vaults the hoard, the Skybridge a way round. Two Rungs: what wakes him (a hoard
taken, a name spoken in the Holding) and what he does next (hunts the Outer City,
burns Thornhaven). The lance is the one `solution`; a party that never finds it can
still carry a hoard out past a sleeping dragon.

**Named Creatures first.** Vermakith, the kobold chieftain at the Chapel, the goblin chief,
the witch, the Steward's and the Guard Leader's wraiths, the Forge Master's last
automaton, and the demon's voice in the caverns. Each is a place for a hook to land.

**Thornhaven as the pressure's face.** The haunted basement, the witch's feud and the
native-transient split are three quests that never enter the hold; keep them cheap and
specific so the surface earns the climb. The river factor is what makes the road worth
reopening.

**Language before names.** Dwarvish needs roots for forge, vault, throne, crypt, rod, tile,
oath, king, knight, servant, and the thirty or so names the hold's wraiths, graffiti and
survivors will use. Write them at 1b, since a name found in a room must already be
coined.
