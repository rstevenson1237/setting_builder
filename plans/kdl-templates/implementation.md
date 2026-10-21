# Implementation - KDL seeds, briefs built from the tables, and KDL templates

Task plan for `spec.md`, every proposal approved as amended. Commits cite tasks as
`kdl-templates T1`. Each phase ends with `python3 tools/validate_setting.py` clean of errors
and both `--check` builds passing, and commits on its own, except T1-T4, which land as one commit: the site reads the seed's
fields from the brief, so neither can change alone.

| Task | Spec | What | Files |
|---|---|---|---|
| T0 | | Baseline metrics | `metrics-before.txt` |
| T1 | S1, S2 | Seed nodes in `Region_Schema.md`; each rating's folder gains a `Seed` line whose counts (`Seed=1 Rung=2`) the validator checks; a Seed node opens with the region code; `Kind` read from the node; a DANGEROUS Block's size defaults to `Conditions`; 13 seeds written as `Seed.md`; the old prose seeds stay as `[Code].md` until T4 rewrites them; `templates/region/Region.md` writes `Seed.md` | `patterns/`, `tools/tables.py`, `tools/validate_setting.py`, `tools/maps.py`, `setting/region/*/Seed.md`, `templates/region/Region.md` |
| T2 | B4 | `Secret` gains `knows gloss opt` and `fact string opt`; every Secret node given its `knows`, and a `fact` where its node does not already say it | `patterns/*_Schema.md`, region tables |
| T3 | B1, B5 | Inhabitants, Services, Loot, Alarm, Leads and Secrets drawn from the tables on the region page and in the PDF; `--check` covers them | `tools/site_common.py`, `tools/build_site.py`, `tools/build_pdf.py` |
| T4 | B2, B3 | `Region_Schema.md`'s `brief` is `[Code].md`'s fields: the seed's as prose, then list fields whose `holds=` assigns each location to exactly one; `BRIEF.md` `words` lines cap each; staleness reads `Seed.md` and the tables; `Brief.md`, `n=` paragraphs and the Inhabitants/Layout/Services name checks retire; 13 `[Code].md` rewritten; `templates/region/Brief.md` and STEPS 3c and 5e | `patterns/Region_Schema.md`, `BRIEF.md`, `tools/`, `setting/region/`, `templates/region/Brief.md`, `STEPS.md` |
| T5 | T1-T5 | Every template's Context becomes a ```kdl fence (`template`, `read`, `field`); standing context implied; `--read-set` from the fence, with fields; `--skeleton STEP` from the schema; `## Template` blocks that restate a schema cut; `Tables.md` split into `step` nodes | `templates/`, `tools/validate_setting.py`, `tools/metrics.py` |
| T6 | | README map, `metrics-after.txt` | `README.md`, this folder |
