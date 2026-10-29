# Challenges of K Ghulvod

```kdl
Encounter K.2 doing="crouch in the wailing dark" reaction="Hostile" far="faint wailing" { Creature bestiary="Ghoul" count="3-6" }
Hazard K.3 type="Field" damage="Damaging" test="Sanity" { Secret trigger="breathe deep" tell="flames gutter" knows="the cult" }
Encounter K.3 doing="stand at the walls" reaction="Hostile" { Creature bestiary="Gargoyle" count="1-2" }
Encounter K.4 doing="tighten their masks" reaction="Hostile" answers="1 turn" { Faction faction="Voxkroth" present=4 members="masked cultists" }
Mystery K.5 type="Mirror" effect="the demon's hall shows in the glass" { Secret trigger="look into it" tell="glass glowing dimly" knows="the cult" }
```
