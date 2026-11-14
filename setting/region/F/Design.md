# Design of F Pyramid Level 4 - The Living Quarters

The landing from the corridor of darts opens on the robbers' guard room and deep camp beside it and on the long
corridor north into the old household: kitchens, laundry, cellar and granary sharing walls, the nobles' rooms with
the nursery, baths and hall of chimes beside them to the east. The servants' cells and the stair gallery down lie west; the
lairs of what came down from the sand - spider hall, scorpion burrow, hyena den, ghoul den - lie east,
on longer ways.

```kdl
Design F.a locations="F.1, F.2, F.3, F.4, F.5, F.6, F.7, F.8, F.9, F.10, F.11, F.12, F.13, F.14, F.15, F.16, F.17, F.18, F.19, F.20" outline="rect 240 240" width=5 seed=1 approved="2026-11-11"
Room F.1 width=10 length=20
Layout F.a id=house arrange=cluster links=none xyz="20,55"
Room F.2 width=10 length=70 xyz="-45,-5"
Room F.12 width=30 length=30 xyz="-25,-65"
Room F.10 width=40 length=40 xyz="10,-70"
Room F.3 layout=house width=40 length=30 xyz="-10,-30"
Room F.16 layout=house width=20 length=20 xyz="-40,-15"
Room F.20 layout=house width=20 length=30 xyz="-40,10"
Room F.6 layout=house width=30 length=40 xyz="-15,5"
Room F.15 layout=house width=20 length=20 xyz="10,5"
Room F.5 layout=house width=30 length=30 xyz="35,10"
Room F.14 layout=house width=30 length=20 shape=apse facing=west xyz="35,35"
Room F.17 layout=house width=20 length=20 xyz="10,35"
Room F.4 width=40 length=30 xyz="-80,15"
Room F.13 width=10 length=70 xyz="-105,-5"
Room F.7 width=40 length=40 xyz="80,-90"
Room F.18 width=40 length=10 xyz="80,-65"
Room F.8 width=30 length=30 shape=organic xyz="95,5"
Room F.19 width=30 length=30 shape=cave xyz="95,-35"
Room F.9 width=30 length=30 shape=organic xyz="95,65"
Room F.11 width=10 length=10 xyz="95,35"
Route F.a ends="F.4, F.7"
Route F.a ends="F.6, F.9"
Route F.a ends="F.1, F.2" kind=door
Route F.a ends="F.1, F.12" kind=door
Route F.a ends="F.12, F.10" kind=door
Route F.a ends="F.12, F.3:south"
Route F.a ends="F.2, F.3:west"
Route F.a ends="F.2, F.4"
Route F.a ends="F.3, F.16" kind=door
Route F.a ends="F.16, F.20" kind=door
Route F.a ends="F.20, F.6" kind=door
Route F.a ends="F.3, F.6" kind=door
Route F.a ends="F.3, F.5"
Route F.a ends="F.6, F.15" kind=door
Route F.a ends="F.5, F.15" kind=door
Route F.a ends="F.5, F.14" kind=door
Route F.a ends="F.14, F.17" kind=door
Route F.a ends="F.4, F.13" kind=door
Route F.a ends="F.7, F.18" kind=door
Route F.a ends="F.18, F.19"
Route F.a ends="F.7, F.8" style=natural
Route F.a ends="F.8, F.19" style=natural
Route F.a ends="F.8, F.11"
Route F.a ends="F.9, F.11"
Route F.a ends="F.5, F.9"
Route F.a ends="F.9, F.17"
Route F.a ends="F.1, E.9" stair=up
Route F.a ends="F.13:south, G.1" stair=down
Place F.1 xyz="-45,-50" outline="rect 10 20" shape=rect
Place F.2 xyz="-45,-5" outline="rect 10 70" shape=rect
Place F.12 xyz="-25,-65" outline="rect 30 30" shape=rect
Place F.10 xyz="10,-70" outline="rect 40 40" shape=rect
Place F.3 xyz="10,25" outline="rect 40 30" shape=rect
Place F.16 xyz="-20,40" outline="rect 20 20" shape=rect
Place F.20 xyz="-20,65" outline="rect 20 30" shape=rect
Place F.6 xyz="5,60" outline="rect 30 40" shape=rect
Place F.15 xyz="30,60" outline="rect 20 20" shape=rect
Place F.5 xyz="55,65" outline="rect 30 30" shape=rect
Place F.14 xyz="55,90" outline="poly 5,10 8,10 10,9 12,7 14,5 15,3 15,0 15,-3 14,-5 12,-7 10,-9 8,-10 5,-10 -15,-10 -15,10"
Place F.17 xyz="30,90" outline="rect 20 20" shape=rect
Place F.4 xyz="-80,15" outline="rect 40 30" shape=rect
Place F.13 xyz="-105,-5" outline="rect 10 70" shape=rect
Place F.7 xyz="80,-90" outline="rect 40 40" shape=rect
Place F.18 xyz="80,-65" outline="rect 40 10" shape=rect
Place F.8 xyz="95,5" outline="rect 30 30" shape=cave
Place F.19 xyz="95,-35" outline="rect 30 30" shape=cave
Place F.9 xyz="95,65" outline="rect 30 30" shape=cave
Place F.11 xyz="95,35" outline="rect 10 10" shape=rect
Link F.1 to="F.12" kind=door
Link F.1 to="F.2" kind=door
Link F.10 to="F.12" kind=door
Link F.14 to="F.17" kind=door
Link F.16 to="F.20" kind=door
Link F.18 to="F.19" kind=passage
Link F.2 to="F.3" kind=passage
Link F.2 to="F.4" kind=passage
Link F.3 to="F.12" kind=passage
Link F.3 to="F.16" kind=door
Link F.3 to="F.5" kind=passage
Link F.3 to="F.6" kind=door
Link F.4 to="F.13" kind=door
Link F.4 to="F.7" kind=passage
Link F.5 to="F.14" kind=door
Link F.5 to="F.15" kind=door
Link F.5 to="F.9" kind=passage
Link F.6 to="F.15" kind=door
Link F.6 to="F.20" kind=door
Link F.6 to="F.9" kind=passage
Link F.7 to="F.18" kind=door
Link F.7 to="F.8" kind=passage
Link F.8 to="F.11" kind=passage
Link F.8 to="F.19" kind=passage
Link F.9 to="F.11" kind=passage
Link F.9 to="F.17" kind=passage
```
