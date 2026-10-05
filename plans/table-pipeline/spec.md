# Spec - table-driven location generation

The request is in `intake.md`. This file gives the analysis first (what the current
pipeline does, what has gone wrong with it, the alternatives, and the friction points),
then the design that follows from it. Decisions that need the user's sign-off are
collected in section 5. Everywhere else, the design states its recommended answer and goes
ahead with it.

---

## 1. Analysis - the pipeline today

Phase 4 today, per `STEPS.md`:

| Step | Writes | Unit of work |
|---|---|---|
| 4a | `Locations.md` per region: name, weight/classification, three tags | region |
| 4b | connection diagrams (`Connections.mmd`, one `[Block].mmd` per DANGEROUS block) | region / block |
| 4c | one `[N].md` per location, from `tools/context.py 4c CODE`. Registry stubs are created as Features call for them | location (DANGEROUS: one block per context) |
| 4d | full registry entries (`Lore`, `Keys`, `Quests`, `NamedCreatures`, `UniqueTreasures`) | setting |

At 4c, everything about a location is decided and written in one pass. `context.py` walks
the location's class file (`dangerous/High.md` and its siblings), settles every rate and
draw from the location code, and prints a sheet. The generator then writes the finished
entry from that sheet. The doctrine is "write each location from those alone, never from
its sibling rooms".

### What the last two validation runs found

These findings come from commit 9c1354b, in its `SettingJudgementCheck.md` and the two
addenda. Each one traces to a property of the location-at-a-time pipeline:

| # | Finding | Why the current shape produces it |
|---|---|---|
| E1 | Near-repeats that no single writer can see: one hazard shape six times, then three; pitch-sealed containers four times; alarm cords seven times; dead vermin as a tell seven times | Each location is written blind to its siblings, so there is no point at which all of a region's hazards are in view together |
| E2 | Rates not realized at region scale: no second name in 30 rooms against 20%; edges about 94% open against 60%; 29 of 34 treasures a table roll against 55% | The rate is settled per location, and nothing ever looks at the region-level total |
| E3 | Gates on 43% of exit-ends, and 7 warded doors in 22 rooms | Each end of an edge draws its own gate independently, because an exit belongs to two locations and gets resolved twice |
| E4 | A household of "about ten" shows up as one creature across the whole block | No contract line draws against the Overview's Inhabitants headcount. The creatures are scattered across sheets that are never summed |
| E5 | MEDIUM "encounter never absent" overridden; household blocks drawing a purpose FAMILY | Bugs in `context.py`'s resolution. They are invisible because no sheet is ever compared to another |
| E6 | Key, Lore and Quest obligations tracked by hand ("nothing is owed at the close of 4c") | Connected content is discovered while writing, not allocated up front |
| E7 | A 173-word Feature; 22 rooms growing from 3,129 to 10,603 words | The sheet hands the writer raw material and the decisions together, and the writer pours everything in |
| E8 | Two Khughik blocks differing in dressing but not in skeleton | Block-level distinctness has no artifact where it could be checked |

E1-E4, E6 and E8 are all distribution problems: a property of many rows at once, invisible
from inside any one of them. Tables are what make a distribution visible. E5 and E7 are
not caused by the location-at-a-time shape, but tables expose E5 and give E7 a structural
fix (section 9).

---

## 2. Alternatives considered

| | Alternative | Gets | Misses | Cost |
|---|---|---|---|---|
| A1 | **Status quo plus checks**: keep 4c and add region-level validator and metrics checks for repeats and rates | Detection of E1-E3 after the fact | Prevention. Every failure costs a rewrite, and the writer still cannot see siblings | Low |
| A2 | **Allocation tables only**: a tool writes every row stub (draws settled, cross-references set) into per-type tables; locations are still written one at a time from their stubs | Fixes E2, E3, E4, E5 and E6 by construction: rates, per-edge gates, headcounts and obligations are all settled before any prose | E1 and E8. Prose is still written blind to siblings | Medium |
| A3 | **Full table pipeline** (the request): A2, then each table is filled in its own pass with every row of that type in view, then a compile step writes the location files | Everything A2 gets, plus E1 and E8: distinctness is written for, not just checked | Room coherence, which has to be designed for (F1) | High |
| A4 | **Tables as the product**: A3 with no compile step; the site builder renders location pages straight from tables | No second writing pass, no drift between table and file | Player Summary and Referee Notes would have to become columns. It contradicts the request's final step, and `build_site.py`, `build_pdf.py`, `metrics.py` and the validator all read `[N].md` | High, and against the request |

