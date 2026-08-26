"""Shared library for the content builder tools.

This is the one module that knows the shape of the repository: where files
live, what frontmatter each scale carries, and how a markdown body decomposes
into sections and tables. It is a library, not a command line interface.

The table catalogue lives here rather than in ``config/weights.yaml`` because
that file's stated purpose is numbers with two consumers, and a catalogue of
codes is structure rather than tuning. Section 4.7 of SPEC.md is its source.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml

# --------------------------------------------------------------------------
# Repository layout
# --------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

SETTING_DIR = "setting"
TABLES_DIR = "setting/tables"
REGIONS_DIR = "setting/regions"
DIAGRAMS_DIR = "build/diagrams"
BUNDLES_DIR = "build/bundles"
LEDGER_PATH = "state/ledger.json"
STATE_PATH = "STATE.md"
WEIGHTS_PATH = "config/weights.yaml"
MECHANICS_PATH = "MECHANICS.md"

SCHEMA_VERSION = 1

# --------------------------------------------------------------------------
# Catalogue (SPEC.md section 4.7)
# --------------------------------------------------------------------------

S_TABLES = {
    "S-HIS": "History",
    "S-TRU": "Truths",
    "S-FAC": "Factions",
    "S-AMB": "Ambiance",
}

T_TABLES = {
    "T-LNG": "Language and Root Vocabulary",
    "T-NAM": "Names",
    "T-LOR": "Lore",
    "T-RUM": "Rumours",
    "T-UNQ": "Unanswered Questions",
    "T-PUZ": "Puzzles",
    "T-KEY": "Keys",
    "T-HAZ": "Hazards",
    "T-BES": "Bestiary",
    "T-CRE": "Named Creatures",
    "T-PRC": "Procedures",
    "T-ARC": "Architecture and Terrain",
    "T-TRE": "Unique Treasures",
    "T-TOM": "Magical Tomes",
    "T-HRD": "Hoards",
    "T-TR1": "Treasure Table I",
    "T-TR2": "Treasure Table II",
    "T-TR3": "Treasure Table III",
    "T-TR4": "Treasure Table IV",
    "T-TR5": "Treasure Table V",
}

# Artifact tables. These receive a Decorator pass at step 4; the rest stop at
# Builder.
DECORATED_TABLES = {"T-LOR", "T-RUM", "T-BES", "T-CRE", "T-TRE", "T-TOM", "T-HRD"}

# Columns a structurally checked table must carry. Every other table takes the
# default, and its own pattern replaces the header at Milestone 4.
DEFAULT_TABLE_COLUMNS = ["ID", "Entry"]
TABLE_COLUMNS = {
    "T-LNG": ["ID", "Root", "Meaning"],
    "T-KEY": ["ID", "Key", "Found in", "Opens"],
    "T-ARC": ["ID", "Entry", "Types"],
    "T-PRC": ["ID", "Procedure", "Roll", "Outcomes"],
}


def table_columns(code: str) -> list[str]:
    return list(TABLE_COLUMNS.get(code, DEFAULT_TABLE_COLUMNS))


# Diagram file names, by tier. `mermaid_gen.py` writes these and nothing else.
def diagram_name(tier: int, *parts: str) -> str:
    tail = "_".join(re.sub(r"[^A-Za-z0-9]+", "_", part).strip("_").upper() for part in parts)
    return f"T{tier}_{tail}.md" if tail else f"T{tier}.md"


# Required body headings by scale (SPEC.md section 4.6).
REQUIRED_HEADINGS = {
    "setting": ["Overview", "Style", "Tables", "Regions"],
    "region": ["Overview", "Fields", "Tables", "Connections", "Diagram"],
    "location": ["Player Overview", "Referee Overview", "Features", "Exits"],
}

# The table a region of each type carries, and its direction (SPEC.md 9.2).
REGION_TABLE_BY_TYPE = {
    "SAFE": ("Events", "ascending"),
    "WILD": ("Encounters", "ascending"),
    "DANGEROUS": ("Dangers", "descending"),
}

# Fields every location declares, by its region's type (SPEC.md 9.2). Written
# as bold labels in the Referee Overview. `None` plus a reason is a legal
# value; a bare `None` is not.
REQUIRED_FIELDS_BY_TYPE = {
    "SAFE": ["Service", "Cost", "Refusal"],
    "WILD": ["Approach", "Terrain"],
    "DANGEROUS": ["Reactions", "Gate"],
}

# Codes
RE_S_CODE = re.compile(r"^S-[A-Z]{3}$")
RE_T_CODE = re.compile(r"^T-[A-Z0-9]{3}$")
RE_REGION_CODE = re.compile(r"^R\d{2}$")
RE_LOCATION_CODE = re.compile(r"^R\d{2}-L\d{2}$")
RE_ENTRY_ID = re.compile(r"^[ST]-[A-Z0-9]{3}-\d{2}$")
RE_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Inline marks (SPEC.md section 10.6)
RE_SECTION_MARK = re.compile(r"\(([A-Z][A-Z0-9 _-]*),\s*([^)]+)\)")
RE_POINTER = re.compile(r"->\s*([A-Za-z0-9-]+)")
RE_ARCHITECT_NOTE = re.compile(r"\[\[.*?\]\]", re.DOTALL)
RE_DIAGRAM_MARKER = re.compile(r"<!--\s*DIAGRAM:\s*([^\s>]+?)\s*-->")
RE_MERMAID_BLOCK = re.compile(r"^```mermaid\b", re.MULTILINE)
RE_TOKEN = re.compile(r"\{([A-Z][A-Z0-9_]*)\s*:\s*([^}]*)\}")
RE_BOLD = re.compile(r"\*\*([^*]+)\*\*")


def slugify(name: str) -> str:
    """Lowercase, hyphenated form of a name. Used for filenames and container ids."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug


