#!/usr/bin/env python3
"""Seeded dice and weighted table rolls. All randomness passes through here.

A language model produces biased, non-reproducible randomness, so nothing in
this repository rolls in prose. The seed for any roll is derived from the
setting seed, the target code and a nonce, which means the same target rolls
the same result on a rebuild and two different targets do not share a stream.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402
import ledger as ledger_mod  # noqa: E402

RE_DICE = re.compile(r"^\s*(\d*)d(\d+)\s*(?:([+-])\s*(\d+))?\s*$", re.IGNORECASE)


class RollError(Exception):
    """A roll could not be made as asked."""


def setting_seed(root: Path | None = None) -> int:
    """The setting seed, from the ledger first and ``setting.md`` second."""
    root = root or common.REPO_ROOT
    led = ledger_mod.load(root)
    if led.seed is not None:
        return led.seed
    setting_file = root / common.SETTING_DIR / "setting.md"
    if setting_file.exists():
        doc = common.read_doc(setting_file, "setting")
        if doc.fm.get("seed") is not None:
            return int(doc.fm["seed"])
    raise RollError(
        "no seed found. Run `python tools/ledger.py init --seed N` first."
    )


def stream(seed: int, target: str = "", nonce: str = "") -> random.Random:
    """A deterministic generator for one seed, target and nonce."""
    digest = hashlib.sha256(f"{seed}:{target}:{nonce}".encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest, "big"))


def parse_dice(notation: str) -> tuple[int, int, int]:
    match = RE_DICE.match(notation)
    if not match:
        raise RollError(f"{notation!r} is not dice notation such as 2d6+1")
    count = int(match.group(1) or 1)
    faces = int(match.group(2))
    modifier = int(match.group(4) or 0)
    if match.group(3) == "-":
        modifier = -modifier
    if count < 1 or faces < 2:
        raise RollError(f"{notation!r} asks for an impossible die")
    return count, faces, modifier


def roll_dice(notation: str, rng: random.Random) -> dict[str, Any]:
    count, faces, modifier = parse_dice(notation)
    rolls = [rng.randint(1, faces) for _ in range(count)]
    return {
        "notation": notation,
        "rolls": rolls,
        "modifier": modifier,
        "total": sum(rolls) + modifier,
    }


def _weights(rows: list[dict[str, str]], column: str | None) -> list[float]:
    if column is None:
        return [1.0] * len(rows)
    weights: list[float] = []
    for index, row in enumerate(rows):
        raw = row.get(column, "").strip()
        try:
            weight = float(raw)
        except ValueError as exc:
            raise RollError(
                f"row {index + 1} has a non-numeric {column!r} of {raw!r}"
            ) from exc
        if weight < 0:
            raise RollError(f"row {index + 1} has a negative {column!r}")
        weights.append(weight)
    if sum(weights) <= 0:
        raise RollError(f"every {column!r} is zero, so nothing can be drawn")
    return weights


def roll_table(
    rows: list[dict[str, str]],
    rng: random.Random,
    count: int = 1,
    weight_column: str | None = None,
    unique: bool = False,
) -> list[dict[str, str]]:
    if not rows:
        raise RollError("the table has no rows")
    if unique and count > len(rows):
        raise RollError(f"asked for {count} unique rows from a table of {len(rows)}")

    pool = list(rows)
    weights = _weights(pool, weight_column)
    drawn: list[dict[str, str]] = []
    for _ in range(count):
        pick = rng.choices(range(len(pool)), weights=weights, k=1)[0]
        drawn.append(pool[pick])
        if unique:
            pool.pop(pick)
            weights.pop(pick)
    return drawn


def _resolve_table(root: Path, reference: str) -> tuple[Path, list[dict[str, str]]]:
    """Accept either a path or a table code such as ``T-RUM``."""
    path = Path(reference)
    if not path.is_absolute():
        candidate = root / reference
        if candidate.exists():
            path = candidate
    if not path.exists():
        matches = sorted((root / common.TABLES_DIR).glob(f"{reference}-*.md"))
        if not matches:
            raise RollError(f"no table found for {reference!r}")
        path = matches[0]
    doc = common.read_doc(path, "table")
    tables = doc.tables()
    if not tables:
        raise RollError(f"{path} carries no markdown table")
    return path, tables[0].rows


def main(argv: list[str] | None = None) -> int:
    # Shared options hang off each subcommand rather than the root parser, so
    # that `roll.py dice 2d6 --target R03` reads the way it is written.
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--root", type=Path, default=common.REPO_ROOT)
    shared.add_argument("--seed", type=int, help="override the setting seed")
    shared.add_argument("--target", default="", help="the code the roll belongs to")
    shared.add_argument("--nonce", default="", help="distinguish two rolls for one target")
    shared.add_argument("--json", action="store_true")

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p_dice = sub.add_parser("dice", parents=[shared], help="roll dice notation such as 2d6+1")
    p_dice.add_argument("notation")
    p_dice.add_argument("--times", type=int, default=1)

    p_table = sub.add_parser("table", parents=[shared], help="draw rows from a table")
    p_table.add_argument("table", help="a table code such as T-RUM, or a path")
    p_table.add_argument("--count", type=int, default=1)
    p_table.add_argument("--weight-column", default=None)
    p_table.add_argument("--unique", action="store_true")

    p_choose = sub.add_parser("choose", parents=[shared],
                              help="draw from options given on the command line")
    p_choose.add_argument("options", nargs="+")
    p_choose.add_argument("--count", type=int, default=1)
    p_choose.add_argument("--unique", action="store_true")

    args = parser.parse_args(argv)
    root = args.root.resolve()

    try:
        seed = args.seed if args.seed is not None else setting_seed(root)
        rng = stream(seed, args.target, args.nonce)

        if args.command == "dice":
            results = [roll_dice(args.notation, rng) for _ in range(max(1, args.times))]
            payload: dict[str, Any] = {
                "seed": seed,
                "target": args.target,
                "nonce": args.nonce,
                "results": results,
            }
            if args.json:
                print(json.dumps(payload, indent=2))
            else:
                for result in results:
                    detail = "+".join(str(value) for value in result["rolls"])
                    mod = f" {result['modifier']:+d}" if result["modifier"] else ""
                    print(f"{result['total']}  ({detail}{mod})")
            return 0

        if args.command == "table":
            path, rows = _resolve_table(root, args.table)
            drawn = roll_table(rows, rng, args.count, args.weight_column, args.unique)
            if args.json:
                print(json.dumps({"seed": seed, "table": str(path), "rows": drawn}, indent=2))
            else:
                for row in drawn:
                    first = row.get("ID") or next(iter(row.values()), "")
                    rest = " | ".join(
                        value for key, value in row.items() if key != "ID" and value
                    )
                    print(f"{first}  {rest}".strip())
            return 0

        if args.command == "choose":
            rows = [{"option": option} for option in args.options]
            drawn = roll_table(rows, rng, args.count, None, args.unique)
            if args.json:
                print(json.dumps({"seed": seed, "picks": [r["option"] for r in drawn]}, indent=2))
            else:
                for row in drawn:
                    print(row["option"])
            return 0

    except (RollError, common.DocError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
