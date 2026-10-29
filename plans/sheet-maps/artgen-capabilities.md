# artgen capabilities - what the framework writes, and how it behaves

Against artgen-maps 0.11.0, the commit `brief-engines.md` records and `tools/artgen/VERSION`
holds. `node tools/artgen/artgen-maps.js --help` lists the commands; this note lists what
`tools/maps.py` and `tools/dungeon.py` put in a file instead, and what a render does with it,
as observed. What artgen lacks, and what the framework built round it, is
`plans/dungeon-maps/report-artgen.md`. Check each line again when the engine is upgraded.

## Every file

- `artgen <engine> check --file F --json` lists errors with their JSON paths, then warnings.
  It exits 1 on an error; warnings never fail it.
- `render --format svg --fit WxH(mm|px) --json --out DIR` sizes labels and strokes for the page,
  and its JSON lists in `unplaced` each overlay label it found no room for. Room labels are
  never in that list.
- Sides are cells: a map at most 200 a side, a dungeon 160, a settlement 240.

## Dungeon (`dungeon.block_map`)

| Key | What it does |
|---|---|
| `scale.perCell`, `unit` | Feet a cell. A corridor's `width` and every position are in cells, so a 10-ft passage is 2 on a 5-ft grid. |
| `rooms[]` `shape` | `rect`, `circle`, `octagon`, `cave`; the framework draws a `hall` as `rect`. |
| `rooms[]` `number` | A badge above the code, both at the room's centre and never moved. `false` drops the badge. |
| `corridors[]` `from`/`to` | `{room, side n|e|s|w, offset}`: `offset` is cells along that wall from the room's x or y. With no offset, artgen picks one. |
| `corridors[]` `via` | Bends, as flat `x, y` pairs: with ports, enough to draw any right-angled route exactly. |
| `corridors[]` `route` | `auto`, `hv`, `vh`, `straight`, `around`. These are hints, and `around` can still cross rooms. |
| `corridors[]` `doors` | `[from, to]` kinds or `null`. `style: "natural"` draws a rough-cut passage. |
| `connections[]` | `{a, b, at, kind}`: a door or opening in the wall two touching rooms share. |
| `style.sharedWalls` | A wall between touching rooms. When unset it is on only if the file has a `connection` or a `block`, so set it explicitly. |
| `style.wall` | One stroke factor for outlines and partitions alike. The framework uses 2.5 on a packed level. |
| `style.hatch` | `band` leaves voids inside a dense level; `full` hatches all the rock. |
| `overlay.symbols[]` | `stairs-up`, `stairs-down`, `arrow`, `trap`. `angle` is in degrees, 0 east, clockwise (inferred from renders). |
| `overlay.labels[]` | `kind` `name`, `note` or `area`. Notes are placed clear of each other only under `--fit`. |

- A corridor run along a room's wall gets no wall between them: partitions are drawn only
  between two rooms. `tools/route.py` keeps passages a cell off every wall but their doors'.
- `render --room CODE --margin N` crops round a room, its doors and the first cells of each
  corridor. The location cuts use it.
- `facts --json` gives each room's box and doors, each corridor's ends and length, overlaps and
  unreached rooms, but no corridor path, door wall or floor. That is why `tools/mapcheck.py`
  rebuilds the floor itself.

## Settlement (`maps.settlement_map`)

| Key | What it does |
|---|---|
| `kind` | `hamlet`, `village`, `town`, `city`, `castle`. The framework writes `castle`, with its own walls. |
| `buildings[]` | `{id, kind, shape, x, y, w, h, label, number}`, with `kind` from the names the engine draws (inn, shop, hall, chapel, ...). |
| `walls[]` | `{kind, points, closed, gates: [{at, kind postern|gatehouse}], towers: {shape}}`. |
| `roads[]`, `water[]`, `areas[]` | Polylines and polygons in cells, each with a `kind`. |
| `underlay` | `{map, origin, scale}`: a terrain map drawn beneath, its path relative to the file. |
| `overlay.labels[]` | `kind` `name`, `note`, `area` or `street`. `water` is refused here, though a terrain map takes it. |