def normalise_key(text: str) -> str:
    """Fold a section name or an entry key to a comparable form."""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


# --------------------------------------------------------------------------
# Frontmatter and body
# --------------------------------------------------------------------------


class DocError(Exception):
    """A file could not be read as markdown with YAML frontmatter."""


@dataclass
class Table:
    """One markdown table, with its header row and its rows as dicts."""

    headers: list[str]
    rows: list[dict[str, str]]
    heading: str = ""

    def column(self, name: str) -> list[str]:
        return [row.get(name, "") for row in self.rows]


@dataclass
class Section:
    """One ``##`` section of a body, with its ``###`` subsections."""

    title: str
    text: str = ""
    subsections: list["Section"] = field(default_factory=list)

    @property
    def full_text(self) -> str:
        parts = [self.text]
        for sub in self.subsections:
            parts.append(f"### {sub.title}\n{sub.text}")
        return "\n".join(parts)

    def subsection(self, title: str) -> "Section | None":
        want = normalise_key(title)
        for sub in self.subsections:
            if normalise_key(sub.title) == want:
                return sub
        return None


@dataclass
class Doc:
    """A content file: frontmatter, body, and the scale it belongs to."""

    path: Path
    fm: dict[str, Any]
    body: str
    scale: str  # setting | region | location | table | connections

    _sections: list[Section] | None = None

    @property
    def relpath(self) -> str:
        try:
            return str(self.path.relative_to(REPO_ROOT))
        except ValueError:
            return str(self.path)

    @property
    def code(self) -> str:
        return str(self.fm.get("code", ""))

    @property
    def sections(self) -> list[Section]:
        if self._sections is None:
            self._sections = parse_sections(self.body)
        return self._sections

    def section(self, title: str) -> Section | None:
        want = normalise_key(title)
        for sec in self.sections:
            if normalise_key(sec.title) == want:
                return sec
        return None

    def tables(self) -> list[Table]:
        return parse_tables(self.body)


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split ``---`` delimited YAML frontmatter from the markdown body."""
    if not text.startswith("---"):
        raise DocError("file does not open with YAML frontmatter")
    parts = text.split("\n")
    if parts[0].strip() != "---":
        raise DocError("file does not open with YAML frontmatter")
    for index in range(1, len(parts)):
        if parts[index].strip() == "---":
            raw = "\n".join(parts[1:index])
            body = "\n".join(parts[index + 1 :])
            try:
                data = yaml.safe_load(raw) or {}
            except yaml.YAMLError as exc:  # pragma: no cover - message passthrough
                raise DocError(f"frontmatter is not valid YAML: {exc}") from exc
            if not isinstance(data, dict):
                raise DocError("frontmatter is not a mapping")
            return data, body
    raise DocError("frontmatter is not closed by a second ---")


def read_doc(path: Path, scale: str) -> Doc:
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    return Doc(path=path, fm=fm, body=body, scale=scale)


def write_doc(path: Path, fm: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # `default_flow_style=None` keeps flat lists inline, so `tags: [a, b, c]`
    # reads on one line while the container list stays a block.
    front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                           default_flow_style=None).rstrip("\n")
    body = body.rstrip("\n")
    path.write_text(f"---\n{front}\n---\n\n{body}\n", encoding="utf-8")


def parse_sections(body: str) -> list[Section]:
    """Decompose a body into ``##`` sections, each holding its ``###`` children."""
    sections: list[Section] = []
    current: Section | None = None
    current_sub: Section | None = None
    in_fence = False

    for line in body.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            current = Section(title=line[3:].strip())
            current_sub = None
            sections.append(current)
            continue
        if not in_fence and line.startswith("### ") and current is not None:
            current_sub = Section(title=line[4:].strip())
            current.subsections.append(current_sub)
            continue
        target = current_sub or current
        if target is not None:
            target.text += line + "\n"

    return sections


