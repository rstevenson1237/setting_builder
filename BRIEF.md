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

A `pack` line is how a DANGEROUS block's rooms are packed into a square: `fill`, the share of
the square they cover, from the least the validator holds to the most the packer starts from;
`passages`, the share of its ways run as passages rather than doors through a shared wall;
and, in a region, `footprint`, the square's side.

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
  Factions count=5 marks=2                          // marks: identity marks each shows
  Quests count=5
  History events=4
  Truths count=4
  Language affixes="3-5" roots="15-20"               // per tongue
  Procedures wounds="Piercing Crushing Poison Fire" madness=6   // a Wound table per Wound_Type listed; madness: 6 for a d6 Madness table, 0 for none
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
  target Reward.contents Keys="10%" Lore="15%"
  pack fill="30-45%" passages="35%"
}

// -- This setting --------------------------------------------------------------

setting {
  sheet Sands square="25 yards" extent="1200 by 1200 yards" regions="A"
  sheet Lake square="20 yards" extent="1000 by 1000 yards" regions="B"
  test "The Lost City in play, not in text, built fresh by the framework and transcribed from nothing: a party caught in a sandstorm takes cover in a buried ruin, survives its first days on what it can find, and goes down through a pyramid that gets larger for five levels, passes factions to bargain with, and reaches a lake city of dreamers, then goes deeper still, narrowing, toward the thing that corrupted a people. Every location type, procedure kind and registry the framework has is used at least once."
  outline "A lost city under the dunes and, beneath it, a pyramid ten levels deep: a sandstorm drives the party into the ruins, where the pyramid's tip stands from the sand ringed by three wind-swept statues. Level 1 is one trapped room whose clues open ways down. Levels 1 to 5 widen, from a puzzle room to a history, a hall of factions, living quarters and a funerary level; from level 5 a path opens to a lake city of masked dreamers. Levels 6 to 10 narrow again toward a demon below."
  pressure "Food, water and shelter run short from the first night. Nothing outside the ruins is known to the party and nothing from outside will come for it; nothing in the ruins or under them is safe. A party can build a place of respite among the ruins or win one from a faction, and either costs what it will not spend elsewhere. The three branches of the cynidiceans each mean to break the demon's hold and will not work together, and the demon's cult is looking for the keys the lost king hid."
  history "The cynidiceans raised a city of the sands, and a pyramid at its centre to house the dead of their line."
  history "A demon was invited into the royal line, and its priests corrupted the court, the clergy and the soldiers in turn."
  history "The last king and queen were interred at level 5, with a false tomb beside them to mislead the demon's servants."
  history "The living took the stair down to the lake city to live out their lives in dreams and masks, and the city above was left to the sand."
  truth "Every way down the pyramid is opened by something done in the room above: which way a party takes depends on what it solves, breaks or leaves alone."
  truth "The three branches of the cynidiceans share one aim, to break the demon's hold and restore their people, and each holds that it alone has the strength and foresight to do it; none will work with the others, and each offers membership to a party that serves it."
  truth "The lake city's people have no shared leadership and are no faction: they chose the fungus, the masks and the dream, and will not be rescued."
  truth "The demon below is the cause of the corruption and a thing still being fed: it is the end of the descent, not a mistake that can be undone."
  procedures "Hazards are Tests of Constitution and Fate, and a Test of Sanity at the lake city's psychosis-inducing fungi and wherever the demon's corruption reaches, from level 6 down. Food, water and shelter are tracked from the first day, and a party that has none loses Wounds to thirst and exposure. Poison is Lethal at least once, in a hazard or a creature's Special."
  tongue "the common tongue of the party, spoken by the cynidiceans only in a broken form"
  tongue "the speech of the cynidiceans, living and carved into every wall of the pyramid"
  tongue "the black speech of the demon's cult and its servants"
  bestiary Skeleton Zombie Mummy Ghoul Gargoyle "Giant Scorpion" "Giant Centipede" "Giant Spider" "Giant Rat" Stirge Hyena Soldier Wraith   // up front; the rest added as a location needs them
  bestiary-note "Men are the rank and file a faction fields, never one entry per human occupation. No two factions' creatures share both an AD and a Special."
  faction "the Royal Guard: the cynidiceans' former soldiers and their heirs, who hold that strength of arms will free their people"
  faction "the Priesthood: the former female-led clergy, who hold that faith and the old rites will free their people"
  faction "the Scholars: the learned and the practitioners of dark magic who first found the demon, who hold that knowledge of it will free their people"
  faction "the demon's cult: priests below level 6 who feed the thing and seek the lost king's keys"
  faction "the tomb robbers: outsiders who moved into the upper levels and trade what they take"
  relations "The Royal Guard, the Priesthood and the Scholars each hold the other two at Antipathy, and the cult at Hatred (fear)."
  relations "The cult holds the three branches at Hatred and the tomb robbers Tolerated."
  relations "The tomb robbers hold the cult Hatred (fear) and the three branches Neutral. Every pair not named is Neutral."
  rumours "Twelve, each pointing at a place or person: one at each faction, the buried city, the pyramid's tip, the lake city, the funerary level, the false tomb, the demon, and the storm. At least one is true and sounds false, and each P names which faction or number is wrong."
  quest "water for a party's first camp, sought by a branch that will trade a guide for it"
  quest "a tomb robber's stolen relic, given at their camp"
  quest "the Royal Guard's missing captain, last seen on level 4"
  quest "a mask-seller's request to find a kinsman who walked into the lake"
  quest "proof of what feeds the demon, wanted by the Scholars"
}

