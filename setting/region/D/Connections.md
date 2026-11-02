# Connections of D Pyramid Level 2 - The Halls of History

```kdl
Connection D.1 to="D.3" type="Wooden"
Connection D.1 to="D.9" type="Archway" { Encounter doing="patrol the archway" reaction="Wary" want="the hall cleared of robbers" { Faction faction="Kurumisa" present=2 members="two soldiers" } }
Connection D.1 to="C.2" type="Stone" climb=20
Connection D.2 to="D.8" type="Open"
Connection D.2 to="D.9" type="Stone"
Connection D.3 to="D.1" type="Wooden"
Connection D.3 to="D.7" type="Open"
Connection D.3 to="D.4" type="Open" { Encounter doing="gnaw through the doorway" reaction="Hostile" { Creature bestiary="Giant Rat" count="4-8" } }
Connection D.4 to="D.3" type="Open"
Connection D.4 to="D.10" type="Open"
Connection D.4 to="D.11" type="Stone"
Connection D.5 to="D.9" type="Stone"
Connection D.5 to="D.6" type="Archway" { Lock key="The Sun-Disc Key" }
Connection D.6 to="D.5" type="Archway"
Connection D.6 to="D.12" type="Stone"
Connection D.6 to="E.1" type="Open" climb=-20
Connection D.7 to="D.3" type="Open"
Connection D.8 to="D.2" type="Open" { Hazard type="Dart" damage="Nuisance" test="Constitution" wound="Piercing" { Secret trigger="touch the sill" tell="pinholes in the jambs" knows="the tomb robbers" } }
Connection D.8 to="C.3" type="Stone" climb=20
Connection D.9 to="D.1" type="Archway"
Connection D.9 to="D.2" type="Stone"
Connection D.9 to="D.5" type="Stone" { Encounter doing="copy the name plates" reaction="Wary" know="the order of the kings" { Faction faction="Sihuahet" present=1 members="an adept" } }
Connection D.10 to="D.4" type="Open" { Hazard type="Pit" damage="Nuisance" test="Constitution" wound="Crushing" { Secret trigger="wade the deep drift" tell="dust sunk, hollow" knows="nobody" } }
Connection D.10 to="C.4" type="Stone" climb=20
Connection D.11 to="D.4" type="Stone"
Connection D.11 to="D.12" type="Open"
Connection D.12 to="D.11" type="Open"
Connection D.12 to="D.6" type="Stone"
```
