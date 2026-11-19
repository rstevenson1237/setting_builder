# Brief

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
step that writes what it names. The `test` line's `walks` is how many times step 5e walks it. A `target` is measured by `tools/metrics.py`; a `rate` is
how many entries each location of a type holds in a table file; `words` is how long each
field of a region's brief runs, or each item of a list field and each row of a table.
An `architecture` or `construction` line in `setting` is how its SAFE or DANGEROUS regions are
built, so a region states only where it differs.

The maps are asked for here. `setting` holds a `sheet` per terrain map: its name, `square`
(a distance), `extent` (`"W by H unit"`), `regions`, the codes it holds, and optionally `ground`,
the terrain it is wherever no region's ground reaches, or `land=island`, one generated island in a sea,
its land shared among its regions; a DANGEROUS region is on none.
A region on a sheet may hold one `ground` line, a terrain its area must have, optionally a `height`
its area stands at (a distance or `"N-M unit"` above the sea), then prose the writing reads and the solver does not, and `place` lines: another region on a sheet
with it, a compass direction, and a distance or `"N-M unit"` from that region's way in.
`origin` names the master map, the sheet whose centre at the sea is (0,0,0), x east, y north, z up, in
feet; without one, the regions state their places from a point of their own. A WILD region's `height`
is also the elevation its locations keep to. `maps` holds one `look` line
per map kind, how every map of that kind is drawn; a key a line leaves out keeps today's drawing.

A `design` line in a region asks for its blocks to be designed before their tables are written (step 3e); a
DANGEROUS region's always are. It holds `fill`, the share of a block's ground its rooms cover; `pad`, the ground
kept clear round each room; and `footprint`, the block's ground round its centre - a distance for a square, or
`"rect W L"`, `"circle R"` or `"poly x,y x,y ..."` in feet - that a settlement is laid out on and a level's drawing comes
as near as a readable layout allows.

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
  Factions count=7 marks=2                          // marks: identity marks each shows
  Quests count=7
  History events=4
  Truths count=5
  Language affixes="3-5" roots="15-20"               // per tongue
  Procedures wounds="Piercing Crushing Poison Fire Exposure Suffocation" madness=6 exchange="3%" resale="20%" {   // a Wound table per Wound_Type listed; madness: 6 for a d6 Madness table, 0 for none
    weather "1 storm, no boat puts out and travel inland is halved; 2 and 3 rain; 4 to 6 hot and still"
    carousing "1 and 2 against the carouser; 3 and 4 nothing; 5 and 6 for them"
  }
}

safe {
  rate Inn Dressing=1 Purchases="2-4" People="2-3" Rewards=0
  rate Merchant Dressing=1 Purchases="2-4" People="1-2" Rewards=0
  rate Bank Market Dressing=1 Purchases="1-3" People="1-2" Rewards=0
  rate Authority Dressing=1 Purchases="0-2" People="1-3" Garrison="0-1" Rewards=0
  rate Temple Dressing=1 Purchases="0-1" People="1-2" Rewards=0
  rate Gate Dressing=1 Purchases="0-1" People="1-2" Rewards=0
  rate Secret Dressing=1 Purchases="0-1" People="0-1" Rewards=0 Challenges=0
  words Overview=120 View=90 Approach=90 Law=70 Arrival=50 Plan=90 Places=35 Tables=25
}

wild {
  rate Lair Dressing=1 Challenges=1 Rewards=0 Purchases=0
  rate Ruin Natural Hidden Secret Dressing=1 Challenges="0-1" Rewards=0 Purchases=0
  rate Route Dressing=1 Challenges="0-1" Stops="3-6" Rewards=0 Purchases=0
  words Overview=120 Approach=80 Terrain=110 Ways=120 Landmarks=40 Places=40 Tables=25
}

dangerous {
  rate High Purpose=1 Dressing=1 Challenges="1-2" Rewards="1-2"
  rate Medium Dressing=1 Challenges=1 Rewards="0-1"
  rate Low Dressing=1 Rewards="0-1"
  words Overview=100 Approach=70 Entrances=60 Prizes=50 Places=35 Tables=25
  target Location.type High="17%" Medium="50%" Low="33%"
  target Hazard.damage Nuisance="40%" Damaging="40%" Lethal="20%"
  target Reward.contents Keys="10%" Lore="15%"
}

