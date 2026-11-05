# Implementation - visual design

The task plan for `spec.md`, written for the agent that builds it. Commits cite tasks as
`visual-design T1`.

## Before you start

- Read `CLAUDE.md`, `README.md`, `GENRE.md`, `STYLE.md`, `STEPS.md`, then `intake.md` and
  `spec.md` in this folder. Read the `setting-maps` skill before touching any map tool.
- Develop on `claude/admiring-planck-9nadaj`. Push with `git push -u origin claude/admiring-planck-9nadaj`.
  Open no pull request unless the user asks.
- Python stays stdlib only. Run artgen only through `maps.artgen()` or
  `node tools/artgen/artgen-maps.js ... --file <path>`.
- **Every task ends** with `python3 tools/validate_setting.py` at 0 errors,
  `python3 tools/build_site.py --out <scratch>/site --check` and `python3 tools/build_pdf.py --check`
  passing, and its own commit. Never loosen a check to get there; fix the cause.
- After writing any framework file (template, schema, skill, CLAUDE.md, README.md), review it as
  `CLAUDE.md` asks: state it more simply, and cut lines that record work history or repeat what is
  true elsewhere.
- **STOP** marks a point where you show the user something and wait for their answer. Do not go
  past it on your own judgement.
- Never set a design's `approved`, send an artgen report, or run `report --issue` without the
  user's word.
- Map files are built, never edited by hand.

| Task | Spec | What | Files |
|---|---|---|---|
| T0 | | Baseline | `metrics-before.txt` |
| T1 | S10 | Install artgen 0.13 | `tools/artgen/`, `.claude/`, `CLAUDE.md`, `tools/dungeon.py`, `tools/maps.py`, `plans/sheet-maps/artgen-capabilities.md` |
| T2 | S12 | Claude Code settings | `.claude/settings.json` |
| T3 | S11 | House look (STOP) | `BRIEF.md`, `tools/tables.py`, `tools/dungeon.py`, `tools/maps.py`, `tools/validate_setting.py` |
| T4 | S1, S2, S4, S6, S9 | Schemas, step ids, `Void`, `space.py from` | `patterns/`, `tools/validate_setting.py`, `tools/tables.py`, `tools/space.py`, `tools/schema_graph.py` |
| T5 | S4, S7 | Layout library, `design.py layouts` and `expand` | `layouts/`, `tools/design.py` |
| T6 | S7 | SAFE/WILD solver spike (STOP) | `plans/visual-design/spike-settlement.md` |
| T7 | S3, S5, S7 | `solve`, `accept`, `check`; the validator holds tables to designs | `tools/design.py`, `tools/validate_setting.py`, `tools/maps.py`, `tools/space.py` |
| T8 | S1, S8, S13 | Templates, steps, skill, docs | `templates/region/`, `templates/checks/Map_Judgement_Check.md`, `STEPS.md`, `.claude/skills/block-design/`, `CLAUDE.md`, `README.md` |
| T9 | all | Pilot: design region E (STOP twice) | `BRIEF.md`, `setting/region/E/` |
| T10 | | artgen report (STOP) | `plans/visual-design/report-artgen.md` |
| T11 | | Close | `metrics-after.txt`, this folder |

## T0 - baseline

- `python3 tools/metrics.py > plans/visual-design/metrics-before.txt`.
- In your scratchpad, keep the validator's output, `python3 tools/space.py`'s output, a site build
  (`build_site.py --out <scratch>/before`), and the block maps
  (`maps.py draw --out <scratch>/maps-before --fit 1600x1600px`). Later tasks diff against these.

## T1 - install artgen 0.13

- `npx -y github:rstevenson1237/image_tools#artgen-dist-v0.13.0 update --no-scaffold --notes <scratch>/notes.md`.
  Read the notes. `node tools/artgen/artgen-maps.js status` lists files edited here; keep those edits.
