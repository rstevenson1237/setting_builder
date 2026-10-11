# Spec - table-driven location generation

The request, its follow-up and the user's decisions are in `intake.md`. This file records
the analysis (sections 1-3) and the decisions (section 5). It then settles the two
structural questions (the table format, section 6, and where the lines between columns,
tables and files fall, section 7) before the pipeline itself.

Three ideas run through the whole design:

- **Patterns specify rows; templates own tables** (D2). A pattern file says what one row
  holds. A table template says which locations get rows, how many and in what mix, and it
  holds the region's table.
- **Storage and passes are separate.** Files are storage. A pass is a unit of work: one
  family of tables (every creature in a region), or one coordinated build across rooms.
- **Hand first, tools after** (D8). The pilot runs without `draw.py` or `context.py`. The
  validator stays, because it is the lint.

---

## 1. Analysis - the pipeline today

Phase 4 today: 4a gazetteer, 4b diagrams, 4c one location at a time from
`context.py 4c`'s sheet, and 4d registry entries. The doctrine is "write each location from
those alone, never from its sibling rooms".

What the last two validation runs found (commit 9c1354b):

| # | Finding | Why the current shape produces it |
|---|---|---|
| E1 | Near-repeats no single writer can see (one hazard shape six times, then three; alarm cords seven times) | Each location is written blind to its siblings |
| E2 | Rates not realized at region scale (no second name in 30 rooms against 20%; 94% open edges against 60%) | Rates settle per location; nothing reads the region total |
| E3 | Gates on 43% of exit-ends; 7 warded doors in 22 rooms | Each end of an edge draws its own gate |
| E4 | A household of "about ten" appears as one creature | Nothing sums creatures against the Overview's Inhabitants |
| E5 | MEDIUM "never absent" overridden; household blocks drawing a FAMILY | `context.py` bugs, invisible because no sheet meets another |
| E6 | Key, Lore and Quest obligations tracked by hand | Connected content is discovered while writing |
| E7 | A 173-word Feature; rooms tripling in length | Raw material and decisions handed over together |
| E8 | Two blocks differing in dressing, not skeleton | Block-level distinctness has nowhere to be checked |
| E9 | No multi-room puzzle anywhere | A location-at-a-time writer cannot place the far half of anything |

Every finding except E5 and E7 is about many rows or many rooms at once.

---

## 2. Alternatives (settled)

A1 (status quo plus checks), A2 (allocation tables only), A3 (the full table pipeline) and
A4 (tables as the product) were weighed in the first draft. **A3, run by hand first**, is
the route. A2 remains the fallback if the analysis finds the fill passes not worth their
cost.

---

## 3. Friction points

**F1 - Room coherence with standalone rows.** Compile reads all of a room's rows and makes
them one room, adding and dropping nothing; a row that won't fit goes back to its pass. The
pilot measures how often that happens.

**F2 - The sibling doctrine is reversed.** Compile still writes each room from its own rows
only. Inside a table pass, seeing every sibling is how E1 and E8 are prevented: every clue
in the region sits in one column. 5c gains an item for passes that read as a form.

**F3 - Renumbering.** Resolved by D1.

**F4 - Single authority.** Resolved by D2: the template never lists columns, because the
pattern's Spec lines are the columns (7.1).

**F5 - Weight is a value.** It is a column of `Locations.md` § Location, created empty at
4a and filled at 4b.

**F6 - Region tables against setting registries.** The setting registries stay the table
for anything with an identity beyond one placement. Region rows hold placements and an id
column naming the registry entry.

**F7 - Compile writes facts twice.** Resolved by D4: cells are tags and glosses, never
prose.

**F8 - Cost.** The pilot log records every pass's read set and size.

**F9 - Cross-references.** References are id columns. A pass reads the rows its rows name.

**F10 - Naming last, names used early.** Tables key by code. The naming pass updates
`Locations.md`, then the name sync updates diagram labels and registry lines.

**F11 - Tool bugs at scale.** Deferred with the tools. E5 is fixed before `context.py`'s
walk is reused.

**F12 - Changes ripple.** A pass that changes a filled row re-reads every row naming it.

**F13 - Tables in the region folder** (D3). The validator errors on any non-numbered `.md`
in a region folder. Its glob narrows to `[0-9]*.md` in phase 1.

