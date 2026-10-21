# Tables

## Purpose
The table files of one region, `setting/region/[Region Code]/[Table].md`: one file per
table its rating's schema, `patterns/[Rating]_Schema.md`, names, each holding entries.

## Context
Read first:
- `GENRE.md`, `STYLE.md` and `BRIEF.md`, as `python3 tools/validate_setting.py --brief [Region Code]` prints it
- `patterns/Common_Schema.md`, `patterns/Setting_Schema.md` and this region's rating schema
- this region's seed, `setting/region/[Region Code].md`
- this region's die in `setting/region/Regions.md`, and `setting/Language.md`
- this region's table files, as far as they exist, and its `Ground.md`: the terrain, rivers, roads and hills of its area
- `setting/region/Regions.md` - the regions this one joins
- the setting files `patterns/Setting_Schema.md` names for the values being written, and the
  setting entries `python3 tools/validate_setting.py --pending` owes

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
  an entrance the seed's Approach names, and a way into a gated location carries the gate its
  folder's `join` line names. A way to another region joins only a region this one joins in
  `setting/region/Regions.md`. Where the schema holds Blocks, every location is in exactly one
  block, and a way that climbs joins two blocks.
- **4c, the stubs** - every other table, its entries bare: `[Node] [Location Code]`.
  Each room gets the entries its type's `rate` line in `BRIEF.md` gives, choosing within a range for a
  reason its tags give, and toward `BRIEF.md`'s targets. The occupants the seed's Overview
  names are placed as Encounters - in a SAFE region as People, Named Creatures and Faction
  members, and a Garrison at an Authority - and a `procedure` line in the region's node of `BRIEF.md`
  as a Procedure entry at the location it fits, any type and at most one a location. A member or child is written now only where the
  design already fixes it.
- **5a, filling** - Purpose first, where the folder has one; then each table in one pass, every stub in view. Write
  every member a stub lacks, toward its room's Purpose and `BRIEF.md`'s targets; a room a
  Purpose's `signs` names carries a sign of it. A stub that will not fit its room is a finding for 6c, never moved
  or dropped here. A Dressing's `mark` is the Identity of a faction that holds, passes
  through or contests the room; every faction a region's Overview names is marked somewhere
  in it. A Dressing's `left` is each History event whose Left mark the room shows.
  A Hazard's `test` names the die its trigger rolls: Constitution with the `wound`, Fate with the `condition`, Sanity
  only from a Chaos source.
  A Garrison's `call` and `within` state what brings it out and how soon; a DANGEROUS Encounter's `answers` is set where the region's Alarm brings it out. An Encounter's `reaction` opens with one `Reaction` item, then ` - ` and what it does.
- **5a, locks and keys** - a `Lock` goes where the design wants a gate, on whatever node the
  schema lets hold one, naming its key; the key's `Keys.md` entry is written with it. Once
  the pass is filled, the validator owes 5a each key it has no place for: a stub Reward
  pulling `Keys: [name]`, in a location the lock does not bar, in this region or another.
  A key whose region is not yet laid out stays a warning until its 4c. Likewise a setting
  entry whose Found at or Appears at names a location no table holds it is placed there as
  a stub. A stub holds only what placement fixes; the next 5a fills the rest.

## Template
````
# [Table] of [Region Code] [Region Name]

```kdl
[Node] [Location Code] [member]=[value] { [Child] [member]=[value] }
```
````
