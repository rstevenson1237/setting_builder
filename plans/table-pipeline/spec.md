# Spec - table-driven location generation

The request, its follow-up and the user's decisions are in `intake.md`. This file gives
the analysis (sections 1-3), records the decisions (section 5), works through the table
format (section 6, the one decision still open), and then sets out the design that
follows.

Three ideas run through the whole design:

- **Patterns specify rows; templates own tables** (D2). A pattern file says what one row
  holds. A table template (`templates/Table_Creatures.md`) says which locations get a row, how
  many and in what mix, and it holds the region's table.
- **Storage and passes are separate.** One file per table is the storage. A pass is a unit
  of work: it can fill one table (every creature in a region) or cut across several (one
  coordinated build across five rooms).
- **Hand first, tools after** (D8). The pilot runs without `draw.py` or `context.py`. An
  analysis decides what comes back. The validator stays, because it is the lint.

---

## 1. Analysis - the pipeline today

Phase 4 today: 4a gazetteer, 4b diagrams, 4c one location at a time from
`context.py 4c`'s sheet with registry stubs added as Features call for them, and 4d
registry entries. The doctrine is "write each location from those alone, never from its
sibling rooms".

What the last two validation runs found (commit 9c1354b, `SettingJudgementCheck.md` and
its two addenda):

| # | Finding | Why the current shape produces it |
|---|---|---|
| E1 | Near-repeats no single writer can see: one hazard shape six times, then three; pitch-sealed containers four times; alarm cords seven times | Each location is written blind to its siblings |
| E2 | Rates not realized at region scale: no second name in 30 rooms against 20%; edges about 94% open against 60%; 29 of 34 treasures a table roll against 55% | Rates are settled per location; nothing reads the region total |
| E3 | Gates on 43% of exit-ends; 7 warded doors in 22 rooms | Each end of an edge draws its own gate |
| E4 | A household of "about ten" shows up as one creature in its block | Nothing sums creatures against the Overview's Inhabitants |
| E5 | MEDIUM "never absent" overridden; household blocks drawing a FAMILY | `context.py` resolution bugs, invisible because no sheet is compared to another |
| E6 | Key, Lore and Quest obligations tracked by hand | Connected content is discovered while writing |
| E7 | A 173-word Feature; 22 rooms growing from 3,129 to 10,603 words | The writer is handed raw material and decisions together, and pours it all in |
| E8 | Two blocks differing in dressing but not in skeleton | Block-level distinctness has nowhere to be checked |
| E9 | No multi-room puzzle anywhere; `STYLE.md`'s "what opens it is met outside this location" is met only by Keys | A location-at-a-time writer cannot place the far half of anything |

Every finding except E5 and E7 is about many rows or many rooms at once.

---

## 2. Alternatives (settled)

A1 (status quo plus checks), A2 (allocation tables only), A3 (full table pipeline) and A4
(tables as the product, no compile) were weighed in the first draft. **A3, run by hand
first**, is the chosen route (D8). A2 stays available as a fallback, if the analysis finds
the fill passes not worth their cost.

---

## 3. Friction points

Each is stated with its resolution in this design. Points that the decisions settled
outright are listed only by their resolution.

**F1 - Room coherence with standalone rows.** Rows are written without the room around
them ("there is an orc here, named x, reacts y, wants z"). *Resolution:* compile reads all
of a room's rows and makes them one room. It may not add or drop a fact, and a row that
cannot share the room goes back to its pass. The pilot measures how often this happens.

**F2 - The sibling doctrine is reversed.** A table pass shows every sibling of one type.
*Resolution:* compile still writes each room from its own rows only. Inside a table pass,
seeing every sibling is how E1 and E8 are prevented. Under D5, all of a table's clues sit
in one column, so a repeat is visible at a glance. 5c gains an item for passes that read
as a form.

**F3 - Step renumbering.** *Resolved by D1:* phase 4 is renumbered.

**F4 - Single authority.** *Resolved by D2:* the pattern is the row spec, and the table
template never lists columns. Under D5 the columns are the pattern's Spec lines, one each
(section 7).

