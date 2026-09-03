# Steps

A record of the steps taken to build this setting. Each step names what it creates, the
context it reads, and the template it follows. Pattern guidance lives in `patterns/`, in
five folders - `setting/`, `region/`, `safe/`, `wild/`, `dangerous/` - and a step reads only
the folder that matches what it is building.

1. Establish framework
   - 1a. Customize `GENRE.md` with top level thematic hints (1981 B/X D&D, Conan-esque, Low Magic, Points of Light, Mythic Underworld).
   - 1b. Seed `setting/Procedures.md` with working default mechanics - tests and consequences, trap impact tiers, searching, time by rating, the three Action Dice scales, and the Difficulty roll - following `templates/Procedures.md` and `patterns/setting/Procedures.md`. Generic by design; tailored at 2i.
   - 1c. Seed `setting/Language.md` with three tongues - a common tongue, an older tongue for ruins and the dead, and one non-human tongue - each with phoneme inventories, a syllable shape, affixes, and a starter root list, following `templates/Language.md` and `patterns/setting/Language.md`. Seeding here rather than later is what makes names generative from 2b onward rather than systematized after the fact.
2. Build the setting
   - 2a. Create `setting/Outline.md` (region count, rating mix, a die per region, party altitude), using `GENRE.md` as context, following `templates/Outline.md` and `patterns/setting/Outline.md`. First because everything downstream scales against it.
   - 2b. Create `setting/Setting.md` (name, three tags, referee outline), following `templates/Setting.md` and `patterns/setting/Setting.md`.
   - 2c. Create `setting/History.md` (major events, oldest to newest, each leaving something findable), following `templates/History.md` and `patterns/setting/History.md`.
   - 2d. Create `setting/Truths.md` (rules, classes, or ideas unique to this setting), following `templates/Truths.md` and `patterns/setting/Truths.md`.
   - 2e. Create `setting/Rumours.md` (a d20 table of leads, marked T/P/F), following `templates/Rumours.md` and `patterns/setting/Rumours.md`.
   - 2f. Create `setting/Bestiary.md` (reusable creature templates, each with Description, Range, Sign and Disposition), following `templates/Bestiary.md` and `patterns/setting/Bestiary.md`. The AD spread is anchored to party altitude from 2a - **not** to the region dice, which are a separate axis.
   - 2g. Create `setting/Factions.md` (3 factions, each with a visual identity), following `templates/Factions.md` and `patterns/setting/Factions.md`.
   - 2h. Create `setting/Treasure1.md` through `setting/Treasure5.md` (Treasure Tables I-V), following `templates/Treasure.md` and `patterns/setting/Treasure.md`.
   - 2i. Tailor `setting/Procedures.md` and `setting/Language.md` to this setting, and create `setting/Lore.md`, `setting/Keys.md`, `setting/Quests.md`, `setting/NamedCreatures.md`, and `setting/UniqueTreasures.md` as empty stub tables. These five fill in two phases: a stub row (name and location) during 4c, and the full entry at 4d.
3. Build the region
   - 3a. Create `setting/region/Regions.md` (a Regional Gazetteer), taking the region count, ratings and dice from `setting/Outline.md`, following `templates/Region_Gazetteer.md`.
   - 3b. Create `setting/region/Connections.mmd` (a mermaid graph of region-to-region connections, existence only), following `templates/Connections.mmd`.
   - 3c. Create one `setting/region/[Code].md` Region Overview per region, including its d6 table, using `GENRE.md`, the setting-level artifacts, and `setting/region/Regions.md` as context, following `templates/Region.md` and the matching `patterns/region/Safe.md`, `Wild.md`, or `Dangerous.md`. Fields differ materially by rating - a SAFE overview carries the People roster and the current Situation, a WILD overview the Terrain and Foraging texture narrated between points, a DANGEROUS overview the Architecture and the Danger countdown.
4. Build locations
   - 4a. Create one folder per region, each with a `Locations.md` gazetteer, using each region's overview as context and taking counts and class mix from its `patterns/region/` file, following `templates/Location_Gazetteer.md`. Stubs carry only a name, weight or classification, and tags. **Every location in the setting exists as a stub after this step**, which is what lets a Quest or Key name a real target at 4c.
   - 4b. Create each region's `Connections.mmd`, following `templates/Region_Connections.mmd` and the topology in its `patterns/region/` file - a shallow hub for SAFE, a forest of trees for WILD, a dense graph for DANGEROUS. For DANGEROUS, assign each location its node role (empty, dead end, branch, loop leg, divide) here; 4c reads it rather than inventing it.
   - 4c. Create one `[Location Code].md` file per location, using `GENRE.md`, the parent Region Overview, the location's own stub, `setting/Procedures.md`, `setting/Language.md`, and **the three files of its rating folder in order** - the class file for the inclusion spec, the element files its spec lines draw from, then `Dressing.md`, `Secrets.md` and `Naming.md` - following `templates/Location.md`. Record every coined proper noun back into `setting/Language.md`. Whenever a Feature calls for Lore, a Key, a Quest, a Named Creature, or a Unique Treasure, add a stub row to the matching `setting/` file. Within a DANGEROUS region generate one weight tier at a time, high to low by default so medium and low can foreshadow what is already decided. Within a WILD region the order is not optional: Landmark, then Hidden, then Secret, since each child's connection is written into its parent.
   - 4d. Once every region has completed 4a-4c, write the full entry for each stub row in `setting/Lore.md`, `Keys.md`, `Quests.md`, `NamedCreatures.md`, and `UniqueTreasures.md`, using every location file the stub points to as context, following the matching template and `patterns/setting/` file. Also grow `setting/Language.md` with any coinage not yet recorded.
5. Judgement checks
   - 5a. Create/update `checks/TemplateJudgementCheck.md`, using `GENRE.md`, `CLAUDE.md`, `STEPS.md`, `templates/`, and `patterns/` as context, following `templates/Template_Judgement_Check.md`.
   - 5b. Create/update `checks/PatternJudgementCheck.md`, using `GENRE.md` and every file in `patterns/` as context, following `templates/Pattern_Judgement_Check.md`. Note that the duplication check is **inverted** for `patterns/` - restatement across rating folders is deliberate, so two versions that read the same are a finding.
   - 5c. Once a region's locations are complete, create/update `checks/SettingJudgementCheck.md`, following `templates/Setting_Judgement_Check.md`. Unlike other steps this one reads broadly across levels, since cross-level coherence is what is being judged.
