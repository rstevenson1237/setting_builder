# Drakenhold

Working notes on the predecessor project, `rstevenson1237/drakenhold`, read at the source
rather than at its published site. Two directions, and the second is the one that matters:
what its corpus looks like measured against this framework's current artifacts, and - if
its content were harvested as inspiration for a clean rebuild here - where the friction
would actually be. Like `PLANS.md` this is running state, not authority; `STEPS.md` and
`patterns/SPEC.md` remain the authorities wherever this file disagrees with them.

The corpus audited is what Drakenhold publishes: its setting outline, `outlines/`,
`regions/`, `blocks/`, and the setting diagram. Its own `DESIGN_PATTERNS.md` and
`patterns/` are process documents there, excluded from its deliverable, and they are read
here anyway because they are the direct ancestor of `patterns/` in this repo and they are
the most useful thing in it.

## Part one: what fits

### The three tests hold

Drakenhold passes `GENRE.md`'s **What a line has to earn** more consistently than anything
this framework has generated. Three mechanisms are doing that work, and all three are
reproducible:

- **Every History event carries a `Trace:`** - this framework's `Left:` field under another
  name, and filled with a findable physical thing rather than left at `[pending 4d]`. *"The
  seam is visible - everything above the Main Level is finer, later work in a different
  stone, and the join runs clean around all three peaks."*
- **Its Truths are mechanisms, not propositions.** Tiles gate lateral movement and never
  vertical; rods gate action; the dark is hostile to light, so a torch below the Under
  Levels is a declaration. Each is a rule a party can plan against, which is what a Handle
  is for.
- **The genre position is stated as a refusal.** *"Vermakith is weather"*; *"Rumours of his
  deeper purpose should be seeded generously and are all wrong."* That is `give situations,
  not stories` written into the setting outline as policy, and the regions keep it.

### Structural correspondence

| Drakenhold | This framework |
|---|---|
| `Drakenhold_Setting_Outline.md` Overview | `setting/Setting.md` |
| `outlines/01`-`06` | `Truths` `Rumours` `History` `Factions` `Bestiary` `Treasure` |
| `regions/00_INDEX.md` | `setting/region/Regions.md` - rating and die, correct |
| `diagrams/T1`-`T4` | `Connections.mmd` and per-region `Connections.mmd`, and T3/T4 go below what this framework specifies |
| `## LOCATION STUBS` | `Locations.md` |
| per-region `## TABLES` | the mandated d6, correct type per rating in all 22 regions, DANGEROUS counting down from 6 |
| location entries | `templates/Location.md`'s Player Summary / Referee Notes / Features shape |

The rating vocabulary and the HIGH/MEDIUM/LOW weights are this framework's own, inherited.
The Feature decomposition rule - one bolded name, one thing per line, no connective prose -
was arrived at independently there and is confirmation rather than coincidence.

## Part two: what does not fit

Ordered by how much work the divergence represents, not by severity.

1. **Five rating-specific Region Overview fields are absent.** All 22 region files carry
   exactly `Overview, Ambiance, Layout, Features, Dangers, Creatures, Secrets, Treasure`.
   None carries **Architecture** (DANGEROUS), **People** or **Situation** (SAFE),
   **Terrain** or **Foraging** (WILD), or **Factions** - which `templates/Region.md`
   requires be answered even when the answer is none. The People and Situation content
   exists in `A Thornhaven`; it is dissolved into Overview and Creatures, where the referee
   will not look for it.

2. **Region Overview runs five-plus sentences against a three-sentence hard cap**, and
   fails the way the cap exists to prevent: Thornhaven's restates the die, the layout and
   the tags, then writes the referee's conclusion twice (*"Its job is resupply, rumour,
   downtime and the module's first lesson"*, *"which is the register the whole region plays
   in"*).

3. **No `Tags.md` at either level.** Every location carries three freely-authored tags
   (388 of 393 stubs, three each). This framework draws exactly two, from a 25-tag setting
   pool and a 25-tag region pool. Drakenhold's are better prose and worse structure: nothing
   binds the setting at the tag layer, and step 1b has no pool to compile against.

4. **No `Language.md`.** The root inventory lives as bullets inside `01_TRUTHS.md`. The
   roots are good and already generative - they gloss every region name - but as part of
   Truths they cannot receive coinage back at 4c/4d, which is the job the artifact exists
   for, and Truths is carrying content that is not a truth.

5. **The five registries do not exist.** No `Lore.md`, `Keys.md`, `Quests.md`,
   `NamedCreatures.md`, `UniqueTreasures.md`. `LORE_INDEX.md` is the nearest thing and
   declares itself *"an index and not a source"*. The container/data split is therefore
   inverted: Vermakith, the lance, the tiles and the rods are each described in several
   places instead of cited from one.