**F5 - Weight fails the table test.** It is a value. *Resolution:* it is a column of
`Locations.md`'s `Location` section, created empty at 4a and filled at 4b.

**F6 - Region tables against setting registries.** *Resolution:* the setting registries
stay the table for anything with an identity beyond one placement. A region row holds the
placement and a foreign key to the registry.

**F7 - Compile writes facts twice.** *Resolved by D4:* cells are tags and glosses, and
there is no prose to copy. Compile writes the sentences.

**F8 - Cost.** *Resolution:* the pilot log records every pass's read set and size; the
analysis costs it.

**F9 - Cross-references.** *Resolution:* references are foreign-key cells. A pass reads
the rows its rows name.

**F10 - Naming last, names used early.** *Resolution:* tables key by code. The naming pass
updates `Locations.md`, and the name sync updates diagram labels and registry lines.

**F11 - Tool bugs at scale.** *Resolution:* deferred. E5 is fixed before `context.py`'s
walk is reused for anything.

**F12 - Changes ripple.** *Resolution:* a pass that changes a filled row re-reads every
row naming it. Retrofit (10.2) is the same rule seen from the room.

**F13 - Tables in the region folder** (D3). The validator treats every `*.md` in a region
folder except `Locations.md` as a location file, and errors on extras. *Resolution:* its
glob narrows to `[0-9]*.md`, a one-line change made in phase 1. `metrics.py` and
`context.py` already glob that way. Table names must never collide with a block's
`.mmd` name, which can't happen since the extensions differ.

**F14 - SAFE and WILD access.** *Resolution:* WILD access is a section of `Exits.md`
holding only the hidden and secret parent→child edges (section 6), which retires the
Landmark → Hidden → Secret write order.

**F15 - `Locations.md` changes format.** Under D5 it becomes pipe tables. Today the
validator and `site_common` parse it line by line, and the validator errors on any line
that isn't a gazetteer line. *Resolution:* both parsers read the `Location` section
instead. It is a small, mechanical change in phase 1, keeping the lint and the site
builder working, and it is not a generator rewire.

**F16 - Coordinated builds against "never two triggers deep".** *Resolution:* the rule
stays per room. Each link's clue is obvious in its own room, or one trigger from obvious
there. What carries the chain between rooms is something the party holds or knows, which
is exactly what `STYLE.md`'s clue/answer rule asks for (E9).

**F17 - A coordinated build against room classes.** A part in a LOW room can turn it
MEDIUM. *Resolution:* parts fill stubs the room's class allocated. A part beyond that is a
named exception in the composition entry, with its reason, and the pilot counts them.

**F18 - Retrofit against an authored compile.** *Resolution:* targeted recompile from the
`Realized` column (10.2).

**F19 - Hand allocation and rate collapse.** *Resolution:* accepted as the experiment.
Every rated decision is logged, and `draw.py` returns for allocation only if the analysis
shows the collapse E2 showed.

**F20 - Spec lines need column labels, and some ask several things** (from D4 and D5). A
gloss holds at most six words, and a pipe column needs a label. Many Spec lines already
open with one (`Clue -`, `Tier -`, `Trigger -`), some don't ("What it is doing when the
party arrives"), and some ask two or three things at once. For example, Treasure's
Container line asks what it is in, what that is made of, whether it moves, and what
reaches it. *Resolution:* `patterns/SPEC.md` gains two rules. Every Spec line opens with
a short column label, unique within the file its section lands in. A line that cannot be
answered in one tag or one gloss is several lines, and splits. This is the "pathways
change, content largely resembles" migration D2 anticipates. It is listed per file in
implementation T1.3.

**F21 - The Region Overview grows after 3c** (from D7). Compositions are designed at 4e,
but the Overview is written at 3c. *Resolution:* the new field is written at 4e (and
again on any retrofit). `templates/Region.md` already treats Overview claims as promises
audited at 5c, so a field filled later is checked the same way. "Never a fact of the
Overview restated in a room" holds, because the entry states the chain (which part
unlocks which, by row id) and the rooms state the parts.

