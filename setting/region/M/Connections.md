# Connections of M Thalosae

```kdl
Connection M.1 to="E.9" type="Archway" bearing="south" distance="50 feet" climb=-30 orientation="fifty steps down"
Connection M.1 to="M.2" type="Banded" bearing="north" distance="60 feet"
Connection M.2 to="M.1" type="Banded" bearing="south" distance="60 feet"
Connection M.2 to="M.3" type="Wooden" bearing="west" distance="70 feet"
Connection M.3 to="M.2" type="Wooden" bearing="east" distance="70 feet"
Connection M.2 to="M.4" type="Archway" bearing="east" distance="70 feet"
Connection M.4 to="M.2" type="Archway" bearing="west" distance="70 feet"
Connection M.3 to="M.5" type="Wooden" bearing="north-east" distance="99 feet"
Connection M.5 to="M.3" type="Wooden" bearing="south-west" distance="99 feet"
Connection M.4 to="M.5" type="Wooden" bearing="north-west" distance="99 feet"
Connection M.5 to="M.4" type="Wooden" bearing="south-east" distance="99 feet"
Connection M.5 to="M.14" type="Wooden" bearing="east" distance="40 feet" { Secret trigger="push the black hanging" tell="soot on the cloth" }
Connection M.14 to="M.5" type="Wooden" bearing="west" distance="40 feet"
Connection M.14 to="K.4" type="Stone" bearing="south-west" distance="120 feet" climb=-120
Connection M.2 to="M.6" type="Archway" bearing="east" distance="40 feet" climb=-40
Connection M.6 to="M.2" type="Archway" bearing="west" distance="40 feet" climb=40
Connection M.6 to="M.7" type="Archway" bearing="north" distance="60 feet"
Connection M.7 to="M.6" type="Archway" bearing="south" distance="60 feet"
Connection M.7 to="M.8" type="Open" bearing="west" distance="50 feet"
Connection M.8 to="M.7" type="Open" bearing="east" distance="50 feet"
Connection M.7 to="M.9" type="Stone" bearing="north" distance="50 feet"
Connection M.9 to="M.7" type="Stone" bearing="south" distance="50 feet"
Connection M.13 to="M.8" type="Stone" bearing="north-east" distance="60 feet"
Connection M.8 to="M.13" type="Stone" bearing="south-west" distance="60 feet" { Secret trigger="press the emptiest niche" tell="dust-free streaks on floor" }
Connection M.13 to="L.5" type="Archway" bearing="south" distance="120 feet" climb=-120
Connection M.5 to="M.10" type="Archway" bearing="north" distance="40 feet"
Connection M.10 to="M.5" type="Archway" bearing="south" distance="40 feet"
Connection M.9 to="M.10" type="Stone" bearing="west" distance="40 feet" climb=40
Connection M.10 to="M.9" type="Stone" bearing="east" distance="40 feet" climb=-40
Connection M.10 to="M.11" type="Iron" bearing="north" distance="60 feet" { Lock key="The Sanctum Key" }
Connection M.11 to="M.10" type="Iron" bearing="south" distance="60 feet"
Connection M.11 to="M.12" type="Stone" bearing="north" distance="70 feet" { Lock key="The Vault Key" }
Connection M.12 to="M.11" type="Stone" bearing="south" distance="70 feet"
```
