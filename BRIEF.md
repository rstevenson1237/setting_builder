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
  Magic rolls=6
  Rumours die=6 T=2 P=2 F=1 U=1
  Bestiary specials-from=4                           // AD below which a Special is rare
  Factions count=2 marks=2                           // marks: identity marks each shows
  Quests count=1
  History events=0
  Truths count=0
  Language affixes="3-5" roots="15-20"               // per tongue
}

safe {
  rate Inn Merchant Bank Market Dressing=1 Purchases="1-3" People="1-2"
  rate Authority Dressing=1 Purchases="0-2" People="1-2"
}

wild {
  rate Lair Dressing=1 Challenges=1
  rate Ruin Natural Route Hidden Secret Dressing=1 Challenges="0-1"
}

dangerous {
  rate High Purpose=1 Dressing=1 Challenges="1-2" Rewards="1-2"
  rate Medium Dressing=1 Challenges=1 Rewards="0-1"
  rate Low Dressing=1 Rewards="0-1"
  target Location.type High="17%" Medium="50%" Low="33%"
  target Reward.contents Keys="20%" Lore="20%"
}

// -- This setting --------------------------------------------------------------

setting {
  test "The thinnest setting that runs every step once - a keep, the ravine beyond it, and one cave - whose shape a reader recognises as Keep on the Borderlands, built fresh by the framework, not transcribed from the module."
  outline "One frontier, crossed on foot in half a day: a keep at the end of the road from the realm, a ravine beyond it, and one cave opening off the ravine."
  pressure "A goblin tribe in the cave raiding the road, not an invasion or a war. Nobody at the keep knows how many goblins there are."
  history "Shallow: what the land held before matters through what the cave's earlier makers left behind."
  procedures "B/X's own shape: hit points and saving throws stand behind every Test, and there is no madness track - Wounds and Madness covers wounds only."
  tongue "the common tongue of the keep and the realm"
  tongue "the goblins' tongue"
  tongue "the dead tongue of the cave's makers, met only carved into its walls"
  bestiary Goblin Wolf Soldier                         // up front; the rest added as a location needs them
  bestiary-note "Men are the rank and file a faction fields, never one entry per human occupation."
  faction "the keep: its commander, its garrison, and the realm's claim they stand for"
  faction "the goblin tribe of the cave, out for what the road carries"
  rumours "At least one points at the cave, and one is true and sounds false."
  quest "given at the keep"
}

region A rating=SAFE die=d8 locations=4 people=4 {
  outline "The keep: a hold at the road's end - its gate, an inn, a trader, and the commander's hall."
}

region B rating=WILD die=d8 locations=4 {
  outline "The ravine: the walk from the keep to the cave, along a stream path - the cave mouth is the only way into the cave."
  target Location.type Landmark=3 Route=1
}

region C rating=DANGEROUS die=d4 locations=6 {
  outline "The cave: a single holding - the goblin tribe's home, in workings older than the tribe, with one entrance."
}
```
