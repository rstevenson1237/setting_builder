# Spine and ring hub

One long corridor the full height of the block crossing a ring chamber with a door on each of its
eight points: where every way of a level turns.

```kdl
Layout spine-ring-hub name="A spine through a ring hub" tags="hub, spine, axial, turning" source="drawn from map 2"
Param name=spine range="70-120"
Param name=ring range="20-30"
Part role=spine shape=hall width="10" length=spine
Part role=hub shape=round width=ring length=ring focal=focal
Tie a=hub b=spine kind=door
Socket name=spine-n part=spine bearing=north width=5
Socket name=spine-s part=spine bearing=south width=5
Socket name=hub-n part=hub bearing=north width=5
Socket name=hub-ne part=hub bearing=north-east width=5
Socket name=hub-e part=hub bearing=east width=5
Socket name=hub-se part=hub bearing=south-east width=5
Socket name=hub-s part=hub bearing=south width=5
Socket name=hub-sw part=hub bearing=south-west width=5
Socket name=hub-w part=hub bearing=west width=5
Socket name=hub-nw part=hub bearing=north-west width=5
Constraint kind=straight parts=spine
```
