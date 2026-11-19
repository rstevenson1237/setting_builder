# Challenges of HB The Pyramid's Halls

```kdl
Encounter HB.2 doing="turning the cranks in shifts" reaction="Hostile" answers="2 turns" far="gears grinding below" { Creature bestiary="Tribesman" count=4 }
Encounter HB.3 doing="drawing lots by the lamp" reaction="Hostile" answers="1 turn" far="spear-butts on stone" { Faction faction="Tuuzesh" present=6 members="two snake men and four bound men" }
Encounter HB.4 doing="coiled in the vault above the hall" reaction="Hostile" far="sloughed skin on floor" { Creature bestiary="Giant Python" count=1 }
Encounter HB.5 doing="crowded in the pens, chained" reaction="Fearful" want="rescue, or a quick death" know="who was taken from where" { Creature bestiary="Tribesman" count=8 }
Encounter HB.5 doing="keeping the pens with whips" reaction="Hostile" answers="1 turn" { Faction faction="Tuuzesh" present=3 members="bound men with whips and keys" }
Encounter HB.7 doing="resting in bunks, armed" reaction="Hostile" answers="1 turn" far="snoring and a hiss" { Faction faction="Tuuzesh" present=8 members="six bound men and two snake men" }
Encounter HB.8 doing="coiled in warm nest-beds" reaction="Hostile" answers="1 turn" far="long hiss in dark" { Creature bestiary="Snake Man" count=4 }
Hazard HB.8 type="Gas" damage="Damaging" test="Constitution" wound="Poison" { Secret trigger="disturbing the nest-beds" tell="sour musk, thick air" knows="the snake people" }
Encounter HB.9 doing="coiled among the coin chests" reaction="Hostile" far="dry rustle in coin" { Creature bestiary="Giant Centipede" count=4 }
Hazard HB.9 type="Spike" damage="Lethal" test="Constitution" wound="Piercing" { Secret trigger="lifting a chest lid" tell="bronze points under rim" knows="the treasurer" }
Encounter HB.11 doing="reading at the lectern" reaction="Wary" answers="1 turn" want="a captive for the Sleeper" know="the sanctum's every way" { NamedCreature named="Thazsheek" presence="60%" { Purchase type="sale" item="a vial of the sleeper's venom" price="300 cn" per="a vial" limit="three vials" } }
Hazard HB.12 type="Hammer" damage="Nuisance" test="Constitution" wound="Crushing" { Secret trigger="lifting a racked spear" tell="oiled chain behind rack" }
Encounter HB.13 doing="watching the stair under the brazier" reaction="Hostile" answers="1 turn" far="hissing on the stair" { Creature bestiary="Snake Man" count=2 }
```