def _split_row(line: str) -> list[str]:
    """Split a markdown table row on unescaped pipes."""
    cells: list[str] = []
    buf = ""
    text = line.strip()
    index = 0
    while index < len(text):
        char = text[index]
        # Only `\|` is an escape. Every other backslash survives, because table
        # cells carry regular expressions.
        if char == "\\" and index + 1 < len(text) and text[index + 1] == "|":
            buf += "|"
            index += 2
            continue
        if char == "|":
            cells.append(buf)
            buf = ""
            index += 1
            continue
        buf += char
        index += 1
    cells.append(buf)
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [cell.strip() for cell in cells]


def _is_divider(cells: Iterable[str]) -> bool:
    cells = list(cells)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def parse_tables(text: str) -> list[Table]:
    """Every markdown table in ``text``, tagged with the heading above it."""
    tables: list[Table] = []
    lines = text.split("\n")
    heading = ""
    index = 0
    in_fence = False
    while index < len(lines):
        line = lines[index]
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            index += 1
            continue
        if not in_fence and line.startswith("#"):
            heading = line.lstrip("#").strip()
        if not in_fence and line.strip().startswith("|") and index + 1 < len(lines):
            headers = _split_row(line)
            divider = _split_row(lines[index + 1])
            if _is_divider(divider) and len(divider) == len(headers):
                rows: list[dict[str, str]] = []
                cursor = index + 2
                while cursor < len(lines) and lines[cursor].strip().startswith("|"):
                    cells = _split_row(lines[cursor])
                    cells += [""] * (len(headers) - len(cells))
                    rows.append(dict(zip(headers, cells[: len(headers)])))
                    cursor += 1
                tables.append(Table(headers=headers, rows=rows, heading=heading))
                index = cursor
                continue
        index += 1
    return tables


# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------


def load_weights(root: Path | None = None) -> dict[str, Any]:
    root = root or REPO_ROOT
    path = root / WEIGHTS_PATH
    if not path.exists():
        raise DocError(f"{WEIGHTS_PATH} is missing")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


# --------------------------------------------------------------------------
# Corpus
# --------------------------------------------------------------------------


