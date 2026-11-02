# Connections of K Pyramid Level 9 - The Antechamber

```kdl
Connection K.1 to="K.2" type="Open" { Encounter doing="stand in a king's robe" reaction="Hostile" want="no steel drawn" { Creature bestiary="Wraith" count=1 } }
Connection K.1 to="J.6" type="Open" climb=20
Connection K.2 to="K.1" type="Open"
Connection K.2 to="K.3" type="Archway"
Connection K.2 to="K.4" type="Open"
Connection K.3 to="K.2" type="Archway"
Connection K.3 to="K.5" type="Iron"
Connection K.3 to="K.4" type="Stone"
Connection K.4 to="K.2" type="Open"
Connection K.4 to="K.3" type="Stone"
Connection K.5 to="K.3" type="Iron"
Connection K.5 to="L.1" type="Open" climb=-30
Connection K.2 to="K.6" type="Open"
Connection K.6 to="K.2" type="Open"
Connection K.6 to="K.8" type="Archway"
Connection K.8 to="K.6" type="Archway"
Connection K.8 to="K.3" type="Archway"
Connection K.3 to="K.8" type="Archway"
Connection K.4 to="K.7" type="Wooden" { Hazard type="Gas" damage="Nuisance" test="Fate" condition="Poisoned" { Secret trigger="open the door" tell="sweet smoke under it" knows="the cult" } }
Connection K.7 to="K.4" type="Wooden"
```
