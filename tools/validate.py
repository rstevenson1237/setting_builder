#!/usr/bin/env python3
"""Run the mechanical checks of SPEC.md section 14.1 with severity handling.

`ERROR` fails the run. `REPORT` prints and continues. `--final` promotes every
`REPORT` to `ERROR`, and is step 12's acceptance test.

Some checks cannot be true until the step that writes their input has run. A
region does not hold its full location count before step 9, and no table is
cited before step 10. Those checks carry a gate: while the ledger shows the
prerequisite step incomplete, the finding is downgraded to `REPORT` and
labelled `deferred`. `--final` ignores every gate, so the acceptance test is
the full set at full severity.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build as build_mod  # noqa: E402
import common  # noqa: E402
import ledger as ledger_mod  # noqa: E402

CHECKS: dict[str, str] = {
    "M1": "Code uniqueness across the corpus",
    "M2": "Filename prefix matches the frontmatter code",
    "M3": "Exactly three tags on every Setting, Region and Location",
    "M4": "Required frontmatter keys present and correctly typed",
    "M5": "Location cell prefix matches its region's type",
    "M6": "Region location count and HIGH minimum",
    "M7": "Every exit target resolves to a real location",
    "M8": "Every exit has a reverse exit unless typed one-way",
    "M9": "No orphan locations",
    "M10": "Every region and location belongs to exactly one container",
    "M11": "Derived diagrams match what mermaid_gen.py re-derives",
    "M12": "Typed edges appear at tier 4 only",
    "M13": "Every splice marker resolves, and no mermaid outside build/diagrams",
    "M14": "No location sources entry begins with S-",
    "M15": "Every T table is cited by at least one location",
    "M16": "Every sources ID and every (SECTION, key) token resolves",
    "M17": "Every bolded noun in a Player Overview has a matching feature",
    "M18": "Every proper name decomposes into roots recorded in T-LNG",
    "M19": "Region table matches region type, six rows, Dangers descend",
    "M20": "Every T-KEY row names a key location and a gate location",
    "M21": "Every mechanical token matches the vocabulary in MECHANICS.md",
    "M22": "Required fields are present, with None and a reason allowed",
    "M23": "-> appears only inside a feature connection pointer",
    "M24": "No bare mechanical value in prose, no token in player-facing text",
    "M25": "No architect note survives in a file the Decorator has closed",
}

REPORT_CHECKS = {"M24", "M25"}

# The scan for hand-authored mermaid is limited to the content tree and the
# build output. SPEC.md, CLAUDE.md and the pattern library are documentation
# and may illustrate freely.
MERMAID_SCAN_DIRS = ("setting", "build")

# Three paths inside that scan hold derived mermaid rather than authored
# mermaid. `build/diagrams/` is where every diagram is written, a bundle in
# `build/bundles/` carries a copy of one it resolved, and `build/playbook.md` is
# what `build.py` produces by splicing the markers. None is hand-edited, and the
# thing M13 exists to catch is a diagram somebody drew by hand in a host file.
MERMAID_SKIP_DIRS = (common.DIAGRAMS_DIR, common.BUNDLES_DIR)
MERMAID_SKIP_FILES = (build_mod.PLAYBOOK_PATH,)

RE_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
RE_EDGE_LABEL = re.compile(r"(-->\s*\|[^|]+\||--\s*[^->\n]+\s*-->)")


@dataclass
class Finding:
    check: str
    code: str
    message: str
    fix: str = ""
    severity: str = "ERROR"
    deferred: str = ""

    def as_dict(self) -> dict[str, str]:
        return {
            "check": self.check,
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "fix": self.fix,
            "deferred": self.deferred,
        }


@dataclass
class Gate:
    """A prerequisite that must be met before a check can be true."""

    kind: str  # step | diagrams | mermaid_gen
    value: Any
    why: str


class Validator:
    def __init__(self, root: Path, final: bool = False, only: set[str] | None = None) -> None:
        self.root = root
        self.final = final
        self.only = only
        self.findings: list[Finding] = []
        self.notes: list[str] = []
        self.corpus = common.load_corpus(root)
        self.weights = common.load_weights(root)
        self.ledger = ledger_mod.load(root)
        self.tokens, self.bare_patterns = self._load_mechanics()

    # -- plumbing ---------------------------------------------------------

    def enabled(self, check: str) -> bool:
        return self.only is None or check in self.only

    def add(
        self,
        check: str,
        code: str,
        message: str,
        fix: str = "",
        gate: Gate | None = None,
    ) -> None:
        severity = "REPORT" if check in REPORT_CHECKS else "ERROR"
        deferred = ""
        if gate is not None and not self.final and not self._gate_open(gate):
            severity = "REPORT"
            deferred = gate.why
        if self.final:
            severity = "ERROR"
        self.findings.append(
            Finding(check=check, code=code, message=message, fix=fix,
                    severity=severity, deferred=deferred)
        )

    def _gate_open(self, gate: Gate) -> bool:
        if gate.kind == "step":
            return self.ledger.is_complete(int(gate.value))
        if gate.kind == "diagrams":
            directory = self.root / common.DIAGRAMS_DIR
            return directory.is_dir() and any(directory.glob("*.md"))
        if gate.kind == "mermaid_gen":
            return (self.root / "tools" / "mermaid_gen.py").exists()
        return True

    def _load_mechanics(self) -> tuple[dict[str, tuple[str, list[str]]], list[tuple[re.Pattern[str], str]]]:
        path = self.root / common.MECHANICS_PATH
        if not path.exists():
            self.notes.append(f"{common.MECHANICS_PATH} is missing, so M21 and M24 cannot run")
            return {}, []
        tables = common.parse_tables(path.read_text(encoding="utf-8"))
        tokens: dict[str, tuple[str, list[str]]] = {}
        bare: list[tuple[re.Pattern[str], str]] = []
        for table in tables:
            if {"Token", "Form", "Values"} <= set(table.headers):
                for row in table.rows:
                    name = row["Token"].strip().strip("`")
                    form = row["Form"].strip()
                    values = [v.strip() for v in row["Values"].split(",") if v.strip()]
                    if name:
                        tokens[name] = (form, values)
            elif {"Pattern", "Catches"} <= set(table.headers):
                for row in table.rows:
                    pattern = row["Pattern"].strip().strip("`")
                    if not pattern:
                        continue
                    try:
                        bare.append((re.compile(pattern), row.get("Catches", "")))
                    except re.error as exc:
                        self.notes.append(f"MECHANICS.md pattern {pattern!r} is invalid: {exc}")
        return tokens, bare

    # -- corpus helpers ---------------------------------------------------

    def content_docs(self) -> list[common.Doc]:
        docs: list[common.Doc] = []
        if self.corpus.setting:
            docs.append(self.corpus.setting)
        docs += list(self.corpus.tables.values())
        docs += list(self.corpus.regions.values())
        docs += list(self.corpus.locations.values())
        return docs

    def doc_code(self, doc: common.Doc) -> str:
        if doc.scale == "setting":
            return "setting"
        return doc.code or doc.path.stem

    def region_of(self, location: common.Doc) -> common.Doc | None:
        return self.corpus.regions.get(str(location.fm.get("region", "")))

    def all_edges(self) -> list[tuple[str, common.Edge]]:
        edges: list[tuple[str, common.Edge]] = []
        for code, doc in self.corpus.region_connections.items():
            for edge in common.edges_from(doc):
                edges.append((code, edge))
        return edges

    def exits_of(self, doc: common.Doc) -> list[dict[str, str]]:
        section = doc.section("Exits")
        if section is None:
            return []
        for table in common.parse_tables(section.full_text):
            lowered = {common.normalise_key(h): h for h in table.headers}
            if "to" in lowered:
                return [
                    {
                        "to": row.get(lowered["to"], "").strip(),
                        "type": row.get(lowered.get("type", ""), "").strip(),
                        "cue": row.get(lowered.get("cue", ""), "").strip(),
                    }
                    for row in table.rows
                    if row.get(lowered["to"], "").strip()
                ]
        return []

    # ------------------------------------------------------------------
    # Checks
    # ------------------------------------------------------------------

    def run(self) -> None:
        for path, message in self.corpus.read_errors:
            rel = path.relative_to(self.root) if path.is_relative_to(self.root) else path
            self.add("M4", str(rel), f"file could not be read: {message}",
                     "Restore the YAML frontmatter block.")
        for name in sorted(CHECKS, key=lambda key: int(key[1:])):
            if not self.enabled(name):
                continue
            getattr(self, f"check_{name.lower()}")()

    # M1 ----------------------------------------------------------------
    def check_m1(self) -> None:
        seen: dict[str, list[str]] = {}
        for doc in self.corpus.docs:
            if doc.scale not in {"table", "region", "location"}:
                continue
            code = doc.code
            if code:
                seen.setdefault(code, []).append(doc.relpath)
        for code, paths in sorted(seen.items()):
            if len(paths) > 1:
                self.add("M1", code, f"code is claimed by {len(paths)} files: " + ", ".join(paths),
                         "A code is a primary key and never changes. Renumber one file.")

        entries: dict[str, list[str]] = {}
        for table_code, doc in self.corpus.tables.items():
            for row in self.corpus.table_rows(table_code):
                entry = row.get("ID", "").strip()
                if entry:
                    entries.setdefault(entry, []).append(doc.relpath)
        for entry, paths in sorted(entries.items()):
            if len(paths) > 1:
                self.add("M1", entry, f"entry ID appears {len(paths)} times: " + ", ".join(paths),
                         "Renumber the duplicate row.")

        if self.corpus.setting:
            self._duplicate_containers("setting", self.corpus.setting)
        for code, doc in sorted(self.corpus.regions.items()):
            self._duplicate_containers(code, doc)

    def _duplicate_containers(self, code: str, doc: common.Doc) -> None:
        seen: set[str] = set()
        for entry in doc.fm.get("containers", []) or []:
            if not isinstance(entry, dict):
                continue
            ident = str(entry.get("id", ""))
            if ident in seen:
                self.add("M1", code, f"container id {ident!r} is declared twice",
                         "Container ids are unique within their level.")
            seen.add(ident)

    # M2 ----------------------------------------------------------------
    def check_m2(self) -> None:
        for code, doc in sorted(self.corpus.tables.items()):
            self._filename(doc, code, doc.path.stem)
        for code, doc in sorted(self.corpus.regions.items()):
            self._filename(doc, code, doc.path.parent.name, "the region directory")
        for code, doc in sorted(self.corpus.locations.items()):
            self._filename(doc, code, doc.path.stem)

    def _filename(self, doc: common.Doc, code: str, stem: str, what: str = "the filename") -> None:
        if not code:
            self.add("M2", doc.relpath, "frontmatter carries no code",
                     "Add a `code:` key matching the filename prefix.")
            return
        if not stem.startswith(f"{code}-"):
            self.add("M2", code, f"{what} {stem!r} does not open with the code {code!r}",
                     f"Rename to {code}-<slug>.")
            return
        expected = common.slugify(str(doc.fm.get("name", "")))
        actual = stem[len(code) + 1 :]
        if expected and actual != expected:
            self.add("M2", code, f"{what} slug is {actual!r} but the name slugs to {expected!r}",
                     f"Rename to {code}-{expected}.")

    # M3 ----------------------------------------------------------------
    def check_m3(self) -> None:
        want = int(self.weights["tags"]["count"])
        targets: list[tuple[str, common.Doc]] = []
        if self.corpus.setting:
            targets.append(("setting", self.corpus.setting))
        targets += sorted(self.corpus.regions.items())
        targets += sorted(self.corpus.locations.items())
        for code, doc in targets:
            tags = doc.fm.get("tags")
            if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
                self.add("M3", code, "tags is not a list of strings",
                         f"Write exactly {want} thematic tags.")
                continue
            if len(tags) != want:
                self.add("M3", code, f"carries {len(tags)} tags, not {want}",
                         f"Write exactly {want} thematic tags.")

    # M4 ----------------------------------------------------------------
    def check_m4(self) -> None:
        weights = self.weights
        if self.corpus.setting:
            self._typed(
                "setting",
                self.corpus.setting,
                {"name": str, "tags": list, "seed": int, "containers": list,
                 "schema_version": int},
            )
            self._containers_shape("setting", self.corpus.setting)

        for code, doc in sorted(self.corpus.regions.items()):
            self._typed(
                code, doc,
                {"code": str, "name": str, "tags": list, "type": str, "difficulty": str,
                 "weight": str, "container": str, "containers": list, "sources": list,
                 "schema_version": int},
            )
            self._enum(code, doc, "type", weights["region_types"])
            self._enum(code, doc, "difficulty", weights["difficulty"]["dice"])
            self._enum(code, doc, "weight", sorted(weights["region_weights"]))
            self._containers_shape(code, doc)
            if not common.RE_REGION_CODE.match(code):
                self.add("M4", code, "code is not in R## form", "Renumber as R01, R02 and so on.")

        for code, doc in sorted(self.corpus.locations.items()):
            self._typed(
                code, doc,
                {"code": str, "name": str, "tags": list, "region": str, "container": str,
                 "cell": str, "sources": list, "schema_version": int},
            )
            if not common.RE_LOCATION_CODE.match(code):
                self.add("M4", code, "code is not in R##-L## form", "Renumber the location.")

        for code, doc in sorted(self.corpus.tables.items()):
            kind = str(doc.fm.get("kind", ""))
            self._typed(code, doc, {"code": str, "name": str, "kind": str, "schema_version": int})
            if kind not in {"S", "T"}:
                self.add("M4", code, f"kind is {kind!r}, not S or T", "Set kind to S or T.")
                continue
            if kind == "S":
                if code not in common.S_TABLES:
                    self.add("M4", code, "is not in the S table catalogue",
                             "SPEC.md section 4.7 lists the four S tables.")
                if doc.fm.get("draws_on"):
                    self.add("M4", code, "an S table may not draw on another table",
                             "Remove draws_on. S tables are the root.")
            else:
                if code not in common.T_TABLES:
                    self.add("M4", code, "is not in the T table catalogue",
                             "SPEC.md section 4.7 lists the twenty T tables.")
                    continue
                expected = code in common.DECORATED_TABLES
                if bool(doc.fm.get("decorate", False)) != expected:
                    self.add("M4", code,
                             f"decorate is {doc.fm.get('decorate')!r} but the catalogue says {expected}",
                             "Artifact tables carry decorate: true, parameter tables false.")

    def _typed(self, code: str, doc: common.Doc, schema: dict[str, type]) -> None:
        for key, kind in schema.items():
            if key not in doc.fm:
                self.add("M4", code, f"frontmatter is missing {key!r}", f"Add {key}.")
                continue
            value = doc.fm[key]
            if kind is int and isinstance(value, bool):
                self.add("M4", code, f"{key!r} is a boolean, expected an integer", f"Set {key} to a number.")
                continue
            if not isinstance(value, kind):
                self.add("M4", code, f"{key!r} is {type(value).__name__}, expected {kind.__name__}",
                         f"Correct the type of {key}.")
        if "schema_version" in doc.fm and doc.fm["schema_version"] != common.SCHEMA_VERSION:
            self.add("M4", code, f"schema_version is {doc.fm['schema_version']}, expected {common.SCHEMA_VERSION}",
                     "Migrate the file or correct the version.")

    def _enum(self, code: str, doc: common.Doc, key: str, allowed: Iterable[Any]) -> None:
        allowed = list(allowed)
        value = doc.fm.get(key)
        if value is not None and value not in allowed:
            self.add("M4", code, f"{key} is {value!r}, not one of {allowed}",
                     f"Set {key} to one of {allowed}.")

    def _containers_shape(self, code: str, doc: common.Doc) -> None:
        for entry in doc.fm.get("containers", []) or []:
            if not isinstance(entry, dict) or "id" not in entry or "name" not in entry:
                self.add("M4", code, f"container entry {entry!r} is not an id and name pair",
                         "Each container is `- id: slug` with a `name:`.")
                continue
            if not common.RE_SLUG.match(str(entry["id"])):
                self.add("M4", code, f"container id {entry['id']!r} is not a lowercase slug",
                         "Container ids are lowercase and hyphenated.")

    # M5 ----------------------------------------------------------------
    def check_m5(self) -> None:
        allowed = self.weights["location_weights"]
        for code, doc in sorted(self.corpus.locations.items()):
            cell = str(doc.fm.get("cell", ""))
            region = self.region_of(doc)
            if "_" not in cell:
                self.add("M5", code, f"cell {cell!r} is not TYPE_WEIGHT",
                         "Write the cell as SAFE_LOW, WILD_HIGH and so on.")
                continue
            prefix, _, suffix = cell.partition("_")
            if suffix not in allowed:
                self.add("M5", code, f"cell weight {suffix!r} is not one of {allowed}",
                         f"Use one of {allowed}.")
            if region is None:
                self.add("M5", code, f"region {doc.fm.get('region')!r} does not exist",
                         "Point the location at a real region.")
                continue
            region_type = str(region.fm.get("type", ""))
            if prefix != region_type:
                self.add("M5", code, f"cell says {prefix} but region {region.code} is {region_type}",
                         f"Set cell to {region_type}_{suffix or 'WEIGHT'}, or move the location.")

    # M6 ----------------------------------------------------------------
    def check_m6(self) -> None:
        gate = Gate("step", 9, "step 9 has not closed, so the region is not fully populated")
        bands = self.weights["region_weights"]
        for code, doc in sorted(self.corpus.regions.items()):
            weight = str(doc.fm.get("weight", ""))
            band = bands.get(weight)
            if band is None:
                continue
            locations = self.corpus.locations_in(code)
            count = len(locations)
            if not band["locations_min"] <= count <= band["locations_max"]:
                self.add("M6", code,
                         f"carries {count} locations, and weight {weight} bands at "
                         f"{band['locations_min']} to {band['locations_max']}",
                         "Adjust the location count, or change the region weight.", gate)
            high = sum(1 for loc in locations if str(loc.fm.get("cell", "")).endswith("_HIGH"))
            if high < band["high_min"]:
                self.add("M6", code,
                         f"carries {high} HIGH locations, and weight {weight} needs "
                         f"{band['high_min']}",
                         "Promote a location to HIGH, or add a landmark.", gate)

    # M7 ----------------------------------------------------------------
    def check_m7(self) -> None:
        known = set(self.corpus.locations)
        for region_code, edge in self.all_edges():
            for end in (edge.source, edge.target):
                if end not in known:
                    self.add("M7", region_code,
                             f"{edge.origin} names {end!r}, which is not a location",
                             "Correct the code, or scaffold the location.")

        directed = self._directed_edges()
        for code, doc in sorted(self.corpus.locations.items()):
            for exit_row in self.exits_of(doc):
                target = exit_row["to"]
                if target not in known:
                    self.add("M7", code, f"exit to {target!r} does not resolve to a location",
                             "Correct the code, or scaffold the location.")
                    continue
                if (code, target) not in directed:
                    self.add("M7", code,
                             f"exit to {target} has no row in the region connections table",
                             "The connections table is the source of truth. Add the edge there.")

        # The setting's edges are written at step 2 and the regions they name are
        # stubbed at step 5, so this branch cannot be true in between.
        region_gate = Gate("step", 5, "regions are stubbed at step 5")
        setting_edges = common.edges_from(self.corpus.setting_connections)
        for edge in setting_edges:
            for end in (edge.source, edge.target):
                if end not in self.corpus.regions:
                    self.add("M7", "setting", f"setting connections name {end!r}, which is not a region",
                             "Correct the code, or scaffold the region.", region_gate)

        for code, doc in sorted(self.corpus.locations.items()):
            body = RE_HTML_COMMENT.sub("", doc.body)
            for target in common.RE_POINTER.findall(body):
                if target not in known:
                    self.add("M7", code, f"pointer -> {target} does not resolve to a location",
                             "A pointer names the location the feature leads to.")

    def _directed_edges(self) -> set[tuple[str, str]]:
        directed: set[tuple[str, str]] = set()
        for _, edge in self.all_edges():
            directed.add((edge.source, edge.target))
            if not edge.one_way:
                directed.add((edge.target, edge.source))
        return directed

    # M8 ----------------------------------------------------------------
    def check_m8(self) -> None:
        gate = Gate("step", 10, "exits are written at step 10")
        listed: set[tuple[str, str]] = set()
        for code, doc in self.corpus.locations.items():
            for exit_row in self.exits_of(doc):
                listed.add((code, exit_row["to"]))

        for region_code, edge in self.all_edges():
            if (edge.source, edge.target) not in listed:
                self.add("M8", edge.source,
                         f"the edge {edge.source} to {edge.target} has no matching Exits row",
                         "Add the exit, or remove the edge.", gate)
            if edge.one_way:
                if (edge.target, edge.source) in listed:
                    self.add("M8", edge.target,
                             f"lists an exit back to {edge.source}, but that edge is typed one-way",
                             "Remove the reverse exit, or clear the one-way flag.")
            elif (edge.target, edge.source) not in listed:
                self.add("M8", edge.target,
                         f"has no reverse exit to {edge.source}, and the edge is not typed one-way",
                         "Add the reverse exit, or type the edge one-way.", gate)

    # M9 ----------------------------------------------------------------
    def check_m9(self) -> None:
        gate = Gate("step", 10, "the location graph is only closed once step 10 has run")
        by_region: dict[str, list[str]] = {}
        for code, doc in self.corpus.locations.items():
            by_region.setdefault(str(doc.fm.get("region", "")), []).append(code)

        directed = self._directed_edges()
        for region_code, codes in sorted(by_region.items()):
            if len(codes) < 2:
                continue
            neighbours: dict[str, set[str]] = {code: set() for code in codes}
            inbound: dict[str, int] = {code: 0 for code in codes}
            for source, target in directed:
                if source in neighbours and target in neighbours:
                    neighbours[source].add(target)
                    neighbours[target].add(source)
                if target in inbound:
                    inbound[target] += 1

            start = sorted(codes)[0]
            seen = {start}
            stack = [start]
            while stack:
                node = stack.pop()
                for neighbour in neighbours[node]:
                    if neighbour not in seen:
                        seen.add(neighbour)
                        stack.append(neighbour)
            for code in sorted(codes):
                if code not in seen:
                    self.add("M9", code, f"is not reachable from the rest of {region_code}",
                             "Connect it, or move it to the region it belongs in.", gate)
                elif inbound[code] == 0:
                    self.add("M9", code, "has no inbound edge, so nothing leads to it",
                             "Add an edge into it, or clear a one-way flag.", gate)

    # M10 ---------------------------------------------------------------
    def check_m10(self) -> None:
        setting_containers: set[str] = set()
        if self.corpus.setting:
            setting_containers = {
                str(entry["id"])
                for entry in self.corpus.setting.fm.get("containers", []) or []
                if isinstance(entry, dict) and "id" in entry
            }

        members: dict[str, int] = {ident: 0 for ident in setting_containers}
        for code, doc in sorted(self.corpus.regions.items()):
            container = doc.fm.get("container")
            if not isinstance(container, str) or not container:
                self.add("M10", code, "names no setting-level container",
                         "Every region names exactly one.")
                continue
            if setting_containers and container not in setting_containers:
                self.add("M10", code, f"names container {container!r}, which setting.md does not declare",
                         f"Declared: {', '.join(sorted(setting_containers)) or 'none'}.")
                continue
            members[container] = members.get(container, 0) + 1

        gate5 = Gate("step", 5, "regions are placed at step 5")
        for ident, count in sorted(members.items()):
            if count == 0:
                self.add("M10", "setting", f"container {ident!r} holds no region",
                         "A container exists to group nodes on a diagram. Remove it or fill it.",
                         gate5)

        gate9 = Gate("step", 9, "locations are placed at step 9")
        for region_code, region in sorted(self.corpus.regions.items()):
            declared = {
                str(entry["id"])
                for entry in region.fm.get("containers", []) or []
                if isinstance(entry, dict) and "id" in entry
            }
            counts = {ident: 0 for ident in declared}
            for code, doc in sorted(self.corpus.locations.items()):
                if str(doc.fm.get("region", "")) != region_code:
                    continue
                container = doc.fm.get("container")
                if not isinstance(container, str) or not container:
                    self.add("M10", code, "names no region-level container",
                             "Every location names exactly one.")
                    continue
                if container not in declared:
                    self.add("M10", code,
                             f"names container {container!r}, which {region_code} does not declare",
                             f"Declared: {', '.join(sorted(declared)) or 'none'}.")
                    continue
                counts[container] += 1
            for ident, count in sorted(counts.items()):
                if count == 0:
                    self.add("M10", region_code, f"container {ident!r} holds no location",
                             "Remove the container, or place a location in it.", gate9)

    # M11 ---------------------------------------------------------------
    def check_m11(self) -> None:
        gate = Gate("mermaid_gen", None, "tools/mermaid_gen.py arrives at Milestone 5")
        if not self._gate_open(gate):
            self.notes.append("M11 skipped: tools/mermaid_gen.py does not exist yet")
            if self.final:
                self.add("M11", "build", "tools/mermaid_gen.py is missing, so no diagram can be re-derived",
                         "Milestone 5 writes it.")
            return
        sys.path.insert(0, str(self.root / "tools"))
        import mermaid_gen  # type: ignore  # noqa: PLC0415

        derived = mermaid_gen.derive(self.corpus)  # type: ignore[attr-defined]
        directory = self.root / common.DIAGRAMS_DIR
        for name, text in sorted(derived.items()):
            path = directory / name
            if not path.exists():
                self.add("M11", name, "derived diagram has no file",
                         "Run python tools/mermaid_gen.py.")
            elif path.read_text(encoding="utf-8").strip() != text.strip():
                self.add("M11", name, "file differs from what mermaid_gen.py re-derives",
                         "Diagrams are derived. Edit the connections table and regenerate.")
        if directory.is_dir():
            for path in sorted(directory.glob("*.md")):
                if path.name not in derived:
                    self.add("M11", path.name, "diagram file is not derived from any table",
                             "Delete it, or add the container it claims to draw.")

    # M12 ---------------------------------------------------------------
    def check_m12(self) -> None:
        doc = self.corpus.setting_connections
        if doc is not None:
            for table in doc.tables():
                lowered = {common.normalise_key(h): h for h in table.headers}
                if "from" not in lowered:
                    continue
                if "type" in lowered:
                    typed = [r for r in table.rows if r.get(lowered["type"], "").strip()]
                    if typed:
                        self.add("M12", "setting",
                                 f"setting connections carry {len(typed)} typed edges",
                                 "Connection type is drawn at tier 4 and nowhere else.")

        for code, conn in sorted(self.corpus.region_connections.items()):
            for table in conn.tables():
                lowered = {common.normalise_key(h): h for h in table.headers}
                if "from" not in lowered:
                    continue
                if "type" not in lowered:
                    self.add("M12", code, "region connections carry no Type column",
                             "Tier 4 is typed. Add a Type column.")
                    continue
                for index, row in enumerate(table.rows, start=1):
                    if not row.get(lowered["type"], "").strip():
                        self.add("M12", code, f"connections row {index} carries no type",
                                 "Every tier-4 edge is typed.")

        directory = self.root / common.DIAGRAMS_DIR
        if directory.is_dir():
            for path in sorted(directory.glob("*.md")):
                tier = path.name[1:2]
                if tier in {"1", "2", "3"} and RE_EDGE_LABEL.search(path.read_text(encoding="utf-8")):
                    self.add("M12", path.name, f"tier {tier} diagram carries a labelled edge",
                             "Tiers 1 to 3 answer only whether two nodes connect.")

    # M13 ---------------------------------------------------------------
    def check_m13(self) -> None:
        gate = Gate("diagrams", None, "the diagram layer is built at Milestone 5")
        directory = self.root / common.DIAGRAMS_DIR

        skip = [self.root / name for name in MERMAID_SKIP_DIRS + MERMAID_SKIP_FILES]
        for base in MERMAID_SCAN_DIRS:
            root_dir = self.root / base
            if not root_dir.is_dir():
                continue
            for path in sorted(root_dir.rglob("*.md")):
                if any(path.is_relative_to(skipped) for skipped in skip):
                    continue
                if common.RE_MERMAID_BLOCK.search(path.read_text(encoding="utf-8")):
                    self.add("M13", str(path.relative_to(self.root)),
                             "carries a mermaid block outside build/diagrams",
                             "Every diagram is derived. Replace it with a DIAGRAM marker.")

        for doc in self.content_docs():
            for name in common.RE_DIAGRAM_MARKER.findall(doc.body):
                if not (directory / name).exists():
                    self.add("M13", self.doc_code(doc), f"splice marker names {name}, which does not exist",
                             "Run python tools/mermaid_gen.py.", gate)

    # M14 ---------------------------------------------------------------
    def check_m14(self) -> None:
        for code, doc in sorted(self.corpus.locations.items()):
            for source in doc.fm.get("sources", []) or []:
                if str(source).startswith("S-"):
                    self.add("M14", code, f"cites {source}, and no location may cite an S table",
                             "S table content reaches a player through a T table. Cite the T entry.")

    # M15 ---------------------------------------------------------------
    def check_m15(self) -> None:
        gate = Gate("step", 10, "location citations are written at step 10")
        cited: set[str] = set()
        for doc in self.corpus.locations.values():
            for source in doc.fm.get("sources", []) or []:
                cited.add(str(source).rsplit("-", 1)[0])
        for code, doc in sorted(self.corpus.tables.items()):
            if str(doc.fm.get("kind", "")) != "T":
                continue
            if code not in cited:
                self.add("M15", code, "is cited by no location",
                         "A T table is connective. Cite it, or fold it away.", gate)

    # M16 ---------------------------------------------------------------
    def check_m16(self) -> None:
        entry_ids = self.corpus.entry_ids()
        by_section = self.corpus.table_by_section()

        for scope, docs in (("region", self.corpus.regions), ("location", self.corpus.locations)):
            for code, doc in sorted(docs.items()):
                for source in doc.fm.get("sources", []) or []:
                    source = str(source)
                    if not common.RE_ENTRY_ID.match(source):
                        self.add("M16", code, f"source {source!r} is not a table entry ID",
                                 "Cite a row such as T-RUM-07, not a table code.")
                    elif source not in entry_ids:
                        self.add("M16", code, f"source {source} resolves to no table row",
                                 "Correct the ID, or write the row.")

        for code, doc in sorted(self.corpus.tables.items()):
            for other in doc.fm.get("draws_on", []) or []:
                if str(other) not in self.corpus.tables:
                    self.add("M16", code, f"draws_on names {other}, which does not exist",
                             "Scaffold the table, or drop the reference.")

        for doc in self.content_docs():
            body = RE_HTML_COMMENT.sub("", doc.body)
            for section, key in common.RE_SECTION_MARK.findall(body):
                target = by_section.get(common.normalise_key(section))
                if target is None:
                    self.add("M16", self.doc_code(doc), f"({section}, ...) names no table",
                             "The section name is the table's name or its code.")
                    continue
                if not self._key_resolves(target, key.strip()):
                    self.add("M16", self.doc_code(doc),
                             f"({section}, {key.strip()}) resolves to no row in {target}",
                             "Correct the key, or write the row.")

    def _key_resolves(self, table_code: str, key: str) -> bool:
        """Whether a mark names a row. `build.py` asks which row, from the same rule."""
        return common.resolve_entry(self.corpus.table_rows(table_code), key) is not None

    # M17 ---------------------------------------------------------------
    def check_m17(self) -> None:
        for code, doc in sorted(self.corpus.locations.items()):
            overview = doc.section("Player Overview")
            features = doc.section("Features")
            if overview is None:
                continue
            titles = [sub.title for sub in features.subsections] if features else []
            keys = [self._noun_key(title) for title in titles]
            text = RE_HTML_COMMENT.sub("", common.RE_ARCHITECT_NOTE.sub("", overview.full_text))
            for noun in common.RE_BOLD.findall(text):
                want = self._noun_key(noun)
                if not want:
                    continue
                if not any(self._noun_match(want, key) for key in keys):
                    self.add("M17", code, f"the Player Overview bolds {noun!r} with no feature below it",
                             "A bolded noun is a promise. Write the feature, or unbold the noun.")

    @staticmethod
    def _noun_key(text: str) -> str:
        key = common.normalise_key(text)
        return re.sub(r"^(the|a|an)\s+", "", key)

    @staticmethod
    def _noun_match(want: str, have: str) -> bool:
        def fold(value: str) -> str:
            return re.sub(r"s$", "", value)

        if fold(want) == fold(have):
            return True
        return re.search(rf"\b{re.escape(fold(want))}s?\b", have) is not None

    # M18 ---------------------------------------------------------------
    def check_m18(self) -> None:
        gate = Gate("step", 3, "T-LNG roots are recorded at step 3")
        roots = self._roots()
        naming = self.weights.get("naming", {})
        stop = {str(word).lower() for word in naming.get("stop_words", [])}
        min_len = int(naming.get("min_root_length", 2))

        names: list[tuple[str, str]] = []
        if self.corpus.setting:
            names.append(("setting", str(self.corpus.setting.fm.get("name", ""))))
            for entry in self.corpus.setting.fm.get("containers", []) or []:
                if isinstance(entry, dict):
                    names.append(("setting", str(entry.get("name", ""))))
        for code, doc in sorted(self.corpus.regions.items()):
            names.append((code, str(doc.fm.get("name", ""))))
            for entry in doc.fm.get("containers", []) or []:
                if isinstance(entry, dict):
                    names.append((code, str(entry.get("name", ""))))
        for code, doc in sorted(self.corpus.locations.items()):
            names.append((code, str(doc.fm.get("name", ""))))

        if not roots:
            if names:
                self.add("M18", "T-LNG", "records no roots, so no name can be decomposed",
                         "Write the root vocabulary into T-LNG.", gate)
            return

        for code, name in names:
            for token in re.split(r"[\s'’-]+", name):
                word = re.sub(r"[^a-z]", "", token.lower())
                if not word or word in stop:
                    continue
                if not self._segments(word, roots, min_len):
                    self.add("M18", code, f"the name {name!r} uses {token!r}, which is in no T-LNG root",
                             "Propose the root in the step's question batch, then record it in T-LNG.",
                             gate)

    def _roots(self) -> set[str]:
        roots: set[str] = set()
        for row in self.corpus.table_rows("T-LNG"):
            for header in ("Root", "Entry"):
                value = row.get(header, "")
                if value:
                    for part in re.split(r"[,/]", value):
                        cleaned = re.sub(r"[^a-z]", "", part.lower())
                        if cleaned:
                            roots.add(cleaned)
                    break
        return roots

    @staticmethod
    def _segments(word: str, roots: set[str], min_len: int) -> bool:
        length = len(word)
        reachable = [False] * (length + 1)
        reachable[0] = True
        for end in range(1, length + 1):
            for start in range(0, end):
                if not reachable[start] or end - start < min_len:
                    continue
                piece = word[start:end]
                if piece in roots or (piece.endswith("s") and piece[:-1] in roots):
                    reachable[end] = True
                    break
        return reachable[length]

    # M19 ---------------------------------------------------------------
    def check_m19(self) -> None:
        want_rows = int(self.weights["region_tables"]["rows"])
        weather_rows = int(self.weights["region_tables"]["weather_rows"])
        for code, doc in sorted(self.corpus.regions.items()):
            region_type = str(doc.fm.get("type", ""))
            expected = common.REGION_TABLE_BY_TYPE.get(region_type)
            if expected is None:
                continue
            name, direction = expected
            section = doc.section("Tables")
            if section is None:
                self.add("M19", code, "carries no Tables section", "Re-run the region scaffold.")
                continue
            sub = section.subsection(name)
            if sub is None:
                found = ", ".join(s.title for s in section.subsections) or "nothing"
                self.add("M19", code, f"a {region_type} region carries a {name} table, and holds {found}",
                         f"Rename the table to {name}.")
                continue
            tables = common.parse_tables(sub.text)
            if not tables:
                self.add("M19", code, f"the {name} table has no rows", "Re-run the region scaffold.")
                continue
            rolls = [row.get(tables[0].headers[0], "").strip() for row in tables[0].rows]
            if len(rolls) != want_rows:
                self.add("M19", code, f"the {name} table has {len(rolls)} rows, not {want_rows}",
                         f"Every referee table is {want_rows} rows on a "
                         f"{self.weights['region_tables']['die']}.")
                continue
            try:
                numbers = [int(value) for value in rolls]
            except ValueError:
                self.add("M19", code, f"the {name} table has a non-numeric roll column",
                         f"Number the rungs 1 to {want_rows}.")
                continue
            want = (list(range(want_rows, 0, -1)) if direction == "descending"
                    else list(range(1, want_rows + 1)))
            if numbers != want:
                self.add("M19", code,
                         f"the {name} table runs {numbers}, and a {region_type} table runs {want}",
                         f"A Danger table counts down from {want_rows} to 1. The others count up.")

            weather = section.subsection("Weather")
            if weather is not None:
                wtables = common.parse_tables(weather.text)
                rows = len(wtables[0].rows) if wtables else 0
                if rows != weather_rows:
                    self.add("M19", code, f"the Weather table has {rows} rows, not {weather_rows}",
                             f"A Weather table is {weather_rows} rows.")

    # M20 ---------------------------------------------------------------
    def check_m20(self) -> None:
        gate = Gate("step", 10, "a gate and its key are paired at step 10")
        if "T-KEY" not in self.corpus.tables:
            return
        rows = self.corpus.table_rows("T-KEY")
        for row in rows:
            ident = row.get("ID", "").strip() or "T-KEY row"
            for column, role in (("Found in", "the key"), ("Opens", "the gate")):
                value = row.get(column, "").strip()
                if not value:
                    self.add("M20", ident, f"names no location for {role} ({column})",
                             "A gate and its key are two locations by definition.", gate)
                    continue
                for candidate in re.findall(r"R\d{2}-L\d{2}", value):
                    if candidate not in self.corpus.locations:
                        self.add("M20", ident, f"{column} names {candidate}, which does not exist",
                                 "Correct the code, or scaffold the location.")
                if not re.search(r"R\d{2}-L\d{2}", value):
                    self.add("M20", ident, f"{column} is {value!r}, which carries no location code",
                             "Name the location by code so both ends are checkable.", gate)

    # M21 ---------------------------------------------------------------
    def check_m21(self) -> None:
        if not self.tokens:
            return
        for doc in self.content_docs():
            for name, value in common.RE_TOKEN.findall(doc.body):
                if name not in self.tokens:
                    self.add("M21", self.doc_code(doc), f"{{{name}: ...}} is not in the token vocabulary",
                             f"MECHANICS.md defines: {', '.join(sorted(self.tokens))}.")
                    continue
                form, allowed = self.tokens[name]
                problem = self._token_problem(form, allowed, value.strip())
                if problem:
                    self.add("M21", self.doc_code(doc), f"{{{name}: {value.strip()}}} {problem}",
                             "MECHANICS.md carries the form and the values.")

    @staticmethod
    def _token_problem(form: str, allowed: list[str], value: str) -> str:
        if form == "enum":
            lowered = {item.lower() for item in allowed}
            if value.lower() not in lowered:
                return f"is not one of {', '.join(allowed)}"
            return ""
        if form.startswith("parts:"):
            want = int(form.split(":", 1)[1])
            parts = [part.strip() for part in value.split("/")]
            if len(parts) != want or not all(parts):
                return f"needs {want} non-empty parts separated by /"
            return ""
        if form == "ad":
            match = re.fullmatch(r"(\d+)\s*,\s*([+-]\d+)", value)
            if not match:
                return "is not written as `n, +m`"
            if not -2 <= int(match.group(2)) <= 6:
                return "carries a modifier outside -2 to +6"
            return ""
        if form == "value":
            if not re.fullmatch(r"\d+\s*cn", value, re.IGNORECASE):
                return "is not written as `n cn`"
            return ""
        if form == "int":
            if not re.fullmatch(r"\d+", value):
                return "is not a bare integer"
            return ""
        return ""

    # M22 ---------------------------------------------------------------
    def check_m22(self) -> None:
        scales = (
            ([("setting", self.corpus.setting)] if self.corpus.setting else [])
            + sorted(self.corpus.regions.items())
            + sorted(self.corpus.locations.items())
        )
        for code, doc in scales:
            for heading in common.REQUIRED_HEADINGS[doc.scale]:
                if doc.section(heading) is None:
                    self.add("M22", code, f"carries no {heading!r} heading",
                             f"A {doc.scale} carries: "
                             f"{', '.join(common.REQUIRED_HEADINGS[doc.scale])}.")

        gate = Gate("step", 11, "location fields are written at step 11")
        for code, doc in sorted(self.corpus.locations.items()):
            region = self.region_of(doc)
            if region is None:
                continue
            required = common.REQUIRED_FIELDS_BY_TYPE.get(str(region.fm.get("type", "")), [])
            section = doc.section("Referee Overview")
            text = section.full_text if section else ""
            for label in required:
                match = re.search(rf"\*\*{re.escape(label)}:\*\*(.*)", text)
                if match is None:
                    self.add("M22", code, f"declares no {label!r} field, and its region is "
                                          f"{region.fm.get('type')}",
                             f"A {region.fm.get('type')} location declares: {', '.join(required)}.")
                    continue
                value = match.group(1).strip()
                if not value:
                    self.add("M22", code, f"the {label!r} field is empty",
                             "State the value, or write `None` with a brief reason.", gate)
                elif re.fullmatch(r"none\.?", value, re.IGNORECASE):
                    self.add("M22", code, f"the {label!r} field is a bare None",
                             "An omitted reason is ambiguous. Write `None` and why.")

    # M23 ---------------------------------------------------------------
    def check_m23(self) -> None:
        for doc in self.content_docs():
            for section in doc.sections:
                if common.normalise_key(section.title) == "features":
                    continue
                text = RE_HTML_COMMENT.sub("", section.full_text)
                for line in text.split("\n"):
                    if "->" in line:
                        self.add("M23", self.doc_code(doc),
                                 f"uses -> outside a feature: {line.strip()!r}",
                                 "A pointer is what the diagram derivation reads. "
                                 "Move it into a feature.")

    # M24 ---------------------------------------------------------------
    def check_m24(self) -> None:
        for doc in self.content_docs():
            if doc.code == "T-PRC":
                continue  # the one place a die roll may gate a result
            body = RE_HTML_COMMENT.sub("", doc.body)
            stripped = common.RE_TOKEN.sub("", body)
            for pattern, catches in self.bare_patterns:
                for match in pattern.finditer(stripped):
                    self.add("M24", self.doc_code(doc),
                             f"prose carries the bare mechanical value {match.group(0)!r}",
                             f"Carry it as a token instead. This pattern catches {catches}.")
                    break

        for code, doc in sorted(self.corpus.locations.items()):
            section = doc.section("Player Overview")
            if section is None:
                continue
            for name, _ in common.RE_TOKEN.findall(section.full_text):
                self.add("M24", code, f"the Player Overview carries the token {{{name}: ...}}",
                         "A token is referee-facing. Move it into the Referee Overview or a feature.")

    # M25 ---------------------------------------------------------------
    def check_m25(self) -> None:
        for doc in self.content_docs():
            code = self.doc_code(doc)
            notes = common.RE_ARCHITECT_NOTE.findall(doc.body)
            if not notes:
                continue
            if self.final or self.ledger.is_decorated(code):
                self.add("M25", code, f"carries {len(notes)} architect notes after the Decorator closed it",
                         "A note is struck when its content is absorbed.")

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def in_scope(self, scope: str, finding: Finding) -> bool:
        if scope in {"all", ""}:
            return True
        code = finding.code
        if scope == "tables":
            return code in self.corpus.tables
        if scope == "setting":
            return code in {"setting", "build"} or code in self.corpus.tables
        if common.RE_LOCATION_CODE.match(scope):
            return code == scope
        if common.RE_REGION_CODE.match(scope):
            return code == scope or code.startswith(f"{scope}-")
        return code == scope


def report(findings: list[Finding], notes: list[str], as_json: bool) -> int:
    errors = [f for f in findings if f.severity == "ERROR"]
    reports = [f for f in findings if f.severity == "REPORT"]

    if as_json:
        print(json.dumps(
            {"errors": len(errors), "reports": len(reports),
             "findings": [f.as_dict() for f in findings], "notes": notes},
            indent=2,
        ))
        return 1 if errors else 0

    for note in notes:
        print(f"note: {note}")
    if findings:
        print()
        print("| Code | Check | Severity | Finding | Suggested fix |")
        print("| :--- | :--- | :--- | :--- | :--- |")
        for finding in sorted(findings, key=lambda f: (int(f.check[1:]), f.code)):
            severity = finding.severity
            if finding.deferred:
                severity += f" (deferred: {finding.deferred})"
            message = finding.message.replace("|", "\\|")
            fix = finding.fix.replace("|", "\\|")
            print(f"| {finding.code} | {finding.check} | {severity} | {message} | {fix} |")
        print()
    print(f"{len(errors)} errors, {len(reports)} reports.")
    return 1 if errors else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", type=Path, default=common.REPO_ROOT)
    parser.add_argument("--scope", default="all",
                        help="all, setting, tables, a region code, or a location code")
    parser.add_argument("--target", help="shorthand for --scope <code>")
    parser.add_argument("--final", action="store_true",
                        help="promote every REPORT to ERROR, and ignore every gate")
    parser.add_argument("--only", help="run only these checks, such as M6,M17")
    parser.add_argument("--list", action="store_true", help="list the checks and exit")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.list:
        for name, description in sorted(CHECKS.items(), key=lambda item: int(item[0][1:])):
            severity = "REPORT" if name in REPORT_CHECKS else "ERROR"
            print(f"{name:<4} {severity:<6} {description}")
        return 0

    only = None
    if args.only:
        only = {name.strip().upper() for name in args.only.split(",") if name.strip()}
        unknown = only - set(CHECKS)
        if unknown:
            print(f"error: unknown checks {', '.join(sorted(unknown))}", file=sys.stderr)
            return 2

    root = args.root.resolve()
    scope = args.target or args.scope

    try:
        validator = Validator(root, final=args.final, only=only)
    except common.DocError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    validator.run()
    findings = [f for f in validator.findings if validator.in_scope(scope, f)]
    return report(findings, validator.notes, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
