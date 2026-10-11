# Implementation - the content loop

Each task ends with `python3 tools/validate_setting.py` clean, and with the minimal-set
review from `CLAUDE.md` run on every file it wrote. Task ids are cited in commit messages.

## Phase 1 - Framework

| Task | What | Files |
|---|---|---|
| T1 | Renumber every phase contiguously, with no retired stubs. Phase 4 ends at 4c and phase 5 is the loop. Cut `STEPS.md` to the minimal set. Move every step-id citation with it | `STEPS.md`, `templates/**`, `README.md`, `tools/validate_setting.py` |
| T2 | Mark each region pattern field as seed (3c) or brief (5e); `templates/region/Region.md` writes each at its step; the validator owes the brief fields to 5e | `patterns/region/*.md`, `templates/region/Region.md`, `tools/validate_setting.py` |
| T3 | Stubs: a bare entry is a warning owed to 5a, and `--pending` lists stubs; the schema's percentage rates become ranges; `templates/dangerous/Tables.md` 4c (stubs) and 5a (fill) | `patterns/Schema.md`, `tools/tables.py`, `templates/dangerous/Tables.md` |
| T4 | `BRIEF.md` targets: format, validator checks on paths and totals, metrics realized-against-target; the template mixes move into `BRIEF.md` | `BRIEF.md`, `tools/tables.py`, `tools/metrics.py`, `templates/**` |
| T5 | Staleness from `git blame` at entry grain, listed by `--pending`; metrics reads tables for MIX and names 5b in READ SET | `tools/validate_setting.py`, `tools/tables.py`, `tools/metrics.py` |
| T6 | Quests point one way, written at 5d; key pairing; key not behind its own lock | `patterns/setting/Quests.md`, `templates/setting/Quests.md`, `tools/tables.py` |
| T7 | `templates/checks/Location_Review.md` (5c); trim `Setting_Judgement_Check.md` to the cross-level items | `templates/checks/` |
| T8 | 5d placement: Rumours (from 2d), Quests, locks then keys, the setting registries' write steps | `templates/setting/Rumours.md`, `Quests.md`, `Keys.md`, `Lore.md`, `Truths.md`, `History.md` |

## Phase 2 - Pilot on region A

| Task | What | Done when |
|---|---|---|
| T9 | Rewrite `A.md` to its seed; restate A's entries as 4c stubs with the members placement fixed | The validator lists the stubs |
| T10 | Passes until the loop exits: 5a, 5b, 5c with `setting/checks/Review.md`, 5d with the rumour table, one quest and one lock-then-key | Exit reached; every pass's readings are in `Review.md` |
| T11 | The determinism probe: rewrite one non-stale location and read the diff | The result is recorded in `Review.md` |
| T12 | 5e brief for A; 6c on A | `SettingJudgementCheck.md` written |

## Phase 3 - SAFE and WILD

Written piece by piece as a pilot region needs them: the schema folder, the 4c/5a
template, and lint for each new node.
