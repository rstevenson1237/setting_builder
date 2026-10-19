# Findings - phase 1, artgen as it is

`implementation.md` T1.1 to T1.5. artgen installed from `artgen-dist` into a scratch game;
the prototype converters in `prototype/` run from the repo root, the Frontier built by hand
with `artgen map` commands from the outline. Sizes in feet are from each `Brief.md`.

## What rendered

| Task | Run | Result |
|---|---|---|
| T1.1 | F (`F.1=8x1 F.2=8x1 F.3=6x6 F.4=4x3 F.5=3x2`) | Draws as `spec.md` 6 asks: five rooms to size, two doors, two trap marks, the exit corridor labelled `to E.2`. |
| T1.1 | M, all fourteen rooms on one canvas | Draws, but the crypt (level -1) lies over the stair-hall level: M.8 over M.7, M.6 over M.2, M.13 inside M.8's gallery. Four blocks, one per level, are needed, as `spec.md` 5.2 says. |
| T1.2 | E at 10 yards, river up the path, rock walls hand-painted four squares either side | Renders at 16 x 184 squares. Legible at native size; as a whole page it is a 1:11 strip. Ledge marks and labels are readable only zoomed in. |
| T1.3 | A to E on a 200-yard sheet, 106 x 141 squares | Renders. Terrain areas painted by polygon are hard rectangles; contours ignore the painted terrain and the rock plateau is flat. |
| T1.4 | A's thirteen buildings, hatching off | Renders as scattered rectangles: no walls, towers or ground; A.12 and A.13 draw under A.4 and A.10; A.9 and A.13 touch and read as one room. |

## Per item

| # | Finding | Verdict |
|---|---|---|
| A1 | Both converters call the CLI as a subprocess; nothing here needed the pixel-art pipeline | Confirmed |
| A2 | The Frontier needed every region's area by hand, and the generator added a river nothing asked for. Needed: `require` for area, terrain, a height band and a stream or road path, and a check that lists each unmet | Confirmed |
| A3 | Not exercised: no command reads terrain, height or slope back from a map, so `Ground.md`'s facts would have to be read from the JSON by hand. `facts` is needed | Confirmed |
| A4 | A crop is wanted at once: the Ravine strip is only usable cut into stretches (a stretch round E.2 was legible, the whole page was not), and F and M need per-location cuts | Confirmed |
| A5 | The Keep drew rooms on white. It needs the terrain underneath, a wall with towers and a gate, and a fill that is not rock | Confirmed |
| A6 | The ravine's cave mark is the stock `cave` and the Keep's gate has none; M.6's crypt stair draws as a small notch with no direction. Not tested: whether stairs up and down differ | Confirmed as in `spec.md` 9 |
| A7 | Labels are 0.5 square at 10 yards and unreadable on the strip; on the Frontier the castle mark and labels are small at page size. Label and stroke size must follow the page | Confirmed |
| A8 | No hand edit survived: the converters delete a map to rebuild it, so the Ravine's river and walls were reapplied on each run | Confirmed |

## For the later tasks

- The converters' position walk puts rooms from different levels on one plane; `maps.py`
  walks per block, so this goes away with T3.2's `Blocks.md`.
- A WILD location is a mark, not a room, so E's twelve marks fit a map with no footprint.
- The Keep's rooms spread over 113 x 77 squares of 5 feet because `at` is in yards; a SAFE
  building's `at` is its centre, so T4.6 must set each building's place with its footprint.
- `to_map.py` takes hand edits as strings. A8 replaces that, and `Ground.md` (7.2) reads the
  result, so the edits are the part that must be kept.
