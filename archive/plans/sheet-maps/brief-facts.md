# Brief - facts read back from a map (artgen A3)

For an artgen session in `rstevenson1237/image_tools`, from setting_builder's sheet-maps plan
(`implementation.md` T2.2; `spec.md` 7.2 and 9 A3). It needs `brief-engines.md` (path mode).

setting_builder's writers never see a render. What they need from a map reaches them as
`Ground.md`, a file of facts by location code that code writes from the map. artgen has no way
to give those facts.

## What phase 1 found

- No command reads terrain, height or slope back from a map. `generateMap` holds them
  (`MapField.elevation`, `terrain`, `rivers`, `roads`), but only the renderer uses them.
- The facts `Ground.md` needs, from `spec.md` 7.2:

  ```kdl
  Ground C way-in="Frontier 24,52" ground="forest 92%, marsh 8%" {
    Feature "stream" from="north-west, 6 miles" to="south, 1 mile"
    Feature "hill" at="north-east, 7 miles" height="180 feet"
  }
  At C.4 ground="forest" height="140 feet" slope="gentle" note="on a rise above the trail"
  ```

  For the Ravine it also needs each cave mouth's height above the stream.
- A dungeon's facts are needed by the validator, not the writers. These are the rooms that
  overlap, the rooms no corridor reaches, and where each exit leaves the map. The `keep`
  fixture's A.12 under A.4 is an overlap that went unreported.

## What to build

All in map units and in the map's own scale unit. Every result carries `version`.

1. **`artgen map facts --file … --json [--at x,y …] [--area x,y,x,y,…]`**
   - For each point: the terrain, the height in `topo.unit`, the slope (the gradient in
     `topo.unit` per `scale.unit`, and a band: flat, gentle, steep, cliff), and the distance to
     the nearest river and road.
   - For each area: the share of each terrain, the lowest and highest ground, and the rivers
     and roads that cross it, with where each enters and leaves.
   - With neither: the whole map's features, which are the rivers and roads as point lists,
     the hilltops and hollows with their heights, and each terrain's share.
   - `--above river|lowest` gives each point's height above the nearest river, or above the
     lowest ground within `--radius`. This is the Ravine's "60 feet up the west wall".
2. **`artgen dungeon facts --file … --json`**
   - Each room's box in cells and in feet, its shape, and its doors.
   - Each corridor's ends, doors and length.
   - Each exit's point and the map edge it leaves by.
   - The overlaps (room pairs and the cells they share) and the rooms no corridor reaches.
3. **Stable.** The same file gives the same facts, to a stated rounding: heights to the topo
   interval, shares to whole percent. A change to that rounding is a format change.

The consumer turns map units into compass and distance itself. artgen states positions, not
bearings.

## The cases

| Case | Query | Facts the test holds it to |
|---|---|---|
| `ravine` (exists) | `--at` each of the eleven marks, `--above river` | Every mark reports terrain `rock` or `water`. The west-wall marks are higher above the river than the river's own points. Heights are whole multiples of the topo interval. |
| `ravine` | no query | The road, and the river the edits drew, each a point list that runs the length of the map. A generated river (`gen.rivers` is 1) is reported apart from it. |
| `keep` (exists) | `dungeon facts` | Thirteen rooms at their sizes. The overlaps A.12/A.4 and A.13/A.10 are reported. |
| `warren` (exists) | `dungeon facts` | Five rooms, four corridors between rooms, one exit, no overlaps, no unreached rooms |

## Done when

- Both commands run by `--file`, with each field covered by a test.
- The same file gives byte-identical `--json` twice.
- The CHANGELOG states the rounding and that it is part of the format.

## setting_builder's side

- T3.7's `tools/maps.py ground` calls `map facts` per region and `dungeon facts` per block,
  and writes `Ground.md` from the results. It never reads the JSON's field arrays itself.
- T3.10's validator reads `dungeon facts` for overlaps and unreached rooms.
