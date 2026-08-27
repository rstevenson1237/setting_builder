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
| `tools/mermaid_gen.py`, `tools/build.py` | Milestone 5 | Until they exist, M11 is skipped and M13's marker resolution is deferred. |
| The setting, region, location and table patterns | Milestones 4 to 6 | `patterns/GENRE.md` and the genre pattern exist. Nothing else generates content yet. |
| Hand-written test content in `setting/` | Milestone 4 onward | The Ashen Reach, `R03` and its two locations are a fixture written to exercise the checks, and it predates `GENRE.md`. Steps 1 to 4 regenerate the setting and the tables, and steps 5 to 12 the regions and locations. Until then the fixture is a shape to check against and not setting canon. |
