# Steps

The build, in order. Each step names what it creates and the template it follows; the
template's Context names what to read.

Every step closes by running `python3 tools/validate_setting.py`; a warning names the step
that owes it, and `--pending` lists what each still owes.

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
   - 2g. Tailor `setting/Procedures.md` and `setting/Language.md`, following `templates/setting/Procedures.md` and `templates/setting/Language.md`, and create the registries empty - each its title line only - following `templates/setting/Lore.md`, `templates/setting/Keys.md`, `templates/setting/NamedCreatures.md`, `templates/setting/UniqueTreasures.md`, `templates/setting/MagicalTomes.md`, `templates/setting/Hoards.md` and `templates/setting/LocalProcedures.md`.
3. Build the regions
   - 3a. Create `setting/region/Regions.md`, following `templates/region/Region_Gazetteer.md`.
   - 3b. Place the regions on the sheets `BRIEF.md` asks for: run `python3 tools/maps.py place`, which writes `setting/Sheets.md` and each sheet's map file, and send each request it reports unmet to `BRIEF.md`; then run `python3 tools/maps.py ground`, which writes each placed region's `Ground.md`.
   - 3c. For each region, create its folder and its seed, `setting/region/[Code]/Seed.md`, following `templates/region/Region.md`.
4. Lay out the locations - structure, no content
   - 4a. Create each region's `Locations.md`, following `templates/region/Tables.md`.
   - 4b. Create each region's `Connections.md`, and its `Blocks.md` where its rating's schema asks for one, following `templates/region/Tables.md`.
   - 4c. Create each region's other table files, every entry a stub, following `templates/region/Tables.md`.
   - 4d. Add the ground at each location: run `python3 tools/maps.py ground` again, which adds an `At` entry to each placed region's `Ground.md` for every location with a bearing and distance from the way in.
5. Layer the content, one region at a time (a block at a time in a collection) - 5a to 5d repeat until a pass changes nothing; then 5e
   - 5a. Seed: fill every stub, Purpose first, following `templates/region/Tables.md`, and write every setting entry a table names, or bring its Found at or Appears at in line with the tables, following `templates/setting/Bestiary.md`, `templates/setting/Factions.md`, `templates/setting/NamedCreatures.md`, `templates/setting/Lore.md`, `templates/setting/Keys.md`, `templates/setting/UniqueTreasures.md`, `templates/setting/MagicalTomes.md`, `templates/setting/Hoards.md` and `templates/setting/LocalProcedures.md`, recording a tongue or family name's coinage in `setting/Language.md` before it is used, following `templates/setting/Language.md`; write a `Lock` where the design wants a gate; then resolve what the validator now owes 5a - a stub Reward pulling `Keys: [name]` for each lock without its key, and a stub for each entry whose Found at or Appears at names a location no table holds it.
   - 5b. Write: every location whose write-up is missing or stale, rewriting only the lines its changed entries touch, following `templates/region/Location.md`.
   - 5c. Check: run `python3 tools/validate_setting.py` and `python3 tools/metrics.py`, and send each reading outside its range to the step that owes it - a stub or an unmet target to 5a, a stale write-up or a tell to 5b, an open thread to 5d. A pass that leaves none ends the loop.
   - 5d. Thread: write `setting/Rumours.md` and `setting/Quests.md`, following `templates/setting/Rumours.md` and `templates/setting/Quests.md`, leaving a row's Settled at or Points to empty until the region holding its answer has a pass; set each Person's `quest` to the quest they give; bring each `setting/Lore.md` entry in line with the Rumours, Quests, History and Truths now written, following `templates/setting/Lore.md`; and fill each Truth's Handle and Codes, following `templates/setting/Truths.md`.
   - 5e. Brief: write each region's brief, `setting/region/[Code].md`, that is missing or stale, following `templates/region/Brief.md`.
6. Judge the build
   - 6a. Create or update `setting/checks/TemplateJudgementCheck.md`, following `templates/checks/Template_Judgement_Check.md`.
   - 6b. Create or update `setting/checks/SchemaJudgementCheck.md`, following `templates/checks/Schema_Judgement_Check.md`, after 6c, starting from 6c's findings traced to a schema.
   - 6c. Create or update `setting/checks/SettingJudgementCheck.md`, following `templates/checks/Setting_Judgement_Check.md`.
