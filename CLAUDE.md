# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is not a software project in the usual sense — it is a plain-text framework for authoring OSR (Old-School Renaissance) adventure settings as markdown (and a few `.mmd` mermaid diagrams). All "development" here is content generation following the templates and workflow below. The one exception is `tools/validate_setting.py` (see "Validation" below), a structural linter run in CI on every pull request — it exists to check generated content against the templates, not to build or ship software, and nothing beyond it should be added (no build step, no package manager, no test framework for the linter itself beyond running it against the content).

## Directory structure

- `GENRE.md` — the top-level thematic spine (1981 B/X D&D, Conan-esque, Low Magic, Points of Light, Mythic Underworld, situations not authored plots), plus **What a line has to earn**: the three tests — every word is translated, setting that is not actionable cannot be played, never make the player's decision for them — that every line at every level must pass. **Those three outrank the templates**: a line that fails them is cut even where a template asks for it, and a template that keeps producing such lines is the wrong template. Every template's Context section names this file explicitly and states what to check against it — re-read it at every generation step, don't just skim it once. Two failure modes to watch: genre drift (an authored plot creeping in, magic becoming common, an implied central authority), and inert prose (mood in place of a handle, a fact restated downward from the level where it was already true).
- `templates/` — one template per artifact type. Each is structured as **Purpose / Context / Instructions / Template**. Context always lists exactly which files to read before drafting (GENRE.md first) — do not pull in more than a template's Context section names. `templates/Location.md` is deliberately the narrowest: only GENRE.md, the parent region overview, and the location's own gazetteer stub — other setting files are consulted only to look up a name already referenced, never wholesale.
- `patterns/` — pattern guidance, in **five folders** matching the five levels of generation: `setting/`, `region/`, `safe/`, `wild/`, `dangerous/`. A generation step reads only the folder matching what it is building.
  - `patterns/setting/` is flat: one file per setting artifact (`Outline.md`, `Setting.md`, `History.md`, `Truths.md`, `Rumours.md`, `Bestiary.md`, `Factions.md`, `Treasure.md`), one per registry (`Lore.md`, `Keys.md`, `Quests.md`, `NamedCreatures.md`, `UniqueTreasures.md`), and one each for the two living artifacts (`Language.md`, `Procedures.md`).
  - `patterns/region/` is one file per rating — `Safe.md`, `Wild.md`, `Dangerous.md` — each directing that rating's Region Overview fields, location count, class mix, and connection topology. The three ratings need materially different overviews, which is why this splits by rating rather than by tier.
  - `patterns/safe/`, `wild/` and `dangerous/` each hold **three kinds of file, read in order**: a class file naming what this location *is* (`Settlement.md`; `Landmark.md`/`Hidden.md`/`Secret.md`; `High.md`/`Medium.md`/`Low.md`) and carrying its inclusion spec; element files supplying what the spec's lines draw from (`Trap.md`, `Creature.md`, `Treasure.md`, `Mystery.md`, `Faction.md`, `Quest.md`, `Key.md`, `Lore.md`, plus SAFE's `Commerce.md`/`Authority.md`/`Social.md`/`Situation.md`/`People.md` and WILD's `Ruin.md`/`Lair.md`/`NaturalFeature.md`); and three files read unconditionally at the end — `Dressing.md`, `Secrets.md`, `Naming.md`.
  - **Restatement across the three rating folders is deliberate.** A trap in SAFE is a swindle, in WILD a snare, in DANGEROUS a deadfall, and writing each separately is what forces the differentiation. The cost is drift, which `checks/PatternJudgementCheck.md` manages by treating two restatements that read the same as a *finding*.
  - Note the two middle tiers use different axes: `wild/` organizes its element files by **kind of place**, `dangerous/` by **kind of element**. That follows what actually varies — in WILD the question is what sort of place this is, in DANGEROUS the place is a room and the question is what is in it.
  - Every pattern file uses one skeleton: **Decides / Read at / Spec / Patterns / Constraints**. The Constraints section starts empty and fills only from observed generation failures, never from anticipation.
