# Connections of A The Smoke Hole

```kdl
Connection A.1 to=A.2 type=Open orientation="east side, slopes down"
Connection A.1 to=A.3 type=Crude orientation="north side, stake gate"
Connection A.1 to=A.4 type=Archway orientation="straight back, smoke-filled"
Connection A.2 to=A.1 type=Open orientation="up the slope"
Connection A.2 to=A.5 type=Crude orientation="foot of the heap" { Secret trigger="dig the heap's foot" tell="draught through the bones" }
Connection A.3 to=A.1 type=Crude orientation="south, stake gate"
Connection A.4 to=A.1 type=Archway orientation="behind the table, out"
Connection A.4 to=A.5 type=Wooden orientation="left of the seat"
Connection A.4 to=A.6 type=Banded orientation="right of the seat"
Connection A.5 to=A.4 type=Wooden orientation="near wall, two steps"
Connection A.5 to=A.6 type=Broken orientation="far wall, fallen timbers"
Connection A.5 to=A.2 type=Crude orientation="crack beside the windlass"
Connection A.6 to=A.4 type=Banded orientation="low door, east"
Connection A.6 to=A.5 type=Broken orientation="rubble-choked gap, west"
```
