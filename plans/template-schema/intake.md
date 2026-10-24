# Intake - a template schema, and no editable template hard-coded in Python

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

Clarified on review:

> don't split it as we will run together but different phases is fine. Clarifying and
> agreeing with your assessment that "no hard coded template" may be over reaching. Our
> deliverable is a flexible and readable template format that is exposed in the embedded
> kdl that the user can easily parse and suggest improvements/changes. I think the measure
> is "would the user reasonably want to change this directly" as opposed to formatting
> embedded in python which is just honoring our requested output styling or relies upon
> another template decision. This should minimally touch the PDF/web presentation

## How each clause is read

| Clause | Read as |
|---|---|
| "a template schema ... in templates/" | `templates/Template_Schema.md`: the KDL definitions of every fence node, as `patterns/*_Schema.md` defines every table node. Today the grammar lives only in `tools/templates.py`'s docstring and its `NODES`, `SHAPES`, `RUNS`, `SCOPES`, `LENGTH_UNITS`, `STANDING` tuples. |
| "each field states where it is pulling from" | A field's source is stated, or it is authored; the user-facing page shows the source of every member, stated or not. |
| "an output type" | One word per member saying how it is set down (prose, bullets, ...). |
| "completely replace the old markdown templates" | The embedded fence carries everything a tool reads: `## Template` skeletons and `## Citations` lists become fence nodes. Purpose and Instructions stay markdown (kdl-templates D4). |
| "user facing statement of our templates" | The templates, drawn in the existing Schema Reference (`patterns.html`) beside the schemas they name. |
| "information presentation ... additional schema types" | Proposed in the spec, each approved on its own. |
| "no more hard coded templates in the python" | Narrowed by the measure above: a shape leaves the Python when the user would reasonably want to change it directly. Styling, and renderings that follow from a schema or template decision, stay code. The PDF and site change as little as that allows. |

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

Output shapes written as Python, by file. Spec section 4 sorts each by the measure.

| Where | What it fixes | Size |
|---|---|---|
| `tools/templates.py` | the writer's skeletons: `table_skeleton`, `members_line`, `gazetteer_skeleton`, `region_skeleton` | ~90 lines |
| `tools/site_common.py` `entry_card`, `bestiary_prose`, `table_html`, `value_html`, `prose_html` | how a setting entry, roll table and prose file render: title line, type tag, dice, kv rows, Bestiary prose, `layout=rows` | ~150 lines |
| `tools/site_common.py` `_inhabitants` ... `_secrets`, `DRAWERS`, `GUARDS` | the seven `drawn` sections of a region: which nodes each reads, the sentence each row is set in | ~130 lines |
| `tools/site_common.py` `render_inline`, `ROLL_CITE_RE`, `BESTIARY_CITE_RE`, `LOC_CODE_RE` | the grammar of a citation and what it links to; also written out in `Location.md`'s `## Citations` and `validate_setting.py`'s `CITE_LABELS` | ~100 lines |
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
- A shape a user would edit is data; styling, and drawing that follows from a schema, stays
  code (spec section 4).
- Templates stay markdown with an embedded fence, readable and editable by the person who
  maintains the setting.
- Nothing is renumbered and no template is renamed: step ids and template paths stay.
