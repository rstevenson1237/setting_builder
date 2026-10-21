# Connections of G Goblin Hold

```kdl
Connection G.1 to="E.3" type="Open" bearing="east" distance="20 feet"
Connection G.1 to="G.2" type="Crude" bearing="west" distance="70 feet"
Connection G.2 to="G.1" type="Crude" bearing="east" distance="70 feet"
Connection G.2 to="G.3" type="Crude" bearing="south" distance="80 feet"
Connection G.3 to="G.2" type="Crude" bearing="north" distance="80 feet"
Connection G.2 to="G.4" type="Wooden" bearing="north" distance="60 feet"
Connection G.4 to="G.2" type="Wooden" bearing="south" distance="60 feet"
Connection G.2 to="G.5" type="Wooden" bearing="west" distance="60 feet"
Connection G.5 to="G.2" type="Wooden" bearing="east" distance="60 feet"
Connection G.2 to="G.6" type="Banded" bearing="south-west" distance="100 feet"
Connection G.6 to="G.2" type="Banded" bearing="north-east" distance="100 feet"
Connection G.5 to="H.5" type="Stone" bearing="north" distance="50 yards" orientation="behind new stones" { Secret trigger="pull out loose stones" tell="newer stones, fresh mortar" }
```
