# Setting Builder

A plain-text framework for authoring OSR (Old-School Renaissance) adventure settings as
markdown (and a few `.mmd` mermaid diagrams). This file is the full orientation and
reference doc - read once per session (a SessionStart hook in `.claude/settings.json`
injects it automatically). `CLAUDE.md` stays short on purpose: it carries only the handful
of rules that need active re-checking on every single request, and points back here for
everything else.

## What this repository is

Not a software project in the usual sense - all "development" here is content generation
following the templates and workflow below. The one exception is `tools/validate_setting.py`,
a structural linter run in CI on every pull request; it exists to check generated content
against the templates, not to build or ship software, and nothing beyond it should be added
(no build step, no package manager, no test framework for the linter itself beyond running
it against the content).

## Root files

- `GENRE.md` - the top-level thematic spine (era, tone, magic level, structure), customized
  at STEPS.md step 1a, plus the fixed **What a line has to earn** section: the three tests
  every line at every level must pass. See "The three tests" in `CLAUDE.md` for the short
  version; those tests outrank every template.
- `STEPS.md` - the authoritative, sequential build log. Every artifact created follows a
  numbered step here (e.g. `4c`) naming its template and its context files. This is more
  current than any summary of it, including this one.
- `CLAUDE.md` - always loaded as system context; the short list of rules that need active
  re-checking on every request.

## Setting content (`setting/`)

Mirrors the template set, created in the order `STEPS.md` lays out:

- `Setting.md`, `History.md`, `Truths.md`, `Rumours.md`, `Bestiary.md`, `Factions.md` -
  setting-level artifacts (steps 2a-2f).
- `Treasure1.md` through `Treasure5.md` - Treasure Tables I-V (step 2g).
- `Procedures.md`, `Language.md` - the two living artifacts: seeded generic at steps 1b/1c,
  tailored to the setting at step 2h, and (Language.md only) appended to continuously
  afterward as proper nouns are coined.
- `Lore.md`, `Keys.md`, `Quests.md`, `NamedCreatures.md`, `UniqueTreasures.md` - the five
  registries. Stubbed empty at step 2h, given a stub row (name + location) per entry during
  location generation (step 4c), and written in full at step 4d.
- `region/Regions.md` + `region/Connections.mmd` - the Regional Gazetteer and the
  region-to-region connection graph (step 3a-3b).
- `region/[Code].md` - one Region Overview per region (step 3c).
- `region/[Code]/` - one folder per region, each holding that region's `Locations.md`
  gazetteer, `Connections.mmd`, and one `[LocationCode].md` per location (step 4a-4c).

## `templates/`

One template per artifact type, each structured as **Purpose / Context / Instructions /
Template**. Context always lists exactly which files to read before drafting (GENRE.md
first) - don't pull in more than a template's Context section names. `templates/Location.md`
is deliberately the narrowest: only GENRE.md, the parent region overview, and the location's
own gazetteer stub - other setting files are consulted only to look up a name already
referenced, never wholesale.

## `patterns/`

Pattern guidance, in **five folders** matching the five levels of generation: `setting/`,
`region/`, `safe/`, `wild/`, `dangerous/`. A generation step reads only the folder matching
what it is building.

- `patterns/setting/` is flat: one file per setting artifact, one per registry, and one
  each for the two living artifacts.
- `patterns/region/` is one file per rating (`Safe.md`, `Wild.md`, `Dangerous.md`), each
  directing that rating's Region Overview fields, location count, class mix, and connection
  topology. The three ratings need materially different overviews, hence splitting by
  rating rather than by tier.
- `patterns/safe/`, `wild/` and `dangerous/` each hold **three kinds of file, read in
  order**: a class file naming what this location *is* and carrying its inclusion spec;
  element files supplying what the spec's lines draw from; and three files read
  unconditionally at the end - `Dressing.md`, `Secrets.md`, `Naming.md`. The two middle
  tiers use different axes: `wild/` organizes its element files by **kind of place**,
  `dangerous/` by **kind of element** - in WILD the question is what sort of place this is,
  in DANGEROUS the place is a room and the question is what is in it.
