# Challenges of C Goblin Cave

```kdl
Encounter C.1 doing="watching the passage from a side niche" reaction="Hostile; shout warning, fight from the niche" want="to warn the warren" { Creature bestiary="Goblin" count=2 }
Encounter C.3 doing="sleeping in heaps, a few awake gambling" reaction="Hostile; wake and swarm intruders" { Creature bestiary="Goblin" count=10 }
Hazard C.4 type="Broken/Weak Floor" damage=Nuisance { Secret trigger="step on crusted refuse" tell="flies over one patch" }
Encounter C.6 doing="feasting around the fire" reaction="Hostile; fight to the chief's death" want="to hold the chest" { Faction faction="The Zhakuk" present=6 members="the chief and five guards" }
```
