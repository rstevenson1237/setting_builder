# Design of HA The Pyramid's Upper Temple

The first terrace, the great stair, the second terrace, the bell court and the shrine run up the pyramid's face in a line. The guard room and the vestry stand on its west side, and the offering terrace, the blood channel and the shaft room in a line on its east, the channel running from the offering terrace to the shaft room, whose shaft goes down to the halls.

```kdl
Design HA.a locations="HA.1, HA.2, HA.3, HA.4, HA.5, HA.6, HA.7, HA.8, HA.9, HA.10" outline="rect 150 160" fill="25-45%"
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
```
