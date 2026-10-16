# Brief

This build's design requests: every count, mix and rate it is built to, and what this one
setting should hold. Templates and schemas set none of their own.
It never overrides a schema's rules or `STYLE.md`.

- `files`, `safe`, `wild` and `dangerous` hold the framework's levers at reasonable
  defaults. Change a value to customise it.
- `setting` holds this setting's outline and what it asks of the setting files.
- `region` holds one region each, in gazetteer order: its rating, die, location count and
  outline, and any target of its own.

A share is `"N%"`; a count is `N`, or a range `"N-M"`. A quoted line is prose, read by the
step that writes what it names. A `target` is measured by `tools/metrics.py`; a `rate` is
how many entries each location of a type holds in a table file.

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
  Quests count=5
  History events=4
  Truths count=4
  Language affixes="3-5" roots="15-20"               // per tongue
  Procedures wounds="Piercing Crushing Poison Fire" madness=6   // a Wound table per Wound_Type listed; madness: 6 for a d6 Madness table, 0 for none
}

safe {
  rate Inn Dressing=1 Purchases="2-4" People="2-3" Procedures="0-1"
  rate Merchant Dressing=1 Purchases="2-4" People="1-2" Procedures="0-1"
  rate Bank Market Dressing=1 Purchases="1-3" People="1-2" Procedures="0-1"
  rate Authority Dressing=1 Purchases="0-2" People="1-3" Garrison="0-1"
  rate Gate Dressing=1 Purchases="0-1" People="1-2"
  rate Secret Dressing=1 Purchases="0-1" People="0-1"
}

wild {
  rate Lair Dressing=1 Challenges=1
  rate Ruin Natural Route Hidden Secret Dressing=1 Challenges="0-1" Procedures="0-1"
}

dangerous {
  rate High Purpose=1 Dressing=1 Challenges="1-2" Rewards="1-2" Procedures="0-1"
  rate Medium Dressing=1 Challenges=1 Rewards="0-1" Procedures="0-1"
  rate Low Dressing=1 Rewards="0-1"
  target Location.type High="17%" Medium="50%" Low="33%"
  target Hazard.damage Nuisance="40%" Damaging="40%" Lethal="20%"
  target Reward.contents Keys="10%" Lore="15%"
}

// -- This setting --------------------------------------------------------------

