# Design of E Pyramid Level 3 - The Turning Hall

The turning hall at the centre with a passage on each of its eight points: the three branches' halls north,
north-west and south with their rooms against them, the stirge roost and the corridor of darts on the
diagonals, the stair landing west, the long store east and the hidden strongroom between it and the hall.

```kdl
Design E.a locations="E.1, E.2, E.3, E.4, E.5, E.6, E.7, E.8, E.9, E.10, E.11, E.12, E.13, E.14, E.15" outline="rect 220 220" fill="25-45%" seed=7 approved="2026-11-11"
Layout E.a id=ring arrange=ring entry=E.2 gap=10
Room E.2 layout=ring width=60 length=60 shape=round
Room E.3 layout=ring width=50 length=20 facing=north
Room E.15 layout=ring width=30 length=30 shape=round facing=north-east
Room E.1 layout=ring width=20 length=20 facing=west
Room E.9 layout=ring width=10 length=50 shape=hall facing=south-west
Room E.5 layout=ring width=50 length=20 facing=south
Room E.14 layout=ring width=20 length=20 facing=south-east
Room E.13 layout=ring width=20 length=50 facing=east
Room E.4 layout=ring width=50 length=20 shape=apse facing=north-west
Room E.6 width=20 length=20
Room E.10 width=20 length=20
Room E.7 width=20 length=20
Room E.11 width=20 length=20
Room E.8 width=20 length=20
Room E.12 width=20 length=20
Route E.a ends="E.3:north:e, E.6" kind=door
Route E.a ends="E.3:north:w, E.10" kind=door
Route E.a ends="E.4:north, E.7" kind=door
Route E.a ends="E.4:west, E.11" kind=door
Route E.a ends="E.5:south:w, E.8" kind=door
Route E.a ends="E.5:south:e, E.12" kind=door
Route E.a ends="E.13:south, E.14"
Route E.a ends="E.1, D.6" stair=up
Route E.a ends="E.9:south, F.1" stair=down
Place E.2 xyz="0,10" outline="rect 60 60" shape=round
Place E.3 xyz="-5,60" outline="rect 50 20" shape=rect
Place E.15 xyz="55,65" outline="rect 30 30" shape=round
Place E.1 xyz="-50,10" outline="rect 20 20" shape=rect
Place E.9 xyz="-45,-55" outline="rect 10 50" shape=hall
Place E.5 xyz="-5,-40" outline="rect 50 20" shape=rect
Place E.14 xyz="50,-40" outline="rect 20 20" shape=rect
Place E.13 xyz="50,15" outline="rect 20 50" shape=rect
Place E.4 xyz="-65,60" outline="poly 15,10 18,10 20,9 22,7 24,5 25,3 25,0 25,-3 24,-5 22,-7 20,-9 18,-10 15,-10 -25,-10 -25,10"
Place E.6 xyz="0,80" outline="rect 20 20" shape=rect
Place E.10 xyz="-30,90" outline="rect 20 20" shape=rect
Place E.7 xyz="-60,80" outline="rect 20 20" shape=rect
Place E.11 xyz="-100,60" outline="rect 20 20" shape=rect
Place E.8 xyz="0,-60" outline="rect 20 20" shape=rect
Place E.12 xyz="30,-70" outline="rect 20 20" shape=rect
Link E.1 to="E.2" kind=passage
Link E.13 to="E.14" kind=passage
Link E.2 to="E.13" kind=passage
Link E.2 to="E.14" kind=passage
Link E.2 to="E.15" kind=passage
Link E.2 to="E.3" kind=passage
Link E.2 to="E.4" kind=passage
Link E.2 to="E.5" kind=passage
Link E.2 to="E.9" kind=passage
Link E.3 to="E.10" kind=passage
Link E.3 to="E.6" kind=door
Link E.4 to="E.11" kind=door
Link E.4 to="E.7" kind=door
Link E.5 to="E.12" kind=passage
Link E.5 to="E.8" kind=door
```
