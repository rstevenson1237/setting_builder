# Spec - maps drawn from the setting, in place of the mermaid diagrams

What `intake.md` asks for, as a design. Section 1 sets the aim, section 2 the Decisions,
3 to 8 the design, 9 the artgen work, 10 the checks, 11 what retires.

## 1. Aim

A setting is drawn on **sheets**, the way B2 is drawn on three: a play map per scale. Code
draws every map from the tables and a generated terrain; nothing is drawn by hand that a
table could state, and nothing a writer needs from a map reaches them as an image.

Plays like the reference when:

| Sheet | At the table |
|---|---|
| Frontier | A party picks a route on one grid, counted in squares: road or off it, round the marsh or through, which hill to climb. Every WILD location is a keyed mark; the keep and the ravine are marks with sheets of their own. |
| Ravine | Contours show which mouth is higher and how far apart they are. Each lair's entrance is keyed; nothing inside one is drawn. |
| Block | A lair's interior: numbered rooms to size, doors, traps, secret ways, exits labelled with the code they reach. |
| Keep | Numbered buildings inside walls and towers on a 10 ft grid, the ground and road outside it. |

Out of scope: a market town's streets and lots; an artistic finish beyond artgen's two
themes.

## 2. Decisions

| # | Decision | Settled as |
|---|---|---|
| D1 | Merge adjoining WILD regions into one, as the reference does | **No merge here; the workflow supports both.** A merged region is one region on a sheet, so nothing below assumes either. |
| D2 | Where sheets, ground and placement are requested | **`BRIEF.md`** (section 4). |
| D3 | What is committed | **Each map's JSON and `Ground.md`.** Renders are made by the site and PDF builds. |
| D4 | How artgen arrives, and how improvements flow back | **Recommended, for sign-off**: the current loop kept and made cheaper (section 12). |
| D5 | How a footprint and a place are written | **Typed fields** (5.1, 5.3): a footprint on Dressing, and `at` and `orientation` as direction, distance and unit, not strings. The agent turns fields back into prose for the reader. A review of every schema for the same gain is its own plan (`implementation.md` T0.4). |
| D6 | The ravine's scale | **Fit the sheet**: compress E, or coarsen the square where that plays better (it is already 10 yards, not 10 feet). |
| D7 | Hand edits to a generated map | **Only what no table states survives a rebuild.** A wrong map is fixed on the map. Drawing a map is also a review: what it shows wrong in the tables is offered to the user, and changed only on their word. |
| D8 | Drop the site's `plan_html` plan along with mermaid | **Yes.** One drawing path. |

## 3. Sheets

### 3.1 What a sheet is

A sheet is one terrain map at one scale: its square size, its extent in squares, its seed,
and the regions it holds. A region is **on** every sheet listing it; its **home** sheet is
the finest of them, and its map is a crop of that sheet around its area (3.3). A region on a
coarser sheet shows there as an area and its locations as marks.

DANGEROUS regions are on no sheet. They are drawn per block (section 6), and their entrances
are keyed on the sheet of the WILD region they open from.

### 3.2 Thornmarch's sheets

| Sheet | Square | Holds | Notes |
|---|---|---|---|
| Frontier | 200 yards | A B C D E | A and E show as marks: each has a finer sheet. |
| Ravine | 10 yards | E | Rendered scaled to fit the page. Keys F to M's entrances. |
| Keep | 10 feet | A | A dungeon layer over terrain (8.2). |

### 3.3 Crops

A region's map is its home sheet cropped to its area plus a margin, at the sheet's scale.
A location's cut is the same crop around one location. Because both are crops, two regions
never disagree at their edge, and the whole sheet is the printed play map, as the reference's
is.

## 4. The module overview in `BRIEF.md`

The `setting` node gains the sheets; each region node gains its ground and its place. All of
it is a request the solver must meet, and the validator reports which it does not.

```kdl
setting {
  sheet Frontier square="200 yards" extent="12 by 16 miles" regions="A B C D E"
  sheet Ravine square="10 yards" extent="500 by 160 yards" regions="E"
  sheet Keep square="10 feet" extent="220 by 180 yards" regions="A"
  ...
}
region C rating=WILD die=d6 locations=7 {
  ground forest "low hills to the north-east"
  place A north "0-1 mile"          // C's way in lies north of A's, within a mile
  place E south "12 miles"          // and 12 miles south of E's
  ...
}
```

- `ground` - the terrain the region's area requires (one of artgen's terrains), then prose
  the solver does not read and the writing does.
- `place` - another region's way in, the direction from it, and the distance. Two `place`
  lines fix a region; one leaves it free along an arc.
- Region adjacency, today `setting/region/Connections.mmd`, is a `Joins` column of the
  Regional Gazetteer, written at 3a from the outline. A cross-region Connection must join
  regions the gazetteer joins.

`--brief REGION` prints a region's slice as now, with its sheets.

## 5. Tables

### 5.1 Footprint, on Dressing

A footprint is typed, not prose. `Common_Schema.md` gains:

