# Intake - placement: every block and location at a point in one space

## The request, verbatim

> I'd like to continue building out our block placement model, my thoughts below. First start
> by restating the goal back to me to make sure we are on the same page: assign blocks a space
> within the region in 3d space (x,y,z) - every block can be expressed with a firm relation to
> 0,0,0 (and be calculated against each other) - we should be able to closely map against an
> adjacent block for tight mapping - blocks can also have a bounding shape, rectangular ( length
> and width) circular (radius) or an arbitrary list of bounding points for irregular shapes - we
> should be able to dry fire a setting and pin point every single location in this 3d space to
> prove that the design works

## Follow-up, verbatim

The goal was restated and four questions put: where (0,0,0) is (one origin for the setting, at
the foot of the pyramid's tip in region A, since each pyramid level is its own region); which
blocks (every rating's, and the sheet regions); whether locations are placed the same way
inside their blocks; and whether the numbers are authored, written by the tools, or both.

> agreed on all four, both for 4 — write the plan

## How it is read

| Asked | Read as |
|---|---|
| A space in x, y, z | One frame for the whole setting: x east, y north, z up, in whole feet. |
| A firm relation to 0,0,0 | (0,0,0) is region A's way in at its ground. Every region, block and location has an origin in its parent's frame - setting, region, block, location - so each resolves to an absolute point by adding its ancestors'. |
| Calculated against each other | Any two absolute points give a distance, a bearing and a climb. |
| Mapped against an adjacent block | An anchor: a thing placed touching a sibling on a side, with an optional slide along it and gap from it. |
| A bounding shape | An outline - a rectangle, a circle or a polygon - round the thing's origin, standing from its floor to its height. |
| Dry fire | One command resolves every region, block and location to an absolute point and lists what does not fit. The validator runs it. |
| Which blocks | Every rating's blocks and locations, and the regions themselves. |
| Who writes the numbers | Both: any place may be authored; `place` and `pack` write the ones they solve; the dry fire checks whatever is stored. |

## What today's model leaves unsaid

- No height. Levels relate only through the rule that blocks a climbing way joins share their
  centre, and through each way's `climb`.
- Places are stated four ways, each from a different origin in a different unit: a DANGEROUS
  room's `east` and `north` (feet, from its block's centre); a SAFE or WILD location's
  `bearing` and `distance` or `north` and `east` (any unit, from its region's way in); a region's
  square on a sheet; and a block's square `footprint`.
- Nothing checks across regions. Worked by hand from today's tables, two contradictions no
  check sees:
  - B's two ways in disagree in height by 30 feet. G.14 to B.1 climbs -30, putting B.1 30 feet
    below G; H lies 20 feet below G and H.1 to B.10 climbs +20, putting B.10 level with G. Both
    stand at height 550 on B's ground.
  - They disagree in plan by about 300 feet. B.10 lies 180 yards west-south-west of B.1, so H.1,
    30 feet east of B.10, would lie about 300 feet west of H's centre, outside H's 200-foot
    footprint, which shares its centre with G's.
- More will show once the levels are packed: G's 24-foot rooms reach 4 feet into F's floor, 20
  feet up, wherever one lies under an F room; L's 30-foot rooms reach 10 feet into K's.

## Out of scope

- Rotation. Everything lies square to the compass, as rooms do now; a polygon outline draws
  anything else.
- Terrain. `Ground.md`'s Features and a sheet's relief stay the sheet's; only `At` heights feed z.
- Drawing from the space. The site, the PDF and the cuts draw as they do now, reading places
  through the new module.
