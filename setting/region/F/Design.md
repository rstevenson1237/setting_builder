# Design of F Lemuni

Two villages of stilt-houses either side of a river's mouth with the council house on the nearer bank: a quay runs from the beach past the fish market and the council house to the river trail's head, a lane runs west to the guest house, the net-makers and the headland track, and a path runs up the bluff to the hunters' camp.

```kdl
Design F.a locations="F.9, F.1, F.2, F.3, F.4, F.5, F.6, F.7, F.8, F.10" seed=1 score="100" approved="2026-11-19"
Fill F.a locations="F.9" width=40 length=40
Fill F.a locations="F.1" width=25 length=25
Fill F.a locations="F.2" width=25 length=25
Fill F.a locations="F.3" width=70 length=30
Fill F.a locations="F.4" width=40 length=25
Fill F.a locations="F.5" width=60 length=40
Fill F.a locations="F.6" width=40 length=25
Fill F.a locations="F.7" width=50 length=40
Fill F.a locations="F.8" width=50 length=25
Fill F.a locations="F.10" width=15 length=15
Tie F.a from="F.9" to="F.1" bearing="south" distance="95 yards"
Tie F.a from="F.9" to="F.2" bearing="west" distance="90 yards"
Tie F.a from="F.9" to="F.3" bearing="north" distance="75 yards"
Tie F.a from="F.9" to="F.4" bearing="west-south-west" distance="35 yards"
Tie F.a from="F.9" to="F.5" bearing="north-east" distance="40 yards"
Tie F.a from="F.9" to="F.6" bearing="west" distance="55 yards"
Tie F.a from="F.9" to="F.7" bearing="south-east" distance="85 yards"
Tie F.a from="F.9" to="F.8" bearing="north-west" distance="55 yards"
Tie F.a from="F.9" to="F.10" bearing="south-west" distance="22 yards"
Street F.a past="F.3, F.5, F.9, F.1"
Street F.a past="F.2, F.6, F.4, F.9" kind="lane"
Street F.a past="F.1, F.7" kind="path"
Street F.a past="F.3, F.8" kind="lane"
Fabric F.a kind=house share="40%"
Place F.9 xyz="0,0" outline="rect 40 40" shape=rect
Place F.1 xyz="0,-285" outline="rect 25 25" shape=rect
Place F.2 xyz="-270,0" outline="rect 25 25" shape=rect
Place F.3 xyz="0,225" outline="rect 70 30" shape=rect
Place F.4 xyz="-97,-40" outline="rect 40 25" shape=rect
Place F.5 xyz="85,85" outline="rect 60 40" shape=rect
Place F.6 xyz="-165,0" outline="rect 40 25" shape=rect
Place F.7 xyz="180,-180" outline="rect 50 40" shape=rect
Place F.8 xyz="-117,117" outline="rect 50 25" shape=rect
Place F.10 xyz="-47,-47" outline="rect 15 15" shape=rect
```
