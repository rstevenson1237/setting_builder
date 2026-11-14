# Design of L Pyramid Level 10 - The Demon's Chamber

The rooms where the packing set them, the level moved to stand under the last threshold: the feeding floor with
the round offering pit and the demon's seat beside it, the bone gallery and the offering ledge.

```kdl
Design L.a locations="L.1, L.2, L.3, L.4, L.5, L.6" outline="poly -130,70 20,70 20,-70 -130,-70" seed=1 approved="2026-11-14"
Room L.1 width=20 length=20 xyz="5,5"
Room L.2 width=40 length=50 xyz="-35,25"
Room L.3 width=40 length=40 shape=round xyz="-60,-45"
Room L.4 width=30 length=40 xyz="-70,30"
Room L.5 width=30 length=30 xyz="0,30"
Room L.6 width=20 length=20 xyz="-65,0"
Route L.a ends="L.1, L.2"
Route L.a ends="L.1, K.5" stair=up
Route L.a ends="L.2, L.3"
Route L.a ends="L.2, L.4" kind=door
Route L.a ends="L.3, L.4"
Route L.a ends="L.1, L.5" kind=door
Route L.a ends="L.5, L.2" kind=door
Route L.a ends="L.2, L.6" kind=door
Route L.a ends="L.6, L.3"
Place L.1 xyz="10,0" outline="rect 20 20" shape=rect
Place L.2 xyz="-30,25" outline="rect 40 50" shape=rect
Place L.3 xyz="-60,-50" outline="rect 40 40" shape=round
Place L.4 xyz="-65,30" outline="rect 30 40" shape=rect
Place L.5 xyz="5,25" outline="rect 30 30" shape=rect
Place L.6 xyz="-60,0" outline="rect 20 20" shape=rect
Link L.1 to="L.2" kind=passage
Link L.1 to="L.5" kind=door
Link L.2 to="L.3" kind=passage
Link L.2 to="L.4" kind=door
Link L.2 to="L.5" kind=door
Link L.2 to="L.6" kind=door
Link L.3 to="L.4" kind=passage
Link L.3 to="L.6" kind=passage
```
