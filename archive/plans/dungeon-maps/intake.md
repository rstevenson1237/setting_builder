# Intake - dungeon maps: what the framework gets wrong

## The request, verbatim

> read through @plans/dungeon-maps/report-framework.md and design and implement a plan to
> address the issues noted.

## Follow-up, verbatim

Asked whether a block's map file is committed or built (F9), given `plans/sheet-maps/spec.md`
D7 keeps hand edits to a generated map:

> Build them (Recommended)

## How it is read

The findings are `report-framework.md`'s F1-F11 and its seven recommendations; they are not
restated here. `report-artgen.md` (A1-A13) is work in artgen, a separate repository: this plan
changes only what the framework does with the engine as vendored, and leaves `pack.py`,
`route.py` and `mapcheck.py` in place until artgen takes them over.

| Finding | Read as |
|---|---|
| F1 | A way's position is stated once, in the tables. A write-up's Exits line carries none; the site and PDF add it. Prose naming a direction toward a cited room is checked against the same position. |
| F2, F3 | `Connection.bearing` and `distance` mean one thing everywhere: where the far end lies, as designed. They are optional, and a way between two placed rooms states neither, because the rooms' positions place it and the route gives the wall and the walk. |
| F4 | `pack` reads what it keeps from what is stored and writes only positions. A block records the router version its passages were routed by, so a router change is one stated event per block. Packing a packed block that still routes changes nothing. |
| F5 | The packer's fill and passage share are `BRIEF.md` levers. Wall weight, hatch and label sizes are how artgen draws, not what the build is built to, and stay in code (report 2, A9-A10). |
| F6 | `BRIEF.md` states each level's footprint, so the pyramid's widening and narrowing is written down and checked. Levels share a centre, so a stair stands over the stair it meets, and `pack` places it there. |
| F7 | `Room_Shape` gains `hall`, a room one passage wide. The content states it; the validator holds the dimensions to it; the tools draw it with its code alone. |
| F8 | Step 5 gains a map judgement check with a fixed viewing recipe. |
| F9 | A block's map is built from the tables whenever it is needed, and never committed. D7 now covers the terrain sheets only. |
| F10 | `tools/dungeon.py` holds a DANGEROUS block's drawing, packing and checks behind one entry each; `maps.py` and the validator call it. |
| F11 | A note of what artgen's dungeon and settlement files accept, beside `plans/sheet-maps/brief-engines.md`. |

Out of scope: packing the nine unpacked levels (C-F, H-L). That is content work this plan
makes cheaper: once it lands, packing a level costs only the prose directions the validator
names.
