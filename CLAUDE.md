# CLAUDE.md

Loaded on every request; it holds only what must be re-checked each time.

- Re-read `GENRE.md` and `STYLE.md` at every generation step.
- Every framework file is the minimal set. After writing one, review it: state it more
  simply and more generally where possible, and cut any line that records work trajectory,
  restates what is true elsewhere, or enforces an edge case as the general rule. Decisions
  and their reasons belong in git history.
- Extend `tools/validate_setting.py` alongside any new artifact type or template rule.

<!-- artgen:begin — managed by the artgen installer; `update` rewrites this section -->
- Maps are built from the tables by `tools/maps.py` and never edited by hand: the
  `setting-maps` skill says how, and when artgen's own map skills apply.
- artgen's CLI here is `node tools/artgen/artgen-maps.js`, always with `--file <path>`: this
  repo has no `art/` project and no `artgen.js`, whatever an installed artgen file says.
<!-- artgen:end -->
