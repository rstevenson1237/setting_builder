# Steps

A record of the steps taken to build this setting.

1. Establish framework
   - 1a. Customize `GENRE.md` with top level thematic hints (1981 B/X D&D, Conan-esque, Low Magic, Points of Light, Mythic Underworld).
2. Build the setting
   - 2a. Create `setting/Setting.md` (setting name, thematic tags, and referee outline), following the format in `templates/Setting.md`.
   - 2b. Create `setting/History.md` (major events, oldest to newest), using `GENRE.md` and `setting/Setting.md` as context, following the format in `templates/History.md`.
   - 2c. Create `setting/Truths.md` (unique truths, object classes, or thematic ideas not already established), using `GENRE.md`, `setting/Setting.md`, and `setting/History.md` as context, following the format in `templates/Truths.md`.
   - 2d. Create `setting/Rumours.md` (a table of 20 rumours of varying truth, serving as adventure hooks), using `GENRE.md`, `setting/Setting.md`, `setting/History.md`, and `setting/Truths.md` as context, following the format in `templates/Rumours.md`.
   - 2e. Create `setting/Bestiary.md` (20 reusable creature templates in a system neutral rule set, HD=AD), using `GENRE.md`, `setting/Setting.md`, `setting/History.md`, and `setting/Truths.md` as context, following the format in `templates/Bestiary.md`.
   - 2f. Create `setting/Factions.md` (3 factions with AD, Resources, Knowledge, Tactics, Reactions, and Goals), using `GENRE.md`, `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`, `setting/Rumours.md`, and `setting/Bestiary.md` as context, following the format in `templates/Factions.md`.
   - 2g. Create `setting/Treasure1.md` through `setting/Treasure5.md` (Treasure Tables I-V: Scavenged Loot, Equipment and Armaments, Gems and Jewelry, Luxury and Trade Goods, and Treasure Cache - each a d20 table of item, value in cn, and weight in wt), using `GENRE.md`, `setting/Setting.md`, `setting/History.md`, and `setting/Truths.md` as context, following the format in `templates/Treasure.md`.
3. Build the region
   - 3a. Create `setting/region/Regions.md` (a Regional Gazetteer), starting with a SAFE d6 settlement, a WILD d10 pocket near it, and a DANGEROUS d8 dungeon within the WILD region, following the format in `templates/Region_Gazetteer.md`.
   - 3b. Create `setting/Connections.mmd` (a mermaid graph of high level region connections, existence only, no type or quantity), using `setting/region/Regions.md` as context, following the format in `templates/Connections.mmd`.
   - 3c. Create `setting/region/A.md`, `setting/region/B.md`, `setting/region/C.md` (a Region Overview per region, including its Tables now rather than deferred), using `GENRE.md`, `setting/Setting.md`, `setting/History.md`, `setting/Truths.md`, `setting/Rumours.md`, `setting/Bestiary.md`, `setting/Factions.md`, and `setting/region/Regions.md` as context, following the format in `templates/Region.md`.
4. Build locations
   - 4a. Create one folder per region (`setting/region/A/`, `setting/region/B/`, `setting/region/C/`), each with a `Locations.md` location gazetteer - major landmarks for SAFE/WILD regions (about as many as the region's die type), one location per room for DANGEROUS regions (about 3x the die type, each weighted low/medium/high) - using each region's `setting/region/[Code].md` overview as context, following the format in `templates/Location_Gazetteer.md`. Stubs carry only a name, weight, and tags - a map skeleton, not content.
   - 4b. Create `setting/region/A/Connections.mmd`, `B/Connections.mmd`, `C/Connections.mmd` (a mermaid graph of that region's location connections, plus links to neighboring regions), using each region's `Locations.md` as context - unlike `setting/Connections.mmd`, these may be directional and use different connection types (normal, hidden, one-way), following the format in `templates/Region_Connections.mmd`.
   - 4c. Create one `[Location Code].md` file per location (e.g. `setting/region/A/1.md`), using only `GENRE.md`, the parent Region Overview, and the location's own gazetteer stub as context - the Pattern is chosen now, at generation time, from the matching `patterns/` file - other setting files are consulted only to look up a name already referenced, never included wholesale - following the format in `templates/Location.md`.
