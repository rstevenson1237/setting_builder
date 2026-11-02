# Connections of E Pyramid Level 3 - The Turning Hall

```kdl
Connection E.1 to="E.2" type="Archway"
Connection E.1 to="D.6" type="Open" climb=20
Connection E.2 to="E.1" type="Archway" wall="east"
Connection E.2 to="E.3" type="Archway" wall="north"
Connection E.2 to="E.15" type="Archway" wall="north-east"
Connection E.2 to="E.9" type="Archway" wall="south-east"
Connection E.2 to="E.5" type="Archway" wall="south"
Connection E.2 to="E.14" type="Stone" wall="south-west" { Secret trigger="the pair pressed" tell="a blank, runed wall" knows="the Scholars" fact="its arch is walled behind plaster" }
Connection E.2 to="E.13" type="Archway" wall="west"
Connection E.2 to="E.4" type="Archway" wall="north-west"
Connection E.3 to="E.2" type="Archway"
Connection E.3 to="E.6" type="Iron" { Lock key="The Armoury Key" }
Connection E.3 to="E.10" type="Open"
Connection E.4 to="E.2" type="Archway"
Connection E.4 to="E.7" type="Open"
Connection E.4 to="E.11" type="Wooden"
Connection E.5 to="E.2" type="Archway"
Connection E.5 to="E.8" type="Open"
Connection E.5 to="E.12" type="Wooden"
Connection E.6 to="E.3" type="Iron"
Connection E.7 to="E.4" type="Open"
Connection E.8 to="E.5" type="Open"
Connection E.9 to="E.2" type="Archway"
Connection E.9 to="F.1" type="Open" climb=-24 { Hazard type="Pit" damage="Lethal" test="Constitution" wound="Piercing" { Secret trigger="the stair's top step" tell="a hairline seam" knows="the Royal Guard" } }
Connection E.10 to="E.3" type="Open"
Connection E.11 to="E.4" type="Wooden"
Connection E.12 to="E.5" type="Wooden"
Connection E.13 to="E.2" type="Archway"
Connection E.13 to="E.14" type="Stone" { Secret trigger="push the end shelf" tell="a shelf on runners" knows="nobody" }
Connection E.14 to="E.13" type="Stone"
Connection E.14 to="E.2" type="Stone"
Connection E.15 to="E.2" type="Archway"
```