**F14 - WILD access.** WILD access lines are values of the Hidden and Secret class files,
so they are columns of their class tables (7.1). The Landmark → Hidden → Secret write
order falls away, because every table exists as stubs from allocation.

**F15 - Existing files change format** (D10). The validator and `site_common` parse ten
files with bespoke regexes today. Both move to the two generic parsers in phase 1. This
is a lint and site change, not a generator rewire, and `setting/` is empty, so no content
converts.

**F16 - Coordinated builds against "never two triggers deep".** The rule stays per room.
Each link's clue is obvious in its own room, or one trigger from obvious there. What
carries the chain between rooms is something the party holds or knows (E9).

**F17 - Coordinated builds against room classes.** Parts fill stubs the room's class
allocated. A part beyond that is a named exception in the composition entry, and the pilot
counts them.

**F18 - Retrofit.** Targeted recompile from the `Realized` column (11.2).

**F19 - Hand allocation and rate collapse.** Accepted as the experiment. Every rated
decision is logged.

**F20 - Labels and compound lines.** Every Spec line opens with a column label unique
within its table and the tables it joins. A line no tag or gloss can answer is several
lines, and splits; a rule line with nothing to answer leaves the Spec. `inventory.md`
places every line.

**F21 - The Overview grows after 3c** (D7). The `Compositions` field is written at 4e and
audited at 5c, as every Overview claim already is.

**F22 - Complexity** (the user's deal breaker). One table per pattern file means as many
tables as the pattern library has files. Section 7 caps files at five per region, adds no
table the patterns don't already imply, and names the one lever left (merging pattern
files) together with its test.

**F23 - Template folders** (D9). Moving templates into folders changes every
`templates/X.md` citation in `STEPS.md`, the read-set graph's path regex in the
validator, and the template globs in `metrics.py` and `context.py`. Phase 1 rewrites
every phase-4 citation anyway, so the move lands in the same pass and nothing is cited
twice.

---

## 4. Goals and non-goals

**Goals**
- Every unit a location contains exists as a row before any prose, with every reference
  set.
- A pass fills one family of tables with every row in view (E1, E8), or writes a
  coordinated build across rooms (E9).
- A table pass reads only its stubs and the roster it draws from.
- The to-do list is mechanical: every unfilled cell is a warning naming its step (D6).
- Retrofit is a targeted diff.
- Location files keep `templates/region/Location.md`'s output shape.
- One firm rule places every line as a column, every pattern file as a table, and every
  table in one of at most five files.
- Templates are foldered like `patterns/`.
- Every table-like file is one of two shapes, each read by one generic parser (6.3).

**Non-goals**
- Changing phases 1-3, `STYLE.md`, `GENRE.md` or `BRIEF.md`, except the Overview's
  `Compositions` field.
- Changing what patterns ask, beyond labels, splits and the five pathway simplifications
  in 7.4.
- Rendering tables on the site.

---

## 5. Decisions

| # | Decision | Settled as |
|---|---|---|
| D1 | Step ids | **Renumber phase 4** |
| D2 | What "supersede the patterns" means | **A pattern specifies one row; the table template owns the table** |
| D3 | Where tables live | **`setting/region/[Code]/`**, next to `Locations.md` |
| D4 | What a cell holds | **A tag** (1-2 words) **or a gloss** (at most 6 words) |
| D5 | Table format | **Two shapes, each with one generic parser**: pipe tables where every field fits one sentence, record files otherwise (section 6); region tables placed by section 7 |
| D6 | Connected stubs | **Their own pass (4h)**; every unfilled cell is a validator warning |
| D7 | Coordinated builds | **A `Compositions` field in the Region Overview** |
| D8 | Hand first | **Yes** |
| D9 | Template layout | **Folders mirroring `patterns/`** (section 8) |
| D10 | Migrate existing table files | **Yes, by the format test** (6.4), in phase 1, while `setting/` is empty |

---

## 6. D5 - pipe tables, judged by what a script can be written around

### 6.1 The evidence in the repository

The framework already uses three shapes for table-like files, and the tools show what
each costs:

