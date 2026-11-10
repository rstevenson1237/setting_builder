# Brief - crop and fit renders (artgen A4)

For an artgen session in `rstevenson1237/image_tools`, from setting_builder's sheet-maps plan
(`implementation.md` T2.3; `spec.md` 3.3, 6 and 9 A4). It needs `brief-engines.md`.

setting_builder prints each sheet whole as its play map. It also prints each region's map as a
crop of its sheet, and each location's cut as a crop of its region's map or its block's map.
Because every map is a crop of one sheet, two regions never disagree at their shared edge.

## What phase 1 found

- **The Ravine is only usable cut up.** At 16 x 184 squares, the whole page is a 1:11 strip
  and its labels are unreadable. A stretch round E.2 was legible.
- **F and M need per-location cuts.** A location's write-up shows its own room and its doors,
  not the whole block.
- **The page sets the size, not the map.** `render` takes `--ppu` only, so a consumer must
  work out the pixels per unit for each page.

## What to build

1. **`--crop x,y,w,h`** on `map render` and `dungeon render`, in map units or cells. The
   crop is a window on the full render: the terrain, contours, rivers and labels inside it
   match the full sheet's, and nothing is regenerated for the window. A label or symbol cut
   by the window edge is drawn clipped, never moved.
2. **`--room id [--margin n]`** on `dungeon render`: the crop round one room, its doors and
   the first `n` cells of each corridor. Several `--room` flags crop round all of them.
3. **`--fit WxH[mm|px]`**: choose `ppu` so the crop, or the whole map, fits the box with its
   aspect kept. SVG carries the size in the unit given.
4. **Furniture follows the crop.** The legend, scale bar and compass are placed inside the
   crop's frame. Grid coordinates stay the full sheet's, so a square on a region map has the
   same name as on the sheet.
5. **`--json`** reports the crop in map units and the `ppu` chosen.

## The cases

| Case | Render | Facts the test holds it to |
|---|---|---|
| `ravine` (exists) | `--crop` a 16 x 46 stretch round E.2 | The SVG's terrain paths inside the window are the same as the full render's, clipped. The scale bar reads in yards. |
| `ravine` | `--fit 180x260mm` whole | `ppu` is chosen so the long side fits, and the SVG is 180 mm wide or 260 mm tall |
| `warren` (exists) | `--room` F.3 `--margin 2` | The crop holds F.3, the doors to F.4 and F.5, and the start of the corridor to F.2. It holds no other room whole. |
| `keep` (exists) | `--room` for A.9 and A.13 | One crop round both rooms |

## Done when

- Crop, room and fit work on both kinds, each covered by a test.
- A crop of a fixture equals the full render clipped to the window, checked on the SVG
  structure.
- The CHANGELOG lists the flags.

## setting_builder's side

T3.8's `tools/maps.py draw` renders each sheet whole, each region as `--crop` of its home
sheet round its area, and each location cut as `--room` or a crop round its mark. All are
fitted to the site's column and the PDF's page.