---

## 4. Goals and non-goals

**Goals**
- Every unit a location contains exists as a row, before any prose, with every reference
  set.
- A pass can fill one table with every row in view (E1, E8), or write a coordinated build
  across rooms in one go (E9), and both are validated.
- A table pass reads only its stubs and the roster it draws from.
- The to-do list is mechanical: an unfilled cell is a warning naming the step it is owed
  to (D6).
- Retrofit is a targeted diff.
- Location files keep `templates/Location.md`'s output shape.
- One firm, decidable test places every Spec line as a column, a section or a file.
- Tools are rebuilt only where the pilot shows the need.

**Non-goals**
- Changing phases 1-3, `STYLE.md`, `GENRE.md` or `BRIEF.md`, except the one new Overview
  field (D7).
- Changing what patterns ask, beyond labelling and splitting lines (F20) and moving step
  citations.
- Reformatting the setting registries, whose full entries are prose. They keep today's
  format.
- Rendering tables on the site.

---

## 5. Decisions

| # | Decision | Settled as |
|---|---|---|
| D1 | Step ids | **Renumber phase 4**, explicitly authorised |
| D2 | What "supersede the patterns" means | **A pattern specifies one row; the table template owns the table**: which locations, how many, in what mix. Pattern content largely stays; pathways change |
| D3 | Where tables live | **`setting/region/[Code]/`**, next to `Locations.md` |
| D4 | What a cell holds | **A tag** (1-2 categorizing words) **or a gloss** (at most 6 terse words). Compile writes the prose, records `Realized`, and recompiles in a targeted way on retrofit |
| D5 | Table format | **Recommended, awaiting confirmation: strict pipe tables, one section per pattern file** (section 6) |
| D6 | Connected stubs | **Filled in their own pass (4h)**, as 4d is today; every unfilled cell is a validator warning naming its step |
| D7 | Coordinated builds | **No table; a `Compositions` field in the Region Overview** whose entries name their part rows |
| D8 | Hand first | **Yes** |

---

## 6. D5 - table format, and the test it settles

### 6.1 The question

The user's framing: one `Hazards.md` where each line decides whether it carries trap,
environmental or residual detail, or a table per mechanism, possibly in the same file.
Behind it sits the general question, strict columns against flexible entries, and the
answer decides the shape of every table in the pipeline.

What the three mechanism files actually ask (`dangerous/Trap.md`, `Environmental.md`,
`Residual.md`): each has four to seven lines. Two labels recur in all three (Trigger,
Damage), but with different draws and qualifiers. The rest are their own (a Trap's setter,
an Environmental's course and threshold, a Residual's maker and what it protects). Every
hazard shares one set of lines (`dangerous/Hazard.md`: mechanism, clue, tier, already
caught), and each has exactly one of three different sets on top.

### 6.2 Options

| | Option | Shape |
|---|---|---|
| a | One wide pipe table | Every hazard row carries Hazard's columns plus the union of all three mechanisms' columns; the ones that don't apply are marked n/a |
| **b** | **One file, one strict pipe table per pattern file** | `Hazards.md` holds a `## Hazard` section (every hazard) and `## Trap`, `## Environmental`, `## Residual` sections, each holding only the hazards whose mechanism picked it, keyed by the same row id |
| c | One file per mechanism | `Traps.md`, `Environmentals.md`, `Residuals.md`, plus a `Hazards.md` for the shared lines or with them repeated |
| d | Flexible records | One entry per hazard, carrying whichever fields its mechanism needs, in `Field: value` lines |

### 6.3 Criteria

