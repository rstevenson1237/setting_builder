# Connections of C The Goblin Cave

```kdl
Connection C.1 to=C.2 type=Crude orientation="hide curtain, left"
Connection C.1 to=C.3 type=Open orientation="right fork, slopes down"
Connection C.1 to=B.3 type=Open orientation="outer end, daylight"
Connection C.2 to=C.1 type=Crude orientation="hide curtain, entrance"
Connection C.2 to=C.4 type=Archway orientation="north side, wide arch"
Connection C.2 to=C.5 type=Wooden orientation="east wall, plank door"
Connection C.3 to=C.1 type=Open orientation="up the slope"
Connection C.3 to=C.6 type=Archway orientation="deep end, worn stair"
Connection C.4 to=C.2 type=Archway orientation="south side, arch"
Connection C.4 to=C.5 type=Crude orientation="behind heaped crates" { Secret trigger="shift the heaped crates" tell="draught behind the crates" }
Connection C.5 to=C.2 type=Wooden orientation="near wall, plank door"
Connection C.5 to=C.4 type=Crude orientation="gap behind seat"
Connection C.6 to=C.3 type=Archway orientation="up the worn stair"
```