@dataclass
class Corpus:
    """Every content file under ``setting/``, loaded once and indexed by code."""

    root: Path
    setting: Doc | None = None
    tables: dict[str, Doc] = field(default_factory=dict)
    regions: dict[str, Doc] = field(default_factory=dict)
    locations: dict[str, Doc] = field(default_factory=dict)
    setting_connections: Doc | None = None
    region_connections: dict[str, Doc] = field(default_factory=dict)
    read_errors: list[tuple[Path, str]] = field(default_factory=list)
    # Every content file read, in the order read. The indexes above are keyed by
    # code, so a duplicated code would silently drop a file from them. M1 reads
    # this list instead, which is the only place the collision is still visible.
    docs: list[Doc] = field(default_factory=list)

    def locations_in(self, region_code: str) -> list[Doc]:
        return [
            doc
            for doc in self.locations.values()
            if str(doc.fm.get("region", "")) == region_code
        ]

    def table_rows(self, code: str) -> list[dict[str, str]]:
        doc = self.tables.get(code)
        if doc is None:
            return []
        tables = doc.tables()
        return tables[0].rows if tables else []

    def entry_ids(self) -> set[str]:
        ids: set[str] = set()
        for code in self.tables:
            for row in self.table_rows(code):
                entry = row.get("ID", "").strip()
                if entry:
                    ids.add(entry)
        return ids


def load_corpus(root: Path | None = None) -> Corpus:
    root = root or REPO_ROOT
    corpus = Corpus(root=root)

    def _read(path: Path, scale: str) -> Doc | None:
        try:
            doc = read_doc(path, scale)
        except (DocError, OSError) as exc:
            corpus.read_errors.append((path, str(exc)))
            return None
        corpus.docs.append(doc)
        return doc

    setting_file = root / SETTING_DIR / "setting.md"
    if setting_file.exists():
        corpus.setting = _read(setting_file, "setting")

    setting_conn = root / SETTING_DIR / "connections.md"
    if setting_conn.exists():
        corpus.setting_connections = _read(setting_conn, "connections")

    tables_dir = root / TABLES_DIR
    if tables_dir.is_dir():
        for path in sorted(tables_dir.glob("*.md")):
            doc = _read(path, "table")
            if doc is not None:
                corpus.tables[doc.code or path.stem] = doc

    regions_dir = root / REGIONS_DIR
    if regions_dir.is_dir():
        for region_dir in sorted(p for p in regions_dir.iterdir() if p.is_dir()):
            region_file = region_dir / "region.md"
            if region_file.exists():
                doc = _read(region_file, "region")
                if doc is not None:
                    corpus.regions[doc.code or region_dir.name] = doc
            conn_file = region_dir / "connections.md"
            if conn_file.exists():
                doc = _read(conn_file, "connections")
                if doc is not None:
                    key = str(doc.fm.get("code", region_dir.name.split("-")[0]))
                    corpus.region_connections[key] = doc
            loc_dir = region_dir / "locations"
            if loc_dir.is_dir():
                for path in sorted(loc_dir.glob("*.md")):
                    doc = _read(path, "location")
                    if doc is not None:
                        corpus.locations[doc.code or path.stem] = doc

    return corpus


# --------------------------------------------------------------------------
# Edges
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str = ""
    one_way: bool = False
    origin: str = ""


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"yes", "true", "y", "1", "one-way", "one way"}


def edges_from(doc: Doc | None) -> list[Edge]:
    """Read a connections table into edges. Columns: From, To, Type, One-way."""
    if doc is None:
        return []
    edges: list[Edge] = []
    for table in doc.tables():
        lowered = {normalise_key(header): header for header in table.headers}
        src_key = lowered.get("from")
        dst_key = lowered.get("to")
        if not src_key or not dst_key:
            continue
        kind_key = lowered.get("type")
        way_key = lowered.get("one way")
        for row in table.rows:
            source = row.get(src_key, "").strip()
            target = row.get(dst_key, "").strip()
            if not source or not target:
                continue
            edges.append(
                Edge(
                    source=source,
                    target=target,
                    kind=row.get(kind_key, "").strip() if kind_key else "",
                    one_way=_truthy(row.get(way_key, "")) if way_key else False,
                    origin=doc.relpath,
                )
            )
    return edges
