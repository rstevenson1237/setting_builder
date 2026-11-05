# CLAUDE.md

Loaded on every request; it holds only what must be re-checked each time.

- Re-read `GENRE.md` and `STYLE.md` at every generation step.
- Every framework file is the minimal set. After writing one, review it: state it more
  simply and more generally where possible, and cut any line that records work trajectory,
  restates what is true elsewhere, or enforces an edge case as the general rule. Decisions
  and their reasons belong in git history.
- Extend `tools/validate_setting.py` alongside any new artifact type or template rule.
- Maps are built from the tables by `tools/maps.py` and never edited by hand: the
  `setting-maps` skill says how, and when artgen's own map skills apply. A designed block's tables
  follow its approved design (step 3d, the `block-design` skill); its map is still built from the tables.

<!-- artgen:begin — managed by the artgen installer; `update` rewrites this section -->
## Sending feedback back to artgen
- A render that is wrong, or something artgen can't do yet: `node tools/artgen/artgen-maps.js report --file <map, dungeon or settlement file> --note "what is wrong" --made-by "<the command that wrote the file>"`
  writes `artgen-feedback/<date>-<id>/` at the repo root (git ignores it): the file, its render, the versions and a `case.md`, plus `ISSUE.md`, the
  text of the issue. Nothing is sent: show the user the folder, and only when they agree run it again with `--issue` (or give them the link it prints).
- A fix you made to an installed skill or command (`/artgen-upstream`): `node tools/artgen/artgen-maps.js upstream` writes your local edits as a patch against their
  sources in the artgen repo, so the edit is not lost at the next `update`.

## Tabletop maps (artgen)
- This repo writes its own map files and names each with `--file <path>`: `node tools/artgen/artgen-maps.js <map|dungeon|settlement> <command> --file <path> --json`.
  There is no `art/` project, so the steps that need one (`new <id>`, `brief`, `version`, `review`, `approve`, `ui`) do not apply.
- The **terrain-map**, **dungeon-map** and **settlement-map** skills say what each file can hold; `artgen schema <kind> --keys` lists every key.
  `check --json` lists the file's errors and warnings (each with an `id`), `facts --json` reads it back as numbers.
<!-- artgen:end -->
