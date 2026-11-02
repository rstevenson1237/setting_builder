# Connections of J Pyramid Level 8 - The Lieutenants' Halls

```kdl
Connection J.1 to="J.2" type="Archway" { Encounter doing="flank the door" reaction="Hostile" far="stone grating" { Creature bestiary="Gargoyle" count=2 } }
Connection J.1 to="I.9" type="Open" climb=20
Connection J.2 to="J.1" type="Archway" { Lock key="The Lieutenants' Word" }
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
Connection J.2 to="J.7" type="Stone"
Connection J.7 to="J.2" type="Stone"
Connection J.7 to="J.4" type="Archway"
Connection J.4 to="J.7" type="Archway"
Connection J.5 to="J.9" type="Stone"
Connection J.9 to="J.5" type="Stone"
Connection J.4 to="J.9" type="Stone"
Connection J.9 to="J.4" type="Stone"
Connection J.1 to="J.8" type="Wooden" { Hazard type="Dart" damage="Nuisance" test="Constitution" wound="Piercing" { Secret trigger="part the hanging" tell="pinholes in the jamb" knows="the lieutenants" } }
Connection J.8 to="J.1" type="Wooden"
Connection J.8 to="J.3" type="Wooden"
Connection J.3 to="J.8" type="Wooden"
```
