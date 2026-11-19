# Design of HA The Pyramid's Upper Temple

The first terrace, the great stair, the second terrace, the bell court and the shrine run up the pyramid's face in a line. The guard room and the vestry stand on its west side, and the offering terrace, the blood channel and the shaft room in a line on its east, the channel running from the offering terrace to the shaft room, whose shaft goes down to the halls.

```kdl
Design HA.a locations="HA.1, HA.2, HA.3, HA.4, HA.5, HA.6, HA.7, HA.8, HA.9, HA.10" outline="rect 150 160" fill="25-45%" seed=3 approved="2026-11-19"
Layout HA.a id=ascent arrange=column facing=south entry=HA.1 gap=0
Room HA.1 layout=ascent width=60 length=20
Room HA.2 layout=ascent width=10 length=40 shape=hall
Room HA.3 layout=ascent width=60 length=20
Room HA.4 layout=ascent width=40 length=30
Room HA.8 layout=ascent width=50 length=30
Layout HA.a id=west arrange=column facing=west gap=10
Room HA.6 layout=west width=30 length=20
Room HA.9 layout=west width=20 length=30
Layout HA.a id=east arrange=column facing=east gap=0
Room HA.5 layout=east width=40 length=30
Room HA.7 layout=east width=10 length=40 shape=hall
Room HA.10 layout=east width=30 length=30 shape=round
Route HA.a ends="HA.a:south, HA.1:south" door=none
Route HA.a ends="HA.3:west, HA.6" length=short
Route HA.a ends="HA.8:west, HA.9" length=short
Route HA.a ends="HA.4:east, HA.5" length=short
Route HA.a ends="HA.8:east, HA.10" length=short
Route HA.a ends="HA.10, HB.1" stair=down
Place HA.1 xyz="-5,60" outline="rect 60 20" shape=rect
Place HA.2 xyz="-10,30" outline="rect 10 40" shape=hall
Place HA.3 xyz="-5,0" outline="rect 60 20" shape=rect
Place HA.4 xyz="-5,-25" outline="rect 40 30" shape=rect
Place HA.8 xyz="-10,-55" outline="rect 50 30" shape=rect
Place HA.6 xyz="-60,10" outline="rect 30 20" shape=rect
Place HA.9 xyz="-65,-25" outline="rect 20 30" shape=rect
Place HA.5 xyz="55,15" outline="rect 40 30" shape=rect
Place HA.7 xyz="50,-20" outline="rect 10 40" shape=hall
Place HA.10 xyz="50,-65" outline="rect 30 30" shape=round
Link HA.1 to="HA.2" kind=door
Link HA.2 to="HA.3" kind=door
Link HA.3 to="HA.4" kind=door
Link HA.3 to="HA.6" kind=passage
Link HA.4 to="HA.5" kind=passage
Link HA.4 to="HA.8" kind=door
Link HA.5 to="HA.7" kind=door
Link HA.6 to="HA.9" kind=passage
Link HA.7 to="HA.10" kind=passage
Link HA.8 to="HA.10" kind=passage
Link HA.8 to="HA.9" kind=passage
```
