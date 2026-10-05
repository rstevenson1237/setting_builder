# Spec - table-driven location generation

The request and its follow-up are in `intake.md`. This file gives the analysis first (what
the current pipeline does, what has gone wrong with it, the alternatives, and the friction
points), then the design that follows from it. Decisions that need the user's sign-off are
collected in section 5. Everywhere else, the design states its recommended answer and goes
ahead with it.

Two ideas from the follow-up run through the whole design:

- **Storage and passes are separate.** Tables are storage: one file per feature type. A
  pass is a unit of work, defined by what it reads and which rows it writes. A pass can
  fill one table (every creature in a region) or cut across several (one coordinated
  puzzle spanning five rooms). Both are first-class.
- **Hand first, tools after.** The pilot runs without `draw.py` or `context.py`. What comes
  back is decided by an analysis of the pilot (section 11).

---

## 1. Analysis - the pipeline today

Phase 4 today, per `STEPS.md`:

| Step | Writes | Unit of work |
|---|---|---|
| 4a | `Locations.md` per region: name, weight/classification, three tags | region |
| 4b | connection diagrams (`Connections.mmd`, one `[Block].mmd` per DANGEROUS block) | region / block |
| 4c | one `[N].md` per location, from `tools/context.py 4c CODE`. Registry stubs are created as Features call for them | location (DANGEROUS: one block per context) |
| 4d | full registry entries (`Lore`, `Keys`, `Quests`, `NamedCreatures`, `UniqueTreasures`) | setting |

At 4c, everything about a location is decided and written in one pass, from a sheet that
`context.py` settles out of the class file. The doctrine is "write each location from
those alone, never from its sibling rooms".

### What the last two validation runs found

From commit 9c1354b, in its `SettingJudgementCheck.md` and the two addenda:

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
| E9 | No multi-room puzzle exists anywhere: every concealed detail resolves inside its own room or one exit away, and the clue/answer rule in `STYLE.md` ("what opens it is met outside this location") is met only by Keys | A location-at-a-time writer cannot place the far half of anything. The only cross-room device is a registry row, discovered mid-write |

E1-E4, E6, E8 and E9 are distribution or coordination problems: a property of many rows
or many rooms at once, invisible from inside any one of them.

---

## 2. Alternatives considered

| | Alternative | Gets | Misses | Cost |
|---|---|---|---|---|
| A1 | **Status quo plus checks**: keep 4c and add region-level validator and metrics checks | Detection of E1-E3 after the fact | Prevention, and E9 entirely | Low |
| A2 | **Allocation tables only**: every row is stubbed with its draws settled; locations are still written one at a time | E2-E6 by construction | E1, E8, E9 | Medium |
| A3 | **Full table pipeline**: stubs, then passes that fill rows, by table or by composition, then compile | E1-E9 | Room coherence, which compile has to carry (F1) | High |
| A4 | **Tables as the product**: no compile step; pages rendered from tables | No second writing pass | Summary and Notes must become columns; contradicts the request; every reader of `[N].md` breaks | High |

**Recommendation: A3, run by hand first.** The first draft of this spec planned to reach
A3 by building A2 as a tool. Following the user's follow-up, the order is now: run A3
completely by hand on a pilot, analyse the result, then build only the tools the analysis
calls for. This tests the shape before any code commits to it, and gives a measured answer
to whether the random draws and the context sheet still earn their place (F19, section 11).

---

## 3. Friction points

Each is stated with its resolution in this design. F1, F2, F4, F16 and F18 are the ones
that could sink the change.

**F1 - Room coherence.** `templates/Location.md` requires "one history per room". If rows
are written standalone, a hazard can end up in a room whose other rows it cannot share.
*Resolution (revised by the follow-up):* rows are deliberately standalone. A table pass
reads only its own stubs and the region-level roster it draws from (8.4), because "there
is an orc here, named x, reacts y, wants z" is complete without the room. Coherence is
compile's job: compile reads every row for one room, may adjust wording to make them one
room, and may not add or drop a fact. A row that cannot share its room goes back to its
pass, the same rule as a reroll today. *Watch:* if compile sends rows back too often in
the pilot, passes need a little more context. Measuring exactly how much is one of the
analysis questions (11).