| Criterion | a | **b** | c | d |
|---|---|---|---|---|
| **Completeness is mechanical**: every cell filled, `none`, or visibly owed | partly: n/a muddies `none` | **yes**: no n/a cell can exist | yes | no: a missing field and a field not needed look the same |
| **Distinctness is visible** (E1): all clues in one column | yes | **yes**: the `Hazard` section has every clue in one column | no: clues are split across files | no: scattered through records |
| **One pattern file maps to one place** (D2) | no: three patterns folded into one row | **yes**: one pattern, one section | yes | no |
| **Readable under D4** (cells of 6 words or fewer) | no: about 25 columns wide | **yes**: 5-8 columns per section | yes | yes |
| **Progressive building and retrofit diffs** | adding a row touches one line | **adding a row touches one line per section it enters** | the same, across files | adding a row adds several lines |
| **Parse and validate** | trivial | **trivial**: header defines the columns, and every row must match | trivial | needs a per-pattern field schema |
| **Rendering on GitHub** | an unreadable grid | **readable grids** | readable grids | text |

**Recommendation: (b).** The first draft preferred flexible records because cells were
going to be long. D4 removed that objection: at six words a cell, pipe tables are compact
and render as grids. Strictness then buys the two things this change exists for:
**completeness without judgement** (D6's warnings become "this cell is empty") and
**distinctness at a glance** (one column holds every clue in the region). Option (a)
gets the strictness but loses one-pattern-one-place and readability. Option (c) loses the
all-hazards view that E1 needs. Option (d) loses both strictness payoffs.

**The answer to the user's question: one `Hazards.md`, holding a table per pattern file.**
Every hazard has a row in `## Hazard`, and exactly one row in whichever mechanism section
its `Mechanism` cell names.

### 6.4 Worked example

Content here is illustrative, to show the shape; it is not a pattern.

```
# Hazards of C The Ravine

## Hazard
| ID  | Location | Mechanism     | Tier      | Clue                        | Searcher's clue      | Caught         | Realized        |
|-----|----------|---------------|-----------|-----------------------------|----------------------|----------------|-----------------|
| HZ1 | C.14     | trap          | damaging  | slack wire across threshold | oil at the hinge     | none           | Threshold Wire  |
| HZ2 | C.18     | environmental | nuisance  | dark sheen on flags         | none                 | rat mid-band   | Silt Floor      |
| HZ3 | C.31     | residual      | lethal    |                             |                      |                |                 |

## Trap
| ID  | Parts               | Trigger     | Damage      | Set by              |
|-----|---------------------|-------------|-------------|---------------------|
| HZ1 | weighted spear rack | wire pulled | 2d Piercing | Gorzgur, maintained |

## Environmental
| ID  | Kind    | Condition              | Cause       | Course    | Threshold      | Damage      | Untouched spot |
|-----|---------|------------------------|-------------|-----------|----------------|-------------|----------------|
| HZ2 | footing | silt film over flags   | sluice seep | worsening | moving quickly | 1d Crushing | none           |

## Residual
| ID  | Maker | Doing | Course | Edge | Damage | Protects |
|-----|-------|-------|--------|------|--------|----------|
| HZ3 |       |       |        |      |        |          |
```

What the example shows:
- **Three cell states, and no fourth.** A filled cell; `none`, where a rated line was not
  taken (HZ1's Caught, HZ2's Untouched spot); and empty, meaning owed. HZ3 is a stub: its
  location and mechanism were decided at allocation (4d), and everything else is owed to
  4f. There is no n/a, because a column that doesn't apply to a row lives in a section that
  row isn't in.
- **The compound line splits** (F20). `dangerous/Hazard.md`'s Clue line ("one anyone
  entering would notice, and where it can, a second only a searcher finds") is two
  columns.
- **Labels are unique per file.** Trap's own "Mechanism" line becomes `Parts`, so it
  doesn't collide with Hazard's `Mechanism`.
- **The pairing is checkable.** Every `## Hazard` row has exactly one row in the section
  its Mechanism names, and every mechanism-section row has its `## Hazard` row.

### 6.5 The table test, three-way

D5 sharpens the two-condition test into a rule that places every Spec line in exactly one
of three homes. It goes into `patterns/SPEC.md` beside "A draw or an edge is decided by
what the pick opens", which it extends.

> **For each unit and each line that draws it:**
>
> 1. **Opens no lines** (a question, or a `{draw}` item) → a **column** of the drawing
>    row's section. A question's cell is a gloss; a draw's cell is a tag. A rated line's
>    cell may be `none`.
> 2. **Opens lines, exactly one per drawing row** → a **section** in the drawing row's
>    file, rows keyed by the drawing row's id. Where a kind draw picks among several such
>    units, each gets its own section, holding only the rows that picked it.
> 3. **Opens lines, and not exactly one per drawing row** (can be absent, can be several,
>    or one shared by several rows) → its **own file**, whose rows carry a foreign-key
>    column naming the drawing row or rows.
>
> **One unit, one home**: if any drawer sends a unit to rule 3, every drawer references
> that file. **One pattern file, one section**, always: a file's first section is its own
> unit's pattern, and its other sections are the patterns rule 2 brought into it.

Corollaries:
- **Shared means connected.** A rule-3 unit shared by two locations is a connected stub,
  filled at 4h (D6). So is a column naming another location.
- **A step or a pass is not a table.** Either may fill columns or sections that already
  exist.
- **Columns exist from creation.** A table is created with every column its sections owe,
  with the cells empty. Later passes fill cells and never add a column, so no pass
  rewrites another pass's lines.
- **Many values in one cell.** A draw saying "at least one" gets a comma-separated tag
  list in one cell. A line rated `2` gets numbered columns (`Detail 1`, `Detail 2`).

### 6.6 The test applied

| Unit | Drawn by | Rule | Home |
|---|---|---|---|
| Weight / classification / prominence | location | 1 | column of `Locations.md` § Location |
| `dangerous/Dressing.md` | every class file, at `1` | 2 | `Locations.md` § Dressing |
| Class file's own lines (HIGH's architecture, 50% ambiance) | location | 2, by weight | `Locations.md` § High / § Medium / § Low |
| WILD / SAFE kind files (`wild/Ruin.md`, `safe/Commerce.md`, ...) | class file's Kind | 2, kind | `Locations.md` § per kind |
| Naming | every class file | 2 | `Locations.md` § Naming |
| Concealed detail (Clue / Trigger / Payload) | class files, rated | 3 | `Secrets.md` |
| `dangerous/Door.md` | every exit | 3 (two locations) | `Exits.md` § Door, one row per edge |
| WILD access | hidden / secret parent→child edge | 2, kind | `Exits.md` § Access |
| Key demand (lock) | a gated exit or mystery | 2 | § Lock in `Exits.md` / `Mysteries.md` |
| `dangerous/Encounter.md` | challenge, treasure guard | 3 | `Encounters.md` § Encounter |
| `dangerous/Faction.md` | encounter kind | 2, kind | `Encounters.md` § Faction |
| `dangerous/Creature.md` | encounter (1), treasure (25%) | 3, via treasure | `Creatures.md`; encounters hold a foreign key |
| `dangerous/Hazard.md` | challenge, treasure, gate | 3 | `Hazards.md` § Hazard |
| `Trap.md` / `Environmental.md` / `Residual.md` | hazard mechanism | 2, kind | `Hazards.md` § Trap / § Environmental / § Residual |
| `dangerous/Mystery.md` | challenge, HIGH 30%, ward | 3 | `Mysteries.md` |
| `dangerous/Treasure.md` | class files | 3 | `Treasures.md` § Treasure |
| `dangerous/Lore.md`, `Key.md` supply, `Quest.md` | treasure kind, payload | 2, kind | § Lore / § Key / § Quest in the drawing file, plus a registry foreign key |
| Setting registries | placements | 3 (shared) | existing `setting/*.md`, format unchanged |
| Foreshadowing detail | MEDIUM 25%, LOW 10% | 1, connected | column of `Locations.md` § Medium / § Low, plus a target column |
| `safe/People.md` as gate | every SAFE location | 3 (one person, several places) | the Overview's People roster; per-visit lines as columns of § Settlement |
| Coordinated build | a composition pass | (D7) | the Overview's `Compositions` field |