6. **No citation format.** `(Predatory, 5, Bestiary : Goblin)`, `(Treasure III, d20)`,
   `(Lore: Title)` appear zero times in the corpus. References are backticked plain names.
   Location codes would still link; nothing else would, and demeanor and number-appearing
   are simply absent.

7. **Locations live inside region files** rather than as `setting/region/A/1.md`, and every
   entry states its edges twice, once as `**Exits:**` and once as `**Connections:**` - a
   restatement at the same level.

8. **Weight is applied to SAFE locations** (`A.1` HIGH, `A.2` MEDIUM, `A.3` LOW), where
   this framework assigns weight to DANGEROUS only. The three WILD regions inside the
   mountain use no landmark/hidden/secret classification at all.

9. **Four outline fields have no home here.** `07_TRAPS` (a setting-level catalogue; this
   framework distributes traps to `dangerous/Trap.md` and `dangerous/Hazard.md` per
   location), `08_GRAFFITI` (a d20 setting-wide table; no analogue), `09_PROCEDURAL_TABLES`
   (extra colour tables beyond the one mandated d6 per region), and `10_STANDING_MYSTERIES`
   (what the module refuses to answer, scoped `[local]` or `[setting]`; no analogue - the
   nearest concept is `checks/SettingJudgementCheck.md`'s Room to Grow, and it is not the
   same act).

10. **`blocks/` has no analogue at all.** Five connective documents between setting and
    region, carrying room budgets, the tribute chain, cross-peak wake conditions and shared
    routes. This framework has setting, region, location and nothing between. For 22 regions
    where four stack vertically into one peak, that middle tier is load-bearing.

11. **Procedures are outsourced** to a read-only mirror of another project's design notes,
    where 1c seeds `setting/Procedures.md` and 2h tailors it. The traps outline's *"No trap
    here introduces a mechanic"* is the right instinct with no local file to cite.

## Resolved

Decisions. Rationale is in the commits that made them; actions are in `PLANS.md`.

**Blocks.** A generation batch, not a level of the setting hierarchy. Authored, not derived.
One block is one functional quarter, drawn from `dangerous/Dressing.md`'s Purpose families,
running roughly 16-65 locations. The unit of generation at 4c is the block.

**Topology stays mermaid.** One diagram per block, no internal format and no dependency.
Block membership is the file a node is declared in.

**The tier contract.** Locations connect only to locations. The location tier is the only
tier carrying connection type. Every group tier - setting, region group, region, location
group - asserts existence only, never type or quantity. A location belongs to exactly one
group. Before writing a location diagram, confirm whether it connects and match the
connection where it does.

**Cross-block edges** are declared in both files and held by a symmetry check over existence,
type and direction.

**Node role is deleted.** `dangerous/Low.md`'s three concealment rates are restated against
the location's own exits: one mundane exit and no concealed one is the honest dead end at
50%, one mundane exit plus a concealed route is 100% by construction, everything else 30%.

**Exits get their own pattern file**, `dangerous/Door.md`, with kinds open, one-way, secret
and vertical. DANGEROUS only; WILD and SAFE keep exits in their `Dressing.md` files.

**Two-ended elements resolve as obligations, not deferral.** The near end records a
`setting/Keys.md` stub row and `Unlocks` is written at 4d, per `templates/Keys.md`. The
demand-side percentages come off all three weight files, replaced by a rate-`1` draw of any
obligation recorded against the location. Obligations point forward only - same batch, or a
batch not yet generated. Zero unconsumed obligations at the close of 4c.

**Quest is unchanged.** It registers supply and lets givers be drafted from the registry, so
it names no far end and creates no obligation.

**Truths are `Mode: second pass`**, read at every location regardless of rating or weight,
and move into `templates/Location.md`'s consult list. Availability is not a quota: where a
location touches a Truth it is an instance of it, never a restatement.

**House rules go into `GENRE.md`'s fixed block**, as the rung below **What a line has to
earn**. The checkable subset additionally becomes validator rules or judgement-check items.

**Reinforcement is an authoring step.** STEPS.md 5c's upward read is promoted from
bookkeeping to authoring supporting detail into locations already written, as a new `5d`.

**Step ids grow by suffix and are never renumbered**, since every `## Read at` cites them.

**The no-repeated-purpose rule is step 5 judgement material**, scoped to the block and
raising a validator warning, never an error.

## Open, with a recommendation each

Each carries the strongest argument against the recommendation, so a later reader can
reopen it on evidence rather than on mood.

**1. Concrete format, and how block membership is stored. - CLOSED by Part eight.**
There is no internal format. Mermaid stays the source of truth, one file per block, and
membership is the file a node is declared in. `tomllib` being parse-only no longer matters.
*Detractor* withdrawn at Part nine - single membership is the rule, and the predecessor's
boundary nodes were drawn twice for emphasis rather than held in two groups. What remains is
that cross-block edges are now declared in two files and held together only by a symmetry
check, so that check is load-bearing rather than a nicety.