**F2 - The sibling doctrine is reversed.** 4c says "never from its sibling rooms" because
writing against siblings converges. A table pass is built to show every sibling of one
type.
*Resolution:* the doctrine is narrowed rather than dropped. Compile still writes each
location from its own rows only. Inside a table pass, seeing every sibling is the
mechanism for E1 and E8: the writer is told to make rows distinct, and can see whether
they are. The 5c check gains an item for passes that read as a form.

**F3 - Step renumbering.** `README.md` says step ids are "never renumbered without explicit
user request"; the validator allows one letter suffix.
*Resolution:* Decision D1.

**F4 - "Supersede the patterns" against single authority.** A table spec that copies a
pattern's Spec lines is a second copy, and the copy is the one that drifts.
*Resolution:* Decision D2. Whichever way it goes, there is exactly one copy.

**F5 - Weight fails the table test.** Exactly one per location, opening no lines, so it is
a field.
*Resolution:* a step is not a table, and a pass is not a table either. Weighting fills a
column of `Locations.md`.

**F6 - Region tables against setting registries.** A key's two ends can sit in different
regions.
*Resolution:* anything with an identity beyond one placement keeps its setting registry
as its table. The region row holds the placement columns plus a foreign key to the
registry. This also settles the split `patterns/SPEC.md` already flags for
`dangerous/Key.md`.

**F7 - Compile writes facts twice.** If cells are prose and compile rewrites them, the two
copies drift.
*Resolution:* Decision D4. Cells are terse facts, compile owns the prose, and each row
records the Feature that realized it.

**F8 - Cost.** More passes per region.
*Resolution:* the pilot logs every pass's read set and size, and the analysis costs the
strategy against the old one before any tool is built.

**F9 - Cross-references between tables.** A treasure guarded by an encounter, a trap on a
gate, a Payload that changes what a challenge is worth.
*Resolution:* references are foreign keys, written at allocation where the class file
already decides them, and by the composition pass where it is the composition that
decides. A pass reads the rows its rows reference, and nothing more.

**F10 - Naming comes last, but names are used early.**
*Resolution:* tables key everything by code. Naming is a late column pass, and every
downstream mention of the name is synced from `Locations.md`. By hand in the pilot,
by tool later if called for.

**F11 - Tool bugs at scale.** E5's resolution bugs would be written into every table by an
allocation tool.
*Resolution:* deferred, because the pilot uses no tool. E5 is fixed, with regression
checks, before `context.py`'s walk is reused for anything (implementation phase 4).

**F12 - Changes ripple.** Changing a filled row (a treasure turning into a key) creates
obligations elsewhere and can strand content that references it.
*Resolution:* a filled row is changed only by a pass that lists every row referencing it,
and each referencing row is re-read in the same pass. Retrofit (9.2) is the same rule
seen from the room's side.

**F13 - Existing consumers of the region folder.** The validator treats every `*.md` in a
region folder except `Locations.md` as a location.
*Resolution:* tables live in `setting/region/[Code]/tables/` (D3).

**F14 - SAFE and WILD access fit unevenly.**
*Resolution:* the test handles both. WILD access is a column group on the parent→child
`Exits` row, stubbed from the diagram, which retires the Landmark → Hidden → Secret write
order. SAFE simply has fewer tables.

**F15 - Gazetteer purpose changes.** Under the test, `Locations.md` is the location table.
*Resolution:* each row's first line stays exactly as today, and column groups go on
indented lines under it.