setting {
  test "Keep on the Borderlands in play, not in text, built fresh by the framework and transcribed from nothing: a party outfits at a safe keep, walks half a day to a ravine of lairs, picks which to try, retreats to heal and sell, and comes back. The lairs hate one another and can be played against one another, and all of them pay a shrine at the ravine's head. Every location type, procedure kind and registry the framework has is used at least once."
  outline "One frontier, crossed in a day: a keep at the end of the road from the realm; between it and the hills a wood, a mere and the road itself; in the hills a ravine whose walls hold six tribes' lairs and a maze, and above the maze a shrine."
  pressure "Chaos is gathering in the ravine. Tribes that fought one another for years now pay the shrine's priests, and the road is where the keep first feels it: wagons lost, patrols back short. Nobody at the keep knows how many raiders there are or who commands them. The priests have two agents inside the keep."
  history "The ravine's makers cut halls, a first shrine, and passages joining what are now separate caves, long ago."
  history "The makers were gone, and their works empty, before any tribe came."
  history "The keep was raised thirty years ago at the end of the realm's road."
  history "Five years ago priests of Chaos reopened the first shrine, and the tribes began to pay it."
  truth "The tribes distrust one another more than they fear the keep; a party can pay, ally with or provoke one against another."
  truth "The makers' passages join caves each tribe believes are separate, and each tribe knows only its own end."
  truth "Every tribe pays the shrine a tithe of what it raids, and a tithe unpaid is collected by the bugbears."
  truth "Chaos is inside the walls: the shrine has agents at the keep, and the keep's own people do not know it."
  procedures "Hazards are Tests of Constitution and Fate, and a Test of Sanity only at the shrine. Poison is Lethal at least once, in a hazard or a creature's Special."
  tongue "the common tongue of the keep and the realm - Law's"
  tongue "the cant of the road, the mere and the wood, spoken by outlaws, lizard-folk and anyone who looks after themselves - Neutrality's"
  tongue "the black speech of the tribes and the shrine's priests - Chaos's"
  tongue "the dead tongue of the ravine's makers, met only carved into its walls"
  bestiary Kobold Goblin Orc Hobgoblin Gnoll Bugbear Owlbear Wolf Soldier "Lizard Man" Zombie   // up front; the rest added as a location needs them
  bestiary-note "Men are the rank and file a faction fields, never one entry per human occupation. No two tribes' creatures share both an AD and a Special."
  faction "the keep: its commander, its garrison and chapel, and the realm's claim they stand for"
  faction "the carters' guild: the wagon crews and traders who run the road and pay for it to stay open"
  faction "the outlaws of the wood: poachers and deserters who prey on the road's stragglers and sell to anyone"
  faction "the lizard-folk of the mere, who hold the causeway and want strangers out of the reeds"
  faction "the kobolds of the first cave: many, poor, cowardly, tribute-payers to the goblins"
  faction "the goblin tribe above them: sly, numerous, at war with the orcs"
  faction "the orc tribe: brutish, quarrelsome, at war with the goblins"
  faction "the hobgoblin tribe: drilled and armoured, at war with the gnolls, holder of a key to the shrine"
  faction "the gnoll tribe: raiders and slavers who sell to any buyer, at war with the hobgoblins"
  faction "the bugbears of the dry fork: few, silent, the shrine's paid enforcers"
  faction "the shrine's cult: priests, acolytes and the dead they keep, with two agents in the keep"
  relations "Goblins and orcs hold each other at Hatred; so do hobgoblins and gnolls."
  relations "The kobolds hold the goblins at Hatred (fear); the goblins hold the kobolds Neutral."
  relations "Every tribe holds the cult at Hatred (fear) and the cult holds every tribe Tolerated; the bugbears and the cult hold each other Friendly."
  relations "The keep holds every tribe and the lizard-folk at Antipathy, the cult and the outlaws at Hatred, and the carters Friendly; the carters hold the keep Friendly and the outlaws Hatred."
  relations "The outlaws hold the gnolls Tolerated, the lizard-folk Antipathy and the keep Hatred (fear). Every pair not named is Neutral."
  rumours "Twelve, each pointing at a place or person: one at each tribe, the shrine, the maze, the keep's own people, and the wood, the mere and the road. At least one is true and sounds false, and each P names which tribe or number is wrong."
  quest "a bounty on the raiders hitting the wagons, posted by the carters' guild"
  quest "a carter's lost wagon and its strongbox, given at the market"
  quest "the chapel's stolen reliquary, given at the chapel"
  quest "a party of adventurers gone into the ravine, sought by a kinsman at the tavern"
  quest "proof that something commands the tribes, wanted by the commander and given at his hall"
}

region A rating=SAFE die=d8 locations=13 people=18 {
  outline "The keep: a hold at the road's end - the main gate on the road and a postern toward the wood, an inn and a tavern, a trader and a smith, a moneychanger, a market in the outer yard, the chapel of Law, the commander's hall and the barracks, and two places kept hidden: the cellar where the cult's two agents meet, and the commander's sally tunnel. A party outfits, hires and sells here, and hears the rumours."
  target Location.type Gate=2 Inn=2 Merchant=2 Bank=1 Market=1 Authority=3 Secret=2
  target Garrison of=Authority "67%"
  procedure "A game of chance at the tavern."
  procedure "Hiring men-at-arms and torchbearers at the market."
  procedure "Selling what a party carries home, at the moneychanger."
}

region B rating=WILD die=d8 locations=5 {
  outline "The wagon road: the realm's road to the keep gate, open country where the fortnightly wagon is the only safe company - a toll post, a ford, the milestone where the last wagons were lost, a roadside shrine of Law. It leaves the map toward the realm, and meets the mere's causeway and the wood path."
  target Location.type Landmark=4 Route=1
  procedure "Travelling with the fortnightly wagon."
}

region C rating=WILD die=d6 locations=7 {
  outline "The Dark Wood: forest between the keep and the ravine; the forest trail from the postern to the ravine's mouth is three watches' walk. In it: the outlaws' camp, a hermit's clearing, a watchtower older than the keep, a ring of standing stones, and the outlaws' hidden cache."
  target Location.type Landmark=5 Route=1 Hidden=1
  procedure "Forage and hunt in the wood."
}

region D rating=WILD die=d6 locations=5 {
  outline "The Black Mere: marsh beside the road, crossed by a causeway the lizard-folk allow and a pole-boat route they do not. In it: the lizard-folk's stilt village, a drowned shrine of the makers, a sinking flat, and a dry island hidden in the reeds. It joins the road and the wood."
  target Location.type Landmark=3 Route=1 Hidden=1
  procedure "Crossing by causeway or pole boat."
}

