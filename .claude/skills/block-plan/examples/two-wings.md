# Two wings

Two blocks of one level side by side and a third under the first. The west wing is a barracks: a grid of
bunk rooms round a drill yard, an officers' suite set exactly where the plan puts it, and a winding way
to the east wing. The east wing is a gallery spine of shrines with a secret pair behind it. One route
joins rooms of both wings and the crypt below: each map shows its own leg, leaving toward the other.

```kdl
Design W.a locations="W.1, W.2, W.3, W.4, W.5, W.6, W.7" xyz="0,0,0" outline="rect 160 160" fill="20-35%"
Room W.1 width=40 length=40 facing=west
Layout W.a id=bunks arrange=grid cols=3 gap=0 facing=north
Room W.2 layout=bunks width=20 length=20
Room W.3 layout=bunks width=20 length=20
Room W.a layout=bunks count=4 width=20 length=20
Layout W.a id=officers arrange=row xyz="50,-60"
Room W.4 layout=officers width=30 length=30
Room W.5 layout=officers width=20 length=20
Room W.6 width=20 length=30 facing=south side=w
Room W.7 width=20 length=20 facing=east
Route W.a ends="W.1:north, bunks" door=arch
Route W.a ends="W.1:east, officers, W.6"
Route W.a ends="W.6, W.7" length=long
Route W.a ends="W.a:west, W.1:west" door=none

Design W.b locations="W.8, W.9, W.10, W.11, W.12, W.13" xyz="240,0,0" outline="rect 140 160" fill="20-35%"
Layout W.b id=gallery arrange=spine entry=W.8 gap=0 facing=north
Room W.8 layout=gallery width=100 length=10 shape=hall
Room W.9 layout=gallery width=30 length=20
Room W.10 layout=gallery width=30 length=20
Room W.11 layout=gallery width=20 length=20
Room W.b layout=gallery count=2 width=20 length=20
Room W.12 width=40 length=40 shape=octagon
Room W.13 width=20 length=20
Route W.b ends="gallery, W.12:north" length=4
Route W.b ends="W.12, W.13" kind=door door=secret

Route W.a ends="W.7:east, W.12:west, W.14"

Design W.c locations="W.14" xyz="0,0,-30" outline="rect 60 60" fill="30-50%"
Room W.14 width=40 length=40 shape=round
```
