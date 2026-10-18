# Connections of H Orc Warren

```kdl
Connection H.1 to="E.4" type="Open" orientation="east, 20 feet"
Connection H.1 to="H.2" type="Archway" orientation="west, 60 feet"
Connection H.2 to="H.1" type="Archway" orientation="east, 60 feet"
Connection H.2 to="H.3" type="Wooden" orientation="north, 50 feet"
Connection H.3 to="H.2" type="Wooden" orientation="south, 50 feet"
Connection H.2 to="H.4" type="Archway" orientation="south, 40 feet"
Connection H.4 to="H.2" type="Archway" orientation="north, 40 feet"
Connection H.2 to="H.6" type="Banded" orientation="west, 70 feet"
Connection H.6 to="H.2" type="Banded" orientation="east, 70 feet"
Connection H.4 to="H.5" type="Broken" orientation="west, 50 feet"
Connection H.5 to="H.4" type="Broken" orientation="east, 50 feet"
Connection H.5 to="G.5" type="Stone" orientation="south, behind sacks" { Secret trigger="lift lowest stones" tell="cold draught, low down" }
```