region E rating=WILD die=d6 locations=12 {
  outline "The ravine: a stream cut through the hills, entered from the wood and climbing to its head. West wall from the mouth up: the kobold, goblin and orc caves. East wall from the mouth up: the hobgoblin and gnoll caves, then a dry fork holding the bugbear den. At the head: the maze in the cliff's foot and the stair up to the shrine. An owlbear's lair is on the east rim. Each mouth is a ledge a tribe watches. Goblins and orcs are neighbours and enemies; so are hobgoblins and gnolls."
  target Location.type Landmark=9 Route=1 Hidden=1 Secret=1
  procedure "Watching the cave mouths from the rim."
}

region F rating=DANGEROUS die=d8 locations=5 {
  outline "The kobold warren: a single holding, the first mouth a party meets, on the west wall. Many small kobolds, cowardly and trap-wise, who pay tribute to the goblins above them and fear the rest. Dart and pit traps guard the way in; the chief is cunning, not strong, and a Named Creature."
  target Location.type High=1 Medium=2 Low=2
  target Reward.contents Hoards=1
}

region G rating=DANGEROUS die=d6 locations=6 {
  outline "The goblin hold: a single holding above the kobolds on the west wall. Sly, numerous and well stocked, with wolves kept and the kobolds' tribute taken. Enemies of the orcs beside them, to whose warren a makers' passage joins its stores. Its boss is a Named Creature."
  target Location.type High=1 Medium=3 Low=2
  target Reward.contents Hoards=1 Lore=1
}

region H rating=DANGEROUS die=d6 locations=6 {
  outline "The orc warren: a single holding at the head of the west wall - a guard cave, pens, a feast hall, the chief's cave. Brutish, quarrelsome and many, drunk by evening. Enemies of the goblins, joined to their stores by the makers' passage. Its chief is a Named Creature."
  target Location.type High=1 Medium=3 Low=2
  target Reward.contents Hoards=1
}

region I rating=DANGEROUS die=d6 locations=6 {
  outline "The hobgoblin hold: a single holding on the east wall, fortified - a drilled gate-guard, barracks, armoury, the warlord's hall. Armoured, disciplined and few. Enemies of the gnolls beside them, joined to their den by a makers' passage. They pay the shrine in goods and hold one key to it. Its warlord is a Named Creature."
  target Location.type High=1 Medium=3 Low=2
  target Reward.contents Hoards=1 Keys=1
}

region J rating=DANGEROUS die=d6 locations=5 {
  outline "The gnoll den: a single holding above the hobgoblins on the east wall. Raiders and slavers who sell to any buyer and keep captives, some of them hirelings or kin of a party's. Enemies of the hobgoblins. They hold the key to the maze. Its pack-leader is a Named Creature."
  target Location.type High=1 Medium=2 Low=2
  target Reward.contents Hoards=1 Keys=1 Lore=1
}

region K rating=DANGEROUS die=d4 locations=5 {
  outline "The bugbear den: a single holding in the dry fork. Few, silent, strong ambushers paid by the shrine to keep the fork and collect the tithe, with a back stair up to the shrine. Its leader is a Named Creature."
  target Location.type High=1 Medium=2 Low=2
  target Reward.contents Hoards=1 Lore=1
}

region L rating=DANGEROUS die=d4 locations=5 {
  outline "The minotaur's maze: a single holding at the ravine head - makers' passages kept by one minotaur, a Named Creature, and what it has collected. The way up to the shrine runs out of its far end. Finding the way is the danger. It holds one key to the shrine and is itself barred by a lock."
  target Location.type High=1 Medium=2 Low=2
  target Reward.contents Keys=1 Lore=1
  procedure "Finding the way through the maze."
}

region M rating=DANGEROUS die=d4 locations=14 {
  outline "The shrine of Chaos: a collection, worked rock above the maze, in four blocks - the stair-hall and outer shrine; the priests' cells and refectory; the crypts, where the dead do not stay; the sanctum and the vault. Three ways in: the stair from the ravine head, the passage from the maze, the bugbears' back stair. Its high priest is a Named Creature; acolytes, guards and the dead hold the blocks. Locks bar the sanctum and the vault, and their keys lie in the hobgoblin hold and the maze. A Test of Sanity is called for here and nowhere else."
  target Location.type High=3 Medium=7 Low=4
  target Reward.contents Hoards=1 "Unique Treasures"=2 "Magical Tomes"=1 Lore=2
}
```