| Shape | Files using it today | How the tools read it |
|---|---|---|
| **Pipe table** | `Rumours.md`, `Treasure1-5.md` | one generic reader, `site_common.parse_table_rows`; the header row names the columns |
| **Record block**: a header line, then `Field: value` lines | `Bestiary.md`, `NamedCreatures.md`, `UniqueTreasures.md`, `Lore.md`, `Factions.md` (as `- Field:`), `Quests.md` (as `- Field:`) | a generic field reader, `site_common.parse_field_lines`, **plus** a bespoke regex per file for the header line (`BESTIARY_HEADER_RE`, `FACTION_HEADER_RE`, the registries' `- found at` split, the Named Creature title split) |
| **Bespoke one-liner**: one line per entry whose punctuation is the schema | `Regions.md`, `Locations.md`, `History.md`, `Truths.md` | one regex per file, each written twice (`REGION_RE` and `LOC_GAZ_RE` exist in both the validator and `site_common`) |

"One line per entry" covers two things here. A pipe row *is* one line per entry, with the
schema written in the header row. A bespoke one-liner is one line per entry with the
schema written only in a regex somewhere in `tools/`. The second kind is what has cost a
parser per file.

### 6.2 What a script needs, by shape

| A script needs to... | Pipe table | Record block | Bespoke one-liner |
|---|---|---|---|
| parse any file of this shape with one function | **yes** | **yes**, once the header line is also fields | no: a regex per file |
| know the columns without being told | **yes**: the header row | no: needs a field list from elsewhere | no |
| detect a stub or missing value (D6) | **yes**: an empty cell | yes: a missing or empty field, against a field list | no: a missing value breaks the regex |
| check columns against the pattern (D2) | **yes**: header labels against the pattern's Spec labels | yes: field names against the same labels | no |
| hold prose (several sentences) | no: cells become unreadable | **yes** | no |
| give a clean diff per entry | **yes**: one line | a few lines | one line |

### 6.3 Recommendation

**Two shapes, each read by one generic parser. Bespoke one-liners retire.**

> **The format test.** A file is a **pipe table** when every entry has the same fields and
> no field runs past one sentence. Otherwise it is a **record file**: one record per
> entry, `### [Name]` and then `Field: value` lines, with field names taken from the
> pattern's Spec labels. Documents that are neither (Region Overviews, `Procedures.md`,
> `Setting.md`, location files, checks) keep their own templates.