Implementation T1.2 completes this over every Spec line in `patterns/`, by hand.

---

## 7. From Spec line to column

Under D2 and D5, a pattern's Spec block *is* the column list. The table template never
repeats it. The mapping is mechanical:

| Spec line | Becomes |
|---|---|
| a question | a gloss column, named by the line's label |
| a `{draw}` | a tag column, named by the line's label; the cell is one item, or a list where the line says "at least one" |
| a rated line (under `1`) | its column, whose cell may be `none` |
| an edge, rule 2 | a section in this file (plus, for a kind draw, the tag column that picks it) |
| an edge, rule 3 | a foreign-key column naming rows in the other file; the other file's rows are created by allocation |
| a `{NAMED}` draw block | no column of its own; it is the vocabulary of the column whose line names it |

Every section also carries `ID` first (or `Code`, in `Locations.md`) and, where it is a
file's first section, `Location` (or the two location columns, in `Exits.md`) and
`Realized` last.

---

## 8. Inventory, by rating

Files sit in `setting/region/[Code]/` (D3). Sections per 6.6.

| File | First section's pattern | DANGEROUS | WILD | SAFE |
|---|---|:-:|:-:|:-:|
| `Locations.md` | the gazetteer row (code, name, tags, weight, block) | ✓ | ✓ | ✓ |
| `Exits.md` | `dangerous/Door.md`, or the `Dressing.md` exit line | ✓ | ✓ | ✓ |
| `Secrets.md` | the class files' concealed-detail lines | ✓ | ✓ | ✓ |
| `Encounters.md` | `dangerous/Encounter.md` | ✓ | | |
| `Creatures.md` | `*/Creature.md` | ✓ | ✓ | |
| `Hazards.md` | `*/Hazard.md` | ✓ | ✓ | |
| `Mysteries.md` | `*/Mystery.md` | ✓ | ✓ | |
| `Treasures.md` | `*/Treasure.md` | ✓ | ✓ | |
| `Factions.md` | `wild/Faction.md`, `safe/Faction.md` | | ✓ | ✓ |
| `Situations.md` | `safe/Situation.md` | | | ✓ |

