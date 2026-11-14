# Design of G Pyramid Level 5 - The Funerary Level

The rooms where the packing set them, the level moved to stand under the stair gallery above: the long hall of
niches off the landing, the octagonal tombs of the king and queen and the false tomb round the royal antechamber,
the round rites hall, the chapel of the sun and the wells, and the lake path out east to the lake city.

```kdl
Design G.a locations="G.1, G.2, G.3, G.4, G.5, G.6, G.7, G.8, G.9, G.10, G.11, G.12, G.13, G.14, G.15, G.16, G.17, G.18, G.19, G.20, G.21, G.22, G.23, G.24, G.25, G.26, G.27, G.28, G.29" outline="poly -200,170 60,170 60,-120 -200,-120" seed=1 approved="2026-11-11"
Room G.1 width=10 length=20 shape=hall xyz="-105,-5"
Room G.2 width=50 length=20 xyz="-105,15"
Room G.3 width=30 length=40 xyz="-135,-15"
Room G.4 width=30 length=30 xyz="-165,100"
Room G.5 width=20 length=20 xyz="-20,-85"
Room G.6 width=40 length=40 xyz="-30,65"
Room G.7 width=30 length=30 xyz="-65,40" shape=octagon
Room G.8 width=30 length=30 xyz="-5,30" shape=octagon
Room G.9 width=30 length=30 xyz="-65,70" shape=octagon
Room G.10 width=20 length=20 xyz="-90,35"
Room G.11 width=20 length=30 xyz="-90,-50"
Room G.12 width=30 length=30 shape=octagon xyz="25,20"
Room G.13 width=30 length=50 xyz="-5,-10"
Room G.14 width=10 length=60 shape=hall xyz="-85,115"
Room G.15 width=40 length=40 xyz="-130,125" shape=round
Room G.16 width=10 length=50 shape=hall xyz="15,120"
Room G.17 width=40 length=30 xyz="20,80" shape=apse
Room G.18 width=30 length=20 xyz="-75,-75"
Room G.19 width=10 length=30 shape=hall xyz="15,50"
Room G.20 width=40 length=50 xyz="-120,80"
Room G.21 width=20 length=10 shape=hall xyz="-90,80"
Room G.22 width=40 length=40 shape=octagon xyz="-20,-55"
Room G.23 width=30 length=20 xyz="-55,-45"
Room G.24 width=40 length=10 shape=hall xyz="-80,-30"
Room G.25 width=20 length=20 xyz="-110,-25"
Room G.26 width=30 length=30 xyz="-55,10"
Room G.27 width=20 length=20 xyz="-40,35"
Room G.28 width=20 length=30 xyz="-150,70"
Room G.29 width=20 length=20 xyz="-90,65"
Route G.a ends="G.1, G.2" kind=door
Route G.a ends="G.1, F.13" stair=up
Route G.a ends="G.2, G.3" kind=door
Route G.a ends="G.2, G.13"
Route G.a ends="G.2, G.4"
Route G.a ends="G.3, G.11"
Route G.a ends="G.4, G.15" kind=door
Route G.a ends="G.5, G.13"
Route G.a ends="G.5, G.18"
Route G.a ends="G.6, G.13"
Route G.a ends="G.6, G.9" kind=door
Route G.a ends="G.6, G.7" kind=door
Route G.a ends="G.6, G.8" kind=door
Route G.a ends="G.7, G.10" kind=door
Route G.a ends="G.8, G.19" kind=door
Route G.a ends="G.11, G.18" kind=door
Route G.a ends="G.12, G.13"
Route G.a ends="G.12, G.16"
Route G.a ends="G.14, B.1" stair=down
Route G.a ends="G.15, G.16"
Route G.a ends="G.16, G.17" kind=door
Route G.a ends="G.17, G.19" kind=door
Route G.a ends="G.19:north, H.1" stair=down
Route G.a ends="G.13, G.22"
Route G.a ends="G.22, G.5" kind=door
Route G.a ends="G.22, G.23"
Route G.a ends="G.23, G.24" kind=door
Route G.a ends="G.24, G.11" kind=door
Route G.a ends="G.24, G.25" kind=door
Route G.a ends="G.6, G.27" kind=door
Route G.a ends="G.27, G.26" kind=door
Route G.a ends="G.4, G.28" kind=door
Route G.a ends="G.28, G.20" kind=door
Route G.a ends="G.20, G.15" kind=door
Route G.a ends="G.20, G.21" kind=door
Route G.a ends="G.21, G.29" kind=door
Route G.a ends="G.21, G.14" kind=door
Place G.1 xyz="-105,0" outline="rect 10 20" shape=hall
Place G.2 xyz="-105,20" outline="rect 50 20" shape=rect
Place G.3 xyz="-135,-10" outline="rect 30 40" shape=rect
Place G.4 xyz="-165,95" outline="rect 30 30" shape=rect
Place G.5 xyz="-20,-80" outline="rect 20 20" shape=rect
Place G.6 xyz="-30,70" outline="rect 40 40" shape=rect
Place G.7 xyz="-65,35" outline="rect 30 30" shape=octagon
Place G.8 xyz="-5,35" outline="rect 30 30" shape=octagon
Place G.9 xyz="-65,75" outline="rect 30 30" shape=octagon
Place G.10 xyz="-90,40" outline="rect 20 20" shape=rect
Place G.11 xyz="-90,-45" outline="rect 20 30" shape=rect
Place G.12 xyz="25,15" outline="rect 30 30" shape=octagon
Place G.13 xyz="-5,-15" outline="rect 30 50" shape=rect
Place G.14 xyz="-85,120" outline="rect 10 60" shape=hall
Place G.15 xyz="-130,130" outline="rect 40 40" shape=round
Place G.16 xyz="15,125" outline="rect 10 50" shape=hall
Place G.17 xyz="20,75" outline="poly 5,15 9,14 12,13 16,11 18,7 19,4 20,0 19,-4 18,-8 16,-11 12,-13 9,-14 5,-15 -20,-15 -20,15"
Place G.18 xyz="-75,-80" outline="rect 30 20" shape=rect
Place G.19 xyz="15,45" outline="rect 10 30" shape=hall
Place G.20 xyz="-120,85" outline="rect 40 50" shape=rect
Place G.21 xyz="-90,85" outline="rect 20 10" shape=hall
Place G.22 xyz="-40,-50" outline="rect 40 40" shape=octagon
Place G.23 xyz="-55,-20" outline="rect 30 20" shape=rect
Place G.24 xyz="-90,-25" outline="rect 40 10" shape=hall
Place G.25 xyz="-110,-40" outline="rect 20 20" shape=rect
Place G.26 xyz="-55,5" outline="rect 30 30" shape=rect
Place G.27 xyz="-40,40" outline="rect 20 20" shape=rect
Place G.28 xyz="-150,65" outline="rect 20 30" shape=rect
Place G.29 xyz="-90,60" outline="rect 20 20" shape=rect
Link G.1 to="G.2" kind=door
Link G.11 to="G.18" kind=passage
Link G.11 to="G.24" kind=door
Link G.12 to="G.13" kind=passage
Link G.12 to="G.16" kind=passage
Link G.13 to="G.22" kind=passage
Link G.14 to="G.21" kind=door
Link G.15 to="G.16" kind=passage
Link G.15 to="G.20" kind=passage
Link G.16 to="G.17" kind=passage
Link G.17 to="G.19" kind=door
Link G.2 to="G.13" kind=passage
Link G.2 to="G.3" kind=door
Link G.2 to="G.4" kind=passage
Link G.20 to="G.21" kind=door
Link G.20 to="G.28" kind=door
Link G.21 to="G.29" kind=passage
Link G.22 to="G.23" kind=passage
Link G.23 to="G.24" kind=door
Link G.24 to="G.25" kind=door
Link G.26 to="G.27" kind=passage
Link G.3 to="G.11" kind=passage
Link G.4 to="G.15" kind=passage
Link G.4 to="G.28" kind=door
Link G.5 to="G.13" kind=passage
Link G.5 to="G.18" kind=passage
Link G.5 to="G.22" kind=passage
Link G.6 to="G.13" kind=passage
Link G.6 to="G.27" kind=door
Link G.6 to="G.7" kind=passage
Link G.6 to="G.8" kind=passage
Link G.6 to="G.9" kind=door
Link G.7 to="G.10" kind=door
Link G.8 to="G.19" kind=door
```
