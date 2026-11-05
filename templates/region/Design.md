# Design

## Purpose
The design of each block of one region, `setting/region/[Region Code]/Design.md`: what its rooms or
buildings are, how they join and where they lie, drawn and approved before any location is written.

## Context
```kdl
template scope="[Region Code]" writes="setting/region/[Region Code]/Design.md" shape="tables"
read "patterns/Layout_Schema.md"
read "layouts"
read "setting/region/[Region Code]/Seed.md"
read "setting/region/Regions.md" part="this region's die"
read "setting/region/[Region Code]/Ground.md"
run "--brief [Region Code]"
```

## Instructions
One `Design` for each block the region holds: its location codes, numbered 1 to N across the
region as `Locations.md` will number them, and an `outline` where the region's brief gives its
block a shape. `BRIEF.md`'s `design` line and the Design line's own settings say how full, how
spaced and how direct.

A DANGEROUS block is built from layouts: a `Use` for each one the seed's shape for the block
calls for (`python3 tools/design.py layouts` lists them by tag), a `Bind` giving each role the
codes and the one type it asks for, a `Join` for each pair of sockets meant to meet, a `Fill` for
each location no layout holds, and a `Void` for ground no room takes. The type mix is `BRIEF.md`'s
for the region. A SAFE or WILD block is fixed geometry: write its `Place` for each location and
its `Link` for each street yourself, from the region's ground and outline, with no layouts.

`solve` and `accept` write each `Place` and `Link` and the seed and score; none of them writes
`approved`, which is the user's word.