**Recommendation: A3, delivered through A2.** A2's allocation tables are the first half of
A3, and A2 is worth shipping on its own: it can be piloted with the existing 4c writing
before the table fill passes exist. `implementation.md` orders the work so that A2 is a
working milestone.

---

## 3. Friction points

Each is stated with its resolution in this design. F1-F4 are the ones that could sink the
change.

**F1 - Room coherence across horizontal passes.** `templates/Location.md` requires "one
history per room". A Hazards pass that writes every hazard in the region, without the
room's encounter in view, can produce a hazard that could not share the room with its
other contents.
*Resolution:* (a) the substrate (each room's Dressing) is written first and is read by
every later pass, so every row is written against what the room is; (b) the passes run in
a fixed dependency order (section 8.3), and each pass reads the already-filled rows it
references; (c) the compile step reads all of a room's rows together and may adjust
wording to make them one room, but may not add or drop a fact (section 9). A row that
cannot be made to fit is sent back with a reroll, the same rule as today.

**F2 - The sibling doctrine is reversed.** 4c says "never from its sibling rooms" because
writing against siblings converges. A table pass is designed to show every sibling of one
type.
*Resolution:* the doctrine is narrowed rather than dropped. It keeps holding where it was
earned: the compile step writes each location from its own rows only and never opens
another location file. Inside a table pass, convergence is countered by settling each
row's draws per row id before the pass starts, which forces variation, and by table-level
distinctness rules the validator can check (section 10). Sibling visibility stops being a
risk and becomes the mechanism for E1 and E8. The 5c judgement check gains an item to
watch whether rows written in one pass have turned formulaic.

**F3 - Step renumbering.** `README.md` says step ids grow by suffix and are "never
renumbered without explicit user request". The validator's step regex allows a single
letter suffix (`[1-9][0-9]*[a-z]`). The requested order (weight, then connect, then
features, then compile) puts a new step before today's 4b and replaces 4c and 4d.
*Resolution:* Decision D1.

**F4 - "Supersede our currently existing patterns" against single authority.**
`CLAUDE.md` says documentation names the authority and never restates it. `BRIEF.md` says
a template never overrides a pattern. If a table spec lists its columns by copying a
pattern's Spec lines, there are two copies, and the copy is the one that drifts.
*Resolution:* Decision D2. Whichever way it goes, there is exactly one copy.

**F5 - Weight fails the table test.** Applied to weight, the firm test (section 6) says it
is a field: exactly one per location, opening no lines. Yet the request gives weighting
its own step.
*Resolution:* a step is not a table. A step may add a column to a table that already
exists. Weighting is a column pass on `Locations.md`, and so are substrate and naming.
"One file per feature type" holds for tables, and nothing requires one file per step.

**F6 - Region tables against setting registries.** Keys, Lore, Quests, Named Creatures and
Unique Treasures already have setting-level homes, and a key's two ends can sit in
different regions. A region `Keys` table would be a second home.
*Resolution:* anything with an identity beyond one location's placement keeps its
setting-level registry as its table. The region tables hold the placement: the treasure
row that *is* a key carries the `dangerous/Key.md` supply columns plus a foreign key to
the `setting/Keys.md` row. This is the firm test applied to the two altitudes
`dangerous/Key.md` and `patterns/setting/Keys.md` already describe. It also settles the
split `patterns/SPEC.md` already flags: Key's demand end becomes columns on the row it
gates (an exit or a mystery).

**F7 - Compile writes facts twice.** If table cells are prose and the compile step writes
prose again, the two copies drift, and the compile pass is where E7's bloat happens.
*Resolution:* Decision D4. The recommended answer is that cells are terse facts, the
compile step owns the prose, and each row records which Feature realized it, so every row
is traceably delivered.

**F8 - Cost.** A3 adds about eight passes per region on top of compile. The compile pass
reads less than today's sheet, but the total goes up.
*Resolution:* `context.py cost` gains the table strategy so the increase is measured, not
guessed. The pilot (implementation phase 7) records it. A table pass reads one row per
instance plus the substrate it references. It never reads whole location files.

**F9 - Cross-references between tables.** Treasure is guarded by an encounter or a hazard;
a hazard can sit on an exit's gate; a MEDIUM concealed detail's Payload changes what the
challenge is worth; a ward on a gate is a mystery.
*Resolution:* every cross-reference is created as a foreign key at allocation, so no fill
pass discovers a relationship. The pass order is a DAG over those keys (section 8.3). The
graph has no cycle, because a guard always points at what it guards and never the other
way round.

**F10 - Naming comes last, but names are used early.** `patterns/setting/Naming.md` names
a location "after everything else is decided", yet the 4a gazetteer gives it a name that
diagram node labels and registry rows then repeat. This tension exists today.
*Resolution:* tables key everything by code, never by name. Naming is a late column pass,
and a tool syncs every downstream mention of the name (diagram labels, registry
`found at` lines) from `Locations.md`.

**F11 - Bugs in the tool become bugs at scale.** Allocation replaces the hand-reading of
sheets with a tool that writes every row. E5's resolution bugs would then be written into
every table.
*Resolution:* E5 is fixed and given regression checks before allocation is built
(implementation phase 1).

**F12 - Rerolls ripple.** Rerolling a treasure from table roll to key creates a Keys stub
and a lock obligation somewhere else. Rerolling after rows are filled can strand content.
*Resolution:* allocation is idempotent and only ever rewrites stubs. A filled row is
locked, and changing it means clearing it explicitly. A reroll that would orphan a
filled row is refused, with the dependent row ids printed.

**F13 - Existing consumers of the region folder.** The validator treats every `*.md` in a
region folder except `Locations.md` as a location file. `site_common`, `build_site` and
`metrics` read `[N].md` and `*.mmd` by glob.
*Resolution:* tables live in `setting/region/[Code]/tables/` (Decision D3), so every
existing glob is untouched. Compiled location files stay the product that the site, the
PDF and metrics read.

**F14 - SAFE and WILD access fit the shape unevenly.** SAFE has no challenge block, and
WILD access (Hidden leads, Secret access triples) currently forces Landmark → Hidden →
Secret write order.
*Resolution:* the test handles both without special cases. WILD access is exactly one per
parent→child edge, so it is a column group on that edge's row in `Exits`, created at
allocation from the diagram. The tier write order then falls away, because the lead
exists as a stub before either end is written. SAFE simply has fewer tables (section 7).

**F15 - Gazetteer purpose changes.** `templates/Location_Gazetteer.md` says the gazetteer
is "a lightweight target list ... not a place for content". Under the test, `Locations.md`
is the location table, and substrate and naming are its columns.
*Resolution:* the record format keeps each row's first line exactly as today, so existing
parsers keep working. Column groups go on indented lines under it (section 8.1). The
template's purpose line is rewritten to match.

---

## 4. Goals and non-goals

**Goals**
- Every unit a location contains exists as a row in a per-type table before any prose is
  written, with every draw settled and every cross-reference set (fixes E2-E6).
- Each table is filled in one pass with all its rows in view (fixes E1, E8).
- Connected content is stubbed at allocation and filled once every location it joins
  exists, through the same two phases the registries use today.
- Location files keep `templates/Location.md`'s output shape. The site, the PDF, metrics
  and the validator's location checks keep working.
- One firm, decidable test sorts every pattern into a field or its own table.

**Non-goals**
- Changing phases 1-3, `STYLE.md`, `GENRE.md` or `BRIEF.md`.
- Changing what any pattern file asks. The pattern library is the row spec, and its
  content is out of scope except where a citation to a retired step id must move.
- Rendering tables on the site. Tables are working artifacts; location files are the
  product.

---

## 5. Decisions needing sign-off

| # | Decision | Recommended | Alternative |
|---|---|---|---|
| D1 | Step ids for the new phase 4 | **Renumber phase 4** (section 8.2). Every phase-4 template is rewritten regardless, so updating the citations costs little, and the ids then read in build order. `README.md` requires the user's explicit request for this | Retire 4a-4d in place (as 1a was) and append the new steps as 4e-4n. No renumber, but the build log reads out of order |
| D2 | What "supersede the patterns" means | **Patterns stay the row spec.** A table's columns are its pattern's Spec lines, read off the file by tool (`tables.py columns`) and never copied into a template. Tables supersede the class-file walk and the 4c sheet, not the pattern library | Rewrite each table-bearing pattern file into table form (Spec lines become a Columns block). Still one copy, but every pattern file, `SPEC.md` and the validator's pattern checks change shape |
| D3 | Where tables live | **`setting/region/[Code]/tables/[Table].md`**, which leaves every existing glob untouched (F13) | Next to the location files in the region folder. Needs every consumer's glob tightened |
| D4 | What a cell holds, and what compile does | **Cells are terse facts; compile writes the prose** from one location's rows, may not add or drop a fact, and records each row's Feature label back into the row (`Realized:`) | Cells hold the finished Feature sentence and compile assembles them plus Summary and Notes. Cheaper, but room coherence (F1) can no longer be fixed at compile |
| D5 | Row format | **Record blocks**: a first line matching today's gazetteer and registry style, then `Field: value` lines. Diff-friendly, and the existing parsers' style | Markdown pipe tables. Unreadable once cells run past a few words, and fragile to edit |
| D6 | Build order across regions | **Per region through the feature passes; setting-wide gate before connected fill.** A connected stub is filled only once every location it names has its substrate (validator `--pending` reports what is owed) | Strict layer by layer: each step across every region before the next |

---

## 6. The table test

This is the rule the request asks for. It goes into `patterns/SPEC.md` (as a section beside
"A draw or an edge is decided by what the pick opens", which it extends), and into
`CLAUDE.md`'s pattern rules as one line pointing there.

> **A unit gets its own table when, for at least one Spec line that draws it, both hold:**
>
> 1. **It opens lines.** Picking it leaves lines of its own to answer, either a file
>    reached by an edge or sub-lines nested under the drawing line. A value (a question's
>    answer, an item of a `{draw}`) never gets a table.
> 2. **It is not exactly one per drawing row.** The drawing line can yield none of it
>    (any rate under `1`, or a condition), more than one, or one instance shared by two or
>    more rows.
>
> **Otherwise it is a column group on the table of the row that draws it.**

Corollaries, each forced by the two conditions rather than added to them:

- **One unit, one table.** If any drawer makes a unit a table, every drawer references
  that table's rows rather than inlining the unit. (`dangerous/Creature.md` is exactly one
  per encounter but 25% on a treasure, so creatures are a table, and the encounter row
  holds a foreign key.)
