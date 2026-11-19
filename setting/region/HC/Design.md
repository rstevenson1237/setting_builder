# Design of HC The God's Sanctum

A stair cut in the rock comes down to the sacrifice hall, with the altar gallery on its east side and the priests' cell on its west. A bone-lined passage runs south from the hall to the god's cavern, with the offering pit beside the cavern's mouth and the emperor's bier at its far end.

```kdl
Design HC.a locations="HC.1, HC.2, HC.3, HC.4, HC.5, HC.6, HC.7, HC.8" outline="rect 150 160" fill="25-45%" pad="0 feet"
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
```
