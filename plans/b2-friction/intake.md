# Intake - friction a fuller Keep on the Borderlands meets

`BRIEF.md` asks for 13 regions and 94 locations: a SAFE keep, four WILD regions, six tribal
holdings, a maze and a shrine. Each item below was read from the framework against that
brief, not observed in a build; the first build's checks (Roadsend) are cited where they
already found it. Each names where it lives and what the brief does about it.

## Structure the brief needs and the schemas lack

| # | Friction | Where | Effect on this build |
|---|---|---|---|
| 1 | A SAFE region holds no creature or faction. | `patterns/Safe_Schema.md` has no Encounter, Creature or Faction node; `templates/region/Tables.md` places a seed's occupants "as Encounters". | The keep's garrison, the carters' guild and the cult's agents have no table to stand in. |
| 2 | A Person carries no allegiance or hidden aim. | `Person.wants` is "of a stranger"; `Secret` gates a place, not a person. | The two cult agents in the keep cannot be recorded; they can only be hinted through a Secret location. |
| 3 | Factions have no relations. | `Setting_Schema.md` Factions: `Want rival` is a want, not a link. | "Goblins fight orcs, hobgoblins fight gnolls" is the ravine's whole play, and lives in prose no check can compare between the two entries. |
| 4 | "Faction Turn" is cited and never defined. | `templates/setting/Factions.md` Tactics; no section of `templates/setting/Procedures.md`. | Eleven factions with Tactics that act on a turn nothing runs. |
| 5 | Identity marks are placed nowhere. | `Setting_Schema.md` Factions Identity; found in Roadsend's Schema check. | Twenty-two marks. A tribe's mark is how a party tells one cave from the next. |
| 6 | Landmarks have no adjacency or order. | `Wild_Schema.md` `top Landmark Route`, "never joined"; Roadsend: a Route has no order. | The ravine is nine landmarks in a line where order and what can see what is the design. |
| 7 | An alarm stops at its region's edge. | `Region_Schema.md` Dangerous `Alarm` and the per-region Danger track; Roadsend: nothing records noise. | Six neighbouring holdings cannot hear one another. |

## Rules that bite at this size

| # | Friction | Where | Effect on this build |
|---|---|---|---|
| 8 | Rates are closed lists. | `tools/tables.py` `_check_rates` reads an unlisted table as 0-0. | A `procedure` line cannot be placed at a Bank, Market, Merchant or any DANGEROUS room. The brief adds `Procedures` to those rates; no template says to. |
| 9 | A region target replaces the rating's whole target of the same key. | `tools/tables.py` `Brief.realized`, keyed on path, form and `of`. | Naming `Hoards=1` in a region silently drops its Keys and Lore shares, so each region restates them. |
| 10 | A rating-wide percent mix is noise on a small region. | Roadsend `Review.md`: one of six is "the nearest whole count". | Every holding uses counts, which leaves the rating default unused. |
| 11 | `BRIEF.md` is read whole by every step. | Every template's Context. | It grew from 717 to 2,209 words; a location write-up's context from 5,646 to 7,138. Only `files`, its rating, `setting` and its own region node are used. |
| 12 | Tongue uniqueness cannot hold past two. | `Setting_Schema.md` Language: Syllable "open or closed, unlike the others'". | GENRE gives each alignment a tongue, so Law, Neutrality, Chaos and the makers make four. |
| 13 | Nothing sequences regions in step 5. | `STEPS.md` 5a-5d; `--pending [REGION]` exists. | The keys run J to L to M and I to M. Placed per region they have no lock to open; all at once the context is 94 locations. |
| 14 | Danger and Difficulty are both "the die". | `Region_Schema.md` Brief Tables "d6 Danger"; Roadsend's Procedures called it "the Danger die of a DANGEROUS region". | Read as the region's die, K, L and M (d4) cannot reach bands 6 and 5. |

## Tooling

| # | Friction | Where | Effect |
|---|---|---|---|
| 15 | The site and PDF builders crash on an empty `setting/`. | `tools/site_common.py` `parse_setting` reads `Setting.md` unguarded; `README.md` says they build empty. | `validate.yml` fails every pull request on a wiped setting. `setting/.gitkeep` keeps the directory; the crash stays. |
| 16 | Carried from Roadsend, now larger. | `Hoards.Total` is hand-summed and unchecked; Lethality needs a hazard that uses it. | Seven hoards; the brief asks for Lethal poison. |

## Baseline

Roadsend: 14 locations, 173 words mean per write-up, 12,329 words in `setting/`. This
brief: 94 locations, about 16,000 words of write-ups at the same mean, 13 regions against 3
and 11 factions against 2, so the tables, seeds, briefs and registries grow with them.
