# Design of D Pyramid Level 2 - The Halls of History

Four areas, each where one of level 1's ways down lands, joined by winding passages: the robbers' halls round
the landing under the tile floor, the founders' halls under the mural stair, the scraped halls under the
plinth, and the gallery of the fall, locked behind the carvers' cells, over the way down.

```kdl
Design D.a locations="D.1, D.2, D.3, D.4, D.5, D.6, D.7, D.8, D.9, D.10, D.11, D.12" outline="rect 160 160" fill="25-40%" seed=1 approved="2026-11-11"
Room D.1 width=10 length=20 shape=hall
Room D.3 width=20 length=20
Room D.7 width=30 length=30
Room D.8 width=10 length=20 shape=hall
Room D.2 width=40 length=20
Room D.9 width=20 length=30
Room D.5 width=30 length=20
Room D.10 width=20 length=20
Room D.4 width=30 length=30 shape=irregular
Room D.11 width=40 length=10 shape=hall
Room D.12 width=30 length=10 shape=hall
Room D.6 width=30 length=40 shape=apse
Route D.a ends="D.1, D.3" kind=door
Route D.a ends="D.3, D.7" kind=door
Route D.a ends="D.1, D.9" length=7
Route D.a ends="D.8, D.2" kind=door
Route D.a ends="D.2, D.9" kind=door
Route D.a ends="D.9, D.5"
Route D.a ends="D.3, D.4" length=7
Route D.a ends="D.4, D.10" kind=door
Route D.a ends="D.4, D.11"
Route D.a ends="D.11, D.12" length=5
Route D.a ends="D.12, D.6"
Route D.a ends="D.5, D.6" length=6
Route D.a ends="D.1, C.2" stair=up
Route D.a ends="D.8, C.3" stair=up
Route D.a ends="D.10, C.4" stair=up
Route D.a ends="D.6, E.1" stair=down
Place D.1 xyz="-15,0" outline="rect 10 20" shape=hall
Place D.3 xyz="0,0" outline="rect 20 20" shape=rect
Place D.7 xyz="15,-25" outline="rect 30 30" shape=rect
Place D.8 xyz="-15,30" outline="rect 10 20" shape=hall
Place D.2 xyz="10,40" outline="rect 40 20" shape=rect
Place D.9 xyz="40,45" outline="rect 20 30" shape=rect
Place D.5 xyz="5,70" outline="rect 30 20" shape=rect
Place D.10 xyz="30,10" outline="rect 20 20" shape=rect
Place D.4 xyz="55,5" outline="poly -5,15 5,15 5,5 15,5 15,-5 5,-5 5,-15 -15,-15 -15,5 -5,5"
Place D.11 xyz="60,-25" outline="rect 40 10" shape=hall
Place D.12 xyz="-25,-25" outline="rect 30 10" shape=hall
Place D.6 xyz="-45,10" outline="poly -15,5 -14,9 -13,12 -11,16 -7,18 -4,19 0,20 4,19 8,18 11,16 13,12 14,9 15,5 15,-20 -15,-20"
Link D.1 to="D.3" kind=door
Link D.1 to="D.9" kind=passage
Link D.11 to="D.12" kind=passage
Link D.2 to="D.8" kind=door
Link D.2 to="D.9" kind=door
Link D.3 to="D.4" kind=passage
Link D.3 to="D.7" kind=door
Link D.4 to="D.10" kind=door
Link D.4 to="D.11" kind=passage
Link D.5 to="D.6" kind=passage
Link D.5 to="D.9" kind=passage
Link D.6 to="D.12" kind=passage
```
