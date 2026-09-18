# Setting Builder

A plain-text framework for authoring OSR (Old-School Renaissance) adventure settings as
markdown and a few `.mmd` mermaid diagrams. All "development" here is content generation
following the templates and workflow below.

This file is a map: where things live and what each part does. It is not a reference for
how any of them work. To understand a system, read the system - the authorities below are
current by construction, and any summary of them here would not be.

## Authorities

Read these rather than a description of them.

- `GENRE.md` - this build's thematic spine (era, tone, magic level, structure), customized
  at STEPS.md step 1a, plus the fixed **What a line has to earn** section: the three tests
  every line at every level must pass. The tests outrank every template.
- `STYLE.md` - the positive prose target, re-read beside `GENRE.md` at every generation
  step: what the sources contribute, the one register and how a spoken Player Summary differs
  from it, which referee asides are allowed, the sentence budget, and the tells.
- `STEPS.md` - the authoritative, sequential build log. Every artifact created follows a
  numbered step here (e.g. `4c`) naming its template and pattern file. Step ids grow by
  suffix and are never renumbered.
- `patterns/SPEC.md` - the full field spec for pattern files.
- `setting/Procedures.md` - the authority on dice, scaling, time and resolution.
- `CLAUDE.md` - always loaded as system context; the rules needing active re-checking on
  every request.

## Directories

- `templates/` - one template per artifact type, each structured **Purpose / Context /
  Instructions / Template**. A template's own Context section lists exactly which files to
  read before drafting; don't pull in more than it names.
- `patterns/` - pattern guidance, in five folders matching the five levels of generation:
  `setting/`, `region/`, `safe/`, `wild/`, `dangerous/`. A generation step reads only the
  folder matching what it is building. Every file shares one skeleton, specified in
  `patterns/SPEC.md`.
- `setting/` - the generated setting, mirroring the template set in the order STEPS.md lays
  out: setting-level artifacts, Treasure Tables I-V, the two living artifacts
  (`Procedures.md`, `Language.md`), the five registries (`Lore.md`, `Keys.md`, `Quests.md`,
  `NamedCreatures.md`, `UniqueTreasures.md`), and `region/`, holding the Regional Gazetteer
  and one folder per region.
- `setting/region/[Code]/` - one region: its own `Tags.md` pool, its `Locations.md`
  gazetteer, its connection diagrams, and one `[LocationCode].md` per location. The Region
  Overview sits beside it at `setting/region/[Code].md`.
- `checks/` - output of the judgement checks (STEPS.md step 5): non-mechanical review
  passes `tools/validate_setting.py` can't do, following the checklist format in the
  matching `templates/*_Judgement_Check.md`.
- `tools/` - exactly what content generation needs and nothing else. Stdlib-only Python, no
  package manager, no test framework beyond running these against the content.
  - `validate_setting.py` - structural linter, run in CI on every pull request.
  - `build_site.py` / `build_pdf.py` - render `setting/` into a website and a PDF, with no
    separate copy to keep in sync.
  - `site_common.py` - parsing helpers shared by the two builders.
  - `metrics.py` - what the framework costs and how the corpus reads, counted. Judges
    nothing; the thresholds are the validator's.

## Commands

```sh
python3 tools/validate_setting.py           # structural lint
python3 tools/validate_setting.py --pending [REGION]    # edges owed to unwritten blocks
python3 tools/validate_setting.py --read-set [STEP]     # what a step reads, per the graph
python3 tools/metrics.py                    # corpus, tells, budget and read-set report
python3 tools/metrics.py --tells [PATH]     # every tell hit, listed, over any markdown
python3 tools/build_site.py --out _site     # static site, including patterns.html
python3 -m http.server -d _site             # preview it locally
pip install -r tools/requirements-pdf.txt   # WeasyPrint, for the PDF only
python3 tools/build_pdf.py                  # single print-formatted PDF
```

`build_site.py` also renders `patterns.html`, a Pattern Reference page built from
`patterns/` rather than `setting/`, so it builds against an empty setting.

## CI and deployment

- `.github/workflows/validate.yml` - runs the validator on every pull request and every
  push to `main`.
- `.github/workflows/pages.yml` - builds the site and the PDF and deploys both to GitHub
  Pages on every push to `main` touching `setting/` or the generators, or on manual
  dispatch. This needs a one-time repository setting: **Settings -> Pages -> Source:
  GitHub Actions**.
