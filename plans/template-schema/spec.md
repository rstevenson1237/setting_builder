# Spec - a template schema, and no editable template hard-coded in Python

Proposals to approve line by line: tick, strike or amend. **Depends on** marks a proposal
that stands only with another. Section 7 holds the open decisions, each with a
recommendation the proposals assume; all are decided.

The measure for every proposal: **would the user reasonably want to change this
directly?** If so, it is stated once, in a template's fence or a schema, and the tools read it
there. If it only applies requested styling, or follows from a schema or template decision,
it stays code. Templates stay markdown with an embedded ```kdl fence (kdl-templates D4).
The PDF and site change only in phase 5, and only by proposals approved one at a time.

---

## 1. The schema of a template

- [ ] **T1. `templates/Template_Schema.md`.** One ```kdl fence defining every fence node
  (`template`, `read`, `run`, `field`, `step`, and `format` from F1), in the notation
  `patterns/` uses. `Scope`, `Shape`, `Run` and `Length_Unit` become enums, and the
  standing reads become a `standing` node. `tools/templates.py` reads them in place of its
  `NODES`, `SHAPES`, `RUNS`, `SCOPES`, `LENGTH_UNITS` and `STANDING` tuples, and its docstring
  grammar is cut. `tools/schema_graph.py` reads it beside `patterns/`.

- [ ] **T2. A field states where it pulls from: `from=`, which replaces `reads=`.** One name
  for one thing. A source is one of:

  | Form | Reads |
  |---|---|
  | `Truths.Truth`, `Encounter`, `Dressing.mark` | a table, node or member, resolved as `reads=` is now |
  | `"setting/Procedures.md"` | a file, which the template must also `read` |
  | `BRIEF:Bestiary` | a `BRIEF.md` lever |

  A member with no `field` line, or with no `from`, is **authored**: the writer invents it.
  No line is required. The user-facing page (U1) shows the source of every member of a
  template's shape, written or not, so a missing source is visible without boilerplate.
  Check: each `from` resolves, and a file source has its `read` line.

- [ ] **T3. Output type is a schema fact: `out=`.** **Depends on** D1. `Common_Schema.md`
  gains `enum Out line prose bullets rows table tag figure`. Each `value` declares its
  default (`value text out=prose`, `value relation out=bullets`), and a member overrides it
  where it differs (`Roots text out=bullets`). It goes in `patterns/` and not the
  template because the same member reads the same way wherever it appears, and the
  renderers already read every table through the schema. `--skeleton` draws its hint from
  `out` (a paragraph, or `- ` items), and the page shows it. The renderers don't read it in
  this plan (phase 5 may).

- [ ] **T4. `items=` length on a `field`** for an `out=bullets` member (`N`, `N-M`, `N+`,
  `-M`, as `words` and `sentences`), linted by `check_lengths`.

---

## 2. Shapes the user edits, moved into the fence

**Depends on** T1.

- [ ] **F1. A `## Template` block that a tool also parses becomes a `format` node in its
  template's fence**: `Location`, `Procedures`, `Setting` and `Factions` (the Relations table
  written out verbatim). A format is an ordered list of lines, each naming the field it holds
  and how it is marked:

  ```kdl
  format {
    line header "{code} **{name}** ({type}) - *{tags}*"   type=opt
    line summary out=prose mark=bold-features            // read aloud; each Feature it names in bold
    line notes   out=prose style=italic
    each feature "**{name}:** {text}"
    line exits   "**Exits:** {exit}, ..."  unless=no-connections
  }
  ```

  It replaces the second copy in each place:
  - `--skeleton` draws the format, with its hints, where it draws the `## Template` now
  - `validate_setting.py` reads it for `LOC_HEADER_RE`, the Exits rule and
    `PROCEDURES_SECTIONS`
  - `site_common.py`'s `LOC_HEADER_RE` and `parse_setting` use the same header pattern,
    compiled from the format. This is the only change to the renderers outside phase 5,
    and the output is unchanged.

  Treasure's `TABLES` block stays prose in Instructions. It is guidance the user edits and
  no tool reads, so it has no second copy.

- [ ] **F2. A citable table states its label in the schema: `cite=`** on its
  `Setting_Schema.md` table line (`table "Named Creatures" ... cite="Named Creature"`).
  `validate_setting.py`'s `CITE_LABELS` and `Location.md`'s `## Citations` list for those
  tables are derived from it, so a new citable table is one word. The three special forms
  (Bestiary, a table roll, a Test) become `cite` nodes in `Location.md`'s fence, with their
  `form`. **Depends on** D2 for how the renderer's regexes follow.

- [ ] **F3. The Bestiary's flowed fields are named in the schema.** **Depends on** D3.
  `table Bestiary ... flow="Description Range | Numbers Sign Disposition"` (the fields of
  each sentence) replaces `BESTIARY_FLOW`. The joining words ("found in groups of",
  "heralded by") stay in `bestiary_prose`. They are styling. `Bestiary.md`'s paragraph
  explaining the flow is cut, and the page shows the flow instead.

