# Design of L Pyramid Level 10 - The Demon's Chamber

The rooms where the packing set them, the level moved to stand under the last threshold: the feeding floor with
the round offering pit and the demon's seat beside it, the bone gallery and the offering ledge.

```kdl
Design L.a locations="L.1, L.2, L.3, L.4, L.5, L.6" outline="poly -140,80 30,80 30,-80 -140,-80" fill="25-45%" pad="0 feet" seed=1 approved="2026-11-11"
Room L.1 width=20 length=20 xyz="0,10"
Room L.2 width=50 length=60 xyz="-55,30"
Room L.3 width=40 length=40 shape=round xyz="-100,-40"
Room L.4 width=40 length=40 xyz="-100,30"
Room L.5 width=30 length=40 xyz="-15,40"
Room L.6 width=20 length=20 xyz="-90,0"
Route L.a ends="L.1, L.2"
Route L.a ends="L.1, K.5" stair=up
Route L.a ends="L.2, L.3"
Route L.a ends="L.2, L.4" kind=door
Route L.a ends="L.3, L.4"
Route L.a ends="L.1, L.5" kind=door
Route L.a ends="L.5, L.2" kind=door
Route L.a ends="L.2, L.6" kind=door
Route L.a ends="L.6, L.3"
Place L.1 xyz="0,10" outline="rect 20 20" shape=rect
Place L.2 xyz="-55,30" outline="rect 50 60" shape=rect
Place L.3 xyz="-100,-40" outline="rect 40 40" shape=round
Place L.4 xyz="-100,30" outline="rect 40 40" shape=rect
Place L.5 xyz="-15,40" outline="rect 30 40" shape=rect
Place L.6 xyz="-90,0" outline="rect 20 20" shape=rect
Link L.1 to="L.2" kind=passage
Link L.1 to="L.5" kind=door
Link L.2 to="L.3" kind=passage
Link L.2 to="L.4" kind=door
Link L.2 to="L.5" kind=door
Link L.2 to="L.6" kind=door
Link L.3 to="L.4" kind=passage
Link L.3 to="L.6" kind=passage
```
