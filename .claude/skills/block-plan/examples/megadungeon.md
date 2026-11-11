# Megadungeon

One crowded level of about seventy rooms. An octagonal crossing at the centre, with its rooms on all
eight points, joins the eight areas round it. At the north is a gate hall with cells off it, a diamond court and
a vault grid behind a great hall. To the west are a cloister of cells, a chapter house and a column of round crypts.
To the east are a cave, a row of lairs and a stair tower. The south holds two warrens of rooms sharing walls and
a gallery. A natural cleft runs across it from the north-west to the lower east side, and passages cross it where they must.
Ways lead out at the north gate, the east tower and the stairs up and down.

```kdl
Design M.a locations="M.1, M.2, M.3, M.4, M.5, M.6, M.7, M.8, M.9, M.10, M.11, M.12, M.13, M.14, M.15, M.16, M.17, M.18, M.19, M.20, M.21, M.22, M.23, M.24, M.25, M.26, M.27, M.28, M.29, M.30, M.31, M.32, M.33, M.34, M.35, M.36, M.37, M.38, M.39, M.40, M.41, M.42, M.43, M.44, M.45, M.46, M.47, M.48, M.49, M.50, M.51, M.52, M.53, M.54, M.55, M.56, M.57, M.58, M.59, M.60, M.61, M.62, M.63, M.64, M.65, M.66, M.67, M.68, M.69, M.70" outline="rect 400 460" fill="30-45%" width=10

// the north: gate hall, diamond court, vaults behind the great hall
Layout M.a id=gate arrange=spine entry=M.1 facing=north side=w
Room M.1 layout=gate width=80 length=10 shape=hall
Room M.2 layout=gate width=20 length=20
Room M.3 layout=gate width=20 length=30
Room M.4 layout=gate width=30 length=20
Room M.5 layout=gate width=20 length=20
Layout M.a id=court arrange=ring entry=M.6 gap=10 facing=north
Room M.6 layout=court width=40 length=40 shape=diamond
Room M.7 layout=court width=20 length=20 facing=north
Room M.8 layout=court width=20 length=20 facing=east
Room M.9 layout=court width=20 length=20 facing=west
Room M.10 layout=court width=20 length=20 facing=south
Layout M.a id=vaults arrange=grid cols=3 facing=north side=e
Room M.11 layout=vaults width=20 length=20
Room M.12 layout=vaults width=20 length=20
Room M.13 layout=vaults width=20 length=20
Room M.14 layout=vaults width=20 length=20
Room M.15 layout=vaults width=20 length=20
Room M.16 layout=vaults width=20 length=20
Room M.17 width=60 length=40

// the west: cloister, chapter house, crypts
Layout M.a id=cloister arrange=spine entry=M.18 facing=west side=n
Room M.18 layout=cloister width=10 length=100 shape=hall
Room M.19 layout=cloister width=20 length=20
Room M.20 layout=cloister width=20 length=20
Room M.21 layout=cloister width=20 length=20
Room M.22 layout=cloister width=20 length=20
Room M.23 layout=cloister width=20 length=20
Room M.24 layout=cloister width=20 length=20
Room M.25 width=50 length=50 shape=octagon facing=west
Layout M.a id=crypts arrange=column gap=10 facing=west side=s
Room M.26 layout=crypts width=30 length=30 shape=round
Room M.27 layout=crypts width=30 length=30 shape=round
Room M.28 layout=crypts width=30 length=30 shape=round

// the centre: the crossing, its eight rooms, the great hall and its strongroom
Layout M.a id=crossing arrange=ring entry=M.29 gap=10
Room M.29 layout=crossing width=60 length=60 shape=octagon
Room M.30 layout=crossing width=30 length=20 facing=north
Room M.31 layout=crossing width=20 length=30 facing=east
Room M.32 layout=crossing width=30 length=20 facing=south
Room M.33 layout=crossing width=20 length=30 facing=west
Room M.34 layout=crossing width=20 length=20 shape=diamond facing=north-east
Room M.35 layout=crossing width=20 length=20 shape=diamond facing=south-east
Room M.36 layout=crossing width=20 length=20 shape=diamond facing=south-west
Room M.37 layout=crossing width=20 length=20 shape=diamond facing=north-west
Room M.38 width=60 length=60
Room M.69 width=20 length=20

// the east: cave, lairs, stair tower
Room M.39 width=70 length=70 shape=round facing=east
Layout M.a id=lairs arrange=row facing=east side=s
Room M.40 layout=lairs width=20 length=30
Room M.41 layout=lairs width=20 length=30
Room M.42 layout=lairs width=20 length=30
Room M.43 layout=lairs width=20 length=30
Room M.44 width=30 length=30 shape=octagon facing=east side=n

// the south: two warrens, the gallery
Layout M.a id=warren-w arrange=grid cols=4 facing=south side=w
Room M.45 layout=warren-w width=20 length=20
Room M.46 layout=warren-w width=20 length=20
Room M.47 layout=warren-w width=20 length=20
Room M.48 layout=warren-w width=20 length=20
Room M.49 layout=warren-w width=20 length=20
Room M.50 layout=warren-w width=20 length=20
Room M.51 layout=warren-w width=20 length=20
Room M.52 layout=warren-w width=20 length=20
Layout M.a id=warren-e arrange=grid cols=3 facing=south side=e
Room M.53 layout=warren-e width=20 length=20
Room M.54 layout=warren-e width=20 length=20
Room M.55 layout=warren-e width=20 length=20
Room M.56 layout=warren-e width=20 length=20
Room M.57 layout=warren-e width=20 length=20
Room M.58 layout=warren-e width=20 length=20
Room M.a layout=warren-e count=3 width=20 length=20
Layout M.a id=gallery arrange=row facing=south
Room M.59 layout=gallery width=20 length=30
Room M.60 layout=gallery width=20 length=30
Room M.61 layout=gallery width=20 length=30
Room M.62 layout=gallery width=20 length=30
Room M.63 layout=gallery width=20 length=30
Room M.64 layout=gallery width=20 length=30
Room M.65 width=10 length=60 shape=hall
Room M.66 width=30 length=30 shape=diamond
Room M.67 width=20 length=20 shape=round
Room M.68 width=20 length=20
Room M.70 width=20 length=20 facing=south side=e

// the cleft, laid first: passages cross it
Route M.a ends="M.a:north:w, M.a:east:s" line=straight style=natural width=20 label="The Cleft"

// ways in and out
Route M.a ends="M.a:north:w, M.1:north" door=none
Route M.a ends="M.44:east, M.a:east" door=none
Route M.a ends="M.7, M.b" stair=up
Route M.a ends="M.70, M.c" stair=down

// the north
Route M.a ends="M.1:east, M.9:west"
Route M.a ends="M.10:south, M.30:north" length=6
Route M.a ends="M.8:east, vaults"
Route M.a ends="vaults:south, M.17:north" kind=door
Route M.a ends="M.17:south, M.34"
Route M.a ends="M.17:east, M.44:north"

// the west
Route M.a ends="M.1:south, cloister:north"
Route M.a ends="M.18:south, M.25:north"
Route M.a ends="M.25:south, crypts:north"
Route M.a ends="M.33:west, M.38:east" door=arch
Route M.a ends="M.38, M.69" kind=door door=secret
Route M.a ends="M.38:west, M.25:east"
Route M.a ends="M.37, M.38:north"

// the east
Route M.a ends="M.31:east, M.39:west" door=arch
Route M.a ends="M.39:south, lairs"
Route M.a ends="M.39:north, M.44:south"
Route M.a ends="M.35, lairs:west"

// the south
Route M.a ends="M.32:south, gallery:north" door=arch
Route M.a ends="gallery, warren-w:east, warren-e:west"
Route M.a ends="crypts:south, warren-w:north"
Route M.a ends="M.36, M.65:north"
Route M.a ends="M.65:south, M.66"
Route M.a ends="M.66, M.67, M.68"
Route M.a ends="warren-e:east, M.70" door=locked
```
