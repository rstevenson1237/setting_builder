# Spec - a template schema, and no template hard-coded in Python

Proposals to approve line by line: tick, strike or amend. **Depends on** marks a proposal
that stands only with another. Section 6 holds the open decisions, each with a
recommendation the proposals assume.

---

## 1. The template schema

- [ ] **T1. `templates/Template_Schema.md`.** One ```kdl fence of node definitions, in the
  notation `patterns/` already uses (`node`, `enum`, `value`), read by `tools/templates.py`
  exactly as `tools/tables.py` reads `patterns/`. `NODES`, `SHAPES`, `RUNS`, `SCOPES`,
  `LENGTH_UNITS` and the docstring grammar leave the Python; each is an enum or node here.
  `tools/schema_graph.py` draws it into `patterns.html` beside the others.

- [ ] **T2. A template is one `.kdl` file** (`templates/setting/Bestiary.kdl`). Nodes:

  ```kdl
  node template {                // the file's one root; its argument is the artifact's name
    scope Scope                  // setting | [Region Code]
    writes path list             // files written, `[Region Code]` etc. as now
    shape shape list             // a Setting_Schema table, or seed | brief | tables | gazetteer
    step step list               // STEPS.md ids that cite it; the validator checks both ways
    purpose text                 // one or two sentences; the user-facing page's first line
  }
  node pull {                    // a file a step reads, as `read` is now
    path path
    part gloss opt               // the part of it read
    once enum Once opt           // written: read once the artifact exists
  }
  node run { flag Run_Flag; arg gloss opt }       // what the validator prints for the step
  node guide { text text }       // one writing rule; many; shown to the writer and on the page
  node field {                   // one field of the artifact
    name path                    // Table.Member, as a `field` line names it now
    from from list               // where it is pulled from: see T3
    out Out                      // how it is set down: see T4
    words length opt             // N | N-M | N+ | -M
    sentences length opt
    items length opt             // for out=bullets
    note text opt                // a rule for this field only
  }
  node step { id step; ... }     // what only one step of several adds: pull, run, field
  node format { ... }            // a file's own shape: see T6
  node view { ... }              // how an entry, a page or a document is drawn: see section 3
  node cite { ... }              // a citation's grammar: see T7
  ```

  Check: every `from` resolves; every `field` names a member of the template's shape
  (today only the `reads` do); every member of the shape has a `field` or is declared
  `inherit` (the 3 rating schemas' members need not be restated per rating: see D2); a
  template with `step` has its steps cited both ways.

- [ ] **T3. `from=` states where a field is pulled from**, one or more of:

  | Form | Reads |
  |---|---|
  | `"setting/Truths.md"` | a file whole |
  | `"Truths.Truth"` | a table member, so the read set shrinks to the column |
  | `"BRIEF.md#Bestiary"` | a lever or line of the brief |
  | `"authored"` | nothing: the writer invents it. The default for a member with no source, stated so a reader can see no source was forgotten |
  | `"derived: Location.tags"` | computed from another field by rule, never written (a count, a total, a stub) |
  | `"enum"` | an item of its schema enum, no source needed |

  `--read-set STEP` reports per field, not per file. `metrics.py` READ SET gains the
  fields column. A field whose `from` names a file the template never `pull`s is an error.

- [ ] **T4. `out=` states how a field is set down**, one word from an enum defined in the
  schema. Currently-used shapes, now named:

  | `out` | Is | Today |
  |---|---|---|
  | `line` | one value on one line | `Type: Humanoid` |
  | `prose` | a paragraph or more | Description, Referee Notes |
  | `bullets` | one `- ` item each | Roots, Services, Relations |
  | `rows` | label / value pairs | an entry card's table |
  | `table` | columns by header, rows by number | roll tables, Procedures' Weather |
  | `tag` | a short word set against a title | `(Humanoid)`, `d6` weight badge |
  | `cite` | a citation to another entry | `(Lore: Title)` |
  | `figure` | a drawing from the data | region sheet, location cut |

  The length keys (`words`, `sentences`, `items`) apply to `prose`, `bullets`, `line`.
  The writer's skeleton, the linter and the renderer all take shape from `out`; today the
  schema's `text` / `list` / `string` say what a value is and nothing says how it reads.

---

## 2. One definition for a file's shape

**Depends on** T2.

- [ ] **T5. Every `## Template` block, skeleton string and `parse_*` regex becomes a
  `format`.** The write-up of a location, the Procedures sections, Treasure's `TABLES`
  line, the Factions relation table, the Setting header: each is a `format` of `line`,
  `block`, `table` nodes naming the field each fills. One definition feeds three readers:

  ```kdl
  format "Location" file="setting/region/[Region Code]/[n].md" {
    line header "{code} **{name}** ({type}) - *{tags}*"         // out=line
    block summary  out=prose  sentences="2-4" mark=bold         // read aloud; each Feature in bold
    block notes    out=prose  style=italic
    each feature   out=bullets  label="**{name}:**"  text=prose // one per Feature entry
    line exits     "**Exits:** {list}"  out=bullets
  }
  ```

  - the writer's skeleton is the format with hints, as `--skeleton` draws now
  - `check_location_file`, `LOC_HEADER_RE`, the header-tag count and the Exits rule are
    read from the format, not hand-written
  - `parse_location_file` and `parse_exits` retire: the format is the parser
  - the site and PDF draw a location from it

