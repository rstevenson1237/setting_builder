# Design of C Pyramid Level 1 - The Trapped Rooms

The tiled hall at the centre with a room against each of its walls: the threshold to the south, the mural
wall to the north with the offering niche behind it, the sand clock to the west, and the round plinth room
to the east, reached from the hall and from the mural wall.

```kdl
Design C.a locations="C.1, C.2, C.3, C.4, C.5, C.6" outline="rect 100 100" fill="35-55%" seed=1 approved="2026-11-11"
Room C.2 width=40 length=40 xyz="-10,0"
Room C.1 width=10 length=20 shape=hall facing=south
Room C.3 width=40 length=20 facing=north
Room C.4 width=30 length=30 shape=round facing=east
Room C.5 width=20 length=20 facing=west
Room C.6 width=10 length=10
Route C.a ends="C.2:south, C.1" kind=door
Route C.a ends="C.2:north, C.3" kind=door
Route C.a ends="C.2:west, C.5" kind=door
Route C.a ends="C.2:east, C.4" length=short
Route C.a ends="C.3:east, C.4"
Route C.a ends="C.3:north, C.6" kind=door
Route C.a ends="C.1, A.1" stair=up
Route C.a ends="C.2, D.1" stair=down
Route C.a ends="C.3, D.8" stair=down
Route C.a ends="C.4, D.10" stair=down
Place C.2 xyz="-10,0" outline="rect 40 40" shape=rect
Place C.1 xyz="-5,-30" outline="rect 10 20" shape=hall
Place C.3 xyz="-10,30" outline="rect 40 20" shape=rect
Place C.4 xyz="35,5" outline="rect 30 30" shape=round
Place C.5 xyz="-40,0" outline="rect 20 20" shape=rect
Place C.6 xyz="-5,45" outline="rect 10 10" shape=rect
Link C.1 to="C.2" kind=door
Link C.2 to="C.3" kind=door
Link C.2 to="C.4" kind=passage
Link C.2 to="C.5" kind=door
Link C.3 to="C.4" kind=passage
Link C.3 to="C.6" kind=door
```
