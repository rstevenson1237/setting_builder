# Inventory - every Spec line, placed

Implementation T1.3. Each region pattern file is shown as the table it becomes, with every
Spec line placed by `patterns/SPEC.md`'s **How a Spec becomes tables**. T1.4 applies the
**Change** column to the pattern files. Where this file and `spec.md` 7.5 disagree, this
file is the correction (listed at the end).

Column kinds:
- **K** - key, owned by the template, not the pattern (`ID`, `Location`, `Code`, `From`,
  `To`, `Realized`)
- **T** - tag: a draw's item
- **G** - gloss: a question's answer
- **R** - rated: the cell may be `none`
- **I** - id or code: names a row, a location, or a registry title
- **-** - no column: the line is an edge (its unit is a table of its own) or a rule

Change codes:
- **label** - add or confirm the column label before ` - `
- **split** - the line asks several things and becomes one line per column
- **rename** - the label collides with a joined table's
- **rule** - a rule line with no answer; it moves into the line it constrains, or into
  Constraints if it closes a pathway
- **P1-P5** - the pathway reroutes in `spec.md` 7.4

Labels must be unique within a table and among the tables its rows join by id (a kind
table joins its classifier's table; § Dressing, § Naming and a class table join
§ Location by code).

---

## DANGEROUS

### Locations.md

**§ Location** (template-owned): Code K, Name K, Tags K, Weight K, Block K.

**§ High** - `dangerous/High.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| Architecture | G | an architecture detail unique to this location | label |
| Ambiance detail | G R 50% | an ambiance detail unique to this location | label; rename (§ Dressing has Smell / Sound) |
| - | - | Dressing; Challenge; Second challenge; Mystery 30%; Treasure; Second treasure; lock obligation; quest supply; Naming; second name | edges: § Dressing, `Challenges.md`, `Treasures.md`, `Links.md` § Lock (P3), `Links.md` § Quest, § Naming |

**§ Medium** - `dangerous/Medium.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| Clue | G R 40% | concealed detail: Clue | label |
| Trigger | G R | concealed detail: Trigger | label |
| Payload | T R | Payload {a way past it \| what it is sitting on \| what the room is not saying} | label |
| Payload row | I R | (new) the treasure row a "sitting on" payload moves behind the clue | split from Payload |
| Foreshadow | G R 25% | a detail that foreshadows a HIGH location | split |
| Foreshadows | I R | (same line) which HIGH | split |
| - | - | "the challenge is present and visible on entry - never drawn absent" | rule: folds into the Challenge line's qualifier; the never-absent part goes to Constraints |
| - | - | 20% "lore instead of a table roll" | edge: sets the treasure row's What to `lore` |
| - | - | Dressing; Challenge; Treasure 50% / 33%; lock obligation; quest supply 10%; Naming; second name | edges, as § High |

