# Design of X

```kdl
Design X.a locations="X.1, X.2, X.3, X.4, X.5, X.6, X.7, X.8, X.9, X.10, X.11, X.12, X.13, X.14, X.15, X.16, X.17, X.18, X.19, X.20, X.21, X.22" spacing="20-40 feet" pad="10 feet" seed=7 score="100" hull="poly -100,90 -90,-40 -60,-70 40,-110 50,-110 90,-100 110,-20 110,0 90,50 70,90 30,100 -100,100"
Use X.a id=fig layout=figure-eight
Use X.a id=vest layout=stair-end
Bind X.a use=fig role=m locations="X.1" type=Medium
Bind X.a use=fig role=a locations="X.2, X.3, X.4, X.5, X.6" type="Low, Medium, High, Medium, Low"
Bind X.a use=fig role=b locations="X.7, X.8, X.9, X.10, X.11" type="Low, Medium, High, Medium, Medium"
Bind X.a use=vest role=vestibule locations="X.12" type=High
Fill X.a locations="X.13" type=Low width=20 length=20
Fill X.a locations="X.14" type=Medium width=20 length=20
Fill X.a locations="X.15, X.16, X.17, X.18, X.19, X.20" type=Low width=10 length=20
Fill X.a locations="X.21, X.22" type=High width=10 length=10
Join X.a from="fig.right-end" to="vest.in"
Join X.a from="fig.left-end" to="X.13"
Join X.a from="X.1" to="X.14"
Join X.a from="X.3" to="X.15"
Join X.a from="X.15" to="X.16"
Join X.a from="X.5" to="X.17"
Join X.a from="X.8" to="X.18"
Join X.a from="X.10" to="X.19"
Join X.a from="X.19" to="X.20"
Join X.a from="X.4" to="X.21"
Join X.a from="X.11" to="X.22"
Join X.a from="X.2" to="X.7"
Join X.a from="X.6" to="X.11"
Place X.1 xyz="10,10" outline="rect 20 20" shape=rect
Place X.2 xyz="-30,10" outline="rect 20 20" shape=rect
Place X.3 xyz="-70,10" outline="rect 20 20" shape=rect
Place X.4 xyz="-40,-30" outline="rect 20 20" shape=rect
Place X.5 xyz="-10,-70" outline="rect 20 20" shape=rect
Place X.6 xyz="0,-30" outline="rect 20 20" shape=rect
Place X.7 xyz="0,50" outline="rect 20 20" shape=rect
Place X.8 xyz="-20,90" outline="rect 20 20" shape=rect
Place X.9 xyz="20,90" outline="rect 20 20" shape=rect
Place X.10 xyz="100,-10" outline="rect 20 20" shape=rect
Place X.11 xyz="40,-30" outline="rect 20 20" shape=rect
Place X.12 xyz="60,80" outline="rect 20 20" shape=rect
Place X.13 xyz="-80,-30" outline="rect 20 20" shape=rect
Place X.14 xyz="50,20" outline="rect 20 20" shape=rect
Place X.15 xyz="-50,45" outline="rect 20 10" shape=rect
Place X.16 xyz="-90,95" outline="rect 20 10" shape=rect
Place X.17 xyz="45,-100" outline="rect 10 20" shape=rect
Place X.18 xyz="-55,80" outline="rect 10 20" shape=rect
Place X.19 xyz="85,-50" outline="rect 10 20" shape=rect
Place X.20 xyz="85,-90" outline="rect 10 20" shape=rect
Place X.21 xyz="-55,-65" outline="rect 10 10" shape=rect
Place X.22 xyz="35,-65" outline="rect 10 10" shape=rect
Link X.1 to="X.2" kind=passage
Link X.1 to="X.6" kind=passage
Link X.1 to="X.7" kind=passage
Link X.1 to="X.11" kind=passage
Link X.1 to="X.14" kind=passage
Link X.2 to="X.3" kind=passage
Link X.2 to="X.7" kind=passage
Link X.3 to="X.4" kind=passage
Link X.3 to="X.15" kind=passage
Link X.4 to="X.5" kind=passage
Link X.4 to="X.13" kind=passage
Link X.4 to="X.21" kind=passage
Link X.5 to="X.6" kind=passage
Link X.5 to="X.17" kind=passage
Link X.6 to="X.11" kind=passage
Link X.7 to="X.8" kind=passage
Link X.8 to="X.9" kind=passage
Link X.8 to="X.18" kind=passage
Link X.9 to="X.10" kind=passage
Link X.9 to="X.12" kind=passage
Link X.10 to="X.11" kind=passage
Link X.10 to="X.19" kind=passage
Link X.11 to="X.22" kind=passage
Link X.15 to="X.16" kind=passage
Link X.19 to="X.20" kind=passage
```
