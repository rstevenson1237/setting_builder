"""Test helpers: a throwaway copy of the repository, and one tool run against it.

Every test that breaks something works on a copy under `/tmp`, never on the
repository itself. A test that mutates content states the exact text it is
replacing, so a content edit that invalidates a test fails loudly with the
missing anchor rather than quietly passing against nothing.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

# Paths inside the content tree, named once so a rename breaks one line.
SETTING = "setting/setting.md"
SETTING_CONN = "setting/connections.md"
REGION = "setting/regions/R03-ashen-fen/region.md"
REGION_CONN = "setting/regions/R03-ashen-fen/connections.md"
L03 = "setting/regions/R03-ashen-fen/locations/R03-L03-bell-causeway.md"
L07 = "setting/regions/R03-ashen-fen/locations/R03-L07-drowned-shrine.md"
T_KEY = "setting/tables/T-KEY-keys.md"
DIAGRAM = "build/diagrams/T3_R03.md"
PLAYBOOK = "build/playbook.md"
LEDGER = "state/ledger.json"
GENRE = "patterns/GENRE.md"
ROUTER = "DESIGN_PATTERNS.md"


class Sandbox:
    """A temporary copy of the repository that a test may break freely.

    Use as a context manager. `without` omits top-level entries from the copy,
    which is how a test starts from an empty content tree.
    """

    def __init__(self, without: Iterable[str] = ()) -> None:
        self._ignore = shutil.ignore_patterns(".git", "__pycache__", *without)
        self._tmp: tempfile.TemporaryDirectory[str] | None = None
        self.root = Path()

    def __enter__(self) -> "Sandbox":
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "repo"
        shutil.copytree(REPO, self.root, ignore=self._ignore)
        return self

    def __exit__(self, *exc: object) -> None:
        if self._tmp is not None:
            self._tmp.cleanup()

    # -- files ------------------------------------------------------------

    def path(self, relative: str) -> Path:
        return self.root / relative

    def read(self, relative: str) -> str:
        return self.path(relative).read_text(encoding="utf-8")

    def write(self, relative: str, text: str) -> Path:
        """Write a file into the copy, creating its parents."""
        path = self.path(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def sub(self, relative: str, old: str, new: str, count: int = 1) -> None:
        """Replace exact text, asserting the anchor is present."""
        text = self.read(relative)
        if old not in text:
            raise AssertionError(f"anchor not found in {relative}: {old!r}")
        self.path(relative).write_text(text.replace(old, new, count), encoding="utf-8")

    def rename(self, relative: str, new_name: str) -> None:
        target = self.path(relative)
        target.rename(target.parent / new_name)

    # -- ledger -----------------------------------------------------------

    def complete_steps(self, *steps: int) -> None:
        """Mark steps complete, so a gated check reaches its full severity."""
        path = self.path(LEDGER)
        data = json.loads(path.read_text(encoding="utf-8"))
        for step in steps:
            data["steps"][str(step)] = {"status": "complete", "targets": 0}
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def mark(self, key: str, *codes: str) -> None:
        """Add codes to the ledger's `built` or `decorated` list."""
        path = self.path(LEDGER)
        data = json.loads(path.read_text(encoding="utf-8"))
        data[key] = sorted(set(data.get(key, [])) | set(codes))
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    # -- tools ------------------------------------------------------------

    def run(self, script: str, *args: str) -> subprocess.CompletedProcess[str]:
        """Run a tool against this copy. `--root` goes last, which every CLI accepts."""
        return subprocess.run(
            [sys.executable, str(self.root / "tools" / script), *args,
             "--root", str(self.root)],
            capture_output=True,
            text=True,
        )

    def validate(self, *args: str) -> dict[str, Any]:
        result = self.run("validate.py", "--json", *args)
        if not result.stdout.strip():
            raise AssertionError(f"validate.py produced no output: {result.stderr}")
        return json.loads(result.stdout)

    def findings(self, check: str, *args: str) -> list[dict[str, str]]:
        return [f for f in self.validate(*args)["findings"] if f["check"] == check]
