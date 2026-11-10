# Three routes

A small room with three ways out that meet again in one wide hall: two the caller makes, and between
them a wide straight lane.

```kdl
Layout three-routes name="Three routes to a wide hall" tags="routes, branching, hall, converging" source="written"
Part role=start shape=octagon width="20" length="20"
Part role=lane shape=hall width="20" length="80" at="start south"
Part role=hall width="80" length="40" at="lane south" focal=focal
Tie a=start b=lane kind=passage
Tie a=lane b=hall kind=passage
Socket name=sw part=start bearing=south-west width=10
Socket name=se part=start bearing=south-east width=10
Socket name=nw part=hall bearing=north-west width=10
Socket name=ne part=hall bearing=north-east width=10
Socket name=s part=hall bearing=south width=10
```