- **Shared means connected.** A unit shared by rows in two locations is created at
  allocation as a stub naming every row it joins, and filled once those rows exist.
  A *column* that names another location (a foreshadowing detail, a lock obligation) is
  connected in the same sense. Connectedness is about depending on another location's
  content, not about table versus field.
- **Parents are already tables.** The test runs downward from the location. A region and a
  block are each one row that many locations point to, so they are tables by condition 2
  read from below. Both already exist: the Region Overview, and the block diagram's header.
- **A step is not a table.** A step may fill a column group of a table that already exists
  (F5).
- **The setting-level twin wins.** Where a unit has a region-placement pattern and a
  setting-entry pattern (`dangerous/Lore.md` and `patterns/setting/Lore.md`), the test is
  applied to each one. The placement is usually exactly one per drawing row, so it becomes
  columns; the entry is shared, so it becomes the registry table (F6).

### The test applied to the hard cases

| Unit | Drawn by | Opens lines? | Exactly one per drawer? | Result |
|---|---|---|---|---|
| Weight / classification / prominence | location | no (a draw) | yes | column of `Locations` |
| `dangerous/Dressing.md` | every class file, at `1` | yes | yes | column group of `Locations` |
| HIGH's architecture detail, 50% ambiance | `dangerous/High.md` | no (questions) | - | columns of `Locations` (`none` when unrolled, per "State the nil") |
| Concealed detail (Clue/Trigger/Payload) | MEDIUM 40%, LOW parameterized, WILD 20%, SAFE 10% | yes (nested) | no (can be absent) | table `Secrets` |
| `dangerous/Door.md` | every exit | yes | no (shared by two locations) | table `Exits`, one row per edge |
| WILD access (Hidden lead, Secret access triple) | parent→child edge | yes | yes, per edge | column group of `Exits` |
| `dangerous/Encounter.md` | HIGH / MEDIUM challenge, treasure guard | yes | no | table `Encounters` |
| `dangerous/Creature.md` | encounter (1), treasure (25%) | yes | no, via treasure | table `Creatures` |
| `dangerous/Faction.md` | encounter kind | yes | yes | column group of `Encounters` |
| `dangerous/Hazard.md` | challenge, treasure, door gate | yes | no | table `Hazards` |
| `dangerous/Trap.md` / `Environmental.md` / `Residual.md` | hazard mechanism | yes | yes | column groups of `Hazards` |
| `dangerous/Mystery.md` | challenge, HIGH 30%, warded gate | yes | no | table `Mysteries` |
| `dangerous/Treasure.md` | HIGH 1 + 40%, MEDIUM / LOW rated | yes | no | table `Treasures` |
| `dangerous/Lore.md`, `dangerous/Key.md` supply, `dangerous/Quest.md` | treasure kind, secret payload, registry lines | yes | yes, per drawing row | column groups of the drawing row, plus a foreign key to the registry |
| `dangerous/Key.md` demand | lock obligation | yes | yes, per gated row | column group of the gated `Exits` or `Mysteries` row |
| `patterns/setting/Keys.md`, `Lore.md`, `Quests.md`, `NamedCreatures.md`, `UniqueTreasures.md` | placements | yes | no (shared) | existing setting registries |
| Foreshadowing detail | MEDIUM 25%, LOW 10% | no (a question) | - | column of `Locations`, connected (names a HIGH) |
| Naming, second name | every class file | yes / no | yes / - | column group / column of `Locations` |
| `safe/People.md` as gate | every SAFE location | yes | no (one person, several locations) | the Overview's People roster is the table; the per-visit lines are a column group of `Locations` with a foreign key |

