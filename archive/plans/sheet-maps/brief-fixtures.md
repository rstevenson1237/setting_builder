# Brief - consumer fixtures and a format version (artgen)

For an artgen session in `rstevenson1237/image_tools`, from setting_builder's sheet-maps plan
(`implementation.md` T0.3; `spec.md` 12.2 items 2 and 4). It is the first brief. A1 to A8
follow, and each one adds its own cases to these fixtures.

A consumer needs two things from artgen. Its real maps must be in artgen's tests, so no later
change breaks them unseen. And it must know which file and JSON shapes it reads, so a change
that breaks one is announced, not found later.

## 1. Format version

`map.json` and `dungeon.json` already carry `version: 1`, but `parseMap` and `parseDungeon`
overwrite it (`version: 1` in the merge), so a newer file is read as version 1 without any
error. The format version follows the same rule as the animation contract
(`w2/contract.ts`): additions extend it, anything else is a break.

- **Read it, don't overwrite it.** A file without a version reads as 1. A file at a version
  older than the tool's is migrated on read. A file at a newer version is refused, with an
  error naming both versions.
- **Report it.** `artgen formats --json` prints `{"map": 1, "dungeon": 1}`. Every `--json`
  result from a `map` or `dungeon` command carries the `version` of the format it reports
  on, as A3's `facts` will.
- **What breaks.** Removing or renaming a field, changing a field's meaning, unit or
  default, or making a field required. Adding an optional field or an enum value is an
  extension, and a consumer ignores what it does not know.
- **A break bumps the version** in the same change: a migration from the previous version,
  the consumer fixtures migrated with it, and a CHANGELOG line (`map format 1 -> 2: ...`).

## 2. Consumer fixtures

A folder of fixtures per consumer, placed the way artgen places its fixtures. This consumer's
is `setting-builder/`, with one folder per case. Each case holds:

- the input file, as the consumer's converter wrote it;
- `case.md`: the setting_builder commit and the exact command it was built with, what it must
  go on drawing (the facts below), and what it does not yet draw well.

### Building them

Clone setting_builder at the head of the branch carrying this brief (or `main` once merged).
Record the sha in each `case.md`. Install artgen from this checkout's own build into a scratch
game directory, then run, from the setting_builder root:

```sh
python3 plans/sheet-maps/prototype/to_dungeon.py F <game> F.1=8x1 F.2=8x1 F.3=6x6 F.4=4x3 F.5=3x2
python3 plans/sheet-maps/prototype/to_map.py E <game> 10 <edits>
python3 plans/sheet-maps/prototype/to_dungeon.py A <game> A.1=8x2 A.2=2x1 A.3=8x4 A.4=6x4 \
  A.5=6x2 A.6=5x4 A.7=3x2 A.8=16x16 A.9=8x4 A.10=10x5 A.11=12x5 A.12=6x3 A.13=30x1
node tools/artgen/artgen.js dungeon style a --hatch none     # in <game>
```

Room sizes are in 5 ft cells, taken from each region's `Brief.md`. No table states them yet;
T3.2 adds them. Take `<edits>` from the ravine row below, in map units around the origin that
`to_map.py` prints.

### The cases

| Case | Input | What it is | Facts the test holds it to |
|---|---|---|---|
| `warren` | `dungeon.json` of F | One block: five rooms, an exit, two traps | Rooms numbered 1-5 at 8x1, 8x1, 6x6, 4x3, 3x2. Corridors F.1-F.2 and F.2-F.3 open, F.3-F.4 and F.3-F.5 doors. One corridor from F.1 to a point labelled `to E.2`. Two trap symbols. |
| `ravine` | `map.json` of E at 10 yards a square | A 1-mile gorge, 80 yards wide, with its mouths as marks. The ground is hand-painted, because no table states any: a river up the path and rock walls raised 4 squares either side (`map edit` `river`, `elevate`, `paint rock`) | 10 yards per cell. A symbol and a label for every location but the route E.1. One road along the stops. |
| `keep` | `dungeon.json` of A, hatching off | Thirteen buildings and gates in one ward, laid out at their places | 13 rooms at the sizes above. `hatch: none`. A.12 and A.13 lie under A.4 and A.10 and overlap them until Blocks split them by level (T3.2). The test asserts nothing about that overlap. |

### The tests

For every case:

- it parses at the format version its `case.md` states;
- it renders to SVG and PNG, in each theme the format has, without error, and renders the
  same twice;
- its facts hold.

The tests check structure, never pixels. A theme, font or symbol may change how a fixture
looks, but never what it states.

A fixture changes only through a brief from its consumer, or through a format bump that
migrates it in the same change. A failing fixture is never edited just to make it pass.

## Done when

- A newer-version file is refused, a file without a version reads as 1, and `formats --json`
  prints both versions, each covered by a test.
- The three cases are committed and their tests run with artgen's own suite.
- The CHANGELOG names both, and states the format versions this release reads.

## setting_builder's side

- Reads: `map` format 1 and `dungeon` format 1.
- Pinned: none yet. T3.1 pins artgen by commit, records the commit here, and checks
  `formats --json` before any map is built.