**F16 - A coordinated puzzle against "never two triggers deep".** `templates/Location.md`
bars a clue reached only by acting on another clue. A multi-room chain is a sequence of
acts.
*Resolution:* the rule stays per room. Each link of a composition puts its clue in the
obvious tier of its own room, or one trigger from obvious in that room. What carries the
chain from room to room is something the party holds (an object taken, a name read, a
sequence watched), never a concealment nested inside another. This is what `STYLE.md`'s
clue/answer rule already asks for ("what opens it is met outside this location"), so
compositions are the device that rule was waiting for (E9).

**F17 - A composition against a room's class contract.** A composition that drops a hazard
into a LOW room turns it into a MEDIUM; one that adds a third treasure to a HIGH room
spends a budget the class never allocated.
*Resolution:* a composition part fills a stub the room's class already allocated
(a LOW room's concealed detail or treasure, a MEDIUM room's challenge) wherever one fits.
A part that exceeds the room's contract is allowed only as a named exception on the
composition row, with its reason. The exception count is an analysis measure: many
exceptions mean the composition is fighting the weights, and the weights should have
been set with it in mind.

**F18 - Retrofit against an authored compile.** If compile writes each room fresh as
prose, retrofitting a composition into five compiled rooms rewrites five rooms, including
prose already accepted.
*Resolution:* targeted recompile (9.2). The `Realized:` trace says which Feature line
each row became, so a retrofit adds lines for new rows and rewrites only the lines whose
rows changed. Summary and Notes are touched only when a new row is obvious-tier.

**F19 - Hand allocation and rate collapse.** E2 showed that judgement drifts toward the
average: rated lines fire when a room "feels thin". With no draw tool, the pilot's author
decides every rated line.
*Resolution:* accepted as the experiment. Every rated decision is logged with the rate it
answers, so the analysis can measure asked against realized at region scale. If hand
allocation collapses the way E2 did, `draw.py` comes back for allocation only. If the
table view lets the author hold the mix, it doesn't.

---

## 4. Goals and non-goals

**Goals**
- Every unit a location contains exists as a row in a per-type table before prose is
  written, with every cross-reference set.
- A pass can fill one table with every row of that type in view (E1, E8), or write a
  coordinated build across rooms and tables in one go (E9), and both are validated.
- Rows are standalone: a table pass reads only its stubs and the roster it draws from.
- Retrofit is cheap: new rows land in already-compiled rooms by targeted recompile.
- Location files keep `templates/Location.md`'s output shape.
- One firm, decidable test sorts every pattern into a field or its own table.
- Tools are rebuilt only where a hand-run pilot shows they are needed.

**Non-goals**
- Changing phases 1-3, `STYLE.md`, `GENRE.md` or `BRIEF.md`.
- Changing what any pattern file asks, except moving citations to retired step ids.
- Rendering tables on the site.

---

## 5. Decisions needing sign-off

| # | Decision | Recommended | Alternative |
|---|---|---|---|
| D1 | Step ids for the new phase 4 | **Renumber phase 4** (8.2). `README.md` requires the user's explicit request | Retire 4a-4d in place and append the new steps as 4e-4n |
| D2 | What "supersede the patterns" means | **Patterns stay the row spec.** A table template names its pattern, and its columns are that pattern's Spec lines, never copied. Tables supersede the class-file walk and the 4c sheet | Rewrite each table-bearing pattern file into table form. Still one copy, but every pattern file changes shape |
| D3 | Where tables live | **`setting/region/[Code]/tables/`**; a composition spanning regions goes in `setting/Compositions.md` | In the region folder, with every consumer's glob tightened |
| D4 | What a cell holds, and what compile does | **Cells are terse facts; compile writes the prose**, may not add or drop a fact, records `Realized:`, and recompiles in a targeted way on retrofit | Cells hold finished Feature sentences and compile assembles them. Retrofit is trivial, but coherence can no longer be fixed at compile |
| D5 | Row format | **Record blocks**: a first line matching today's gazetteer and registry style, then `Field: value` lines | Markdown pipe tables |
| D6 | Build order across regions | **Per region through the table passes; a connected stub is filled once every location it names has its rows** | Strict layer by layer |
| D7 | How a coordinated build is recorded | **As a row in a `Compositions` table** that owns the chain, with each part a row in its own type table carrying `Part of:`. This follows from the table test (it opens lines and is shared by several rows) | As a pass with no record: parts only. Cheaper, but the chain can no longer be validated or retrofitted as one thing |
| D8 | Hand first | **Yes**: the pilot runs with no `draw.py` and no `context.py`, every rated decision is logged, and section 11's analysis decides what comes back | Build the allocation tool first, as the first draft planned |

