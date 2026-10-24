# Brief.md

## Purpose
A region's brief, `setting/region/[Region Code].md`: its run sheet, written once its
locations exist and rewritten when its seed or tables change. A referee holding it, with
what the site draws beside it, can run an excursion into the region without opening a
location.

## Context
```kdl
template scope="[Region Code]" writes="setting/region/[Region Code].md" shape="brief"
read "setting/region/[Region Code]/Seed.md"
read "setting/region/[Region Code]/[Table].md"
read "setting/region/[Region Code]/Ground.md"
field "Overview" from="Seed.comes, Seed.who, Seed.changing, Rung"
field "View" from="View"
field "Approach" from="Entry, Seed.crossing, Seed.off"
field "Law" from="Law"
field "Terrain" from="Seed.terrain, Ruling"
field "Conditions" from="Conditions"
field "Arrival" from="Dressing.obvious, Dressing.layout"
field "Plan" from="Block, Way, Location.type"
field "Ways" from="Stop.feature, Stop.distance, Stop.to, Dressing.obvious"
field "Landmarks" from="Dressing.obvious, Dressing.ambiance, Stop.sight"
field "Entrances" from="Dressing.obvious, Dressing.layout, Connection.to"
field "Prizes" from="Dressing.obvious, Dressing.layout, Connection.type"
field "Places" from="Dressing.obvious, Dressing.ambiance, Dressing.condition, Secret.tell"
field "Tables" from="Encounter.doing, Encounter.reaction, Hazard, Rung"
```

## Instructions
Write every field of the rating's `brief`, in its order, from the seed and the tables
alone. The seed's fields are its nodes as prose, each member once. A list field opens one
`- ` item for each location its `holds=` gives it, in code order, with that code, as
`--skeleton 4e [Region Code]` lists them. What `drawn` names is never written here.

Every fact about a location names it by code. A fact no entry holds is an entry to add to
the tables, not a line here. A setting entry is cited as `(Named Creature: Name)`,
`(Faction: Name)` or `(Local Procedure: Name)`.
