# Design of I

```kdl
Design I.a locations="I.1, I.2, I.3, I.4, I.5, I.6, I.7, I.8, I.9, I.10, I.11, I.12, I.13, I.14" spacing="10-30 feet" seed=20 score="95" hull="poly -60,20 -50,-40 -20,-60 20,-60 50,-40 50,50 40,60 -50,60 -60,40"
Use I.a id=ring layout=spine-ring-hub
Use I.a id=row layout=cell-row params="per-row=2"
Use I.a id=ste layout=suite
Use I.a id=byp layout=secret-bypass
Bind I.a use=ring role=spine locations="I.1" type=Low
Bind I.a use=ring role=hub locations="I.2" type=Medium
Bind I.a use=row role=hall locations="I.3" type=High
Bind I.a use=row role=north-cell locations="I.4, I.5" type=Medium
Bind I.a use=row role=south-cell locations="I.7, I.13" type=Medium
Bind I.a use=ste role=main locations="I.8" type=Medium
Bind I.a use=ste role=sub locations="I.9" type=High
Bind I.a use=byp role=near locations="I.10" type=Medium
Bind I.a use=byp role=far locations="I.11" type=Medium
Bind I.a use=byp role=bypass locations="I.12" type=Low
Fill I.a locations="I.6" type=Low width=20 length=20
Fill I.a locations="I.14" type=Low width=20 length=20
Join I.a from="ring.hub-n" to="I.3"
Join I.a from="ring.hub-e" to="I.8"
Join I.a from="ring.hub-w" to="I.10"
Join I.a from="ring.hub-s" to="I.6"
Join I.a from="I.6" to="I.14"
Join I.a from="I.14" to="I.11"
Place I.1 xyz="45,0" outline="rect 10 80" shape=hall
Place I.2 xyz="5,-5" outline="rect 30 30" shape=round
Place I.3 xyz="-35,30" outline="rect 50 20" shape=rect
Place I.4 xyz="-40,50" outline="rect 20 20" shape=rect
Place I.5 xyz="-20,50" outline="rect 20 20" shape=rect
Place I.6 xyz="10,-50" outline="rect 20 20" shape=rect
Place I.7 xyz="-40,10" outline="rect 20 20" shape=rect
Place I.8 xyz="25,45" outline="rect 30 30" shape=rect
Place I.9 xyz="45,45" outline="rect 10 10" shape=rect
Place I.10 xyz="-40,-30" outline="rect 20 20" shape=rect
Place I.11 xyz="-10,-30" outline="rect 20 20" shape=rect
Place I.12 xyz="-25,-15" outline="rect 30 10" shape=hall
Place I.13 xyz="-20,10" outline="rect 20 20" shape=rect
Place I.14 xyz="-10,-50" outline="rect 20 20" shape=rect
Link I.1 to="I.2" kind=passage
Link I.2 to="I.3" kind=passage
Link I.2 to="I.6" kind=passage
Link I.2 to="I.8" kind=passage
Link I.2 to="I.10" kind=passage
Link I.3 to="I.4" kind=door
Link I.3 to="I.5" kind=door
Link I.3 to="I.7" kind=door
Link I.3 to="I.13" kind=door
Link I.6 to="I.14" kind=door
Link I.8 to="I.9" kind=door
Link I.10 to="I.12" kind=door
Link I.11 to="I.12" kind=door
Link I.11 to="I.14" kind=door
```