- `setting/` — the actual generated content for the current setting, mirroring the template set: `Setting.md`, `History.md`, `Truths.md`, `Rumours.md`, `Bestiary.md`, `Factions.md`, `Treasure1.md` through `Treasure5.md` (Treasure Tables I-V), `Lore.md`, `Keys.md`, `NamedCreatures.md`, `UniqueTreasures.md` (stubbed empty at step 2i, filled in two phases across steps 4c and 4d — see `STEPS.md`), then `region/Regions.md` + `region/Connections.mmd`, then one `region/[Code].md` Region Overview per region, then one `region/[Code]/` folder per region holding that region's `Locations.md` gazetteer, `Connections.mmd`, and one `[LocationCode].md` per location.
- `STEPS.md` — the authoritative, sequential build log. Every artifact created follows a numbered step here (e.g. `4c`) naming its template and its context files. When adding a new step to the workflow, append/renumber here and keep the wording consistent with existing entries (what's created, what context it uses, which template it follows).
- `checks/` — output of the judgement checks (step 5): `TemplateJudgementCheck.md`, `PatternJudgementCheck.md`, `SettingJudgementCheck.md`. These are non-mechanical review passes `tools/validate_setting.py` can't do — they call for human or model judgment the same way GENRE.md's tone does — following the checklist format in `templates/Template_Judgement_Check.md`, `templates/Pattern_Judgement_Check.md`, and `templates/Setting_Judgement_Check.md` respectively.

## Generation workflow

The build order is strict and each stage depends on the previous ones existing. See
`STEPS.md` for exact, current numbering — it is more current than this summary.

1. **Framework** — `GENRE.md`, then seed `setting/Procedures.md` and `setting/Language.md`.
2. **Setting** — `setting/Outline.md` first, since it fixes region count, rating mix, dice and party altitude, and everything downstream scales against it. Then Setting → History → Truths → Rumours → Bestiary → Factions → Treasure I-V, then tailor Procedures and Language and stub the five registries.
3. **Region** — `region/Regions.md` → `region/Connections.mmd` → one Region Overview per region.
4. **Location** — per region: `Locations.md` gazetteer → `Connections.mmd` → one file per location → then, once every region is done, a final pass writing the full content of every stubbed registry entry, and a cash-out pass settling every setting- and region-level claim against the rooms that deliver it.
5. **Judgement checks** — the three non-mechanical review passes.

### Three things this order buys

**Every location exists as a stub before any location file is written.** Step 4a creates
every region's gazetteer before 4b creates any graph and 4c writes any entry. That is what
lets a Quest giver or a Key at one location name a real target in a region whose files do
not exist yet.

**Container and data are separate.** A location file *cites*; the registries *hold*. A
location records only a stub row for a piece of Lore, a Key, a Quest, a Named Creature or a
Unique Treasure at 4c, and the content is written at 4d with every referencing location in
view. A location entry is therefore not a complete scene until 4d, by design.

**The chain has a return path.** Steps 1 through 4d push information downward — GENRE to
pattern to template to artifact — and a one-way chain cannot tell that a claim made at the
top was never built at the bottom. Step 4e runs upward and settles every claim against the
rooms that were supposed to deliver it: Truths fill their Handles or are cut, History events
fill their Left lines or are cut, and anything a Region Overview asserted is either present
in its locations or removed from the overview. **The default at 4e is deletion, not
defence.** Without it the upper levels drift into mood, because nothing above the location
was ever obliged to be actionable — which is the failure mode this framework is least able
to see in itself.

## Scaling and dice

Four numbers in this framework look alike and are not. `setting/Procedures.md` is the
authority; the short version:

- **Players** carry 1-6 dice of d4-d12, d6 average.
- **Creatures** carry d6 only, count 1-18, bonus -2 to +6, reading roughly as classic Hit Dice.
- **Factions** carry d6 only and **no bonus**, and their count is meaningful *only* relative to the other factions.
- **A region's die** is none of these. It is a **difficulty die** rolled 1 = failure, 2-3 = complication, 4+ = success — so a *smaller* die is *harder*. **d8 is baseline**; d6 slightly tougher, d10 slightly easier, d4 and d12 deliberate outliers.

Creature AD is pitched against **party altitude**, never against the region die.

The location counts follow from the difficulty math rather than being conventions: a WILD
region at N locations expects **exactly one** encounter per full traverse at every die, and
a DANGEROUS region at 3N expects **exactly three** of the Danger track's six steps per full
clear. Deviating is a deliberate trade with a measurable cost.

## Location entry format (`templates/Location.md`)

This is the most detail-sensitive template, worth calling out directly:

- Header line: `[Region].[N] **Name** - *three, thematic, tags*`
- Player Summary (plain text, 2 sentences, **bold** any feature named in it)
- Referee Notes (*italicized*: shape, size, sounds/smells)
- One bolded line per **Feature**, labeled with the feature's own name — no leading article (`**Thorn Tangle:**`, not `**The Thorn Tangle:**`) — stating where within the room it sits (a wall, a corner, the center) and its own dimension when spatially significant, not just what it is
- **Exits:** comma-separated, mundane only, each as `[what indicates the exit, and where it sits in the room] -> [Code] [Location Name]` (e.g. `door, set into the east wall -> A.2 Salvage Market`) — position is what keeps two exits of the same type distinguishable, so never leave two reading identically
- Any exit that needs a trigger to reveal or access (a secret door, a puzzle) is described inside a Feature line instead of listed under Exits — Exits is reserved for straightforward access.

## Regions and weights

Regions are rated SAFE, WILD, or DANGEROUS with a die size (d4–d12) and coded A, B, C…
(AA, AB… past 26). The die is a **difficulty die**, not a power level — see "Scaling and
dice" above. It also sets location count: SAFE and WILD hold roughly as many locations as
the die type, DANGEROUS roughly 3× it, one per room.

**DANGEROUS locations carry a weight** — low, medium, or high — selecting
`patterns/dangerous/Low.md`, `Medium.md`, or `High.md`. Weight is a **presentation**
distinction, not a content budget: a class is defined by what it *guarantees*, never by a
ceiling on what may appear. A low-weight room may hide a secret door; what makes it low is
that it *looks* empty, and that is precisely what makes searching a real decision. Low is
the largest class and grows fastest with region size, because unlike the corpus this
framework draws from, we key the connective space rather than drawing it as corridors on a
map — and connective space is where a region's decisions get made, not where its filler
goes. Each DANGEROUS location also carries a **node role** from its region's graph — empty,
dead end, branch, loop leg, or divide — assigned at 4b and read at 4c.

**WILD locations carry a classification instead** — landmark, hidden, or secret — selecting
`patterns/wild/Landmark.md`, `Hidden.md`, or `Secret.md`. Roughly half or more are landmark
(freely discoverable by roaming the region), at least a third hidden (reached only through
a specific parent landmark's visible-but-easy-to-miss detail — a mundane Exit, no trigger),
and the remainder, usually under a fifth, secret (reached only through a Clue/Trigger/
Payload at the parent, connected via a hidden `-.-` edge). Because hidden and secret
locations are defined relative to a parent, WILD generates landmark tier first, then hidden,
then secret.

Every WILD landmark sits at the same baseline. **Depth is how a WILD region carries
weight** — a landmark that matters more gets *children*, not a heavier entry. The same is
true of SAFE, where emphasis arrives as additional locations rather than longer ones, and
where each location's prominence (liner note, working, or central) is decided before
anything is written and is deliberately *not* derived from size.

A landmark must be nameable, revisitable, and connectable. Anything failing that test is
terrain, and belongs in the Region Overview's Terrain field as the connective texture the
referee narrates between points — this is a **point crawl**, and what lies between the
points is procedural.

## Units and time

Dimensions split on indoor vs. outdoor, not on region rating: enclosed spaces are measured
in feet, outdoor locations in yards. A vertical drop or climb stays in feet either way —
it's a mechanical measurement, not an areal footprint. Distance between two points follows
the same split at larger scale: yards for a short hop, miles for a long trek. These rules
live in `templates/Location.md`; they are format, not pattern, and are stated once.

Time defaults by region rating, stated in each Region Overview's Layout field and defined
in `setting/Procedures.md`: WILD runs on 4 hours per action; SAFE isn't time-bound;
DANGEROUS runs on the Danger table's countdown instead of real time.

## Validation

`tools/validate_setting.py` is a structural linter (stdlib-only Python, no dependencies) that checks generated content against the templates and this file's rules — not against GENRE.md's genre/tone, which still needs human or model judgment. It runs automatically in CI (`.github/workflows/validate.yml`) on every pull request and push to `main`, and can be run locally with `python3 tools/validate_setting.py`. It checks:

- **Template format**: region codes are a plain A-Z progression; a region's Locations.md entries are numbered 1..N with no gaps; DANGEROUS locations carry a low/medium/high weight, WILD locations carry a landmark/hidden/secret classification, and SAFE ones carry neither; each location file's header matches its filename, region, and gazetteer stub; Player Summary/Referee Notes/Feature/Exits lines are present and correctly formatted (Referee Notes in single-asterisk italics, Feature labels without a leading article); Treasure Table and Rumours files have 20 numbered rows.
- **Connections**: every location in a region's `Locations.md` appears as a node in that region's `Connections.mmd` and vice versa; every mundane `Exits:` entry has a matching edge in some `Connections.mmd`; an Exit that matches only a hidden (`-.-`) edge is flagged as a warning to confirm it's the far side of an already-triggered secret (or a WILD Secret-tier location's connection) rather than a template violation (the exit-vs-Feature rule in `templates/Location.md` is otherwise enforced as an error when there's no edge at all); two exits in the same location sharing an identical description but leading to different destinations are flagged as a warning to add distinguishing position.
- **Cross-references**: `Lore:`/`Keys:`/`Quest:`/`Named Creature:`/`Unique Treasure:`/`Treasure [I-V]` citations inside a location's Features are cross-checked against stub rows in the matching `setting/` registry, and vice versa. A Quest row naming fewer than two locations is warned, since a Quest is two-ended by definition.
- **Topology report**: not a check. Per the posture below, graph shape is a design decision rather than a rule, so the validator *reports* each region's shape — locations, edges, whether it is a tree or how many independent loops it carries, dead-end count, and any isolated node — and leaves the judgement to `checks/SettingJudgementCheck.md`. SAFE wants a shallow hub, WILD a forest of trees, DANGEROUS a dense graph with loops and at least one divide.

**Posture: strict on format, relaxed on content and ratios.** It errors (fails CI) on
unambiguous breakage — unknown codes, name mismatches, missing files, orphaned nodes,
malformed lines, broken citations — and warns on things that need a human glance but might
be intentional. It deliberately does *not* check ratios, budgets, class mixes, or anything
about prose: weight is a presentation distinction rather than a content budget, so a
low-weight location may legitimately hold four things and counting features would be wrong
in principle, not merely strict. Those judgements belong in `checks/`. When adding a new
artifact type or template rule, extend this script alongside it.

`setting/Procedures.md` and `setting/Language.md` are seeded at steps 1b/1c before any
setting exists, so the validator treats a `setting/` holding only those as a fresh start.
