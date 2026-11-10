# Brief - symbols, and sizes against the page (artgen A6, A7)

For an artgen session in `rstevenson1237/image_tools`, from setting_builder's sheet-maps plan
(`implementation.md` T2.5; `spec.md` 9 A6 and A7). It needs `brief-crop.md`: page size comes
from `--fit`.

A map is read at the table, at print size. Every mark a player or referee must tell apart has
its own symbol in the key, and every label is readable on the page it is printed on, whatever
the square.

## What phase 1 found

- **A6, symbols.** The Ravine's cave mouths are the stock map `cave`, which says nothing about
  which wall a mouth is in. The Keep's gates have no symbol. M.6's crypt stair drew as a small
  notch with no direction. Dungeon `stairs` has one form ("rise to the right"). Whether stairs
  up and down could be told apart was not tested, but the symbol set has no way to.
- **A7, sizes.** Label and stroke sizes scale with `ppu` (`u = k / 40` in both renderers), so
  they follow the square, not the page:
  - On the Ravine, at 10 yards a square, labels are 0.5 square and unreadable on the strip.
  - On the Frontier, at page size, the castle mark and its labels are small.

## What to build

1. **Symbols** (additions; the format version is unchanged):
   - Map `cave-mouth` with an `angle`: an opening in a cliff line, facing its angle. The map
     symbol gains `angle`, as the dungeon symbol already has.
   - Map `gate`: a break in a wall line, for a keep's or town's gate seen on a terrain sheet.
   - Dungeon `stairs-up` and `stairs-down`, distinct at a glance, each pointing its `angle`
     the way it climbs or falls. Plain `stairs` stays.
   - Dungeon `curtain`, along a room edge or across a passage. Dungeon `dais`, a raised floor
     drawn by its outline.
   - Every new symbol is in `map symbols` and `dungeon symbols`, and in the legend when used.
2. **Sizes against the page.**
   - Render takes a page scale: from `--fit`, or `--page-scale` in output pixels per
     millimetre.
   - Label sizes, symbol sizes and stroke widths are then set in points on the page. Stated
     defaults: place labels 9 pt, notes 7 pt, room numbers 8 pt, symbols 5 mm.
   - A label's `size` is a multiple of its kind's default.
   - Without a page scale, sizes follow `ppu` as now, so existing files render as before.
3. **Labels kept off one another.** With a page scale set, a label that would overlap another
   label or a symbol is moved to the nearest free side of its anchor. `--json` reports any
   label it could not place.

## The cases

| Case | Change | Facts the test holds it to |
|---|---|---|
| `ravine` (exists) | Mouths as `cave-mouth`, angled to face across the gorge. Rendered `--fit 180x260mm`. | Every place label is at least 7 pt on the page. No two labels overlap. The west-wall mouths face east and the east-wall ones face west. |
| `frontier` (from `brief-constraints.md`) | Rendered `--fit 260x180mm`, with A as `castle` | Region labels 9 pt or more. The castle mark is 5 mm. |
| `shrine-crypts` (from `brief-engines.md`) | M.6 as `stairs-up` toward M.2; M.13 as `stairs-down` toward L.5 | The two stair symbols differ in the SVG. Each points its angle. |
| `keep` (exists) | A.1 and A.2 as dungeon `door` until `brief-underlay.md` gives gates; A.10 with a `dais` | `dais` is in the legend |

## Done when

- Each new symbol is drawn, listed and in the legend, each covered by a test.
- With a page scale, sizes hold to the point sizes above at three page sizes. Without one,
  every existing fixture renders as before.
- The CHANGELOG lists the symbols and the page-scale defaults.

## setting_builder's side

- T3.8's `draw` passes the site's and the PDF's page sizes as `--fit`.
- `tools/maps.py` takes each mark's symbol from the table that states it:
  - a WILD mouth's `cave-mouth`, from the Connection that reaches its DANGEROUS region;
  - a stair, from a Connection's `climb`;
  - a `curtain` or `dais`, from Dressing `layout`, until typed-fields types them.
- T5.2 checks legibility on every sheet.
