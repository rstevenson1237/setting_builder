# Connections of F Kobold Warren

```kdl
Connection F.1 to="E.2" type="Open" orientation="east, 20 feet"
Connection F.1 to="F.2" type="Crude" orientation="west, 40 feet"
Connection F.2 to="F.1" type="Crude" orientation="east, 40 feet"
Connection F.2 to="F.3" type="Crude" orientation="west, 60 feet" { Hazard type="Pit" damage="Damaging" { Secret trigger="step on thin boards" tell="boards patched with mud" } }
Connection F.3 to="F.2" type="Crude" orientation="east, 60 feet"
Connection F.3 to="F.4" type="Wooden" orientation="south, 30 feet"
Connection F.4 to="F.3" type="Wooden" orientation="north, 30 feet"
Connection F.3 to="F.5" type="Wooden" orientation="west, 50 feet" { Hazard type="Hammer" damage="Nuisance" { Secret trigger="swing the door" tell="wire at the jamb" } }
Connection F.5 to="F.3" type="Wooden" orientation="east, 50 feet"
```
