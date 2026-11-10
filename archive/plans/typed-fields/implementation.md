# Implementation - typed fields wherever prose holds a value

Task plan for `spec.md`, every proposal approved. Commit messages cite tasks as
`typed-fields T1.1`, so they can't be mistaken for sheet-maps' ids. Every task ends with
`python3 tools/validate_setting.py` clean and commits on its own.

Order: make the checker and the staleness model ready, add the two values, then one task
per proposal. Each proposal lands with its schema line, its check, the template that writes
it, and Thornmarch migrated, so the validator passes after each one. The plan starts after
sheet-maps' T3.2 (`spec.md` 6).

---

## Phase 0 - Ready the tools

| Task | What | Files |
|---|---|---|
| T0.1 | One value checker for both paths. `check_field` (setting entries) and `_check_value` (region tables) each test the same value types, with their own copies. Merge them into one function per value, called from both, so each new value is added once | `tools/tables.py` |
| T0.2 | The region path honours `Common_Schema.md`'s rule that an enum field opens with an item and may go on after ` - `. Today the region path wants the item alone, which R2 needs changed | `tools/tables.py` |
| T0.3 | A retyping is not a rewrite. Staleness reads `git blame`, so a migration commit would mark every write-up it touches stale with nothing to fix. `History` passes `--ignore-revs-file .git-blame-ignore-revs` where that file exists. Each migration commit that changes form but not meaning is listed there by the next commit | `tools/tables.py`, `.git-blame-ignore-revs` |
| T0.4 | `metrics.py` read-set report saved as the baseline for T4.2 | `plans/typed-fields/metrics-before.txt` |

---

## Phase 1 - Values

| Task | Spec | What | Files |
|---|---|---|---|
| T1.1 | C1 | `value coin`, with its check: `N cn`, `N-M cn` low to high, or `pennies` | `patterns/Common_Schema.md`, `tools/tables.py` |
| T1.2 | C2 | `enum Time_Unit` and `value time`, with its check, and a warning for a unit the region's rating doesn't keep time in, per `Procedures.md`'s Time and Distance | `patterns/Common_Schema.md`, `tools/tables.py` |

No field uses either value yet, so nothing in `setting/` changes.

---

## Phase 2 - Region tables

Each task migrates every Thornmarch line it covers in the same commit.

| Task | Spec | What | Files |
|---|---|---|---|
| T2.1 | R1 | `enum Test`; `test`, `wound`, `condition` on Hazard in DANGEROUS and WILD; `wound` required for Constitution, `condition` for Fate. Checks: `wound` among `BRIEF.md`'s `Procedures wounds=`; `condition` in `procedures_conditions()`; a Sanity Test outside a Chaos source a warning. A write-up's `(Test of ...)` parenthesis is checked against its Hazard's fields. 13 Hazard lines take their values from the write-ups' parentheses | `patterns/Dangerous_Schema.md`, `Wild_Schema.md`, `templates/region/Tables.md`, `templates/region/Location.md`, `tools/tables.py`, `tools/validate_setting.py`, `setting/region/*/Challenges.md` |
| T2.2 | R2 | `enum Reaction Hostile Wary Fearful Neutral Friendly`; `reaction Reaction`. 51 values rewritten with ` - ` after the item; the Desperate and Cunning ones re-read to an item. `Location.md`'s Demeanor is read from the item | `patterns/Dangerous_Schema.md`, `Wild_Schema.md`, `templates/region/Tables.md`, `templates/region/Location.md`, `setting/region/*/Challenges.md`, `setting/region/*/Rewards.md`, `setting/region/*/Connections.md` |
| T2.3 | R2 | The Reaction mix in `metrics.py`'s corpus report. No `BRIEF.md` default: a mix is the user's to ask for | `tools/metrics.py` |
| T2.4 | R3 | `answers time opt` on DANGEROUS Encounter, with a turn or Round unit. Set on F-M's Encounters from what each `Brief.md` Alarm names. `Brief.md`'s Alarm line is written from them | `patterns/Dangerous_Schema.md`, `templates/region/Tables.md`, `templates/region/Brief.md`, `tools/tables.py`, `setting/region/[F-M]/Challenges.md` |
| T2.5 | R4 | Garrison `answers` becomes `call gloss` and `within time`. Two lines in A | `patterns/Safe_Schema.md`, `templates/region/Tables.md`, `setting/region/A/Garrison.md` |
| T2.6 | R5 | `value price` in the SAFE schema; Purchase `price price` and `per gloss opt`. A `listed` price's item must be on `Procedures.md`'s Coin and Prices list. The Setting Judgement Check compares coin prices against the list. 19 lines in A | `patterns/Safe_Schema.md`, `templates/region/Tables.md`, `templates/region/Location.md`, `templates/checks/Setting_Judgement_Check.md`, `tools/tables.py`, `setting/region/A/Purchases.md` |

