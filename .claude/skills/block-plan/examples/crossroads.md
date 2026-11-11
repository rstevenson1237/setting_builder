# Crossroads

A central chamber with a passage off every side: a pillared hall to the east and a winding way from it
to a hidden pair of rooms, a stack of shrine rooms to the west sharing one passage with a column of round
tombs, a vault row to the south reached the long way round, and a great round chamber to the north.

```kdl
Design Y.a locations="Y.1, Y.2, Y.3, Y.4, Y.5, Y.6, Y.7, Y.8, Y.9, Y.10, Y.11, Y.12, Y.13, Y.14" outline="rect 280 340" fill="20-35%"
Room Y.1 width=30 length=30 xyz="0,0"
Room Y.2 width=70 length=40 facing=east
Layout Y.a id=shrine arrange=column facing=west side=n
Room Y.3 layout=shrine width=40 length=30
Room Y.4 layout=shrine width=40 length=20
Room Y.5 layout=shrine width=40 length=30
Layout Y.a id=tombs arrange=column gap=10 facing=south side=w
Room Y.8 layout=tombs width=30 length=30 shape=round
Room Y.9 layout=tombs width=30 length=30 shape=round
Room Y.10 layout=tombs width=30 length=30 shape=round
Layout Y.a id=vaults arrange=row facing=south side=e
Room Y.6 layout=vaults width=30 length=30
Room Y.7 layout=vaults width=20 length=30
Room Y.a layout=vaults count=2 width=20 length=20
Layout Y.a id=crown arrange=column facing=north
Room Y.11 layout=crown width=60 length=60 shape=round
Room Y.12 layout=crown width=30 length=50 shape=hall
Room Y.13 width=30 length=20
Room Y.14 width=20 length=20
Route Y.a ends="Y.1:north, Y.12:south" length=8
Route Y.a ends="Y.1:west, shrine, tombs:north"
Route Y.a ends="Y.1:east, Y.2:west" door=arch
Route Y.a ends="Y.1:south, vaults" length=long door="door, locked"
Route Y.a ends="Y.2:north, Y.13" length=6
Route Y.a ends="Y.13, Y.14" kind=door door=secret
Route Y.a ends="Y.a:north:w, Y.11:north" door=none
Route Y.a ends="Y.a:east, Y.2:east" door=none
Route Y.a ends="Y.a:west, shrine:west" door=none
Route Y.a ends="Y.10, Z.3" stair=down
```
