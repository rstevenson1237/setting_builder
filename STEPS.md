# Steps

A record of the steps taken to build this setting. Each step names what it creates and the
template (and pattern file) it follows - the template's own Context section owns the file
list to read, so a step restates it only where the step itself adds something the template
can't know: build order, phase gating, or stub/registry bookkeeping. Pattern guidance lives
in `patterns/`: `setting/` and `region/` folders, and `patterns/Schema.md` for every location
table - and a step reads only what matches what it is building.

1. Establish framework
   - 1a. Retired. Tags are generated per location at 4a; the setting's tag line is 2a's and each region's is 3a's.
   - 1b. Seed `setting/Procedures.md` with working default mechanics - tests and consequences, forced damage and hazard tiers, wounds and madness, conditions, searching, time by rating, the three Action Dice scales, and the Difficulty roll - following `templates/setting/Procedures.md`. Generic by design; tailored at 2h.
   - 1c. Seed `setting/Language.md` with three tongues - a common tongue, an older tongue for ruins and the dead, and one non-human tongue - each with phoneme inventories, a syllable shape, affixes, and a starter root list, following `templates/setting/Language.md`. Seeding here rather than later is what makes names generative from 2b onward rather than systematized after the fact.
2. Build the setting
   - 2a. Create `setting/Setting.md` (name, a tag line, referee outline), following `templates/setting/Setting.md`.
   - 2b. Create `setting/History.md` (major events, oldest to newest, each leaving something findable), following `templates/setting/History.md` - empty unless `BRIEF.md` or the prompt asks for a history.
   - 2c. Create `setting/Truths.md` (rules, classes, or ideas unique to this setting), following `templates/setting/Truths.md` - empty unless `BRIEF.md` or the prompt asks for truths.
   - 2d. Create `setting/Rumours.md` (a d20 table of leads, marked T/P/F), following `templates/setting/Rumours.md`.
   - 2e. Create `setting/Bestiary.md` (reusable creature templates, each with Description, Range, Sign and Disposition), following `templates/setting/Bestiary.md` - barebones unless `BRIEF.md` or the prompt asks for a full one, and grown at 3c and 4e as a region or location needs an entry.
   - 2f. Create `setting/Factions.md` (3 factions, each with a visual identity), following `templates/setting/Factions.md`.
   - 2g. Create `setting/Treasure1.md` through `setting/Treasure5.md` (Treasure Tables I-V), following `templates/setting/Treasure.md`.
   - 2h. Tailor `setting/Procedures.md` and `setting/Language.md` to this setting, following `templates/setting/Procedures.md` and `templates/setting/Language.md`, and create `setting/Lore.md`, `setting/Keys.md`, `setting/Quests.md`, `setting/NamedCreatures.md`, and `setting/UniqueTreasures.md` as empty stub tables, following `templates/setting/Lore.md`, `templates/setting/Keys.md`, `templates/setting/Quests.md`, `templates/setting/NamedCreatures.md`, and `templates/setting/UniqueTreasures.md`. Each entry is written at 4e, once a table names it.
3. Build the region
   - 3a. Create `setting/region/Regions.md` (a Regional Gazetteer: region count, rating mix, a die per region), following `templates/region/Region_Gazetteer.md`. Fixed here rather than earlier, since nothing before this step needed it. Each entry carries its region's tag line.
   - 3b. Create `setting/region/Connections.mmd` (a mermaid graph of region-to-region connections, existence only), following `templates/region/Connections.mmd`.
   - 3c. For each region, create its folder (`setting/region/[Code]/`, moved up from 4a since this step now needs it), and its full `setting/region/[Code].md` Region Overview including its two d6 tables, following `templates/region/Region.md`.
4. Build locations - DANGEROUS regions; SAFE and WILD regions have no table templates yet
   - 4a. Create each region's `Locations.md` - every room's code, name, tags and type - following `templates/dangerous/Tables.md`. **Every location in the setting exists as an entry after this step.**
   - 4b. Create each region's `Connections.mmd`, following `templates/dangerous/Connections.mmd`.
   - 4c. Create each region's `Purpose.md`, following `templates/dangerous/Tables.md`, before any table below - each is written toward it.
   - 4d. Create each region's `Dressing.md`, `Challenges.md`, `Rewards.md` and `Connections.md`, one fresh context per file, following `templates/dangerous/Tables.md`. `python3 tools/validate_setting.py --pending [REGION]` lists what each still owes.
   - 4e. Write every setting entry a table names and its setting file lacks, following `templates/setting/Bestiary.md`, `templates/setting/Factions.md`, `templates/setting/NamedCreatures.md`, `templates/setting/Lore.md`, `templates/setting/Keys.md` and `templates/setting/UniqueTreasures.md`.
   - 4f. Write one `[Location Code].md` per location, following `templates/region/Location.md`. Record every coined proper noun back into `setting/Language.md`.
   - 4g. Grow `setting/Language.md` with any coinage not yet recorded, following `templates/setting/Language.md`, and revisit `setting/Procedures.md`, following `templates/setting/Procedures.md`, only if generation turned out to need a mechanic its seed did not cover.
5. Judgement checks
   - 5a. Create/update `setting/checks/TemplateJudgementCheck.md`, following `templates/checks/Template_Judgement_Check.md`.
   - 5b. Create/update `setting/checks/PatternJudgementCheck.md`, following `templates/checks/Pattern_Judgement_Check.md`. Where a build exists, run it after 5c's check, from the findings 5c traced to a pattern.
   - 5c. Once a region's locations are complete, create/update `setting/checks/SettingJudgementCheck.md`, following `templates/checks/Setting_Judgement_Check.md`. Unlike other steps this one reads broadly across levels, since cross-level coherence is what is being judged. This is also where the setting's claims against itself get settled - the only check that reads *upward*: `Truths.md`'s Handles, `History.md`'s Left lines and `Rumours.md`'s Settled-at column get filled with real Location Codes wherever one exists; each Region Overview's claims against its own rooms (a treasure table it says it leans on, a creature it places somewhere, a motif it says repeats) get checked against what the locations actually deliver; `Language.md` gets any coinage not yet recorded. A claim with nothing under it yet is **not** deleted - name it under Room to Grow instead, since a claim already earns its keep at the level that stated it and just hasn't been reached below yet.