- **Restatement across the three rating folders is deliberate.** A trap in SAFE is a
  swindle, in WILD a snare, in DANGEROUS a deadfall, and writing each separately is what
  forces the differentiation. The cost is drift, which `checks/PatternJudgementCheck.md`
  manages by treating two restatements that read the same as a *finding*.
- Every pattern file uses one skeleton: **Decides / Read at / Spec / Patterns /
  Constraints**. The Constraints section starts empty and fills only from observed
  generation failures, never from anticipation.

## `checks/`

Output of the judgement checks (STEPS.md step 5): `TemplateJudgementCheck.md`,
`PatternJudgementCheck.md`, `SettingJudgementCheck.md`. Non-mechanical review passes
`tools/validate_setting.py` can't do - they call for human or model judgment - following the
checklist format in `templates/Template_Judgement_Check.md`, `Pattern_Judgement_Check.md`,
and `Setting_Judgement_Check.md` respectively.

## Generation workflow

The build order is strict and each stage depends on the previous ones existing. See
`STEPS.md` for exact, current numbering.

1. **Framework** - `GENRE.md`, then seed `setting/Procedures.md` and `setting/Language.md`.
2. **Setting** - `setting/Setting.md` first, then History -> Truths -> Rumours -> Bestiary
   -> Factions -> Treasure I-V, then tailor Procedures and Language and stub the five
   registries.
3. **Region** - `region/Regions.md` (fixes region count, rating mix, and a die per region)
   -> `region/Connections.mmd` -> one Region Overview per region.
4. **Location** - per region: `Locations.md` gazetteer -> `Connections.mmd` -> one file per
   location -> then, once every region is done, a final pass writing the full content of
   every stubbed registry entry, and a cash-out pass settling every setting- and
   region-level claim against the rooms that deliver it.
5. **Judgement checks** - the three non-mechanical review passes.

### Three things this order buys

**Every location exists as a stub before any location file is written.** Step 4a creates
every region's gazetteer before 4b creates any graph and 4c writes any entry. That is what
lets a Quest giver or a Key at one location name a real target in a region whose files do
not exist yet.

**Container and data are separate.** A location file *cites*; the registries *hold*. A
location records only a stub row for a piece of Lore, a Key, a Quest, a Named Creature or a
Unique Treasure at 4c, and the content is written at 4d with every referencing location in
view. A location entry is therefore not a complete scene until 4d, by design.

**The chain has a return path.** Steps 1 through 4d push information downward - GENRE to
pattern to template to artifact - and a one-way chain cannot tell that a claim made at the
top was never built at the bottom. Step 4e runs upward and settles every claim against the
rooms that were supposed to deliver it: Truths fill their Handles or are cut, History events
fill their Left lines or are cut, and anything a Region Overview asserted is either present
in its locations or removed from the overview. **The default at 4e is deletion, not
defence.**

## Scaling and dice

Four numbers in this framework look alike and are not. `setting/Procedures.md` is the
authority; the short version:

- **Players** carry 1-6 dice of d4-d12, d6 average.
- **Creatures** carry d6 only, count 1-18, bonus -2 to +6, reading roughly as classic Hit
  Dice.
- **Factions** carry d6 only and **no bonus**, and their count is meaningful *only*
  relative to the other factions.
- **A region's die** is none of these. It is a **difficulty die** rolled 1 = failure, 2-3 =
  complication, 4+ = success - so a *smaller* die is *harder*. **d8 is baseline**; d6
  slightly tougher, d10 slightly easier, d4 and d12 deliberate outliers.

Creature AD is pitched against **party altitude** - what the characters can survive, per
`GENRE.md`'s lethality framing - never against the region die. See "The three tests" in
`CLAUDE.md` for why this is called out there too.

