# Implementation - table-driven location generation

Task plan for `spec.md`. Phases are in dependency order. Each task names the files it
touches and what "done" means. Task ids are cited by `spec.md` (T1.3) and by commit
messages. Phase 4 (A2, allocation only) is a working milestone that can ship and be
piloted on its own before phases 5-6 exist.

Every task that changes framework files ends with `python3 tools/validate_setting.py`
clean against an empty `setting/`, and commits on its own.

---

## Phase 0 - Decisions

| Task | What | Done when |
|---|---|---|
| T0.1 | Get the user's answers to D1-D6 (`spec.md` section 5). D1 needs an explicit yes under `README.md`'s renumbering rule | Each answer recorded in `spec.md` section 5, in place of "Recommended" |
| T0.2 | If any answer differs from the recommendation, update the affected sections of `spec.md` and the tasks below before starting phase 1 | `spec.md` and this file agree with the decisions |

Everything below assumes the recommended answers. The tasks a different answer changes
are marked **[D#]**.

---

## Phase 1 - Foundations

| Task | What | Files | Done when |
|---|---|---|---|
| T1.1 | Fix E5's resolution bugs: Encounter's 25% absent line must yield to MEDIUM's "never drawn absent"; FAMILY must resolve only where the block's basis is purpose | `tools/context.py` | Both cases have regression checks (a `--selftest` flag or a fixture run by the validator) that fail on the old code and pass on the new |
| T1.2 | Write the table test into `patterns/SPEC.md` as a section beside "A draw or an edge is decided by what the pick opens"; cut the `dangerous/Key.md` "two files" paragraph back to a pointer at the test; add one line to `CLAUDE.md`'s Pattern file rules pointing at it | `patterns/SPEC.md`, `CLAUDE.md` | The test reads as in `spec.md` section 6, with no examples beyond the two `SPEC.md` already uses; `CLAUDE.md` gains one line only |
| T1.3 | Produce the table inventory mechanically: a `tables.py inventory` command that walks every Spec line, applies the test's two conditions (opens lines = edge or nested sub-lines; not exactly one = rate under `1`, a condition, a count over 1, or a shared unit), and prints table / column group per unit per rating | `tools/tables.py` (new) | The output matches `spec.md` section 7, or the differences are resolved in `spec.md` (the test wins over the hand list) |
| T1.4 | Specify the record format (`spec.md` 8.1) as a parser, with round-trip writing, shared by every tool | `tools/site_common.py` (parse) and `tools/tables.py` (write) | Parse → write → parse is identity on fixture tables; today's gazetteer lines parse unchanged **[D5]** |

---

## Phase 2 - Steps and templates (framework text)

T2.1 lands last in this phase, in the same commit as T2.3-T2.8. Otherwise the validator
errors on steps that name templates which don't exist yet. Phases 2 and 3 merge together,
before any build is attempted, so `STEPS.md` never names a tool that isn't there.

| Task | What | Files | Done when |
|---|---|---|---|
| T2.1 | Rewrite phase 4 of `STEPS.md` per `spec.md` 8.2. Each step names its template and adds only what the template can't know (build order, gating, stub bookkeeping) **[D1, D6]** | `STEPS.md` | The validator's step regex parses every id; `--read-set 4f` resolves |
| T2.2 | Move every phase-4 step-id citation to its new id | `templates/*.md`, `templates/*.mmd`, `patterns/SPEC.md`, `patterns/dangerous/Key.md`, `patterns/dangerous/Lore.md`, `patterns/wild/Lore.md`, `README.md`, `tools/*.py` comments | `grep` for the old ids finds only intentional ones; the validator raises no "cites step X, which STEPS.md does not define" |
| T2.3 | `templates/Location_Gazetteer.md`: take weight out; rewrite Purpose to say the file is the location table whose first line is the stub; keep counts and tag rules | `templates/Location_Gazetteer.md` | No weight in its Template block; Purpose no longer calls it "not a place for content" |
| T2.4 | New `templates/Location_Weights.md`: DANGEROUS weight mix, WILD classification mix, SAFE prominence (one central per settlement, which is the template's to own, as `--set prominence` admits today); Context reads the Overview and the gazetteer | `templates/Location_Weights.md` | Validator-recognised as 4b's template; the weight mix moved here, not copied |
| T2.5 | New `templates/Allocation.md`: Purpose, the command, how to read the allocation report, when to reroll, and what is never hand-edited | `templates/Allocation.md` | Names `tools/tables.py allocate`; restates no rate |
| T2.6 | New `templates/Table_[Name].md`, one per table in `spec.md` section 7, each Purpose / Context / Instructions / Template. Context = 8.4's read set; Instructions = batching threshold, distinctness rules this table enforces across its rows, the rule that drawn values are never re-decided; Template = the record shape. Columns are **not** listed: they are read off the pattern **[D2]** | `templates/Table_*.md` | Each names exactly one pattern entry; `--read-set` reaches it; no Spec line is copied in |
| T2.7 | `templates/Location.md` becomes compile: Context runs `tables.py sheet [Code]`; Instructions gain "every row realized, nothing without a row, no fact added or dropped, record `Realized:`"; Template block and Citations unchanged **[D4]** | `templates/Location.md` | The output format is byte-for-byte the same shape; the `context.py 4c` reference is gone |
| T2.8 | The five registry templates: stub at 4d (allocation, by tool), full entry at 4h; Context at 4h reads the table rows that place the entry instead of the location files | `templates/Keys.md`, `Lore.md`, `Quests.md`, `NamedCreatures.md`, `UniqueTreasures.md` | Each one's 4c instruction is gone; the Template block is unchanged |
| T2.9 | Judgement checks: add "rows written in one pass read as a form" and "rooms read as one room" to the setting check; "draws realized" answered from the allocation report | `templates/Setting_Judgement_Check.md` | Two items added; nothing else rewritten |
| T2.10 | `README.md`: map `tables/` and `tools/tables.py`; add the commands | `README.md` | Points only, per `CLAUDE.md`; no description of how the pipeline works |

---

## Phase 3 - Allocation tool (A2 core)

| Task | What | Files | Done when |
|---|---|---|---|
| T3.1 | Extract `context.py`'s resolution walk (`resolve`, `resolve_file`, `resolve_line`) so it can emit units rather than a sheet; keep `context.py 4c` working on top of it until T6.4 | `tools/context.py`, `tools/tables.py` | The `4c` sheet for a fixture location is unchanged before and after |
| T3.2 | Apply the table test to the resolved units: each unit becomes a row in its table or a column group on its drawer's row; foreign keys to drawer and referents | `tools/tables.py` | A fixture DANGEROUS region allocates into `Locations`, `Exits`, `Encounters`, `Creatures`, `Hazards`, `Mysteries`, `Treasures` and `Secrets` with no orphan keys |
| T3.3 | Seed by row id for row-owned draws; one `Exits` row per diagram edge, its gate drawn once per edge (E3); WILD access as an `Exits` column group from the diagram's hidden/secret edges | `tools/tables.py`, `tools/draw.py` (seed helper only) | The fixture's gate count across edges sits near Door.md's rate; no edge has two gate draws |
| T3.4 | Registry stubs written at allocation: Keys naming both ends, Quests naming the target, Lore / Named Creature / Unique Treasure naming the placing row | `tools/tables.py` | Every registry foreign key in the tables has its stub; `check_key_obligations` passes at the close of 4d |
| T3.5 | Idempotent re-run and rerolls: `allocate` rewrites stubs only; `--reroll ROWID.KEY=N` refuses when it would orphan a filled row and prints the dependents (F12) | `tools/tables.py` | Re-running on an untouched region is a no-op diff; a refused reroll names its dependents |
| T3.6 | Allocation report: per table, rate asked against realized across the region; Creatures headcount against the Overview's Inhabitants (E2, E4) | `tools/tables.py` | Printed at the end of every `allocate`; tolerance read from the template, not hard-coded in two places |
| T3.7 | `tables.py sheet [Code] [Table]` (a table pass's read set, 8.4) and `tables.py sheet [Code]` (one location's rows, for compile) | `tools/tables.py` | Neither prints a location file, a sibling location's unreferenced rows, or registry content |
| T3.8 | `tables.py columns [pattern]`: a pattern's Spec lines as the column list a table owes, with the file's Constraints **[D2]** | `tools/tables.py` | Used by `sheet`; no template copies its output |

---

## Phase 4 - Milestone A2: allocation with the old writer

| Task | What | Done when |
|---|---|---|
| T4.1 | Validator: parse tables; errors and warnings for format, keys, the Exits/diagram match, and unfilled stubs (`spec.md` section 10, excluding `Realized:`) | Clean on the fixture; each rule has a failing fixture |
| T4.2 | `--pending` reports stubs owed per step, including connected stubs waiting on another region | Lists the fixture's cross-region exit as owed to 4h |
| T4.3 | A2 pilot: build steps 1-3 for `BRIEF.md`, then 4a-4d for one DANGEROUS cave, then write its locations with the **existing** 4c writer, fed by `tables.py sheet [Code]` over stubs | The cave's allocation report is in tolerance, its gates are per edge, its headcount reconciles; record findings in `setting/checks/` |

This is a checkpoint. If A2 alone fixes enough of E1-E8, the user can stop here. Phases
5-6 are the A3 half.

---

## Phase 5 - Fill passes and compile (A3)

| Task | What | Files | Done when |
|---|---|---|---|
| T5.1 | Substrate pass (4e) end to end: `Table_Locations.md` over a real region; fill `Locations.md` column groups | template from T2.6 | Every location row's substrate is filled; the purpose-per-block check passes |
| T5.2 | Feature passes (4f) in `spec.md` 8.3's order, one fresh context per table per region (per block above the template's threshold) | templates from T2.6 | Each table is filled; the distinctness warnings are clear or judged deliberate |
| T5.3 | Naming pass (4g) and `tables.py sync-names`: rewrites `.mmd` node labels and registry `found at` lines from `Locations.md` (F10) | `tools/tables.py` | After a rename, the validator's name-match checks pass with no hand edits |
| T5.4 | Connected fill (4h): remaining connected stubs, then the full registry entries from their placing rows | registry templates | `--pending` is empty for the region |
| T5.5 | Compile (4i) per location with the T2.7 template; `Realized:` written back to each row | `templates/Location.md` | Every row is realized exactly once; the validator's location checks pass unchanged |
| T5.6 | Validator: the `Realized:` checks, plus the heuristic "Feature with no row" warning | `tools/validate_setting.py` | Each has a failing fixture |
| T5.7 | `metrics.py`: per-table rows, fill state, asked against realized, words per cell; `context.py cost` gains the table strategy (F8) | `tools/metrics.py`, `tools/context.py` | Both print for the pilot regions |

---

## Phase 6 - Retire the old route

| Task | What | Done when |
|---|---|---|
| T6.1 | `site_common` / `build_site` / `build_pdf`: confirm `tables/` is ignored and nothing renders it (F13). No change is expected; fix only what breaks | Site and PDF build from the pilot unchanged in shape |
| T6.2 | Validator: drop any check made redundant by a table rule (for example, per-file repeated-feature heuristics that the table distinctness rules now cover exactly) | No check exists twice |
| T6.3 | Cut documentation that restated the old 4c route back to pointers (`CLAUDE.md` rule: never refresh a stale passage) | `grep` for "sheet", "4c", "sibling" in framework prose finds only current meaning |
| T6.4 | Remove `context.py 4c` once compile reads `tables.py sheet`; keep `cost` | `README.md` command list matches the tools |

---

## Phase 7 - Pilot and acceptance

| Task | What | Done when |
|---|---|---|
| T7.1 | Full pilot from `BRIEF.md`: the keep (SAFE), the borderland (WILD), and at least two caves (DANGEROUS, chosen so one cross-region connected stub exists), through 4a-4j | Every location file compiled |
| T7.2 | Run 5c on the pilot, comparing its "Rooms are distinct" and "Draws realized" findings with the second-run addendum at commit 9c1354b | Findings recorded under `setting/checks/` |
| T7.3 | Walk `spec.md` section 12's acceptance list item by item; open a follow-up for every item that fails, with its source (tool, template, pattern, generator) | All eight are met, or each miss has a named follow-up the user accepts |
| T7.4 | 5a and 5b: the template and pattern judgement checks over the new templates and the changed `SPEC.md` | No restatement of a pattern found in a `Table_*.md` template |

---

## Risks to watch during the work

- **A table template drifting into a pattern copy (F4).** T2.6 and T7.4 both check for it.
  The fastest symptom is a template listing columns.
- **Formulaic rows (F2).** If T5.2's tables read as a form, the remedy is more per-row
  draws in the pattern, never longer instructions in the template.
- **Compile adding facts (F7).** T5.5's realized-trace makes it visible. If it keeps
  happening, the cells are too thin, which is a pattern question and not a compile one.
- **Cost (F8).** If T5.7 shows the table strategy unaffordable, A2 (phase 4) remains a
  complete, shippable improvement.
