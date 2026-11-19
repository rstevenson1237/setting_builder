# Design of HB The Pyramid's Halls

The shaft's foot opens on the winch room and the long hall, a spine of side rooms down both its sides: the guard room, barracks, armoury and larder to the west, the pens, the feeding cell and the priests' study to the east. The hall ends on the snake people's quarters, with the treasury behind them, the cistern beside them and the sanctum stair at the far end.

```kdl
Design HB.a locations="HB.1, HB.2, HB.3, HB.4, HB.5, HB.6, HB.7, HB.8, HB.9, HB.10, HB.11, HB.12, HB.13, HB.14" outline="rect 180 200" fill="25-45%"
Room HB.1 width=20 length=20 facing=north
Room HB.2 width=30 length=20 facing=north
Layout HB.a id=hall arrange=spine entry=HB.4 facing=north
Room HB.4 layout=hall width=10 length=100 shape=hall
Room HB.3 layout=hall width=30 length=20
Room HB.7 layout=hall width=40 length=30
Room HB.12 layout=hall width=30 length=20
Room HB.10 layout=hall width=20 length=20
Room HB.5 layout=hall width=40 length=40
Room HB.6 layout=hall width=20 length=20
Room HB.11 layout=hall width=30 length=30
Room HB.8 width=60 length=40 facing=south
Room HB.9 width=30 length=30 facing=south
Room HB.14 width=20 length=30 facing=south
Room HB.13 width=20 length=20 facing=south
Route HB.a ends="HB.1, HB.2" kind=door
Route HB.a ends="HB.2, HB.4"
Route HB.a ends="HB.4:south, HB.8:north"
Route HB.a ends="HB.8, HB.9" kind=door door=locked
Route HB.a ends="HB.8, HB.14"
Route HB.a ends="HB.8:south, HB.13:north"
Route HB.a ends="HB.13, HC.1" stair=down
Route HB.a ends="HB.1, HA.10" stair=up
```
