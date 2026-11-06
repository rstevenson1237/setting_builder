# Design of Z (fixed geometry: a spiral stated by hand)

```kdl
Design Z.a locations="Z.1, Z.2, Z.3, Z.4, Z.5, Z.6, Z.7, Z.8, Z.9, Z.10, Z.11, Z.12, Z.13, Z.14" outline="rect 220 220"
Fill Z.a locations="Z.1" type=Low width=20 length=20 shape=cave
Fill Z.a locations="Z.2" type=Low width=20 length=20 shape=cave
Fill Z.a locations="Z.3" type=Medium width=20 length=20 shape=cave
Fill Z.a locations="Z.4" type=Low width=20 length=20 shape=cave
Fill Z.a locations="Z.5" type=Medium width=20 length=20 shape=cave
Fill Z.a locations="Z.6" type=Medium width=20 length=20 shape=cave
Fill Z.a locations="Z.7" type=High width=20 length=20 shape=cave
Fill Z.a locations="Z.8" type=Medium width=20 length=20 shape=cave
Fill Z.a locations="Z.9" type=Low width=20 length=20 shape=cave
Fill Z.a locations="Z.10" type=Medium width=20 length=20 shape=cave
Fill Z.a locations="Z.11" type=High width=20 length=20 shape=cave
Fill Z.a locations="Z.12" type=Medium width=20 length=20 shape=cave
Fill Z.a locations="Z.13" type=High width=20 length=20 shape=cave
Fill Z.a locations="Z.14" type=High width=40 length=40 shape=cave
Place Z.1 xyz="-50,-50" outline="rect 20 20" shape=cave
Place Z.2 xyz="0,-50" outline="rect 20 20" shape=cave
Place Z.3 xyz="50,-50" outline="rect 20 20" shape=cave
Place Z.4 xyz="100,-50" outline="rect 20 20" shape=cave
Place Z.5 xyz="100,0" outline="rect 20 20" shape=cave
Place Z.6 xyz="100,50" outline="rect 20 20" shape=cave
Place Z.7 xyz="100,100" outline="rect 20 20" shape=cave
Place Z.8 xyz="50,100" outline="rect 20 20" shape=cave
Place Z.9 xyz="0,100" outline="rect 20 20" shape=cave
Place Z.10 xyz="-50,100" outline="rect 20 20" shape=cave
Place Z.11 xyz="-50,50" outline="rect 20 20" shape=cave
Place Z.12 xyz="-50,0" outline="rect 20 20" shape=cave
Place Z.13 xyz="0,0" outline="rect 20 20" shape=cave
Place Z.14 xyz="0,50" outline="rect 40 40" shape=cave
Link Z.1 to="Z.2" kind=passage
Link Z.2 to="Z.3" kind=passage
Link Z.3 to="Z.4" kind=passage
Link Z.4 to="Z.5" kind=passage
Link Z.5 to="Z.6" kind=passage
Link Z.6 to="Z.7" kind=passage
Link Z.7 to="Z.8" kind=passage
Link Z.8 to="Z.9" kind=passage
Link Z.9 to="Z.10" kind=passage
Link Z.10 to="Z.11" kind=passage
Link Z.11 to="Z.12" kind=passage
Link Z.12 to="Z.13" kind=passage
Link Z.13 to="Z.14" kind=passage
```