- [ ] **F4. The setting files a step must have written come from the templates' `writes`**,
  in place of `check_top_level_files`' hand-kept list.

---

## 3. The user-facing statement

- [ ] **U1. Templates in the Schema Reference.** `schema_graph.py` reads `templates/` as it
  reads `patterns/`: each template is a definition, and each name on its fence lines
  links to the schema definition it names. A template's entry shows its purpose, the steps
  that cite it, what it reads, and every member of its shape with source (T2), output (T3)
  and length. It also shows its format (F1) and its Instructions text as written. There is
  no new page and no new builder code: `patterns.html` is already drawn from
  `schema_graph.py`.

---

## 4. What stays code, by the measure

| Shape in Python | Would the user change it directly? | Here |
|---|---|---|
| fence grammar: `NODES`, `SHAPES`, `RUNS`, ... | yes: it is the template language | T1 |
| skeleton builders (`table_skeleton`, `members_line`, ...) | no: they draw the schema, format and `out` | stay, read T3 and F1 |
| citation labels, `## Citations` | yes: adding a citable table | F2 |
| location write-up, Procedures sections, Setting header, Factions table | yes | F1 |
| Bestiary flow | which fields: yes; the joining words: no | F3 |
| `entry_card` tag, dice and rows | no: styling chosen by value type | stay |
| the seven drawn sections' sentences | no: which sections and their order are already `Region_Schema.md`'s `drawn`, and the wording is styling | stay |
| document order, layout, `PDF_CSS`, nav | no: styling | stay |
| `check_rumours`, `check_treasure_tables`, cross-file rules | no: they check schema and brief facts | stay |
| judgement checklists | yes, and they already are markdown the user edits | stay |

---

## 5. Presentation types not used now

Suggestions only. Each is a phase 5 change to the PDF and site, approved and committed on
its own, using data the build already holds.

| Type | What it adds | Data | Cost |
|---|---|---|---|
| `readaloud` | the Player Summary boxed apart from referee text | Location format `summary` | an `out` word and one CSS rule |
| `quickref` | every d6 table (Weather, Encounters, Carousing, Wounds) on one page | Procedures' tables | one PDF section |
| `index` | finding lists with page links: Bestiary by region, Quests by giver, Keys by lock | each entry's `Found at` / `Appears at` | one PDF section, one site page |
| map key | the location list beside each region sheet and block figure | the Locations gazetteer | beside the existing figures |
| `statline` | `AD 1d6-1 · MA 2 · Special` as one scannable strip | Bestiary, Named Creatures | changes `entry_card` |
| `timeline` | History on a rail by Age | History `When`; the PDF's unused `.timeline` rule | one view |
| `glossary` | Language roots and coinages, set apart | Language | one view |
| tracker | turns, light and encounter checks as a strip to tick | Procedures' Time and Distance, Encounters | one PDF section |

Recommended first: `readaloud`, `quickref`, `index`. They change how the PDF is used at
the table and need no new authored content. Running heads and backlinks need no schema word:
the first is CSS and the second is computed, so they are left out of the list. Hidden
referee text and player handouts are out (D4).

---

## 6. Migration

- [ ] **M1. Each template in place, same path.** `reads=` becomes `from=`, and a parsed
  `## Template` or `## Citations` becomes a fence node. A rule already carried by a schema
  comment, a format or `out` is cut from Instructions, per `CLAUDE.md`. The oracle for each:
  - `--read-set` and `--skeleton` for every step list the same reads and shape
  - the validator is clean
  - both `--check` builds pass
  - the site and PDF HTML are byte-equal to the baseline until phase 5
- [ ] **M2. `README.md`** names `Template_Schema.md` under `templates/` and adds the
  templates to its Schema Reference paragraph. `STEPS.md`, `TEMPLATE_CITE_RE` and
  template paths are unchanged.

---

## 7. Decisions - approved as recommended, D4 as answered

- **D1. `out` defaults.** Recommended: `text` prose, `relation` and `finds` bullets, an
  enum `tag`, every other value `line`; a member overrides only where its comment already
  says otherwise (Language's `Roots` and `Coined here`, for example).
- **D2. The special citation forms.** Recommended: the renderer keeps its three regexes, and
  the validator checks that each `cite` node's `form` matches its regex, so the two
  can't drift. The alternative, compiling the regexes from `form`, touches `render_inline`
  for no visible change.
- **D3. Bestiary flow.** Recommended: the field list goes to the schema (F3). The alternative
  leaves all of it in code and keeps `Bestiary.md`'s explanation as the second copy.
- **D4. Who the site faces.** The referee only. What players get is whatever the referee
  relays, and the referee may change it, so nothing on the site is hidden and no player
  copy is drawn.
