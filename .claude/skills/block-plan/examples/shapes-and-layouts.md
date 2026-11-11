# Shapes and layouts

Every layout beyond the simple ones and every room shape, in one block: a dense block of rooms of every
size, a cloister round a yard, a shrine of organic cells on spokes round a round hub, and a row of odd
rooms - oval, apse, ell, cross, irregular - joined by passages that run on the diagonal where it pays.

```kdl
Design L.a locations="L.1, L.2, L.3, L.4, L.5, L.6, L.7, L.8, L.9, L.10" outline="rect 300 260" fill="30-45%"
Layout L.a id=warren arrange=split width=90 length=70 entry=L.1 facing=west side=s loops=20%
Room L.1 layout=warren width=30 length=30
Room L.a layout=warren count=10
Layout L.a id=cloister arrange=court depth=20 width=90 length=80 facing=east side=s
Room L.2 layout=cloister
Room L.a layout=cloister count=8
Layout L.a id=shrine arrange=radial entry=L.3 gap=10 sweep=270 bearing=0 facing=north
Room L.3 layout=shrine width=40 length=40 shape=round
Room L.a layout=shrine count=5 width=20 length=20 shape=organic
Layout L.a id=odd arrange=row gap=10 facing=north side=e
Room L.4 layout=odd width=30 length=20 shape=oval
Room L.5 layout=odd width=30 length=40 shape=apse
Room L.6 layout=odd width=30 length=30 shape=ell
Room L.7 width=30 length=30 shape=cross
Room L.8 width=30 length=30 shape=irregular
Room L.9 width=20 length=20 shape=hexagon
Room L.10 width=30 length=20 shape=organic
Route L.a ends="L.1, L.2"
Route L.a ends="warren:north, L.3"
Route L.a ends="cloister:north, odd"
Route L.a ends="L.4, L.7, L.8"
Route L.a ends="L.8, L.9" kind=door
Route L.a ends="L.9, L.10"
Route L.a ends="L.4, L.a:north" door=none
```
