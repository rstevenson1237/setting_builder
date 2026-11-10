# Design of E Pyramid Level 3 - The Turning Hall

```kdl
Design E.a locations="E.1, E.2, E.3, E.4, E.5, E.6, E.7, E.8, E.9, E.10, E.11, E.12, E.13, E.14, E.15" outline="rect 140 140" seed=7 score="100"
Use E.a id=ring layout=spine-ring-hub params="spine=10 ring=8"
Use E.a id=guard layout=cell-row params="per-row=1"
Use E.a id=temple layout=cell-row params="per-row=1"
Use E.a id=scholars layout=cell-row params="per-row=1"
Bind E.a use=ring role=hub locations="E.2" type=High
Bind E.a use=ring role=spine locations="E.9" type=Medium
Bind E.a use=guard role=hall locations="E.3" type=High
Bind E.a use=guard role=north-cell locations="E.6" type=Medium
Bind E.a use=guard role=south-cell locations="E.10" type=Low
Bind E.a use=temple role=hall locations="E.4" type=Medium
Bind E.a use=temple role=north-cell locations="E.7" type=Medium
Bind E.a use=temple role=south-cell locations="E.11" type=Low
Bind E.a use=scholars role=hall locations="E.5" type=Medium
Bind E.a use=scholars role=north-cell locations="E.8" type=Medium
Bind E.a use=scholars role=south-cell locations="E.12" type=Low
Fill E.a locations="E.1" type=Low width=20 length=20
Fill E.a locations="E.13" type=Medium width=20 length=50
Fill E.a locations="E.14" type=Low width=20 length=20
Fill E.a locations="E.15" type=High width=30 length=30
Join E.a from="ring.hub-n" to="E.3"
Join E.a from="ring.hub-nw" to="E.4"
Join E.a from="ring.hub-s" to="E.5"
Join E.a from="ring.hub-ne" to="E.15"
Join E.a from="ring.hub-se" to="E.9"
Join E.a from="ring.hub-e" to="E.1"
Join E.a from="ring.hub-w" to="E.13"
Join E.a from="ring.hub-sw" to="E.14"
Join E.a from="E.13" to="E.14"
Place E.1 xyz="50,-10" outline="rect 20 20" shape=rect
Place E.2 xyz="-10,0" outline="rect 60 60" shape=round
Place E.3 xyz="25,60" outline="rect 50 20" shape=rect
Place E.4 xyz="-45,60" outline="rect 50 20" shape=rect
Place E.5 xyz="-25,-60" outline="rect 50 20" shape=rect
Place E.6 xyz="60,60" outline="rect 20 20" shape=rect
Place E.7 xyz="-10,60" outline="rect 20 20" shape=rect
Place E.8 xyz="0,-40" outline="rect 20 20" shape=rect
Place E.9 xyz="35,-35" outline="rect 10 50" shape=hall
Place E.10 xyz="50,40" outline="rect 20 20" shape=rect
Place E.11 xyz="-20,40" outline="rect 20 20" shape=rect
Place E.12 xyz="10,-60" outline="rect 20 20" shape=rect
Place E.13 xyz="-60,-5" outline="rect 20 50" shape=rect
Place E.14 xyz="-60,-60" outline="rect 20 20" shape=rect
Place E.15 xyz="55,15" outline="rect 30 30" shape=rect
Link E.1 to="E.2" kind=passage
Link E.2 to="E.3" kind=passage
Link E.2 to="E.4" kind=passage
Link E.2 to="E.5" kind=passage
Link E.2 to="E.9" kind=passage
Link E.2 to="E.13" kind=passage
Link E.2 to="E.14" kind=passage
Link E.2 to="E.15" kind=passage
Link E.3 to="E.6" kind=door
Link E.3 to="E.10" kind=door
Link E.4 to="E.7" kind=door
Link E.4 to="E.11" kind=door
Link E.5 to="E.8" kind=door
Link E.5 to="E.12" kind=door
Link E.13 to="E.14" kind=passage
```
