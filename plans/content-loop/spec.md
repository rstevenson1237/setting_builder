# Spec - the content loop

The request and its decisions are in `intake.md`.

## 1. What the evidence says

Every judgement check run so far has found the same failures. Each comes from content
decided **before** what it depends on exists, or **rolled** where it should be placed.

| Finding (source) | What produced it |
|---|---|
| Rates never realized at region scale: no second name in 30 rooms against 20%; 94% open edges against 60%; treasure 29 of 34 a table roll against 55% (Greywatch 5c, both addenda) | A percentage rolled per room, or not rolled at all. Nothing reads the region total |
| A household of "about ten" appears as one Khughik; encounters copied from the Overview's Alarm and Loot lines (addendum 2) | The Overview stated per-room occupants before any room existed |
| Keys drawn and never written; keys named for locks with no key drawn; one block's key leaking into the next (addendum 2) | Keys and locks discovered while writing, not placed |
| Rumour 3 contradicts B.md and History; every Settled-at pending until 5c (Greywatch 5c) | Rumours written at 2d, before any location existed |
| C.17, C.11, C.12 and C.18 transcribe C.md's Loot, Alarm and d6 table (addendum 2); `A.md` today names the prize's room, the key's room and the alarm timing, and two of its Secrets are also held in `Rewards.md` and `Connections.md` | The Overview holds room facts, so they are written once above and again below |
| `metrics.py` MIX counts 3 treasures from region A's write-ups where `Rewards.md` holds 5; READ SET names a step that no longer reads patterns | metrics reads write-ups, not tables |
| An entry with no members is an error, so the only to-do list is missing files; nothing says whether a write-up's entries have moved since it was written | No stub, and no staleness check |

## 2. The pipeline

```
1. Establish framework       1a Procedures seed, 1b Language seed
2. Build the setting         2a Setting ... 2g tailoring and empty registries
                             (Rumours leave phase 2 for 5d)
3. Build the region          3a gazetteer, 3b region graph, 3c region seed
4. Lay out locations         4a Locations.md, 4b Connections.mmd, 4c stub tables
5. Content loop              5a seed, 5b write, 5c review, 5d place - repeated;
                             then 5e region brief
6. Judgement checks          6a template, 6b pattern, 6c setting
```

A pass of the loop is 5a → 5b → 5c → 5d. The loop exits when a pass leaves no stub, no
stale write-up and no open review finding, and placement added nothing.

- **3c Region seed** - the Overview's fields a table is written from: Kind, Settlement or
  Terrain, Overview, Approach, Conditions, Inhabitants or People as a roster, Services,
  Law, and the Situation with its rungs.
- **4c Stub tables** - every entry each location will hold, as a bare stub
  (`Encounter A.3`). They are placed within the schema's counts and ranges, and toward
  `BRIEF.md`'s targets.
- **5a Seed** - fill every stub, Purpose first, one fresh context per table file with the
  whole file in view; write every setting entry a table names.
- **5b Write** - write every location whose write-up is missing or stale, and record
  coinages.
- **5c Review** - run the validator and metrics; then a fresh context judges this pass's
  write-ups against `templates/checks/Location_Review.md`. Each finding names where it
  goes: an entry (5a), a write-up (5b), a placement (5d), or the framework (`plans/`).
- **5d Place** - write the setting's threads against what exists: the Rumours table, each
  rumour from a location holding its answer; Quests, giver and target; locks where the
  design wants them, then keys for existing locks on the next placement; Lore, Truths'
  Handles and History's Left lines. A new region entry it needs is written with the
  placed member set, and the locations it touches go stale.
- **5e Region brief** - the Overview's remaining fields, from the finished region: Places,
  Inhabitants with counts summed from Encounters, Alarm, Loot, Secrets, the rumours and
  quests pointing here, and the d6 tables. It indexes and never restates.
- **6c** keeps the cross-level items. The per-room items move to the Location review, and
  the bookkeeping moves to 5d.

## 3. Percentages

**The schema holds what a type is; `BRIEF.md` holds how much of it a build wants.**
The schema's `rate` lines become counts and ranges only: High holds 1-2 challenges, Medium
holds one, Low holds none, and a Medium or Low room holds 0-1 rewards. A one-of says which
kinds may fill a slot. Neither says how often.

Is any percentage true at the framework level? A percentage belongs in the framework only
if every setting built with it needs that share to work, so that a build moving it would
break something mechanical rather than just change in taste. I checked each one the
framework holds today against that test:

