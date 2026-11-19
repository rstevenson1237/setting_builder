# Design of A Puluni

Three stockaded villages behind the great wall. Puluni, the largest, stands at the lagoon's head round the chiefs' house: the beach and the market on the lagoon side to the west, the ancestor house and the guest house beside the beach, and a street east past the chiefs' house to the watch house. Naloni, the canoe-makers' and guides' village, stands two miles south along the lagoon, its yard on the shore and the guides' hall behind it. Tiwani, the fishers' village, stands on the east coast round the fish stores.

```kdl
Design A.a locations="A.10, A.2, A.4, A.5, A.9, A.11, A.12"
Fill A.a locations="A.10" width=50 length=40
Fill A.a locations="A.2" width=40 length=80
Fill A.a locations="A.4" width=40 length=30
Fill A.a locations="A.5" width=70 length=50
Fill A.a locations="A.9" width=30 length=20
Fill A.a locations="A.11" width=40 length=30
Fill A.a locations="A.12" width=15 length=15
Tie A.a from="A.10" to="A.2" bearing="west" distance="80 yards"
Tie A.a from="A.10" to="A.5" bearing="west" distance="40 yards"
Tie A.a from="A.10" to="A.4" bearing="south-west" distance="55 yards"
Tie A.a from="A.10" to="A.9" bearing="north-west" distance="50 yards"
Tie A.a from="A.10" to="A.11" bearing="east" distance="45 yards"
Tie A.a from="A.10" to="A.12" bearing="north-west" distance="22 yards"
Street A.a past="A.2, A.5, A.10, A.11"
Street A.a past="A.5, A.9" kind="lane"
Street A.a past="A.5, A.4" kind="lane"
Fabric A.a kind=house share="40%"
Design A.b locations="A.6, A.7"
Fill A.b locations="A.6" width=60 length=40
Fill A.b locations="A.7" width=40 length=25
Tie A.b from="A.6" to="A.7" bearing="east" distance="40 yards"
Street A.b past="A.6, A.7"
Fabric A.b kind=house share="40%"
Design A.c locations="A.8"
Fill A.c locations="A.8" width=40 length=30
Street A.c past="A.8"
Fabric A.c kind=house share="50%"
```
