# Intake - table-driven location generation

## The request, verbatim

> trying a new tactic for our location generation pipeline. combining our setting
> generation strategy of individual tables, each in their own file, progressively building
> the full structure of the setting along with the existing tables within the region. We
> will add addition 4x steps where the locations are given a weight, then connected
> together, then features are added in one file per feature type. For connected features a
> stub is created initially and then filled in similar to the current 4c/4d pattern. A
> final step will then write the content of all tables into the individual 1.md...
> location files using the already established pattern. Tables should be based on and
> supersede our currently existing patterns. we need a firm test for answering if the
> pattern should be a field in the table versus deserving its own its own table. This is a
> major change in our framework, write an intake.md with the users request, spec.md
> detailing the features of the plan and implementation.md with a task oriented
> implementation plan. Start with analysis and identification of alternates or friction
> points prior to writing the three files.

## How each clause is read

Where a clause could be read two ways, the reading taken is stated here. `spec.md` lists
the ones that need sign-off as Decisions.

| Clause | Read as |
|---|---|
| "individual tables, each in their own file" | The setting level already works this way: `Bestiary.md`, `Factions.md`, `Treasure1-5.md`, and the five registries each hold one kind of thing. Phase 4 adopts the same shape inside a region. |
| "progressively building the full structure ... along with the existing tables within the region" | The region already has two tables: `Locations.md` (the gazetteer) and the connection diagrams. New steps add tables next to them, and add columns to the tables that already exist. |
| "locations are given a weight" | Its own step, after the gazetteer, covering all three ratings: DANGEROUS weight, WILD classification, and SAFE prominence. SAFE prominence is currently decided per location at 4c. |
| "then connected together" | The current 4b diagrams, run after weighting. 4b already depends on weight (WILD children, the DANGEROUS LOW shape mix). |
| "features are added in one file per feature type" | One table file per feature type per region (hazards, treasures, exits, and so on), one row per instance, keyed to the location or locations it belongs to. |
| "for connected features a stub is created initially and then filled" | Anything whose content depends on another location gets a stub naming every location it joins, and is filled once those locations exist. This is the same two-phase shape the registries use now. |
| "a final step will then write the content of all tables into the individual 1.md ... files using the already established pattern" | A compile step per location, writing `templates/Location.md`'s existing output shape from that location's rows. |
| "tables should be based on and supersede our currently existing patterns" | Each table's rows are specified by the existing pattern files. Tables replace the per-location route (the class-file walk and the `context.py 4c` sheet) as the way content is generated. Whether the pattern files themselves are reshaped is Decision D2. |
| "a firm test for ... a field in the table versus its own table" | One decidable rule that can be applied to every Spec line in `patterns/`, stated in `patterns/SPEC.md`, with no case left to taste. |
| "start with analysis and identification of alternates or friction points" | `spec.md` opens with them, and the design that follows answers them. |

## State of the repository at intake

- `setting/` is empty: the Greywatch build was removed in commit bf4ea1c. There is no
  generated content to migrate. The change is to the framework only.
- The two most recent validation runs (commit 9c1354b, `setting/checks/SettingJudgementCheck.md`
  at that commit) are the evidence base for what the current per-location pipeline gets
  wrong. `spec.md` cites them by finding.

## Deliverables

- `intake.md` - this file.
- `spec.md` - analysis, alternatives, friction points, the table test, and the design.
- `implementation.md` - the task plan.

Nothing in `STEPS.md`, `templates/`, `patterns/` or `tools/` changes under this intake.
That work is `implementation.md`'s, and it starts once the Decisions in `spec.md` are
settled.
