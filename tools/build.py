#!/usr/bin/env python3
"""Splice the diagram markers and assemble ``build/playbook.md``.

The content tree is the source and the playbook is the artifact. Everything
this script does is a projection: it never decides anything, and deleting the
playbook loses nothing that cannot be rebuilt from the tree in one command.

Four projections, and each is here because the alternative is a hand-edit that
cannot survive a regeneration.

- **Diagram markers.** A host file carries `<!-- DIAGRAM: T4_R03_X.md -->` and
  no mermaid of its own. This splices in the derived file (SPEC.md 5.3).
- **Section marks.** `(BESTIARY, Fen-wight)` resolves to the row it names and
  becomes a link to it (SPEC.md 10.6). The playbook is the one document where
  both ends are present, so it is the one place the link can be written.
- **Architect notes.** `[[ ... ]]` is architect visibility and must not survive
  into the artifact (SPEC.md 4.6). They are struck here and counted, and
  `validate.py` M25 stays the check that says whether they should have been
  gone already.
- **Heading depth.** Each file's own body opens at `##`. Nesting a location
  under its region under the setting demotes those headings so one document
  keeps one outline.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402

PLAYBOOK_PATH = "build/playbook.md"

# The deepest heading markdown carries. A location body's `###` feature sits at
# this depth once demoted, which is what fixes the nesting below.
MAX_DEPTH = 6

RE_HEADING = re.compile(r"^(#{1,6})(\s+)(.*)$")


class BuildError(Exception):
    """The playbook could not be assembled."""


@dataclass
class Build:
    """One assembly run: the text, and what it had to say about the tree."""

    text: str = ""
    diagrams: int = 0
    links: int = 0
    notes: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------
# Projections
# --------------------------------------------------------------------------


def splice(body: str, root: Path, code: str, build: Build) -> str:
    """Replace each diagram marker with the derived diagram it names."""

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        path = root / common.DIAGRAMS_DIR / name
        if not path.exists():
            build.problems.append(
                f"{code}: marker names {name}, which is not derived. "
                f"Run python tools/mermaid_gen.py."
            )
            return match.group(0)
        build.diagrams += 1
        return path.read_text(encoding="utf-8").strip()

    return common.RE_DIAGRAM_MARKER.sub(replace, body)


def anchor(entry_id: str) -> str:
    """The playbook anchor for one table row."""
    return re.sub(r"[^a-z0-9]+", "-", entry_id.lower()).strip("-")


def link_marks(body: str, corpus: common.Corpus, code: str, build: Build) -> str:
    """Turn every `(SECTION, key)` mark into a link to the row it names.

    A mark that resolves to no row is left as written and reported. It is M16's
    finding, and the build restating it as a broken link would hide it.
    """
    by_section = corpus.table_by_section()

    def replace(match: re.Match[str]) -> str:
        section, key = match.group(1), match.group(2).strip()
        table = by_section.get(common.normalise_key(section))
        if table is None:
            build.problems.append(f"{code}: ({section}, {key}) names no table")
            return match.group(0)
        row = common.resolve_entry(corpus.table_rows(table), key)
        if row is None:
            build.problems.append(f"{code}: ({section}, {key}) resolves to no row in {table}")
            return match.group(0)
        entry_id = row.get("ID", "").strip()
        if not entry_id:
            build.problems.append(f"{code}: ({section}, {key}) reaches a row with no ID")
            return match.group(0)
        build.links += 1
        return f"([{section}, {key}](#{anchor(entry_id)}))"

    return common.RE_SECTION_MARK.sub(replace, body)


def strike_notes(body: str, code: str, build: Build) -> str:
    """Remove every architect note, and say where one was."""
    found = common.RE_ARCHITECT_NOTE.findall(body)
    if not found:
        return body
    build.notes += [code] * len(found)
    stripped = common.RE_ARCHITECT_NOTE.sub("", body)
    # A note on its own line leaves the line behind. Collapse the hole rather
    # than shipping a run of blank lines into the artifact.
    return re.sub(r"\n{3,}", "\n\n", stripped)


def anchor_rows(body: str) -> str:
    """Give each table row an anchor, so a section mark has something to reach.

    The anchor goes in the ID cell, which is the cell that names the row. It is
    invisible once rendered and it is the only HTML the playbook carries.
    """
    lines = body.split("\n")
    out: list[str] = []
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.strip().startswith("|"):
            cells = line.split("|")
            # cells[0] is the empty string before the leading pipe.
            if len(cells) > 2 and common.RE_ENTRY_ID.match(cells[1].strip()):
                entry_id = cells[1].strip()
                cells[1] = f' <a id="{anchor(entry_id)}"></a>{entry_id} '
                line = "|".join(cells)
        out.append(line)
    return "\n".join(out)


def demote(body: str, by: int) -> str:
    """Push every heading down ``by`` levels, leaving fenced blocks alone."""
    if by <= 0:
        return body
    out: list[str] = []
    in_fence = False
    for line in body.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        match = RE_HEADING.match(line) if not in_fence else None
        if match:
            depth = min(len(match.group(1)) + by, MAX_DEPTH)
            line = "#" * depth + match.group(2) + match.group(3)
        out.append(line)
    return "\n".join(out)


def render_doc(doc: common.Doc, root: Path, corpus: common.Corpus, under: int,
               build: Build) -> str:
    """One content file, nested under a playbook heading at level ``under``."""
    code = doc.code or doc.scale
    body = splice(doc.body, root, code, build)
    body = anchor_rows(body)
    body = link_marks(body, corpus, code, build)
    body = strike_notes(body, code, build)
    # A body opens at `##`, so demoting by `under - 1` puts its first heading
    # at `under + 1`: one level under the heading this file sits beneath.
    return demote(body, under - 1).strip()


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------


def title_of(doc: common.Doc) -> str:
    code = doc.code
    name = str(doc.fm.get("name", "")).strip()
    return f"{code} {name}".strip() if code else name


def assemble(root: Path) -> Build:
    """The whole playbook: setting, tables, then each region with its locations."""
    corpus = common.load_corpus(root)
    build = Build()

    for path, message in corpus.read_errors:
        build.problems.append(f"{path.relative_to(root)} could not be read: {message}")

    if corpus.setting is None:
        raise BuildError(
            f"{common.SETTING_DIR}/setting.md does not exist. There is nothing to build."
        )

    name = str(corpus.setting.fm.get("name", "The setting"))
    parts = [
        f"# {name}",
        "",
        "Assembled by `tools/build.py` from the content tree. Every diagram is "
        "spliced from `build/diagrams/`, every table reference is a link, and no "
        "architect note survives. Do not edit: rebuild it.",
        "",
        "## Setting",
        "",
        render_doc(corpus.setting, root, corpus, 2, build),
        "",
        "## Tables",
        "",
    ]

    catalogue = sorted(common.S_TABLES) + sorted(common.T_TABLES)
    for code in catalogue:
        doc = corpus.tables.get(code)
        if doc is None:
            build.problems.append(f"{code} is in the catalogue and has no file")
            continue
        parts += [
            f"### {code} {doc.fm.get('name', '')}".rstrip(),
            "",
            render_doc(doc, root, corpus, 3, build),
            "",
        ]

    parts += ["## Regions", ""]
    for region_code, region in sorted(corpus.regions.items()):
        parts += [
            f"### {title_of(region)}",
            "",
            render_doc(region, root, corpus, 3, build),
            "",
        ]
        for location in sorted(corpus.locations_in(region_code), key=lambda d: d.code):
            parts += [
                f"#### {title_of(location)}",
                "",
                render_doc(location, root, corpus, 4, build),
                "",
            ]

    build.text = "\n".join(parts).rstrip("\n") + "\n"
    return build


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def report(build: Build, root: Path) -> None:
    print(f"{build.diagrams} diagrams spliced, {build.links} references linked.")
    if build.notes:
        counts: dict[str, int] = {}
        for code in build.notes:
            counts[code] = counts.get(code, 0) + 1
        listing = ", ".join(f"{code} ({count})" for code, count in sorted(counts.items()))
        print(
            f"struck {len(build.notes)} architect notes: {listing}\n"
            f"A note is struck when its content is absorbed. These were still open.",
            file=sys.stderr,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", type=Path, default=common.REPO_ROOT)
    parser.add_argument("--out", type=Path, default=None,
                        help=f"where to write, default {PLAYBOOK_PATH}")
    parser.add_argument("--check", action="store_true",
                        help="assemble and report, but write nothing")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    try:
        build = assemble(root)
    except (BuildError, common.DocError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if build.problems:
        for problem in build.problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1

    report(build, root)
    if args.check:
        print("assembled cleanly. Nothing written.")
        return 0

    out = args.out if args.out is not None else root / PLAYBOOK_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build.text, encoding="utf-8")
    try:
        shown = out.relative_to(root)
    except ValueError:
        shown = out
    print(f"wrote {shown}, {len(build.text.splitlines())} lines.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