```kdl
value feet                    // a whole number of feet
enum Room_Shape rect round octagon cave
```

and Dressing, in DANGEROUS and SAFE, gains:

```kdl
  width feet                  // across, west to east as the room lies; a round room's diameter
  length feet                 // north to south
  height feet opt             // floor to roof, where it matters at the table
  shape Room_Shape opt        // rect where unset
```

- Required on every DANGEROUS Dressing; on SAFE, where the location is a building drawn to
  size. A SAFE location without them is a mark.
- `layout` no longer states a size: `"Den fifteen by twelve feet, wires over bed"` becomes
  `width=15 length=12 layout="Wires over the bed"`.
- WILD locations stay points: a landmark is a mark on its sheet, as in the reference.

DANGEROUS Location keeps no `at`: a room's place is walked from its block's entrance along
`Connections.md`'s orientations, as `site_common.positions()` does today.

### 5.2 Blocks

A new table, `setting/region/[Code]/Blocks.md`, for DANGEROUS (required) and SAFE (optional):

```kdl
Block F.a name="The Warren" locations="F.1, F.2, F.3, F.4, F.5"
Block A.a name="The Outer Bailey" locations="A.1, A.2, ..." wall="20 feet, walk on top" towers="round, at each corner and two at the gate"
```

- A block is one level. Every location of the region is in exactly one block.
- A Connection between two rooms of one block never goes up or down; one that does joins
  two blocks.
- A single holding is one block unless it changes level. A collection is several.
- `wall` and `towers` (SAFE only) give the enclosure drawn round the block's locations.
- The block's map is `setting/region/[Code]/[Block].json`.

### 5.3 Places, typed

`at` and `orientation` are strings today, taken apart by a pattern in `site_common.py`. A
map is walked from them, so they become typed:

```kdl
enum Compass north north-north-east north-east east-north-east east east-south-east
             south-east south-south-east south south-south-west south-west
             west-south-west west west-north-west north-west north-north-west
enum Distance_Unit feet yards miles
value distance                // a number then a Distance_Unit: 40 feet, 1.5 miles
```

- `at` becomes `bearing=Compass distance=distance`, or `north=distance east=distance` (a
  negative for south or west), or `at="way in"`.
- `orientation` becomes `bearing`, `distance` and `climb` (feet up, negative down; a change
  of level is a climb across blocks).
- `site_common.parse_at` and its two patterns retire; the validator rejects what does not
  parse rather than skipping it.

### 5.4 `Connections.md` written at 4b

The edges the mermaid graph held are written straight into `Connections.md` at 4b, one
entry per side with `to` and `orientation` set and the rest a stub; 4c fills nothing there
it did not before. Orientation is needed this early because every map is walked from it.

## 6. Dangerous: one map per block

`tools/maps.py` builds a block's dungeon from the tables:

1. Its entrance is the room a Connection reaches from outside the block.
2. Each room is placed by walking orientations from the entrance, then drawn at its Dressing's
   `width`, `length` and `shape`, centred on its place.
3. Each Connection inside the block is a corridor; its door is the Connection's type
   (`Open`, `Crude`, `Broken`, `Archway` none; `Wooden`, `Banded`, `Stone` door; `Iron`
   portcullis), overridden by `Lock` (locked) or `Secret` (secret). A `Hazard` is a trap
   mark on the corridor.
4. A Connection out of the block is a corridor to the map's edge, labelled with its code:
   `to E.2`, `up to M.14`.
5. A location's cut is the block map cropped to its room and its doors.

On the Ravine sheet each block's entrance is a cave-mouth mark at the WILD location its
Connection reaches (F.1 to E.2), keyed with the region's code.

## 7. Terrain sheets

### 7.1 Placement first

At 3b, `tools/maps.py place`:

1. Places each region's way in on each sheet from the `place` lines: a small constraint
   solve, every distance and direction met within a tolerance, the rest of the sheet free.
2. Gives each placed region an area, grown from its way in to the size its locations need,
   and turns `ground` into a requirement over that area.
3. Asks artgen for terrain meeting every requirement (9, A2), then checks it. An unmet
   requirement is reported by name; the solver reseeds only after adjusting what it can.
4. Writes each sheet's JSON and `setting/Sheets.md`: each region's way in, as squares on each
   sheet it is on.

Locations are written later (4a), against the ground already there.

### 7.2 What the writing reads: `Ground.md`

Each region gets `setting/region/[Code]/Ground.md`, written by code, never by hand:

```kdl
Ground C way-in="Frontier 24,52" ground="forest 92%, marsh 8%" {
  Feature "stream" from="north-west, 6 miles" to="south, 1 mile"
  Feature "hill" at="north-east, 7 miles" height="180 feet"
}
At C.4 ground="forest" height="140 feet" slope="gentle" note="on a rise above the trail"
```

- Before 4a it holds the region's features in `at` terms, so locations are placed on real
  ground.