- **Region tables are pipe tables** (D4's tags and glosses are far inside one sentence).
  Strict columns give D6's to-do list as "this cell is empty", and put every clue in one
  column.
- **Setting-level files sort by the same test** (6.4). Cells there may run to one sentence,
  since they are read directly. D4's six-word limit is for region tables, which are notes
  for compile.
- **The pattern link is mechanical in both shapes.** A pipe header and a record's field
  names are both the pattern's Spec labels (F20), so a script can check a file against its
  pattern. This replaces the hand-maintained regexes.
- **Pipe mechanics:** each table is a `## [Pattern]` heading over its pipe table, and a
  file may hold several; columns exist from creation (allocation creates every table with
  every column, and later passes only fill cells); a draw saying "at least one" takes a
  comma-separated tag list; a line rated `2` takes numbered columns; `|` never appears in
  a cell.

### 6.4 Migrating the existing files (D10)

`setting/` is empty, so migration changes templates and parsers only. There is no content
to convert. It is the cheapest it will ever be.

| File | Today | Becomes | Why |
|---|---|---|---|
| `Rumours.md`, `Treasure1-5.md` | pipe table | **unchanged** | already passes the test |
| `region/Regions.md` | bespoke one-liner (+ tag line) | **pipe table**: Code, Name, Gloss, Rating, Die, Tag line | every field is a tag or a phrase |
| `region/[Code]/Locations.md` | bespoke one-liner | **pipe tables** (section 7) | planned already |
| `Keys.md` | record (header split on `- found at`) | **pipe table**: Name, Form, Found at, Opens (location), Opens (feature), Apart, Connection | every field in `patterns/setting/Keys.md` is a draw or a phrase; its stub state (empty Opens columns) becomes a D6 warning instead of `check_key_obligations`' special case |
| `Quests.md` | record (`- Field:`) | **pipe table**: Name, Given at, Resolved at, Ask, Reluctance, Object, Obstacle, Terms | every field is a draw or one sentence; Terms is one quoted line |
| `Truths.md` | bespoke (bold bullet + `Handle:`) | **pipe table**: Truth, Handle, Codes | each field is one sentence |
| `Bestiary.md` | record + header regex | **record**, header facts as fields (`Type:`, `AD:`, `MA:`) | Description is prose |
| `NamedCreatures.md`, `UniqueTreasures.md`, `Lore.md` | record + header split | **record**, `Found at:` / `Appears at:` as a field | entries carry prose; stubs detected as records missing their prose fields |
| `Factions.md` | record as `- Field:` bullets + header regex | **record**, `AD:` as a field | fields run past one sentence |
| `History.md` | bespoke (`[x] years ago -` + `Left:`) | **record**: `When:`, `Event:`, `Left:`, `Codes:` | an event may be two sentences |
| `Language.md` | sections with lists | **unchanged** in this change | a document with lists; its Roots and Coined lists would pass the test, but nothing in the pipeline depends on them. The pilot can propose it |

**Result:** about ten per-file parsers (counted in 6.1, several of them duplicated across
the validator and `site_common`) become two generic ones. The value-level grammars that
check meaning rather than shape (`AD: Xd6+N`, forced-damage citations, location codes)
stay, now applied to a field or a cell instead of to a whole line.

**Cost:** the templates of the ten migrated files change their Template block, and
`site_common` and `build_site` read the generic shapes. This lands in phase 1 because the
D6 stub warnings need the registries readable generically anyway: Lore, Named Creature and
Unique Treasure stubs are written at 4d and must show up on the to-do list.

---

## 7. Where the lines fall: columns, tables, files

### 7.1 The placement rule

> 1. **Every line that is not an edge is a column**: a question, a draw, or an inline
>    sub-line. It is a column of the table belonging to the pattern file it is written in.
>    Its cell is a tag (a draw), a gloss (a question), or `none`.
> 2. **Every pattern file is exactly one table**, in exactly one file. Rows appear only
>    for the units that drew it. A table drawn by a kind holds only the rows whose kind
>    cell picked it.
> 3. **Every table sits in one of five files**, chosen by the classifier block of the
>    class-file line it descends from:
>
>    | Block | File |
>    |---|---|
>    | substrate, gate, transaction (what the place *is*, and everything drawn once per location) | `Locations.md` |
>    | any pattern on an edge (shared by two locations) | `Exits.md` |
>    | challenge | `Challenges.md` |
>    | reward | `Treasures.md` |
>    | registry | `Links.md` |
>
> 4. **One home.** A pattern reached from more than one line lives where its first draw
>    puts it: the shallowest, then the topmost line in the class file. Every other drawer
>    holds an id column naming its row.

Why the blocks: `patterns/SPEC.md` already groups every classifier's Spec into the same
four questions in every rating (substrate, challenge, reward, registry, plus WILD's access
and SAFE's gate and transaction), and marks them with `-- block:` headers. The file is
read off the header above the line. No judgement is involved, and the list of files is
closed.

### 7.2 The hazards question, answered by the rule

| Option the user named | Verdict |
|---|---|
| 1 table for hazards | **WILD.** `wild/Hazard.md` draws its mechanism as a value (`{MECHANISM}`), and every mechanism answers the same lines. So it is one table, `Challenges.md` § Hazard |
| 3 tables in 1 file | **DANGEROUS.** `dangerous/Hazard.md` draws its mechanism as an edge to `Trap.md`, `Environmental.md` and `Residual.md`, each asking different lines. So it is four tables in `Challenges.md`: § Hazard (every hazard: location, mechanism, tier, clue, searcher's clue, caught) and § Trap, § Environmental, § Residual (only the hazards their mechanism picked, keyed by the same id) |
| 3 files | **Never.** It splits the all-hazards view E1 needs, and gives one unit three homes |

The choice between one table and several is therefore not made at the table at all. It is
made in the pattern, by `patterns/SPEC.md`'s existing rule: a draw where the pick only
sets a value, an edge where it opens lines of its own. Tables inherit that choice.

### 7.3 The test for folding kinds into one table

The only lever left to reduce tables is merging pattern files. The test:

> **Kind files fold into their classifier, as items of a draw, when every kind answers the
> same lines**: the union of their columns leaves no cell `none` merely because its kind
> doesn't ask that question. A `none` from a rate is fine.

Applied to every kind family in the library today:

| Family | Result | Why |
|---|---|---|
| `wild/Hazard.md` mechanisms | already folded | one set of lines for every mechanism |
| `dangerous/` Trap / Environmental / Residual | keep separate | a trap has no kind, no course and no spared spot; harmonised, every trap row carries three structural `none`s |
| `wild/` Ruin / Lair / NaturalFeature / Crossing | keep separate | no line is shared beyond "faction holds it" |
| `safe/` Commerce / Authority / Social / People / Wealth / Garrison | keep separate | each kind's lines are its own (stock and prices, claim and limit, protection, post) |
| `dangerous/` Encounter kinds (creature / named / faction) | keep separate | a named creature is a registry id; creature and faction ask different lines |

So no merge is recommended now. The pilot logs any table that feels like busywork, and a
merge is proposed only where the test passes.

### 7.4 Pathway simplifications (D2: content stays, pathways change)

Five places where the library sends one unit to two homes, or a value through a whole
pattern. Each is fixed by rerouting, not by an exception to the rule:

| # | Today | Rerouted | Effect |
|---|---|---|---|
| P1 | `dangerous/Treasure.md`'s 25% "lesser thing living on the container" draws `dangerous/Creature.md` | a gloss column on § Treasure | Treasure's own Constraint already says it is never a fight, so it is a tell. Creature keeps one home |
| P2 | Concealed-detail Payloads `{a cache \| a piece of Lore \| a Key}` | a `Treasures.md` row with disposition `hidden`, named by id from the payload column | Key and Lore keep one home each, in `Treasures.md` |
| P3 | `dangerous/Key.md` holds both ends (`SPEC.md` already flags it) | split into `Key.md` (supply, § Key in `Treasures.md`) and `Lock.md` (demand, § Lock in `Links.md`, id column naming the gated exit or mystery) | Every lock in a region lives in one table |
| P4 | The class files' "something here someone elsewhere would want" (`dangerous/Quest.md`) | stays a registry-block line, so § Quest in `Links.md` | Listed for completeness: no change, the rule already puts it there |
| P5 | WILD and SAFE exits are one value line inside `Dressing.md` | that line becomes `wild/Exit.md` and `safe/Exit.md`, each § Exit in `Exits.md`; DANGEROUS keeps `Door.md` | Every rating's `Exits.md` holds one row per diagram edge |

### 7.5 What the rule produces, counted

Tables per file, per rating. Every table is a pattern file, except § Location (the
gazetteer row).

| File | DANGEROUS | WILD | SAFE |
|---|---|---|---|
| `Locations.md` | Location, High, Medium, Low, Dressing, Naming (6) | Location, Landmark, Hidden, Secret, Dressing, Ruin, Lair, Natural Feature, Crossing, Faction, Naming (11) | Location, Settlement, Dressing, Commerce, Authority, Social, People, Wealth, Garrison, Naming (10) |
| `Exits.md` | Door (1) | Exit (1) | Exit (1) |
| `Challenges.md` | Encounter, Creature, Faction, Hazard, Trap, Environmental, Residual, Mystery (8) | Creature, Hazard, Mystery (3) | - |
| `Treasures.md` | Treasure, Key, Lore (3) | Treasure, Key, Lore (3) | - |
| `Links.md` | Lock, Quest (2) | Quest (1) | Quest, Lore, Key, Faction, Situation (5) |
| **Files / tables** | **5 / 20** | **5 / 19** | **3 / 16** |

The complexity accounting:
- **Files: five at most, the same five names in every rating.** SAFE has no challenge or
  reward block, so it has three.
- **Tables: one per pattern file the rating reaches**, the same number of things the
  pattern library already asks a writer to know. Tables add no new concept, only an
  address for each existing one.
- **Per room**, compile meets one row in each of § Location, its class table, § Dressing,
  its kind table (WILD/SAFE) and § Naming, then its exits and a handful of challenge,
  treasure and link rows. That's fewer things than today's 4c sheet, which carried every
  drawn line plus every Constraint.
- **Per pass**, a writer works one file's family: all of `Challenges.md` § Hazard and its
  three mechanism tables, for instance.
- The large `Locations.md` counts in WILD and SAFE are the kind tables. Each room has a
  row in only one of them.

**Alternative, if a `Creatures.md` is preferred** (the user's earlier example): split
`Challenges.md` by its draw's items into `Creatures.md` (Encounter, Creature, Faction),
`Hazards.md` and `Mysteries.md`. Same tables, two more files, and one exception to the
block rule. Not recommended: the block rule's value is that it has no exceptions.

---

## 8. Templates layout (D9)

`templates/` mirrors `patterns/`, plus one folder for the judgement checks:

| Folder | Holds |
|---|---|
| `templates/setting/` | every setting-level artifact: `Setting`, `History`, `Truths`, `Rumours`, `Bestiary`, `Factions`, `Treasure`, `Procedures`, `Language`, and the five registries |
| `templates/region/` | rating-independent region and phase-4 step templates: `Region_Gazetteer`, `Connections.mmd`, `Region`, `Region_Connections.mmd`, `Block_Connections.mmd`, `Allocation`, `Composition`, `Location` (compile) |
| `templates/safe/`, `templates/wild/`, `templates/dangerous/` | one template per region file that rating has: `Locations.md`, `Exits.md`, and where the rating has them, `Challenges.md`, `Treasures.md`, `Links.md` |
| `templates/checks/` | the three judgement-check templates |

Consequences:
- **A rating's folder listing is its file inventory.** `templates/safe/` holds three
  templates because SAFE regions hold three files.
- **Rating templates own their rating's mix**, as the patterns already restate per rating.
  `templates/region/Location_Gazetteer.md` dissolves into the three
  `templates/[rating]/Locations.md`, each owning its rating's count, weight or
  classification or prominence mix, tags, and the sections of `Locations.md`. The
  separate weights template from the earlier draft is no longer needed: 4a, 4b, 4f's
  substrate tables and 4g all name `templates/[rating]/Locations.md`.
- **Names no longer collide.** `templates/dangerous/Treasures.md` and
  `templates/setting/Treasure.md` live in different folders, so the earlier `Table_`
  prefix is dropped.
- A step names its template by path (`templates/dangerous/Challenges.md`). The validator's
  read-set graph learns folder paths (F23).

---

## 9. The pipeline

### 9.1 Steps (D1)

| Id | Was | Step | Template | Writes |
|---|---|---|---|---|
| 4a | 4a | **Gazetteer**: names and tags | `templates/[rating]/Locations.md` | § Location, Weight empty |
| 4b | (in 4a) | **Weights**: weight, classification or prominence, in the rating's mix | `templates/[rating]/Locations.md` | the Weight column |
| 4c | 4b | **Connections**: unchanged | `templates/region/Region_Connections.mmd`, `Block_Connections.mmd` | `*.mmd` |
| 4d | (in 4c) | **Allocation**: every file and table created with its columns; every row the class files decide created as a stub with its allocated tags; one Exits row per edge, gate decided once; registry stubs. By hand, rated decisions logged | `templates/region/Allocation.md` | every file, as stubs |
| 4e | (new) | **Compositions**: optional and repeatable; claims stubs, writes parts and the Overview entry; after 4i, a retrofit | `templates/region/Composition.md` | part rows; the Overview field |
| 4f | (in 4c) | **Table passes**: one per file family, filling every unclaimed, unconnected row | `templates/[rating]/[File].md` | each file |
| 4g | (in 4c) | **Naming**: § Naming, then the name sync | `templates/[rating]/Locations.md` | `Locations.md`; labels; registry lines |
| 4h | 4d | **Connected fill** (D6): exits, locks, foreshadowing, then registry entries | `templates/[rating]/Exits.md`, `templates/[rating]/Links.md`, registry templates | the rest |
| 4i | (in 4c) | **Compile** | `templates/region/Location.md` | `[N].md`; `Realized` cells |
| 4j | 4d (tail) | **Coinage and mechanics** | `templates/setting/Language.md`, `Procedures.md` | as today |

### 9.2 Order within 4f

`Challenges.md` (Creature before Encounter, Exits-referencing hazards and wards after the
exit stubs exist), then `Treasures.md` (rows name their guards), then `Locations.md`'s
class tables (whose concealed-detail Payloads name treasure rows, P2). § Dressing can come
any time before compile.

### 9.3 Read set of a table pass

| Pass | Reads, besides `GENRE.md`, `STYLE.md`, `BRIEF.md` and the patterns of its tables |
|---|---|
| `Challenges.md` | the Overview's Inhabitants and Conditions; the `Bestiary.md` and `Factions.md` entries named; `Procedures.md` for damage; its stubs; the exit rows they name |
| `Treasures.md` | the Overview's Loot; the Treasure tables' headings; its stubs; the guard rows they name |
| `Locations.md` (substrate) | the Overview's Conditions and Places; § Location |
| `Links.md` | its stubs; the rows they name; the registry stubs |

Every stub carries its location code, and § Location gives that room's name, weight and
tags. That is all a pass sees of a room.

### 9.4 The to-do list (D6)

A stub is a row with empty cells. The validator warns once per row, naming file, table,
id, empty columns and owed step. A pass that creates a stub elsewhere (a treasure turning
out to be a key owes a § Lock row) shows up in the warnings immediately. `--pending
[REGION]` groups the list by step.

### 9.5 Compositions (D7)

A `Compositions` field in each `patterns/region/*.md` Spec and in
`templates/region/Region.md`, written at 4e:

```
Compositions:
- [Name] - [row ids, in the order met]; [chain: what is held or known -> where it is
  used -> what it yields, link by link]; way round: [the answer that is not the gate,
  and its price]; exceptions: [part ids beyond their room's class, with reasons, or none]
```

A build spanning regions is entered once, in the Overview of the region holding its last
link. **Proven correct** means all eight hold (⚙ = later mechanical): ⚙ every named id is
a filled row; ⚙ solvable from the entrance, with no part behind the gate it opens and no
cycle; every clue obvious or one trigger from obvious in its own room; ⚙ no clue shares a
room with its answer; ⚙ every part fills an allocated stub or is a listed exception; the
way round exists and is priced; ⚙ every key, lore, quest object, named creature or unique
treasure has its registry row; ⚙ after a retrofit, every part has its `Realized` cell
present in its room.

---

## 10. Worked example - `Challenges.md` (DANGEROUS)

Content is illustrative, to show the shape; it is not a pattern.

```
# Challenges of C The Ravine

## Encounter
| ID  | Location | Kind     | Doing             | Sign              | Wants | Absent | Who | Realized |
|-----|----------|----------|-------------------|-------------------|-------|--------|-----|----------|
| EN1 | C.12     | creature | dicing at brazier | bone dice clatter | none  | none   | CR1 |          |

## Creature
| ID  | Entry           | Shape  | Number | Scale  | Demeanour |
|-----|-----------------|--------|--------|--------|-----------|
| CR1 | Gorzgur Warrior | patrol | 4      | medium | Bored     |

## Faction
| ID | Position | Identity | If lost | Order | Friction | Unwilling |
|----|----------|----------|---------|-------|----------|-----------|

## Hazard
| ID  | Location | Mechanism     | Tier     | Clue                        | Searcher's clue  | Caught       | Realized |
|-----|----------|---------------|----------|-----------------------------|------------------|--------------|----------|
| HZ1 | C.14     | trap          | damaging | slack wire across threshold | oil at the hinge | none         |          |
| HZ2 | C.18     | environmental | nuisance | dark sheen on flags         | none             | rat mid-band |          |
| HZ3 | C.31     | residual      | lethal   |                             |                  |              |          |

## Trap
| ID  | Parts               | Trigger     | Damage      | Set by              |
|-----|---------------------|-------------|-------------|---------------------|
| HZ1 | weighted spear rack | wire pulled | 2d Piercing | Gorzgur, maintained |

## Environmental
| ID  | Kind    | Condition            | Cause       | Course    | Threshold      | Damage      | Spared spot |
|-----|---------|----------------------|-------------|-----------|----------------|-------------|-------------|
| HZ2 | footing | silt film over flags | sluice seep | worsening | moving quickly | 1d Crushing | none        |

## Residual
| ID  | Maker | Doing | Course | Edge | Damage | Protects |
|-----|-------|-------|--------|------|--------|----------|
| HZ3 |       |       |        |      |        |          |

## Mystery
| ID | Location | Fixture | Detail 1 | Detail 2 | Detail 3 | Trigger | Correct | Wrong | Realized |
|----|----------|---------|----------|----------|----------|---------|---------|-------|----------|
```

It shows the three cell states (HZ3 is a stub, owed to 4f), an empty table (no faction
drawn in this region yet), a compound line split (Hazard's clue into Clue and Searcher's
clue), a renamed clashing label (Trap's own "Mechanism" becomes `Parts`), and an id
column linking tables (`Who: CR1`). `Realized` is empty until compile.

---

## 11. Compile (4i)

### 11.1 First compile

`templates/region/Location.md` keeps its Template block, Citations and Feature grammar.
Its Context becomes every row naming this location.

- **Every row is realized; nothing without a row is written.** The row's `Realized` cell
  gets the Feature label (or `Exits`, `Summary`, `Notes`) that carries it.
- **Cells are notes, never copied as text.** Compile writes each Feature in the template's
  grammar from its cells, and adds no fact.
- **One location, its own rows only.**
- The 30-word Feature ceiling holds.

### 11.2 Targeted recompile (retrofit)

New rows get new Feature lines, placed by prominence; a changed row's line is rewritten,
and only that line; the Summary and Notes are revisited only for an obvious-tier change;
every other line stays as it was.

---

## 12. Validation

**Phase 1** (the lint kept working, plus D6): the region-folder glob narrows to
`[0-9]*.md`; template paths with folders resolve in the read-set graph; the two generic
parsers (6.3) replace the per-file ones in the validator and `site_common`. The pipe
parser errors on a cell count that differs from the header, an unknown id or code, or a
duplicate id. The record parser errors on an unknown field. Both **warn per stub**: an
empty cell, or a record missing a field its pattern requires.

**Pilot, by hand**: kind-to-table pairing; one Exits row per diagram edge; the composition
proof; the distinctness rules the columns expose (a purpose repeated in a block, one exit
description across more than a third of a block's exits, two hazards in a block sharing
mechanism and clue).

**After the analysis**, where called for: the mechanical checklist items become validator
checks; `metrics.py` learns per-table counts and asked against realized.

**Judgement checks**: *rows written in one pass read as a form*, *rooms read as one room*,
*each composition is solvable and priced*.

---

## 13. Analysis after the pilot

Written to `plans/table-pipeline/analysis.md`:

| Question | If the answer is no |
|---|---|
| Did hand allocation hold the rates at region scale? | `draw.py` returns for 4d |
| Did standalone read sets carry enough (rows compile sent back)? | add the narrowest missing input |
| Was assembling read sets by hand cheap enough? | rebuild `context.py` as a collector |
| Were the hand checklist items reliable? | each missed item becomes a validator check |
| Did compositions stay inside the weights? | compositions move before 4b for the rooms they claim |
| Did retrofits stay targeted? | revisit D4 |
| Did six-word cells hold every line? | split the line further |
| Did any table feel like busywork? | apply 7.3's fold test to it |
| Did table passes beat E1 / E8? | fall back to A2 |

---

## 14. Documentation changes, by the rules in `CLAUDE.md`

- `STEPS.md`: phase 4 replaced per 9.1, with every template cited by its new path.
- `patterns/SPEC.md`: the placement rule (7.1), the fold test (7.3), the label and split
  rules (F20); the `dangerous/Key.md` paragraph resolved by P3 and cut to a pointer.
- Pattern files: labels, splits, P1-P5 (`dangerous/Key.md` split; `dangerous/Lock.md`,
  `wild/Exit.md`, `safe/Exit.md` new), step citations moved.
- `patterns/region/*.md` and `templates/region/Region.md`: the `Compositions` field.
- `templates/`: moved into folders (section 8); the ten migrated files' Template blocks
  rewritten to their new shape (6.4). The new and rewritten templates are listed
  in `implementation.md`.
- `CLAUDE.md`: one line pointing at the placement rule. `README.md`: the `templates/`
  entry names its folders, and the region-folder entry names its five files.
- No passage is refreshed to describe the new pipeline. A passage that restated the old
  one is cut back to a pointer.

---

## 15. Acceptance

A hand-run pilot (the keep, the borderland, the ravine and at least two caves from
`BRIEF.md`) through 4a-4j and 5c, and:

1. Validator: no errors, and no stub warnings at the end.
2. Every rated line within the template's tolerance at region scale, or a logged choice
   (E2).
3. One Exits row and one gate decision per edge (E3).
4. Creature count reconciles with each Overview's Inhabitants (E4).
5. Every row realized in exactly one location file; no Feature without a row.
6. A three-room composition passes all eight proof items, and a second is applied as a
   retrofit within 11.2's limits.
7. The creature pass runs from 9.3's read set alone.
8. 5c's "rooms are distinct" beats 9c1354b on comparable blocks, and "rooms read as one
   room" is Confirmed.
9. Every region has at most five files, and every table maps to exactly one pattern file
   or to § Location.
10. `analysis.md` answers every question in section 13.
