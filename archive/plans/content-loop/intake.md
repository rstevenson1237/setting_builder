# Intake - the content loop

## The request, verbatim

> Lets look through our judgement checks + what we've discussed in thread and friction
> points that have arrived. I want to stop step 4 at the creation of the stub tables and
> then introduce a step 5 which is a tight content layering loop: seed location and
> setting tables, regenerate location write ups for any locations that have changed,
> separate context judgement of the location write ups, then go back and place setting
> level table entries where they make sense (build your rumour table, place your quests,
> seed the keys you need for your locks) so that our design is less reliant on
> percentages that are never followed and more intentional, then write region briefs that
> give an over view now that the region is actually complete (what kind of creatures
> inhabit, what rumours point here etc). Metrics and validate_setting run iteratively +
> critical review content pass means we are constantly reviewing the produced content.

## How it is read

| Clause | Read as |
|---|---|
| "our judgement checks" | The three `templates/checks/` templates and the last checks run on a build: Greywatch's Setting, Pattern and Template checks and both addenda, at commit 9c1354b. |
| "what we've discussed in thread" | `plans/location-schema/spec.md`, still awaiting approval. |
| "friction points that have arrived" | The table-pipeline plan's findings E1-E9 and friction points F1-F23 (`archive/plans/table-pipeline/spec.md`), and what the region A pilot shows today: its Overview, tables, write-ups, and the validator and metrics output against them. |
| "stop step 4 at the creation of the stub tables" | Step 4 builds structure only: locations, the graph, and every table entry each location will hold, placed but unfilled. Every stub is written by the end of step 4; filling them is step 5's. |
| "a tight content layering loop" | Step 5 repeats seed → write → review → place until a pass changes nothing, and then writes the briefs. |
| "regenerate location write ups for any locations that have changed" | A write-up knows which entries it was written from. The tools list the write-ups whose entries have changed since, and only those are rewritten. |
| "separate context judgement" | A fresh context, which wrote none of the content, reviews each pass's write-ups against a new check template. |
| "place setting level table entries where they make sense" | Rumours, Quests, Keys and the setting's other claims are written against locations that already exist, not ahead of them. Their placement adds region entries (a Lock, a giver, a find) that feed the next pass. |
| "less reliant on percentages that are never followed" | Rates stop being rolled per room. They become region-level targets that placement is held to, checked by the tools. |
| "region briefs ... now that the region is actually complete" | The Region Overview is split. A seed, written at 3c, is what the tables are written from; the brief is written last, from what the region holds. |
| "Metrics and validate_setting run iteratively + critical review" | Every pass opens with both tools, and its review records what moved. |
| "introduce a step 5" | Explicit authorisation to renumber: the current step 5 (judgement checks) becomes step 6, under `README.md`'s rule. |

## Decisions, verbatim

> Largely I'm going to skip the location-schema work as I believe there is enough friction
> there to warrant building piece meal as needed rather than pulling in whole cloth.
>
> I think the "one of" assignments in our schema is about the most specific we want to
> get with percentages within the schema. Instead lets write brief.md as kdl embedded in
> markdown file that can pull in percentages as granular as wanted. By layering our
> content creation we can target areas that are underspecified and hit our percentages in
> a more intentional fashion
>
> Pipeline looks good.
>
> Suggestion is to use commit history to confirm when content is out of date cheaply - if
> modified time is older than the content file then we know to regenerate. Ideally our
> framework is robust enough that generation is somewhat deterministic at this point
> (regenerating a location that has not changed should read almost exactly the same)
>
> renumber - yes and we should run our "For each file we must implement the minimal
> possible set. [...]" check on this file as well. I still see a stubbed 1a which is
> unacceptable.
>
> percentages - see above about the brief, if there is a percentage that makes sense at
> the framework level please respond with your reasoning
> change tracking - is this different than my suggestion? compare and contrast
> pilot first - agreed, we need to continue writing the safe and wild definitions anyways
> quest and key placement - agreed on needing the checks, but I would stay away from
> placing keys and then inventing a lock. Instead create the lock and then place the keys
> where it makes sense as the next step
> damage and content mixes - see above about brief.md

### How they are read

| Decision | Read as |
|---|---|
| Skip location-schema | That plan moves to `archive/plans/`. What the loop needs from it (the quest pathway, the key/lock checks) is pulled in here, and SAFE and WILD are written piece by piece as the pilot reaches them. |
| One-of is the schema's limit | The schema's `rate` lines hold counts and ranges only, which say what a type is. Every percentage moves to `BRIEF.md`. |
| `BRIEF.md` as KDL in markdown | Prose requests stay prose; targets are fenced KDL the tools read, at any grain: setting-wide, per rating, per region, per member. |
| Commit history for staleness | Replaces the digest (spec, Change tracking). |
| Renumber, and the minimal-set check on `STEPS.md` | Every phase is renumbered contiguously, with no retired stubs, and `STEPS.md` is cut to the minimal set. |
| Lock first, then keys | Placement creates a lock where the design wants one; keys are placed only against a lock that already exists, in the next placement. |
