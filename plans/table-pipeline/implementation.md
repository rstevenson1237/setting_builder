# Implementation - table-driven location generation

Task plan for `spec.md`. **Hand first, tools after** (D8). Phase 1 changes the framework
text, plus the few lint changes the new file shapes need. Phases 2-3 run a pilot by hand,
with no `draw.py` and no `context.py`. Phase 4 writes the analysis, and phase 5 rebuilds
only the tools it calls for. Task ids are cited by commit messages.

Every framework change ends with `python3 tools/validate_setting.py` clean and commits on
its own.

---

## Phase 0 - Decisions

| Task | What | Done when |
|---|---|---|
| T0.1 | D1-D4 and D6-D8 settled (`spec.md` section 5) | Done |
| T0.2 | Confirm D5: strict pipe tables, one section per pattern file (`spec.md` section 6) | The user confirms or picks another option; if another, sections 6-8 of `spec.md` and tasks T1.3-T1.6 below are revised first |

---

## Phase 1 - Framework text, and the lint kept working

T1.12 (`STEPS.md`) lands last, in one commit with the templates it names, so the validator
never sees a step whose template doesn't exist.

| Task | What | Files | Done when |
|---|---|---|---|
| T1.1 | Write into `patterns/SPEC.md`: the three-way test (`spec.md` 6.5), the Spec-line-to-column mapping (7), and the two F20 rules (every Spec line opens with a column label unique within its file; a line no tag or gloss can answer splits). Cut the `dangerous/Key.md` "two files" paragraph back to a pointer. Add one line to `CLAUDE.md`'s Pattern file rules | `patterns/SPEC.md`, `CLAUDE.md` | The test reads as in 6.5; `CLAUDE.md` gains one line only |
| T1.2 | Apply the test by hand to every Spec line in `patterns/`, recording each line's home (column / section / file) per rating | `plans/table-pipeline/inventory.md` (new) | Every pattern file appears; `spec.md` 6.6 and 8 are corrected where the test disagrees with them (the test wins) |
| T1.3 | Pattern migration (F20), using T1.2's inventory: give every Spec line a label; split every compound line; rename clashing labels within a file (Trap's "Mechanism" becomes `Parts`); move phase-4 step citations. Content otherwise unchanged (D2) | the pattern files T1.2 flags | Every Spec line answerable by one tag or one gloss; `validate_setting.py`'s pattern checks pass; 5b's duplication check still reads restatement across rating folders as deliberate |
| T1.4 | Lint, region folder (F13): narrow the location-file glob to `[0-9]*.md`, so table files aren't read as locations | `tools/validate_setting.py` | A `Hazards.md` beside `Locations.md` raises nothing |
| T1.5 | Lint, `Locations.md` (F15): the validator's and `site_common`'s gazetteer parsers read the `## Location` pipe-table section, keeping every existing check (codes, names, weight values, 1..N) | `tools/validate_setting.py`, `tools/site_common.py` | A fixture `Locations.md` in the new shape passes; today's checks fire on bad fixtures |
| T1.6 | Lint, tables (D6): generic pipe-table parsing for every table file in a region folder. Errors: a row's cell count differs from its header; an unknown id or code in a foreign-key column; a duplicate id. **Warning per stub row**: file, id, empty columns, owed step. `--pending [REGION]` groups the same list by step | `tools/validate_setting.py` | Fixtures for each error, and for a stub, give the expected output |
| T1.7 | `templates/Location_Gazetteer.md`: the file becomes the location table; its Template block becomes the `## Location` section (Code, Name, Tags, Weight empty, Block), and lists `Locations.md`'s other sections by pattern (Dressing, class, kind, Naming), with columns read off those patterns. Weight's mix moves to the new `templates/Location_Weights.md` (4b), along with SAFE prominence | both templates | The mix lives in exactly one file; no column is listed that a pattern already owns |
| T1.8 | `templates/Allocation.md` (4d, by hand): create every file and section with its header; walk each room's class file across the region; one stub row per decided line, with its allocated tags; one `Exits` row per edge with its gate decided once; count against Inhabitants and each rate; log every rated decision | `templates/Allocation.md` | A reader can allocate a region from it plus the class files; it restates no rate |
| T1.9 | One `templates/Table_[File].md` per file in `spec.md` 8. Context = 9.3's read set for that file; Instructions = which locations get rows and in what mix (D2), fill only unclaimed stubs, never re-decide an allocated tag, cells per D4, the distinctness rules visible in this table's columns; Template = the file's section list, by pattern. No column lists | `templates/Table_*.md` | Each names its first section's pattern as its entry; none copies a Spec line |
| T1.10 | Compositions (D7): add the `Compositions` field to each `patterns/region/*.md` Spec and to `templates/Region.md`'s Template block (written at 4e, audited at 5c); new `templates/Composition.md`: design, claim stubs, author exceptions with reasons, write the parts and the Overview entry in one pass, run the eight-item proof (9.5), and on retrofit recompile per 10.2 | `patterns/region/*.md`, `templates/Region.md`, `templates/Composition.md` | The field appears once per rating; the proof is in the template, not restated elsewhere |
| T1.11 | `templates/Location.md` becomes compile: Context = every row naming this location; Instructions gain "every row realized, nothing without a row, cells are notes rather than text, no fact added or dropped, record `Realized`" and 10.2's targeted recompile. Template block and Citations unchanged. The five registry templates: stubs at 4d or 4e, full entries at 4h, Context reading the placing rows | `templates/Location.md`, five registry templates | The output format is unchanged; no `context.py` reference is left in them |
| T1.12 | Rewrite phase 4 of `STEPS.md` per `spec.md` 9.1, and move every phase-4 step citation in templates, `README.md` and tool comments | `STEPS.md` and citing files | No unknown-step or missing-template diagnostic |
| T1.13 | Judgement items (`spec.md` section 11) added to the setting check; `README.md`'s region-folder entry names its table files | `templates/Setting_Judgement_Check.md`, `README.md` | Additions only; points only |

