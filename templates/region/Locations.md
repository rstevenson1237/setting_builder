# Locations.md

## Purpose
A region's locations, `setting/region/[Region Code]/Locations.md`: what stands where, before any
of it is written.

## Context
```kdl
template scope="[Region Code]" writes="setting/region/[Region Code]/Locations.md" shape="tables"
read "setting/region/[Region Code]/Seed.md"
read "setting/region/Regions.md" part="this region's die"
read "setting/region/[Region Code]/Ground.md"
read "setting/Language.md"
field "Location.name" reads="Language.Coined here"
field "Location.bearing" reads="Feature.bearing, Feature.distance, At.ground"
```

## Instructions
Write the count `BRIEF.md` sets for the region, in its targets' type mix, each placed from the
region's way in by bearing and distance, or north and east, so the region reads as one plan,
distances in the region's units, on ground `Ground.md` shows can hold it.

A location's name carries no form: it is common, or points at a coinage `setting/Language.md`
already records, and never coins one.
