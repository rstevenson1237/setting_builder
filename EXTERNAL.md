# External

The only backlog. Capped at one page. A row here is a dependency on something
outside this repository: a decision the developer owes, a file that has to come
from elsewhere, or a tool that is not written yet.

A build-time question does not belong here. It belongs in the step's opening
question batch. A production rule does not belong here either; it belongs in the
pattern that enforces it.

| Item | Needed by | Note |
| :--- | :--- | :--- |
| The ruleset the setting targets | Milestone 5 | Not in this repository and never read by a pattern. `MECHANICS.md` is the whole interface, and swapping it retargets the setting. Steps 1 to 4 have now written tokens across twenty-four tables against a provisional map, so the pass against the real ruleset is owed before the region tables are written. |
| `tools/mermaid_gen.py`, `tools/build.py` | Milestone 5 | Until they exist, M11 is skipped and M13's marker resolution is deferred. |
| The region and location patterns | Milestones 5 and 6 | The four setting patterns and the twenty-four table patterns exist. `patterns/region/` and `patterns/location/` do not, and nothing generates a region or a location yet. |
| Hand-written test content in `setting/regions/` | Milestone 5 onward | `R03` and its two locations are a fixture written to exercise the checks, and they predate `GENRE.md`. The setting scale and the tables are now generated and are canon; the region and its locations are still a shape to check against, and steps 5 to 12 replace them. |
