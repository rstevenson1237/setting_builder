# Twin loop

A gate room with two routes that loop into each other below it, and room between them for a core.

```kdl
Layout twin-loop name="A gate and two routes that loop together" tags="loop, branching, gate" source="written"
Part role=gate shape=round width="30" length="30"
Part role=left shape=octagon width="20" length="20" count="3" at="gate south-west"
Part role=right shape=hexagon width="20" length="20" count="3" at="gate south-east"
Tie a=gate b=left kind=passage of_b=first
Tie a=left b=left kind=passage
Tie a=gate b=right kind=passage of_b=first
Tie a=right b=right kind=passage
Tie a=left b=right kind=passage of_a=last of_b=last
Socket name=in part=gate bearing=north width=10
Socket name=core part=gate bearing=south width=10
```