- [ ] **T6. A citation is a `cite`**, defined once:

  ```kdl
  cite Lore       form="(Lore: {title})"            to=entry:Lore
  cite Bestiary   form="({demeanor}, {count}, Bestiary : {title})"   to=entry:Bestiary  show=count
  cite Roll       form="({table}, d{n})"            to=table
  cite Test       form="(Test of {test}, {x}d, {type})"  forced=damage
  ```

  `render_inline`'s regexes, `cite_attrs`, the validator's citation checks and
  `Location.md`'s `## Citations` list all read these. A new citable table is one line.

---

## 3. Presentation: what is drawn, and how

**Depends on** T2.

- [ ] **P1. `view` nodes replace `entry_card`, `table_html`, `bestiary_prose`, the drawn
  `_inhabitants` ... `_secrets`, and the page layouts in `build_site.py` and `build_pdf.py`.**
  A view is a tree of presentation nodes over fields; the site and the PDF read the same
  tree and differ only in a small `target` block (columns, page breaks, nav).

  ```kdl
  view entry Bestiary {
    head   "{title}" tag="Type" stat="AD"                       // card heading
    prose  "Description" join="; " {                             // two sentences from five fields
      part Description
      part Range
      part Numbers fmt="found in groups of {}" with=Sign fmt2=", heralded by {}"
      part Disposition
      sentences 2
    }
    rows   Special MA
  }
  view drawn Inhabitants for=region {                            // was _inhabitants
    each Person    in=People       row="{at} **{name}**, {role}{ (Faction: {member})} - wants {wants}; knows {knows}{; gives (Quest: {quest})}"
    each Garrison  in=Garrison     row="{at} {who} under arms - {members}; {call} brings them within {within}"
    each Encounter in=Challenges   row="{at} {who} - {doing}; {reaction.rest}"
  }
  ```

  The row grammar is a format string: `{field}`, `{ text {field} }` for a segment kept only
  when its field is set, `{a.b}` for a member, `join=` and `sort=`. This is the whole
  language (see D3). A row that needs more is a missing field in the schema, not a
  new feature of the language.

- [ ] **P2. Document and page layout as data.** `templates/view/Document.kdl` (the PDF's
  order: cover, contents, setting pages, regions, each region's locations, depth of
  contents, columns for locations) and `templates/view/Site.kdl` (nav, index, region and
  location pages). The CSS leaves the Python strings for `tools/site_assets/pdf.css` and
  the existing site stylesheet; a `target` names which sheet.

