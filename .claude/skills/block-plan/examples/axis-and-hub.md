# Axis and hub

A long axis from the north entrance, side cells paired on it, a pillared hall, then an octagonal hub
with rooms on its points and a hall beyond it; a temple wing to the west on its own passage.

```kdl
Design X.a locations="X.1, X.2, X.3, X.4, X.5, X.6, X.7, X.8, X.9, X.10, X.11, X.12, X.13, X.14, X.15, X.16" outline="rect 200 440" fill="20-35%"
Layout X.a id=gate arrange=spine entry=X.1 facing=north
Room X.1 layout=gate width=10 length=90 shape=hall
Room X.2 layout=gate width=20 length=20
Room X.3 layout=gate width=20 length=20
Room X.4 layout=gate width=20 length=30
Room X.5 layout=gate width=30 length=20
Room X.6 width=60 length=50 shape=octagon
Layout X.a id=hub arrange=ring entry=X.8 gap=20
Room X.8 layout=hub width=40 length=40 shape=octagon
Room X.9 layout=hub width=20 length=20 facing=east
Room X.10 layout=hub width=20 length=20 facing=west
Room X.11 layout=hub width=20 length=30 facing=south
Room X.12 layout=hub width=20 length=20 shape=diamond facing=north-west
Room X.13 layout=hub width=20 length=20 shape=diamond facing=north-east
Room X.7 width=10 length=60 shape=hall
Room X.14 width=60 length=50 shape=octagon facing=south
Layout X.a id=temple arrange=column facing=west
Room X.15 layout=temple width=60 length=80
Room X.16 layout=temple width=40 length=30
Route X.a ends="X.1:north, X.a:north" door=none
Route X.a ends="X.1:south, X.6:north"
Route X.a ends="X.6:south, X.7:north" kind=door
Route X.a ends="X.7:south, X.8:north"
Route X.a ends="X.11, X.14"
Route X.a ends="X.6:west, temple" length=6
Route X.a ends="X.14:south, X.a:south" door=none
```