| Percentage | Where it is now | Framework-level? |
|---|---|---|
| Medium Rewards 50%, Low Rewards 25% | `patterns/Schema.md` | No. It is taste. The type is defined by its challenge slot, and the reward is a range of 0-1. |
| High 20% / Medium 50% / Low the rest | `templates/dangerous/Tables.md` | No. A region of all-Medium rooms runs fine; it only reads flat. |
| T 35% / P 35% / F 20% / U 10% rumours | `templates/setting/Rumours.md` | No. The structural minima that matter ("two true that sound false") are counts, and stay in the template. |
| Location count 3x the die | `templates/dangerous/Tables.md` | **Yes, but it is a multiplier, not a share.** A full clear of a collection burns about half the d6 Danger track at every die size, so the count is tied to a mechanic in `setting/Procedures.md`. It stays as a framework default, which `BRIEF.md` can override. |

So no percentage stays in the framework. A build with no targets in `BRIEF.md` gets only
the schema's ranges, and 5c reports the shares it realized without judging them.

### `BRIEF.md`'s targets

The prose requests stay prose. Targets are fenced KDL blocks under any heading, read by
the tools, as granular as wanted. One node per target:

```kdl
// share of a member's values, among entries in scope
target Location.type High="20%" Medium="50%"
target Reward.contents "Treasure I"="40%" Keys="20%" Lore="20%"
target Hazard.damage Lethal="20%" Damaging="40%" rating=Dangerous
// share of locations of a type that hold a node
target Reward of=Medium "50%"
// share of a node's entries holding a one-of child
target Connection.Lock "10%" region=C
// a count
target Location count=12 region=A
```

- **Scope** is `rating=` and `region=`, and the narrowest target wins.
- **The validator** errors on a path the schema doesn't hold, and on shares in one target
  totalling over 100%.
- **Metrics** prints realized against target. A miss of more than one entry is a review
  finding at 5c, not a validator warning, because a target is the build's own taste.
- **Layering:** 4c places stubs toward targets, 5a fills them, and 5d adds where a target
  is under-met. The underspecified area is always visible as a line of metrics output.

## 4. Change tracking

### Your suggestion against the digest

| | Commit history (yours) | Digest in the write-up (mine) |
|---|---|---|
| Bookkeeping | None. Git already records it | A marker line in every write-up, and a `--stamp` step after each write |
| Content | Untouched | A comment the site and PDF must strip |
| Granularity | Per file. Region tables are one file per kind, so any change to `Challenges.md` stales every room in the region | Per entry, exact |
| A change reverted to the same text | Reads stale | Reads fresh |
| Uncommitted edits | Need handling (see below) | Seen directly |
| Squash merges | `main` is squash-merged, so every file in a PR shares one commit time. An entry changed in a PR with its write-up never rewritten reads fresh after merge | Unaffected |

Both answer "has anything this write-up was written from changed since?". The
difference is where the answer is stored.

**Adopted: yours, at entry grain.** Instead of a file's last commit, the tool takes
`git blame` of the lines holding the location's entries, plus the entries naming it and
the setting entries they name. A write-up is stale when the newest of those lines is
newer than the write-up's last commit. This keeps zero bookkeeping and no marker, and it
fixes the file-grain problem. Lines not yet committed count as now, so they are stale
until committed with their rewrite. The squash caveat is bounded: the loop runs within one
branch and exits before merge, so history is intact for as long as staleness matters.

**On determinism.** Neither scheme needs it, but it is what makes the loop cheap. If an
unchanged location rewrites almost identically, a false stale costs nothing but a no-op
diff. 5c can test it: on the pilot, rewrite one location that is not stale and read the
diff. A rewrite that moves more than wording is a finding against `templates/region/Location.md`.

## 5. Pulled in from `archive/plans/location-schema`

Only what the loop needs:

- **Quest pathway.** `table Quests entry file="setting/Quests.md"`; `Quests` joins
  `Contents_Type`; `Encounter` gains `asks entry Quests opt`.
- **Keys pair.** Each `Lock` names a key that some `Reward` pulls as `Keys:`, and each
  such pull names a key some `Lock` holds. While one end is missing this is a warning;
  once the loop exits it is an error.
- **A key is never behind its own lock.** The key's location is reachable from the
  region's entrance without passing the Connection that key unlocks. This is an error.

SAFE and WILD are written piece by piece as the pilot reaches them.

## 6. Order of work

The framework comes first, then the pilot on region A, then SAFE and WILD. See
`implementation.md`.
