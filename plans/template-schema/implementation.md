# Implementation - a template schema, and no editable template hard-coded in Python

Task plan for `spec.md` once approved, run as one change in phases. Commits cite tasks as
`template-schema P1.2`. Each phase ends with these clean, and is committed on its own:
- `python3 tools/validate_setting.py`
- both `--check` builds
- `--read-set` and `--skeleton` for every step, unchanged against the baseline
- the site and PDF HTML byte-equal to the baseline (phases 1-4), but for `patterns.html` and
  `schema-explorer.js` where a phase adds to the Schema Reference

| Phase | Task | Spec | What | Files |
|---|---|---|---|---|
| 0 | 0.1 | | Baseline: `metrics.py`, every step's `--read-set` and `--skeleton`, the built site and PDF HTML, kept for diffing | this folder |
| 1 | 1.1 | T1 | `Template_Schema.md`; `templates.py` reads its enums and nodes in place of its tuples; `schema_graph.py` reads it | `templates/Template_Schema.md`, `tools/templates.py`, `tools/schema_graph.py` |
| | 1.2 | T2, T4 | `reads=` becomes `from=` in `templates.py` and every template fence; file and `BRIEF:` sources; `items=` | `tools/templates.py`, `templates/**` |
| 2 | 2.1 | T3, D1 | `enum Out`, value defaults, member overrides; `tables.py` reads `out`; `--skeleton` draws from it | `patterns/*.md`, `tools/tables.py`, `tools/templates.py` |
| 3 | 3.1 | F1 | `format` node; `Location`, `Procedures`, `Setting`, `Factions` formats; skeleton, validator and the shared header pattern read it; their `## Template` blocks are cut | `tools/templates.py`, `tools/validate_setting.py`, `tools/site_common.py`, `templates/**` |
| | 3.2 | F2, D2 | `cite=` on citable tables; `cite` nodes in `Location.md`; `CITE_LABELS` and `## Citations` retire; form-against-regex check | `patterns/Setting_Schema.md`, `templates/region/Location.md`, `tools/validate_setting.py` |
| | 3.3 | F3, F4 | Bestiary `flow=`; `check_top_level_files` from `writes` | `patterns/Setting_Schema.md`, `tools/site_common.py`, `tools/validate_setting.py`, `templates/setting/Bestiary.md` |
| 4 | 4.1 | U1 | Templates drawn in `patterns.html`, each entry with members, sources, outputs, format and Instructions | `tools/schema_graph.py`, site assets for the reference |
| | 4.2 | M1, M2 | Instructions pass: cut each rule now carried by a schema, format or `out`; `README.md` | `templates/**`, `README.md` |
| 5 | 5.n | §5 | Each approved presentation type, one commit each, seen in the PDF before the next | as each needs |

**Risk.** Phase 3.1 is the one change that reaches the renderers before phase 5. It is
small (one header pattern), but a location write-up the writer set down loosely must still
parse, so it is run against every existing location before commit. Phase 4.2 cuts
Instructions text, and the oracle can't see a lost rule there. Each template's cuts are
diffed by hand against the schema line or format that now carries the rule.