maps {
  look dungeon hatch=none rock=solid wall=1.5 numbers=plain doors=bar rock-color="#a9824c" floor="#f6ecd6" ink="#3a2a18" grid="#c9b48c" wall-color="#3a2a18"
  look settlement theme=color
  look terrain theme=color
}

// -- This setting --------------------------------------------------------------

setting {
  origin Island
  sheet Island square="1 miles" extent="24 by 54 miles" regions="A B C D E F G" land=island
  test walks=3 "A jungle island in play, not in text, built fresh by the framework and transcribed from nothing: a party lands at the southern villages behind their great wall with a ship that will not wait forever and a partial map marking the serpent crown, trades for a guide, and crosses swamp, coast and hills to the northern villages and back, past cave men, dinosaurs, lizard men at war, mer people in the wrecks and pirates on the same hunt, across forbidden ground to a stepped pyramid where a cult of snake people, with bound men in both peoples' villages, is waking its god. Every procedure kind and registry the framework has is used at least once, and every location type the island has a place for."
  outline "A large island of jungle-covered hills ringed by reef. Two networks of tribal villages hold its coasts, one on the south shore and one on the north, and neither crosses the hills between. The centre is hill jungle where cave men hunt and dinosaurs graze and kill. Lizard men hold the southern swamps and are at war with the southern villages; mer people hold the sea caves and the wrecks on the western reef. In the eastern jungle a stepped pyramid stands over the trees, held by the last of the snake people and the cult of the god they serve. Small and medium lairs of beasts and humanoids are scattered through every wild region, and pirates and treasure hunters land wherever they please."
  pressure "The party's ship lies off the southern villages and sails home on a day set at landing, with or without them. The southern villages are losing the swamp war: each raid takes captives, and the lizard men sell them on to the pyramid. The snake people are feeding their god to wake it, buying captives from the lizard men and the pirates alike, and each sacrifice makes the pyramid's cult bolder. A pirate crew and a rival band of treasure hunters are on the island after the same gold, and either will take a party's map, boat or life for it. Those the cult takes and does not kill come home bound: they look and speak as before, wear a scale-mark hidden on the skin, and do what the snake people ask; some already sit in the chiefs' councils, north and south. Behind their wall the southern villages are safe from the island, and each night something huge comes to the wall's gate and is fed."
  history "The snake people raised the stepped pyramid and ruled the island from it, with the lizard men for soldiers and the tribes for labour and sacrifice."
  history "The tribes rose and burned the snake people's towns; the snake people withdrew into the pyramid and dwindled, and the lizard men went back to the swamps they had been set to hold."
  history "The victors split over the spoils into a northern people and a southern one, and the hill jungle between them was left to the beasts and the cave men."
  history "Ships began to break on the western reef; the mer people took the wrecks for their own, and pirates and treasure hunters followed the tales of the gold the reef and the pyramid hold."
  truth "The northern and southern villages speak one tongue and keep one story of the rising, and each blames the other for what was lost after it; each will trade with strangers, and neither will carry a stranger's word to the other."
  truth "The lizard men's war is over an egg-stone of their god the southern villages took in the rising and keep in their chief's house: returned, it ends the raids, and the southern chiefs will not give it up."
  truth "The mer people keep what the reef takes and trade only for what the sea cannot give them, iron and fire-worked things, and they want the pirates' anchorage gone from their water."
  truth "The eastern jungle is forbidden ground to both peoples since the rising: no guide will cross into it, a villager who does is cast out, and a party known to have gone there loses its standing in the villages that learn of it."
  truth "The snake people's god is a living thing asleep under the pyramid, and each sacrifice brings it nearer waking; it is the end of the pyramid, not a thing a party can bargain with."
  procedures "Hazards are Tests of Constitution and Fate. Overland travel is by the day through jungle, swamp and hill, with an encounter check each watch; a party without a guide loses its way on a failed Test. Disease from the swamps and the jungle water is a Fate Test with a lasting Condition. Poison is Lethal at least once, in a hazard or a creature's Special. Boats are hired at the villages and the anchorage, and the reef wrecks any that crosses it without someone who knows the passages."
  tongue "the common tongue of the party, spoken by the pirates and the treasure hunters and by a few traders in each village"
  tongue "the speech of the island tribes, north and south, the same tongue with two accents and two words for each other"
  tongue "the hissing speech of the snake people, carved on the pyramid and spoken by the lizard men as an old soldiers' tongue"
  tongue "the speech of the mer people, sung under water and spoken in air only as a broken trade-talk"
  bestiary Caveman "Lizard Man" Merman "Snake Man" Pirate Tyrannosaurus Triceratops Pterodactyl "Giant Crab" "Giant Leech" Crocodile "Giant Python" "Giant Centipede"   // up front; the rest added as a location needs them
  bestiary-note "Men are the rank and file a faction fields, never one entry per human occupation. Dinosaurs are beasts, met as a hazard to avoid as often as a fight. No two factions' creatures share both an AD and a Special."
  faction "the southern villages: the larger tribe, stockaded on the south shore, at war with the lizard men and the party's first hosts"
  faction "the northern villages: the smaller tribe, fishers and hill hunters on the north shore, who trade with no one from the south"
  faction "the lizard men: enclaves in the southern swamps, the snake people's old soldiers, raiding the southern villages for the egg-stone and for captives"
  faction "the mer people: the sea caves and the wrecks of the western reef, keepers of the reef's treasure"
  faction "the snake people's cult: the last snake people and the men they have bound, in the stepped pyramid and hidden in both peoples' villages, feeding their god"
  faction "the pirates: one crew at an anchorage on the western coast, trading captives to the pyramid and hunting the reef's gold"
  faction "the treasure hunters: a rival expedition from the party's own homeland, after the pyramid's gold with a map of their own"
  relations "The southern and northern villages hold each other at Antipathy. The southern villages and the lizard men hold each other at Hatred. Both villages hold the cult at Hatred (fear)."
  relations "The cult holds the lizard men and the pirates Tolerated, as suppliers, and every other faction at Hatred. The lizard men hold the cult Neutral. The mer people hold the pirates at Hatred and the villages Neutral."
  relations "The pirates and the treasure hunters hold each other at Antipathy. Every pair not named is Neutral."
  rumours "Twelve, each pointing at a place or person: one at each faction, the pyramid, the god beneath it, the egg-stone, the reef's wrecks, and the cave men's hills. At least one is true and sounds false, and each P names which faction or place is wrong."
  quest "the serpent crown, the snake emperors' crown of gold coiled round a green stone the size of a fist, marked on the party's partial map and kept in the god's sanctum"
  quest "captives taken in the last swamp raid, sought by the southern villages, who pay in guides and canoes"
  quest "a lost northern hunting party, last seen in the hill jungle, given at the northern villages"
  quest "the egg-stone, carried back to the lizard men to end the war, wanted by a southern elder who will not say so to the chiefs"
  quest "the pirates' anchorage driven from the western coast, asked by the mer people for a wreck's treasure"
  quest "a treasure hunter who deserted with half their map, sought by the treasure hunters' leader"
  quest "proof of what the cult feeds its god, wanted by the northern villages before they will send a war party"
}

