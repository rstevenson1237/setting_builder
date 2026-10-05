# Implementation - table-driven location generation

Task plan for `spec.md`. **Hand first, tools after** (D8): phases 1-3 build and run the new
pipeline with no `draw.py` and no `context.py`. Phase 4 writes the analysis. Phase 5
rebuilds only the tools the analysis calls for. Task ids are cited by commit messages.

The validator runs unchanged throughout phases 1-3. Every framework change ends with
`python3 tools/validate_setting.py` clean, and commits on its own.

---

## Phase 0 - Decisions

| Task | What | Done when |
|---|---|---|
| T0.1 | Get the user's answers to D1-D8 (`spec.md` section 5). D1 needs an explicit yes under `README.md`'s renumbering rule | Each answer recorded in `spec.md` section 5 |
| T0.2 | Where an answer differs from the recommendation, update `spec.md` and the tasks below | The two files agree with the decisions |

Tasks a different answer would change are marked **[D#]**.

---

## Phase 1 - Framework text for a hand-run pipeline

Everything a hand-run pilot needs, and nothing tool-side. T1.9 (`STEPS.md`) lands last, in
the same commit as the templates it names, so the validator never sees a step whose
template doesn't exist yet.

| Task | What | Files | Done when |
|---|---|---|---|
| T1.1 | Write the table test into `patterns/SPEC.md` beside "A draw or an edge is decided by what the pick opens"; cut the `dangerous/Key.md` "two files" paragraph back to a pointer; add one line to `CLAUDE.md`'s Pattern file rules | `patterns/SPEC.md`, `CLAUDE.md` | The test reads as in `spec.md` section 6; `CLAUDE.md` gains one line only |
| T1.2 | Apply the test by hand to every Spec line in `patterns/`, and record the inventory: table or column group, per unit, per rating | `plans/table-pipeline/inventory.md` (new) | Every pattern file appears once; `spec.md` section 7 is corrected where the test disagrees with it (the test wins) |
| T1.3 | New `patterns/setting/Compositions.md`: a leaf whose Spec is the composition row's lines and proof items (`spec.md` 8.7), with Constraints for F16 and F17. Add its edge to `patterns/Genre.md`'s SETTING block **[D7]** | `patterns/setting/Compositions.md`, `patterns/Genre.md` | Reachable from the root; the validator's pattern checks pass |
| T1.4 | `templates/Location_Gazetteer.md` loses weight; its Purpose says the file is the location table, whose first line is the stub. New `templates/Location_Weights.md` takes the weight mix (moved, not copied) and SAFE prominence | both templates | No weight left in the gazetteer's Template block; the mix lives in exactly one file |
| T1.5 | New `templates/Allocation.md` (4d, by hand): walk each room's class file across the whole region; one stub per decided line; one `Exits` stub per edge with its gate decided once; count against Inhabitants and against each rate before moving on; log every rated decision. Restates no rate | `templates/Allocation.md` | A reader can allocate a region from it plus the class files |
| T1.6 | New `templates/Composition.md` (4e): design the build, claim stubs first, author exceptions with reasons, write every part and the composition row in one pass, run the proof, and on retrofit, list the rooms and recompile per `templates/Location.md`'s targeted rule **[D7]** | `templates/Composition.md` | Names `patterns/setting/Compositions.md` as its entry |
| T1.7 | New `templates/Table_[Name].md`, one per table in `inventory.md`. Context = `spec.md` 8.4's read set for that table, and nothing more; Instructions = the distinctness rules this table's rows are checked against, "fill only unclaimed stubs", "never re-decide an allocated value"; Template = the record shape (`spec.md` 8.1). Columns are not listed; they are the pattern's Spec **[D2, D5]** | `templates/Table_*.md` | Each names exactly one pattern entry; none copies a Spec line |
| T1.8 | `templates/Location.md` becomes compile: Context reads every row naming this location; Instructions gain "every row realized, nothing without a row, no fact added or dropped, record `Realized:`" and the targeted recompile rule (`spec.md` 9.2). Template block and Citations unchanged. The five registry templates: stubs at 4d/4e, full entries at 4h, with Context reading the placing rows **[D4]** | `templates/Location.md`, five registry templates | The output format is unchanged; no `context.py` reference is left in these files |
| T1.9 | Rewrite phase 4 of `STEPS.md` per `spec.md` 8.2, and move every phase-4 step-id citation to its new id **[D1, D6]** | `STEPS.md`, `templates/*`, `patterns/SPEC.md`, `patterns/dangerous/Key.md`, `patterns/dangerous/Lore.md`, `patterns/wild/Lore.md`, `README.md` | The validator raises no unknown-step citation and no missing-template warning |
| T1.10 | Add the three judgement items (`spec.md` section 10) to the setting check | `templates/Setting_Judgement_Check.md` | Three items added, nothing else rewritten |
| T1.11 | `README.md`: map `tables/` and `setting/Compositions.md` | `README.md` | Points only |

**Note on the tools during phases 1-3.** `README.md` and `templates/Location.md` stop
pointing at `context.py 4c` (T1.8). The tools stay in the tree untouched, still runnable,
and are retired or rebuilt in phase 5. `context.py`'s parsing of `Locations.md` may break
once weight moves out of the gazetteer line. That's acceptable while nothing reads it,
and T5.0 settles it.

---

## Phase 2 - Pilot log

| Task | What | Done when |
|---|---|---|
| T2.1 | Create `plans/table-pipeline/pilot-log.md` with one section per pass: pass id and step; files read, with sizes; rows written; every rated decision as `rate asked -> taken / not taken`; rows compile sent back, with the reason; composition exceptions; the hand checklist (`spec.md` section 10) ticked per pass; time spent | The template sections exist before the first pass runs |

The log is the analysis's evidence. A pass that isn't logged didn't happen, as far as
phase 4 is concerned.

---

## Phase 3 - Hand-run pilot

No `draw.py` and no `context.py`. Read sets are assembled by opening the files the
template names.

| Task | What | Done when |
|---|---|---|
| T3.1 | Build steps 1-3 from `BRIEF.md` under the existing templates (unchanged by this plan) | Validator clean through step 3 |
| T3.2 | 4a-4c for the keep (SAFE), the borderland (WILD), the ravine (WILD), and two caves (DANGEROUS), chosen so that one edge crosses regions | Gazetteers, weights and diagrams exist; validator clean |
| T3.3 | 4d allocation for those five regions, region by region, each in one pass | Every allocated row exists as a stub; counts reconcile with Inhabitants; rated decisions logged |
| T3.4 | 4e: at least one composition spanning three or more rooms in one cave, written in one pass and proven by hand (all eight items) | The composition row and every part row exist; the proof is ticked in the log |
| T3.5 | 4f table passes in `spec.md` 8.3's order. The creatures pass is run strictly from 8.4's read set (Inhabitants, the named Bestiary/Factions entries, and its stubs), as the test of standalone rows | Every unclaimed stub filled; distinctness checklist ticked per table |
| T3.6 | 4g naming and name sync, by hand | Diagram labels and registry lines match `Locations.md` |
| T3.7 | 4h connected fill: the cross-region exit, then every registry's full entry | No stub left |
| T3.8 | 4i compile for every pilot location | Every row realized exactly once; the validator's location checks pass |
| T3.9 | **Retrofit**: a second composition into the other cave (or across the ravine and a cave), touching at least two already-compiled rooms, followed by targeted recompile | Only the lines `spec.md` 9.2 allows changed, visible in the diff; proof ticked |
| T3.10 | 4j coinage and mechanics; then 5c on the pilot regions | `setting/checks/SettingJudgementCheck.md` written, including the three new items |

Commit per pass, so each pass's diff can be read on its own.

---

## Phase 4 - Analysis

| Task | What | Done when |
|---|---|---|
| T4.1 | Write `plans/table-pipeline/analysis.md` answering every question in `spec.md` section 11 from the pilot log and the 5c check, each answer with its decision: keep as is, rebuild a tool, change a template, or revisit a D# | Every question has evidence and a decision |
| T4.2 | Compare the 5c findings with the second-run addendum at commit 9c1354b, item by item for "rooms are distinct" and "draws realized" | The comparison table is in `analysis.md` |
| T4.3 | Walk `spec.md` section 13's acceptance list | All nine met, or each miss has a named follow-up the user accepts |
| T4.4 | Plan phase 5 from the analysis: keep only the tasks below that it calls for, and add any it finds | Phase 5 of this file is trimmed to match `analysis.md` |

This is a checkpoint with the user before any tool work starts.

---

## Phase 5 - Wire back the tools, where called for

Each task runs only if `analysis.md` calls for it. The table names the finding that
triggers it.

| Task | Triggered by | What | Files |
|---|---|---|---|
| T5.0 | always | Make `site_common`'s gazetteer parsing read the new `Locations.md` record (first line plus indented columns), and confirm `build_site` / `build_pdf` ignore `tables/` | `tools/site_common.py` |
| T5.1 | always, if T5.2 or T5.3 runs | Fix E5's resolution bugs (MEDIUM never absent; FAMILY only on purpose blocks), with regression checks, before reusing the walk | `tools/context.py` |
| T5.2 | rates collapsed under hand allocation | `allocate [Code]`: the class-file walk emitting stub rows, seeded per row id (one gate per edge), plus the allocation report (asked against realized; headcount against Inhabitants); idempotent, and refuses to change a filled row | `tools/tables.py` (new), `tools/draw.py` (seed helper) |
| T5.3 | assembling read sets was the costly part | `sheet [Code] [Table]` printing exactly 8.4's read set, and `sheet [Code]` printing one location's rows for compile; then retire `context.py 4c` | `tools/tables.py`, `tools/context.py` |
| T5.4 | checklist items were tedious or missed | Validator: table parsing; format and key errors; one `Exits` row per edge matching its diagram; unfilled-stub and unrealized-row warnings; the distinctness rules; the mechanical composition proof items (8.7, ⚙); `--pending` for connected stubs | `tools/validate_setting.py` |
| T5.5 | name sync was error-prone | `sync-names`: rewrite `.mmd` labels and registry lines from `Locations.md` | `tools/tables.py` |
| T5.6 | the cost question stays open | `metrics.py` per-table counts and asked against realized; `context.py cost` gains the table strategy, calibrated against the pilot log | `tools/metrics.py`, `tools/context.py` |
| T5.7 | after any of the above | `README.md` command list matches the tools; cut any prose that restated the old 4c route back to a pointer | `README.md`, templates |

---

## Risks to watch

- **A table template drifting into a pattern copy (F4).** The fastest symptom is a
  template listing columns. Checked at T1.7 and by 5b.
- **Standalone rows that don't fit their room (F1).** Measured at T3.8 by rows sent back.
  The remedy is the narrowest added input, never a whole room.
- **Compositions fighting the weights (F17).** Measured by the exception count. If it runs
  high, compositions move before 4b for the rooms they claim.
- **Hand allocation collapsing to the average (F19).** This is the experiment. The log
  makes it measurable, and T5.2 is the fix if it happens.
- **Retrofit sprawl (F18).** A retrofit diff touching lines outside 9.2's rule is a
  compile failure, not a style choice.
