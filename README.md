# Setting Builder

A framework for creating OSR (Old-School Renaissance) themed adventure settings.

## Files

- `GENRE.md` — Top level thematic hints included in all content generation.
- `STEPS.md` — A record of the steps taken to build this setting.

## Setting Content

- `setting/Setting.md` — Name, thematic tags, and referee outline for the current setting.
- `setting/History.md` — Major events in the setting's history, oldest to newest.
- `setting/Truths.md` — Unique truths, object classes, and thematic ideas that set the setting apart.
- `setting/Rumours.md` — A table of 20 rumours of varying truth, serving as adventure hooks.
- `setting/Bestiary.md` — Reusable creature templates in a system neutral rule set (HD=AD).
- `setting/Factions.md` — The powers a party may treat with, oppose, or ignore, with Action Dice pools for Faction Turns.
- `setting/region/Regions.md` — Regional Gazetteer: an overview listing of all regions within the setting.
- `setting/Connections.mmd` — Mermaid graph of high level region connections (existence only, no type or quantity).
- `setting/region/A.md`, `B.md`, `C.md` — Region Overviews: Overview, Ambiance, Layout, Features, Dangers, Creatures, Secrets, Treasure, and Tables for each region.
- `setting/region/A/`, `B/`, `C/` — Per-region location gazetteers (`Locations.md`, with each stub pinning a Pattern), a `Connections.mmd` mermaid graph of that region's location connections (directional, typed), and one `[Location Code].md` full entry per location.

## Directory Structure

- `patterns/` — Thematic patterns to follow when creating content.
  - `Safe.md`, `Wild.md` — Patterns for SAFE and WILD region locations.
  - `Dangerous_Low.md`, `Dangerous_Medium.md`, `Dangerous_High.md` — Patterns for DANGEROUS region locations, by weight.
- `setting/` — A record of our created content.
- `templates/` — Formatting templates to follow when creating content.
- `tools/validate_setting.py` — A structural linter that checks `setting/` content against the templates, the region/location connection graphs, and the Lore/Keys/NamedCreatures/UniqueTreasures registries. Run it locally with `python3 tools/validate_setting.py`; it also runs automatically in CI on every pull request (`.github/workflows/validate.yml`).

## Validation

Every pull request runs `tools/validate_setting.py` in CI. It catches structural drift a human proofread easily misses: an `Exits:` entry pointing at a location code or name that doesn't match, a location missing from its region's `Connections.mmd`, a `(Lore: ...)`/`(Keys: ...)`/`(Named Creature: ...)`/`(Unique Treasure: ...)` citation with no matching stub row (or vice versa), a DANGEROUS-region location missing its weight tag, non-sequential location numbering, and similar. It does not check genre or tone against `GENRE.md` — that still takes a human or model read.
