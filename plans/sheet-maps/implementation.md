# Implementation - maps drawn from the setting, in place of the mermaid diagrams

Task plan for `spec.md`. Two repositories move in step: artgen (`rstevenson1237/image_tools`)
is changed from briefs written here and run in an artgen session; how its work reaches this
repo is D4's. Task ids are cited by
commit messages. Every framework task ends with `python3 tools/validate_setting.py` clean
and commits on its own.

Order: settle the Decisions, prove the drawing on one region of each rating with artgen as
it is, build what the proof shows missing, then change the framework and the tools together,
then migrate Thornmarch and judge it against the reference.

---

## Phase 0 - Decisions

| Task | What | Done when |
|---|---|---|
| T0.1 | D1-D3, D5, D6, D8 settled (`spec.md` section 2) | Done |
| T0.2 | D4: a reusable rule for tools that move in step across projects - how a consumer gets a change, how a consumer's need and its evidence reach the tool, and what a change costs each side | The rule written and settled; `plans/` holds it if it outgrows this plan |
| T0.3 | D7 settled | Marked in `spec.md` |

---

## Phase 1 - Proof with artgen as it is

Scratch scripts outside the repo, extending the evaluation's converters. Nothing commits
here but a findings note in this folder.

| Task | What | Done when |
|---|---|---|
| T1.1 | Block maps for F (one block) and M (four blocks), sizes hand-fed | Both render; door and trap mapping agrees with `spec.md` 6 |
| T1.2 | Ravine sheet for E at 10 yards, entrances of F-M as marks | Renders; legibility gaps logged against A6-A7 |
| T1.3 | Frontier sheet with A-E placed by hand from the outline | Renders; the requirements a constrained generator would need are listed (A2) |
| T1.4 | The Keep as rooms over terrain, hatching off | What A5 must add is listed |
| T1.5 | `findings.md` in this folder | Each artgen item in `spec.md` 9 confirmed, cut or reshaped |

---

## Phase 2 - artgen work, by brief

Each item is a brief written into this folder, with the evidence from phase 1 and the
Thornmarch cases it must draw, then run in an artgen session. Each lands by D4's rule.

| Task | What | Needed by |
|---|---|---|
| T2.1 | A1 the map and dungeon engines usable alone, packaged as D4 settles | T3.1 |
| T2.2 | A3 `facts` for maps and dungeons | T3.7 |
| T2.3 | A4 crop and fit renders | T3.8 |
| T2.4 | A2 constrained generation and `map check` | T3.6 |
| T2.5 | A6 symbols, A7 page-relative sizes | T5.2 |
| T2.6 | A8 hand edits kept across regeneration | T3.6 |
| T2.7 | A5 terrain underlay, walls, towers, gates | T5.1 |

---

## Phase 3 - Framework text and tools, together

The validator must pass after every task, so each tool change lands with the text it checks.

| Task | What | Files |
|---|---|---|
| T3.1 | Bring artgen in by D4's rule; `node` in CI; `README.md` tools list | per D4, `.github/workflows/*.yml`, `README.md` |
| T3.2 | `feet` and `Room_Shape`; `width`, `length`, `height`, `shape` on DANGEROUS and SAFE Dressing; `Block` node and `Blocks` table | `patterns/Common_Schema.md`, `Dangerous_Schema.md`, `Safe_Schema.md`; `tools/tables.py` |
| T3.3 | `sheet`, `ground`, `place` in `BRIEF.md`'s grammar and `--brief` slices | `BRIEF.md` header, `tools/validate_setting.py` |
| T3.4 | Gazetteer `Joins` column; 3a writes it | `patterns/Setting_Schema.md`, `templates/region/Region_Gazetteer.md`, validator |
| T3.5 | 4b rewritten: `Connections.md` with `to` and `orientation`, and `Blocks.md`; 4c drops edge-copying; retire the four `Connections.mmd` templates | `STEPS.md`, `templates/region/Tables.md`, `templates/*/Connections.mmd` |
| T3.6 | `tools/maps.py place`: solver, requirements, `setting/Sheets.md`, sheet JSON; 3b rewritten to run it | `tools/maps.py`, `STEPS.md` |
| T3.7 | `tools/maps.py ground`: each region's `Ground.md`; new step 4d runs it; 4a, 5a, 5b and 5e templates read it | `tools/maps.py`, `STEPS.md`, `templates/region/Tables.md`, `Location.md`, `Brief.md` |
| T3.8 | `tools/maps.py draw`: block, region and cut renders, called by the site and PDF builders | `tools/maps.py`, `build_site.py`, `build_pdf.py` |
| T3.9 | Mermaid out: site script, `app.js`, `site_common` readers, validator `.mmd` parsing; the same edge lists read from `Connections.md` | `tools/*` |
| T3.10 | Section 10's checks | `tools/validate_setting.py`, `tools/tables.py` |
| T3.11 | `Ground.md` size in `metrics.py`'s read-set report | `tools/metrics.py` |
| T3.12 | Region Schema Layout lines: a Layout reads its maps and `Ground.md`, and says what a map cannot (what is noticed, what is heard) | `patterns/Region_Schema.md` |

Every task closes with the review `CLAUDE.md` asks: each touched file stated more simply,
nothing restated from elsewhere.

---

## Phase 4 - Migrate Thornmarch

| Task | What | Done when |
|---|---|---|
| T4.1 | `BRIEF.md`: Frontier, Ravine and Keep sheets; each region's `ground` and `place` | `--brief` prints them |
| T4.2 | Gazetteer `Joins` from today's `setting/region/Connections.mmd`; then delete every `.mmd` | No `.mmd` under `setting/` |
| T4.3 | `Blocks.md` for F-M: one block each for F-L unless a change of level splits it; M by its four blocks | Every DANGEROUS location in one block |
| T4.4 | E fitted to the Ravine sheet (D6): compressed, or the square coarsened where that plays better; every E `at` and Stop rewritten | E's locations all on the Ravine sheet |
| T4.5 | K.1 folded into E.7 or rewritten as K's own entrance room, so K starts where its caves start | K draws without a strip |
| T4.6 | Footprints on every DANGEROUS Dressing and A's buildings, taken out of `layout` and each `Brief.md` | No location the validator calls unsized |
| T4.7 | `maps.py place`, `ground`, `draw`; 5b and 5e rerun where `Ground.md` contradicts a write-up | Validator clean; both `--check`s pass |

---

## Phase 5 - SAFE, and judging

| Task | What | Done when |
|---|---|---|
| T5.1 | The Keep drawn with walls, towers and gate (A5) | Renders as a fort plan |
| T5.2 | Legibility pass with A6-A7 on every sheet | Labels readable at print size |
| T5.3 | Play check against `spec.md` 1's table, sheet by sheet, written to `setting/checks/` by the Setting Judgement Check | Each row met, or a finding sent to its step |
| T5.4 | Token check: `metrics.py` before and after, per step's read set | No step's read set grows by more than its `Ground.md` |

---

## Risks to watch

- **The solver never converging.** A `place` set that cannot all hold is reported by line,
  never retried blindly; the remedy is the brief, not the seed.
- **Generated ground contradicting written prose.** `Ground.md` is written before 4a, so
  writing follows the ground; a later regeneration that moves a feature marks the write-ups
  that cite it stale.
- **`Ground.md` growing into a second Layout.** It holds facts by code, never prose; its
  size is counted at T3.11.
- **artgen and this repo drifting.** The vendored file is pinned; upgrading it is its own
  commit, run against Thornmarch's maps.
- **Hand edits lost.** A8 lands before any hand edit is made (T2.6 before T4.7).