region A rating=SAFE die=d6 locations=12 {
  ground grass height="100-200 feet" "gardens, palm groves and cleared ground on the south shore, a lagoon behind a reef, stockades of sharpened logs"
  place D south "18-24 miles"
  outline "The southern villages: three stockaded villages on the south shore of a peninsula, cut off from the rest of the island by a great wall of stone and logs across its neck, built by their ancestors after the rising, with one great gate. The villages are joined by a shore path and canoes on the lagoon. The largest holds the chiefs' house, where the egg-stone is kept, and the beach where strangers' boats land and the party's ship lies at anchor. Guides, canoes, food and a guest house are had here for trade. The lizard men raid by water round the wall's ends, and the war is felt in burned huts and the watch on the lagoon; at the gate the villages leave food each night for the huge thing that comes to it."
  design footprint="600 feet"
  target Location.type Gate="1+"
  procedure "Hiring a guide and canoes."
  procedure "Passing the wall's gate, opened by the chiefs' word."
}

region B rating=WILD die=d8 locations=9 {
  ground marsh "mangrove and reed swamp, black channels, hummocks and drowned trees"
  place A north-east "6-9 miles"
  outline "The southern swamps: the lizard men's enclaves on hummocks in the mangroves, the war's ground between them and the southern villages, and the channels the raiding parties use. Small lairs of leeches, crocodiles and worse sit between the enclaves."
  target Location.type Lair="3+" Natural="2+"
}

