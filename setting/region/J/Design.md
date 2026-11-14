# Design of J Pyramid Level 8 - The Lieutenants' Halls

The rooms where the packing set them, the level moved to stand under the chosen's gate: the three lieutenants'
halls round the first's, the council table and the gate of the way down.

```kdl
Design J.a locations="J.1, J.2, J.3, J.4, J.5, J.6, J.7, J.8, J.9" outline="poly -140,100 60,100 60,-100 -140,-100" seed=1 approved="2026-11-14"
Room J.1 width=10 length=20 shape=hall xyz="15,-40"
Room J.2 width=50 length=50 xyz="-10,-30"
Room J.3 width=40 length=50 xyz="-5,20"
Room J.4 width=40 length=50 xyz="-55,-40"
Room J.5 width=50 length=40 xyz="-50,15"
Room J.6 width=40 length=40 xyz="10,65"
Room J.7 width=40 length=40 xyz="-90,-10"
Room J.8 width=10 length=50 shape=hall xyz="20,0"
Room J.9 width=40 length=40 xyz="-90,-45"
Route J.a ends="J.1, J.2" kind=door
Route J.a ends="J.1, I.9" stair=up
Route J.a ends="J.2, J.3" kind=door
Route J.a ends="J.2, J.4" kind=door
Route J.a ends="J.2, J.5" kind=door
Route J.a ends="J.3, J.5" kind=door
Route J.a ends="J.5, J.6"
Route J.a ends="J.6:east, K.1" stair=down
Route J.a ends="J.2, J.7"
Route J.a ends="J.7, J.4" kind=door
Route J.a ends="J.5, J.9"
Route J.a ends="J.4, J.9" kind=door
Route J.a ends="J.1, J.8" kind=door
Route J.a ends="J.8, J.3" kind=door
Place J.1 xyz="15,-40" outline="rect 10 20" shape=hall
Place J.2 xyz="-15,-35" outline="rect 50 50" shape=rect
Place J.3 xyz="0,15" outline="rect 40 50" shape=rect
Place J.4 xyz="-60,-45" outline="rect 40 50" shape=rect
Place J.5 xyz="-45,10" outline="rect 50 40" shape=rect
Place J.6 xyz="10,60" outline="rect 40 40" shape=rect
Place J.7 xyz="-90,0" outline="rect 40 40" shape=rect
Place J.8 xyz="25,-5" outline="rect 10 50" shape=hall
Place J.9 xyz="-100,-50" outline="rect 40 40" shape=rect
Link J.1 to="J.2" kind=door
Link J.1 to="J.8" kind=passage
Link J.2 to="J.3" kind=door
Link J.2 to="J.4" kind=door
Link J.2 to="J.5" kind=door
Link J.2 to="J.7" kind=passage
Link J.3 to="J.5" kind=door
Link J.3 to="J.8" kind=door
Link J.4 to="J.7" kind=door
Link J.4 to="J.9" kind=door
Link J.5 to="J.6" kind=passage
Link J.5 to="J.9" kind=passage
```