The inventory in section 7 is this table, completed. Implementation task T1.3 produces it
mechanically from every Spec line in `patterns/`, so the list below is checked against the
library rather than trusted.

---

## 7. Table inventory, by rating

Region tables, in `setting/region/[Code]/tables/` (D3), except `Locations.md`, which stays
where it is. A rating gets only the tables its pattern files produce.

| Table | Pattern (row spec) | DANGEROUS | WILD | SAFE |
|---|---|:-:|:-:|:-:|
| `Locations.md` (existing, grows columns) | class file + `Dressing.md` + `patterns/setting/Naming.md` (+ WILD/SAFE kind files as column groups) | ✓ | ✓ | ✓ |
| `Exits.md` | `dangerous/Door.md`; WILD/SAFE `Dressing.md` exit line; WILD access | ✓ | ✓ | ✓ |
| `Secrets.md` | concealed-detail lines of the class files | ✓ | ✓ | ✓ |
| `Encounters.md` | `dangerous/Encounter.md` (+ `Faction.md` columns) | ✓ | | |
| `Creatures.md` | `dangerous/Creature.md` / `wild/Creature.md` | ✓ | ✓ | |
| `Hazards.md` | `*/Hazard.md` (+ mechanism columns) | ✓ | ✓ | |
| `Mysteries.md` | `*/Mystery.md` | ✓ | ✓ | |
| `Treasures.md` | `*/Treasure.md` (+ Lore / Key / Quest placement columns) | ✓ | ✓ | |
| `Factions.md` | `wild/Faction.md`, `safe/Faction.md` | | ✓ | ✓ |
| `Situations.md` | `safe/Situation.md` | | | ✓ |

