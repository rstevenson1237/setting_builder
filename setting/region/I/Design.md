# Design of I Pyramid Level 7 - The Altars

The rooms where the packing set them, the level moved to stand under the cult's stair down: the altars of making
and unmaking and the cells round them, sharing walls.

```kdl
Design I.a locations="I.1, I.2, I.3, I.4, I.5, I.6, I.7, I.8, I.9, I.10, I.11, I.12, I.13, I.14" outline="poly -130,100 50,100 50,-90 -130,-90" width=5 seed=1 approved="2026-11-11"
Room I.1 width=10 length=20 xyz="-55,-30"
Room I.2 width=30 length=50 xyz="-35,-15"
Room I.3 width=40 length=50 xyz="0,25"
Room I.4 width=40 length=30 xyz="-60,25"
Room I.5 width=30 length=40 xyz="-75,-20"
Room I.6 width=30 length=30 xyz="-35,55"
Room I.7 width=30 length=30 xyz="-25,-55"
Room I.8 width=60 length=10 xyz="-70,-55"
Room I.9 width=20 length=40 xyz="20,-40"
Room I.10 width=20 length=20 xyz="-10,-30"
Room I.11 width=20 length=20 xyz="-100,-30"
Room I.12 width=20 length=20 xyz="-60,70"
Room I.13 width=30 length=20 xyz="15,-10"
Room I.14 width=40 length=10 xyz="-80,-43"
Route I.a ends="I.1, I.2" kind=door
Route I.a ends="I.1, I.5" kind=door
Route I.a ends="I.1, H.12" stair=up
Route I.a ends="I.2, I.4" kind=door
Route I.a ends="I.2, I.3" kind=door
Route I.a ends="I.2, I.7" kind=door
Route I.a ends="I.3, I.6" kind=door
Route I.a ends="I.3, I.9"
Route I.a ends="I.4, I.5"
Route I.a ends="I.4, I.6" kind=door
Route I.a ends="I.7, I.8" kind=door
Route I.a ends="I.9:north, J.1" stair=down
Route I.a ends="I.7, I.10" kind=door
Route I.a ends="I.5, I.11" kind=door
Route I.a ends="I.6, I.12" kind=door
Route I.a ends="I.9, I.13" kind=door
Route I.a ends="I.3, I.13" kind=door
Route I.a ends="I.1, I.14"
Route I.a ends="I.14, I.11" kind=door
Place I.1 xyz="-55,-30" outline="rect 10 20" shape=rect
Place I.2 xyz="-35,-15" outline="rect 30 50" shape=rect
Place I.3 xyz="0,25" outline="rect 40 50" shape=rect
Place I.4 xyz="-60,25" outline="rect 40 30" shape=rect
Place I.5 xyz="-75,-20" outline="rect 30 40" shape=rect
Place I.6 xyz="-35,55" outline="rect 30 30" shape=rect
Place I.7 xyz="-25,-55" outline="rect 30 30" shape=rect
Place I.8 xyz="-70,-55" outline="rect 60 10" shape=rect
Place I.9 xyz="20,-40" outline="rect 20 40" shape=rect
Place I.10 xyz="-10,-30" outline="rect 20 20" shape=rect
Place I.11 xyz="-100,-30" outline="rect 20 20" shape=rect
Place I.12 xyz="-60,70" outline="rect 20 20" shape=rect
Place I.13 xyz="15,-10" outline="rect 30 20" shape=rect
Place I.14 xyz="-80,-45" outline="rect 40 10" shape=rect
Link I.1 to="I.14" kind=passage
Link I.1 to="I.2" kind=door
Link I.1 to="I.5" kind=door
Link I.11 to="I.14" kind=door
Link I.2 to="I.3" kind=door
Link I.2 to="I.4" kind=door
Link I.2 to="I.7" kind=door
Link I.3 to="I.13" kind=door
Link I.3 to="I.6" kind=door
Link I.3 to="I.9" kind=passage
Link I.4 to="I.5" kind=passage
Link I.4 to="I.6" kind=door
Link I.5 to="I.11" kind=door
Link I.6 to="I.12" kind=door
Link I.7 to="I.10" kind=door
Link I.7 to="I.8" kind=door
Link I.9 to="I.13" kind=door
```
