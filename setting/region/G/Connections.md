# Connections of G Goblin Hold

```kdl
Connection G.1 to="E.3" type="Open" orientation="east, 20 feet"
Connection G.1 to="G.2" type="Crude" orientation="west, 70 feet"
Connection G.2 to="G.1" type="Crude" orientation="east, 70 feet"
Connection G.2 to="G.3" type="Crude" orientation="south, 80 feet"
Connection G.3 to="G.2" type="Crude" orientation="north, 80 feet"
Connection G.2 to="G.4" type="Wooden" orientation="north, 60 feet"
Connection G.4 to="G.2" type="Wooden" orientation="south, 60 feet"
Connection G.2 to="G.5" type="Wooden" orientation="west, 60 feet"
Connection G.5 to="G.2" type="Wooden" orientation="east, 60 feet"
Connection G.2 to="G.6" type="Banded" orientation="south-west, 85 feet"
Connection G.6 to="G.2" type="Banded" orientation="north-east, 85 feet"
Connection G.5 to="H.5" type="Stone" orientation="west, behind new stones" { Secret trigger="pull out loose stones" tell="newer stones, fresh mortar" }
```
