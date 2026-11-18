# Design of B Zamiun

A city round a still lake, its gate at the centre: a quay runs round the lake's north and east shore past the
gardens, the walk and the market, a street runs north from the gate to the quarters and the revel house, and a
lane runs west to the old granary and the loft behind it.

```kdl
Design B.a locations="B.1, B.2, B.3, B.4, B.5, B.6, B.7, B.8, B.9, B.10" seed=9 score="80"
Fill B.a locations="B.1" width=40 length=25
Fill B.a locations="B.2" width=110 length=40
Fill B.a locations="B.3" width=80 length=60
Fill B.a locations="B.4" width=100 length=50
Fill B.a locations="B.5" width=70 length=50
Fill B.a locations="B.6" width=120 length=80
Fill B.a locations="B.7" width=220 length=170
Fill B.a locations="B.8" width=120 length=20
Fill B.a locations="B.9" width=25 length=20
Fill B.a locations="B.10" width=15 length=15
Tie B.a from="B.1" to="B.2" bearing="north" distance="80 yards"
Tie B.a from="B.1" to="B.3" bearing="east" distance="100 yards"
Tie B.a from="B.1" to="B.4" bearing="north-east" distance="140 yards"
Tie B.a from="B.1" to="B.5" bearing="west" distance="120 yards"
Tie B.a from="B.1" to="B.6" bearing="south-west" distance="150 yards"
Tie B.a from="B.1" to="B.7" bearing="south" distance="70 yards"
Tie B.a from="B.1" to="B.8" bearing="south-east" distance="110 yards"
Street B.a past="B.6, B.7, B.8, B.3"
Street B.a past="B.1, B.2, B.4"
Street B.a past="B.5, B.9" kind="lane"
Fabric B.a kind=house share="30%"
Place B.1 xyz="0,0" outline="rect 40 25" shape=rect
Place B.2 xyz="0,240" outline="rect 110 40" shape=rect
Place B.3 xyz="300,0" outline="rect 80 60" shape=rect
Place B.4 xyz="297,297" outline="rect 100 50" shape=rect
Place B.5 xyz="-360,0" outline="rect 70 50" shape=rect
Place B.6 xyz="-318,-318" outline="rect 120 80" shape=rect
Place B.7 xyz="0,-210" outline="rect 220 170" shape=rect
Place B.8 xyz="233,-233" outline="rect 120 20" shape=rect
Place B.9 xyz="-406,111" outline="rect 25 20" shape=rect
Place B.10 xyz="-269,-219" outline="rect 15 15" shape=rect
```
