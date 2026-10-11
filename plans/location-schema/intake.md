# Intake - the location schema, reviewed against the archive

## The request, verbatim

> Lets do an analysis of our archived work against the newer patterns - items from
> dangerous locations first that you recommend to pull in, then proceed with the
> recommended build outs of safe and wild so I can approve line by line

## How it is read

| Clause | Read as |
|---|---|
| "our archived work" | `archive/patterns/` (the location-level pattern files retired when `patterns/Schema.md` was built clean-room) and `archive/templates/`. `archive/plans/table-pipeline/` is the record of why they took the shape they did. |
| "the newer patterns" | `patterns/Schema.md`, `templates/dangerous/Tables.md`, and the worked region `setting/region/A/`. |
| "items from dangerous locations first that you recommend to pull in" | Every archived DANGEROUS Spec line is checked against the schema. A line is recommended only where the schema has no way to say it and the gap reaches a player (`STYLE.md`); everything else is listed as not pulled in, with the reason, so it can be overruled. |
| "the recommended build outs of safe and wild" | A full `Safe` and `Wild` folder for the schema: nodes, enums, files and rates, plus the template defaults and lint each needs. They reuse the DANGEROUS nodes wherever the archive's lines fit them. |
| "so I can approve line by line" | `spec.md` numbers every proposal with its own checkbox. Nothing in `patterns/`, `templates/`, `STEPS.md` or `tools/` changes until it is approved; `implementation.md` is written from the approved set. |
