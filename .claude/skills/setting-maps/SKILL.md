---
name: setting-maps
description: How this framework draws its maps with artgen - the sheets, each region's ground, a DANGEROUS block as a dungeon and a SAFE or WILD block as a settlement - all built from the tables by tools/maps.py. Use when a step places regions, writes Ground.md, packs a block or draws maps; when a map looks wrong or the validator reports one; when changing tools/maps.py or dungeon.py; when something artgen draws should be reported upstream; or when upgrading artgen.
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
| 4a | `python3 tools/maps.py pack [Code]`, then `python3 tools/space.py settle [Code]` | each room's `xyz`, each block's `outline`; not for a block with an approved design (3d) |
| any | `python3 tools/maps.py draw [--out DIR]` | `setting/region/[Code]/[Block].json`, and the SVGs with `--out` |

A request `place` or `map check` reports unmet goes to `BRIEF.md`, not to a new seed. The
validator and both builders' `--check` run every map through artgen; their findings name the
step that fixes them.

## The engine

- `tools/artgen/` is artgen's `maps` module. Its CLI is `node tools/artgen/artgen-maps.js`,
  always with `--file <path>`: this repo has no `art/` project. The converters call it through
  `maps.artgen()`.
- What a file can say: artgen's `dungeon-map`, `settlement-map` and `terrain-map` skills, and
  `schema <kind> --keys` for how each key behaves. What the framework writes, and why:
  `references/what-we-write.md`. The skills' project steps (`new <id>`, `brief`,
  `version`, `review`, `approve`, `ui`) need `art/` and do not apply here.
- `pack` lays a block out with `dungeon layout --graph`; its `report` (`left`, `detours`) is what
  the validator holds to BRIEF.md's detour.
- The validator reads a block's file back with `dungeon check --errors <ids>` (the ids are
  `dungeon.FAULTS`; `schema dungeon --checks` lists them all) and `dungeon facts` (each passage's
  `path`, its doors, `unreached`, each room's `exits`), held to the tables' ways.
- To read a map without drawing it: `dungeon facts`, `map facts --at x,y`, `check`, each with
  `--json`. To look at one: `render --file F --format png --out <scratch dir>`, then view the PNG.

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
npx -y github:rstevenson1237/image_tools#artgen-dist update --no-scaffold --notes <scratch dir>/notes.md
```

It replaces the files as installed, keeps any edited here (`status` lists them), and with
`--no-scaffold` makes no `art/` project. In a commit of its own, run the validator and both `--check`s, compare
a site build from before and after, and check `artgen-capabilities.md` against the new engine.
Map caches key on the bundle's hash (`maps.BUILD`), so a new build draws everything again.
