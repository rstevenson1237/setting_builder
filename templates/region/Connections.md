# Connections.md

## Purpose
The ways between a region's locations, `setting/region/[Region Code]/Connections.md`, and its
`Blocks.md` where its rating's schema holds one.

## Context
```kdl
template scope="[Region Code]" writes="setting/region/[Region Code]/Connections.md setting/region/[Region Code]/Blocks.md" shape="tables"
read "setting/region/[Region Code]/Seed.md"
read "setting/region/Regions.md" part="the regions this one joins"
read "setting/region/[Region Code]/Locations.md"
field "Way.to" from="Entry.from, Location.type"
field "Connection.to" from="Entry.from, Location.type"
field "Connection.width" from="Conditions.width"
field "Block.locations" from="Location.type"
```

## Instructions
One entry per side of every way between two locations, with `to`, `type`, `bearing` and
`distance` set from this end (and `climb` where the way changes level); the far side's entry reverses the
bearing. What stands in a way - an Encounter, Hazard, Mystery, Secret or Lock - is added with the tables.

Every location is reachable from an entrance the seed's Entries name, and a way into a gated
location carries the gate its folder's `join` line names. A way to another region joins only a
region this one joins in `setting/region/Regions.md`.

Where the schema holds Blocks, every location is in exactly one block, and a way that climbs
joins two blocks. A Block or Connection states its passages' `width` and `height` only where
they differ from the seed's Conditions, a Connection's within both rooms' footprints.