---

## 6. The table test

This goes into `patterns/SPEC.md`, beside "A draw or an edge is decided by what the pick
opens", which it extends, and into `CLAUDE.md`'s pattern rules as one line pointing there.

> **A unit gets its own table when, for at least one Spec line or pass that draws it,
> both hold:**
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
  that table's rows.
- **Shared means connected.** A unit shared by rows in two locations is stubbed naming
  every row it joins, and filled once those rows exist. A column naming another location
  (a foreshadowing detail, a lock) is connected in the same sense.
- **Parents are already tables.** The Region Overview and the block header each serve
  many locations.
- **A step or a pass is not a table.** Either may fill columns of an existing table.
- **The setting-level twin wins.** Where a unit has a placement pattern and a registry
  pattern, each is tested separately (F6).
- **A coordinated build is a table** (D7). It opens lines (its chain) and is shared by
  every row that is one of its parts. So it is a row in `Compositions`, and its parts are
  rows in their own tables.

### The test applied to the hard cases

| Unit | Drawn by | Opens lines? | Exactly one per drawer? | Result |
|---|---|---|---|---|
| Weight / classification / prominence | location | no | yes | column of `Locations` |
| `dangerous/Dressing.md` | every class file, at `1` | yes | yes | column group of `Locations` |
| HIGH's architecture detail, 50% ambiance | `dangerous/High.md` | no | - | columns of `Locations`, `none` when not taken |
| Concealed detail (Clue/Trigger/Payload) | class files, rated | yes (nested) | no | table `Secrets` |
| `dangerous/Door.md` | every exit | yes | no (two locations) | table `Exits`, one row per edge |
| WILD access | parent→child edge | yes | yes, per edge | column group of `Exits` |
| `dangerous/Encounter.md` | challenge, treasure guard | yes | no | table `Encounters` |
| `dangerous/Creature.md` | encounter (1), treasure (25%) | yes | no, via treasure | table `Creatures` |
| `dangerous/Faction.md` | encounter kind | yes | yes | column group of `Encounters` |
| `dangerous/Hazard.md` | challenge, treasure, gate | yes | no | table `Hazards` |
| `Trap.md` / `Environmental.md` / `Residual.md` | hazard mechanism | yes | yes | column groups of `Hazards` |
| `dangerous/Mystery.md` | challenge, HIGH 30%, ward | yes | no | table `Mysteries` |
| `dangerous/Treasure.md` | class files | yes | no | table `Treasures` |
| `dangerous/Lore.md`, `Key.md` supply, `Quest.md` | treasure kind, payload | yes | yes | columns of the drawing row, plus a registry key |
| `dangerous/Key.md` demand | lock obligation | yes | yes, per gated row | columns of the gated `Exits` / `Mysteries` row |
| Setting registries | placements | yes | no (shared) | existing `setting/*.md` registries |
| Foreshadowing detail | MEDIUM 25%, LOW 10% | no | - | column of `Locations`, connected |
| Naming, second name | class files | yes / no | yes / - | column group / column of `Locations` |
| `safe/People.md` as gate | every SAFE location | yes | no (one person, several places) | the Overview's People roster is the table; per-visit lines are columns |
| A coordinated puzzle | a composition pass | yes (its chain) | no (shared by its parts) | table `Compositions` |

