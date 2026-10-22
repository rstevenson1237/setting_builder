# Tables

## Purpose
The table files of one region, `setting/region/[Region Code]/[Table].md`: one file per
table its rating's schema, `patterns/[Rating]_Schema.md`, names, each holding entries.

## Context
```kdl
template scope="[Region Code]" writes="setting/region/[Region Code]/[Table].md" shape="tables"
read "setting/region/[Region Code]/Seed.md"
read "setting/region/Regions.md" part="this region's die"
read "setting/region/[Region Code]/Ground.md"
read "setting/region/[Region Code]/Locations.md"
read "setting/region/[Region Code]/Connections.md"
read "setting/region/[Region Code]/[Table].md"
read "setting/Bestiary.md"
read "setting/Factions.md"
read "setting/History.md"
read "setting/Language.md"
read "setting/Procedures.md" part="Forced Dangers, Conditions, Wounds"
run "--pending [Region Code]"
field "Encounter" reads="Seed.who"
field "Person" reads="Seed.who"
field "Dressing.mark" reads="Seed.who, Factions.Identity"
field "Dressing.left" reads="History.Left"
field "Person.form" reads="Language.Coined here"
field "Person.quest" reads="Quests.Name"
field "Purpose.signs" reads="Location.tags"
field "Hazard.wound" reads="Hazard.damage"
field "Encounter.answers" reads="Connection.to"
field "Lock.key" reads="Keys.Found at"
```

## Instructions
Write each table file its folder names that the region lacks, and add to each Connections
entry what stands in its way. Purpose first, where the folder has one;
then each table in one pass.

Each room gets the entries its type's `rate` line in `BRIEF.md` gives, choosing within a range
for a reason its tags give, and toward `BRIEF.md`'s targets. The occupants the seed's `who`
names are placed as Encounters - in a SAFE region as People, Named Creatures and Faction members, and a
Garrison at an Authority - and a `procedure` line in the region's node of `BRIEF.md` as a
Procedure entry at the location it fits, any type and at most one a location. A room a
Purpose's `signs` names carries a sign of it. An entry that will not fit its room is a finding
for 5c, never moved or dropped here.

A Person's name is written with its `form` per `patterns/Common_Schema.md`; a tongue or family
name is recorded in `setting/Language.md` first. A Dressing's `mark` is the Identity of a
faction that holds, passes through or contests the room; every faction a region's seed names in
`who` is marked somewhere in it. A Dressing's `left` is each History event whose Left mark the
room shows. A Hazard's `test` is Constitution with a `wound`, Fate with a `condition`, or Sanity
from a Chaos source only. A DANGEROUS Encounter's `answers` is set where an alarm raised
elsewhere in the region brings it out.

A `Lock` goes where the design wants a gate, on whatever node the schema lets hold one, naming
its key; the key's `Keys.md` entry is written with it. Once the pass is written, the validator
owes each key it has no place for: a stub Reward pulling `Keys: [name]`, in a location the lock
does not bar, in this region or another. A key whose region is not yet written stays a warning
until its pass. Likewise a setting entry whose Found at or Appears at names a location no table
holds it is placed there as a stub, holding only what placement fixes; the next pass fills the
rest.
