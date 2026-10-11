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
| T0.1 | D1-D4 and D6-D9 settled (`spec.md` section 5) | Done |
| T0.2 | D5 and D10 confirmed | Done |

---

## Phase 1 - Framework text, and the lint kept working

Order matters inside this phase. T1.1 moves the templates before anything else touches
them. T1.13 (`STEPS.md`) lands last, in one commit with the templates it names, so the
validator never sees a step whose template doesn't exist.

| Task | What | Files | Done when |
|---|---|---|---|
| T1.1 | **Template folders (D9).** `git mv` every template into `templates/setting/`, `templates/region/` or `templates/checks/` per `spec.md` section 8; update every `templates/X.md` citation in `STEPS.md`, templates, patterns, `README.md` and tool comments; teach the validator's read-set graph, `metrics.py` and `context.py` folder paths. No content change | `templates/**`, `STEPS.md`, `README.md`, `tools/validate_setting.py`, `tools/metrics.py`, `tools/context.py` | `--read-set` resolves every step as before; `metrics.py` counts the same template words; the validator is clean |
| T1.2 | Write into `patterns/SPEC.md`: the placement rule (`spec.md` 7.1), the fold test (7.3), and the two F20 rules (a unique column label per Spec line; a line no tag or gloss answers splits). Add one line to `CLAUDE.md`'s Pattern file rules pointing there | `patterns/SPEC.md`, `CLAUDE.md` | The rule reads as in 7.1; `CLAUDE.md` gains one line only |
| T1.3 | Apply the rule by hand to every Spec line, recording line → column, pattern → table, table → file, per rating | `plans/table-pipeline/inventory.md` (new) | Every pattern file appears once; `spec.md` 7.5 is corrected where the rule disagrees with it (the rule wins) |
| T1.4 | Pathway simplifications P1-P5 (`spec.md` 7.4): Treasure's lesser thing becomes a gloss line; Payload items `{cache, lore, key}` point at a `Treasures.md` row; split `dangerous/Key.md` into `Key.md` (supply) and new `dangerous/Lock.md` (demand), redirecting the class files' lock lines, Door's fitted gate and Mystery's remote answer to Lock; new `wild/Exit.md` and `safe/Exit.md` from the Dressing exit lines. Then the F20 migration over every file T1.3 flags: labels, splits, clashing labels renamed; phase-4 citations moved | pattern files | Every Spec line answers in one tag or one gloss; every pattern has one home; the validator's pattern and reachability checks pass |
| T1.5 | Lint, region folder (F13): location-file glob narrowed to `[0-9]*.md` | `tools/validate_setting.py` | A `Challenges.md` beside `Locations.md` raises nothing |
| T1.6 | **Generic parsers** (D5): one pipe-table reader (from `site_common.parse_table_rows`) and one record reader (from `parse_field_lines`, extended to `### [Name]` headers), shared by the validator and the site builders. Each check that read a file through a bespoke regex now reads cells or fields; the value-level grammars (`AD:`, forced damage, codes) are kept and applied to a cell or field | `tools/site_common.py`, `tools/validate_setting.py`, `tools/build_site.py`, `tools/build_pdf.py` | Fixtures of every migrated file pass; every existing check still fires on its bad fixture; `REGION_RE`, `LOC_GAZ_RE`, `BESTIARY_HEADER_RE`, `FACTION_HEADER_RE` and the registry marker split are gone |
| T1.7 | **Migrate the existing table files** (D10, `spec.md` 6.4): rewrite the Template blocks of `Region_Gazetteer`, `Keys`, `Quests`, `Truths` (to pipe tables) and `Bestiary`, `NamedCreatures`, `UniqueTreasures`, `Lore`, `Factions`, `History` (to records); column and field names are their patterns' Spec labels. `Rumours`, `Treasure` and `Language` are unchanged | the ten templates | Each Template block matches the format test; no template lists a field its pattern doesn't own |
| T1.7a | **Lint, D6 stubs**: errors for a cell count that differs from its header, an unknown id, code or field, or a duplicate id; **a warning per stub** (an empty cell, or a record missing a field its pattern requires), naming the file, the entry, what's missing and the step it is owed to; `--pending [REGION]` groups them by step. `check_key_obligations` folds into this | `tools/validate_setting.py` | Fixtures for each error and for a stub in each shape give the expected output |
| T1.8 | The three `templates/[rating]/Locations.md` (replacing `Location_Gazetteer.md`, whose content moves rather than being copied): the rating's count, weight / classification / prominence mix, tag rules, and the file's tables by pattern; Context per step (4a, 4b, 4f substrate, 4g) | `templates/safe/`, `templates/wild/`, `templates/dangerous/Locations.md` | No column is listed that a pattern owns; each rating's mix lives in exactly one file |
| T1.9 | The remaining rating templates: `Exits.md` (all three ratings), and `Challenges.md`, `Treasures.md`, `Links.md` where the rating has them (`spec.md` 7.5). Context = 9.3's read set; Instructions = which locations get rows and in what mix (D2), fill only unclaimed stubs, never re-decide an allocated tag, cells per D4, the distinctness rules this file's columns expose; Template = the file's tables, by pattern. No column lists | `templates/[rating]/*.md` | Each rating folder lists exactly that rating's files; no template copies a Spec line |
| T1.10 | `templates/region/Allocation.md` (4d, by hand): create every file and table with its header; one stub per decided line, with its allocated tags; one Exits row per edge with its gate decided once; count against Inhabitants and each rate; log every rated decision | `templates/region/Allocation.md` | A reader can allocate a region from it plus the class files; it restates no rate |
| T1.11 | Compositions (D7): the `Compositions` field in each `patterns/region/*.md` and in `templates/region/Region.md`; new `templates/region/Composition.md` with the design steps, stub claiming, exceptions, the eight-item proof (9.5), and retrofit recompile | `patterns/region/*.md`, `templates/region/Region.md`, `templates/region/Composition.md` | The field appears once per rating; the proof lives only in the template |
| T1.12 | `templates/region/Location.md` becomes compile (11.1, 11.2); Template block and Citations unchanged. The five registry templates: stubs at 4d or 4e, entries at 4h, Context reading the placing rows | `templates/region/Location.md`, `templates/setting/` registries | Output format unchanged; no `context.py` reference left in them |
| T1.13 | Rewrite phase 4 of `STEPS.md` per `spec.md` 9.1, with every template by path | `STEPS.md` | No unknown-step or missing-template diagnostic |
| T1.14 | Judgement items added to `templates/checks/Setting_Judgement_Check.md`; `README.md` names the template folders and the five region files | those two files | Additions only; points only |

