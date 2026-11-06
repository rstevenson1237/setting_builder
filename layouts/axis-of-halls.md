# Axis of halls

Large halls in a row, each opening on the next by a wide passage: an approach to a throne, a
processional, the spine of a temple.

```kdl
Layout axis-of-halls name="A row of halls" tags="halls, axial, approach, grand" source="drawn from map 1"
Param name=halls range="2-4"
Part role=hall shape=round width="30-40" length="30-40" count=halls at="hall east" focal=focal
Tie a=hall b=hall kind=passage
Socket name=first part=hall of=first bearing=west width=10
Socket name=last part=hall of=last bearing=east width=10
Constraint kind=straight parts=hall
```
