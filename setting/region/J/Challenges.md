# Challenges of J Pyramid Level 8 - The Lieutenants' Halls

```kdl
Encounter J.2 doing="sit the throne" reaction="Hostile" answers="1 turn" { NamedCreature named="Krulox" presence="100%" }
Encounter J.3 doing="lie on the couch" reaction="Wary" want="the demon's favour" { NamedCreature named="Xothox" presence="100%" }
Encounter J.4 doing="drum and drill" reaction="Hostile" answers="1 turn" { NamedCreature named="Zhurjul" presence="100%" }
Encounter J.5 doing="sit the empty chairs" reaction="Hostile" { Creature bestiary="Mummy" count="1-2" }
Encounter J.6 doing="hover before the gate" reaction="Hostile" { Creature bestiary="Wraith" count="1-2" }
Hazard J.7 type="Pit" damage="Damaging" test="Constitution" wound="Crushing" { Secret trigger="weight, centre plate" tell="rings worn smooth" knows="the lieutenants" fact="the rings sink toward the middle" }
Encounter J.9 doing="spar and keep the halls" reaction="Hostile" answers="1 turn" { Creature bestiary="Cultist" count="4-6" }
```
