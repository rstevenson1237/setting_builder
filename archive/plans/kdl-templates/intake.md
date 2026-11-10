# Intake - KDL seeds, briefs built from the tables, and KDL templates

## The request, verbatim

> planning phase to look at how kdl patterns are built into our templates. throwing a few
> things out here to work through prior to execution:
> * region brief building needs to be split into a seed.md built into X/seed.md as a kdl
>   table, 5e build the brief (user facing text) from all of the tables
> * templates seem to be very repetitive and need to pass a python parser anyways, evaluate
>   moving to kdl based templates that have stronger control over inputs and output format
> * many of our output templates have poor control over input, for examples tables.md has
>   multiple built from its template with no specification of an individual fields input,
>   same for the region briefs
> * current region briefs output is messy with large repeats and needs to be condensed
> * three paragraphs in the region briefs can be split into appropriate fields to keep the
>   one off exclusion into the parser

## How each clause is read

| Clause | Read as |
|---|---|
| "a seed.md built into X/seed.md as a kdl table" | The seed moves from `setting/region/[Code].md` into the region's folder as a table file, one ```kdl fence, written at 3c against `Region_Schema.md`'s `seed`, now nodes and members rather than `Label:` prose. |
| "5e build the brief (user facing text) from all of the tables" | The seed and every table file are the brief's only inputs. The brief is what a referee reads; what it states, a table holds. |
| "templates ... need to pass a python parser anyways" | `validate_setting.py` already regex-reads each template's Context and its step citations. Make the parsed part KDL, read by `tools/kdl.py`, so it is exact. |
| "stronger control over inputs and output format" | A template names, per field it writes, the files and members that field reads; the output's shape comes from the schema, not a hand-written skeleton. |
| "tables.md has multiple built from its template" | `templates/region/Tables.md` serves 4a, 4b, 4c and 5a, every node of three ratings, with no line saying which input feeds which member. |
| "messy with large repeats and needs to be condensed" | A brief restates the seed and the tables, and the same location across several fields. Measured below. |
| "three paragraphs ... split into appropriate fields" | `Layout text n=3` becomes three fields, one per paragraph's job. |
| "keep the one off exclusion into the parser" | "The rest" (every location the first two paragraphs did not name) is a rule the parser computes and checks, not prose the writer is trusted with. Likewise the other one-off rules that prose carries today. |

## Findings

Measured on Thornmarch at `HEAD` (13 regions, 94 locations).

**Briefs are nearly as long as what they summarise.** The 13 briefs hold 11,847 words. All
94 location write-ups together hold 13,167. A brief meant to let a referee run a region
"without opening a location" is 90% the length of opening every location.

| Field | Words, all briefs | Share |
|---|---|---|
| Layout | 5,812 | 49% |
| Inhabitants | 1,998 | 17% |
| Loot / Services | 1,339 | 11% |
| Secrets | 814 | 7% |
| Alarm | 485 | 4% |
| Leads | 213 | 2% |
| Tables (d6), labels | 1,186 | 10% |

**The repeats are paraphrase, so no check sees them.** Under 10% of any field's 5-word runs
appear verbatim in the seed or tables, yet each location is cited in 3.4 brief fields on
average and up to 7 (`F`). A's Layout paragraph 1 is the seed's View and Approach retold;
A's Inhabitants is `People.md` retold row by row; G's Loot retells its Rewards. The schema
asks for this: Layout "folds in" the seed's Approach, View and Conditions.

**Most brief fields are a table, read back.**

| Brief field | Every fact in it is held by |
|---|---|
| Inhabitants | People, Garrison, Encounter (`count`, `reaction`, `doing`, `want`, `know`) |
| Services | Purchase (`item`, `price`, `per`, `limit`), Procedure |
| Loot | Reward (`container`, `contents`), Purchase at the nearest SAFE region |
| Alarm | Encounter `answers`, its location, the Connections between |
| Leads | Rumours `Settled at`, Quests `Points to`, Person `quest` |
| Secrets | Secret `trigger`, `tell`; the fact itself is held nowhere |
| Layout | Location, Dressing (`obvious`, `ambiance`), Stop, Block, Way/Connection; and the seed |
| Tables (d6) | nothing: authored |

**Seed prose is parsed by grep.** `validate_setting.py` decides a single holding by
searching the seed for the string `Kind: single holding` (line 843). `site_common.py`
splits fields on `Label:` lines and guesses where a roll table starts (`is_table_head`).
Two rules exist only for prose briefs: `n=N` meaning paragraphs (used only by Layout) and
"a list field writes each item as its own `- ` line".

**Templates repeat themselves and the schema.** 23 of 26 templates open their Context with
the same standing line (`GENRE.md`, `STYLE.md` and `BRIEF.md`); 17 then list
`Common_Schema.md` and `Setting_Schema.md`. A setting template's `## Template` block restates
its table's fields from `Setting_Schema.md` (`Lore.md`: Form, Found at, Voice, Does, Text;
"read aloud in under a minute" is in both). Those blocks hold 1,562 words. `--read-set`
resolves a step to whole files, never to the members a field reads.

**Tables.md has no per-field inputs.** One template, four steps, three ratings. Where a
member's input is stated at all it is in prose (`mark` reads Factions' Identity; `left`
reads History's Left marks; `wound` reads `BRIEF.md`'s Procedures). A 5a writer reads every
input for every member.

## What the plan weighs

- **Said once** (`STYLE.md`) is the measure: a fact a table holds is rendered from it, not
  retold.
- Code renders what is a lookup; an agent writes only what no table can hold.
- Read sets must shrink, not grow: `tools/metrics.py` READ SET is the before and after.
- Every rule moved into the parser leaves the prose that carried it.
