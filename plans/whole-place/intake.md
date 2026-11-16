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

| Found by hand | Why the dry fire passes it |
|---|---|
| The Black Stair's head (B.10) lies at z -63, four feet above F.6's ceiling and inside level 4's block. Nothing written says the lake city's stair comes up inside the pyramid. | B.10 has an outline and no height, and a WILD location is not tested against another region's block. |
| The passage up to it from the old granary (B.5), 80 yards climbing 50 feet, crosses the footprints of levels 4 and 5. | A way between places is a bearing and a distance: it has no path. |
| The lake cavern is a circle of radius 600 feet at z -113 with no roof. Pyramid levels 5 to 10 stand inside that circle, and its floor cuts level 6 (-127 to -103). | A region is an outline at one height. |
| The stair from H.1 to B.10 climbs 64 feet in 30. | A way's climb is held to its ends, not to what can be walked. |
| `Ground.md` puts the lake city's ground at height 550; the shared space puts it at z -113. | A sheet's heights are artgen's own datum. |
| A passage within a level is drawn and never tested. | Its path is solved again at each draw and held nowhere `space.py` reads. |

Each is a question the text should answer - is the lake city under the pyramid or beside it; is the Black
Stair a stair or a shaft - before it is one for an engine.

## Out of scope

A 3D viewer, a scene file, and anything drawn in a room (the map-contents plan).
