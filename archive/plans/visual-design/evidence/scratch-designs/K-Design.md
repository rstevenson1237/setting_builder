# Design of K

```kdl
Design K.a locations="K.1, K.2, K.3, K.4, K.5, K.6, K.7, K.8" outline="rect 100 100" fill="20-55%" spacing="10-30 feet" seed=1 score="95"
Use K.a id=v1 layout=stair-vestibule
Use K.a id=v2 layout=stair-vestibule
Use K.a id=ring layout=spine-ring-hub params="spine=40 ring=40"
Bind K.a use=v1 role=vestibule locations="K.1" type=Low
Bind K.a use=v2 role=vestibule locations="K.5" type=High
Bind K.a use=ring role=hub locations="K.2" type=Medium
Bind K.a use=ring role=spine locations="K.4" type=Medium
Fill K.a locations="K.3" type=High width=20 length=20
Fill K.a locations="K.6" type=Medium width=20 length=20
Fill K.a locations="K.7" type=Low width=20 length=20
Fill K.a locations="K.8" type=High width=20 length=20
Join K.a from="ring.hub-n" to="K.1"
Join K.a from="ring.hub-e" to="K.3"
Join K.a from="ring.hub-s" to="K.5"
Join K.a from="ring.hub-w" to="K.6"
Join K.a from="K.6" to="K.7"
Join K.a from="K.3" to="K.8"
Place K.1 xyz="-25,15" outline="rect 10 10" shape=rect
Place K.2 xyz="-20,-10" outline="rect 40 40" shape=round
Place K.3 xyz="30,20" outline="rect 20 20" shape=rect
Place K.4 xyz="25,-10" outline="rect 10 40" shape=hall
Place K.5 xyz="45,5" outline="rect 10 10" shape=rect
Place K.6 xyz="-40,40" outline="rect 20 20" shape=rect
Place K.7 xyz="-20,30" outline="rect 20 20" shape=rect
Place K.8 xyz="10,10" outline="rect 20 20" shape=rect
Link K.1 to="K.2" kind=passage
Link K.2 to="K.3" kind=passage
Link K.2 to="K.4" kind=passage
Link K.2 to="K.5" kind=passage
Link K.2 to="K.6" kind=passage
Link K.3 to="K.8" kind=door
Link K.6 to="K.7" kind=door
```