- After 4a it adds one `At` per location: ground, height, slope.
- For the Ravine, each entrance's height above the floor. A Layout reads it and may say
  "the orc mouth is 60 feet up the west wall".

It is the only map output a step reads. Its size is counted by `tools/metrics.py`.

## 8. SAFE

### 8.1 Drawn as a block over terrain

A SAFE region's home sheet holds the ground and road. Each block with a `wall` is drawn as
walls with towers at the vertices of the hull of its locations' footprints, with a gate
where a Gate location sits. Each building is a room drawn at its Dressing's footprint, no rock hatching. A location
with no footprint is a mark.

### 8.2 What this leaves rough

Lanes, yards and lots are not generated. The draft is a fort plan: enough for a keep, a
manor or a walled village.

## 9. artgen work

The project is ours, so missing pieces are built there, from briefs written here and run
in an artgen session. How a finished item reaches this repo is D4's.

| # | Feature | Used by |
|---|---|---|
| A1 | The map and dungeon engines usable without the pixel-art pipeline, in whatever form D4 settles | D4 |
| A2 | Constrained generation: `require` entries in `map.json` (area, terrain, height band, stream or road path); `map check` lists each unmet | 7.1 |
| A3 | `map facts` / `dungeon facts`: features, and terrain, height and slope at given points, as JSON | 7.2 |
| A4 | Crop render: `--crop x,y,w,h`, `--room id --margin n`, `--fit WxH` | 3.3, 6 |
| A5 | A dungeon over a terrain underlay; `wall` with towers and gate; no hatching | 8.1 |
| A6 | Symbols: cave mouth (terrain), curtain, dais, stairs up and down distinct | 6, reference key |
| A7 | Label and stroke size against the page, not the square | legibility on scaled sheets |
| A8 | Hand edits kept when rooms and placements are regenerated | D7 |

Token cost stays near zero: code calls the CLI with `--json`, and no step reads a render.

## 10. Checks

`tools/validate_setting.py` gains, for every rule above:

- Every sheet in `BRIEF.md` exists in `setting/Sheets.md` and as JSON; every `place` and
  `ground` request is met, or reported by name.
- Every WILD and SAFE location's `at` lies on its home sheet; outside its region's area is a
  warning.
- Every DANGEROUS location is in exactly one block, has a footprint, and is reached from its
  block's entrance; two routes placing a room apart, or two footprints overlapping, is an
  error.
- No same-block Connection goes up or down.
- A cross-region Connection joins regions the gazetteer `Joins`.
- `Ground.md` matches what `maps.py` would write now; stale is a warning sent to 4d.
- `build_site.py --check` and `build_pdf.py --check` fail a map left out.

## 11. What retires

| Retires | Replaced by |
|---|---|
| `setting/region/Connections.mmd`, `templates/region/Connections.mmd` | Gazetteer `Joins`; the Frontier sheet as the region map |
| Each `setting/region/[Code]/Connections.mmd`, three rating templates | `Connections.md` at 4b; `Blocks.md`; maps |
| Mermaid in `build_site.py`, `app.js`, the CDN script | Inline SVG maps; connection text read from `Connections.md` |
| `describe_edges` / `mmd_edges_by_code` / `load_mmd` in `site_common.py` | The same lists read from `Connections.md` |
| `plan_html` and its plan | Block and region maps (D8) |
| `.mmd` in `TEMPLATE_CITE_RE`, `parse_mmd_edges`, the 3b two-way claim | Section 10's checks |

Step ids 3b and 4b keep their numbers and change their content; 4d is new (implementation
T2.6). Nothing is renumbered.

## 12. D4 - tools that move in step

### 12.1 The loop today

A consumer tests a tool against its own work, writes a brief of the findings, the brief is
taken into the tool's repo, and the change ships in a release the consumer then installs.
It works and gives back; its cost is the wait for a release, and that nothing in the tool
guards the consumer's case once the brief is closed.

### 12.2 The rule, for any tool and any consumer

1. **The brief carries its evidence.** The consumer's scratch prototype and its output
   (the evaluation's converters and renders, here) go with the findings, so the tool's
   session starts from working code, not a description.
2. **The consumer's cases become the tool's fixtures.** A brief lands with the consumer's
   real inputs as test fixtures in the tool (for artgen: F's block, the ravine, the keep).
   Every later change to the tool is tested against every consumer, which is how one
   project's need improves the whole suite and is never broken by the next.
3. **Pin by commit, release when it suits.** artgen's `artgen-dist` branch is installable at
   any commit (`#<sha>`), so a consumer takes a landed change at once; a tagged release
   gathers several. Upgrading is its own commit in the consumer, passing the consumer's
   checks.
4. **A versioned contract.** The CLI's JSON and file formats carry a version; a consumer
   states the one it reads, and a breaking change bumps it.
5. **Briefs on both sides.** The consumer keeps its brief and the commit it pinned in its
   plan; the tool keeps the brief that produced each change.

Whatever the consumer needs that the tool lacks is never built in the consumer beyond a
prototype; it goes back as a brief.
