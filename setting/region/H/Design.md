# Design of H Pyramid Level 6 - The Cult's Level

The rooms where the packing set them, the level moved to stand under the stair down from the funerary level:
the cult's rooms round the black corridor, sharing walls.

```kdl
Design H.a locations="H.1, H.2, H.3, H.4, H.5, H.6, H.7, H.8, H.9, H.10, H.11, H.12, H.13, H.14, H.15, H.16, H.17, H.18, H.19, H.20" outline="poly -200,120 40,120 40,-110 -200,-110" fill="25-45%" pad="0 feet" seed=1 approved="2026-11-11"
Room H.1 width=10 length=20 shape=hall xyz="15,45"
Room H.2 width=10 length=50 shape=hall xyz="-85,30"
Room H.3 width=40 length=30 xyz="-110,60"
Room H.4 width=40 length=30 xyz="-80,-10"
Room H.5 width=40 length=40 xyz="-120,15"
Room H.6 width=30 length=30 xyz="-145,50"
Room H.7 width=40 length=40 xyz="-80,-65"
Room H.8 width=30 length=30 xyz="-115,-70"
Room H.9 width=40 length=50 xyz="-160,10"
Room H.10 width=30 length=30 xyz="-15,30"
Room H.11 width=40 length=30 xyz="-120,-20"
Room H.12 width=10 length=20 shape=hall xyz="-75,-35"
Room H.13 width=10 length=50 shape=hall xyz="-35,20"
Room H.14 width=20 length=20 xyz="-140,75"
Room H.15 width=20 length=20 xyz="-50,-25"
Room H.16 width=20 length=30 xyz="-20,0"
Room H.17 width=10 length=40 shape=hall xyz="-145,-35"
Room H.18 width=40 length=10 shape=hall xyz="-60,30"
Room H.19 width=30 length=30 xyz="-145,-70"
Room H.20 width=20 length=20 xyz="-70,50"
Route H.a ends="H.18, H.20" kind=door
Route H.a ends="H.1, H.2"
Route H.a ends="H.1, H.10"
Route H.a ends="H.1, G.19" stair=up
Route H.a ends="H.1, B.10" stair=up
Route H.a ends="H.2, H.3" kind=door
Route H.a ends="H.2, H.4" kind=door
Route H.a ends="H.3, H.5"
Route H.a ends="H.3, H.6" kind=door
Route H.a ends="H.3, H.10"
Route H.a ends="H.4, H.5" kind=door
Route H.a ends="H.4, H.7"
Route H.a ends="H.4, H.12" kind=door
Route H.a ends="H.5, H.9" kind=door
Route H.a ends="H.6, H.9" kind=door
Route H.a ends="H.7, H.8" kind=door
Route H.a ends="H.8, H.11"
Route H.a ends="H.9, H.11" kind=door
Route H.a ends="H.10, H.13" kind=door
Route H.a ends="H.12, I.1" stair=down
Route H.a ends="H.3, H.14" kind=door
Route H.a ends="H.10, H.16" kind=door
Route H.a ends="H.4, H.15" kind=door
Route H.a ends="H.6, H.17"
Route H.a ends="H.17, H.19" kind=door
Route H.a ends="H.8, H.19" kind=door
Route H.a ends="H.13, H.18" kind=door
Place H.1 xyz="15,50" outline="rect 10 20" shape=hall
Place H.2 xyz="-85,35" outline="rect 10 50" shape=hall
Place H.3 xyz="-110,65" outline="rect 40 30" shape=rect
Place H.4 xyz="-80,-15" outline="rect 40 30" shape=rect
Place H.5 xyz="-120,20" outline="rect 40 40" shape=rect
Place H.6 xyz="-145,55" outline="rect 30 30" shape=rect
Place H.7 xyz="-80,-60" outline="rect 40 40" shape=rect
Place H.8 xyz="-115,-75" outline="rect 30 30" shape=rect
Place H.9 xyz="-160,15" outline="rect 40 50" shape=rect
Place H.10 xyz="-15,25" outline="rect 30 30" shape=rect
Place H.11 xyz="-120,-15" outline="rect 40 30" shape=rect
Place H.12 xyz="-55,-30" outline="rect 10 20" shape=hall
Place H.13 xyz="-35,15" outline="rect 10 50" shape=hall
Place H.14 xyz="-140,80" outline="rect 20 20" shape=rect
Place H.15 xyz="-40,-30" outline="rect 20 20" shape=rect
Place H.16 xyz="-20,-5" outline="rect 20 30" shape=rect
Place H.17 xyz="-145,-40" outline="rect 10 40" shape=hall
Place H.18 xyz="-60,35" outline="rect 40 10" shape=hall
Place H.19 xyz="-145,-75" outline="rect 30 30" shape=rect
Place H.20 xyz="-70,50" outline="rect 20 20" shape=rect
Link H.1 to="H.10" kind=passage
Link H.1 to="H.2" kind=passage
Link H.10 to="H.13" kind=door
Link H.10 to="H.16" kind=door
Link H.13 to="H.18" kind=door
Link H.17 to="H.19" kind=door
Link H.18 to="H.20" kind=door
Link H.2 to="H.3" kind=door
Link H.2 to="H.4" kind=passage
Link H.3 to="H.10" kind=passage
Link H.3 to="H.14" kind=door
Link H.3 to="H.5" kind=passage
Link H.3 to="H.6" kind=door
Link H.4 to="H.12" kind=door
Link H.4 to="H.15" kind=passage
Link H.4 to="H.5" kind=passage
Link H.4 to="H.7" kind=passage
Link H.5 to="H.9" kind=door
Link H.6 to="H.17" kind=passage
Link H.6 to="H.9" kind=door
Link H.7 to="H.8" kind=door
Link H.8 to="H.11" kind=passage
Link H.8 to="H.19" kind=door
Link H.9 to="H.11" kind=door
```
