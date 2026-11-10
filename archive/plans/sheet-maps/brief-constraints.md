# Brief - constrained generation and `map check` (artgen A2)

For an artgen session in `rstevenson1237/image_tools`, from setting_builder's sheet-maps plan
(`implementation.md` T2.4; `spec.md` 7.1 and 9 A2). It needs `brief-engines.md` and
`brief-facts.md`: `check` measures through `facts`.

setting_builder places each region's way in on a sheet from its brief, gives each region an
area, and states the ground that area must have. It then asks artgen for terrain that meets
every requirement, with the rest of the sheet left free. An unmet requirement must be reported
by name, so the remedy goes to the brief and not to a blind reseed.

## What phase 1 found

On the Frontier (A to E, 200 yards a square, 106 x 141), built with `paint` and `elevate`:

- **Painted areas are hard rectangles.** `paint` overwrites terrain after simplification
  (`generateMap`), so a forest asked for by polygon ends at a straight edge.
- **Contours ignore painted terrain.** A painted `rock` plateau is flat, and a painted `marsh`
  can sit on a hill. Height and terrain are classified together (`classify`), but a paint
  bypasses height.
- **Unasked rivers.** The generator traced a river that nothing in the brief asked for, across
  the road. `gen.rivers` is a count, not "only these".
- **Nothing says what was missed.** Whether C ended up forest, or the road kept to open
  ground, had to be judged by eye.

## What to build

1. **`require` in `map.json`**, an optional list (a format extension). Each entry has an `id`
   the consumer chooses, and one of:
   - `terrain`: an `area` (a shape, as edits take), a terrain, and the share it needs, such as
     `forest` at 0.8 or more.
   - `height`: an `area` and a band, low and high, in `topo.unit`.
   - `path`: `stream` or `road`, through given points within a tolerance.
   - `clear`: an `area` that no generated river or road may cross.
2. **Generation shapes ground to the requirements.** It does not paint over the ground.
   - A terrain requirement biases moisture and height inside its area, with the edge blended
     over `feature`, so a forest has a forest's edge and a marsh lies low.
   - A height band raises or lowers the field before classification, so contours follow it.
   - A `stream` path carves its valley; a `road` path keeps to its points and prefers gentle
     slope between them.
   - Generated rivers stay out of every `clear` area. With `gen.rivers` at 0, only required
     streams exist.
3. **`artgen map check --file … --json`** lists every requirement with what it measured and
   whether it is met: `C-forest terrain forest 0.71 < 0.80 unmet`. It exits non-zero when any
   is unmet. It also reports the format errors `dungeon check` reports.
4. **Fixed by seed.** The same file gives the same field. artgen never reseeds by itself.
   A consumer that reseeds does so knowing which requirement failed.

## The cases

| Case | What it is | Facts the test holds it to |
|---|---|---|
| `frontier` (new) | The Frontier at 200 yards a square, 106 x 141, with requirements from Thornmarch's outline, listed below | `check` reports every requirement met at the committed seed. No generated river crosses `B-road-clear`. C's forest edge is not a straight line: no run of more than 4 squares along one row or column. |
| `frontier-unmet` | `frontier` with C needing `rock` at 0.9 over the same area as its forest | `check` exits non-zero and names `C-ground` alone |
| `ravine` (exists) | Rebuilt with `require` in place of the hand `paint` and `elevate` edits: rock walls at 30 to 40 feet, a stream up the path | `check` is met. The walls' contours run along the gorge, not across it. |

`frontier` requirements, from `BRIEF.md`'s outline (setting_builder writes these itself from
T3.6 on):

- `A-ground`: a rise at the road's end, height 20 to 60 feet over a disc round A's way in.
- `B-road`: a road from the south edge to A's way in. `B-road-clear` keeps rivers off it.
- `C-ground`: forest at 0.8 or more between A and E, round the forest trail.
- `D-ground`: marsh at 0.7 or more beside the road, low, at 0 to 10 feet.
- `E-ground`: rock at 0.6 or more, hills 150 to 400 feet, in the north.
- `E-stream`: a stream down E's area to the wood.

Build the areas from the hand placement in `findings.md` T1.3, and record the
setting_builder sha in `case.md`.

## Done when

- Each `require` kind is met on `frontier`, and `check` names each unmet one on
  `frontier-unmet`, each covered by a test.
- A painted map with no `require` renders as it did. The format version is unchanged.
- The CHANGELOG describes `require` and `check`.

## setting_builder's side

T3.6's `tools/maps.py place` writes each sheet's `require` from the `ground` and `place` lines
in `BRIEF.md`, runs `check`, and reports each unmet requirement against the `BRIEF.md` line
that asked for it.
