# Design

## Purpose
The design of each block of one region, `setting/region/[Region Code]/Design.md`: what its rooms or
buildings are, how they join and where they lie, drawn and approved before any table but `Locations.md` is written.

## Context
```kdl
template scope="[Region Code]" writes="setting/region/[Region Code]/Design.md" shape="tables"
read "setting/region/[Region Code]/Seed.md"
read "setting/region/Regions.md" part="this region's die"
read "setting/region/[Region Code]/Ground.md"
read "setting/region/[Region Code]/Locations.md"
run "--brief [Region Code]"
```

## Instructions
One `Design` for each block the region holds: the codes of its locations, as `Locations.md` numbers them, and an
`outline` near the brief's `footprint`, the level's target size. `BRIEF.md`'s `design` line says how full and how
padded; a Design line states a setting only where its block differs from the region's. Each room or building is
sized for what its location's name, tags and type say it is, and one the seed places (a hall at the centre, a tomb
at the far end) is given that place, as its `xyz`.

A DANGEROUS block is a plan, following the `block-plan` skill: a `Layout` for each group of rooms set against one
another, a `Room` for each location, a `Route` for each way with the walls it leaves by and how long it runs, and
a `Void` for ground no room takes. A SAFE or WILD block is a settlement: a `Fill` for each location's footprint; a
`Tie` for each place set a bearing and distance from another, from the region's ground and outline; a `Street`
for each street, the buildings it runs past in order. Its first location stands at the block's centre.

`solve` and `accept` write each `Place`, `Link` and `Part` and the seed and score; none of them writes
`approved`, which is the user's word.