The full inventory is this table completed over every Spec line in `patterns/`, by hand
in implementation T1.2.

---

## 7. Table inventory, by rating

Region tables, in `setting/region/[Code]/tables/`, except `Locations.md`, which stays where
it is.

| Table | Pattern (row spec) | DANGEROUS | WILD | SAFE |
|---|---|:-:|:-:|:-:|
| `Locations.md` (existing, grows columns) | class file + `Dressing.md` + `patterns/setting/Naming.md` (+ kind files as column groups) | ✓ | ✓ | ✓ |
| `Exits.md` | `dangerous/Door.md`; WILD/SAFE `Dressing.md` exit line; WILD access | ✓ | ✓ | ✓ |
| `Secrets.md` | concealed-detail lines of the class files | ✓ | ✓ | ✓ |
| `Encounters.md` | `dangerous/Encounter.md` (+ `Faction.md` columns) | ✓ | | |
| `Creatures.md` | `dangerous/Creature.md` / `wild/Creature.md` | ✓ | ✓ | |
| `Hazards.md` | `*/Hazard.md` (+ mechanism columns) | ✓ | ✓ | |
| `Mysteries.md` | `*/Mystery.md` | ✓ | ✓ | |
| `Treasures.md` | `*/Treasure.md` (+ placement columns) | ✓ | ✓ | |
| `Factions.md` | `wild/Faction.md`, `safe/Faction.md` | | ✓ | ✓ |
| `Situations.md` | `safe/Situation.md` | | | ✓ |
| `Compositions.md` | the composition contract (8.7) | ✓ | ✓ | ✓ |

Setting files: the five registries keep their roles, with stubs written at allocation or
by a composition pass instead of 4c. `setting/Compositions.md` holds any composition whose
parts span regions.

The composition contract needs a home in the pattern tree. Recommended: a new
`patterns/setting/Compositions.md`, a leaf whose Spec is the chain's lines (8.7), reached
from `patterns/Genre.md`'s SETTING block. It is setting-level because a composition's
parts can sit in any rating.

---

## 8. The pipeline

### 8.1 Table format (D5)

One record per row, blank line between records.

```
[Row ID] [Location Code(s)] - [what allocation decided]
  [Column]: [value]
  Part of: [Composition row id, where it is one]
  Realized: [Feature label in the location file, written at compile]
```

- **Row ID**: `[TABLE PREFIX][n]`, scoped to the region (`HZ3`, `TR12`, `EX7`, `CP2`),
  stable, never reused. In `Locations.md` the location code is the row id, and the first
  line stays today's gazetteer line.
- **Foreign key**: a cell naming another row by id, or a location by code. A registry key
  uses its existing citation form (`Keys: Title`).
- **Stub**: a first line plus foreign keys. **Filled**: every column its pattern requires
  answered, with nil written as `none`.
- **Provenance**: a row is either allocated (from a class file's line) or authored (by a
  composition pass, or as a named exception, per F17). The first line says which.

### 8.2 Steps (D1, recommended numbering)

