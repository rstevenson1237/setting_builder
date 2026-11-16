# Intake - content schema: what a place holds, stated once for every rating

## The request, verbatim

> Will need to look at a design for 2 to approve, we tried inserting tags into the setting/ probably and the
> generation struggled.

## How it is read

| Clause | Read as |
|---|---|
| "a design for 2 to approve" | `spec.md` numbers each proposal with its own checkbox. Nothing in `patterns/`, `templates/`, `BRIEF.md` or `tools/` changes until a line is ticked. |
| "we tried inserting tags into the setting/ ... and the generation struggled" | The design may put nothing new into `setting/` for the writer to choose or label, and may not widen what a step is shown. It is tested on one region before anything is migrated. |

The earlier attempt is not in `archive/plans/`: what was tried and where it struggled is asked in `spec.md`.

## What the rating decides today

A region's rating picks its schema file, and the file bundles three things: how the place is laid out (rooms
and doors, or places on ground), which tables a location may hold, and the vocabulary of its types.

| Node | SAFE | WILD | DANGEROUS | Lines that differ |
|---|---|---|---|---|
| NamedCreature, Faction, Procedure | yes | yes | yes | 0 |
| Creature | - | yes | yes | 0 |
| Secret | yes | yes | yes | 1 (`when`) |
| Encounter | - | yes | yes | 1 (`answers`) |
| Hazard | - | yes | yes | 2 (`sign`, or a Secret) |
| Mystery | - | yes | yes | 3 (`act` and `tell`, or a Secret) |
| Person | yes | yes | - | 0 |
| Dressing | yes | yes | yes | 10 (size, place and shape) |
| Purchase, Garrison | yes | - | - | |
| Reward, Lock, Purpose | - | - | yes | |

The same node is written out two or three times. `tools/tables.py` already reads a schema as scopes, a narrower
one shadowing a wider: `Rung` and `Entry` are defined once in `Region_Schema.md` and used by all three ratings.

## What the bundling costs this build

- A key's `Found at` comes from a Reward and WILD holds none, so no key can lie in the surface ruins or the
  lake city, and neither can treasure in a lair (A.7, the scouts' camp).
- DANGEROUS holds no Person. The Royal Guard, the Priesthood and the Scholars are met as "sixes of soldiers",
  "acolytes" and "adepts"; the four Named Creatures are all the demon's.
- Purchase is SAFE's. The lake city's drug market (B.3) is a Local Procedure standing in for one, and the tomb
  robbers, who "trade what they take", sell nothing.
- The lake city is a settlement by its shape and WILD by its danger: the rating had to pick one.

## Out of scope

How a place is laid out and drawn (`Connection` and `Way`, `Block`, `Stop`, `Ground`, the Design nodes), a
rating's Seed and brief, and the location type enums stay each rating's own.
