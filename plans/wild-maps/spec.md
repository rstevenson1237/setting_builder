# Spec - wild maps

Tick a line to approve it. Each was tried; what the trial proved stands under it.

- [ ] **W1. A sheet states its ground.** `sheet Sands ... ground=sand`: the terrain artgen fills with wherever
  no region's `ground` reaches, in place of its own choice. A region's `ground` line still wins inside its area.
  *Built.* The sheet is painted its ground, each region's ground painted over its area, with no generated river
  and no tempering; a region's terrain requirement stays, so its area keeps flat. Sands is all sand, Lake all rock,
  and a block's settlement ground follows its region's (sand, stone).
- [ ] **W2. Regions A and B are designed (step 3e).** A `design` line for each in `BRIEF.md`; a `Street` for each
  street the seed names (A's grid past the ruins, B's quay round the lake), a `Tie` for each place the seed
  fixes. Solved, shown and approved as any design.
  *Built, approved and applied* (A seed 1, score 70; B seed 9, score 80). With streets, `settlement layout` broke
  every tie (it turns the whole layout to straighten a street); so every place the ties reach, or the tables place by
  `xyz`, now stands fixed and the solve lays only the streets. A's faults are its grid's crossings and A.1 touching
  the pyramid's tip; B's are the quay's bends round the lake. An approved design's streets are drawn on the map.
- [ ] **W3. Fabric: what stands between the keyed places.** One line in a SAFE or WILD design,
  `Fabric [Block] kind=ruin share="40%"`, drawn as unkeyed buildings of that kind along the streets, from the
  design's seed.
  *Built, on the framework's side.* The spike: `settlement gen` keeps placed buildings but lays its own town across
  them; `settlement layout` collapses unkeyed buildings between fixed places to the centre. So `maps.fabric` lots
  each street front from the design's seed, clear of every place and street. The engine's gap is image_tools#67.
- [ ] **W4. An underground region's edge is drawn.** Its outline as a cavern wall, the ground beyond it rock.
  *Needs artgen.* The sheet's half is W1 (`ground=rock`). On the block map, the nearest pieces the engine has - a
  closed drystone wall, rubble beyond it - read as a walled field, and a rock underlay hatches the cavern floor too.
  Reported as image_tools#66: a cavern wall kind with solid rock beyond it.
- [ ] **W5. What opens from the region is drawn on it.** The outline of each block of a joined region that
  breaks this region's ground - the pyramid's tip on A's map - as a ghosted shape with its code.
  *Built.* Any other region's block whose floor lies below the region's way in, its roof above, inside its outline:
  C.a on A, an open square with its code. The design's streets and fabric keep off it.
- [x] **W6. The Map Judgement Check reviews every block.** Its items read for any rating; a SAFE or WILD block
  adds "the place reads as its seed says" and "what a party walks on between two places is drawn".
  *Done in #121.*

## Asked

1. W2 changes A's and B's places where a solve moves them: are their written bearings and distances fixed, or
   may the design restate them?
   *Answered by the trial:* fixed. A tie holds its place exactly, so `apply` writes the same place as an `xyz`.

## Found

- A.1's Dressing says the statues ring the tip; the tables put them 40 feet square beside it, touching. Step 3d or 4a.
