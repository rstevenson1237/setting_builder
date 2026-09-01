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
  - `Template_Judgement_Check.md`, `Pattern_Judgement_Check.md`, `Setting_Judgement_Check.md` — checklists for the judgement checks below.
- `checks/` — Non-mechanical judgement checks (step 5), the human/model-judgment counterpart to `tools/validate_setting.py`: `TemplateJudgementCheck.md` (do templates pull the right patterns in the right order, and preserve known edge cases), `PatternJudgementCheck.md` (do patterns overlap/contradict, stay specific/discoverable/interactive, and cover everything needed), `SettingJudgementCheck.md` (do locations reinforce their region and regions reinforce the setting, with discrete/discoverable detail rather than vague motif).
- `tools/validate_setting.py` — A structural linter that checks `setting/` content against the templates, the region/location connection graphs, and the Lore/Keys/NamedCreatures/UniqueTreasures registries. Run it locally with `python3 tools/validate_setting.py`; it also runs automatically in CI on every pull request (`.github/workflows/validate.yml`).
- `tools/site_common.py`, `tools/build_site.py`, `tools/build_pdf.py`, `tools/site_assets/` — the web view / PDF generator, see below.

## Validation

Every pull request runs `tools/validate_setting.py` in CI. It catches structural drift a human proofread easily misses: an `Exits:` entry pointing at a location code or name that doesn't match, a location missing from its region's `Connections.mmd`, a `(Lore: ...)`/`(Keys: ...)`/`(Named Creature: ...)`/`(Unique Treasure: ...)` citation with no matching stub row (or vice versa), a DANGEROUS-region location missing its weight tag, non-sequential location numbering, and similar. It does not check genre or tone against `GENRE.md` — that still takes a human or model read.

## Web view and PDF

`setting/` also builds into a hyperlinked, mobile-friendly website and a single downloadable PDF, both generated straight from the same markdown - there's no separate copy to keep in sync.

- **Website**: `python3 tools/build_site.py --out _site` renders one static HTML page per document, region, and location, with a responsive nav (search box, mobile menu, a Regions dropdown), badges for region rating and location weight, and automatic cross-linking of every `A.1`-style location code, `(Lore: ...)`/`(Keys: ...)`/`(Named Creature: ...)`/`(Unique Treasure: ...)`/`(Treasure I-V, d20)` citation, and `Creature Name (Bestiary)` mention to the page it points to. Region and location `Connections.mmd` graphs render live as clickable Mermaid diagrams. Pure standard library - no npm, no build step beyond running the script. Preview locally with `python3 -m http.server -d _site`.
- **PDF**: `python3 tools/build_pdf.py` combines the same content into one print-formatted, internally hyperlinked PDF (automatic bookmarks/outline, a table of contents with page numbers, the same cross-reference links as the website) using [WeasyPrint](https://weasyprint.org/). Install it first with `pip install -r tools/requirements-pdf.txt`. Mermaid diagrams can't run inside a PDF, so each `Connections.mmd` is rendered there as a plain connection list instead.
- **Deployment**: `.github/workflows/pages.yml` builds both and deploys them to GitHub Pages on every push to `main` that touches `setting/` or the generator itself (or on manual dispatch). The PDF is published alongside the site and linked from its nav as "Download PDF". This requires a one-time repository setting: **Settings → Pages → Source: GitHub Actions**.
