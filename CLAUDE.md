# CLAUDE.md

Loaded on every request; it holds only what must be re-checked each time.

- Re-read `GENRE.md` and `STYLE.md` at every generation step.
- Every framework file is the minimal set. After writing one, review it: state it more
  simply and more generally where possible, and cut any line that records work trajectory,
  restates what is true elsewhere, or enforces an edge case as the general rule. Decisions
  and their reasons belong in git history.
- Extend `tools/validate_setting.py` alongside any new artifact type or template rule.
