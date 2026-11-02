# Challenges of G Pyramid Level 5 - The Tombs

```kdl
Encounter G.2 doing="stand in the niches" reaction="Hostile" far="linen rustling" { Creature bestiary="Skeleton" count="6-12" }
Encounter G.3 doing="chant before the dais" reaction="Wary" answers="2 turns" want="the stair sealed" know="the rites for the dead" { Faction faction="Ruhiahe" present=6 members="priestesses and acolytes" }
Encounter G.4 doing="shamble between the slabs" reaction="Hostile" { Creature bestiary="Zombie" count="4-8" }
Mystery G.6 type="Statue" effect="the kings' statues turn toward the true tomb" { Secret trigger="touch the first king" tell="floor scuffed in arcs" knows="the Scholars" }
Encounter G.7 doing="lie in the sarcophagus" reaction="Hostile" left="gold leaf flaking" { Creature bestiary="Mummy" count=1 }
Encounter G.8 doing="hover over the queen's bier" reaction="Hostile" { Creature bestiary="Wraith" count=1 }
Hazard G.9 type="Spike" damage="Lethal" test="Constitution" wound="Piercing" { Secret trigger="lift the lid" tell="scratches on the dais" knows="nobody" }
Hazard G.10 type="Dart" damage="Lethal" test="Constitution" wound="Poison" { Secret trigger="open a chest" tell="pinholes in the lids" knows="nobody" }
Hazard G.12 type="Ravine/Climb" damage="Damaging" test="Constitution" wound="Crushing" { Secret trigger="lean over a rim" tell="cracked stone lip" knows="nobody" }
Encounter G.13 doing="watch from their plinths" reaction="Hostile" far="stone cracking" { Creature bestiary="Gargoyle" count="1-2" }
Hazard G.14 type="Water" damage="Nuisance" test="Fate" condition="Exposed" { Secret trigger="step off the path" tell="wet, glowing stone" knows="the dreamers" }
Mystery G.15 type="Altar" effect="the dead stir where blood is spilled" { Secret trigger="spill blood on it" tell="old brown stains" knows="Ruhiahe" }
Encounter G.17 doing="feast among the bones" reaction="Hostile" far="gnawing" { Creature bestiary="Ghoul" count="3-6" }
Encounter G.19 doing="guard the stair" reaction="Hostile" { Creature bestiary="Skeleton" count="3-6" }
Encounter G.20 doing="stand ranked before the doors" reaction="Hostile" answers="1 turn" left="old bronze scale" { Creature bestiary="Skeleton" count="4-8" }
Mystery G.22 type="Altar" effect="daylight fills it; the dead stay out" { Secret trigger="light the sun-bowl" tell="oil channels, sooty bowl" knows="Ruhiahe" }
Mystery G.22 type="Fountain" effect="a drink heals a Wound, once per drinker" { Secret trigger="drink, the bowl lit" tell="dry font, sun carvings" knows="Ruhiahe" }
Hazard G.23 type="Pit" damage="Damaging" test="Constitution" wound="Crushing" { Secret trigger="weight on one half" tell="a central seam" knows="nobody" fact="equal weight on each half holds it" }
Hazard G.26 type="Water" damage="Damaging" test="Constitution" wound="Suffocation" { Secret trigger="lift the bier's lid" tell="tide line, wet drains" knows="nobody" fact="the room floods to the roof" }
Hazard G.28 type="Gas" damage="Nuisance" test="Fate" condition="Blinded" { Secret trigger="take down a mask" tell="powder heaped below" knows="Ruhiahe" }
Encounter G.29 doing="rest on mats before the climb" reaction="Neutral" want="fungus, lamp oil, quiet" know="the side door and the path" { Creature bestiary="Masked Dreamer" count="2-4" }
```
