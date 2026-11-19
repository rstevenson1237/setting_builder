# Design of A Puluni

The largest of the three stockaded villages at the lagoon's head, the chiefs' house at its centre: a street runs north from the beach past the market, the chiefs' house and the watch house to the great gate in the wall, a lane runs east to the fish stores, and a lane runs west to the guest house and the guides' hall, with the canoe yard on the shore and the wall's east end beyond the gate.

```kdl
Design A.a locations="A.10, A.1, A.2, A.3, A.4, A.5, A.6, A.7, A.8, A.9, A.11, A.12"
Fill A.a locations="A.10" width=50 length=40
Fill A.a locations="A.1" width=30 length=30
Fill A.a locations="A.2" width=80 length=40
Fill A.a locations="A.3" width=30 length=30
Fill A.a locations="A.4" width=40 length=30
Fill A.a locations="A.5" width=70 length=50
Fill A.a locations="A.6" width=60 length=40
Fill A.a locations="A.7" width=40 length=25
Fill A.a locations="A.8" width=40 length=30
Fill A.a locations="A.9" width=20 length=20
Fill A.a locations="A.11" width=40 length=30
Fill A.a locations="A.12" width=15 length=15
Tie A.a from="A.10" to="A.1" bearing="north" distance="90 yards"
Tie A.a from="A.10" to="A.2" bearing="south" distance="80 yards"
Tie A.a from="A.10" to="A.3" bearing="north-east" distance="110 yards"
Tie A.a from="A.10" to="A.4" bearing="west" distance="45 yards"
Tie A.a from="A.10" to="A.5" bearing="south-east" distance="50 yards"
Tie A.a from="A.10" to="A.6" bearing="south-south-west" distance="75 yards"
Tie A.a from="A.10" to="A.7" bearing="west-south-west" distance="65 yards"
Tie A.a from="A.10" to="A.8" bearing="east" distance="60 yards"
Tie A.a from="A.10" to="A.9" bearing="south" distance="30 yards"
Tie A.a from="A.10" to="A.11" bearing="north" distance="45 yards"
Tie A.a from="A.10" to="A.12" bearing="north-west" distance="22 yards"
Street A.a past="A.2, A.5, A.10, A.11, A.1"
Street A.a past="A.7, A.4, A.10, A.8" kind="lane"
Street A.a past="A.6, A.2" kind="lane"
Street A.a past="A.1, A.3" kind="lane"
Fabric A.a kind=house share="40%"
```
