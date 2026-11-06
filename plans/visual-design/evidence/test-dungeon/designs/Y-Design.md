# Design of Y

```kdl
Design Y.a locations="Y.1, Y.2, Y.3, Y.4, Y.5, Y.6, Y.7, Y.8, Y.9, Y.10, Y.11, Y.12, Y.13, Y.14, Y.15, Y.16, Y.17, Y.18, Y.19, Y.20, Y.21, Y.22, Y.23, Y.24, Y.25, Y.26, Y.27" outline="rect 320 320" spacing="20-40 feet" pad="10 feet" fill="25-55%" seed=11 score="85"
Use Y.a id=tr layout=three-routes
Use Y.a id=tl layout=twin-loop
Use Y.a id=blk layout=dense-block
Bind Y.a use=tr role=start locations="Y.1" type=Low
Bind Y.a use=tr role=lane locations="Y.2" type=Medium
Bind Y.a use=tr role=hall locations="Y.3" type=High
Bind Y.a use=tl role=gate locations="Y.10" type=Medium
Bind Y.a use=tl role=left locations="Y.11, Y.12, Y.13" type="Low, Medium, Low"
Bind Y.a use=tl role=right locations="Y.14, Y.15, Y.16" type="Low, High, Low"
Bind Y.a use=blk role=hall locations="Y.17" type=Medium pad="0 feet"
Bind Y.a use=blk role=north-cell locations="Y.18, Y.19, Y.20" type="Low, Medium, High" pad="0 feet"
Bind Y.a use=blk role=south-cell locations="Y.21, Y.22, Y.23" type="Low, Medium, High" pad="0 feet"
Fill Y.a locations="Y.4" type=Low width=40 length=30 outline="poly -20,-10 -10,-15 10,-15 20,0 10,15 -20,15"
Fill Y.a locations="Y.5" type=Medium width=30 length=30 outline="poly -15,-15 5,-15 15,-5 15,15 -5,15 -15,5"
Fill Y.a locations="Y.6" type=Low width=40 length=20 outline="poly -20,-10 0,-10 20,0 10,10 -10,10"
Fill Y.a locations="Y.7" type=Low width=30 length=30 shape=round
Fill Y.a locations="Y.8" type=Medium width=40 length=30 shape=hexagon
Fill Y.a locations="Y.9" type=Low width=20 length=20 shape=round
Fill Y.a locations="Y.24" type=Low width=20 length=20 outline="poly -10,-10 10,-10 10,0 0,10 -10,10"
Fill Y.a locations="Y.25" type=Low width=20 length=20 outline="poly -10,-10 0,-10 10,0 10,10 -10,10"
Fill Y.a locations="Y.26" type=Low width=20 length=20 outline="poly -10,-10 10,-10 10,10 -5,10 -10,5"
Fill Y.a locations="Y.27" type=Medium width=20 length=20 outline="poly -10,0 0,-10 10,0 0,10"
Join Y.a from="tr.sw" to="Y.4"
Join Y.a from="Y.4" to="Y.5"
Join Y.a from="Y.5" to="Y.6"
Join Y.a from="Y.6" to="tr.nw"
Join Y.a from="tr.se" to="Y.7"
Join Y.a from="Y.7" to="Y.8"
Join Y.a from="Y.8" to="Y.9"
Join Y.a from="Y.9" to="tr.ne"
Join Y.a from="tr.s" to="tl.in"
Join Y.a from="tl.core" to="blk.north"
Join Y.a from="Y.11" to="Y.24"
Join Y.a from="Y.13" to="Y.25"
Join Y.a from="Y.14" to="Y.26"
Join Y.a from="Y.16" to="Y.27"
Place Y.1 xyz="60,80" outline="rect 20 20" shape=octagon
Place Y.2 xyz="80,-10" outline="rect 20 80" shape=hall
Place Y.3 xyz="-70,110" outline="rect 80 40" shape=rect
Place Y.4 xyz="20,65" outline="poly -20,15 10,15 20,0 10,-15 -10,-15 -20,-10" shape=rect
Place Y.5 xyz="-15,65" outline="poly -15,5 -5,15 15,15 15,-5 5,-15 -15,-15" shape=rect
Place Y.6 xyz="-50,70" outline="poly 20,-10 0,-10 -20,0 -10,10 10,10" shape=rect
Place Y.7 xyz="125,45" outline="rect 30 30" shape=round
Place Y.8 xyz="100,115" outline="rect 40 30" shape=hexagon
Place Y.9 xyz="20,100" outline="rect 20 20" shape=round
Place Y.10 xyz="-25,25" outline="rect 30 30" shape=round
Place Y.11 xyz="40,0" outline="rect 20 20" shape=octagon
Place Y.12 xyz="40,-40" outline="rect 20 20" shape=octagon
Place Y.13 xyz="40,-80" outline="rect 20 20" shape=octagon
Place Y.14 xyz="-20,-60" outline="rect 20 20" shape=hexagon
Place Y.15 xyz="-60,-80" outline="rect 20 20" shape=hexagon
Place Y.16 xyz="0,-100" outline="rect 20 20" shape=hexagon
Place Y.17 xyz="-70,-35" outline="rect 60 10" shape=rect
Place Y.18 xyz="-60,-20" outline="rect 20 20" shape=rect
Place Y.19 xyz="-30,-30" outline="rect 20 20" shape=rect
Place Y.20 xyz="-90,-20" outline="rect 20 20" shape=rect
Place Y.21 xyz="-110,-40" outline="rect 20 20" shape=rect
Place Y.22 xyz="-80,-50" outline="rect 20 20" shape=rect
Place Y.23 xyz="-50,-50" outline="rect 20 20" shape=rect
Place Y.24 xyz="10,10" outline="poly 10,-10 0,-10 -10,0 -10,10 10,10" shape=rect
Place Y.25 xyz="70,-70" outline="poly 10,-10 0,-10 -10,0 -10,10 10,10" shape=rect
Place Y.26 xyz="10,-50" outline="poly -10,-10 -10,10 10,10 10,-5 5,-10" shape=rect
Place Y.27 xyz="10,-70" outline="poly 0,10 10,0 0,-10 -10,0" shape=rect
Link Y.1 to="Y.2" kind=passage
Link Y.1 to="Y.4" kind=passage
Link Y.1 to="Y.7" kind=passage
Link Y.2 to="Y.3" kind=passage
Link Y.3 to="Y.6" kind=passage
Link Y.3 to="Y.9" kind=passage
Link Y.3 to="Y.10" kind=passage
Link Y.4 to="Y.5" kind=door
Link Y.5 to="Y.6" kind=door
Link Y.7 to="Y.8" kind=passage
Link Y.8 to="Y.9" kind=passage
Link Y.10 to="Y.11" kind=passage
Link Y.10 to="Y.14" kind=passage
Link Y.10 to="Y.17" kind=passage
Link Y.11 to="Y.12" kind=passage
Link Y.11 to="Y.24" kind=passage
Link Y.12 to="Y.13" kind=passage
Link Y.13 to="Y.16" kind=passage
Link Y.13 to="Y.25" kind=passage
Link Y.14 to="Y.15" kind=passage
Link Y.14 to="Y.26" kind=passage
Link Y.15 to="Y.16" kind=passage
Link Y.16 to="Y.27" kind=passage
Link Y.17 to="Y.18" kind=door
Link Y.17 to="Y.19" kind=door
Link Y.17 to="Y.20" kind=door
Link Y.17 to="Y.21" kind=door
Link Y.17 to="Y.22" kind=door
Link Y.17 to="Y.23" kind=door
```
