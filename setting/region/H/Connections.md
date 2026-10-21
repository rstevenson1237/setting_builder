# Connections of H Orc Warren

```kdl
Connection H.1 to="E.4" type="Open" bearing="east" distance="20 feet"
Connection H.1 to="H.2" type="Archway" bearing="west" distance="60 feet"
Connection H.2 to="H.1" type="Archway" bearing="east" distance="60 feet"
Connection H.2 to="H.3" type="Wooden" bearing="north" distance="50 feet"
Connection H.3 to="H.2" type="Wooden" bearing="south" distance="50 feet"
Connection H.2 to="H.4" type="Archway" bearing="south" distance="40 feet"
Connection H.4 to="H.2" type="Archway" bearing="north" distance="40 feet"
Connection H.2 to="H.6" type="Banded" bearing="west" distance="70 feet"
Connection H.6 to="H.2" type="Banded" bearing="east" distance="70 feet"
Connection H.4 to="H.5" type="Broken" bearing="west" distance="50 feet"
Connection H.5 to="H.4" type="Broken" bearing="east" distance="50 feet"
Connection H.5 to="G.5" type="Stone" bearing="south" distance="50 yards" orientation="behind the sacks" { Secret trigger="lift lowest stones" tell="cold draught, low down" knows="neither tribe" fact="each tribe thinks it ends at its wall" }
```