The location counts follow from the difficulty math rather than being conventions: a WILD
region at N locations expects **exactly one** encounter per full traverse at every die, and
a DANGEROUS region at 3N expects **exactly three** of the Danger track's six steps per full
clear. Deviating is a deliberate trade with a measurable cost.

## Location entry format (`templates/Location.md`)

The most detail-sensitive template, worth calling out directly:

- Header line: `[Region].[N] **Name** - *three, thematic, tags*`
- Player Summary (plain text, 2 sentences, **bold** any feature named in it)
- Referee Notes (*italicized*: shape, size, sounds/smells)
- One bolded line per **Feature**, labeled with the feature's own name - no leading article
  (`**Thorn Tangle:**`, not `**The Thorn Tangle:**`) - stating where within the room it sits
  and its own dimension when spatially significant, not just what it is
- **Exits:** comma-separated, mundane only, each as `[what indicates the exit, and where it
  sits in the room] -> [Code] [Location Name]` - position is what keeps two exits of the
  same type distinguishable, so never leave two reading identically. An exit that leaves
  the map entirely (open water, an unstaked wilderness edge) uses the same form with
  `-> [where it leads, in plain terms, with no Code]` and is always listed **last**.
- Any exit that needs a trigger to reveal or access is described inside a Feature line
  instead of listed under Exits - Exits is reserved for straightforward access.

## Regions and weights

Regions are rated SAFE, WILD, or DANGEROUS with a die size (d4-d12) and coded A, B, C...
(AA, AB... past 26). The die is a **difficulty die**, not a power level. It also sets
location count: SAFE and WILD hold roughly as many locations as the die type, DANGEROUS
roughly 3x it, one per room.

**DANGEROUS locations carry a weight** - low, medium, or high - selecting
`patterns/dangerous/Low.md`, `Medium.md`, or `High.md`. Weight is a **presentation**
distinction, not a content budget: a class is defined by what it *guarantees*, never by a
ceiling on what may appear. Low is the largest class and grows fastest with region size,
because connective space is where a region's decisions get made, not where its filler goes.
Each DANGEROUS location also carries a **node role** from its region's graph - empty, dead
end, branch, loop leg, or divide - assigned at 4b and read at 4c.

**WILD locations carry a classification instead** - landmark, hidden, or secret - selecting
`patterns/wild/Landmark.md`, `Hidden.md`, or `Secret.md`. Roughly half or more are landmark
(freely discoverable), at least a third hidden (reached through a parent landmark's
visible-but-easy-to-miss detail), and the remainder, usually under a fifth, secret (reached
through a Clue/Trigger/Payload, connected via a hidden `-.-` edge). WILD generates landmark
tier first, then hidden, then secret.

Every WILD landmark sits at the same baseline. **Depth is how a WILD region carries
weight** - a landmark that matters more gets *children*, not a heavier entry. SAFE works the
same way: emphasis arrives as additional locations rather than longer ones, and each
location's prominence (liner note, working, or central) is decided before anything is
written and is deliberately *not* derived from size.

A landmark must be nameable, revisitable, and connectable. Anything failing that test is
terrain, belonging in the Region Overview's Terrain field as connective texture the referee
narrates between points - this is a **point crawl**, and what lies between the points is
procedural.

## Units and time

Dimensions split on indoor vs. outdoor, not on region rating: enclosed spaces in feet,
outdoor locations in yards. A vertical drop or climb stays in feet either way. Distance
between two points follows the same split at larger scale: yards for a short hop, miles for
a long trek.

Time defaults by region rating, stated in each Region Overview's Layout field and defined in
`setting/Procedures.md`: WILD runs on 4 hours per action; SAFE isn't time-bound; DANGEROUS
runs on the Danger table's countdown instead of real time.

## Validation

`tools/validate_setting.py` is a structural linter (stdlib-only Python, no dependencies)
that checks generated content against the templates and this file's rules - not against
GENRE.md's genre/tone, which still needs human or model judgment. Runs automatically in CI
(`.github/workflows/validate.yml`) on every pull request and push to `main`; run locally
with `python3 tools/validate_setting.py`. It checks:

