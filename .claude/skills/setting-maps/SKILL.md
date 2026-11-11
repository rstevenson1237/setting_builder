---
name: setting-maps
description: How this framework draws its maps with artgen - the sheets, each region's ground, a DANGEROUS block as a dungeon and a SAFE or WILD block as a settlement - all built from the tables by tools/maps.py, and what it writes into each artgen file and why. Use when a step places regions, writes Ground.md, packs a block or draws maps; when a map looks wrong or the validator reports one; when changing tools/maps.py or dungeon.py; when something artgen draws should be reported upstream; or when upgrading artgen.
---

# Maps

The tables and `BRIEF.md` are the source. Every map file is built from them, is never
committed and is never edited by hand: a wrong map is fixed in a table, a `BRIEF.md` line or
the converter, then built again.

## Building

| Step | Command | Writes |
|---|---|---|
| 3b | `python3 tools/maps.py place` | `setting/Sheets.md`, `setting/[Sheet].json`, each region's `outline` and `xyz` |
| 3b, 3g | `python3 tools/maps.py ground` | each placed region's `Ground.md` |
| 3d | `python3 tools/design.py` (the `block-design` or `block-plan` skill) | a designed block's places, in `Design.md` |
| 4a | `python3 tools/maps.py pack [Code]`, then `python3 tools/space.py settle [Code]` | each room's `xyz`, each block's `outline`; not for a block with an approved design; `python3 tools/plan.py apply [Code]` for an approved plan |
| any | `python3 tools/maps.py draw [--out DIR]` | `setting/region/[Code]/[Block].json`, and the SVGs with `--out` |

A request `place` or `map check` reports unmet goes to `BRIEF.md`, not to a new seed. The
validator and both builders' `--check` run every map through artgen; their findings name the
step that fixes them.

## The engine

- `tools/artgen/` is artgen's `maps` module. Its CLI is `node tools/artgen/artgen-maps.js`,
  always with `--file <path>`: this repo has no `art/` project, so the steps of artgen's skills that need one
  (`new <id>`, `brief`, `version`, `review`, `approve`, `ui`) do not apply. The converters call it through `maps.artgen()`.
- What a file can say: artgen's `dungeon-map`, `dungeon-design`, `settlement-map` and `terrain-map` skills, and
  `schema <kind> --keys` for how each key behaves (`schema dungeon --checks` for the ids `check` gives).
- To read a map without drawing it: `dungeon facts`, `map facts --at x,y`, `check`, each with
  `--json`. To look at one: `render --file F --format png --out <scratch dir>`, then view the PNG.

## What the framework writes, and why

**A packed block** (`maps.py pack`, `dungeon.graph_of`): a `dungeon layout --graph`, not a file. Rooms in 5 ft cells, each way
with the bearing it keeps; a room `against` another, a stair's room `over` the room it meets, Rock as `keepOut`, a poly
outline as the footprint, BRIEF.md's fill, passages and detour. The `report` (`left`, `detours`) is what the validator holds
to BRIEF.md's detour. **A designed block** (step 3d) is an artgen design instead, laid out by `dungeon layout --design`.
**An approved plan** (`plan.block_map`) is its own solve: rooms where the plan put them, each passage along the squares
it was routed on (a branch joins its trunk as `{corridor}`, a way off the map is an `exit` end), each door the kind the
tables' Connection gives it; its ground and fill are the Design line's, not the `pack` line's.

**A block's map** (`dungeon.block_map`):

| Key | What, and why |
|---|---|
| `scale.perCell` | 5 ft a cell, so a 10 ft passage is `width: 2`. |
| `rooms[].shape` | `rect`, `circle`, `cave`, `octagon` (`cut` 1/(2+√2), so a square one is regular) and `hexagon` as themselves; a `poly` outline as a `poly`. |
| `rooms[].number` | `false`: the code alone labels a room. |
| `corridors[]` | Where two rooms do not touch: `route: "maze"`, `width: 2`, its ends `{room, side}` at the wall the Connection names, else `{room}`. Written shortest first, as `dungeon layout` routed them, so the map draws the passages `pack` measured. |
| `connections[]` | A door or opening where two rooms touch. |
| `rooms[].exits` | Each way out of the block, a stair or arrow by the wall facing it, with a note naming the way. |
| `bounds`, `areas[]` | A block's poly outline, and each of its Rock as a `rock` area. |
| `style` | `BRIEF.md`'s `maps` look; on a packed level `wall: 2.5` and `hatch: full`; shared walls on by default. |
| `furniture.place` | `outside`, so nothing stands on the map. |
| `overlay` | A trap in the middle of its way, or in its doorway. |

The validator reads the file back with `dungeon check --errors <ids>` (the ids are `dungeon.FAULTS`; `dungeon.SEEN` the
warnings it passes on) and `dungeon facts` (each passage's `path`, its doors, `unreached`, each room's `exits`), held to
the tables' ways. The location cuts are `render --room CODE --margin N`.

**A SAFE or WILD block** (`maps.settlement_map`): `kind: castle` with the block's own walls where it has them, rather than
the engine's; each location as a `buildings[]`, `areas[]`, `water[]` or `roads[]` entry by its type and the words of its
name, a Gate as the wall's gate; the home sheet's terrain map as the `underlay`.

## When artgen is wrong

Gaps already reported are image_tools' issues labelled `artgen-feedback`. For a new one:

```sh
node tools/artgen/artgen-maps.js report --file setting/region/G/G.a.json --note "what is wrong" --made-by "python3 tools/maps.py draw"
```

It writes `artgen-feedback/<date>-<id>/` (ignored by git): the file, the render, the versions,
`case.md` and `ISSUE.md`, and sends nothing. Show the user; only when they agree, run it again
with `--issue`, which opens the issue on the artgen repo with `GH_TOKEN` or `GITHUB_TOKEN`, or
prints a link without one. A cloud session's token is not one GitHub's API takes (it answers 401):
there, give the user the link, with `ISSUE.md`'s body to paste where it is too long for one. That repo
turns each report into a consumer fixture each release is tested on.

## Upgrading artgen

```sh
npx -y github:rstevenson1237/image_tools#artgen-dist-v<version> update --no-scaffold --notes <scratch dir>/notes.md
```

Pin the release tag. The installer replaces the files it installed, keeps any edited here, writes its section of
`CLAUDE.md`, and with `--no-scaffold` makes no `art/` project. Before it, keep the validator's output and a site build
and the block maps (`maps.py draw --out`); after it, run the validator, `space.py` and both `--check`s, and compare the
maps. Commit the install alone. Then read the release notes for anything the framework now does round a fault the engine
fixes, try it without the workaround, and drop the workaround where `check` finds no more. Map caches key on the bundle's
hash (`maps.BUILD`), so a new build draws everything again.
