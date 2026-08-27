# External

The only backlog. Capped at one page. A row here is a dependency on something
outside this repository: a decision the developer owes, a file that has to come
from elsewhere, or a tool that is not written yet.

A build-time question does not belong here. It belongs in the step's opening
question batch. A production rule does not belong here either; it belongs in the
pattern that enforces it.

| Item | Needed by | Note |
| :--- | :--- | :--- |
| The ruleset the setting targets | Milestone 6 | Not in this repository and never read by a pattern. `MECHANICS.md` is the whole interface, and swapping it retargets the setting. Steps 1 to 4 have now written tokens across twenty-four tables against a provisional map, and the region tables have now been written against it too, so the pass against the real ruleset is owed before the locations are. |
| The location patterns, `traps.md` and `hoards.md` | Milestone 6 | The setting, table and region patterns exist. `patterns/location/` does not, and nothing generates a location yet. |
| Hand-written test content in `setting/regions/` | Milestone 6 | `R03-L03` and `R03-L07` are a fixture written to exercise the checks, and they predate `GENRE.md`. Every region is now generated and is canon. The two locations are still a shape to check against, and steps 9 to 12 replace them. |