- **Template format**: region codes a plain A-Z progression; a region's Locations.md
  entries numbered 1..N with no gaps; DANGEROUS locations carry a low/medium/high weight,
  WILD locations a landmark/hidden/secret classification, SAFE ones neither; each location
  file's header matches its filename, region, and gazetteer stub; Player Summary/Referee
  Notes/Feature/Exits lines present and correctly formatted; Treasure Table and Rumours
  files have 20 numbered rows.
- **Connections**: every location in a region's `Locations.md` appears as a node in that
  region's `Connections.mmd` and vice versa; every mundane `Exits:` entry has a matching
  edge in some `Connections.mmd`; an Exit matching only a hidden (`-.-`) edge is a warning
  (confirm it's the far side of an already-triggered secret rather than a violation); two
  exits sharing an identical description but leading to different destinations are a
  warning to add distinguishing position.
- **Cross-references**: `Lore:`/`Keys:`/`Quest:`/`Named Creature:`/`Unique Treasure:`/
  `Treasure [I-V]` citations inside a location's Features are cross-checked against stub
  rows in the matching `setting/` registry, and vice versa. A Quest row naming fewer than
  two locations is warned, since a Quest is two-ended by definition.
- **Topology report**: not a check. Graph shape is a design decision, so the validator
  *reports* each region's shape - locations, edges, tree-or-loop-count, dead-end count, any
  isolated node - and leaves the judgement to `checks/SettingJudgementCheck.md`. SAFE wants
  a shallow hub, WILD a forest of trees, DANGEROUS a dense graph with loops and at least one
  divide.

**Posture: strict on format, relaxed on content and ratios.** It errors (fails CI) on
unambiguous breakage - unknown codes, name mismatches, missing files, orphaned nodes,
malformed lines, broken citations - and warns on things that need a human glance but might
be intentional. It deliberately does *not* check ratios, budgets, class mixes, or anything
about prose - those judgements belong in `checks/`. When adding a new artifact type or
template rule, extend this script alongside it.

`setting/Procedures.md` and `setting/Language.md` are seeded at steps 1b/1c before any
setting exists, so the validator treats a `setting/` holding only those as a fresh start.

## Web view and PDF

`setting/` also builds into a hyperlinked, mobile-friendly website and a single downloadable
PDF, both generated straight from the same markdown - there's no separate copy to keep in
sync.

- **Website**: `python3 tools/build_site.py --out _site` renders one static HTML page per
  document, region, and location, with a responsive nav (search box, mobile menu, a Regions
  dropdown), badges for region rating and location weight, and automatic cross-linking of
  every `A.1`-style location code, `(Lore: ...)`/`(Keys: ...)`/`(Named Creature: ...)`/
  `(Unique Treasure: ...)`/`(Treasure I-V, d20)` citation, and `Creature Name (Bestiary)`
  mention to the page it points to. Region and location `Connections.mmd` graphs render
  live as clickable Mermaid diagrams. Pure standard library - no npm, no build step beyond
  running the script. Preview locally with `python3 -m http.server -d _site`.
- **PDF**: `python3 tools/build_pdf.py` combines the same content into one print-formatted,
  internally hyperlinked PDF (automatic bookmarks/outline, a table of contents with page
  numbers, the same cross-reference links as the website) using
  [WeasyPrint](https://weasyprint.org/). Install it first with
  `pip install -r tools/requirements-pdf.txt`. Mermaid diagrams can't run inside a PDF, so
  each `Connections.mmd` is rendered there as a plain connection list instead.
- **Deployment**: `.github/workflows/pages.yml` builds both and deploys them to GitHub
  Pages on every push to `main` that touches `setting/` or the generator itself (or on
  manual dispatch). The PDF is published alongside the site and linked from its nav as
  "Download PDF". This requires a one-time repository setting: **Settings -> Pages ->
  Source: GitHub Actions**.
</content>
