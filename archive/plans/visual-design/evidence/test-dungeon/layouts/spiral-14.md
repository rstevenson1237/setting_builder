# Spiral

A chain of rooms wound inward in a square spiral to a larger room at its centre.

```kdl
Layout spiral-14 name="A square spiral of fourteen rooms" tags="spiral, chain, winding, centre" source="written"
Part role=p1 shape=cave width="20" length="20"
Part role=p2 shape=cave width="20" length="20" at="p1 east"
Part role=p3 shape=cave width="20" length="20" at="p2 east"
Part role=p4 shape=cave width="20" length="20" at="p3 east"
Part role=p5 shape=cave width="20" length="20" at="p4 north"
Part role=p6 shape=cave width="20" length="20" at="p5 north"
Part role=p7 shape=cave width="20" length="20" at="p6 north"
Part role=p8 shape=cave width="20" length="20" at="p7 west"
Part role=p9 shape=cave width="20" length="20" at="p8 west"
Part role=p10 shape=cave width="20" length="20" at="p9 west"
Part role=p11 shape=cave width="20" length="20" at="p10 south"
Part role=p12 shape=cave width="20" length="20" at="p11 south"
Part role=p13 shape=cave width="20" length="20" at="p12 east"
Part role=p14 shape=cave width="40" length="40" at="p13 north"
Tie a=p1 b=p2 kind=passage
Tie a=p2 b=p3 kind=passage
Tie a=p3 b=p4 kind=passage
Tie a=p4 b=p5 kind=passage
Tie a=p5 b=p6 kind=passage
Tie a=p6 b=p7 kind=passage
Tie a=p7 b=p8 kind=passage
Tie a=p8 b=p9 kind=passage
Tie a=p9 b=p10 kind=passage
Tie a=p10 b=p11 kind=passage
Tie a=p11 b=p12 kind=passage
Tie a=p12 b=p13 kind=passage
Tie a=p13 b=p14 kind=passage
Socket name=in part=p1 bearing=south width=10
```