The connection diagrams stay as they are. `Exits.md` adds what an edge physically is, and
must agree with its diagram edge.

---

## 9. The pipeline

### 9.1 Steps (D1)

| Id | Was | Step | Template | Writes |
|---|---|---|---|---|
| 4a | 4a | **Gazetteer**: names and tags | `Location_Gazetteer.md` | `Locations.md` § Location, Weight column empty |
| 4b | (in 4a) | **Weights**: DANGEROUS weight, WILD classification, SAFE prominence | `Location_Weights.md` (new) | the Weight column |
| 4c | 4b | **Connections**: unchanged | `Region_Connections.mmd`, `Block_Connections.mmd` | `*.mmd` |
| 4d | (in 4c) | **Allocation**: every file and section created with its columns. Every row the class files decide is created as a stub, carrying its location and its allocated tags (a MEDIUM's challenge as an `Encounters` or `Hazards` row; a hazard's mechanism, with its empty mechanism-section row). One `Exits` row per edge, gate decided once. Registry stubs where a line requires both ends. By hand in the pilot, every rated decision logged. *Every allocated row exists after this step* | `Allocation.md` (new) | every table, as stubs |
| 4e | (new) | **Compositions**: optional and repeatable; claims stubs first, authors exceptions, writes its parts, and writes its Overview entry. After 4i, it is a retrofit | `Composition.md` (new) | part rows; the Overview's `Compositions` field |
| 4f | (in 4c) | **Table passes**: one per file, filling every unclaimed, unconnected row | `Table_[File].md`, one per file (new) | each table |
| 4g | (in 4c) | **Naming**: § Naming, then the name sync | `Location_Gazetteer.md`, naming section | `Locations.md`; `.mmd` labels; registry lines |
| 4h | 4d | **Connected fill** (D6): every connected stub (exits, locks, foreshadowing), then every registry's full entry | `Table_Exits.md`; registry templates | the rest |
| 4i | (in 4c) | **Compile**: one `[N].md` per location | `Location.md` | `[N].md`; `Realized` cells |
| 4j | 4d (tail) | **Coinage and mechanics** | `Language.md`, `Procedures.md` | as today |

