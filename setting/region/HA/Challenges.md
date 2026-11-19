# Challenges of HA The Pyramid's Upper Temple

```kdl
Encounter HA.2 doing="carrying a captive up the stair" reaction="Hostile" answers="2 turns" want="the captive at the shrine" know="when the next patrol climbs" far="drums and chanting above" { Faction faction="Tuuzesh" present=4 members="bound men, one snake man leading" }
Mystery HA.4 type="Flooring" effect="Any tread rings the great bell" { Secret trigger="stepping on a flagstone" tell="worn, polished flagstones" knows="the guards" }
Encounter HA.5 doing="chanting over the channel" reaction="Hostile" answers="2 turns" far="chanting on the wind" { Creature bestiary="Tribesman" count=6 }
Encounter HA.6 doing="drawing lots by the brazier" reaction="Hostile" answers="1 turn" far="spear-butts on stone" { Faction faction="Tuuzesh" present=6 members="two snake men and four bound men" }
Encounter HA.8 doing="feeding the altar's flames" reaction="Hostile" answers="1 turn" want="the fire fed" know="the day of the next sacrifice" far="roaring fire, a hiss" { Creature bestiary="Snake Man" count=3 }
Mystery HA.8 type="Altar" effect="Flames answer a spoken name with visions" test="Sanity" damage="Damaging" { Secret trigger="naming someone over flames" tell="flames lean toward speaker" }
Hazard HA.9 type="Dart" damage="Lethal" test="Constitution" wound="Poison" { Secret trigger="opening the robe chest" tell="pinprick hole in lid" knows="the priests" }
Encounter HA.10 doing="working the winch ropes" reaction="Hostile" answers="2 turns" want="no one near the shaft" far="rope creaking" { Creature bestiary="Tribesman" count=4 }
Hazard HA.10 type="Ravine/Climb" damage="Lethal" test="Constitution" wound="Crushing" { Secret trigger="stepping to the edge" tell="cold updraught from rim" }
```
