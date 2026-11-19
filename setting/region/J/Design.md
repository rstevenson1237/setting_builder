# Design of J The Troglodytes' Warren

The sinkhole's floor is the hub, with the rope cave and the guard gallery on its near side and long natural passages running from it to the warren hall, the bone midden, the captives' pit and, beyond the hall, the chief's cave with the loot cave hidden behind it.

```kdl
Design J.a locations="J.1, J.2, J.3, J.4, J.5, J.6, J.7, J.8" outline="rect 120 140" fill="35-55%" seed=1 approved="2026-11-19"
Room J.1 width=30 length=30 shape=cave xyz="0,40"
Room J.2 width=20 length=20 shape=cave facing=west
Room J.3 width=20 length=30 shape=cave facing=east
Room J.4 width=50 length=40 shape=cave facing=south
Room J.5 width=20 length=20 shape=cave facing=west
Room J.6 width=20 length=20 shape=cave facing=east
Room J.7 width=30 length=30 shape=cave facing=south
Room J.8 width=20 length=20 shape=cave
Route J.a ends="J.1:north, J.a:north" door=none style=natural
Route J.a ends="J.1, J.2" style=natural
Route J.a ends="J.1, J.3" style=natural
Route J.a ends="J.1:south, J.4:north" style=natural length=long
Route J.a ends="J.4, J.5" style=natural
Route J.a ends="J.4, J.6" style=natural
Route J.a ends="J.4:south, J.7:north" style=natural
Route J.a ends="J.7, J.8" style=natural door=secret
Place J.1 xyz="5,35" outline="rect 30 30" shape=cave
Place J.2 xyz="-30,30" outline="rect 20 20" shape=cave
Place J.3 xyz="40,5" outline="rect 20 30" shape=cave
Place J.4 xyz="-5,-10" outline="rect 50 40" shape=cave
Place J.5 xyz="-50,0" outline="rect 20 20" shape=cave
Place J.6 xyz="40,-30" outline="rect 20 20" shape=cave
Place J.7 xyz="-5,-55" outline="rect 30 30" shape=cave
Place J.8 xyz="-40,-50" outline="rect 20 20" shape=cave
Link J.1 to="J.2" kind=passage
Link J.1 to="J.3" kind=passage
Link J.1 to="J.4" kind=passage
Link J.4 to="J.5" kind=passage
Link J.4 to="J.6" kind=passage
Link J.4 to="J.7" kind=passage
Link J.7 to="J.8" kind=passage
```