| New id | Was | Step | Template | Writes |
|---|---|---|---|---|
| 4a | 4a | **Gazetteer**: names and tags | `Location_Gazetteer.md` (weight removed) | `Locations.md` first lines |
| 4b | (in 4a) | **Weights**: DANGEROUS weight, WILD classification, SAFE prominence, in the template's mix | `Location_Weights.md` (new) | `Locations.md` weight column |
| 4c | 4b | **Connections**: diagrams, unchanged | `Region_Connections.mmd`, `Block_Connections.mmd` | `*.mmd` |
| 4d | (in 4c) | **Allocation**: one pass over `Locations.md` and the class files. Every line the class file decides becomes a stub row in its table (a MEDIUM's challenge as an `Encounters` or `Hazards` stub, an edge as an `Exits` stub). Registry stubs where a line requires both ends. *Every allocated row in the region exists as a stub after this step.* By hand in the pilot, with every rated decision logged | `Allocation.md` (new) | all tables, as stubs; registry stubs |
| 4e | (new) | **Compositions**: optional and repeatable. Each pass designs one coordinated build, fills existing stubs where they fit, authors named exceptions where they don't, and writes the composition row. Can also run after 4i, as a retrofit | `Composition.md` (new) | `Compositions.md`; part rows in any table; registries |
| 4f | (in 4c) | **Table passes**: one pass per table, filling every stub not already claimed by a composition. Read set per 8.4 | `Table_[Name].md` (new, one per table) | each table |
| 4g | (in 4c) | **Naming**: the naming column pass, then the name sync | `Table_Locations.md` naming section | `Locations.md`; `.mmd` labels; registry lines |
| 4h | 4d | **Connected fill**: remaining connected stubs, then every registry's full entry | registry templates | remaining stubs; registries |
| 4i | (in 4c) | **Compile**: one `[N].md` per location from its rows (9) | `Location.md` (Context rewritten) | `[N].md`; each row's `Realized:` |
| 4j | 4d (tail) | **Coinage and mechanics**: as today | `Language.md`, `Procedures.md` | as today |

Compositions run before the table passes so they get first claim on the region's stubs.
The puzzle shapes the rooms; the rooms don't get bent around the puzzle afterward. Run
after compile, the same pass is a retrofit (9.2).

Phase 5 is unchanged except for step-id citations and the check items in section 10.

### 8.3 Order within the table passes

Rows are standalone, so the order only has to respect foreign keys: a row is filled after
the rows it references.

```
Creatures -> Encounters   (an encounter names its creature)
Encounters, Hazards -> Treasures   (a treasure names its guard)
Exits -> Hazards, Mysteries   (a trap on a gate, a ward)
Treasures, Exits -> Secrets   (a Payload may name either)
Locations substrate: any time before compile
```

### 8.4 Read set of a table pass (standalone rows)

The follow-up's rule: a pass knows the region-level facts it draws from and which rooms
call for its unit, and nothing else.

| Pass | Reads, besides `GENRE.md`, `STYLE.md`, `BRIEF.md` and its pattern |
|---|---|
| Creatures / Encounters | the Overview's Inhabitants; the `Bestiary.md` and `Factions.md` entries those name; this table's stubs (code, name, weight, tags) |
| Hazards / Mysteries | the Overview's Conditions; `Procedures.md` for forced damage; this table's stubs; the `Exits` rows its stubs name |
| Treasures | the Overview's Loot; the Treasure tables' headings; this table's stubs; the guard rows they name |
| Secrets | this table's stubs; the rows a Payload names |
| Exits | the diagrams; this table's stubs |
| Locations substrate | the Overview's Conditions and Places; `Locations.md` first lines |

No pass reads a location file or a table it doesn't reference. In the pilot the author
assembles these by hand. Whether a collector earns its way back is an analysis question.

### 8.5 Allocation (4d), by hand

Allocation turns weights into stubs, using the class file of each room. That is the list
the follow-up asks for ("which rooms have a weight that calls for a potential creature"):
after 4d, the `Encounters` and `Creatures` stubs *are* that list. The author:

- walks each room's class file and writes one stub per line it decides, choosing for each
  rated line and each `{draw}` against its rate, across the whole region at once;
- writes one `Exits` stub per diagram edge, with its gate decided once per edge (E3);
- counts what the region now holds against the Overview's Inhabitants (E4) and against
  each rated line (E2), and corrects before moving on;
- logs every rated decision as `rate asked → taken / not taken`, for the analysis.

### 8.6 Connected features

"Connected" means a row or column whose content depends on another location.

| Connected unit | Stub names | Filled at |
|---|---|---|
| Exit (every edge) | both locations, kind from the diagram, opening and gate | 4f `Exits`, or 4h when the far end is in another region not yet at 4f |
| WILD access | parent and child | 4f `Exits` |
| Lock (Key demand) | the gated row, the Keys stub | with the gated row |
| Foreshadowing detail | the room and the HIGH it points at | substrate pass, or 4h |
| Keys / Quests | both locations | placement at 4f; registry entry at 4h |
| Lore / Named Creature / Unique Treasure | every placing row | registry entry at 4h |
| Composition | every part row | in its own pass (4e), all at once |

### 8.7 Compositions (4e)

A composition is a coordinated build across rooms: clues, triggers, objects and
interactive features in several rooms, designed together and written in one pass. Its
row in `Compositions.md`:

```
CP[n] [every Location Code it touches] - [what it is, in a few words]
  Parts: [row ids, in the order a party meets them]
  Chain: [link by link: what the party holds or knows -> where it is used -> what it
          yields; every link names its part rows]
  Way round: [the answer that is not the gate, and its price]
  Exceptions: [parts beyond their room's contract, each with its reason, or none]
  Retrofit: [compiled rooms this pass changed, or none]
```

**Proven correct** means every one of these holds, checked by hand in the pilot and by
the validator later where it can be mechanized (marked ⚙):

1. ⚙ Every part is a row in its own table, carrying `Part of:`, and every row id in
   `Parts` and `Chain` exists.
2. ⚙ **Solvable from the entrance.** Walking the region's diagrams from its entrance,
   every link's inputs can be reached using only what earlier links yield. No part sits
   behind the gate it opens, and the dependency graph has no cycle.
3. Every link's clue is obvious-tier in its own room, or one trigger from obvious in that
   room. Never two triggers deep inside one room (F16).
4. ⚙ No link's clue and its answer sit in the same room (`STYLE.md`'s clue/answer rule).
5. ⚙ Every part fills a stub its room's class allocated, or is listed in `Exceptions`
   (F17).
