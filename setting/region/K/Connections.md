# Connections of K Bugbear Den

```kdl
Connection K.1 to="E.7" type="Open" orientation="west, 200 yards"
Connection K.1 to="K.3" type="Open" orientation="east, 200 yards"
Connection K.3 to="K.1" type="Open" orientation="west, 200 yards"
Connection K.3 to="K.2" type="Wooden" orientation="north, 40 feet"
Connection K.2 to="K.3" type="Wooden" orientation="south, 40 feet"
Connection K.3 to="K.5" type="Crude" orientation="east, 60 feet"
Connection K.5 to="K.3" type="Crude" orientation="west, 60 feet"
Connection K.5 to="K.4" type="Stone" orientation="south, 30 feet" { Secret trigger="break the plaster" tell="hollow sound, cracked seam" }
Connection K.4 to="K.5" type="Stone" orientation="north, 30 feet"
Connection K.4 to="M.14" type="Stone" orientation="north-east, 120 feet"
```
