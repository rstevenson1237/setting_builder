# Intake - friction a fuller Keep on the Borderlands meets

`BRIEF.md` asks for 13 regions and 94 locations: a SAFE keep, four WILD regions, six tribal
holdings, a maze and a shrine. Each item below was read from the framework against that
brief, not observed in a build; the first build's checks (Roadsend) are cited where they
already found it. Each names where it lives and what the brief does about it.

## Structure the brief needs and the schemas lack

| # | Friction | Where | Effect on this build |
|---|---|---|---|
| 1 | "Faction Turn" is cited and never defined. | `templates/setting/Factions.md` Tactics; no section of `templates/setting/Procedures.md`. | Eleven factions with Tactics that act on a turn nothing runs, and Relation dice (d4 to d12) that nothing rolls. |
| 2 | Landmarks are still not joined. | `Wild_Schema.md` `top Landmark Route`, "never joined". | `at` and Layout give each landmark's distance from the way in, not what sees or hears what from the next one along the ravine. |
| 3 | An alarm stops at its region's edge. | `Region_Schema.md` Dangerous `Alarm` and the per-region Danger track; Roadsend: nothing records noise. | Six neighbouring holdings cannot hear one another. |

## Rules that bite at this size

| # | Friction | Where | Effect on this build |
|---|---|---|---|
| 4 | Rates are closed lists. | `tools/tables.py` `_check_rates` reads an unlisted table as 0-0. | A `procedure` line cannot be placed at a Bank, Market, Merchant or any DANGEROUS room. The brief adds `Procedures` to those rates; no template says to. |
| 5 | A region target replaces the rating's whole target of the same key. | `tools/tables.py` `Brief.realized`, keyed on path, form and `of`. | Naming `Hoards=1` in a region silently drops its Keys and Lore shares, so each region restates them. |
| 6 | A rating-wide percent mix is noise on a small region. | Roadsend `Review.md`: one of six is "the nearest whole count". | Every holding uses counts, which leaves the rating default unused. |
| 7 | `BRIEF.md` is read whole by every step. | Every template's Context; analysis below. | It grew from 717 to 2,321 words (about 3,600 tokens); a location write-up's context from 5,646 to 7,396. |
| 8 | Tongue uniqueness cannot hold past two. | `Setting_Schema.md` Language: Syllable "open or closed, unlike the others'". | GENRE gives each alignment a tongue, so Law, Neutrality, Chaos and the makers make four. |
| 9 | Danger and Difficulty are both "the die". | `Region_Schema.md` Brief Tables "d6 Danger"; Roadsend's Procedures called it "the Danger die of a DANGEROUS region". | Read as the region's die, K, L and M (d4) cannot reach bands 6 and 5. |

## Tooling

| # | Friction | Where | Effect |
|---|---|---|---|
| 10 | The site and PDF builders crash on an empty `setting/`. | `tools/site_common.py` `parse_setting` reads `Setting.md` unguarded; `README.md` says they build empty. | `validate.yml` fails every pull request on a wiped setting. `setting/.gitkeep` keeps the directory; the crash stays. |
| 11 | Carried from Roadsend, now larger. | `Hoards.Total` is hand-summed and unchecked; Lethality needs a hazard that uses it. | Seven hoards; the brief asks for Lethal poison. |

## `BRIEF.md` as a `CLAUDE.md` import

At present, every template's Context names `BRIEF.md` and the validator requires it
(`STANDING_CONTEXT`). Importing it (`@BRIEF.md` in `CLAUDE.md`) would load it once, and
those 27 lines and the check would go.

| For | Against |
|---|---|
| It survives compaction and is present in a fresh reviewing context (5c), where a skipped read is silent. | It loads on every request, generation or not: about 3,600 tokens. Inside a generation step the saving is nil, as the template's read costs the same. |
| One place states that it is always read. | The edit goes unseen if the import is not refreshed mid-session; `BRIEF.md` is edited directly by the user, so a stale brief would build to a superseded spec. Unverified: test by editing it and asking what it says. |
| | `CLAUDE.md` holds "only what must be re-checked each time"; `GENRE.md` and `STYLE.md` are re-read, not imported, for that reason. |
| | It does not touch the waste: a region's step needs the header, levers, `setting` and its own node, 1,350 of 2,321 words (levers 243, `setting` 885, a region 81 on average). |

Not changed. The slice is the larger saving, and needs `tables.py` to read more than one
file. If the import goes ahead, the edit set is `CLAUDE.md`, the Context line of each
template, `STANDING_CONTEXT`, and `metrics.py`'s read set.

## Baseline

Roadsend: 14 locations, 173 words mean per write-up, 12,329 words in `setting/`. This
brief: 94 locations, about 16,000 words of write-ups at the same mean, 13 regions against 3
and 11 factions against 2, so the tables, seeds, briefs and registries grow with them.