6. The gate the composition builds has a `Way round` that is priced (`STYLE.md`'s gate
   rule).
7. ⚙ Every part that is a key, lore, quest object, named creature or unique treasure has
   its registry stub.
8. ⚙ Every room listed in `Retrofit` has been recompiled, and every new part row has a
   `Realized:` label present in that room's file.

A Keys registry row is the smallest composition there is: two parts, one link. Keys keep
their registry. A composition may include them as parts.

---

## 9. Compile (4i)

### 9.1 First compile

`templates/Location.md` keeps its Template block, its Citations and its Feature grammar.
Its Context changes from "run `context.py 4c` and write from the sheet" to "read every
row naming this location" (assembled by hand in the pilot).

- **Every row is realized; nothing without a row is written.** Each row's `Realized:`
  cell gets the Feature label (or `Exits`, `Summary`, `Notes`) that carries it.
- **No fact added or dropped.** Compile chooses words, order, prominence, the Player
  Summary and the Referee Notes. A row that cannot share the room goes back to its pass.
- **One location, its own rows only.** The sibling doctrine holds here unchanged.
- Instruction 2's 30-word Feature ceiling holds. Cells are already terse facts, so the
  bloat seen in E7 has no raw material to come from.

### 9.2 Targeted recompile (retrofit)

When rows are added to or changed in a room that is already compiled (a composition run
after 4i, or any edit to a filled row):

- each **new** row gets a new Feature line, placed by prominence, and its `Realized:`;
- each **changed** row's realized line is rewritten, and only that line;
- the Player Summary and the Referee Notes are revisited only when a new or changed row is
  obvious-tier, and every bolded noun still has its Feature (`STYLE.md`);
- every other line is left exactly as it was.

Written this way, a retrofit is a diff on a handful of lines, which a reviewer can read.

---

## 10. Validation and checks

**In the pilot (hand)**: the validator runs unchanged. It is a format lint, it already
tolerates partial work, and with D3 it won't see `tables/`. Everything table-specific is
checked by hand against a checklist kept in the pilot log: record format, foreign keys,
one `Exits` row per edge, stubs filled, `Realized:` present, the composition proof (8.7),
and the distinctness rules tables make visible (a purpose repeated within a block, one
exit description across more than a third of a block's exits, two hazards in a block
sharing mechanism and clue category).

