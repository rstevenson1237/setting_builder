# Design of J Pyramid Level 8 - The Lieutenants' Halls

The rooms where the packing set them, the level moved to stand under the chosen's gate: the three lieutenants'
halls round the first's, the council table and the gate of the way down.

```kdl
Design J.a locations="J.1, J.2, J.3, J.4, J.5, J.6, J.7, J.8, J.9" outline="poly -110,80 50,80 50,-80 -110,-80" fill="25-45%" pad="0 feet" seed=1 approved="2026-11-11"
Room J.1 width=10 length=20 shape=hall xyz="20,-40"
Room J.2 width=40 length=40 xyz="-5,-30"
Room J.3 width=30 length=40 xyz="0,10"
Room J.4 width=30 length=40 xyz="-40,-40"
Room J.5 width=40 length=30 xyz="-35,5"
Room J.6 width=30 length=30 xyz="10,45"
Room J.7 width=30 length=30 xyz="-70,-15"
Room J.8 width=10 length=40 shape=hall xyz="20,-10"
Room J.9 width=30 length=30 xyz="-70,-45"
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
Place J.2 xyz="-10,-30" outline="rect 40 40" shape=rect
Place J.3 xyz="5,10" outline="rect 30 40" shape=rect
Place J.4 xyz="-45,-40" outline="rect 30 40" shape=rect
Place J.5 xyz="-30,5" outline="rect 40 30" shape=rect
Place J.6 xyz="5,45" outline="rect 30 30" shape=rect
Place J.7 xyz="-75,-15" outline="rect 30 30" shape=rect
Place J.8 xyz="25,-10" outline="rect 10 40" shape=hall
Place J.9 xyz="-75,-45" outline="rect 30 30" shape=rect
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
