# Design of J

```kdl
Design J.a locations="J.1, J.2, J.3, J.4, J.5, J.6, J.7, J.8, J.9" outline="rect 100 100" spacing="10-30 feet" seed=7 score="95"
Use J.a id=v1 layout=stair-vestibule
Use J.a id=v2 layout=stair-vestibule
Use J.a id=ste layout=suite
Use J.a id=row layout=cell-row params="per-row=1"
Bind J.a use=v1 role=vestibule locations="J.1" type=Low
Bind J.a use=v2 role=vestibule locations="J.6" type=High
Bind J.a use=ste role=main locations="J.2" type=High
Bind J.a use=ste role=sub locations="J.9" type=High
Bind J.a use=row role=hall locations="J.3" type=Medium
Bind J.a use=row role=north-cell locations="J.4" type=Medium
Bind J.a use=row role=south-cell locations="J.5" type=Medium
Fill J.a locations="J.7" type=Medium width=20 length=20
Fill J.a locations="J.8" type=Low width=20 length=20
Join J.a from="J.1" to="J.3"
Join J.a from="J.2" to="J.3"
Join J.a from="J.3" to="J.7"
Join J.a from="J.7" to="J.6"
Join J.a from="J.8" to="J.2"
Place J.1 xyz="15,-15" outline="rect 10 10" shape=rect
Place J.2 xyz="15,5" outline="rect 30 30" shape=rect
Place J.3 xyz="-15,-20" outline="rect 50 20" shape=rect
Place J.4 xyz="-10,0" outline="rect 20 20" shape=rect
Place J.5 xyz="-10,-40" outline="rect 20 20" shape=rect
Place J.6 xyz="-25,15" outline="rect 10 10" shape=rect
Place J.7 xyz="-30,0" outline="rect 20 20" shape=rect
Place J.8 xyz="40,-10" outline="rect 20 20" shape=rect
Place J.9 xyz="35,5" outline="rect 10 10" shape=rect
Link J.1 to="J.3" kind=door
Link J.2 to="J.3" kind=door
Link J.2 to="J.8" kind=door
Link J.2 to="J.9" kind=door
Link J.3 to="J.4" kind=door
Link J.3 to="J.5" kind=door
Link J.3 to="J.7" kind=door
Link J.6 to="J.7" kind=door
```