Setting registries (existing files, new stub timing): `Keys.md`, `Lore.md`, `Quests.md`,
`NamedCreatures.md`, `UniqueTreasures.md`. Their stubs are written at allocation instead
of 4c, and their full entries at connected fill, as at 4d today.

A pattern file whose name is shared across ratings (`dangerous/Hazard.md`,
`wild/Hazard.md`) produces one table per region, following that region's rating's file.
The restatement across rating folders stays deliberate, as `STEPS.md` 5b says.

---

## 8. The pipeline

### 8.1 Table format (D5)

One record per row, blank line between records.

```
[Row ID] [Location Code(s)] - [drawn values, settled at allocation]
  [Column]: [value]
  [Column]: [value]
  Realized: [Feature label in the location file, written at compile]
```

- **Row ID**: `[TABLE PREFIX][n]`, scoped to the region (`HZ3`, `TR12`, `EX7`), stable,
  never reused once filled. In `Locations.md` the location code is the row id, and the
  first line stays exactly today's gazetteer line, so existing parsers keep reading it.
- **Foreign key**: a cell naming another row by id (`Guard: EN4`), or a location by code.
  A registry key is cited in its existing citation form (`Keys: Title`).
- **Stub**: a record carrying only its first line and its foreign keys. **Filled**: every
  column its pattern requires answered, with nil written as `none`.
