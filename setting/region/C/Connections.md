# Connections of C Kashura

```kdl
Connection C.1 to="C.2" type="Open" { Hazard type="Pit" damage="Damaging" test="Constitution" wound="Piercing" { Secret trigger="step on a tile" tell="tiles sit lower" knows="the tomb robbers" } }
Connection C.1 to="A.1" type="Archway" bearing="south" distance="20 feet" climb=15
Connection C.2 to="C.1" type="Open"
Connection C.2 to="C.3" type="Archway"
Connection C.2 to="C.4" type="Open"
Connection C.3 to="C.2" type="Archway"
Connection C.3 to="C.4" type="Stone"
Connection C.4 to="C.2" type="Open"
Connection C.4 to="C.3" type="Stone"
Connection C.4 to="D.1" type="Open" climb=-20 { Secret trigger="turn the plinth" tell="scraped arc, plinth foot" knows="the Scholars" }
```
