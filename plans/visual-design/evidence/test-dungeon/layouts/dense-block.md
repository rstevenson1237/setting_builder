# Dense block

A hall with rooms off both long sides, wall to wall: a barracks, a warren, a vault block.

```kdl
Layout dense-block name="A hall with rooms on both sides, touching" tags="dense, block, rooms" source="written"
Part role=hall width="60" length="10"
Part role=north-cell width="20" length="20" count="3" at="hall north"
Part role=south-cell width="20" length="20" count="3" at="hall south"
Tie a=hall b=north-cell kind=door
Tie a=hall b=south-cell kind=door
Socket name=north part=hall bearing=north width=10
Socket name=south part=hall bearing=south width=10
```
