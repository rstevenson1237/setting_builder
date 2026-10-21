# Tables

## Purpose
The table files of one region, `setting/region/[Region Code]/[Table].md`: one file per
table its rating's schema, `patterns/[Rating]_Schema.md`, names, each holding entries.

## Context
```kdl
template scope="[Region Code]" writes="setting/region/[Region Code]/[Table].md" shape="tables"
read "setting/region/[Region Code]/Seed.md"
read "setting/region/Regions.md" part="this region's die, and the regions it joins"
read "setting/region/[Region Code]/Ground.md"
read "setting/Language.md"
step 4a writes="Locations" {
  field "Location.name" reads="Language.Coined here"
  field "Location.bearing" reads="Feature.bearing, Feature.distance, At.ground"
}
step 4b writes="Connections Blocks" {
  read "setting/region/[Region Code]/Locations.md"
  field "Way.to" reads="Entry.from, Location.type"
  field "Connection.to" reads="Entry.from, Location.type"
  field "Connection.width" reads="Conditions.width"
  field "Block.locations" reads="Location.type"
}
step 4c writes="Purpose Dressing Purchases People Garrison Challenges Rewards Procedures Stops" {
  read "setting/region/[Region Code]/Locations.md"
  read "setting/region/[Region Code]/Connections.md"
  field "Encounter" reads="Seed.who"
  field "Person" reads="Seed.who"
}
step 5a writes="Purpose Dressing Purchases People Garrison Challenges Rewards Procedures Stops Connections" {
  read "setting/region/[Region Code]/[Table].md"
  read "setting/Bestiary.md"
  read "setting/Factions.md"
  read "setting/History.md"
  read "setting/Procedures.md" part="Forced Dangers, Conditions, Wounds"
  run "--pending [Region Code]"
  field "Dressing.mark" reads="Seed.who, Factions.Identity"
  field "Dressing.left" reads="History.Left"
  field "Person.form" reads="Language.Coined here"
  field "Person.quest" reads="Quests.Name"
  field "Purpose.signs" reads="Location.tags"
  field "Hazard.wound" reads="Hazard.damage"
  field "Encounter.answers" reads="Connection.to"
  field "Lock.key" reads="Keys.Found at"
}
```

## Instructions
- **4a, Locations** - the count `BRIEF.md` sets for the region, in its targets' type mix,
  each placed from the region's way in by bearing and distance, or north and east, so the region reads as one plan, distances in the region's units, on ground `Ground.md` shows can hold it.
  A location's name carries no form: it is common, or points at a coinage
  `setting/Language.md` already records, and never coins one. A Person's name, at 5a, is
  written with its `form` per `patterns/Common_Schema.md`; a tongue or family name is
  recorded in `setting/Language.md` first.
- **4b, Connections and Blocks** - one entry per side of every way between two locations, with
  `to`, `bearing` and `distance` set from this end (and `climb` where the way changes level), and
  the rest a stub; the far side's entry reverses the bearing. Every location is reachable from
  an entrance the seed's Entries name, and a way into a gated location carries the gate its
  folder's `join` line names. A way to another region joins only a region this one joins in
  `setting/region/Regions.md`. Where the schema holds Blocks, every location is in exactly one
  block, and a way that climbs joins two blocks. A Block or Connection states its passages' `width` and `height` only where they
  differ from the seed's Conditions, a Connection's within both rooms' footprints.
- **4c, the stubs** - every other table, its entries bare: `[Node] [Location Code]`.
  Each room gets the entries its type's `rate` line in `BRIEF.md` gives, choosing within a range for a
  reason its tags give, and toward `BRIEF.md`'s targets. The occupants the seed's `who`
  names are placed as Encounters - in a SAFE region as People, Named Creatures and Faction
  members, and a Garrison at an Authority - and a `procedure` line in the region's node of `BRIEF.md`
  as a Procedure entry at the location it fits, any type and at most one a location. A member or child is written now only where the
  design already fixes it.
- **5a, filling** - Purpose first, where the folder has one; then each table in one pass, every stub in view. Write
  every member a stub lacks, toward its room's Purpose and `BRIEF.md`'s targets; a room a
  Purpose's `signs` names carries a sign of it. A stub that will not fit its room is a finding for 6c, never moved
  or dropped here. A Dressing's `mark` is the Identity of a faction that holds, passes
  through or contests the room; every faction a region's seed names in `who` is marked somewhere
  in it. A Dressing's `left` is each History event whose Left mark the room shows.
  A Hazard's `test` is Constitution with a `wound`, Fate with a `condition`, or Sanity from a Chaos source only. A
  DANGEROUS Encounter's `answers` is set where an alarm raised elsewhere in the region brings it out.
- **5a, locks and keys** - a `Lock` goes where the design wants a gate, on whatever node the
  schema lets hold one, naming its key; the key's `Keys.md` entry is written with it. Once
  the pass is filled, the validator owes 5a each key it has no place for: a stub Reward
  pulling `Keys: [name]`, in a location the lock does not bar, in this region or another.
  A key whose region is not yet laid out stays a warning until its 4c. Likewise a setting
  entry whose Found at or Appears at names a location no table holds it is placed there as
  a stub. A stub holds only what placement fixes; the next 5a fills the rest.