- A drawn value is written as settled and never re-decided by the filling pass. Rerolls go
  through the tool (F12).

### 8.2 Steps (D1, recommended numbering)

| New id | Was | Step | Template | Unit | Writes |
|---|---|---|---|---|---|
| 4a | 4a | **Gazetteer**: names and tags | `Location_Gazetteer.md` (weight removed) | region | `Locations.md` first lines |
| 4b | (in 4a) | **Weights**: DANGEROUS weight, WILD classification, SAFE prominence, in the template's mix | `Location_Weights.md` (new) | region | `Locations.md` weight column |
| 4c | 4b | **Connections**: diagrams, unchanged | `Region_Connections.mmd`, `Block_Connections.mmd` | region / block | `*.mmd` |
| 4d | (in 4c) | **Allocation**: every row in every table, and every registry stub, created with draws settled and foreign keys set. *Every row in the setting exists as a stub after this step*, the row-level counterpart of today's 4a guarantee | `Allocation.md` (new), run by `tools/tables.py allocate` | region | all tables, as stubs; registry stubs |
| 4e | (in 4c) | **Substrate**: fill `Locations.md`'s Dressing and class-file substrate columns | `Table_Locations.md` (new) | region (DANGEROUS: block) | `Locations.md` |
| 4f | (in 4c) | **Feature tables**: one pass per table, in 8.3's order, every row of that table for the region in view | `Table_[Name].md` (new, one per table) | region × table | each table |
| 4g | (in 4c) | **Naming**: the naming column pass, then a name sync | `Table_Locations.md` naming section | region | `Locations.md`; `.mmd` labels and registry lines via `tables.py sync-names` |
| 4h | 4d | **Connected fill**: every connected stub whose locations all have substrate (cross-region exits and links); then every registry's full entry | registry templates (contexts updated) | setting | remaining stubs; registries |
| 4i | (in 4c) | **Compile**: one `[N].md` per location from its rows | `Location.md` (Context rewritten) | location | `[N].md`; each row's `Realized:` |
| 4j | 4d (tail) | **Coinage and mechanics**: grow `Language.md`; revisit `Procedures.md` only if needed | `Language.md`, `Procedures.md` | setting | as today |