Table templates are named `templates/Table_[File].md` (`templates/Table_Creatures.md`
holds the region's `Creatures.md`). The prefix keeps them together, and keeps them clear
of setting-level templates with near names (`templates/Treasure.md`,
`templates/Factions.md`). `Locations.md` keeps `templates/Location_Gazetteer.md`, which
grows its section list.

### 9.2 Order within 4f

A row is filled after the rows it names: `Creatures` → `Encounters` → (`Hazards`,
`Mysteries`) → `Treasures` (which name their guards) → `Secrets` (whose Payload may name a
treasure). `Locations.md` § Dressing can come any time before compile.

### 9.3 Read set of a table pass (standalone rows)

| Pass | Reads, besides `GENRE.md`, `STYLE.md`, `BRIEF.md` and its pattern |
|---|---|
| Creatures / Encounters | the Overview's Inhabitants; the `Bestiary.md` and `Factions.md` entries they name; this file's stub rows |
| Hazards / Mysteries | the Overview's Conditions; `Procedures.md` for damage; this file's stubs; the `Exits.md` rows they name |
| Treasures | the Overview's Loot; the Treasure tables' headings; this file's stubs; the guard rows they name |
| Secrets | this file's stubs; the rows a Payload names |
| Dressing | the Overview's Conditions and Places; `Locations.md` § Location |

A stub row carries its location code, and § Location gives that location's name, weight
and tags. That is the user's "which rooms have a weight that calls for a creature", and it
is all a pass sees of a room.

### 9.4 Connected stubs and the to-do list (D6)

A stub is a row with empty cells. The validator warns once per row, naming its file, its
id, its empty columns, and the step they are owed to (read off which section and file
they sit in). A feature pass that creates a stub in another file (a treasure pass turning
up a key, which owes a Keys stub and a § Lock row on some exit) adds those rows, and they
appear in the warnings immediately. `--pending [REGION]` prints the same list grouped by
step. The to-do list is never kept by hand.

### 9.5 Compositions (D7)

A new field in each `patterns/region/*.md` Spec and in `templates/Region.md`, written at
4e:

```
Compositions:
- [Name] - [row ids, in the order met]; [chain: what is held or known -> where it is
  used -> what it yields, link by link]; way round: [the answer that is not the gate,
  and its price]; exceptions: [part ids beyond their room's class, with reasons, or none]
```

A build spanning regions is entered once, in the Overview of the region holding its last
link. Others don't repeat it ("say a fact once").

**Proven correct** means every one of these holds, checked by hand in the pilot and by the
validator later where mechanical (⚙):

1. ⚙ Every id the entry names exists as a filled row.
2. ⚙ **Solvable from the entrance**: walking the diagrams from the region's entrance, each
   link's inputs are reachable using only what earlier links yield. No part sits behind
   the gate it opens, and the chain has no cycle.
3. Every link's clue is obvious in its own room, or one trigger from obvious there (F16).
4. ⚙ No link's clue and its answer share a room.
5. ⚙ Every part fills a stub its room's class allocated, or is listed under exceptions
   (F17).
6. The way round exists and is priced.
7. ⚙ Every part that is a key, lore, quest object, named creature or unique treasure has
   its registry row.
8. ⚙ After a retrofit, every part has a `Realized` cell present in its room's file.

---

## 10. Compile (4i)

### 10.1 First compile

`templates/Location.md` keeps its Template block, its Citations and its Feature grammar.
Its Context becomes: every row naming this location, across every file in the region
(assembled by hand in the pilot).

- **Every row is realized; nothing without a row is written.** The row's `Realized` cell
  gets the Feature label (or `Exits`, `Summary`, `Notes`) that carries it.
- **Cells become sentences.** Tags and glosses are notes, never copied verbatim as a
  Feature. Compile writes each Feature in the template's grammar from its cells, and adds
  no fact. A row that won't fit the room goes back to its pass.
- **One location, its own rows only.**
- The 30-word Feature ceiling holds. At six words a cell, E7's bloat has no material to
  come from.

### 10.2 Targeted recompile (retrofit)

When rows are added to or changed in a compiled room: each new row gets a new Feature line,
placed by prominence; each changed row's realized line is rewritten, and only that line;
the Player Summary and the Referee Notes are revisited only when a new or changed row is
obvious; every other line stays exactly as it was.

---

## 11. Validation

**In phase 1** (the lint, kept working; D8 does not cover it):
- the region-folder glob narrows to `[0-9]*.md` (F13);
- the gazetteer parsers (validator and `site_common`) read `Locations.md` § Location
  (F15);
- generic pipe-table parsing for every table file: an error where a row's cell count
  differs from its section header, or an id or code is unknown, and **a warning per stub
  row** (9.4). That is D6's test.

**In the pilot**, by hand from a checklist in the pilot log: pairing between a kind cell
and its section, one `Exits` row per diagram edge, the composition proof, and the
distinctness rules the column view makes visible (a purpose repeated in a block; one exit
description across more than a third of a block's exits; two hazards in a block sharing
mechanism and clue).

**After the analysis**, where called for: the checklist's mechanical items become
validator checks; `metrics.py` learns per-table counts and asked against realized.

**Judgement checks**: the setting check gains *rows written in one pass read as a form*
(F2), *rooms read as one room* (F1), and *each composition is solvable and priced*.

---

## 12. Analysis after the pilot

Written to `plans/table-pipeline/analysis.md`, from the pilot log and 5c:

| Question | If the answer is no |
|---|---|
| Did hand allocation hold the rates at region scale (against E2's figures)? | `draw.py` returns for 4d |
| Did the standalone read sets carry enough? (rows compile sent back, and why) | add the narrowest missing input to that pass |
| Was assembling read sets by hand cheap enough? | rebuild `context.py` as a collector for 9.3 and compile |
| Were the hand checklist items reliable? | each missed item becomes a validator check |
| Did compositions stay inside the weights? (exception count) | compositions move before 4b for the rooms they claim |
| Did retrofits stay targeted? (lines changed per retrofit) | revisit D4 |
| Did six-word cells hold every line? (lines that wouldn't fit) | split the line further, never widen the cell |
| Did table passes beat E1 / E8? (5c against 9c1354b) | the core claim fails: fall back to A2 |

---

## 13. Documentation changes, by the rules in `CLAUDE.md`

- `STEPS.md`: phase 4 replaced per 9.1, first.
- `patterns/SPEC.md`: the three-way test (6.5), the line-to-column mapping (7), the label
  and split rules (F20); the `dangerous/Key.md` paragraph cut back to a pointer.
- Pattern files: labels added and compound lines split (F20); step citations moved.
- `patterns/region/*.md` and `templates/Region.md`: the `Compositions` field (D7).
- `CLAUDE.md`: one line under Pattern file rules, pointing at the test.
- `README.md`: the region folder's entry names its table files; tool lines change only
  when the tools do.
- Templates: `Location_Weights.md`, `Allocation.md`, `Composition.md`, one `Table_[File].md`
  per file; rewritten Context for `Location_Gazetteer.md`, `Location.md`, the registry
  templates.
- No passage is refreshed to describe the new pipeline; a passage that restated the old
  one is cut back to a pointer.

---

## 14. Acceptance

A pilot build (the keep, the borderland, the ravine and at least two caves from
`BRIEF.md`) runs through 4a-4j and 5c by hand, and:

1. The validator reports no errors, and no stub warnings at the end.
2. Every rated line is within the template's tolerance at region scale, or the log names
   the deliberate choice (E2).
3. Every edge has one `Exits` row and one gate decision (E3).
4. The creature count reconciles with each Overview's Inhabitants (E4).
5. Every row is realized in exactly one location file; no Feature lacks a row.
6. A composition spanning three or more rooms passes all eight proof items, and a second
   is applied as a retrofit, changing only the lines 10.2 allows.
7. The creatures pass runs from 9.3's read set alone.
8. 5c's "rooms are distinct" finds fewer near-repeats than at 9c1354b on comparable blocks,
   and "rooms read as one room" is Confirmed.
9. `analysis.md` answers every question in section 12.
