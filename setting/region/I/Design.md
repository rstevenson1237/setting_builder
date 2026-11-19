# Design of I The Drowned Galleon

The galleon lies bow to the south across the reef gap: the stern deck at the north is the way in, with the captain's cabin below it, then the gun deck, the cargo hold and the flooded hold in a line down the ship, the galley off the gun deck and the bilge at the bow end.

```kdl
Design I.a locations="I.1, I.2, I.3, I.4, I.5, I.6, I.7" outline="rect 60 140" fill="35-55%"
Layout I.a id=ship arrange=column facing=north entry=I.1 gap=0
Room I.1 layout=ship width=30 length=20
Room I.2 layout=ship width=30 length=20
Room I.3 layout=ship width=30 length=30
Room I.5 layout=ship width=30 length=30
Room I.4 layout=ship width=30 length=30
Room I.7 layout=ship width=20 length=10 shape=hall
Room I.6 width=20 length=20 facing=west
Route I.a ends="I.a:north, I.1:north" door=none
Route I.a ends="I.3, I.6" kind=door
```
