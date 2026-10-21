# Connections of K Bugbear Den

```kdl
Connection K.1 to="E.7" type="Open" bearing="west" distance="50 yards" orientation="down the dry bed"
Connection K.1 to="K.3" type="Open" bearing="east" distance="40 feet"
Connection K.3 to="K.1" type="Open" bearing="west" distance="40 feet"
Connection K.3 to="K.2" type="Wooden" bearing="north" distance="40 feet"
Connection K.2 to="K.3" type="Wooden" bearing="south" distance="40 feet"
Connection K.3 to="K.5" type="Crude" bearing="east" distance="60 feet"
Connection K.5 to="K.3" type="Crude" bearing="west" distance="60 feet"
Connection K.5 to="K.4" type="Stone" bearing="south" distance="30 feet" { Secret trigger="break the plaster" tell="hollow sound, cracked seam" }
Connection K.4 to="K.5" type="Stone" bearing="north" distance="30 feet"
Connection K.4 to="M.14" type="Stone" bearing="north-east" distance="120 feet" climb=120
```
