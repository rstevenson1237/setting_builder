# Intake - a template schema, and no template hard-coded in Python

## The request, verbatim

> We need a template schema as well, should probably put in templates/ not patterns/. Each
> template field should state where it is pulling from as well as an output type (prose
> text, bullet point list, etc). Do a full overview of our current templates and propose a
> schema + connecting templates that would 1) completely replace the old markdown
> templates 2) provide a flexible and user facing statement of our templates 3) look at
> information presentation and suggest some additional schema types that are not currently
> being utilized that would add to the presentation 4) no more hard coded templates in the
> python

Earlier in the same session, and already built: a `field "Table.Field" words|sentences=`
length on a template's fence, linted against entries (`tools/templates.py`, `check_lengths`).

## How each clause is read

| Clause | Read as |
|---|---|
| "a template schema ... in templates/" | `templates/Template_Schema.md`: the KDL definitions of every template node, as `patterns/*_Schema.md` defines every table node. `tools/templates.py` reads it, as `tools/tables.py` reads the patterns; today the fence grammar lives only in that file's docstring and its `NODES`, `SHAPES`, `RUNS` tuples. |
| "each field states where it is pulling from" | Every `field` line has `from=`: the files, members or `BRIEF.md` levers it reads. Today a `field` line is optional, covers 10-20% of a template's fields, and says nothing for the rest. |
| "an output type" | Every `field` has `out=`: how it is set down (prose, bullets, rows, table, ...). One word that the writer's skeleton, the validator and the site/PDF renderer all read. |
| "completely replace the old markdown templates" | Each `templates/**/X.md` becomes `X.kdl`: Purpose, Context, Instructions and `## Template` blocks all become nodes. No markdown is parsed to find a template's parts. |
| "user facing statement of our templates" | A page (`templates.html`, beside `patterns.html`) drawn from the template files: per artifact, what it is, what it reads, each field's source and output, the rules for writing it. |
| "information presentation ... additional schema types" | Section 3 of the spec. |
| "no more hard coded templates in the python" | Every output shape now written as Python string-building becomes a template node the engine interprets. Inventory below. |

## What is in templates/ now

28 markdown files, 968 lines.

| Group | Files | Shape today |
|---|---|---|
| Setting generation | 18 (`Setting`, `History`, `Truths`, `Bestiary`, `Factions`, `Rumours`, `Treasure`, ...) | Purpose / Context (KDL fence) / Instructions; 3 add `## Template`, 1 a `## Citations` list |
| Region generation | 7 (`Region_Gazetteer`, `Region`, `Locations`, `Connections`, `Tables`, `Brief`, `Location`) | the same; `Tables` serves four steps and three ratings |
| Judgement checks | 3 | prose Context, a checklist of bolded items, scraped by `parse_checklist_source` for the site |

What the fence states and what it leaves out, measured on the 25 generation templates:

- `template`, `read`, `run`, `step` are structured; `field` is optional and holds `reads=`
  (and, since this session, a length). `Tables.md` has 10 `field` lines for the several
  hundred members of three ratings; `Location.md` has none.
- Output form is never stated structurally. `Bestiary` prose says "two sentences", `Location`
  keeps a 5-line skeleton in a code block, `Procedures` a 35-line one, `Treasure` an ASCII
  `TABLES` block, `Factions` a markdown table "copied as written".
- Instructions are free prose, so a rule (a count, a length, "once per X") reaches the
  validator only when someone writes a check for it by hand.

## What is hard-coded in Python now

Output shapes written as Python, by file. Each is a template that happens to be code.

| Where | What it fixes | Size |
|---|---|---|
| `tools/templates.py` | the writer's skeletons: `table_skeleton`, `members_line`, `gazetteer_skeleton`, `region_skeleton` | ~90 lines |
| `tools/site_common.py` `entry_card`, `bestiary_prose`, `table_html`, `value_html`, `prose_html` | how a setting entry, roll table and prose file render: title line, type tag, dice, kv rows, Bestiary prose, `layout=rows` | ~150 lines |
| `tools/site_common.py` `_inhabitants` ... `_secrets`, `DRAWERS`, `GUARDS` | the seven `drawn` sections of a region: which nodes each reads, the sentence each row is set in | ~130 lines |
| `tools/site_common.py` `render_inline`, `ROLL_CITE_RE`, `BESTIARY_CITE_RE`, `LOC_CODE_RE` | the grammar of a citation and what it links to; also written out in `Location.md`'s `## Citations` | ~100 lines |
| `tools/site_common.py` `parse_location_file`, `parse_exits`; `validate_setting.py` `check_location_file`, `LOC_HEADER_RE` | the location write-up's shape, parsed and linted from regexes | ~150 lines |
| `tools/build_pdf.py` `build_document`, `PDF_CSS` | document order, cover, contents, region and location layout, columns, badges | ~300 lines |
| `tools/build_site.py` `build_index`, `build_region`, `build_location`, `build_tables`, `nav_links` | the same for pages | ~250 lines |
| `tools/validate_setting.py` `check_top_level_files`, `check_procedures`, `check_rumours`, `check_treasure_tables` | the section list of `Procedures.md`, Treasure's `TABLES` line, the Rumours form: each also written in a template's prose | ~200 lines |

Two copies of each rule is the cost: the markdown template says it for the writer, the Python
for the reader, and nothing makes them agree. This session's Bestiary change was exactly
that: renderer edited, template found stale afterwards.

## What the plan weighs

- **Said once** (`STYLE.md`): a shape is defined in one place; writer skeleton, linter and
  renderer are all derived from it.
- The engine stays in Python; every shape it draws is data. Where the plan cannot reach
  that, it says what stays code and why (spec section 5).
- Templates stay readable by the person who maintains the setting: `.kdl` files with
  plain-language `guide` lines, and a generated page, not a developer's DSL.
- Nothing is renumbered: step ids stay; `STEPS.md` still cites a template by path (now
  `.kdl`).
