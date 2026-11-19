# Design of HC The God's Sanctum

A stair cut in the rock comes down to the sacrifice hall, with the altar gallery on its east side and the priests' cell on its west. A bone-lined passage runs south from the hall to the god's cavern, with the offering pit beside the cavern's mouth and the emperor's bier at its far end.

```kdl
Design HC.a locations="HC.1, HC.2, HC.3, HC.4, HC.5, HC.6, HC.7, HC.8" outline="rect 150 160" fill="25-45%" pad="0 feet" seed=1 approved="2026-11-19"
Room HC.2 width=60 length=40 xyz="0,20"
Room HC.1 width=20 length=20 facing=north
Room HC.3 width=30 length=30 facing=east
Room HC.5 width=20 length=20 facing=west
Room HC.4 width=10 length=40 shape=hall facing=south
Room HC.6 width=70 length=50 shape=cave facing=south
Room HC.8 width=30 length=30 shape=round facing=east
Room HC.7 width=30 length=30 shape=round facing=west
Route HC.a ends="HC.1, HC.2" kind=door
Route HC.a ends="HC.2, HC.3" kind=door
Route HC.a ends="HC.2, HC.5" kind=door
Route HC.a ends="HC.2:south, HC.4:north"
Route HC.a ends="HC.4:south, HC.6:north"
Route HC.a ends="HC.6, HC.8"
Route HC.a ends="HC.6:west, HC.7:east" length=short
Route HC.a ends="HC.1, HB.13" stair=up
Place HC.2 xyz="5,20" outline="rect 60 40" shape=rect
Place HC.1 xyz="-5,50" outline="rect 20 20" shape=rect
Place HC.3 xyz="50,15" outline="rect 30 30" shape=rect
Place HC.5 xyz="-35,0" outline="rect 20 20" shape=rect
Place HC.4 xyz="40,-20" outline="rect 10 40" shape=hall
Place HC.6 xyz="0,-55" outline="rect 70 50" shape=cave
Place HC.8 xyz="60,-15" outline="rect 30 30" shape=round
Place HC.7 xyz="-60,-55" outline="rect 30 30" shape=round
Link HC.1 to="HC.2" kind=door
Link HC.2 to="HC.3" kind=door
Link HC.2 to="HC.4" kind=passage
Link HC.2 to="HC.5" kind=door
Link HC.4 to="HC.6" kind=passage
Link HC.6 to="HC.7" kind=passage
Link HC.6 to="HC.8" kind=passage
```
