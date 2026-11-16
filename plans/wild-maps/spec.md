# Spec - wild maps

Tick a line to approve it. W1 and W2 use what exists; W3 and W4 need a spike on artgen first.

- [ ] **W1. A sheet states its ground.** `sheet Sands ... ground=sand`: the terrain artgen fills with wherever
  no region's `ground` reaches, in place of its own choice. A region's `ground` line still wins inside its area.
- [ ] **W2. Regions A and B are designed (step 3d).** A `design` line for each in `BRIEF.md`; a `Street` for each
  street the seed names (A's grid past the ruins, B's quay round the lake), a `Tie` for each place the seed
  fixes. Solved, shown and approved as any design.
- [ ] **W3. Fabric: what stands between the keyed places.** One line in a SAFE or WILD design,
  `Fabric [Block] kind=ruins share="40%"`, drawn as unkeyed buildings of that kind along the streets, from the
  design's seed. **Spike first**: whether `artgen settlement` fills round buildings already placed
  (`gen.density` exists; its behaviour with fixed buildings is untested). If not, it is a report to artgen.
- [ ] **W4. An underground region's edge is drawn.** Its outline as a cavern wall, the ground beyond it rock.
  **Spike first**, as W3.
- [ ] **W5. What opens from the region is drawn on it.** The outline of each block of a joined region that
  breaks this region's ground - the pyramid's tip on A's map - as a ghosted shape with its code.
- [ ] **W6. The Map Judgement Check reviews every block.** Its items read for any rating; a SAFE or WILD block
  adds "the place reads as its seed says" and "what a party walks on between two places is drawn".

## Asked

1. W2 changes A's and B's places where a solve moves them: are their written bearings and distances fixed, or
   may the design restate them?