**§ Low** - `dangerous/Low.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| Clue kind | T R (by exits) | Clue {CLUE} | split |
| Clue | G R | (same line) the clue itself | split |
| Trigger kind | T R | Trigger {TRIGGER} | split |
| Trigger | G R | (same line) the stated act | split |
| Payload | T R | the concealed route, or {a cache \| a piece of Lore \| a Key \| a hazard understood before it fires} | label; items become `route \| cache \| lore \| key \| hazard` |
| Payload row | I R | (new) the exit, treasure or hazard row the payload names | P2 |
| Foreshadow | G R 10% | a detail that foreshadows a HIGH | split |
| Foreshadows | I R | (same line) | split |
| - | - | Dressing; Treasure 30%; lock obligation; quest supply 5%; Naming; second name | edges |

**§ Dressing** - `dangerous/Dressing.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| Size | G | Size and shape | split |
| Shape | G | (same line) | split |
| Condition | T | Condition {active \| abandoned \| decayed \| ruined \| destroyed} | label |
| Family | T | Purpose - its family (from `dangerous/Block.md`'s FAMILY) | split |
| Use | G | (same line) the room's own use within it | split |
| Left | G | (same line) what that use left in the fabric | split |
| Smell | G | Ambiance - smell and sound | split |
| Sound | G | (same line) | split |
| - | - | temperature and footing follow from Condition | rule: no column; compile derives them |
| - | - | every exit typed and positioned (`dangerous/Door.md`) | edge: `Exits.md` |

**§ Naming** - `patterns/setting/Naming.md` (shared by every rating)

| Column | Kind | Line | Change |
|---|---|---|---|
| - | - | a name, for what turned out to be here | writes § Location's Name |
| Mouth | T | whose name it is {MOUTH} | label |
| Name shape | T | its shape {SHAPE} | label; rename (§ Dressing has Shape) |
| Second name | G R | where the class calls for a second name | split |
| Second mouth | T R | (same line) from a different mouth | split |

### Exits.md

**§ Door** - `dangerous/Door.md`, one row per diagram edge

| Column | Kind | Line | Change |
|---|---|---|---|
| ID, From, To | K | where it goes | rule: From/To come from the diagram; a map-leaving exit's To is plain terms |
| Kind | T | Kind, read off the diagram edge | label |
| Opening | T | {OPENING} | label |
| Material | G | material, construction and condition | split |
| Make | G | (same line) | split |
| Wear | G | (same line) | split |
| Position from | G | Position | split, one per end |
| Position to | G | (same line) | split |
| Gate | T R 40% | {GATE} | split |
| Opens with | G R | (same line) what opens it | split |
| Ward | I R | where warded: what the ward refuses (`dangerous/Mystery.md`) | id of a § Mystery row |
| Gate trap | I R 15% | something set on the way through (`dangerous/Hazard.md`, `dangerous/Trap.md`) | id of a § Hazard row |
| - | - | GATE `fitted` owes a Keys row per Key.md's demand end | P3: a § Lock row in `Links.md` names this exit |

### Challenges.md

**§ Encounter** - `dangerous/Encounter.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| ID, Location | K | | |
| Kind | T | {creature \| named creature \| faction} | label |
| Who | I | (same line, edge) the § Creature or § Faction row, or the Named Creature title | split |
| Doing | G | what it is doing on arrival | label |
| - | - | "Number, and scale - stated by the kind file" | rule: removed, the kind table holds them |
| Sign | G | a sign readable before it is met | label |
| Wants | G R 30% | something it wants that is not a fight | label |
| Absent | G R 25% | absent: its signs, and where it is instead | label |

**§ Creature** - `dangerous/Creature.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| Entry | I | Bestiary entry, or an inline description | label |
| Shape | T | {SHAPE} | label |
| Number | G | Number | label |
| Scale | T | {SCALE} by room weight | label |
| Demeanour | G | one word | label |
| Named | I R 25% | a Named Creature, at high weight | label |

**§ Faction** - `dangerous/Faction.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| Faction | I | which faction | split |
| Position | T | (same line) {POSITION} | split |
| Identity | G | something visible that identifies them | label |
| If lost | G | what happens elsewhere if lost or alarmed | label |
| Order | G R 50% | a standing order | label |
| Friction | T R 30% | Friction {...} | label |
| Unwilling | G R 20% | someone who would rather be elsewhere | label |

**§ Hazard** - `dangerous/Hazard.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| ID, Location | K | | |
| Mechanism | T | {trap \| environmental \| residual} | label |
| Clue | G | Clue - one anyone entering would notice | split |
| Searcher's clue | G R | (same line) where it can, a second only a searcher finds | split |
| Tier | T | {TIER} | label |
| Caught | G R 20% | something already caught in it | label |

**§ Trap** - `dangerous/Trap.md`: Parts G (the "Mechanism" line; **rename**, it joins § Hazard), Trigger G, Damage G (the `Xd Type` expression, a short phrase), Set by G (who set it, and whether maintained).

**§ Environmental** - `dangerous/Environmental.md`: Kind T, Condition G (with its edge), Cause G, Course T, Threshold T (the "Trigger" line; **rename** for sense, not collision), Damage G, Spared spot G R 30%.

**§ Residual** - `dangerous/Residual.md`: Maker T (split from the line) and Event G (the History event; split), Doing G, Course T, Edge G (the "Trigger" line; **rename**), Damage G, Protects G R 30%.

**§ Mystery** - `dangerous/Mystery.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| ID, Location | K | | |
| Fixture | T | {FIXTURE} | label |
| Detail 1, Detail 2 | G | 2 physical details | label; numbered (rate `2`) |
| Detail 3 | G R 40% | a third detail | label |
| Trigger kind | T | Trigger {placed \| spoken \| ...} | split |
| Trigger | G | (same line) the act | split |
| Correct | G | what the correct trigger accomplishes | label |
| Wrong | G | what a wrong attempt costs | label |
| - | - | Constraint: a fixture whose answer is elsewhere is a lock | P3: a § Lock row in `Links.md` names this mystery |

### Treasures.md

**§ Treasure** - `dangerous/Treasure.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| ID, Location | K | | |
| Disposition | T | {DISPOSITION} | label |
| What | T | {table roll \| key \| lore \| unique treasure} | label |
| Table | T R | (same line, edge to `patterns/setting/Treasure.md`) I-V | split |
| Unique | I R | (same line, edge) the Unique Treasure title | split |
| Container | G | what it is in, under, or behind | split |
| Material | G | (same line) what it is made of | split |
| Moves | T | (same line) whether it can be moved {yes \| no} | split |
| Reach | G | (same line) the search or trigger that reaches it | split |
| Seal | T | (same line) {sealed \| breached \| reclosed \| fused in place} | split |
| Guard | I R | Guarded: drawn as an Encounter or a Hazard (where disposition is guarded) | label; id of an § Encounter or § Hazard row |
| Lesser thing | G R 25% | a lesser thing living on the container | **P1**: a gloss, no longer an edge to `dangerous/Creature.md` |
| Set on | I R 25% | something set on the container (`Hazard.md`, `Trap.md`) | id of a § Hazard row |
| Tried | G R 30% | something already tried for it and failed | label |
| Left because | T R 20% | {too heavy \| ...} | label |

**§ Key** - `dangerous/Key.md` supply end (**P3**: the file keeps only this end)

| Column | Kind | Line | Change |
|---|---|---|---|
| Object | G | the object, and what it physically is | label |
| Held | T | {carried \| fitted \| buried \| mounted \| owed} | label |
| Keys row | I | stub row in `setting/Keys.md` | label |
| Opens | I | (same line) the location it opens | split |
| Connection | G R 40% | a clue connecting object to lock | label |
| Used | G R 20% | evidence it has been used before | label |

**§ Lore** - `dangerous/Lore.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| Form | G | physical form, its condition part of what it tells | label |
| Survived | G | why it survived where it did | label |
| Voice | G | whose voice it is in | split |
| Wrong about | G | (same line) what they were wrong about | split |
| Does | T | {DOES} | label |
| Lore row | I | stub row in `setting/Lore.md` | label |
| Detail | G R 50% | a detail that only makes sense once another location is seen | split |
| Seen at | I R | (same line) which location | split; connected |

### Links.md

**§ Lock** - `dangerous/Lock.md` (**new, P3**: Key.md's demand end)

| Column | Kind | Line | Change |
|---|---|---|---|
| ID, Location | K | | |
| On | I | the feature it sits on (an `Exits.md` or § Mystery row) | from Key.md demand |
| Lock | G | the lock, and what it physically is | from Key.md demand |
| Keys row | I | the `setting/Keys.md` row that named it | from Key.md demand |
| Forced | G R 20% | evidence it has been forced at | from Key.md demand |

**§ Quest** - `dangerous/Quest.md`: ID K, Location K, Supplies T, Obstacle T, Quests row I (stub row line), Tried G R 30%.

### Not a region table

`dangerous/Block.md` - its unit is the block, already recorded in each `[Block].mmd`
header (Block, Basis, Family or Household, Ways in). § Location's Block column names it.
§ Dressing's Family column takes its vocabulary from Block's FAMILY.

---

## WILD

### Locations.md

**§ Location** (template-owned): Code, Name, Tags, Weight (the classification).

**§ Landmark** - `wild/Landmark.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| Clue kind | T R 20% | Clue {growth \| ground \| weather \| wear} | split |
| Clue | G R | (same line) | split |
| Trigger | G R | Trigger - a stated act at a stated spot | label |
| Payload | T R | {a cache \| a piece of Lore \| a Key \| a vantage \| what this place was for} | label |
| Payload row | I R | (new) the treasure row a cache, lore or key payload names | P2 |
| - | - | "freely discoverable by roaming" | rule: the class's definition; moves to Provides |
| Reason to stop | G | a reason to stop, visible from outside | label |
| - | - | "a visible detail leading onward to each Hidden child"; "a Clue for each Secret child" | rule: the child's row holds it (§ Hidden Lead, § Secret Access clue); removed here |
| - | - | Dressing; Kind; Challenge 35%; Treasure 15%; quest role 10%; Naming | edges |

**§ Hidden** - `wild/Hidden.md`: Clue kind T R 20%, Clue G R, Trigger G R, Payload T R (`... \| what the parent implied, one step further`), Payload row I R (P2), Parent I, Lead G (the visible detail at the parent - a mundane exit), Implied G (what the parent implied, made concrete). The Secret-child Clue line is removed (rule), since the child's row holds it.

**§ Secret** - `wild/Secret.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| Parent | I | parent location, named | label |
| Access clue | G | Clue - already visible in the parent's Features | label; rename (inner triple) |
| Access trigger | G | Trigger - the act at the parent | label; rename |
| - | - | Payload - an Exit to this location, marked hidden | rule: the diagram's hidden edge is the payload |
| Concealed because | G | a reason it was worth concealing | label |
| Clue kind, Clue, Trigger, Payload, Payload row | as § Hidden, R 20% | the inner concealed detail | split; P2 |

**§ Dressing** - `wild/Dressing.md`: Size G, Shape G (split), Position G, Condition T and Weathered G (split: what weather has done, and rain and night), Smell G, Sound G (split). "Purpose - per its kind file" is a rule (removed). The exit line becomes `wild/Exit.md` (**P5**).

**Kind tables** (one row per location of that kind):

| Table | Columns (all labels; splits marked *) |
|---|---|
| § Ruin - `wild/Ruin.md` | Was T* and When G*, State G, Holds T, Second occupancy G R 40%, Lost practice G R 30%; faction 25% is an edge to § Faction |
| § Lair - `wild/Lair.md` | Lives I* and Holding T*, Territory G, Sign G, Eats G, Child T (where the graph gives one), Dependants G R 40%, Absent G R 30%, People T R 20%; faction is an edge |
| § Natural Feature - `wild/NaturalFeature.md` | Is G*, Scale G*, Matter T*, Stop for T, Unlike G, Mysterious G R 30%, Resource G R 30%, Hazard G R 20% (a value: "simply part of the place", not a § Hazard row); faction 15% is an edge |
| § Crossing - `wild/Crossing.md` | Crossing T* and Why G*, Control T, Far side G, Caught T R 40%, Toll G R 30%; faction 30% is an edge |
| § Faction - `wild/Faction.md` | Location K, Faction I* and For T*, Identity G, Reach G* and Enforced by T*, Order G R 40%, Friction T R 30%, Unwilling G R 20% |

**§ Naming**: as DANGEROUS.

### Exits.md

**§ Exit** - `wild/Exit.md` (**new, P5**, from `wild/Dressing.md`'s exit line): ID, From,
To K, Kind T (from the diagram), Way G (typed: a path, a ford, a climb), Position from G,
Position to G (a compass direction or a stated relation; never two exits reading
identically).

### Challenges.md

| Table | Columns |
|---|---|
| § Creature - `wild/Creature.md` | ID, Location K, Entry I, Number G, Scale G, Doing T* and Noticed T* {yes \| no}, Reaction G, Limit kind T* and Limit G*, Demeanour G, Range G R 40%, Absent G R 30% |
| § Hazard - `wild/Hazard.md` | ID, Location K, Mechanism T, Tier T, Warning kind T* (at least one: a tag list) and Warning G*, Trigger G, Damage G, Set for G R (where the mechanism is `set`; the line states the condition), Caught G R 20% |
| § Mystery - `wild/Mystery.md` | ID, Location K, Thing T, Detail 1 G, Detail 2 G, Trigger kind T* and Trigger G*, Correct G, Wrong G, Price G |

### Treasures.md

| Table | Columns |
|---|---|
| § Treasure - `wild/Treasure.md` | ID, Location K, What T, Table T R*, Unique I R*, Why here T, Reach T, Claim T R 30% |
| § Key - `wild/Key.md` | Object G, Opens I* and Feature G*, How here T* and Where G*, Clue T R 30%, Known G R 20%, Keys row I (new: the registry title, as in DANGEROUS) |
| § Lore - `wild/Lore.md` | Form T* and Weathered G*, Voice T* and Wrong about G*, Names G, Does T, Lore row I, Partial G R 30% |

### Links.md

**§ Quest** - `wild/Quest.md`: ID, Location K, Role T, Quests row I, Others T R 30%.

---

## SAFE

### Locations.md

**§ Location** (template-owned): Code, Name, Tags, Weight (the prominence: `liner note | working | central`).

**§ Settlement** - `safe/Settlement.md`

| Column | Kind | Line | Change |
|---|---|---|---|
| - | - | the settlement's type, from the Overview | rule: removed, the Overview holds it |
| - | - | Prominence {PROMINENCE} | rule: it is § Location's Weight; the PROMINENCE block stays as Weight's vocabulary |
| Clue kind | T R 10% | Clue {mismatch \| behaviour} | split |
| Clue | G R | (same line) | split |
| Trigger kind | T R | Trigger {asking \| ...} | split |
| Trigger | G R | (same line) | split |
| Payload | G R | what is concealed | split |
| Finds out | G R | (same line) who finds out the party knows | split |
| How soon | G R | (same line) | split |
| Response | G R | (same line) what they do about it | split |
| - | - | a person, from the roster (`safe/People.md`) | edge: § People |
| - | - | what it takes to get anything out of them | rule: each kind table's gate column answers it (Prices, Hearing, Talked to, Lets through, Protection) |
| Obtainable | T | {good \| service \| name \| permission \| place to stand} | split |
| Thing | G | (same line) the one thing obtainable here | split |
| Cannot | G | what this place cannot do | split |
| Sends to | I | (same line) where it sends them | split |
| Named | I R 30% | a Named Creature, where the person will recur | label |
| - | - | hooks by prominence {quest \| lore \| key \| faction}; Situation | edges: `Links.md` |
| - | - | Kind; Dressing; Naming | edges |

**§ Dressing** - `safe/Dressing.md`: Size G, Shape G (split), Condition G and Signs of use G (split), Smell G, Sound G (split), Departs G R (from the settlement's shared way of building). "Purpose - per its Kind" is a rule (removed). The DETAIL BUDGET is allocation's (rule, removed from the row). The exit line becomes `safe/Exit.md` (**P5**).

**§ People** - `safe/People.md` (drawn as the gate person and as the `people` kind; both exactly one per location, so one table): Name I, Doing G, Distinctive kind T* and Distinctive G*, Wants G, Opinion G R 20%.

**Kind tables**:

| Table | Columns (splits marked *) |
|---|---|
| § Commerce - `safe/Commerce.md` | Trade T* and Proprietor I*, Stock kind T* (tag list) and Stock G*, Prices G, Terms G R (where hospitality or market; the line states the condition), Unusual G R 40%, Condition T R 30%, Wants G R 20% |
| § Authority - `safe/Authority.md` | Claim T* and Holder I*, Settles kind T* and Settles G*, Limit G, Hearing T, Rival G R 40%, Posted G R 30%, Custom kind T R* 20% and Custom G R* |
| § Social - `safe/Social.md` | Who G* and Doing G*, Circulating G, Talked to T, Tension kind T R* 40% and Tension G R*, Knows G R 20% |
| § Wealth - `safe/Wealth.md` | Contents T (edges: a table roll, a Unique title, or a `Links.md` § Lore row), Contents row I R*, Owner T* and Knows T*, Protection T, Protection detail G*, Second protection T R 30%, Rival G R 20% |
| § Garrison - `safe/Garrison.md` | Post T, Watch I* and Count G*, Watches for G* and Order G*, Lets through T, Short of T, Graft G R 30%, Punished G R 20% |

**§ Naming**: as DANGEROUS.

### Exits.md

**§ Exit** - `safe/Exit.md` (**new, P5**, from `safe/Dressing.md`'s exit line): ID, From, To K, Kind T, Way G, Position from G, Position to G, Who may use G (access here is social as well as physical).

### Links.md

| Table | Columns (splits marked *) |
|---|---|
| § Quest - `safe/Quest.md` | ID, Location K, Giver I, Reluctance G, Object G* and Target I*, Terms G, Quests row I, Omission T R 40%, Deadline G R 30%, Asked already G R 20% |
| § Lore - `safe/Lore.md` | ID, Location K, Form G, Holder T* and Why held G*, Access G, Voice G* and Wrong about G*, Does T, Lore row I (new, as DANGEROUS), Incomplete G R 30% |
| § Key - `safe/Key.md` | ID, Location K, Object G, Opens I* and Feature G*, Holder G* and Knows T*, Get by T, Clue G R 30%, Rival G R* 20% and How close G R*, Keys row I (new) |
| § Faction - `safe/Faction.md` | ID, Location K, Faction I* and Want T*, Identity G, Member G* and Known T* {openly \| hidden}, Return G, Rival G R 40%, Hidden doing G R 30%, Former G R 20% |
| § Situation - `safe/Situation.md` | ID, Location K, Visible G, Worse off I, Rung G* and Next G*, Benefits T R* 40% and Beneficiary G R*, Doing about G R 30%, Worse T R 20% |

`safe/Wealth.md` draws `safe/Lore.md` at depth 3 and the hook line at depth 2, so the
hook's home wins (`Links.md` § Lore), and Wealth's Contents row names it.

---

## Setting registries and files (D10)

Field and column names are their patterns' Spec labels, cut down to what each template
outputs. Template blocks are rewritten at T1.7.

| File | Shape | Columns or fields |
|---|---|---|
| `region/Regions.md` | table | Code, Name, Gloss, Rating, Die, Tag line |
| `Keys.md` | table | Name, Form, Found at, Opens, Feature, Apart, Connection |
| `Quests.md` | table | Name, Given at, Resolved at, Ask, Reluctance, Object, Obstacle, Terms |
| `Truths.md` | table | Truth, Kind, Handle, Codes |
| `Bestiary.md` | record | Type, AD, MA, Description, Range, Sign, Disposition, Special |
| `NamedCreatures.md` | record | Type, AD, MA, Appears at, Role, Motivation, Reaches by, Remembers, Wants, Description, Special |
| `UniqueTreasures.md` | record | Found at, Does, Cost, Origin, Description |
| `Lore.md` | record | Form, Found at, Voice, Does, Text |
| `Factions.md` | record | AD, Want, Identity, Resources, Knowledge, Tactics, Reactions, Goals, Fields |
| `History.md` | record | When, Kind, Event, Left, Codes |

---

## Corrections to `spec.md`

1. **WILD access needs no `Exits.md` section.** The Hidden and Secret class files already
   carry their parent, lead and access triple, and each is exactly one per location, so
   they are columns of § Hidden and § Secret. The Landmark's matching registry lines
   become rule lines pointing at the child's row.
2. **Labels are unique within a table and among the tables its rows join**, not across
   the whole file. File-wide uniqueness would force renames like "Trap damage" against
   "Environmental damage", tables that never join.
3. **A draw usually needs its instance as well.** Where a draw line also asks for the
   thing itself (a clue's kind and the clue), it is compound and splits into a tag column
   and a gloss column.
4. **Rule lines produce no column.** Lines stating a rule rather than asking something
   ("present and visible on entry", "freely discoverable", "stated by the kind file") move
   into the line they constrain, into Constraints, or into Provides.
5. **`safe/People.md` resolves to one table**: both of its draws are exactly one per
   location in the same file.
6. Counts are unchanged from 7.5: DANGEROUS 5 files / 20 tables, WILD 5 / 19, SAFE 3 / 16.
