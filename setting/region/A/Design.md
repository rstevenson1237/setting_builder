# Design of A The Drifted Streets

A gridded city under the sand, the three statues at its centre: one processional way runs north and south
through them from the barracks to the scouts' camp, a cross street runs east from the dry canal to the
market, and two side streets run past the ruins west and east of them.

```kdl
Design A.a locations="A.1, A.2, A.3, A.4, A.5, A.6, A.7, A.8, A.9" seed=1 score="70" approved="2026-11-18"
Fill A.a locations="A.1" width=40 length=40
Fill A.a locations="A.2" width=30 length=25
Fill A.a locations="A.3" width=40 length=40
Fill A.a locations="A.4" width=90 length=70
Fill A.a locations="A.5" width=120 length=25
Fill A.a locations="A.6" width=100 length=50
Fill A.a locations="A.7" width=70 length=60
Fill A.a locations="A.8" width=150 length=20
Fill A.a locations="A.9" width=20 length=15
Tie A.a from="A.1" to="A.2" bearing="south-west" distance="120 yards"
Tie A.a from="A.1" to="A.3" bearing="north-west" distance="200 yards"
Tie A.a from="A.1" to="A.4" bearing="east" distance="180 yards"
Tie A.a from="A.1" to="A.5" bearing="north" distance="300 yards"
Tie A.a from="A.1" to="A.6" bearing="south-east" distance="250 yards"
Tie A.a from="A.1" to="A.7" bearing="south" distance="330 yards"
Tie A.a from="A.1" to="A.8" bearing="west" distance="150 yards"
Street A.a past="A.5, A.1, A.7"
Street A.a past="A.8, A.4"
Street A.a past="A.3, A.2"
Fabric A.a kind=ruin share="40%"
Place A.1 xyz="0,0" outline="rect 40 40" shape=rect
Place A.2 xyz="-255,-255" outline="rect 30 25" shape=rect
Place A.3 xyz="-424,424" outline="rect 40 40" shape=rect
Place A.4 xyz="540,0" outline="rect 90 70" shape=rect
Place A.5 xyz="0,900" outline="rect 120 25" shape=rect
Place A.6 xyz="530,-530" outline="rect 100 50" shape=rect
Place A.7 xyz="0,-990" outline="rect 70 60" shape=rect
Place A.8 xyz="-450,0" outline="rect 150 20" shape=rect
Place A.9 xyz="-289,-338" outline="rect 20 15" shape=rect
```
