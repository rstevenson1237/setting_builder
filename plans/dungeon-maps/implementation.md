# Implementation - dungeon maps

Task plan for `spec.md`. Commits cite tasks as `dungeon-maps T1`. Each task ends with
`python3 tools/validate_setting.py` clean of errors and both `--check` builds passing, and
commits on its own.

| Task | Spec | What | Files |
|---|---|---|---|
| T0 | | Baseline metrics | `metrics-before.txt` |
| T1 | S11 | `tools/dungeon.py` takes `block_map`, `plan_of`, `pack_region` and `check_packing`; no behaviour changes, every map file byte for byte the same | `tools/dungeon.py`, `tools/maps.py`, `tools/validate_setting.py` |
| T2 | S10 | Block maps built where used and ignored by git; sync and the stale-map check retired | `tools/maps.py`, `tools/dungeon.py`, `tools/site_common.py`, `tools/validate_setting.py`, `.gitignore`, workflows, `setting/region/*/*.json` |
| T3 | S1, S2 | Exits positions added by the builders, rejected in write-ups, direction words checked; every Exits line rewritten without its position; `pack` stops editing write-ups | `templates/region/Location.md`, `tools/site_common.py`, `tools/build_site.py`, `tools/build_pdf.py`, `tools/validate_setting.py`, `tools/dungeon.py`, `setting/region/*/*.md` |
| T4 | S3-S5 | Schema; positions from the block's centre; `pack` reads positions, strips ways, stamps `seed` and `router`, idempotent; checks; G's Dressing re-centred and its inner ways stripped; Connections template and STEPS 3e, 4a | `patterns/Dangerous_Schema.md`, `tools/dungeon.py`, `tools/pack.py`, `tools/route.py`, `tools/validate_setting.py`, `templates/region/Connections.md`, `STEPS.md`, `setting/region/G/` |
| T5 | S6, S7 | `pack` lines read and checked by `tables.Brief`; the packer's rates from them; footprints for every level; stairs pulled over stairs and checked | `BRIEF.md`, `tools/tables.py`, `tools/pack.py`, `tools/dungeon.py` |
| T6 | S8 | `hall` in `Room_Shape`; validator rule; drawn with its code alone; the narrow rooms of C-L made halls | `patterns/Common_Schema.md`, `tools/dungeon.py`, `tools/pack.py`, `setting/region/*/Dressing.md` |
| T7 | S9, S12 | Map judgement check and step 5d; checklists read from every check template; artgen note; README; `metrics-after.txt` | `templates/checks/Map_Judgement_Check.md`, `STEPS.md`, `tools/build_site.py`, `plans/sheet-maps/artgen-capabilities.md`, `README.md`, this folder |

## Risks

- **G moves.** T4 re-centres G's positions by a translation, which the router ignores, so its
  passages and walls stay as drawn. G is not repacked.
- **Footprints that cannot be met.** T5's footprints are checked against the fill bounds, and
  each is tried with `pack` on a scratch copy before it is written; a level that cannot meet
  the pyramid's sequence is reported, not forced.
- **Builds slow down.** T2 builds maps on demand; renders stay cached by content, and the map
  file is written only when it changes.
