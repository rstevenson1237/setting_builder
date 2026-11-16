# Intake - the whole place: a dry fire that tests everything a party walks through

## The request, verbatim

> 5 seems reasonable.

## How it is read

Review item 5, from the exercise of handing the setting to a 3D engine: stored passage paths, a roof on a
region, ways between regions routed, and a side elevation. `spec.md` numbers each for approval; none is built.

## What the dry fire tests today

`tools/space.py` places 182 of 190 things at a point with an outline and a floor-to-roof range, and reports
0 errors. It reports what is unplaced, what overlaps or lies outside its parent's outline, and a way whose
climb, bearing or distance disagrees with where its ends lie.

## What it cannot see, in this build

Found by hand before the lake city was moved, and what moving it settled:

| Found | Now |
|---|---|
| The Black Stair's head (B.10) stood inside pyramid level 4, and the passage up to it crossed levels 4 and 5. | Settled: the city lies 900 feet east-north-east of the pyramid, and the stair's head with it. |
| The lake cavern's circle held pyramid levels 5 to 10, its floor cutting level 6. | Settled: the circle stands 90 feet clear of the pyramid. |
| The path from G.14 ran through the tombs G.6 and G.17. | The tunnel now leaves by the one bearing that crosses least, and still crosses level 5's outer passage 70 feet out. Every bearing from G.14 crosses something: clearing it means moving a Route of G's plan. |
| The stair from H.1 climbed 64 feet in 30. | It climbs 64 in 500. Its first 10 feet run through a passage of level 6 beside the landing. |

Each was found with a scratch script or by eye. Still open, and what the dry fire cannot test:

| Open | Why the dry fire passes it |
|---|---|
| The cavern has no roof, so nothing says whether the stair's head, 50 feet above the city's floor, is in rock or in air. | A region is an outline at one height. |
| A way between two places crossing a room or passage it does not join. | A way is a bearing and a distance: it has no path. |
| A passage within a level crossing anything. | Its path is solved again at each draw and held nowhere `space.py` reads. |
| `Ground.md` puts the lake city's ground at height 550; the shared space puts it at z -113. | A sheet's heights are artgen's own datum. |

## Out of scope

A 3D viewer, a scene file, and anything drawn in a room (the map-contents plan).
