# Figure eight

Two loops of rooms round one shared room: a ring on each side of it.

```kdl
Layout figure-eight name="Two loops round a shared room" tags="loop, figure-eight, loops" source="written"
Part role=m width="20" length="20" focal=focal
Part role=a width="20" length="20" count="5" at="m west"
Part role=b width="20" length="20" count="5" at="m east"
Tie a=m b=a kind=passage of_b=first
Tie a=m b=a kind=passage of_b=last
Tie a=a b=a kind=passage
Tie a=m b=b kind=passage of_b=first
Tie a=m b=b kind=passage of_b=last
Tie a=b b=b kind=passage
Socket name=left-end part=a of=3 bearing=west width=10
Socket name=right-end part=b of=3 bearing=east width=10
```
