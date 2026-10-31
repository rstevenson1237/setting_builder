# Connections of D Sihura

```kdl
Connection D.1 to="D.2" type="Archway" { Encounter doing="patrol the archway" reaction="Wary" want="the hall cleared of robbers" { Faction faction="Kurumisa" present=2 members="two soldiers" } }
Connection D.1 to="D.3" type="Wooden"
Connection D.1 to="C.4" type="Open" climb=20
Connection D.2 to="D.1" type="Archway"
Connection D.2 to="D.4" type="Open" { Encounter doing="copy the scraped glyphs" reaction="Wary" know="what the murals showed" { Faction faction="Sihuahet" present=1 members="an adept" } }
Connection D.2 to="D.5" type="Stone"
Connection D.3 to="D.1" type="Wooden"
Connection D.3 to="D.5" type="Open" { Encounter doing="gnaw through the doorway" reaction="Hostile" { Creature bestiary="Giant Rat" count="4-8" } }
Connection D.4 to="D.2" type="Open"
Connection D.4 to="D.6" type="Stone"
Connection D.5 to="D.3" type="Open"
Connection D.5 to="D.2" type="Stone"
Connection D.5 to="D.6" type="Archway" { Lock key="The Sun-Disc Key" }
Connection D.6 to="D.5" type="Archway"
Connection D.6 to="D.4" type="Stone"
Connection D.6 to="E.1" type="Open" climb=-20
```
