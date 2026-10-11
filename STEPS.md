# Steps

The build, in order. Each step names what it creates and the template it follows; the
template's Context names what to read.

1. Establish the framework
   - 1a. Seed `setting/Procedures.md`, following `templates/setting/Procedures.md`.
   - 1b. Seed `setting/Language.md`, following `templates/setting/Language.md`.
2. Build the setting
   - 2a. Create `setting/Setting.md`, following `templates/setting/Setting.md`.
   - 2b. Create `setting/History.md`, following `templates/setting/History.md`.
   - 2c. Create `setting/Truths.md`, following `templates/setting/Truths.md`.
   - 2d. Create `setting/Bestiary.md`, following `templates/setting/Bestiary.md`.
   - 2e. Create `setting/Factions.md`, following `templates/setting/Factions.md`.
   - 2f. Create `setting/Treasure1.md` through `setting/Treasure5.md`, following `templates/setting/Treasure.md`, and `setting/Magic.md`, following `templates/setting/Magic.md`.
   - 2g. Tailor `setting/Procedures.md` and `setting/Language.md`, following `templates/setting/Procedures.md` and `templates/setting/Language.md`, and create the registries empty, following `templates/setting/Lore.md`, `templates/setting/Keys.md`, `templates/setting/NamedCreatures.md`, `templates/setting/UniqueTreasures.md`, `templates/setting/MagicalTomes.md` and `templates/setting/Hoards.md`.
3. Build the regions
   - 3a. Create `setting/region/Regions.md`, following `templates/region/Region_Gazetteer.md`.
   - 3b. Create `setting/region/Connections.mmd`, following `templates/region/Connections.mmd`.
   - 3c. For each region, create its folder and its seed, `setting/region/[Code].md`, following `templates/region/Region.md`.
4. Lay out the locations - structure, no content
   - 4a. Create each region's `Locations.md`, following `templates/dangerous/Tables.md`.
   - 4b. Create each region's `Connections.mmd`, following `templates/dangerous/Connections.mmd`.
   - 4c. Create each region's other table files, every entry a stub, following `templates/dangerous/Tables.md`.
5. Layer the content - 5a to 5d repeat until a pass changes nothing; then 5e
   - 5a. Seed: fill every stub, Purpose first, following `templates/dangerous/Tables.md`, and write every setting entry a table names, following `templates/setting/Bestiary.md`, `templates/setting/Factions.md`, `templates/setting/NamedCreatures.md`, `templates/setting/Lore.md`, `templates/setting/Keys.md`, `templates/setting/UniqueTreasures.md`, `templates/setting/MagicalTomes.md` and `templates/setting/Hoards.md`.
   - 5b. Write: every location whose write-up is missing or stale, following `templates/region/Location.md`, recording coinages in `setting/Language.md`, following `templates/setting/Language.md`.
   - 5c. Review: run `python3 tools/validate_setting.py` and `python3 tools/metrics.py`, then review this pass's write-ups in a fresh context, following `templates/checks/Location_Review.md`.
   - 5d. Place: write `setting/Rumours.md` and `setting/Quests.md`, following `templates/setting/Rumours.md` and `templates/setting/Quests.md`; place locks, then keys for locks already placed, following `templates/dangerous/Tables.md` and `templates/setting/Keys.md`; and fill the Handles and Left lines the build now delivers, following `templates/setting/Truths.md` and `templates/setting/History.md`.
   - 5e. Brief: write each region's `Brief.md`, following `templates/region/Brief.md`.
6. Judge the build
   - 6a. Create or update `setting/checks/TemplateJudgementCheck.md`, following `templates/checks/Template_Judgement_Check.md`.
   - 6b. Create or update `setting/checks/PatternJudgementCheck.md`, following `templates/checks/Pattern_Judgement_Check.md`, after 6c, starting from 6c's findings traced to a pattern.
   - 6c. Create or update `setting/checks/SettingJudgementCheck.md`, following `templates/checks/Setting_Judgement_Check.md`.
