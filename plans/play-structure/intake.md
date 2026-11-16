# Intake - play structure: what moves, and how many ways through

## The request, verbatim

> We can design 7.

## How it is read

Review item 7. `spec.md` numbers each proposal for approval; none is built. The first draft of this plan was
written from the Buried City alone; the history below changes most of it.

## What the history holds

| Commit | What it decided or found | Here |
|---|---|---|
| 666c137 | The region die and the location count are one mechanism. WILD at N locations: "expected encounters per full traverse is exactly 1 at every die". DANGEROUS at 3N: "expected countdown steps per full clear is exactly 3 - half the track ... the get-in-and-get-out pressure, built into the sizing". | The Danger track is this framework's wandering monster. The review called it missing. |
| bdc375e | "An occupant is not always home, which is what makes a wandering monster result mean something": `presence`. | It survives on a Named Creature only. |
| 346b373 (D16) | "DANGEROUS a dense graph with few entrances". | One way into the pyramid is the design. |
| fd7b4d5 (F9, F10) | "Connective space carries the dungeon's decisions rather than its filler": node roles (dead end, branch, loop leg, divide), set when the connections are written. It "proposes graph-shape reporting as a validator diagnostic rather than a rule". | `TOPOLOGY` is that diagnostic. |
| 42ebf21 (#22) | A built region came out with 5 of 9 LOW rooms "empty", so a rule was added: 60% of LOW rooms carry a role, none over a third. | Graph shape was once held to numbers; the rule went with the patterns at #68. |
| 2702dbb (#69), `archive/plans/content-loop/` | "Rates stop being rolled per room. They become region-level targets ... checked by the tools." | How a number is held today: a `target` in `BRIEF.md`. |
| `archive/plans/location-schema/spec.md` D9, built in `tools/tables.py` `_behind` | A key cannot lie behind the lock it opens: walked from the region's entrances. | The review said nothing walks the graph. It does, within one region and one lock at a time. |
| `archive/plans/table-pipeline/spec.md` E9, 9.5 | "No multi-room puzzle anywhere"; Compositions answered it, each with a chain, a "way round ... and its price", and an eight-item proof. | Lost at #68. Locks, keys and `Purpose.signs` are what remains. |
| `archive/plans/b2-friction/intake.md` items 1 and 3, closed in 778ff41 | "Faction Turn is cited and never defined" and "an alarm stops at its region's edge" were raised and declined. | A faction procedure is not proposed here. |

## What the build holds today

- Every Encounter stands in one room. The Danger table's six rows are prose written at step 4e, so when the track
  reaches 2 or 1, who comes is whatever that row happens to say, and no room is emptied by it.
- The validator prints each region's loops and dead ends and holds nothing to them. Level 3 has one loop and nine
  dead ends among fifteen rooms; the Map Judgement Check records "It plays: Confirmed".
- Level 1 to 2 has three ways; every other pair of levels has one. The lake city is the one other route.
- A key in one region for a lock in another is not walked, and neither is a chain of two locks.

## Out of scope

Timelines and countdowns aimed at a party, which `patterns/Setting_Schema.md` rules out; a faction turn and
alarms across regions, both declined; named leaders, which follow from the content-schema plan (C2).