region A rating=WILD die=d6 locations=9 {
  ground sand "dunes, drifted streets and rooftops half-buried in sand, a storm wall overhead"
  outline "The lost city: a sand-buried ruin with the pyramid's tip standing from its centre, three wind-swept statues carved on top. A party's first shelter is here - a roofed house, a cistern, a collapsed market, a barracks wall, a temple colonnade, a dry canal - and the first tomb robbers' scouts working the rubble. It holds the first food and water a party can find, and the only ground where a party can build its own place of respite. One way in to the pyramid, the tip's door at the foot of the statues."
  target Location.type Landmark=7 Ruin=6 Lair=1 Hidden=1 Route=1
  procedure "Foraging for food and water among the ruins."
  procedure "Making shelter and a place of respite."
}

region B rating=WILD die=d8 locations=10 {
  ground rock "a cavern floor of rock and fungus gardens, with a still lake at the city's heart, a ceiling lit by glowing growths"
  outline "The subterranean city: a cavern built round a still lake, where the cynidiceans' descendants live in a waking dream - masked as animals, feasting, reveling and eating the fungus they grow. A party reaches it by a path from level 5. Quarters, a market of drugs, the fungus gardens, a lake shore and a revel house make a city; the way back up the path and the stair down to level 6 are the party's two exits."
  target Location.type Landmark=7 Ruin=1 Natural=2 Lair=4 Hidden=1 Secret=1 Route=1
  procedure "Trading for the fungus and its drugs."
  procedure "Joining the revels."
}

region C rating=DANGEROUS die=d12 locations=4 {
  outline "Pyramid level 1: a single room laden with puzzles, traps and clues to the pyramid's story. Depending on how a party proceeds, one or more ways to the lower levels open: a trapped floor, a mural stair, a statue's plinth. The room is the pyramid's first lesson."
  pack footprint="120 feet"
  target Location.type High=1 Medium=2 Low=1
  target Reward.contents Keys=1 Lore=1
}

region D rating=DANGEROUS die=d10 locations=6 {
  outline "Pyramid level 2: the history of the cynidiceans told in murals, carvings and the rooms between them, in a series of trap rooms and encounters to test a party, with chances to meet the tomb robbers who have moved in and scouts of the three branches below."
  pack footprint="140 feet"
  target Location.type High=1 Medium=3 Low=2
  target Reward.contents Lore=2
}

region E rating=DANGEROUS die=d10 locations=9 {
  outline "Pyramid level 3: a rotating room with eight exits, each chosen by the rune a party selects. The three branches of the cynidiceans - the Royal Guard, the Priesthood and the Scholars - each hold a base here, and each can be explored. By a party's actions one may offer an alliance or membership."
  pack footprint="170 feet"
  target Location.type High=2 Medium=5 Low=2
  target Reward.contents Keys=1 Lore=1
  procedure "Joining a faction."
}

region F rating=DANGEROUS die=d8 locations=13 {
  outline "Pyramid level 4: the former living quarters, with strange cynidicean encounters, lairs of stronger monsters that came down from the sand, hints of the evil below, and the tomb robbers' deepest camp."
  pack footprint="200 feet"
  target Location.type High=3 Medium=6 Low=4
  target Reward.contents Hoards=1 Lore=2
}

region G rating=DANGEROUS die=d8 locations=19 {
  outline "Pyramid level 5: the funerary level, with the last king and queen interred, a false tomb beside them, and the areas of the former clergy. The largest level. From here a path can be opened to the subterranean city."
  pack footprint="250 feet"
  target Location.type High=4 Medium=10 Low=5
  target Reward.contents Hoards=1 Keys=2 "Unique Treasures"=1 Lore=2
}

region H rating=DANGEROUS die=d6 locations=13 {
  outline "Pyramid level 6: the first level of the descent, laid out in the shape of level 4 and given to the demon's cult and its sacrifices. The way up is behind a party."
  pack footprint="200 feet"
  target Location.type High=3 Medium=6 Low=4
  target Reward.contents Hoards=1 Lore=1
}

region I rating=DANGEROUS die=d6 locations=9 {
  outline "Pyramid level 7: a smaller level of altars and cells where the cult's chosen are made and unmade."
  pack footprint="170 feet"
  target Location.type High=2 Medium=5 Low=2
  target Reward.contents Keys=1 Lore=1
}

region J rating=DANGEROUS die=d6 locations=6 {
  outline "Pyramid level 8: the lieutenants' halls, a short level of powerful servants who keep the way down."
  pack footprint="160 feet"
  target Location.type High=2 Medium=3 Low=1
  target Reward.contents Hoards=1 Keys=1 "Unique Treasures"=1
}

region K rating=DANGEROUS die=d4 locations=5 {
  outline "Pyramid level 9: the antechamber of the demon, where the corruption is thick enough to cost Sanity."
  pack footprint="140 feet"
  target Location.type High=2 Medium=2 Low=1
  target Reward.contents Lore=1
}

region L rating=DANGEROUS die=d4 locations=4 {
  outline "Pyramid level 10: the demon's chamber, a single hall where the corrupting entity feeds, and the end of the descent. Its demon is a Named Creature."
  pack footprint="140 feet"
  target Location.type High=2 Medium=1 Low=1
  target Reward.contents "Unique Treasures"=1 "Magical Tomes"=1
}
```
