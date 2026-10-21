# Connections of F Kobold Warren

```kdl
Connection F.1 to="E.2" type="Open" bearing="east" distance="20 feet"
Connection F.1 to="F.2" type="Crude" bearing="west" distance="40 feet"
Connection F.2 to="F.1" type="Crude" bearing="east" distance="40 feet"
Connection F.2 to="F.3" type="Crude" bearing="west" distance="60 feet" { Hazard type="Pit" damage="Damaging" test="Constitution" wound="Piercing" { Secret trigger="step on thin boards" tell="boards patched with mud" knows="Nib and the kobolds" } }
Connection F.3 to="F.2" type="Crude" bearing="east" distance="60 feet"
Connection F.3 to="F.4" type="Wooden" bearing="south" distance="30 feet"
Connection F.4 to="F.3" type="Wooden" bearing="north" distance="30 feet"
Connection F.3 to="F.5" type="Wooden" bearing="west" distance="50 feet" { Hazard type="Hammer" damage="Nuisance" test="Constitution" wound="Crushing" { Secret trigger="swing the door" tell="wire at the jamb" knows="the kobolds" } }
Connection F.5 to="F.3" type="Wooden" bearing="east" distance="50 feet"
```
