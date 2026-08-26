# External

The only backlog. Capped at one page. A row here is a dependency on something
outside this repository: a decision the developer owes, a file that has to come
from elsewhere, or a tool that is not written yet.

A build-time question does not belong here. It belongs in the step's opening
question batch. A production rule does not belong here either; it belongs in the
pattern that enforces it.

| Item | Needed by | Note |
| :--- | :--- | :--- |
| The ruleset the setting targets | Milestone 4 | Not in this repository and never read by a pattern. `MECHANICS.md` is the whole interface, and swapping it retargets the setting. Its current token map is provisional and wants one pass against the real ruleset. |
| `tools/resolve_deps.py`, `tools/router.py` | Milestone 2 | Selectors, the S boundary, the genre cap, and `DESIGN_PATTERNS.md`. |
| `tools/mermaid_gen.py`, `tools/build.py` | Milestone 5 | Until they exist, M11 is skipped and M13's marker resolution is deferred. |
| `patterns/` | Milestones 2 to 6 | The tree is empty. Nothing generates content yet. |
| Hand-written test content in `setting/` | Milestone 5 onward | `R03` and its two locations are a fixture written to exercise the checks. Steps 5 to 12 regenerate them. |
