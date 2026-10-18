# Connections of M Thalosae

```kdl
Connection M.1 to="E.9" type="Archway" orientation="south, 50 steps down"
Connection M.1 to="M.2" type="Banded" orientation="north, 60 feet"
Connection M.2 to="M.1" type="Banded" orientation="south, 60 feet"
Connection M.2 to="M.3" type="Wooden" orientation="west, 70 feet"
Connection M.3 to="M.2" type="Wooden" orientation="east, 70 feet"
Connection M.2 to="M.4" type="Archway" orientation="east, 70 feet"
Connection M.4 to="M.2" type="Archway" orientation="west, 70 feet"
Connection M.3 to="M.5" type="Wooden" orientation="north-east, 99 feet"
Connection M.5 to="M.3" type="Wooden" orientation="south-west, 99 feet"
Connection M.4 to="M.5" type="Wooden" orientation="north-west, 99 feet"
Connection M.5 to="M.4" type="Wooden" orientation="south-east, 99 feet"
Connection M.5 to="M.14" type="Wooden" orientation="east, 40 feet" { Secret trigger="push the black hanging" tell="soot on the cloth" }
Connection M.14 to="M.5" type="Wooden" orientation="west, 40 feet"
Connection M.14 to="K.4" type="Stone" orientation="south-west, 120 feet down"
Connection M.2 to="M.6" type="Archway" orientation="east, 40 feet down"
Connection M.6 to="M.2" type="Archway" orientation="west, 40 feet up"
Connection M.6 to="M.7" type="Archway" orientation="north, 60 feet"
Connection M.7 to="M.6" type="Archway" orientation="south, 60 feet"
Connection M.7 to="M.8" type="Open" orientation="west, 50 feet"
Connection M.8 to="M.7" type="Open" orientation="east, 50 feet"
Connection M.7 to="M.9" type="Stone" orientation="north, 50 feet"
Connection M.9 to="M.7" type="Stone" orientation="south, 50 feet"
Connection M.13 to="M.8" type="Stone" orientation="north-east, 60 feet"
Connection M.8 to="M.13" type="Stone" orientation="south-west, 60 feet" { Secret trigger="press the emptiest niche" tell="dust-free streaks on floor" }
Connection M.13 to="L.5" type="Archway" orientation="south, 120 feet down"
Connection M.5 to="M.10" type="Archway" orientation="north, 40 feet"
Connection M.10 to="M.5" type="Archway" orientation="south, 40 feet"
Connection M.9 to="M.10" type="Stone" orientation="west, 40 feet up"
Connection M.10 to="M.9" type="Stone" orientation="east, 40 feet down"
Connection M.10 to="M.11" type="Iron" orientation="north, 60 feet" { Lock key="The Sanctum Key" }
Connection M.11 to="M.10" type="Iron" orientation="south, 60 feet"
Connection M.11 to="M.12" type="Stone" orientation="north, 70 feet" { Lock key="The Vault Key" }
Connection M.12 to="M.11" type="Stone" orientation="south, 70 feet"
```
