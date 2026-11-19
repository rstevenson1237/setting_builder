# Design of HB The Pyramid's Halls

The shaft's foot opens on the winch room and the long hall, a spine of side rooms down both its sides: the guard room, barracks, armoury and larder to the west, the pens, the feeding cell and the priests' study to the east. The hall ends on the snake people's quarters, with the treasury behind them, the cistern beside them and the sanctum stair at the far end.

```kdl
Design HB.a locations="HB.1, HB.2, HB.3, HB.4, HB.5, HB.6, HB.7, HB.8, HB.9, HB.10, HB.11, HB.12, HB.13, HB.14" outline="rect 180 200" fill="25-45%" seed=1 approved="2026-11-19"
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
Place HB.1 xyz="60,70" outline="rect 20 20" shape=rect
Place HB.2 xyz="65,90" outline="rect 30 20" shape=rect
Place HB.4 xyz="-5,45" outline="rect 10 110" shape=hall
Place HB.3 xyz="-25,90" outline="rect 30 20" shape=rect
Place HB.7 xyz="20,65" outline="rect 40 30" shape=rect
Place HB.12 xyz="-25,70" outline="rect 30 20" shape=rect
Place HB.10 xyz="10,40" outline="rect 20 20" shape=rect
Place HB.5 xyz="-30,40" outline="rect 40 40" shape=rect
Place HB.6 xyz="10,20" outline="rect 20 20" shape=rect
Place HB.11 xyz="-25,5" outline="rect 30 30" shape=rect
Place HB.8 xyz="0,-80" outline="rect 60 40" shape=rect
Place HB.9 xyz="45,-85" outline="rect 30 30" shape=rect
Place HB.14 xyz="-50,-85" outline="rect 20 30" shape=rect
Place HB.13 xyz="80,-90" outline="rect 20 20" shape=rect
Link HB.1 to="HB.2" kind=door
Link HB.2 to="HB.4" kind=passage
Link HB.3 to="HB.4" kind=door
Link HB.4 to="HB.10" kind=door
Link HB.4 to="HB.11" kind=door
Link HB.4 to="HB.12" kind=door
Link HB.4 to="HB.5" kind=door
Link HB.4 to="HB.6" kind=door
Link HB.4 to="HB.7" kind=door
Link HB.4 to="HB.8" kind=passage
Link HB.8 to="HB.13" kind=passage
Link HB.8 to="HB.14" kind=passage
Link HB.8 to="HB.9" kind=door
```
