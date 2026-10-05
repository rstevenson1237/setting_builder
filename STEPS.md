# Steps

A record of the steps taken to build this setting. Each step names what it creates and the
template (and pattern file) it follows - the template's own Context section owns the file
list to read, so a step restates it only where the step itself adds something the template
can't know: build order, phase gating, or stub/registry bookkeeping. Pattern guidance lives
in `patterns/`, in five folders - `setting/`, `region/`, `safe/`, `wild/`, `dangerous/` - and
a step reads only the folder that matches what it is building.

1. Establish framework
   - 1a. Retired. Tags are generated per location at 4a; the setting's tag line is 2a's and each region's is 3a's.
   - 1b. Seed `setting/Procedures.md`, following `templates/setting/Procedures.md`.
   - 1c. Seed `setting/Language.md`, following `templates/setting/Language.md`.
2. Build the setting
   - 2a. Create `setting/Setting.md`, following `templates/setting/Setting.md`.
   - 2b. Create `setting/History.md`, following `templates/setting/History.md`.
   - 2c. Create `setting/Truths.md`, following `templates/setting/Truths.md`.
   - 2d. Create `setting/Rumours.md`, following `templates/setting/Rumours.md`.
   - 2e. Create `setting/Bestiary.md`, following `templates/setting/Bestiary.md`.
   - 2f. Create `setting/Factions.md`, following `templates/setting/Factions.md`.
   - 2g. Create `setting/Treasure1.md` through `setting/Treasure5.md` (Treasure Tables I-V), following `templates/setting/Treasure.md`.
   - 2h. Tailor `setting/Procedures.md` and `setting/Language.md` to this setting, following `templates/setting/Procedures.md` and `templates/setting/Language.md`, and create `setting/Lore.md`, `setting/Keys.md`, `setting/Quests.md`, `setting/NamedCreatures.md`, and `setting/UniqueTreasures.md` as empty stub tables, following `templates/setting/Lore.md`, `templates/setting/Keys.md`, `templates/setting/Quests.md`, `templates/setting/NamedCreatures.md`, and `templates/setting/UniqueTreasures.md`.
3. Build the region
   - 3a. Create `setting/region/Regions.md` (the Regional Gazetteer), following `templates/region/Region_Gazetteer.md`.
   - 3b. Create `setting/region/Connections.mmd` (region-to-region connections), following `templates/region/Connections.mmd`.
   - 3c. For each region, create its folder `setting/region/[Code]/` and its Region Overview `setting/region/[Code].md`, following `templates/region/Region.md`.
4. Build locations
   - 4a. Create each region's `Locations.md` with its § Location table, Weight left empty, following `templates/safe/Locations.md`, `templates/wild/Locations.md` or `templates/dangerous/Locations.md` by the region's rating. **Every location in the setting exists as a row after this step.**
   - 4b. Fill § Location's Weight column, following `templates/safe/Locations.md`, `templates/wild/Locations.md` or `templates/dangerous/Locations.md`.
   - 4c. Create each region's `setting/region/[Code]/Connections.mmd`, following `templates/region/Region_Connections.mmd`, and for a DANGEROUS region one `[Block Name].mmd` per block, following `templates/region/Block_Connections.mmd`.
   - 4d. Allocate each region, following `templates/region/Allocation.md`: every table file created and every row created as a stub, plus the registry stub any row names. **Every row in the region exists as a stub after this step.** `python3 tools/validate_setting.py --pending` lists what each later step owes.
   - 4e. Optional and repeatable: write a coordinated build across a region's rooms in one pass, following `templates/region/Composition.md`. Run here it claims stubs before the table passes; run after 4i it is a retrofit.
   - 4f. Fill each region's tables, one fresh context per file, in this order: `Challenges.md`, `Treasures.md`, then `Locations.md`'s class, kind and Dressing tables - following `templates/dangerous/Challenges.md` or `templates/wild/Challenges.md`, `templates/dangerous/Treasures.md` or `templates/wild/Treasures.md`, and `templates/safe/Locations.md`, `templates/wild/Locations.md` or `templates/dangerous/Locations.md`.
   - 4g. Name each region's locations - `Locations.md` § Naming, then every mention of a changed name brought into line (diagram labels, registry Found at cells) - following `templates/safe/Locations.md`, `templates/wild/Locations.md` or `templates/dangerous/Locations.md`.
   - 4h. Once every region has completed 4a-4g, fill every connected stub: each region's `Exits.md` and `Links.md`, following `templates/safe/Exits.md`, `templates/wild/Exits.md` or `templates/dangerous/Exits.md` and `templates/safe/Links.md`, `templates/wild/Links.md` or `templates/dangerous/Links.md`; then every registry's full entry in `setting/Lore.md`, `Keys.md`, `Quests.md`, `NamedCreatures.md` and `UniqueTreasures.md`, following `templates/setting/Lore.md`, `templates/setting/Keys.md`, `templates/setting/Quests.md`, `templates/setting/NamedCreatures.md` and `templates/setting/UniqueTreasures.md`.
   - 4i. Write one `[Location Code].md` per location, following `templates/region/Location.md`.
   - 4j. Grow `setting/Language.md`, following `templates/setting/Language.md`, and revisit `setting/Procedures.md`, following `templates/setting/Procedures.md`.
5. Judgement checks
   - 5a. Create/update `setting/checks/TemplateJudgementCheck.md`, following `templates/checks/Template_Judgement_Check.md`.
   - 5b. Create/update `setting/checks/PatternJudgementCheck.md`, following `templates/checks/Pattern_Judgement_Check.md`. Where a build exists, run it after 5c's check, from the findings 5c traced to a pattern.
   - 5c. Once a region's locations are complete, create/update `setting/checks/SettingJudgementCheck.md`, following `templates/checks/Setting_Judgement_Check.md`.
