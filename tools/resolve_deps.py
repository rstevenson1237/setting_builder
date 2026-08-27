#!/usr/bin/env python3
"""Expand a pattern's dependency selectors into one bundle.

A bundle is the whole context for one generation call. `resolve_deps.py` reads
the pattern's frontmatter, fills the variables from the command arguments,
resolves each of the seven selector forms against the content tree, injects the
genre and the mechanics map, and writes `build/bundles/<pattern-id>-<code>.md`.

Two rules are enforced here rather than trusted to a writer. The S boundary is
mechanical: a `table:S-...` selector is refused on any pattern whose target is
a location, because S content reaches a player through a T table and never
directly. The genre cap is mechanical too: `patterns/GENRE.md` enters every
bundle, so its size is a tax on every subagent call.

`GENRE.md` and `MECHANICS.md` are injected and never declared. The cell file
and the config arrive as ordinary selectors, so a pattern that needs them says
so and a pattern that does not carries neither.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402

CONTRACT = """This bundle is the whole context for one generation call. Read the pattern, this
bundle and the current target file. Return the complete replacement content of
the target file and nothing else.

Never read the `setting/` tree directly. If a fact you need is not here, the
dependency selector was wrong and the pattern has to change."""


class ResolveError(Exception):
    """The bundle could not be resolved as asked."""


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


def guidance(path: Path, label: str) -> str:
    """A file read for its prose. Frontmatter is dropped if it carries any."""
    if not path.exists():
        raise ResolveError(f"{label} is missing: {path}")
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        try:
            _, text = common.split_frontmatter(text)
        except common.DocError:
            pass
    return text.strip()


def render_doc(doc: common.Doc) -> str:
    """A content file, whole: its frontmatter as YAML and its body as written."""
    front = yaml.safe_dump(doc.fm, sort_keys=False, allow_unicode=True,
                           default_flow_style=None).rstrip("\n")
    return f"```yaml\n{front}\n```\n\n{doc.body.strip()}"


def fence(text: str) -> str:
    """Wrap a file quoted whole, so its own headings cannot read as the bundle's.

    A tilde fence is used because the quoted text carries backtick fences of its
    own, and it is lengthened if the text somehow carries tilde fences too.
    """
    longest = max((len(run) for run in re.findall(r"~{3,}", text)), default=0)
    rail = "~" * max(3, longest + 1)
    return f"{rail}markdown\n{text.strip()}\n{rail}"


def section(title: str, source: str | list[str], body: str,
            verbatim: bool = False) -> str:
    """One bundle section. `verbatim` quotes a file that is carried whole."""
    sources = [source] if isinstance(source, str) else list(source)
    named = " and ".join(f"`{item}`" for item in sources)
    body = fence(body) if verbatim else body.strip()
    return f"## {title}\n\nFrom {named}.\n\n{body}"


def table_block(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join([":---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Resolution
# --------------------------------------------------------------------------


class Resolver:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.corpus = common.load_corpus(root)
        self.weights = common.load_weights(root)
        self.notes: list[str] = []
        # The code the bundle is for. A target is not its own sibling, and the
        # writer already holds its own file.
        self.target = ""

    # -- injected ---------------------------------------------------------

    def genre(self) -> str:
        """The genre brief, checked against the cap it is capped at for a reason."""
        path = self.root / common.GENRE_PATH
        if not path.exists():
            raise ResolveError(
                f"{common.GENRE_PATH} does not exist. It is generated from "
                f"{common.GENRE_EXAMPLE_PATH} at Milestone 2, and every bundle carries it."
            )
        text = guidance(path, common.GENRE_PATH)
        cap = int(self.weights["genre"]["max_words"])
        words = len(text.split())
        if words > cap:
            raise ResolveError(
                f"{common.GENRE_PATH} is {words} words, over the {cap} word cap. "
                f"It enters every bundle, so its size is a tax on every call. "
                f"Demote what is true of one region into that region."
            )
        return text

    # -- selectors --------------------------------------------------------

    def resolve(self, selector: common.Selector) -> str:
        handler = {
            "table": self.resolve_table,
            "region": self.resolve_region,
            "container": self.resolve_container,
            "siblings": self.resolve_siblings,
            "cell": self.resolve_cell,
            "config": self.resolve_config,
        }[selector.kind]
        return handler(selector.value)

    def resolve_table(self, code: str) -> str:
        doc = self.corpus.tables.get(code)
        if doc is None:
            raise ResolveError(
                f"table {code} does not exist. Scaffold it: python tools/scaffold.py "
                f"tables --only {code}."
            )
        name = doc.fm.get("name", code)
        return section(f"Table {code}: {name}", doc.relpath, render_doc(doc),
                       verbatim=True)

    def resolve_region(self, code: str) -> str:
        doc = self.region(code)
        front = yaml.safe_dump(doc.fm, sort_keys=False, allow_unicode=True,
                               default_flow_style=None).rstrip("\n")
        overview = doc.section("Overview")
        body = overview.full_text.strip() if overview else "[[ not written yet ]]"
        if overview is None:
            self.notes.append(f"{code} carries no Overview yet. It is written at step 8.")
        return section(f"Region {code}: {doc.fm.get('name', code)}", doc.relpath,
                       f"```yaml\n{front}\n```\n\n### Overview\n\n{body}")

    def resolve_container(self, container_id: str) -> str:
        """A container's member list, and its diagram.

        Type is drawn at tier 4 and nowhere else, so a region-level container
        carries its tier-4 diagram. A setting-level container carries the tier-2
        diagram of the same grouping, which is the binary view of its regions.
        """
        region = next(
            (doc for doc in self.corpus.regions.values()
             if container_id in self.container_ids(doc)),
            None,
        )
        if region is not None:
            members = [
                [doc.code, str(doc.fm.get("name", "")), str(doc.fm.get("cell", ""))]
                for doc in sorted(self.corpus.locations_in(region.code),
                                  key=lambda d: d.code)
                if str(doc.fm.get("container", "")) == container_id
            ]
            listing = table_block(["Code", "Name", "Cell"], members) if members \
                else "No locations yet. They are stubbed at step 9."
            diagram = common.diagram_name(4, region.code, container_id)
            name = self.container_name(region, container_id)
            return section(
                f"Container {container_id}: {name}",
                [region.relpath, f"{common.DIAGRAMS_DIR}/{diagram}"],
                f"A region-level container of {region.code}. Its locations:\n\n"
                f"{listing}\n\n{self.diagram(diagram)}",
            )

        setting = self.corpus.setting
        if setting is not None and container_id in self.container_ids(setting):
            members = [
                [doc.code, str(doc.fm.get("name", "")), str(doc.fm.get("type", "")),
                 str(doc.fm.get("weight", ""))]
                for doc in sorted(self.corpus.regions.values(), key=lambda d: d.code)
                if str(doc.fm.get("container", "")) == container_id
            ]
            listing = table_block(["Code", "Name", "Type", "Weight"], members) if members \
                else "No regions yet. They are stubbed at step 5."
            diagram = common.diagram_name(2, container_id)
            name = self.container_name(setting, container_id)
            return section(
                f"Container {container_id}: {name}",
                [setting.relpath, f"{common.DIAGRAMS_DIR}/{diagram}"],
                f"A setting-level container. Its regions:\n\n"
                f"{listing}\n\n{self.diagram(diagram)}",
            )

        declared = sorted(
            set().union(*(self.container_ids(doc) for doc in self.every_holder())) or set()
        )
        raise ResolveError(
            f"no container {container_id!r} is declared. Declared: "
            f"{', '.join(declared) or 'none'}."
        )

    def resolve_siblings(self, region_code: str) -> str:
        region = self.region(region_code)
        rows = [
            [doc.code, str(doc.fm.get("name", "")),
             ", ".join(str(tag) for tag in doc.fm.get("tags", []) or []),
             str(doc.fm.get("cell", ""))]
            for doc in sorted(self.corpus.locations_in(region_code), key=lambda d: d.code)
            if doc.code != self.target
        ]
        body = table_block(["Code", "Name", "Tags", "Cell"], rows) if rows \
            else "No sibling locations yet. They are stubbed at step 9."
        return section(
            f"Sibling locations in {region_code}",
            f"{region.path.parent.relative_to(self.root)}/locations/",
            "Code, name, tags and cell only. A sibling's content is not carried, "
            "because a writer that needs it is reading the wrong bundle.\n\n" + body,
        )

    def resolve_cell(self, cell: str) -> str:
        path = self.root / common.CELLS_DIR / f"{cell}.md"
        if not path.exists():
            raise ResolveError(
                f"{path.relative_to(self.root)} does not exist. The nine cell files are "
                f"written at Milestone 3, and nothing good is generated before they exist."
            )
        return section(f"Cell {cell}", str(path.relative_to(self.root)),
                       guidance(path, f"cell {cell}"), verbatim=True)

    def resolve_config(self, _: str) -> str:
        text = (self.root / common.WEIGHTS_PATH).read_text(encoding="utf-8").strip()
        return section("Config", common.WEIGHTS_PATH,
                       "Every number with two consumers. Cite a key by name; never copy "
                       f"a checked number into prose.\n\n```yaml\n{text}\n```")

    # -- helpers ----------------------------------------------------------

    def region(self, code: str) -> common.Doc:
        doc = self.corpus.regions.get(code)
        if doc is None:
            known = ", ".join(sorted(self.corpus.regions)) or "none"
            raise ResolveError(f"region {code} does not exist. Known: {known}.")
        return doc

    def every_holder(self) -> list[common.Doc]:
        holders = list(self.corpus.regions.values())
        if self.corpus.setting is not None:
            holders.append(self.corpus.setting)
        return holders or [common.Doc(Path(), {}, "", "setting")]

    @staticmethod
    def container_ids(doc: common.Doc) -> set[str]:
        return {
            str(entry["id"])
            for entry in doc.fm.get("containers", []) or []
            if isinstance(entry, dict) and "id" in entry
        }

    @staticmethod
    def container_name(doc: common.Doc, container_id: str) -> str:
        for entry in doc.fm.get("containers", []) or []:
            if isinstance(entry, dict) and entry.get("id") == container_id:
                return str(entry.get("name", container_id))
        return container_id

    def diagram(self, name: str) -> str:
        path = self.root / common.DIAGRAMS_DIR / name
        if not path.exists():
            self.notes.append(
                f"{name} is not derived yet. mermaid_gen.py arrives at Milestone 5."
            )
            return f"Diagram `{name}` is not derived yet."
        return path.read_text(encoding="utf-8").strip()


# --------------------------------------------------------------------------
# Variables and the bundle
# --------------------------------------------------------------------------


def variables_for(resolver: Resolver, target: str, overrides: dict[str, str]) -> dict[str, str]:
    """Fill `${...}` from the target code, reading the tree for what it implies."""
    variables: dict[str, str] = {}
    if common.RE_LOCATION_CODE.match(target):
        variables["LOCATION_CODE"] = target
        variables["REGION_CODE"] = target.split("-")[0]
        location = resolver.corpus.locations.get(target)
        if location is not None:
            variables["CONTAINER_ID"] = str(location.fm.get("container", ""))
            variables["CELL"] = str(location.fm.get("cell", ""))
    elif common.RE_REGION_CODE.match(target):
        variables["REGION_CODE"] = target
        region = resolver.corpus.regions.get(target)
        if region is not None:
            # The setting-level container the region sits in. A region-level one
            # is a choice among several and is named with --var.
            variables["CONTAINER_ID"] = str(region.fm.get("container", ""))
    variables.update(overrides)
    return {name: value for name, value in variables.items() if value}


def check_s_boundary(pattern: common.Pattern, selectors: list[common.Selector]) -> None:
    if pattern.target != "location":
        return
    for selector in selectors:
        if selector.kind == "table" and selector.value.startswith("S-"):
            raise ResolveError(
                f"{pattern.id} targets a location and declares {selector.raw!r}. "
                f"S tables are referee-facing and no location may cite one. S content "
                f"reaches a player through a T table, never directly."
            )


def build_bundle(resolver: Resolver, pattern: common.Pattern, target: str,
                 variables: dict[str, str]) -> str:
    try:
        selectors = pattern.selectors(variables)
    except common.SelectorError as exc:
        raise ResolveError(str(exc)) from exc
    check_s_boundary(pattern, selectors)

    resolver.target = target
    genre = resolver.genre()
    mechanics = guidance(resolver.root / common.MECHANICS_PATH, common.MECHANICS_PATH)

    parts = [
        section("Genre", common.GENRE_PATH, genre, verbatim=True),
        section("Mechanics", common.MECHANICS_PATH, mechanics, verbatim=True),
    ]
    for selector in selectors:
        parts.append(resolver.resolve(selector))

    if pattern.output_template:
        template = resolver.root / common.PATTERNS_DIR / pattern.output_template
        parts.append(section("Output template",
                             f"{common.PATTERNS_DIR}/{pattern.output_template}",
                             guidance(template, "output_template"), verbatim=True))

    fm = {
        "pattern": pattern.id,
        "target": target,
        "phase": pattern.phase,
        "writes": pattern.writes,
        "dependencies": [selector.raw for selector in selectors],
        "schema_version": common.SCHEMA_VERSION,
    }
    front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                           default_flow_style=None).rstrip("\n")
    body = "\n\n".join([f"# Bundle: {pattern.id} for {target}", CONTRACT, *parts])
    return f"---\n{front}\n---\n\n{body}\n"


def bundle_path(root: Path, pattern_id: str, target: str) -> Path:
    return root / common.BUNDLES_DIR / f"{pattern_id}-{target}.md"


def default_target(pattern: common.Pattern) -> str:
    if pattern.target == "setting":
        return "setting"
    raise ResolveError(
        f"{pattern.id} targets a {pattern.target}, so it needs --target <code>."
    )


# --------------------------------------------------------------------------
# Check mode
# --------------------------------------------------------------------------


def check(root: Path) -> list[str]:
    """Everything resolvable without a target: the cap, and every pattern's shape."""
    problems: list[str] = []
    resolver = Resolver(root)
    if (root / common.GENRE_PATH).exists():
        try:
            resolver.genre()
        except ResolveError as exc:
            problems.append(str(exc))

    patterns, read_errors = common.load_patterns(root)
    problems += [f"{path.relative_to(root)}: {message}" for path, message in read_errors]
    for pattern in patterns:
        problems += [f"{pattern.relpath}: {problem}"
                     for problem in common.pattern_errors(pattern, root)]
        try:
            check_s_boundary(pattern, [
                common.parse_selector(raw) for raw in pattern.dependencies
            ])
        except (ResolveError, common.SelectorError) as exc:
            problems.append(f"{pattern.relpath}: {exc}")
    return problems


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", type=Path, default=common.REPO_ROOT)
    parser.add_argument("--pattern", help="the pattern id, as listed in DESIGN_PATTERNS.md")
    parser.add_argument("--target", help="the code the bundle is for, such as R03-L07")
    parser.add_argument("--var", action="append", default=[], metavar="NAME=VALUE",
                        help=f"fill a variable. One of: {', '.join(common.VARIABLES)}")
    parser.add_argument("--stdout", action="store_true",
                        help="print the bundle instead of writing it")
    parser.add_argument("--check", action="store_true",
                        help="check the genre cap and every pattern's shape, and write nothing")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.check:
        try:
            problems = check(root)
        except (common.DocError, ResolveError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        if problems:
            return 1
        print("patterns and genre are within their bounds.")
        return 0

    if not args.pattern:
        parser.error("--pattern is required unless --check is passed")

    overrides: dict[str, str] = {}
    for item in args.var:
        if "=" not in item:
            print(f"error: --var {item!r} is not in NAME=VALUE form", file=sys.stderr)
            return 2
        name, value = item.split("=", 1)
        overrides[name.strip().upper()] = value.strip()

    try:
        pattern = common.find_pattern(args.pattern, root)
        problems = common.pattern_errors(pattern, root)
        if problems:
            raise ResolveError(
                f"{pattern.relpath} is not a usable pattern: " + "; ".join(problems)
            )
        resolver = Resolver(root)
        target = args.target or default_target(pattern)
        variables = variables_for(resolver, target, overrides)
        bundle = build_bundle(resolver, pattern, target, variables)
    except (ResolveError, common.DocError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for note in resolver.notes:
        print(f"note: {note}")

    if args.stdout:
        print(bundle)
        return 0

    path = bundle_path(root, pattern.id, target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(bundle, encoding="utf-8")
    words = len(bundle.split())
    print(f"wrote {path.relative_to(root)}: {words} words.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