**Tools during phases 2-3.** `README.md` and `templates/Location.md` stop pointing at
`context.py 4c` (T1.11). `draw.py` and `context.py` stay in the tree, untouched and
unused. `context.py` may stop parsing the new `Locations.md`, and that's acceptable
while nothing reads it. Phase 5 settles them.

---

## Phase 2 - Pilot log

| Task | What | Done when |
|---|---|---|
| T2.1 | Create `plans/table-pipeline/pilot-log.md`: one section per pass, recording step; files read, with sizes; rows written; every rated decision as `rate asked -> taken / not taken`; rows compile sent back, and why; lines that wouldn't fit a six-word cell; composition exceptions; the hand checklist (`spec.md` section 11) ticked; time spent | Its sections exist before the first pass |

---

## Phase 3 - Hand-run pilot

| Task | What | Done when |
|---|---|---|
| T3.1 | Steps 1-3 from `BRIEF.md`, with the existing templates plus the new Overview field left empty | Validator clean through step 3 |
| T3.2 | 4a-4c for the keep (SAFE), the borderland and the ravine (WILD), and two caves (DANGEROUS), chosen so one edge crosses regions | Gazetteers, weights and diagrams exist; validator clean |
| T3.3 | 4d allocation, region by region | Every allocated row is a stub; the stub warnings are the to-do list; counts reconcile with Inhabitants; rated decisions logged |
| T3.4 | 4e: a composition across three or more rooms in one cave, in one pass, proven by hand | The Overview entry and its part rows exist; proof ticked in the log |
| T3.5 | 4f table passes in 9.2's order. The creatures pass runs strictly from 9.3's read set | Every unclaimed, unconnected stub filled |
| T3.6 | 4g naming and the name sync, by hand | Labels and registry lines match `Locations.md` |
| T3.7 | 4h connected fill: exits, locks, foreshadowing (the cross-region exit included), then registry entries | No stub warnings left |
| T3.8 | 4i compile for every pilot location | Every row realized exactly once; the validator's location checks pass |
| T3.9 | Retrofit: a second composition touching at least two compiled rooms, then targeted recompile | Only the lines 10.2 allows changed, visible in the diff; proof ticked |
| T3.10 | 4j; then 5c on the pilot regions | `setting/checks/SettingJudgementCheck.md` written, including the new items |

Commit per pass, so each pass's diff can be read on its own.

---

## Phase 4 - Analysis (checkpoint with the user)

| Task | What | Done when |
|---|---|---|
| T4.1 | Write `plans/table-pipeline/analysis.md`, answering every question in `spec.md` section 12 with evidence and a decision | Every question answered |
| T4.2 | Compare 5c with the second-run addendum at 9c1354b, item by item, for "rooms are distinct" and "draws realized" | Comparison table in `analysis.md` |
| T4.3 | Walk `spec.md` section 14's acceptance list | All nine met, or each miss has a follow-up the user accepts |
| T4.4 | Trim phase 5 to what `analysis.md` calls for | Phase 5 of this file matches it |

---

## Phase 5 - Wire back the tools, where called for

| Task | Triggered by | What | Files |
|---|---|---|---|
| T5.1 | T5.2 or T5.3 running | Fix E5 (MEDIUM never absent; FAMILY on purpose blocks only), with regression checks | `tools/context.py` |
| T5.2 | hand allocation collapsed the rates | `allocate [Code]`: the class-file walk writing stub rows into the pipe tables, seeded per row id (one gate per edge), plus the allocation report (asked against realized; headcount against Inhabitants); idempotent, and never changes a filled row | `tools/tables.py` (new), `tools/draw.py` (seed helper) |
| T5.3 | assembling read sets by hand was the costly part | `sheet [Code] [File]` (9.3's read set) and `sheet [Code]` (one location's rows, for compile); retire `context.py 4c` | `tools/tables.py`, `tools/context.py` |
| T5.4 | checklist items were missed | Validator: kind-to-section pairing, one `Exits` row per diagram edge (matching kind and direction), unrealized rows, the distinctness rules, and the ⚙ composition proof items | `tools/validate_setting.py` |
| T5.5 | name sync was error-prone | `sync-names`: diagram labels and registry lines from `Locations.md` | `tools/tables.py` |
| T5.6 | cost still open | `metrics.py` per-table counts and asked against realized; `context.py cost` gains the table strategy, calibrated on the pilot log | `tools/metrics.py`, `tools/context.py` |
| T5.7 | after any of the above | `README.md` commands match the tools; prose that restated the old route cut back to pointers | `README.md`, templates |

---

## Risks to watch

- **A table template listing columns (F4).** It means the template has become a second
  copy of the pattern. Checked at T1.9 and by 5b.
- **Six words not enough (D4).** A line that keeps overflowing is asking two things.
  The remedy is to split the line, never to widen the cell. Logged at every pass.
- **Standalone rows that don't fit their room (F1).** Measured at T3.8. The remedy is the
  narrowest added input.
- **Compositions fighting the weights (F17).** Measured by the exception count.
- **Hand allocation collapsing to the average (F19).** This is the experiment. T5.2 is the
  fix if it happens.
