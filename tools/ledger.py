#!/usr/bin/env python3
"""Read and write ``state/ledger.json`` and regenerate ``STATE.md``.

``state/ledger.json`` is canonical. ``STATE.md`` is a generated human view of
it and holds nothing else. Every mutation here rewrites both.

The ledger carries two guards. ``built`` is the overwrite guard of SPEC.md
section 8.1: the Architect refuses any target listed there. ``decorated``
records the targets a Decorator has closed, which is what M25 needs in order
to know whether a surviving ``[[ ... ]]`` note is late or merely early.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402

STEPS: dict[int, tuple[str, str]] = {
    1: ("Setting headers", "Architect"),
    2: ("Setting connections", "Engineer"),
    3: ("Setting fields", "Builder"),
    4: ("Setting prose", "Decorator"),
    5: ("Region headers", "Architect"),
    6: ("Region connections", "Engineer"),
    7: ("Region fields", "Builder"),
    8: ("Region prose", "Decorator"),
    9: ("Location headers", "Architect"),
    10: ("Location connections", "Engineer"),
    11: ("Location fields", "Builder"),
    12: ("Location prose", "Decorator"),
}

PASSES = ["HIGH", "MEDIUM", "LOW"]


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Ledger:
    """The progress record. Construct through :func:`load`."""

    def __init__(self, root: Path, data: dict[str, Any]) -> None:
        self.root = root
        self.data = data

    # -- reading ----------------------------------------------------------

    @property
    def path(self) -> Path:
        return self.root / common.LEDGER_PATH

    @property
    def seed(self) -> int | None:
        seed = self.data.get("seed")
        return int(seed) if seed is not None else None

    @property
    def current_step(self) -> int:
        return int(self.data.get("current_step", 0))

    @property
    def current_pass(self) -> str | None:
        return self.data.get("current_pass")

    def step(self, number: int) -> dict[str, Any]:
        return self.data.setdefault("steps", {}).setdefault(str(number), {})

    def status(self, number: int) -> str:
        return str(self.data.get("steps", {}).get(str(number), {}).get("status", "pending"))

    def is_complete(self, number: int) -> bool:
        return self.status(number) == "complete"

    def is_built(self, code: str) -> bool:
        return code in self.data.get("built", [])

    def is_decorated(self, code: str) -> bool:
        return code in self.data.get("decorated", [])

    # -- writing ----------------------------------------------------------

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.data, indent=2, sort_keys=False) + "\n", encoding="utf-8"
        )
        write_state(self)

    def _append(self, key: str, codes: list[str]) -> list[str]:
        listing = self.data.setdefault(key, [])
        added = [code for code in codes if code not in listing]
        listing.extend(added)
        listing.sort()
        return added


def empty(seed: int | None = None) -> dict[str, Any]:
    return {
        "schema_version": common.SCHEMA_VERSION,
        "seed": seed,
        "current_step": 0,
        "current_pass": None,
        "steps": {},
        "built": [],
        "decorated": [],
    }


def load(root: Path | None = None) -> Ledger:
    root = root or common.REPO_ROOT
    path = root / common.LEDGER_PATH
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = empty()
    for key, default in empty().items():
        data.setdefault(key, default)
    return Ledger(root, data)


# --------------------------------------------------------------------------
# STATE.md
# --------------------------------------------------------------------------


def write_state(ledger: Ledger) -> Path:
    data = ledger.data
    lines = [
        "# State",
        "",
        "Generated from `state/ledger.json` by `tools/ledger.py`. Do not edit by hand.",
        "",
        f"- **Seed:** {data.get('seed') if data.get('seed') is not None else 'not set'}",
        f"- **Current step:** {data.get('current_step') or 'not started'}",
    ]
    if data.get("current_pass"):
        lines.append(f"- **Current pass:** {data['current_pass']}")
    lines += [
        f"- **Built targets:** {len(data.get('built', []))}",
        f"- **Decorated targets:** {len(data.get('decorated', []))}",
        "",
        "## Steps",
        "",
        "| Step | Name | Phase | Status | Done | Pending | Completed |",
        "| ---: | :--- | :--- | :--- | ---: | ---: | :--- |",
    ]
    for number, (name, phase) in STEPS.items():
        entry = data.get("steps", {}).get(str(number), {})
        status = entry.get("status", "pending")
        done = entry.get("done", [])
        pending = entry.get("pending", [])
        count = entry.get("targets")
        done_cell = str(count) if status == "complete" and count is not None else str(len(done))
        lines.append(
            f"| {number} | {name} | {phase} | {status} | {done_cell} | "
            f"{len(pending)} | {entry.get('completed_at', '')} |"
        )

    step = data.get("steps", {}).get(str(data.get("current_step")), {})
    pending = step.get("pending", [])
    if pending:
        lines += ["", "## Pending in the current step", ""]
        lines += [f"- `{code}`" for code in pending]

    path = ledger.root / common.STATE_PATH
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    # `--root` hangs off each subcommand rather than the root parser, so every
    # tool in this directory takes its options in the same place.
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--root", type=Path, default=common.REPO_ROOT)

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", parents=[shared], help="create a ledger")
    p_init.add_argument("--seed", type=int, required=True)
    p_init.add_argument("--force", action="store_true")

    sub.add_parser("show", parents=[shared], help="print the ledger as JSON")
    sub.add_parser("state", parents=[shared], help="regenerate STATE.md from the ledger")
    sub.add_parser("seed", parents=[shared], help="print the setting seed")

    p_start = sub.add_parser("start", parents=[shared], help="open a step")
    p_start.add_argument("step", type=int)
    p_start.add_argument("--targets", nargs="*", default=[])
    p_start.add_argument("--pass", dest="pass_name", choices=PASSES)

    p_done = sub.add_parser("done", parents=[shared], help="record one or more finished targets")
    p_done.add_argument("step", type=int)
    p_done.add_argument("targets", nargs="+")

    p_complete = sub.add_parser("complete", parents=[shared], help="close a step")
    p_complete.add_argument("step", type=int)

    p_pass = sub.add_parser("pass", parents=[shared], help="set the current pass of step 11")
    p_pass.add_argument("name", choices=PASSES)

    p_built = sub.add_parser("built", parents=[shared], help="mark targets as Builder-touched")
    p_built.add_argument("targets", nargs="+")

    p_dec = sub.add_parser("decorated", parents=[shared], help="mark targets as Decorator-closed")
    p_dec.add_argument("targets", nargs="+")

    p_pending = sub.add_parser("pending", parents=[shared], help="print the pending targets of a step")
    p_pending.add_argument("step", type=int)

    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.command == "init":
        path = root / common.LEDGER_PATH
        if path.exists() and not args.force:
            print(f"{path} already exists. Pass --force to overwrite.", file=sys.stderr)
            return 1
        ledger = Ledger(root, empty(args.seed))
        ledger.save()
        print(f"wrote {path} with seed {args.seed}")
        return 0

    ledger = load(root)

    if args.command == "show":
        print(json.dumps(ledger.data, indent=2))
        return 0

    if args.command == "seed":
        if ledger.seed is None:
            print("seed is not set", file=sys.stderr)
            return 1
        print(ledger.seed)
        return 0

    if args.command == "state":
        print(f"wrote {write_state(ledger)}")
        return 0

    if args.command == "pending":
        for code in ledger.step(args.step).get("pending", []):
            print(code)
        return 0

    if args.command == "start":
        if args.step not in STEPS:
            print(f"step {args.step} is not one of 1 to 12", file=sys.stderr)
            return 1
        entry = ledger.step(args.step)
        entry["status"] = "in_progress"
        entry.setdefault("done", [])
        if args.targets:
            entry["pending"] = [t for t in args.targets if t not in entry["done"]]
        entry.setdefault("pending", [])
        entry["started_at"] = now()
        ledger.data["current_step"] = args.step
        if args.pass_name:
            ledger.data["current_pass"] = args.pass_name
        ledger.save()
        print(f"step {args.step} in_progress, {len(entry['pending'])} pending")
        return 0

    if args.command == "done":
        entry = ledger.step(args.step)
        done = entry.setdefault("done", [])
        pending = entry.setdefault("pending", [])
        for target in args.targets:
            if target not in done:
                done.append(target)
            if target in pending:
                pending.remove(target)
        entry.setdefault("status", "in_progress")
        ledger.save()
        print(f"step {args.step}: {len(done)} done, {len(pending)} pending")
        return 0

    if args.command == "complete":
        entry = ledger.step(args.step)
        pending = entry.get("pending", [])
        if pending:
            print(
                f"step {args.step} still has {len(pending)} pending targets: "
                + ", ".join(pending),
                file=sys.stderr,
            )
            return 1
        entry["status"] = "complete"
        entry["targets"] = len(entry.get("done", []))
        entry["completed_at"] = now()
        entry.pop("pending", None)
        ledger.data["current_step"] = args.step
        if args.step != 11:
            ledger.data["current_pass"] = None
        ledger.save()
        print(f"step {args.step} complete, {entry['targets']} targets")
        return 0

    if args.command == "pass":
        ledger.data["current_pass"] = args.name
        ledger.save()
        print(f"current pass is {args.name}")
        return 0

    if args.command in {"built", "decorated"}:
        added = ledger._append(args.command, args.targets)
        ledger.save()
        print(f"{args.command}: added {len(added)}, total {len(ledger.data[args.command])}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
