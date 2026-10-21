# Spec - KDL seeds, briefs built from the tables, and KDL templates

What `intake.md` asks for, as proposals to approve line by line: tick, strike or amend.
**Depends on** marks a proposal that stands only with another. Section 5 holds the open
decisions; each has a recommendation, and the proposals assume it.

---

## 1. The seed is a table file

- [ ] **S1. `setting/region/[Code]/Seed.md`.** One ```kdl fence of nodes keyed by the
  region code, as `Ground.md` is (`Ground A ...`). `Region_Schema.md`'s `seed` becomes
  nodes; the folder line of each rating gains `Seed`. Written at 3c as now, still naming no
  location. `setting/region/[Code].md` is retired. *(Name: see D2.)*

- [ ] **S2. Each prose field split into the members it already packs.** The schema comments
  already list them; they become members, typed with `Common_Schema.md`'s values.

  ```kdl
  node Overview {             // every rating
    comes string              // what a party comes to do
    who entry Bestiary Factions list
    changing string           // what is changing, true whether or not the party engages
  }
  node Rung {                 // n=2 in each seed: the rule "two rungs, each with what sets it off"
    if string
    then string
  }
  node View {                 // SAFE
    from string
    distance distance
    outline string
    wall feet opt
    material gloss opt
    ground gloss
    shows string              // roofs, colours, devices, lights
  }
  node Entry {                // a way in, every rating: SAFE Approach, WILD Approach, DANGEROUS entrance
    name gloss
    from string opt
    stands string             // what stands at it or watches it
    takes string opt          // what passing takes
    refused string opt        // what befalls the turned away
    best time opt             // WILD: a crossing on the best route
    off time opt              // and off it
  }
  node Law { offence gloss; cost string; enforcer gloss }     // SAFE, one per rule
  node Ruling { on gloss; buys string }                       // WILD Terrain, one per ruling
  node Conditions {           // DANGEROUS, every room unless it says otherwise
    material gloss
    height feet
    width feet
    light gloss
    sound gloss
    footing gloss
    air gloss
    fire string
  }
  ```

  - Check: `Kind` is read from the node, retiring the `Kind: single holding` grep. Two
    `Rung`s. A DANGEROUS Block's `width` and `height` default to `Conditions` and are
    written only where they differ, retiring the 4b rule that restates them.
  - Cost: 13 seeds (3,322 words) rewritten as nodes; Region.md's template rewritten (T-rules
    below); the site and PDF render the seed through the schema-driven readers tables use.

---

## 2. The brief: rendered where it is a lookup, written where it is not

**Depends on** S1, D1.

- [ ] **B1. Rendered sections.** Built by code from the seed and tables at site and PDF
  build, never written by hand and never stale:

  | Section | From |
  |---|---|
  | Inhabitants | People, Garrison, Encounter: who, how many, where, reaction, wants, knows |
  | Services (SAFE) | Purchase and Procedure, by location |
  | Loot (WILD, DANGEROUS) | Reward `container` and `contents` by location; Hoards; who buys, from the nearest SAFE region's Purchases |
  | Alarm (DANGEROUS) | Encounters with `answers`, soonest first, with their locations |
  | Leads | Rumours `Settled at`, Quests `Points to`, Person `quest` naming a location here |
  | Secrets | Secret `tell` and `trigger` by location, and `fact` (B4) |

  A roster renders as a table or list, one row per entry, so nothing in it can be said
  twice. Retires `check_inhabitants`, the Services and Layout name checks, and the brief
  `Tables:` parser.

- [ ] **B2. `Brief.md` holds only what no table holds, as KDL.** Written at 5e:

  ```kdl
  // SAFE                         WILD                      DANGEROUS
  Arrival A.1 "..."            // Way B.1 "..."            Entrance F.1 "..."
  Plan "..."                   // Landmark B.3 "..."       Prize F.5 "..."
  Place A.3 "..."              // Place B.4 "..."          Place F.2 "..."
  Event 1 at=A.4 "..."         // Event 1 at=B.2 "..."     Danger 6 at=F.1 "..."
  ```

  - The three Layout paragraphs become the first three node kinds (Layout `n=3` retired).
    SAFE: `Arrival` per way in, `Plan` (how the wards and walls divide the locations, once),
    `Place`. WILD: `Way` per way in and Route, `Landmark`, `Place`. DANGEROUS: `Entrance`,
    `Prize` per High location, `Place`.
  - **The exclusion is the parser's**: `Place` is owed for exactly the locations no earlier
    node names. Every location is named by exactly one node; a code in two is an error.
  - A node's text says what the tables and maps do not: what a party notices, hears or goes
    there for. Each carries `words=` from `BRIEF.md` (B3).
  - `Event` / `Danger` nodes replace the d6 `Tables:` block; their count and die come from
    the schema.

- [ ] **B3. Brief size is a lever.** `BRIEF.md` gains `brief place=30 arrival=60 event=20`
  (words per node, defaults to tune). Estimate at these defaults: 94 location nodes and 78
  events come to about 5,000 written words against 11,847 today; the rendered rosters add
  rows, not prose.

- [ ] **B4. A Secret states its fact.** `Secret` (SAFE, WILD, DANGEROUS) gains
  `fact string opt` and `knows gloss opt`, so Secrets renders whole. Without it, Secrets
  stays a written `Secret` node in `Brief.md`. *(See D3.)*

- [ ] **B5. The site and PDF draw a region page as: seed, then the B2 nodes in schema order,
  then the B1 sections.** `--check` fails a build that drops any node. `_parse_region_fields`,
  `is_table_head` and `REGION_LABEL_RE` retire; `n=` means items only.

---

## 3. Templates carry a KDL fence

**Depends on** D4.

- [ ] **T1. A template's machine part is a ```kdl fence; its prose stays markdown**, as a
  schema's does. `kdl.py`'s strings are single-line, so instructions stay prose.

  ```kdl
  template Brief step=5e writes="setting/region/[Code]/Brief.md" schema="Region Safe brief"
  read "setting/region/[Code]/Seed.md"
  read "setting/Rumours.md" for=Leads
  field Place reads="Dressing.obvious Dressing.ambiance Location.tags"
  field Event reads="Encounter Challenge Seed.Rung"
  ```

