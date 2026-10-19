# Brief - terrain underlay, walls, towers and gates (artgen A5)

For an artgen session in `rstevenson1237/image_tools`, from setting_builder's sheet-maps plan
(`implementation.md` T2.7; `spec.md` 8 and 9 A5). It needs `brief-crop.md`, and
`brief-symbols.md` for `gate`.

A SAFE region is drawn as a fort plan: numbered buildings inside walls and towers, on a 10 ft
grid, with the ground and the road outside. Its terrain comes from its home sheet. Its
buildings come from its tables, each drawn at its Dressing's footprint. Lanes, yards and lots
are not generated (`spec.md` 8.2).

## What phase 1 found

The Keep (A's thirteen locations, hatching off) drew as scattered rectangles on white:

- **No ground.** A dungeon has no terrain, so the road, the rise the keep stands on, and the
  wood beyond the postern are missing.
- **No enclosure.** Nothing draws a wall, its towers or its gates, so the bailey is not there.
- **Fills read as rooms underground.** With hatching off, buildings are white boxes with a
  dungeon's thick walls. A building, a yard and a cellar look the same.
- **Levels overlap.** A.12 and A.13 drew under A.4 and A.10, and A.9 and A.13 touch and read as
  one room. setting_builder's Blocks split these by level (T3.2), so artgen needs nothing for
  it beyond A3's overlap report.

## What to build

1. **`underlay` in `dungeon.json`**, optional, so the format version is unchanged.
   - It names a map file, an origin in that map's units, and the scale between them. The
     Keep sheet is 10 ft a square; a dungeon cell is 5 ft.
   - The render draws the map's terrain, contours and roads under the rooms, cropped to the
     dungeon's extent, by A4's crop.
   - The map's own legend, title and compass are off; the dungeon's are kept.
2. **`walls`**, an optional list. Each wall has:
   - `rooms`, the ids it encloses, or a `poly`;
   - a `thickness` and an `inset`, in cells;
   - `towers`: `round` or `square`, a size, and where they stand (`corners`, or a list of
     vertex indices);
   - `gates`: each a point on the wall, a `kind` (`gate`, `postern`), and an optional room id
     it opens into.

   From `rooms`, the wall follows the convex hull of their footprints plus the inset. A gate
   is drawn as A6's `gate` symbol set into the wall, with a tower each side for `gate` and
   none for `postern`.
3. **Room `fill`**: `floor` (as now), `building` (roofed, a plain tone, thin walls), `yard`
   (open ground, no walls, the underlay showing through) or `cellar` (dashed outline, drawn
   above everything else). It is optional, and defaults to `floor`.
4. **`hatch: none` with an underlay** shows the underlay between rooms, not white.

## The cases

| Case | Change | Facts the test holds it to |
|---|---|---|
| `keep` (exists) | Upper-level rooms only: A.1 to A.11, with A.12 and A.13 in a separate `keep-cellars` file. An underlay of a 66 x 54 square map at 10 ft (the Keep sheet's extent, 220 by 180 yards) with the road running to A.1. One wall round A.1 to A.11, round towers at the corners, a `gate` at A.1 and a `postern` at A.2. A.8 `yard`, the rest `building`. | The wall encloses every upper room. Towers at every hull corner. Two gates, the main one with two towers. The road reaches the main gate. A.8 shows the underlay. |
| `keep-cellars` (new) | A.12 and A.13 as `cellar`, the same underlay | Both drawn dashed. No wall. |

Take the footprints from `setting/region/A/Brief.md`, as `brief-fixtures.md`'s command does,
and the places from each Location's `at`. T4.6 will set each building's place with its
footprint (`findings.md`); until then, nudge rooms off one another by hand in the fixture, and
note it in `case.md`.

## Done when

- Underlay, walls, towers, gates and fills render on `keep` and `keep-cellars`, each covered by
  a test.
- Every existing dungeon fixture renders as before.
- The CHANGELOG describes `underlay`, `walls` and `fill`.

## setting_builder's side

- T3.8's `draw` renders each SAFE block over a crop of its home sheet. It takes the block's
  `wall` and `towers` from `Blocks.md`, each building's footprint from its Dressing, and each
  gate from a Gate location.
- T5.1 judges the Keep as a fort plan.
