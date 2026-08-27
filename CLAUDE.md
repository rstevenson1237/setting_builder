# CLAUDE.md

The non-negotiables. `SPEC.md` is the full specification; this page is what must
be true in every session.

## The four rules

- **Deterministic work runs in code.** Scaffolding, dice, validation, diagram
  derivation and dependency resolution never run as prose instructions.
- **Judgement runs in patterns.** Anything needing taste, theme or fiction runs
  through a pattern file.
- **Every generated file is reproducible** from its pattern, its dependencies
  and its recorded seed.
- **Every file carries current state only.** A superseded decision is rewritten,
  never annotated. Git holds the history.

## Three disciplines

- **Never invent an answer to an open item.** Stop and ask. An invented answer
  becomes canon silently and no check will catch it.
- **Rewrite, never annotate.** No file carries its own revision history in prose.
- **Every file has a stated purpose and holds nothing else.** `CLAUDE.md` and
  `MECHANICS.md` are one page each. `GENRE.md` is capped at 2,000 words.
  `STATE.md` is generated. `EXTERNAL.md` is the only backlog.

## Neutrality

Prose never states a mechanical value. A feature reads as fiction and carries
its mechanic beside it as a bracketed token from `MECHANICS.md`. Tokens are
referee-facing and never appear in player-facing text.

## Overwrite discipline

The Architect overwrites freely until a Builder pass has touched a file. After
that `state/ledger.json` lists the target in `built`, and `scaffold.py` refuses
it. Regeneration is then a booked step re-run, never a hand-patch toward the new
shape: a patched file cannot survive its own regeneration.

`scaffold.py --force` replaces a stub and is ordinary Architect work.
`--rerun` is what replaces a file marked built, and only a booked step re-run
passes it.

## Tools

| Command | Does |
| :--- | :--- |
| `python tools/scaffold.py setting\|tables\|region\|location ...` | Write stubs, frontmatter and empty headings. |
| `python tools/validate.py [--scope X] [--final] [--only M6,M17] [--list]` | Run the mechanical checks. |
| `python tools/roll.py dice 2d6 --target R03-L07` | Seeded dice. All randomness passes through here. |
| `python tools/roll.py table T-RUM --target R03 [--count n]` | Seeded table draws. |
| `python tools/ledger.py start\|done\|complete\|built\|decorated ...` | Move the progress record and regenerate `STATE.md`. |
| `python tools/router.py [--check]` | Regenerate `DESIGN_PATTERNS.md` from pattern frontmatter. |
| `python tools/resolve_deps.py --pattern <id> --target <code> [--var N=V]` | Resolve one bundle into `build/bundles/`. |
| `python -m unittest discover -s tests` | Run the tests. |

`tools/common.py` is the shared library: repository layout, the table catalogue
of SPEC.md section 4.7, frontmatter and markdown parsing. It is not a CLI.

## Patterns and bundles

A pattern carries `id`, `target`, `phase`, `writes`, `dependencies` and
`schema_version`, and a body of `## Patterns`, `## Excluded patterns` and
`## Design questions`. `router.py` refuses to index one that does not, and
`DESIGN_PATTERNS.md` is generated from that frontmatter and never hand-edited.
Files under `patterns/cells/` and `patterns/templates/`, and `GENRE.md` itself,
are not routed patterns.

`GENRE.md` and `MECHANICS.md` are injected into every bundle and no pattern
declares them. The cell file and the config arrive as ordinary selectors, so a
pattern that needs them says so and a pattern that does not carries neither.

Two rules are mechanical rather than trusted to a writer. `resolve_deps.py`
refuses a `table:S-...` selector on a pattern whose target is a location,
because S content reaches a player through a T table and never directly. It
also fails above `genre.max_words`, because `GENRE.md` enters every bundle and
its size is a tax on every call.

**`GENRE.md` is frozen at the close of Milestone 2.** Editing it afterwards is a
step re-run of everything downstream.

## Tests

Every mechanical check carries a case in `tests/test_validate.py` that breaks one
thing and proves the check reports it. **A new or changed check arrives with its
case**, and `test_every_check_has_a_case` fails if one is missing. A check with no
case is indistinguishable from a check that no longer runs.

`tests/test_tools.py` holds the round trip: a tree scaffolded from nothing must
pass the checks with no errors. That test is what makes "`scaffold.py` fixes the
shape and `validate.py` checks it, so the two agree by construction" a fact
rather than an intention. Run the suite before closing any milestone.

`.github/workflows/checks.yml` runs `router.py --check`, `resolve_deps.py
--check`, `validate.py` and the suite on every push and pull request. It runs
the commands in the table above and adds no checks of its own, so CI and this
page cannot drift.

## Body shape

`scaffold.py` fixes the shape and `validate.py` checks it, so the two agree by
construction. Do not invent a different one.

- **Features** are `### Name` subsections. A connection pointer `-> R03-L07`
  appears inside a feature and nowhere else (M23).
- **Exits** is a table of `To | Type | Cue`. The region's `connections.md` is
  the source of truth for the edges; the Exits table is the per-location view of
  the same edges, and M7 and M8 hold the two together.
- **Referee Overview** opens with the fields the region type requires, written
  as `**Label:** value`. `None` is a legal value only with a reason after it.
- **Diagrams** are never hand-authored. A host file carries
  `<!-- DIAGRAM: T4_R03_DROWNED_TIER.md -->` and nothing else.
- **Region referee tables** are `### Events`, `### Encounters` or `### Dangers`
  by region type, six rows, and Dangers count down from 6 to 1.

## Completeness gates

Some checks cannot be true before the step that writes their input has run. M6
needs step 9, M8, M9, M15 and M20 need step 10, M22's field values need step 11,
M18 needs step 3, and M11 and M13 need the diagram layer of Milestone 5. While
the ledger shows the prerequisite incomplete, those findings print as
`REPORT (deferred: ...)` instead of failing the run.

`validate.py --final` ignores every gate and promotes every `REPORT` to `ERROR`.
It is step 12's acceptance test, and it is expected to fail until the setting is
finished.
