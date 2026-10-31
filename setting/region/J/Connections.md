# Connections of J Krothox

```kdl
Connection J.1 to="J.2" type="Archway" { Encounter doing="flank the door" reaction="Hostile" far="stone grating" { Creature bestiary="Gargoyle" count=2 } }
Connection J.1 to="I.9" type="Open" climb=20
Connection J.2 to="J.1" type="Archway"
Connection J.2 to="J.3" type="Stone"
Connection J.2 to="J.4" type="Stone"
Connection J.2 to="J.5" type="Archway"
Connection J.3 to="J.2" type="Stone"
Connection J.3 to="J.5" type="Stone"
Connection J.4 to="J.2" type="Stone"
Connection J.5 to="J.2" type="Archway"
Connection J.5 to="J.6" type="Iron" { Lock key="The Council Seal" }
Connection J.5 to="J.3" type="Stone"
Connection J.6 to="J.5" type="Iron"
Connection J.6 to="K.1" type="Open" climb=-20
```
