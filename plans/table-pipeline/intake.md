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

## Follow-up, verbatim

> my thoughts are an additional consideration, iterative writing. The author can think of a
> coordinated puzzle feature, write in clues, triggers, objects and multiple pieces of
> interactive features throughout multiple rooms and then write the entire coordinated
> build in one pass, all validated and proven correct and this works even when
> retrofitting on locations that have already been written. It also works in the opposite
> direction, if I"m writing creatures into a region I want to know what creatures inhabit
> that region and which rooms have a weight that calls for a potential creature but I
> don't really need any further context, the line of "there is an orc here. Its name is x,
> it reacts y and wants z" can exist on its own. I would do the work completely without
> our existing tools first, then do an analysis and wire back up the random chance
> generator and the context collector if still called for.

### How the follow-up is read

| Clause | Read as |
|---|---|
| "a coordinated puzzle feature ... throughout multiple rooms ... in one pass" | A unit of work that writes rows into several tables across several rooms at once. Storage stays one file per feature type, but a writing pass is no longer tied to one table. The coordinating record is itself a table row (`spec.md` 8.7). |
| "all validated and proven correct" | A composition has checkable invariants: every part exists as a row, the chain can be solved from the region's entrance, no clue sits in the same room as its answer, and each part fits its room's class. They are checked by hand in the pilot and automated later if called for. |
| "works even when retrofitting on locations that have already been written" | Adding rows to a compiled room triggers a targeted recompile of that room, driven by each row's `Realized:` trace. Nothing else in the room is rewritten (`spec.md` 9.2). |
| "the opposite direction ... the line ... can exist on its own" | A row is a standalone fact about one thing at one code. A table pass reads only its own stubs plus the region-level roster it draws from: no room substrate, no other tables. Making the room hang together is compile's job. This replaces the first draft's answer to F1. |
| "which rooms have a weight that calls for a potential creature" | The stubs that allocation writes into each table, by hand from the class files, are exactly that list. |
| "completely without our existing tools first ... then wire back up ... if still called for" | The pilot runs with no `draw.py` and no `context.py`. The author makes every rated decision by hand, against the template's mix, and logs it. An analysis then decides which tools come back. The validator keeps running as it is, since it is a format lint and not a generator. |

## Decisions, verbatim

> decisions:
> d1 - yes
> d2 - content will largely resemble for former work, however its pathways will change.
> For example a creature pattern will specify row content that feeds into the template for
> creatures.md that holds the table assigning all creature locations throughout the region
> d3 - we already write setting/region/b/Locations.md, it would make sense to continue this
> d4 - cells should be tags (1-2 categorizing words) or gloss (up to 6 terse descriptive
> words)
> d5 - should look at the pipe tables if the strictness of format is needed (every entry
> must have the same columns) vs the generalness of the proposed format (one line per entry
> d6 - I would do the filling out of connected stubs as a separate pass similar to how we
> are now, if features are adding stubs that is easy to write a test and issue a warning so
> our to-do list is always clear
> d7 - I would skip the compositions table but I would consider adding as a field (or part
> of the layout field) within the region overview
> d8 - yes
>
> I think d5 is the most important as it decides if we have one hazards.md (with each line
> deciding if it includes the detail for a trap, environmental or residual or if we need a
> table for each (perhaps in the same file?)

### How the decisions are read

| Decision | Read as |
|---|---|
| D1 | Explicit authorisation, under `README.md`'s rule, to renumber phase 4. |
| D2 | A pattern file specifies one row. The table template (`templates/Creatures.md`) owns the table: which locations get a row, how many, in what mix. Pattern content stays close to today's; what changes is where it flows. |
| D3 | Tables sit in `setting/region/[Code]/` next to `Locations.md`, not in a subfolder. The validator's region-folder glob has to narrow to numbered files. |
| D4 | A cell holds a tag (1-2 words naming a category, usually a draw item) or a gloss (at most 6 terse words). Compile turns cells into sentences. A Spec line that can't be answered in a gloss is asking more than one thing, and splits. |
| D5 | Open; the user asks for the analysis. It becomes `spec.md` section 6, with a recommendation. |
| D6 | Connected stubs are filled in their own pass, as 4d is today. A stub is visible as unfilled cells, and the validator warns on each one, so the to-do list is always mechanical. |
| D7 | No `Compositions` table. A coordinated build is an entry in a new Region Overview field. Its parts are ordinary rows, and the entry names them. |
| D8 | Hand first, as planned. |

## Second follow-up, verbatim

> split templates into folders similar to patterns/.
>
> What is our recommendation for where to draw the lines on the tables (for example, 1
> table for hazards, 3 tables in 1 file for each type of hazard or 3 files total; extended
> out to all of the patterns, unacceptable complexity is a deal breaker)

### How it is read

| Clause | Read as |
|---|---|
| "split templates into folders similar to patterns/" | Decision D9. `templates/` gets `setting/`, `region/`, `safe/`, `wild/`, `dangerous/` and `checks/`. It is planned as the first framework task (`implementation.md` T1.1) rather than done now: phase 1 rewrites every phase-4 citation anyway, so moving templates in the same pass avoids updating every citation twice. |
| "where to draw the lines on the tables ... extended out to all of the patterns" | One placement rule for every line, pattern and table (`spec.md` section 7), with the hazards case answered explicitly (7.2) and the result counted per rating (7.5). |
| "unacceptable complexity is a deal breaker" | The rule caps files at five per region and adds no table the pattern library doesn't already imply. Its complexity is accounted for in 7.5, and the one lever left (folding kind files) is given a test (7.3). |

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

After the follow-up, `spec.md` and `implementation.md` were revised in place. The tool-built
allocation milestone became a hand-run pilot followed by an analysis. After the
decisions, both were revised again: D5's analysis is `spec.md` section 6.

Nothing in `STEPS.md`, `templates/`, `patterns/` or `tools/` changes under this intake.
That work is `implementation.md`'s, and it starts once the Decisions in `spec.md` are
settled.