Phase 5 is unchanged except for step-id citations and the judgement-check items in
section 10.

### 8.3 Fill order within 4f

Each table is filled after every table its rows reference:

```
Locations (4e substrate)
  -> Exits         (needs both ends' substrate)
  -> Creatures
  -> Encounters    (references Creatures)
  -> Hazards       (may reference Exits, for a trap on a gate)
  -> Mysteries     (may reference Exits, for a ward)
  -> Treasures     (references its guard: Encounters / Hazards)
  -> Secrets       (Payload may reference Treasures, Exits)
  -> Factions, Situations   (WILD / SAFE)
```

A row whose referenced row is still a stub (one held for 4h because the far end is in
another region) is filled against the stub's drawn values and flagged for re-reading at
4h.

### 8.4 Read set of a table pass

`GENRE.md`, `STYLE.md` and `BRIEF.md` every time (per `CLAUDE.md`); the region's Overview;
`setting/Procedures.md` where the table carries forced damage. Then
`python3 tools/tables.py sheet [Code] [Table]`, which prints:

- the columns this table owes, read off its pattern file (D2), with that file's
  Constraints;
- every row of this table for the region: drawn values and foreign keys;
- for each row, the substrate columns of its location(s), and the filled cells of every
  row it references.

It never prints a location file, a row of a table not referenced, or registry content.
A large DANGEROUS region may be split per block. The template sets the threshold.

### 8.5 Allocation (4d)

`tools/tables.py allocate [Code]` reuses `context.py`'s resolution walk (the class file,
rates, draws and conditionals, seeded per `tools/draw.py`), with two changes:

- **The seed is the row id where the draw belongs to a row**, and the location code where
  it belongs to the location. An exit's gate is drawn once per edge, keyed by edge (E3).
