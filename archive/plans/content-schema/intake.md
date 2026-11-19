# Intake - content schema: what a place holds, stated once for every rating

## The request, verbatim

> Will need to look at a design for 2 to approve, we tried inserting tags into the setting/ probably and the
> generation struggled.

## How it is read

| Clause | Read as |
|---|---|
| "a design for 2 to approve" | `spec.md` numbers each proposal with its own checkbox. Nothing in `patterns/`, `templates/`, `BRIEF.md` or `tools/` changes until a line is ticked. |
| "we tried inserting tags into the setting/ ... and the generation struggled" | The design may put nothing new into `setting/` for the writer to choose or label, and may not widen what a step is shown. It is tested on one region before anything is migrated. |

## What the history holds

Read after the first draft of this plan, which it changes.

| Commit | What it decided or found | Here |
|---|---|---|
| 9467adb (F12) | "A class describes what is obvious and mandatory, never a ceiling on what may appear." | The principle this plan rests on: a rating should not forbid a table. |
| bdc375e | The hook layer: "Quest, Key and Lore belong in all three folders ... SAFE gives, WILD carries, DANGEROUS holds." `wild/Treasure.md`, `wild/Key.md` and `wild/Lore.md` stood from then until the patterns were archived. | Treasure, keys and lore in WILD are a capability the framework had and lost, not a new one. |
| f1a1934 (#68) | The KDL schema was built clean-room for DANGEROUS; SAFE and WILD became "stub folders holding Locations only". | Where it was lost. |
| `archive/plans/location-schema/spec.md` | Proposed `Rewards` in the WILD folder (W4), with "nothing is pristine outdoors" (W7); `Rewards` in SAFE as "the vault or the treasury" (S6); and `Person` as an Encounter child that "Dangerous gets for free" (S2). | C3, C4 and part of C6 were proposed before. Nothing records them being declined. |
| 0df4b9f (#71) | SAFE and WILD got "their tables: Dressing for both, Ways and join rules for WILD", built "minimal". The nodes every rating shared sat in `Region_Schema.md`. | The shared nodes this plan first proposed are the state of that commit. |
| 3c24a31 (#72), the next day | "Each rating schema defines every node its tables hold, so Location, Dressing and Encounter can drift per rating." | Sharing was tried and deliberately undone. C1 is rewritten below. |
| 42ebf21, b6e0bf7, 48afaff | Genre-derived tag pools: in `GENRE.md`, then `setting/Tags.md` and a pool per region. | The tags tried in `setting/`. |
| 6924638 (#64) | "The setting and region tag pools are retired": three tags a location, written for it alone. | |
| 84795e4, b9fed83, then b288649 | Genre lists moved out of the patterns into `genre/bx-1981/`, with a draw; the tree was then reverted to `framework-v0`. | A build-held genre vocabulary was built and taken back out. C9 is withdrawn below. |
| cfb6e42 | "A compiled option menu can return a member of a category but never a consequence." | Why a wider vocabulary did not make content denser. |
| 4eb9250 (#95) | Drakenhold needed `Lift` and `Chute`: they were added to the schema's enum. | How a build gets vocabulary today, and it works. |

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

The same node is written out two or three times, by design since #72: each rating may change its own.

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