**2. Blocks authored or derived. - CLOSED by Part eight.**
Authored, structurally: a block is a file, so there is nothing to derive.
*Detractor* an authored block can still disagree with the graph, producing a quarter that
reads as a unit on the page and plays as scattered rooms. Cheap mitigation: warn when a
block file's own edges leave it disconnected.

**3. `networkx`, or no dependency.**
*Recommend* no dependency - **this reversed on Part seven and Part eight only strengthens
it.** The case for `networkx` was that the unenforced mix rules are graph queries, and the
hard ones were articulation points and cycle membership, both needed to derive node roles.
Roles are now deleted. What remains is arithmetic: dead ends are degree 1, branches degree 3
or more, the one-way rate is an edge-attribute count, independent loops are `E - V + C`, and
connectivity is a breadth-first walk. That is tens of lines, not a library.
*Detractor* if per-node topological facts are ever wanted again - which nodes sit on a loop,
which are articulation points - a worse `networkx` gets rebuilt by hand. The escape is cheap
though: the data is JSON either way, so adopting the library later is a read, not a
migration.

**4. Whether obligations may cross regions.**
*Recommend* yes, with no rule beyond the forward-only one already decided. Regions generate
in order, so "forward" is well defined across them, and cross-region obligations are the ones
worth having - a key found in the first region opening something in the fourth is the whole
point of a two-ended element.
*Detractor* these have the longest lifetimes and so are the most likely to strand if
generation order changes or a region is regenerated, and an obligation held across five
regions freezes a design decision for a long time - the far location's lock is dictated by a
choice made long before anyone knew what that location would be. The zero-unconsumed
invariant catches stranding; nothing catches staleness, so report obligation distance as a
diagnostic.

**5. `Door.md` for WILD and SAFE.**
*Recommend* not yet - DANGEROUS only. WILD carries concealed access in its location
*classification* rather than on its edges, SAFE's gate is social rather than physical, and
three files for one concept triples the surface with no current consumer.
*Detractor* deliberate restatement across ratings is this library's convention, to the point
that step 5b **inverts** the duplication check for `patterns/` - so a single-rating file is
the anomaly here, not the norm, and a reader finding exits inline in `wild/Dressing.md` and
as a whole file in DANGEROUS has found exactly the asymmetry that invites drift.

**6. Whether LOW NODE ROLE MIX survives.**
*Recommend* restate it as a graph-shape rule joined to stub weight. The content is still
wanted - a region whose every LOW location is a corridor is a boring region - but it has to be
expressed as dead-end, branch, one-way and loop rates rather than as role labels.
*Detractor* the rule says something the graph-wide rates do not, and
`patterns/region/Dangerous.md` says so in as many words: a region where every non-baseline
shape landed on HIGH or MEDIUM while every LOW defaulted to a corridor *"has technically
satisfied the graph-wide counts above while failing this rule."* So the restatement cannot be
purely about the graph - it has to cross-reference stub weight, which makes it a two-source
check rather than the clean single-source one the deletion was meant to buy.

**7. Step numbering, which blocks all of the above.**
Batching at 4c, promoting 5c to authoring, and adding `Door.md` all touch STEPS.md - and
`CLAUDE.md` warns that `## Read at` names step ids and a renumber "silently stales every one
of them," with the validator checking those ids against STEPS.md.
*Recommend* grow by suffix and never renumber: reinforcement becomes `5d`, batching is a
property of `4c` rather than a new step. Every existing `## Read at` line survives untouched.
*Detractor* suffix-only growth makes the numbering progressively less useful as a reading
order, and the renumber only gets more expensive the longer it waits. The validator already
parses every step id, so a scripted rewrite is not the frightening part - deciding the new
order is.

**8. A `CLAUDE.md` line pointing at the house rules.**
*Recommend* add it - one line naming the `GENRE.md` block as the rung below the three tests.
That file's entire remit is what must be re-checked every request, and this is the cheapest
lever against the dilution problem.
*Detractor* `CLAUDE.md` is short by explicit design and every line added dilutes the rest,
which is the same failure one level up. And if a rule needs a pointer in the
always-loaded file to get applied, that is evidence it is not checkable - in which case the
effort belongs in making it checkable, not in pointing harder at it.

**9. Standing Mysteries as an artifact.**
*Recommend* add it at setting level, scoped `[local]` and `[setting]`. It expresses something
this framework currently cannot say at all: that a question is deliberately unanswered rather
than merely unwritten.
*Detractor* the pressure that motivated it is largely gone now that obligations give a hard
zero-dangling invariant, and a new artifact costs a template, a pattern file, a step id, a
validator rule and a place in the build - a lot of machinery for something that may hold four
lines. A section inside `setting/Truths.md` would carry it at a fraction of the cost.
