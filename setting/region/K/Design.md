# Design of K Pyramid Level 9 - The Antechamber

The rooms where the packing set them, the level moved to stand under the gate of the way down: the wailing and
choking halls, the round breathing room, and the last threshold over the demon's chamber.

```kdl
Design K.a locations="K.1, K.2, K.3, K.4, K.5, K.6, K.7, K.8" outline="poly -150,120 50,120 50,-80 -150,-80" width=5 seed=1 approved="2026-11-14"
Room K.1 width=10 length=20 xyz="10,60"
Room K.2 width=60 length=40 xyz="-30,55"
Room K.3 width=50 length=50 xyz="-50,10"
Room K.4 width=40 length=40 xyz="-80,55"
Room K.5 width=30 length=30 xyz="5,20"
Room K.6 width=30 length=30 xyz="-100,85" shape=round
Room K.7 width=30 length=30 xyz="-90,20"
Room K.8 width=40 length=40 xyz="-95,-15"
Route K.a ends="K.1, K.2" kind=door
Route K.a ends="K.1, J.6" stair=up
Route K.a ends="K.2, K.3" kind=door
Route K.a ends="K.2, K.4" kind=door
Route K.a ends="K.3, K.5"
Route K.a ends="K.3, K.4" kind=door
Route K.a ends="K.5:east, L.1" stair=down
Route K.a ends="K.2, K.6"
Route K.a ends="K.6, K.8"
Route K.a ends="K.8, K.3" kind=door
Route K.a ends="K.4, K.7" kind=door
Place K.1 xyz="15,60" outline="rect 10 20" shape=rect
Place K.2 xyz="-30,50" outline="rect 60 40" shape=rect
Place K.3 xyz="-45,5" outline="rect 50 50" shape=rect
Place K.4 xyz="-80,50" outline="rect 40 40" shape=rect
Place K.5 xyz="5,5" outline="rect 30 30" shape=rect
Place K.6 xyz="-95,85" outline="rect 30 30" shape=round
Place K.7 xyz="-85,15" outline="rect 30 30" shape=rect
Place K.8 xyz="-90,-20" outline="rect 40 40" shape=rect
Link K.1 to="K.2" kind=passage
Link K.2 to="K.3" kind=door
Link K.2 to="K.4" kind=door
Link K.2 to="K.6" kind=passage
Link K.3 to="K.4" kind=door
Link K.3 to="K.5" kind=passage
Link K.3 to="K.8" kind=door
Link K.4 to="K.7" kind=door
Link K.6 to="K.8" kind=passage
```