- 0.13 keeps dungeon format 2 and adds only optional keys, so the maps should draw as before
  except where 0.13 fixes a fault: exit notes kept on the floor (#44), exits on one wall spread
  apart (#45), labels moved off notes. Diff the maps against T0 and look at every changed one.
- Read `tools/dungeon.py` and `tools/maps.py` for code that works around a fault 0.13 fixes: exit
  notes, exits on a wall, thin `poly` rooms, junction hints. Remove each workaround and confirm the
  map is no worse.
- Run `node tools/artgen/artgen-maps.js schema dungeon --checks`. Add to `dungeon.FAULTS` each new
  check id that the validator should hold as an error for this build: `note-off-floor`,
  `marks-overlap`, `end-in-room`, `offset-moved`, `junction-at-bend`. Leave out any the current
  build fails for a reason the content should fix; list those for the user instead.
- Update `plans/sheet-maps/artgen-capabilities.md` to what the framework writes on 0.13. Leave
  `tools/artgen/MANIFEST.json` to the installer.
- Commit the install alone (`visual-design T1`), as the `setting-maps` skill asks.

## T2 - Claude Code settings

- Look up the current permission-rule syntax for `.claude/settings.json` (allow, ask, deny;
  wildcards in Bash rules) in the Claude Code documentation before writing rules.
- Keep the existing SessionStart hook and the artgen allow rule.
- Allow without a prompt: `python3 tools/validate_setting.py`, `space.py`, `maps.py`,
  `metrics.py`, `build_site.py`, `build_pdf.py`, and `design.py` once it exists.
- Ask first: `node tools/artgen/artgen-maps.js report` with `--issue`, the `npx ...artgen-dist`
  installer, and `git push`. If the rule syntax cannot match `--issue` mid-command, ask for every
  `report` call.
- Check the file is valid JSON. Commit.

## T3 - the house look

1. Read `BRIEF.md`'s intro and `setting` node, and `tools/tables.py` `Brief`. Add a `look` line
   per map kind to the `setting` node's grammar (spec S11), with a sentence in `BRIEF.md`'s
   intro saying what it is. A missing `look` keeps today's drawing exactly.
2. Find every fixed style value: `dungeon.py` (`"style": {"hatch": "band", ...}`, `ROUTED_WALL`)
   and `maps.py` (`--theme color` in `render_fresh`, and the settlement and terrain renders). Read
   them from `look`, falling back to today's values.
3. Render three candidate looks in scratch on block `G.a` (the largest level) and `A.a` (a WILD
   settlement), each at 1600x1600px and at the PDF's 110x150mm: (a) today's black on white with
   `numbers: plain` and `doors: square`; (b) the `dark` preset; (c) a sand palette for the
   Lost City (warm rock, pale floor, dark brown ink) with the settlement `color` theme. Check each
   is legible at the PDF size.
4. **STOP.** Send the user the six PNGs and a one-line note on each. Wait for their pick or
   their changes.
5. Write their pick into `BRIEF.md`. Extend `tools/validate_setting.py` to reject an unknown preset,
   theme or a palette value that is not `#rrggbb`. Diff the site build against T0. Commit.

## T4 - schemas, step ids, voids, one place from another

- **Step ids.** In `tools/validate_setting.py`, let `TEMPLATE_STEP_CITE_RE` and `STEP_BODY_RE`
  take a suffix of one or more letters (`[a-z]+`). Check every other place that parses a step id
  (`grep -rn "\[a-z\]" tools/`), including `--pending`, `--read-set` and `--skeleton`. Then add
  step 3ca to `STEPS.md` as one line (its full wording comes in T8) and confirm the validator
  resolves it.
- **Design node.** In `patterns/Region_Schema.md`, define `Design` (spec S2) as a region file,
  `setting/region/[Code]/Design.md`, for any rating. Make `tools/tables.py` read and check it like
  the other table files. Fields marked `drawn` are the ones `design.py accept` writes.
- **Layout schema.** Write `patterns/Layout_Schema.md` (spec S4). Check that `tools/schema_graph.py`
  and `patterns.html` pick up a new schema file; extend them if not.
- **Void.** Add `Void` to `patterns/Safe_Schema.md` and `patterns/Wild_Schema.md`, shaped like
  DANGEROUS `Rock`. `tools/space.py` reports a location inside a void as a problem. `maps.py`
  draws a void as open ground in the settlement map.
- **`space.py from A to B`.** Prints distance (feet), compass bearing and climb between two
  codes from their absolute places. Unplaced ends are an error message, not a crash.
- Confirm the validator, `--check` builds and `space.py` are unchanged on the current setting.
  Commit.

## T5 - layout library and expansion

- Create `layouts/` with one file per layout: `cell-row`, `spine-ring-hub`, `axis-of-halls`,
  `suite`, `stair-vestibule`, `secret-bypass`. Write each from the structure table in
  image_tools `docs/DUNGEON-DESIGN.md` §2 (fetch it from `rstevenson1237/image_tools` at
  `86e957d`), in this repo's KDL. Give sizes as ranges in feet on the 5 ft grid. Set `source` to
  `drawn` with the map it came from.
- `tools/design.py layouts` lists them: id, tags, parameters, sockets.
- `tools/design.py expand CODE` reads `Design.md`. It expands each layout with its parameters,
  binds roles to codes, joins sockets as ways, adds fill rooms for codes no layout binds, and
  prints the `dungeon layout` graph JSON. Reuse `tools/dungeon.py` `graph_of` for frames, cells,
  pins (`over`) and `keepOut` from Rock; do not copy it.
- Test it on a hand-written `Design.md` for region C in scratch (not committed): six rooms round
  one hall, `axis-of-halls` plus fill. The graph must pass `dungeon layout` with every way routed.
- Commit the library and the two commands.

## T6 - SAFE/WILD solver spike

- Region A's block `A.a` is a WILD settlement of nine locations. In scratch, write a design for it
  with locations as building footprints and ways as streets, expand it, and run `dungeon layout`.
  Turn the result into a settlement file the way `maps.settlement_map` does, and render it.
- Write `plans/visual-design/spike-settlement.md`: what worked, what did not, and a picture.
- **STOP.** Show the user the render and recommend one of two options: (a) SAFE/WILD designs use the
  same solver; or (b) SAFE/WILD layouts state fixed geometry and are not solved. T7 builds the
  chosen one. Commit the spike note.

## T7 - solve, accept, check

- `design.py solve CODE [--seeds N=12] [--keep K=3]`: for each block, run the solver over N seeds,
  in a parallel pool when it is slow. Score each candidate against its design brief: location count, fill
  in range, every way routed, dead-end share, spacing (the median joined-room distance against
  `spacing`), detours against BRIEF.md's detour, and mirror symmetry when a layout asks for it.
  Render the best K to PNG in the house look, put them on one contact sheet, and print a score
  table with one line each on what the candidate trades off.
- Unbounded designs (spec S5): leave the footprint unset, centre on the block's `xyz`, and write the
  block's outline as the hull afterwards.
- `design.py accept CODE --seed S`: writes the candidate's places, ways, seed and score into
  `Design.md`. It never writes `approved`.
- `design.py check`: the agreement rules in spec S3, returning findings the validator prints with
  the step that owes each.
- Validator: call `design.check`. A region with `design` in BRIEF.md and no approved design is a
  warning owed by 3ca; `--pending` lists it.
- `maps.py pack` refuses a block with an approved design and names 3ca.
- `space.py` reads design places, so a design and a table that disagree on a place show in the
  dry fire as well as in the validator.
- Prove each agreement error fires on a scratch copy of the setting (change one `xyz`, drop one
  Connection, change a type) and is gone when the change is reverted. Commit.

## T8 - templates, steps, skill, docs

- `templates/region/Design.md`: Purpose / Context / Instructions, with a KDL Context fence
  (`templates/Template_Schema.md`) that reads the region's `BRIEF.md` node, `Seed.md`, `GENRE.md`
  and `layouts/`, and writes `Design.md`.
- `templates/region/Locations.md` and `Connections.md`: read `Design.md` where it exists. Codes,
  types, places, shapes and ways come from it; names, write-ups and what stands in a way do not.
- `STEPS.md`: the full wording of 3ca (design the blocks of each region whose `BRIEF.md` node
  has `design`: write the design, solve, show the user the candidates, accept their pick), and the
  4a note that a designed block is not packed. Change no other step id.
- `templates/checks/Map_Judgement_Check.md`: one item, per designed block, "the drawing reads
  as the approved design".
- `.claude/skills/block-design/SKILL.md` (spec S8). Its description says when to use it: step
  3ca, choosing layouts, or changing a design. Give the commands and the order; point at the
  `dungeon-map` skill for artgen keys and at `layouts/` for the library.
- `CLAUDE.md`: amend the maps line (spec S13). `README.md`: `layouts/`, `Design.md`,
  `tools/design.py`, the skill, `space.py from`.
- Run `python3 tools/validate_setting.py --read-set 3ca` and `--skeleton 3ca E` and check the output.
  Commit.

## T9 - pilot on region E

Region E (level 3) is a turning hall with eight passages to three faction complexes: it is
`spine-ring-hub` and `cell-row`. It is packed today, so the pilot rewrites its places.

1. Add a `design` line to region E in `BRIEF.md`. Using the `block-design` skill, write
   `setting/region/E/Design.md` with E's fifteen codes and today's types.
2. Run `design.py solve E`. **STOP.** Show the user the contact sheet beside today's E map (from
   T0), with the score table. Wait for their pick, or for changes to the design and another solve.
3. `design.py accept E --seed <pick>`. Set `approved` only when the user says so.
4. Rewrite E's tables to agree: places and shapes in `Locations.md`, ways in `Connections.md`,
   `Blocks.md` and Rock. Run step 4b for every E write-up whose directions or neighbours changed,
   and 4c until clean. **STOP** before rewriting any write-up's prose beyond the lines its changed
   entries touch, and show the user the list.
5. Run `space.py settle E` and the dry fire; fix what it reports in the content.
6. Commit. Record in this folder what the pilot changed and what it showed about the layouts.

## T10 - the artgen report

- `report-artgen.md` in this folder is a draft. Bring it up to date with what T5 to T9 found:
  which layouts needed which constraints, how unbounded designs behaved, the SAFE/WILD spike.
- **STOP.** Show the user the report. Only on their word, open it as an issue on
  `rstevenson1237/image_tools` with the label `artgen-feedback`, or give them the text to paste.

## T11 - close

- `python3 tools/metrics.py > plans/visual-design/metrics-after.txt`, and compare with
  `metrics-before.txt`.
- Re-read every framework file this plan changed and cut what is not needed.
- Commit and push.

## Risks

- **The solver ignores layout shape.** A flexible layout only states rooms and ways, so the
  annealer may pack a cell row as a cluster, not a row. Use `against` and `over` pins to hold
  shape where it matters, and score shape in `solve`. What still cannot be held goes to the
  report as a constraint request.
- **Unbounded designs come out square.** An unset footprint is the least square, not growth from
  a point. Accept that for now; the report asks for growth.
- **The pilot changes content.** E's write-ups were checked at step 5. Rewriting E's places can
  make them stale. The STOPs in T9 keep the user in charge of how far that goes.
- **Step-id regex.** Widening it could match prose by accident. Check that the set of resolved
  citations before and after is the same, plus 3ca.
