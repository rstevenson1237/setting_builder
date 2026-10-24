# Implementation - a template schema, and no template hard-coded in Python

Task plan for `spec.md` once approved. Commits cite tasks as `template-schema T1`. Each
phase ends with `python3 tools/validate_setting.py` clean of errors, both `--check` builds
passing, and `--read-set`, `--skeleton` for every step unchanged in what they list (the
oracle), and commits on its own.

| Task | Spec | What | Files |
|---|---|---|---|
| T0 | | Baseline: `metrics.py`, every step's `--read-set` and `--skeleton`, the site and PDF as built, kept for diffing | this folder |
| T1 | T1, D1, D5 | `kdl.py` takes `"""` multi-line strings; `Template_Schema.md` with the node definitions; `templates.py` reads its enums and nodes in place of `NODES`, `SHAPES`, `RUNS`, `SCOPES`, `LENGTH_UNITS`; `schema_graph.py` draws it | `tools/kdl.py`, `tools/templates.py`, `tools/schema_graph.py`, `templates/Template_Schema.md` |
| T2 | T2-T4 | `field` gains `from`, `out`, `items`, `note`; `from` resolves; `--read-set` reports per field; the length lint moves onto it; the validator errors on a `from` naming an unread file | `tools/templates.py`, `tools/validate_setting.py`, `tools/metrics.py` |
| T3 | M1 (setting) | 18 setting templates to `.kdl`, one commit, `--read-set`/`--skeleton` diffed; the markdown files removed in the same commit | `templates/setting/`, `STEPS.md`, `README.md` |
| T4 | M1, M2 (region) | 7 region templates to `.kdl`; `Tables` split by rating with `inherit` | `templates/region/` |
| T5 | T5 | `format` node; `Location`, `Procedures`, `Treasure`, `Factions`, `Setting` formats; `skeleton` draws from `format`; `check_location_file`, `check_procedures`, `check_treasure_tables`, `check_rumours` read their shape from it; `parse_location_file`, `parse_exits`, `LOC_HEADER_RE` retire | `tools/templates.py`, `tools/validate_setting.py`, `tools/site_common.py` |
| T6 | T6 | `cite` node; `render_inline`, `cite_attrs`, the validator's citation checks and `Location`'s Citations list read it | `tools/site_common.py`, `tools/validate_setting.py` |
| T7 | P1 | The view engine (`tools/views.py`): row grammar, `each`, `part`, `join`, `sort`, `lookup`. `entry_card`, `table_html`, `bestiary_prose` and the seven `_drawn` functions replaced by `view` nodes; `site`/`pdf` HTML diffed against T0 until equal | `tools/views.py`, `tools/site_common.py`, `templates/view/` |
| T8 | P2 | Document and Site layout as `view` nodes; `build_pdf.py` and `build_site.py` shrink to the engine and a target block; `PDF_CSS` to `tools/site_assets/pdf.css` | `tools/build_*.py`, `templates/view/` |
| T9 | P3 | The first presentation types (`readaloud`, `statline`, `index`, `quickref`, `runhead`), each its own commit, each seen in the PDF before the next | `Template_Schema.md`, `tools/views.py`, `templates/view/` |
| T10 | P4, T8 | `templates.html`; judgement checks as `check` templates; `parse_checklist_source` retires | `tools/build_site.py`, `templates/checks/` |
| T11 | M3 | `README.md` map, `CLAUDE.md` bullet, `metrics.py` counts the hard-coded shapes left (target: none but the named code views), `metrics-after.txt` | `README.md`, `CLAUDE.md`, this folder |

**Order and risk.** T1-T2 change no output. T3-T4 are the large mechanical change and the
one most worth a second pair of eyes: the oracle (`--read-set`, `--skeleton`) catches a
lost read, not a lost sentence of guidance, so each template's `guide` lines are diffed
against its old Instructions by hand. T7 is the largest single risk: the drawn sections and
the entry cards are the output people see, so its definition of done is byte-equal HTML
for every page before any change in appearance (T9) is allowed.