**After the analysis (tool, where called for)**: the checklist items marked mechanical
move into `tools/validate_setting.py` (errors for format and keys, warnings for unfilled
stubs, unrealized rows and the distinctness rules), `--pending` learns connected stubs,
and `metrics.py` learns per-table counts and asked against realized.

**Judgement checks**: `templates/Setting_Judgement_Check.md` gains *rows written in one
pass read as a form* (F2), *rooms read as one room* (F1) and *each composition is
solvable and priced* (8.7, items 3 and 6).

---

## 11. Analysis after the pilot

The pilot log records, per pass: what was read and how large it was, what was written,
every hand decision on a rated line, every row compile sent back, and every composition
exception. The analysis answers these, each with a decision attached:

| Question | Evidence | If yes |
|---|---|---|
| Did hand allocation hold the rates at region scale? | asked against realized, per rated line, against E2's figures | no tool needed for allocation; if not, `draw.py` returns for 4d only |
| Did the standalone read sets carry enough context? | how often compile sent rows back, and why | keep 8.4 as is; if not, add the narrowest missing input to the pass that needed it |
| Was assembling read sets by hand the expensive part? | pilot time and tokens per pass | if so, rebuild `context.py` as a collector for 8.4's read sets and compile's rows |
| Which checklist items were tedious or missed? | checklist misses found later | each becomes a validator check |
| Did compositions stay inside the weights? | exception count per composition | if not, compositions run before weighting for the rooms they claim |
| Did retrofit stay targeted? | lines changed per retrofit against lines in the room | if not, revisit D4 |
| Did table passes beat E1/E8? | the 5c "rooms are distinct" item against 9c1354b | the core claim of this change |

The analysis is written to `plans/table-pipeline/analysis.md`, and tool work is planned
from it rather than from this spec.

---

## 12. Documentation changes, by the rules in `CLAUDE.md`

- `STEPS.md`: phase 4 replaced per 8.2, first, since it is the authority.
- `patterns/SPEC.md`: the table test as a new section; the `dangerous/Key.md` paragraph
  cut back to a pointer.
- `patterns/setting/Compositions.md` (new) and an edge to it from `patterns/Genre.md`.
- `CLAUDE.md`: one line under Pattern file rules pointing at the test.
- `README.md`: `tables/` in the map. Tool lines change only when the tools do.
- Pattern files: only step-id citations move.
- Templates: new `Location_Weights.md`, `Allocation.md`, `Composition.md`, and one
  `Table_[Name].md` per table; rewritten Context for `Location_Gazetteer.md`,
  `Location.md` and the five registry templates.
- No passage is refreshed to describe the new pipeline. A passage that restated the old
  one is cut back to a pointer.

---

## 13. Acceptance

A pilot build (the keep, the borderland and at least two caves from `BRIEF.md`) runs
through 4a-4j and 5c by hand, and:

1. The validator reports no errors.
2. Every rated line is within the template's tolerance at region scale, or the log names
   the deliberate choice that moved it (E2).
3. Every edge has exactly one `Exits` row and one gate decision (E3).
4. The creature count reconciles with each Overview's Inhabitants (E4).
5. Every row is realized in exactly one location file, and no Feature lacks a row.
6. At least one composition spanning three or more rooms passes all eight proof items, and
   at least one is applied as a retrofit to rooms already compiled, changing only the
   lines 9.2 allows.
7. At least one table pass (creatures) is run from 8.4's read set alone, without compile
   sending more than an occasional row back.
8. The 5c "rooms are distinct" item finds fewer near-repeats than the second-run addendum
   at 9c1354b on comparable blocks, and "rooms read as one room" is Confirmed.
9. `analysis.md` exists and answers every question in section 11.
