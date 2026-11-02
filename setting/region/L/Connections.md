# Connections of L Pyramid Level 10 - The Demon's Hall

```kdl
Connection L.1 to="L.2" type="Open" { Encounter doing="stand until the threshold is crossed" reaction="Hostile" want="no light carried" { Creature bestiary="Wraith" count=1 } }
Connection L.1 to="K.5" type="Open" climb=30
Connection L.2 to="L.1" type="Open"
Connection L.2 to="L.3" type="Open"
Connection L.2 to="L.4" type="Archway"
Connection L.3 to="L.2" type="Open"
Connection L.3 to="L.4" type="Stone"
Connection L.4 to="L.2" type="Archway"
Connection L.4 to="L.3" type="Stone"
Connection L.1 to="L.5" type="Open"
Connection L.5 to="L.1" type="Open"
Connection L.5 to="L.2" type="Open"
Connection L.2 to="L.5" type="Open"
Connection L.2 to="L.6" type="Open" { Hazard type="Ravine/Climb" damage="Damaging" test="Constitution" wound="Fire" { Secret trigger="step on the lip" tell="steam through cracks" knows="nobody" } }
Connection L.6 to="L.2" type="Open"
Connection L.6 to="L.3" type="Open"
Connection L.3 to="L.6" type="Open"
```