- [ ] **P3. Presentation types not used now.** Each is an `out` or `view` word added to the
  schema, each justified by data the build already holds, none requiring a new field:

  | Type | What it adds | Data already there |
  |---|---|---|
  | `readaloud` | a boxed paragraph set apart from referee text | a location's Player Summary, now an unmarked paragraph before the italic Referee Notes |
  | `statline` | the compact `AD 1d6-1 · MA 2 · Special` strip a referee scans | Bestiary `AD`, `MA`, `Special`; Named Creatures |
  | `callout` | a ruled box for referee-only matter | Secrets, hidden exits, Conditions of a DANGEROUS region |
  | `reveal` | referee-only text collapsed on the site, a margin note in print | the Rumours' `Settled at` column, a Secret's `fact` |
  | `timeline` | dated entries on a rail, in order | History by `Age`; the PDF already carries a `.timeline` rule that no content uses |
  | `glossary` | a term list, set apart, with page references | Language roots, "Coined here" entries |
  | `index` | an alphabetical or by-kind finding list with page links | every entry's `Found at` / `Appears at`: "Bestiary by region", "Quests by giver", "Keys by lock" |
  | `quickref` | every d6 table (Weather, Encounters, Carousing, Wounds) on one page | Procedures' tables |
  | `rows-merged` | a roll table whose adjacent equal results merge: `1-2 ...` | Rumours, Treasure, Procedures tables |
  | `runhead` | the region and location code in the page margin | codes already in every heading; the PDF has page numbers only |
  | `backlinks` | "Seen at A.3, G.6" under an entry | the same `Found at` data, computed |

  Recommended first: `readaloud`, `statline`, `index`, `quickref`, `runhead`: they change
  how the PDF is used at a table (finding a thing, reading a room aloud) and need no new
  authored content. `callout`/`reveal` follow where the referee-only rule is
  settled (D4).

- [ ] **P4. A user-facing page of the templates.** `templates.html`, drawn from the
  `.kdl` files by `build_site.py`, one entry per template: purpose, steps, what it reads
  (fields, not files), each field's source and output, the guides, a worked skeleton.
  The judgement checks appear as `check` templates (T8) and drop `parse_checklist_source`.

---

## 4. Migration of the existing templates

- [ ] **M1. Mechanical, with the validator as the oracle.** For each of the 25
  generation templates: Context fence -> `template`/`pull`/`run`/`field`/`step`;
  Instructions -> `guide` lines (kept in the maintainer's words; a rule already carried by
  a schema comment is cut, per `CLAUDE.md`); `## Template` -> `format`; `## Citations` ->
  `cite`. Each is checked by `--read-set` and `--skeleton` giving the same reads and shape
  before and after, then both `--check` builds.
- [ ] **M2. `Tables.md` splits** into `Tables_Safe.kdl`, `Tables_Wild.kdl`,
  `Tables_Dangerous.kdl` sharing a base by `inherit`, so a member's `from` and `out` are
  stated once per rating rather than guessed (D2).
- [ ] **T8. Judgement checks** keep their three files as `.kdl` with `check` and `ask`
  nodes (the item, what to look at, what a finding is), read by the site as data.
- [ ] **M3. `STEPS.md` and `README.md`** cite `.kdl` paths; the validator's
  `TEMPLATE_CITE_RE` follows. `CLAUDE.md` bullet 3 gains: "A new artifact adds its
  template".

---

## 5. What stays code

- The engine: reading KDL, resolving `from`, interpreting `view`, drawing SVG maps
  (`maps.py`), the dice overlay, link resolution per target.
- Judgements that need a lookup across files (a key has a lock, a quest points to a place,
  a rumour is settled): these are named `rule`s in the schema (`rule keys-have-locks`) that
  point at one registered check, so a template can switch one on or off but not define it.
  They are today ~900 lines of `validate_setting.py` and are not template shapes.
- The fixed words of the interface (nav labels, "Roll", "Exits"): `view` nodes carry them
  where they are content, and the engine keeps those that are chrome.

---

## 6. Open decisions

- **D1. File format.** Recommended: `.kdl` throughout, with `guide` lines as quoted strings.
  Needs `tools/kdl.py` to take multi-line `"""` strings (it takes none now); the alternative
  is markdown with a leading fence per template, which keeps today's parsing trouble.
- **D2. Member-level `field` lines.** Recommended: required, with `inherit` from the
  schema's own comment when a template adds nothing (`field Bestiary.* inherit`), so the
  default costs one line and every override is visible. A template then states 5-30
  lines, not 3. The alternative, only the fields a template changes, repeats what the
  kdl-templates plan found: a member whose source is unstated.
- **D3. How far the row grammar goes.** Recommended: the minimal one in P1 and nothing
  Turing-shaped. `_alarm` sorting by time and `_loot` reading `BRIEF.md`'s die are covered
  by `sort=` and `lookup=BRIEF`; anything beyond stays a named code view (`view drawn X
  code=name`), counted and listed so none is hidden.
- **D4. Referee-only matter.** Is the site one referee's reference (so `reveal` hides
  nothing) or does it also face players? Decides `reveal` and `callout`.
- **D5. Name.** `Template_Schema.md` in `templates/` as asked, with `schema_graph.py`
  extended to read both directories; the alternative is a `templates/schema/` folder.
