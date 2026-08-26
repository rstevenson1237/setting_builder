#!/usr/bin/env python3
"""Create file stubs, frontmatter and empty headings for a scale.

Scaffolding is deterministic, so it runs here rather than as a prose
instruction. This script also fixes the shape the rest of the pipeline
assumes: which headings a body carries, how an Exits table is laid out, how a
region's referee table is numbered, and where a diagram marker sits.
`validate.py` checks that shape, so the two files agree by construction.

The Architect overwrites freely until a Builder pass has touched a file. After
that `state/ledger.json` marks the target built and this script refuses,
because a regeneration is a booked step re-run rather than a hand-patch.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402
import ledger as ledger_mod  # noqa: E402

NOTE = "[[ {} ]]"


class ScaffoldError(Exception):
    """The stub could not be written as asked."""


def _pairs(values: list[str], label: str) -> list[dict[str, str]]:
    """Parse repeated ``id=Name`` arguments into container entries."""
    entries: list[dict[str, str]] = []
    for value in values:
        if "=" not in value:
            raise ScaffoldError(f"{label} {value!r} is not in id=Name form")
        ident, name = value.split("=", 1)
        ident = ident.strip()
        name = name.strip()
        if not common.RE_SLUG.match(ident):
            raise ScaffoldError(f"container id {ident!r} is not a lowercase slug")
        if not name:
            raise ScaffoldError(f"container {ident!r} has no name")
        entries.append({"id": ident, "name": name})
    return entries


def _tags(value: str) -> list[str]:
    tags = [tag.strip() for tag in value.split(",") if tag.strip()]
    if len(tags) != 3:
        raise ScaffoldError(f"expected exactly three tags, got {len(tags)}")
    return tags


def _guard(path: Path, code: str, root: Path, args: argparse.Namespace) -> None:
    """Two separate refusals, because they mean different things.

    Replacing a stub is ordinary Architect work and `--force` covers it.
    Replacing a file a Builder has already written destroys content, so it takes
    `--rerun`, which is the flag a booked step re-run passes and nothing else does.
    """
    led = ledger_mod.load(root)
    if led.is_built(code) and not getattr(args, "rerun", False):
        raise ScaffoldError(
            f"{code} is marked built in the ledger. Regeneration is a booked step "
            f"re-run, not a hand-patch. Pass --rerun only inside that re-run."
        )
    if path.exists() and not (args.force or getattr(args, "rerun", False)):
        raise ScaffoldError(f"{path.relative_to(root)} already exists. Pass --force to replace it.")


def _table_block(headers: list[str], rows: list[list[str]] | None = None) -> str:
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join([":---"] * len(headers)) + " |"]
    for row in rows or []:
        cells = list(row) + [""] * (len(headers) - len(row))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Setting
# --------------------------------------------------------------------------


def scaffold_setting(root: Path, args: argparse.Namespace) -> list[Path]:
    containers = _pairs(args.container, "--container")
    if not containers:
        raise ScaffoldError("a setting needs at least one setting-level container")

    fm: dict[str, Any] = {
        "name": args.name,
        "tags": _tags(args.tags),
        "seed": args.seed,
        "containers": containers,
        "schema_version": common.SCHEMA_VERSION,
    }

    catalogue = [
        [code, name, "S", "no"] for code, name in sorted(common.S_TABLES.items())
    ] + [
        [code, name, "T", "yes" if code in common.DECORATED_TABLES else "no"]
        for code, name in sorted(common.T_TABLES.items())
    ]

    diagrams = [f"<!-- DIAGRAM: {common.diagram_name(1, 'SETTING')} -->"]
    for container in containers:
        diagrams.append(f"<!-- DIAGRAM: {common.diagram_name(2, container['id'])} -->")

    body = "\n\n".join(
        [
            "## Overview",
            NOTE.format("Written at step 4, Decorator, in Player register."),
            "## Style",
            NOTE.format("Written at step 4, Decorator."),
            "## Tables",
            _table_block(["Code", "Table", "Kind", "Decorated"], catalogue),
            "## Regions",
            # The index carries placement only. Difficulty and weight are dials,
            # and they live in the region's own frontmatter so they cannot drift.
            _table_block(["Code", "Name", "Type", "Container"]),
            "\n\n".join(diagrams),
        ]
    )

    path = root / common.SETTING_DIR / "setting.md"
    _guard(path, "setting", root, args)
    common.write_doc(path, fm, body)

    conn = root / common.SETTING_DIR / "connections.md"
    written = [path]
    if not conn.exists() or args.force:
        common.write_doc(
            conn,
            {"scale": "setting", "schema_version": common.SCHEMA_VERSION},
            "# Region connections\n\n"
            "Region to region. Binary and untyped: tiers 1 to 3 answer only whether "
            "two nodes connect. Type is drawn at tier 4 and nowhere else.\n\n"
            + _table_block(["From", "To"]),
        )
        written.append(conn)

    led = ledger_mod.load(root)
    if led.seed is None:
        led.data["seed"] = args.seed
        led.save()
    return written


# --------------------------------------------------------------------------
# Tables
# --------------------------------------------------------------------------


def scaffold_tables(root: Path, args: argparse.Namespace) -> list[Path]:
    wanted = args.only or (sorted(common.S_TABLES) + sorted(common.T_TABLES))
    written: list[Path] = []
    for code in wanted:
        if code in common.S_TABLES:
            kind, name = "S", common.S_TABLES[code]
        elif code in common.T_TABLES:
            kind, name = "T", common.T_TABLES[code]
        else:
            raise ScaffoldError(f"{code} is not in the table catalogue")

        fm: dict[str, Any] = {"code": code, "name": name, "kind": kind}
        if kind == "T":
            fm["decorate"] = code in common.DECORATED_TABLES
            fm["draws_on"] = []
        fm["schema_version"] = common.SCHEMA_VERSION

        note = (
            "Rows written at step 3, Builder. Entries decorated at step 4."
            if code in common.DECORATED_TABLES
            else "Rows written at step 3, Builder. This table stops at Builder."
        )
        body = NOTE.format(note) + "\n\n" + _table_block(common.table_columns(code))

        path = root / common.TABLES_DIR / f"{code}-{common.slugify(name)}.md"
        _guard(path, code, root, args)
        common.write_doc(path, fm, body)
        written.append(path)
    return written


# --------------------------------------------------------------------------
# Region
# --------------------------------------------------------------------------


def scaffold_region(root: Path, args: argparse.Namespace) -> list[Path]:
    weights = common.load_weights(root)
    if not common.RE_REGION_CODE.match(args.code):
        raise ScaffoldError(f"{args.code} is not a region code such as R03")
    if args.type not in weights["region_types"]:
        raise ScaffoldError(f"{args.type} is not one of {weights['region_types']}")
    if args.difficulty not in weights["difficulty"]["dice"]:
        raise ScaffoldError(f"{args.difficulty} is not one of {weights['difficulty']['dice']}")
    if args.weight not in weights["region_weights"]:
        raise ScaffoldError(f"{args.weight} is not one of {sorted(weights['region_weights'])}")

    containers = _pairs(args.sub, "--sub")
    if not containers:
        raise ScaffoldError("a region needs at least one region-level container")

    fm: dict[str, Any] = {
        "code": args.code,
        "name": args.name,
        "tags": _tags(args.tags),
        "type": args.type,
        "difficulty": args.difficulty,
        "weight": args.weight,
        "container": args.container,
        "containers": containers,
        "sources": [],
        "schema_version": common.SCHEMA_VERSION,
    }

    table_name, direction = common.REGION_TABLE_BY_TYPE[args.type]
    rows_count = int(weights["region_tables"]["rows"])
    order = range(rows_count, 0, -1) if direction == "descending" else range(1, rows_count + 1)
    region_table = _table_block(["Roll", table_name[:-1]], [[str(n), ""] for n in order])

    tables_section = [f"### {table_name}", region_table]
    if args.weather:
        weather_rows = int(weights["region_tables"]["weather_rows"])
        tables_section += [
            "### Weather",
            _table_block(["Roll", "Weather"], [[str(n), ""] for n in range(1, weather_rows + 1)]),
        ]

    diagrams = [f"<!-- DIAGRAM: {common.diagram_name(3, args.code)} -->"]
    for container in containers:
        diagrams.append(
            f"<!-- DIAGRAM: {common.diagram_name(4, args.code, container['id'])} -->"
        )

    body = "\n\n".join(
        [
            "## Overview",
            NOTE.format("Written at step 8, Decorator, in Player register."),
            "## Fields",
            NOTE.format("Written at step 7, Builder."),
            "## Tables",
            "\n\n".join(tables_section),
            "## Connections",
            NOTE.format(
                "Written at step 6, Engineer. Edges live in this region's "
                "connections.md, which is the source of truth."
            ),
            "## Diagram",
            "\n\n".join(diagrams),
        ]
    )

    region_dir = root / common.REGIONS_DIR / f"{args.code}-{common.slugify(args.name)}"
    path = region_dir / "region.md"
    _guard(path, args.code, root, args)
    common.write_doc(path, fm, body)
    (region_dir / "locations").mkdir(parents=True, exist_ok=True)

    written = [path]
    conn = region_dir / "connections.md"
    if not conn.exists() or args.force:
        common.write_doc(
            conn,
            {"code": args.code, "scale": "region", "schema_version": common.SCHEMA_VERSION},
            "# Location connections\n\n"
            "Location to location, and typed. Tier 4 is the one tier that draws "
            "connection type. A row with One-way `no` must appear in the Exits table "
            "of both locations.\n\n"
            + _table_block(["From", "To", "Type", "One-way"]),
        )
        written.append(conn)
    return written


# --------------------------------------------------------------------------
# Location
# --------------------------------------------------------------------------


def scaffold_location(root: Path, args: argparse.Namespace) -> list[Path]:
    weights = common.load_weights(root)
    if not common.RE_LOCATION_CODE.match(args.code):
        raise ScaffoldError(f"{args.code} is not a location code such as R03-L07")
    region_code = args.code.split("-")[0]

    corpus = common.load_corpus(root)
    region = corpus.regions.get(region_code)
    if region is None:
        raise ScaffoldError(f"region {region_code} does not exist yet. Scaffold it first.")
    region_type = str(region.fm.get("type", ""))
    if region_type not in common.REQUIRED_FIELDS_BY_TYPE:
        raise ScaffoldError(f"region {region_code} carries no usable type")

    if args.weight not in weights["location_weights"]:
        raise ScaffoldError(f"{args.weight} is not one of {weights['location_weights']}")
    cell = f"{region_type}_{args.weight}"

    declared = {c["id"] for c in region.fm.get("containers", []) if isinstance(c, dict)}
    if args.container not in declared:
        raise ScaffoldError(
            f"{args.container!r} is not a container of {region_code}. "
            f"Declared: {', '.join(sorted(declared)) or 'none'}"
        )

    fm: dict[str, Any] = {
        "code": args.code,
        "name": args.name,
        "tags": _tags(args.tags),
        "region": region_code,
        "container": args.container,
        "cell": cell,
        "pattern": args.pattern,
        "sources": [],
        "schema_version": common.SCHEMA_VERSION,
    }

    fields = "\n".join(
        f"**{label}:** " for label in common.REQUIRED_FIELDS_BY_TYPE[region_type]
    )

    body = "\n\n".join(
        [
            "## Player Overview",
            NOTE.format(
                "Written at step 12, Decorator, in Player register. Every bolded "
                "noun here needs a feature below it."
            ),
            "## Referee Overview",
            fields,
            NOTE.format("Fields written at step 11, Builder. Prose at step 12, Decorator."),
            "## Features",
            NOTE.format(
                "Written at step 11, Builder. One `### Name` per feature. A "
                "connection pointer inside a feature is the only place `->` may appear."
            ),
            "## Exits",
            _table_block(["To", "Type", "Cue"]),
        ]
    )

    path = region.path.parent / "locations" / f"{args.code}-{common.slugify(args.name)}.md"
    _guard(path, args.code, root, args)
    common.write_doc(path, fm, body)
    return [path]


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--root", type=Path, default=common.REPO_ROOT)
    shared.add_argument("--force", action="store_true",
                        help="replace an existing stub")
    shared.add_argument("--rerun", action="store_true",
                        help="replace a file marked built. Only a booked step re-run passes this.")

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="scale", required=True)

    p_set = sub.add_parser("setting", parents=[shared], help="stub setting.md and connections.md")
    p_set.add_argument("--name", required=True)
    p_set.add_argument("--tags", required=True, help="exactly three, comma separated")
    p_set.add_argument("--seed", type=int, required=True)
    p_set.add_argument("--container", action="append", default=[],
                       help="id=Name, repeatable, setting-level")

    p_tab = sub.add_parser("tables", parents=[shared], help="stub the S and T table files")
    p_tab.add_argument("--only", nargs="*", default=[], help="table codes, default all 24")

    p_reg = sub.add_parser("region", parents=[shared], help="stub one region")
    p_reg.add_argument("--code", required=True)
    p_reg.add_argument("--name", required=True)
    p_reg.add_argument("--tags", required=True)
    p_reg.add_argument("--type", required=True)
    p_reg.add_argument("--difficulty", required=True)
    p_reg.add_argument("--weight", required=True)
    p_reg.add_argument("--container", required=True, help="the setting-level container")
    p_reg.add_argument("--sub", action="append", default=[],
                       help="id=Name, repeatable, region-level")
    p_reg.add_argument("--weather", action="store_true", help="the region has outdoor extent")

    p_loc = sub.add_parser("location", parents=[shared], help="stub one location")
    p_loc.add_argument("--code", required=True)
    p_loc.add_argument("--name", required=True)
    p_loc.add_argument("--tags", required=True)
    p_loc.add_argument("--container", required=True, help="the region-level container")
    p_loc.add_argument("--weight", required=True, choices=["LOW", "MEDIUM", "HIGH"])
    p_loc.add_argument("--pattern", default="", help="report only, never fails a check")

    args = parser.parse_args(argv)
    root = args.root.resolve()

    handlers = {
        "setting": scaffold_setting,
        "tables": scaffold_tables,
        "region": scaffold_region,
        "location": scaffold_location,
    }
    try:
        written = handlers[args.scale](root, args)
    except (ScaffoldError, common.DocError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for path in written:
        print(f"wrote {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