- [ ] **T2. Standing context is implied, never listed.** Every template reads `GENRE.md`,
  `STYLE.md`, its `BRIEF.md` slice and `Common_Schema.md`; `template` names its scope
  (`setting` or `[Code]`). Retires 23 identical Context lines and 17 schema lines.

- [ ] **T3. The output skeleton comes from the schema.** `--skeleton STEP` prints the shape
  a step writes, from the `schema=` its template names. Each `## Template` block that
  restates a schema (1,562 words in `templates/setting/`) is cut; a template keeps a
  skeleton only for a shape no schema holds.

- [ ] **T4. Per-field inputs.** A `field` line names the members it reads; `--read-set STEP
  [Code]` resolves to files and members, and the writer reads that set, nothing more. A
  member a field reads that no schema defines is an error.

- [ ] **T5. `templates/region/Tables.md` splits by step.** One `step` node per step
  (4a Locations, 4b Connections and Blocks, 4c stubs, 5a fill, 5a locks), each with its own
  `writes`, `read` and `field` lines, so 4a reads no 5a input. Its prose sections follow the
  same split. One file still, per "one template per artifact type".

---

## 4. Rules moved into the parser

Each leaves the prose that carried it:

| Rule, as prose today | Becomes |
|---|---|
| Layout "every location by code" | B2: each location named by exactly one node |
| Layout `n=3` paragraphs | B2: three node kinds |
| "Nothing the seed says is repeated, unless a field folds it in" | B1/B5: the seed renders once, above the brief; nothing folds it in |
| "A DANGEROUS Alarm is written from the Encounters' answers" | B1: rendered |
| "Leads - each rumour by number, each quest by name" | B1: rendered |
| "two rungs, each with what sets it off" | S2: two `Rung` nodes |
| "A list field writes each item as its own `- ` line" | retired: no prose lists |
| A Block's passages "as the seed's Conditions give it" | S2: default from `Conditions` |
| `Kind: single holding` grep | S2: read from the node |

---

## 5. Open decisions

- **D1. Who writes the rosters.** (a) *Recommended*: code renders Inhabitants, Services,
  Loot, Alarm, Leads and Secrets (B1); the agent writes only B2. (b) The agent writes every
  field from KDL inputs (T4) under word caps. (a) cannot repeat a table and is never stale;
  it reads as a run sheet of lists, not paragraphs. (b) reads as prose and keeps 5e's cost.
- **D2. File name.** `Seed.md`, *recommended*, matching the folder's table files
  (`Locations.md`, `Ground.md`); or `seed.md` as written in the request.
- **D3. Secrets.** B4 adds `fact` to `Secret` so Secrets renders, *recommended*; or Secrets
  stays a written node in `Brief.md`.
- **D4. Template form.** Markdown with a ```kdl fence, *recommended* (T1); or pure `.kdl`
  files, which needs multi-line strings in `kdl.py` and puts every instruction in quotes.

---

## 6. Order, once approved

S1-S2 (seed, with Thornmarch's 13 seeds migrated) → B4 → B1, B5 (renderers, against the
old briefs still on disk) → B2-B3 (13 briefs rewritten, old fields retired) → T1-T5
(templates, `--read-set` and `--skeleton`). `implementation.md` is written after this spec
is approved. `tools/metrics.py` READ SET and brief word counts are saved before and after.