---

## Phase 3 - Setting tables

| Task | Spec | What | Files |
|---|---|---|---|
| T3.1 | S1 | `value finds` and Hoards `Items finds`; `Total` dropped. `PRICED_RE` moves into the value's check, and `check_hoard_totals` goes. The site and PDF print the sum under each hoard, in place of the dropped field. 7 Hoards | `patterns/Common_Schema.md`, `Setting_Schema.md`, `templates/setting/Hoards.md`, `tools/tables.py`, `tools/validate_setting.py`, `tools/site_common.py`, `setting/Hoards.md` |
| T3.2 | S2 | Bestiary `Numbers number opt`, and the count taken out of `Range`. A warning for a single holding whose count of a creature (its Encounters' `count`, plus the `present` of each Faction whose `Fields` name it) falls outside `Numbers`. 11 entries | `patterns/Setting_Schema.md`, `templates/setting/Bestiary.md`, `tools/validate_setting.py`, `setting/Bestiary.md` |
| T3.3 | S3 | `enum Age recent living old ancient`; `When Age`; the entries in oldest-first order. The site draws History in that order. 4 entries | `patterns/Setting_Schema.md`, `templates/setting/History.md`, `tools/validate_setting.py`, `setting/History.md` |
| T3.4 | S4 | `enum Roll_Die Combat Skill Magic Difficulty d6`; `Roll Roll_Die`. 8 entries | `patterns/Setting_Schema.md`, `templates/setting/LocalProcedures.md`, `setting/LocalProcedures.md` |
| T3.5 | S5 | `enum Pay fee share favour loan bait`; `Terms Pay`. 5 Quests | `patterns/Setting_Schema.md`, `templates/setting/Quests.md`, `setting/Quests.md` |

---

## Phase 4 - After sheet-maps, and closing

| Task | Spec | What | Files |
|---|---|---|---|
| T4.1 | R6 | `width feet` and `height feet` on Block; the same two `opt` on Connection. A Connection's own size must fall within its rooms' footprints. Each F-M block takes its seed's Conditions sizes; `maps.py` draws corridors at the width. **Waits on sheet-maps T3.2 and T3.8** | `patterns/Dangerous_Schema.md`, `templates/region/Tables.md`, `tools/tables.py`, `tools/maps.py`, `setting/region/[F-M]/Blocks.md` |
| T4.2 | - | `metrics.py` against T0.4's baseline. No step's read set grows by more than the types it reads | - |
| T4.3 | - | `--pending` clean, apart from write-ups whose meaning changed (T2.2's re-read reactions, T3.2's Range). Those are rerun at 5b | `setting/region/*/[0-9]*.md` as owed |
| T4.4 | - | Both builds' `--check`s pass, and `patterns.html` shows every new type | - |

Every task closes with the review `CLAUDE.md` asks: each touched file stated more simply,
nothing restated from elsewhere.

---

## Risks to watch

- **Templates drifting from schemas.** `Tables.md` and `Location.md` describe the fields
  in prose too. Each task edits them alongside the schema, never after it.
- **Retyping that changes meaning.** Only commits that change form and not meaning go in
  `.git-blame-ignore-revs`. A re-read value (T2.2's Desperate and Cunning) is left out, so
  its write-up shows as owed.
- **A check nobody can satisfy.** T3.2's count and T2.6's price comparison are warnings,
  not errors: both compare against a rough figure.
- **Mysteries also ask Tests.** R1 types Hazards only. A Mystery's Test stays in its
  `effect` prose and its write-up's parenthesis. Typing it is a new proposal, not part of
  this plan.
