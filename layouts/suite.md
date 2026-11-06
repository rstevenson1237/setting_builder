# Suite

A room with a smaller room off it, numbered with it: a chamber and its closet, a hall and its alcove.

```kdl
Layout suite name="A room and its sub-room" tags="suite, chamber, alcove" source="drawn from maps 1 and 2"
Part role=main width="20-30" length="20-30"
Part role=sub width="10-15" length="10-15" at="main east"
Tie a=main b=sub kind=door
Socket name=door part=main bearing=south width=5
Socket name=back part=main bearing=north width=5
```
