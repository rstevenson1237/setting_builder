# Design of F Lemuni

Two villages of stilt-houses either side of a river's mouth with the council house on the nearer bank: a quay runs from the beach past the fish market and the council house to the river trail's head, a lane runs west to the guest house, the net-makers and the headland track, and a path runs up the bluff to the hunters' camp.

```kdl
Design F.a locations="F.9, F.1, F.2, F.3, F.4, F.5, F.6, F.7, F.8, F.10"
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
```
