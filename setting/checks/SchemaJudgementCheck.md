# Schema Judgement Check - build 1, Roadsend, 2026-10-15

Evidence: `setting/checks/SettingJudgementCheck.md` of this build (its schema-traced findings: faction marks unplaced, Route position, Alarm, Lethality), and one location of each rating read against its table files: A.2, B.2, C.6.

Confirmed on every item: `patterns/Common_Schema.md`, `patterns/Region_Schema.md`, and every node and enum of `patterns/Setting_Schema.md` not named below.

## Across the schemas
- Gaps: Needs Attention - `patterns/Safe_Schema.md` has only Location and Dressing. A SAFE region's people, services, secrets and the Brief's Secrets and Leads have no entry to be written from, so A's four write-ups carry Features (the Sergeant's Post, the Counter, the Carters' Bench) that no entry holds, which `templates/region/Location.md` forbids ("nothing without one").
- Unhoused content: Needs Attention - a faction's Identity marks (`Setting_Schema.md` Factions, "repeated identically everywhere") fit no field in any location table, so nothing makes a room show them; two of this build's four marks are absent from the rooms where they belong.

## Findings by file
- patterns/Safe_Schema.md Location and Dressing - gap: no node for a person, a service or a secret at a SAFE location. Dangerous and Wild have Encounter and Mystery for the same job.
- patterns/Wild_Schema.md Way and Location - gap: a Route has no place in the order of the landmarks along it; B.2, B.3 and B.4 are in sequence only because the seed says so. Nothing records a distance along the Route.
- patterns/Dangerous_Schema.md Encounter and Location - gap: nothing records how far a noise carries or who comes to it. The Brief's Alarm line has to be built from Referee Notes prose, against `Region_Schema.md`'s "written from the tables alone".
- patterns/Setting_Schema.md Factions Identity - enforceable: a free-text field whose answer is a short list of marks (device, colour, phrase, habit), repeated verbatim; the build can neither place nor count them.
- patterns/Setting_Schema.md Hoards Items and Total - enforceable: Items is free text and Total is its sum, written by hand; a wrong sum passes.
- patterns/Dangerous_Schema.md Reward container - interactive: `container gloss` names what holds a prize but not whether it can be taken whole; C.6's chest and bales are different problems (a locked chest, bales a party must break up) and the field does not ask for the difference.
- patterns/Dangerous_Schema.md Hazard damage - specific: `Damage_Type Nuisance Damaging Lethal` classes a hazard by cost, and Common_Schema's enum carries no Type (Piercing, Crushing, Poison, Fire, Frost, Blast) that the Location template and validator require; the two live in different files.

## Open Items
- Give SAFE locations an entry for a person, a service and a secret - gap, Safe_Schema.
- Place a faction's marks - gap, Setting_Schema Factions Identity.
- Order along a Route - gap, Wild_Schema.
- Record noise and alarm - gap, Dangerous_Schema.
- Check a Hoard's Total against its Items - field, Setting_Schema.
- Name the damage Types where `Damage_Type` is defined - comment, Common_Schema.
