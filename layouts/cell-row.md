# Cell row

Small rooms in two rows, each with one door onto a shared hall: cells, a barracks, a warren of stores.

```kdl
Layout cell-row name="A row of cells off a hall" tags="cells, hall, rooms" source="drawn from map 1, rooms 7 to 12"
Param name=per-row range="1-4"
Part role=hall width="30-60" length="10-30"
Part role=north-cell width="10-30" length="10-30" count=per-row at="hall north"
Part role=south-cell width="10-30" length="10-30" count=per-row at="hall south"
Tie a=hall b=north-cell kind=door
Tie a=hall b=south-cell kind=door
Socket name=west part=hall bearing=west width=10
Socket name=east part=hall bearing=east width=10
Constraint kind=mirror parts="north-cell, south-cell"
```