region C rating=WILD die=d8 locations=10 {
  ground sand height="0-200 feet" "beaches, sea cliffs and caves, and the western reef awash with broken hulls"
  place D south-west "7-10 miles"
  outline "The wreck coast: the western shore and its reef, where the mer people hold sea caves and the wrecks of a dozen ships, the pirates keep an anchorage in a cove, and the treasure hunters have a beach camp. The way into the drowned galleon is here."
  target Location.type Lair="2+" Ruin="3+"
  procedure "Diving the wrecks and the sea caves."
}

region D rating=WILD die=d10 locations=12 {
  ground forest height="400-2000 feet" "jungle-covered hills, ridges and ravines, grassy clearings where the dinosaurs graze"
  outline "The hill jungle: the island's centre, where cave men hunt from caves in the ridges and dinosaurs graze the clearings and hunt the trails. No village claims it; a party crossing between the shores crosses it. Small and medium lairs of fantastic beasts and humanoids are scattered through it, and the way into the troglodytes' warren is here."
  target Location.type Lair="4+" Natural="2+"
}

region E rating=WILD die=d8 locations=9 {
  ground forest "low jungle under a closed canopy, vine-choked ruins of the snake people's towns, a slow brown river"
  place D east "5-8 miles"
  outline "The eastern jungle: forbidden ground, the overgrown towns of the snake people's empire around the stepped pyramid, which stands over the canopy and is seen from the hills. Boundary posts carved with serpents mark its edge, where guides turn back. Cult patrols and bound men walk its roads, and small lairs fill the ruins. The way into the pyramid is here."
  target Location.type Ruin="3+" Lair="2+"
}

region F rating=SAFE die=d6 locations=10 {
  ground grass height="100-200 feet" "fishing beaches, terraced gardens and stilt-houses at a river mouth on the north shore"
  place D north "14-18 miles"
  outline "The northern villages: two villages at a river mouth and a hunters' camp up the river, smaller and warier than the south. Fish, hill guides and word of the hill jungle are had here, at a higher price for anyone who has come from the south."
  design footprint="500 feet"
}

region G rating=WILD die=d6 locations=8 {
  ground scrub "windward headlands of scrub and grass above cliffs, the rim of an old volcanic crater"
  place F south-west "6-9 miles"
  outline "The northern headlands: the island's windward corner, with a crater rim, sea-bird cliffs and the treasure hunters' second landing. Small lairs of flying beasts and a humanoid band's camp hold the high ground."
  target Location.type Lair="2+" Landmark="2+"
}

region HA rating=DANGEROUS die=d10 locations=10 {
  outline "The stepped pyramid, its upper temple: the terraces, the stair and the shrine on top, held by the cult's bound men and the first of the snake people. Its way in opens from the eastern jungle, and a shaft and a stair lead down."
  design fill="25-45%" footprint="140 feet"
  target Location.type High=2 Medium=5 Low=3
  target Reward.contents Lore=1
}

region HB rating=DANGEROUS die=d8 locations=14 {
  outline "The stepped pyramid, the cult's halls: the snake people's living halls, the captives' pens and the cult's treasury, inside the pyramid's body."
  design fill="25-45%" footprint="180 feet"
  target Location.type High=3 Medium=7 Low=4
  target Reward.contents Hoards=1 Keys=1 Lore=1
}

region HC rating=DANGEROUS die=d6 locations=8 {
  outline "The stepped pyramid, the god's sanctum: the sacrifice hall and the cavern below the pyramid where the god sleeps, and the serpent crown on the last emperor's bones. Its god is a Named Creature, and the crown its Unique Treasure."
  design fill="25-45%" pad="0 feet" footprint="140 feet"
  target Location.type High=3 Medium=3 Low=2
  target Reward.contents "Unique Treasures"=1 "Magical Tomes"=1
}

region I rating=DANGEROUS die=d6 locations=7 {
  outline "The drowned galleon: a medium lair, a great ship sunk across a reef gap off the wreck coast, its hold half in air, held by the mer people and a sea beast they keep, with the reef's best treasure aboard."
  design fill="35-55%" footprint="rect 50 140"
  target Location.type High=2 Medium=3 Low=2
  target Reward.contents Hoards=1
}

region J rating=DANGEROUS die=d6 locations=8 {
  outline "The troglodytes' warren: a medium lair in a sinkhole in the hill jungle, caves held by a troglodyte band that raids cave men and travellers alike."
  design fill="35-55%" footprint="120 feet"
  target Location.type High=2 Medium=4 Low=2
}
```
