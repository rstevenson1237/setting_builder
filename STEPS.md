# Steps

The build, in order. Each step names what it creates and the template it follows; the
template's Context names what to read, and `python3 tools/validate_setting.py --read-set
STEP` lists it; `--skeleton STEP [REGION]` prints the shape its schema or its format gives
what the step writes.

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
   - 2g. Tailor `setting/Procedures.md` and `setting/Language.md`, following `templates/setting/Procedures.md` and `templates/setting/Language.md`.
3. Build the regions
   - 3a. Create `setting/region/Regions.md`, following `templates/region/Region_Gazetteer.md`.
   - 3b. Place the regions on the sheets `BRIEF.md` asks for: run `python3 tools/maps.py place`, which writes `setting/Sheets.md` and each sheet's map file, and send each request it reports unmet to `BRIEF.md`; then run `python3 tools/maps.py ground`, which writes each placed region's `Ground.md`.
   - 3c. For each region, create its folder and its seed, `setting/region/[Code]/Seed.md`, following `templates/region/Region.md`.
   - 3d. Create each region's `Locations.md`, following `templates/region/Locations.md`.
   - 3e. Create each region's `Connections.md`, and its `Blocks.md` where its rating's schema asks for one, following `templates/region/Connections.md`.
   - 3f. Add the ground at each location: run `python3 tools/maps.py ground` again, which adds an `At` entry to each placed region's `Ground.md` for every location with a bearing and distance from the way in.
4. Layer the content, one region at a time (a block at a time in a collection) - 4a to 4d repeat until a pass changes nothing; then 4e
   - 4a. Seed: create each table file and fill every entry, Purpose first, following `templates/region/Tables.md`, and write every setting entry a table names, creating its registry file where it is missing, or bring its Found at or Appears at in line with the tables, following `templates/setting/Bestiary.md`, `templates/setting/Factions.md`, `templates/setting/NamedCreatures.md`, `templates/setting/Lore.md`, `templates/setting/Keys.md`, `templates/setting/UniqueTreasures.md`, `templates/setting/MagicalTomes.md`, `templates/setting/Hoards.md` and `templates/setting/LocalProcedures.md`, recording a tongue or family name's coinage in `setting/Language.md` before it is used, following `templates/setting/Language.md`; write a `Lock` where the design wants a gate; then resolve what the validator now owes 4a - a stub Reward pulling `Keys: [name]` for each lock without its key, and a stub for each entry whose Found at or Appears at names a location no table holds it. Then, for a DANGEROUS region with Blocks, run `python3 tools/maps.py pack [Code]`, which packs each block's rooms into a square, routes a passage for every way, and writes their `east` and `north`, the block's `footprint`, and the wall each way leaves by and its length, here and in each Exits line, then `python3 tools/maps.py draw`; a write-up's prose that names a direction follows.
   - 4b. Write: every location whose write-up is missing or stale, rewriting only the lines its changed entries touch, following `templates/region/Location.md`.
   - 4c. Check: run `python3 tools/validate_setting.py` and `python3 tools/metrics.py`, and send each reading outside its range to the step that owes it - a stub or an unmet target to 4a, a stale write-up or a tell to 4b, an open thread to 4d. A pass that leaves none ends the loop.
   - 4d. Thread: write `setting/Rumours.md` and `setting/Quests.md`, following `templates/setting/Rumours.md` and `templates/setting/Quests.md`, leaving a row's Settled at or Points to empty until the region holding its answer has a pass; set each Person's `quest` to the quest they give; bring each `setting/Lore.md` entry in line with the Rumours, Quests, History and Truths now written, following `templates/setting/Lore.md`; and fill each Truth's Handle and Codes, following `templates/setting/Truths.md`.
   - 4e. Brief: write each region's brief, `setting/region/[Code].md`, that is missing or stale, following `templates/region/Brief.md`.
5. Judge the build
   - 5a. Create or update `setting/checks/TemplateJudgementCheck.md`, following `templates/checks/Template_Judgement_Check.md`.
   - 5b. Create or update `setting/checks/SchemaJudgementCheck.md`, following `templates/checks/Schema_Judgement_Check.md`, after 5c, starting from 5c's findings traced to a schema.
   - 5c. Create or update `setting/checks/SettingJudgementCheck.md`, following `templates/checks/Setting_Judgement_Check.md`.
