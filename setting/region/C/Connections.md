# Connections of C Pyramid Level 1 - The Trapped Rooms

```kdl
Connection C.1 to="C.2" type="Open" { Hazard type="Pit" damage="Nuisance" test="Constitution" wound="Crushing" { Secret trigger="step on blue" tell="tiles sit lower" knows="the tomb robbers" } }
Connection C.1 to="A.1" type="Archway" bearing="south-east" distance="42 feet" climb=15
Connection C.2 to="C.1" type="Open"
Connection C.2 to="C.3" type="Archway"
Connection C.2 to="C.4" type="Open"
Connection C.2 to="C.5" type="Wooden"
Connection C.2 to="D.1" type="Stone" climb=-20 { Hazard type="Spike" damage="Damaging" test="Constitution" wound="Piercing" { Secret trigger="tiles stepped unordered" tell="numerals on twelve tiles" knows="the tomb robbers" fact="in order, the tiles fold into stairs" } }
Connection C.3 to="C.2" type="Archway"
Connection C.3 to="C.4" type="Stone"
Connection C.3 to="C.6" type="Open" { Hazard type="Dart" damage="Nuisance" test="Constitution" wound="Piercing" { Secret trigger="reach past the bowls" tell="pinholes in the ledge" knows="nobody" } }
Connection C.3 to="D.8" type="Stone" climb=-20 { Hazard type="Hammer" damage="Nuisance" test="Constitution" wound="Crushing" { Secret trigger="tread the third step" tell="a groove overhead" knows="the Scholars" fact="panels read in order open it" } }
Connection C.4 to="C.2" type="Open"
Connection C.4 to="C.3" type="Stone"
Connection C.4 to="D.10" type="Stone" climb=-20 { Hazard type="Gas" damage="Damaging" test="Constitution" wound="Poison" { Secret trigger="turn the plinth sunwise" tell="scraped arc, plinth foot" knows="the Scholars" fact="turned against the sun, it opens" } }
Connection C.5 to="C.2" type="Wooden"
Connection C.6 to="C.3" type="Open"
```