**Tools during phases 2-3.** `draw.py` and `context.py` stay in the tree, untouched beyond
T1.1's path fix, and unused. `context.py` may stop parsing the new `Locations.md`, and
that's acceptable while nothing reads it. Phase 5 settles them.

---

### Phase 1 status: done

Landed in commits dc243e8 (T1.1) through 9d891b6 (T1.8-T1.14). Where the work departed
from the table above:

- **No separate weights template.** Each `templates/[rating]/Locations.md` owns its
  rating's count, mix, tags and weights (`spec.md` section 8), so steps 4a, 4b, 4f and 4g
  all name it.
- **`To` is a key column, not a Spec line.** `dangerous/Door.md`, `wild/Exit.md` and
  `safe/Exit.md` lost their "where it goes" line. Allocation also writes a row for each way
  off the map that the Overview's Approach names.
- **`Realized` is owed only once its location file exists**, so the to-do list does not
  carry one line per row before compile.
- **`check_key_obligations` survives only as the build-complete error.** The open case is
  an ordinary stub (an empty Opens cell).
- **Rule lines became `--` comment lines** inside the Spec block where they carry a rule
  about other lines (Settlement's gate terms, Secret's access payload). Other rule lines
  moved to Constraints or Provides, per `inventory.md`.
- **Pre-existing, not changed:** `build_site.py` fails on an empty `setting/` (it reads
  `setting/Setting.md` unconditionally), and `patterns/setting/Language.md` carries two
  rate-notation warnings. Both predate this change.
- **Proven on a fixture setting** (in the scratchpad, not committed). Every planted fault
  was caught (short row, duplicate ID, unknown location, dangling id reference, unknown
  record field), stubs were listed by step, and the site, metrics and `context.py` all ran.

## Phase 2 - Pilot log

| Task | What | Done when |
|---|---|---|
| T2.1 | Create `plans/table-pipeline/pilot-log.md`: one section per pass, recording step; files read, with sizes; rows written; every rated decision as `rate asked -> taken / not taken`; rows compile sent back, and why; lines that wouldn't fit a six-word cell; composition exceptions; the hand checklist (`spec.md` section 11) ticked; time spent | Its sections exist before the first pass |

---

## Phase 3 - Hand-run pilot

| Task | What | Done when |
|---|---|---|
| T3.1 | Steps 1-3 from `BRIEF.md`, with the moved templates and the new Overview field left empty | Validator clean through step 3 |
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
  copy of the pattern. Checked at T1.8-T1.9 and by 5b.
- **Six words not enough (D4).** A line that keeps overflowing is asking two things.
  The remedy is to split the line, never to widen the cell. Logged at every pass.
- **Standalone rows that don't fit their room (F1).** Measured at T3.8. The remedy is the
  narrowest added input.
- **Compositions fighting the weights (F17).** Measured by the exception count.
- **Too many tables (F22).** Any table the pilot logs as busywork is put to `spec.md`
  7.3's fold test. It merges only if the test passes.
- **Hand allocation collapsing to the average (F19).** This is the experiment. T5.2 is the
  fix if it happens.
