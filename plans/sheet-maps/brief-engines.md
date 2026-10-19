# Brief - the map and dungeon engines usable alone (artgen A1)

For an artgen session in `rstevenson1237/image_tools`, from setting_builder's sheet-maps plan
(`implementation.md` T2.1; `spec.md` 9 A1 and 12). It follows `brief-fixtures.md`, which has
landed: the formats are versioned and `fixtures/setting-builder/` holds `warren`, `ravine` and
`keep`.

setting_builder is a Python repo with no package manager. Its builders will call artgen as a
subprocess for maps and dungeons and nothing else. Today that needs the whole committed install,
and a project folder it does not have.

## What phase 1 found

- **A project is required.** Every `map` and `dungeon` command finds `art/artgen.config.json`
  up the tree and takes an id, never a path (`map.ts` `mapFile`). setting_builder commits each
  map where its tables are (`setting/region/F/F.a.json`, `setting/Frontier.json`), so the
  prototype had to build a scratch game and copy files in and out.
- **One process per change.** The prototype ran one `node` process per room, link, label and
  symbol: about 25 for F, over 60 for the Keep.
- **The install is too large for the need.** The committed install brings skills, agents,
  commands, a `CLAUDE.md` section, the MCP server and the runtime. A map consumer uses none of
  them. `artgen.js` is 964 KB with every pipeline in it, and `resvg.wasm` (2.5 MB) is needed
  only for PNG. setting_builder renders SVG for its site and PDF.

## What to build

1. **Path mode.** Every `map` and `dungeon` command takes `--file <path>` in place of an id,
   and then needs no project. Renders go to `--out`, which defaults to the file's folder. Ids
   keep working inside a project.
2. **A whole file in one call.** A consumer writes the JSON itself, at a format version
   `formats --json` reports, then calls:
   - `artgen dungeon check --file F.a.json --json`, which lists every error with its JSON
     path. `map check` is A2's, and adds its requirements to this.
   - `artgen dungeon fit --file …` and `artgen map render --file … --format svg`.

   The file format is the contract, so the per-change commands become a convenience.
3. **A maps-only bundle.** `artgen-maps.js` holds `map`, `dungeon` and `formats`, and nothing
   that loads the pixel-art pipeline. It is built beside the full bundle and published on
   `artgen-dist` under `maps/`, with `VERSION`, the fonts and `resvg.wasm` as separate files.
   SVG renders without `resvg.wasm`. A PNG render without it fails, naming the missing file.
   Fonts are optional: without them, labels fall back to the CSS font list already in the
   renderer.
4. **Installable at a commit.** A consumer copies `maps/` from `artgen-dist` at a sha into its
   own `tools/artgen/` and commits it. Nothing runs at install. `artgen-maps.js --version`
   prints the release and the sha it was built from.

## The cases

Add these to `fixtures/setting-builder/`, keeping the three cases already there:

| Case | What it is | Facts the test holds it to |
|---|---|---|
| `warren` (exists) | Now also run through path mode, with no project | `dungeon check --file` reports no errors; render by `--file` matches render by id |
| `shrine-crypts` | M's crypt block (M.6 to M.9, M.13), written whole by the consumer as `dungeon.json`, then run through `fit` | Five rooms; corridors M.6-M.7, M.7-M.8, M.7-M.9, and M.13-M.8 with a secret door at M.8; three exits labelled `up to M.2`, `up to M.10` and `down to L.5`; `check` reports no errors |
| `bad-file` | `warren` with a corridor to a room id that does not exist, and a room 0 cells wide | `check` exits non-zero and names both errors by JSON path |

Build `shrine-crypts` by hand from `setting/region/M/Connections.md` and the sizes in
`setting/region/M/Brief.md`. No table states sizes yet (T3.2 adds them). Record the
setting_builder sha in its `case.md`.

## Done when

- Every `map` and `dungeon` command runs by `--file` from an empty folder, each covered by a
  test.
- `artgen-maps.js` builds, runs the fixtures with SVG output and no `resvg.wasm`, and its size
  is in the CHANGELOG beside the full bundle's.
- `artgen-dist` holds `maps/`, and the CHANGELOG says how a consumer copies it at a sha.

## setting_builder's side

- T3.1 copies `maps/` at a sha into `tools/artgen/`, records the sha here, adds `node` to CI,
  and checks `formats --json` before any map is built.
- `tools/maps.py` writes each map's JSON, calls `check`, `fit` and `render` by `--file`, and
  reads every result as `--json`.
- Pinned: `artgen-dist` `fbde602523a947197d0db7155d88b093d2eb2cbb` (artgen 0.10.0, built from
  `da9eb9c`), copied whole into `tools/artgen/` at T3.1.