- **The output is rows, not a sheet.** Each drawn unit becomes a row in its table (or a
  column group on its drawer's row, by section 6), with foreign keys to its drawer and
  referents. Registry stubs are written to the setting registries naming both ends where
  a pattern requires both (Keys).

It also prints the allocation report: per table, rate asked against rate realized across
the region, and the region's creature headcount against the Overview's Inhabitants
(E2, E4). Anything off the template's tolerance is surfaced for a deliberate reroll,
never silently adjusted.

### 8.6 Connected features

"Connected" means a row or column whose content depends on another location's content.
The stub/fill lifecycle:

| Connected unit | Stub at 4d names | Filled at |
|---|---|---|
| Exit (every edge) | both locations, kind from the diagram, drawn opening and gate | 4f `Exits` if both ends are in the region and have substrate, otherwise 4h |
| WILD access lead / secret triple | parent and child | 4f `Exits` |
| Lock (Key demand) | the gated row, the Keys stub | 4f, on the gated row |
| Foreshadowing detail | the room and the HIGH it points at | 4e if the HIGH has substrate, otherwise 4h |
| Keys / Quests | both locations | registry entry at 4h, placement columns at 4f |
| Lore / Named Creature / Unique Treasure | every placing location | registry entry at 4h |

---

## 9. Compile (4i)

`templates/Location.md` keeps its Template block, its Citations and its Feature grammar;
the output format does not change. Its Context changes from "run `context.py 4c` and write
from the sheet" to "run `tables.py sheet [Code]` and write from the rows". That command,
with a location code, prints every row of every table naming this location, filled, plus
its exits as `Exits.md` states them.

The compile rules (D4):

- **Every row is realized; nothing without a row is written.** This is the structural
  form of today's instruction 1. Each row's `Realized:` cell gets the Feature label (or
  `Exits`, `Summary`, `Notes`) that carries it.
- **No fact added or dropped.** Compile chooses words, order, prominence, the Player
  Summary and the Referee Notes. A fact that does not fit is a reroll of the row, never a
  quiet omission.
- **One location, its own rows only.** The sibling doctrine holds here unchanged.
- Instruction 2's 30-word Feature ceiling holds. Because cells are already terse facts,
  the bloat seen in E7 has no raw material to come from. Compile translates; it does not
  elaborate.

---

## 10. Validation and checks

`tools/validate_setting.py` adds (format is strict, ratios are relaxed, per `CLAUDE.md`):

- **Errors**: malformed record; unknown row id or location code in a foreign key;
  duplicate row id; a table a rating does not produce; an `Exits` row disagreeing with its
  diagram edge in existence, kind or direction; one edge with two `Exits` rows; a
  `Realized:` label absent from its location file.
- **Warnings**: an unfilled stub (with the step it is owed to); a filled location file
  with an unrealized row; a Feature tracing to no row (heuristic, by label); the
  distinctness rules made checkable by tables: a purpose repeated within a block (from
  `dangerous/Dressing.md`'s Constraint); one exit description across more than a third of
  a block's exits (`dangerous/Door.md`); two hazards in one block sharing mechanism and
  clue category.
- `--pending [REGION]` lists stubs owed per step, including connected stubs waiting on
  another region (D6).
- The read-set graph (`--read-set`) resolves the new steps through their templates to the
  pattern files, as now.

`tools/metrics.py` reports per table: rows, fill state, rate asked against rate realized,
and words per cell.

**Judgement checks.** `templates/Setting_Judgement_Check.md` gains two items: *rows
written in one pass read as a form* (F2's watch), and *rooms read as one room* (F1's
watch). "Draws realized at their rates" is answered from the allocation report rather
than by hand counting.

---

## 11. Documentation changes, by the rules in `CLAUDE.md`

- `STEPS.md`: phase 4 replaced per 8.2. It is the authority, so it is changed first and
  the rest points at it.
- `patterns/SPEC.md`: the table test (section 6) as a new section; "What a spec line owes"
  keeps the Feature as the unit of content; the paragraph that flags `dangerous/Key.md`
  as two files is resolved by the test and cut back to a pointer.
- `CLAUDE.md`: one line under Pattern file rules pointing at the test. Nothing else; the
  rule lives in `SPEC.md`.
- `README.md`: the directory map gains `tables/`, and the command list gains
  `tables.py`. The `context.py 4c` line goes when the sheet does.
- Pattern files: only step-id citations move (`dangerous/Key.md`, `dangerous/Lore.md`,
  `wild/Lore.md`, `SPEC.md`). "Nothing is owed at the close of 4c" becomes "at the close
  of 4d" (allocation creates every obligation).
- Templates: new `Location_Weights.md`, `Allocation.md`, and one `Table_[Name].md` per
  table; rewritten Context for `Location_Gazetteer.md`, `Location.md` and the five
  registry templates; step-id moves elsewhere.
- No passage gets refreshed to describe the new pipeline. Where a passage restated the
  old one, it is cut back to a pointer.

---

## 12. Acceptance

The change is done when a pilot build (one SAFE, one WILD, one DANGEROUS region from
`BRIEF.md`) runs through 4a-4j and 5c, and:

1. The validator reports no errors, and no warnings beyond intentionally unbuilt regions.
2. The allocation report shows every rated line within the template tolerance at region
   scale, or names the deliberate reroll that moved it (E2).
3. Every edge has exactly one `Exits` row and one gate draw (E3).
4. The `Creatures` headcount reconciles with each Overview's Inhabitants (E4).
5. The E5 regressions (MEDIUM encounter never absent; no FAMILY on a household block) pass
   as checks.
6. Every row is realized in exactly one location file, and no Feature lacks a row.
7. The 5c judgement check's "Rooms are distinct" item finds fewer near-repeats than the
   second-run addendum at 9c1354b on comparable blocks, and "rooms read as one room" is
   Confirmed.
8. `context.py cost` (extended) reports the table strategy's cost next to the old one,
   and the user accepts the difference.
