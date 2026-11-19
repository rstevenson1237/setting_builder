# Challenges of HC The God's Sanctum

```kdl
Encounter HC.2 doing="chanting at the altar in robes" reaction="Hostile" answers="1 turn" far="chanting below" { Creature bestiary="Snake Man" count="3-6" }
Mystery HC.2 type="Altar" effect="Whispers the names of the sacrificed" test="Sanity" damage="Nuisance" { Secret trigger="touching the altar's stain" tell="warm, wet stone" }
Encounter HC.3 doing="chained in the niches" reaction="Fearful" want="rescue" know="who is taken next" { Creature bestiary="Tribesman" count="4-10" }
Hazard HC.5 type="Runes" damage="Nuisance" test="Sanity" { Secret trigger="opening the stone box" tell="runes ringing the lid" knows="the priests" }
Encounter HC.6 doing="asleep on its heap of bones" reaction="Neutral" far="breathing through rock" { NamedCreature named="Zuuthtuuz" presence="100%" }
Hazard HC.6 type="Broken/Weak Floor" damage="Damaging" test="Constitution" wound="Crushing" { Secret trigger="walking the bone heap" tell="shifting bones, hollow rattle" }
Mystery HC.7 type="Throne" effect="Lifting the crown stirs the god" test="Sanity" damage="Lethal" { Secret trigger="lifting the crown" tell="warm bones, soft rattle" }
Hazard HC.8 type="Pit" damage="Lethal" test="Constitution" wound="Crushing" { Secret trigger="stepping past the rim" tell="chains hanging into dark" }
```
