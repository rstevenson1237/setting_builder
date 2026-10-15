# Connections of C Goblin Cave

```kdl
Connection C.1 to=B.4 type=Open orientation="south, mouth of cleft"
Connection C.1 to=C.2 type=Archway orientation="north end of passage"
Connection C.2 to=C.1 type=Archway orientation="south door"
Connection C.2 to=C.3 type=Crude orientation="west wall, behind pillars"
Connection C.3 to=C.2 type=Crude orientation="east wall, wide gap"
Connection C.2 to=C.5 type=Stone orientation="east wall, flush stone" { Secret trigger="press the central spiral" tell="spiral worn smooth" }
Connection C.5 to=C.2 type=Stone orientation="west wall, flush stone"
Connection C.3 to=C.4 type=Open orientation="south end, low gap"
Connection C.4 to=C.3 type=Open orientation="north end, low gap"
Connection C.3 to=C.6 type=Wooden orientation="north end, plank barricade"
Connection C.6 to=C.3 type=Wooden orientation="south door, plank barricade"
Connection C.5 to=C.6 type=Broken orientation="north wall, rubble slope"
Connection C.6 to=C.5 type=Broken orientation="east wall, collapsed arch"
```
