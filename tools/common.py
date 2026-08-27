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
PATTERNS_DIR = "patterns"
CELLS_DIR = "patterns/cells"
LEDGER_PATH = "state/ledger.json"
STATE_PATH = "STATE.md"
WEIGHTS_PATH = "config/weights.yaml"
MECHANICS_PATH = "MECHANICS.md"
GENRE_PATH = "patterns/GENRE.md"
GENRE_EXAMPLE_PATH = "patterns/GENRE.example.md"
ROUTER_PATH = "DESIGN_PATTERNS.md"

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


class _FrontmatterDumper(yaml.SafeDumper):
    """Block style for the frontmatter itself, flow style for a flat list in it.

    `default_flow_style=None` collapses any collection holding no collection of
    its own, which is what puts `tags: [a, b, c]` on one line. Applied to the
    frontmatter mapping it also collapses a flat one such as a table's onto a
    single line, so the top level is forced back to block here and every other
    node keeps the rule.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._mapping_depth = 0

    def represent_mapping(self, tag: str, mapping: Any, flow_style: Any = None) -> Any:
        self._mapping_depth += 1
        try:
            if self._mapping_depth == 1:
                flow_style = False
            return super().represent_mapping(tag, mapping, flow_style)
        finally:
            self._mapping_depth -= 1


def write_doc(path: Path, fm: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    front = yaml.dump(fm, Dumper=_FrontmatterDumper, sort_keys=False,
                      allow_unicode=True, default_flow_style=None).rstrip("\n")
    # `split_frontmatter` hands back a body that opens with the newline after the
    # closing `---`. Trimming both ends here means a read-and-rewrite round trip
    # is a fixed point rather than adding a blank line each time.
    body = body.strip("\n")
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
# Patterns
# --------------------------------------------------------------------------

# A pattern's frontmatter is the router's whole input and the dependency
# resolver's whole input, so its vocabulary is fixed here rather than in either
# script (SPEC.md section 7.1).
PATTERN_TARGETS = ["setting", "region", "location", "table"]
PATTERN_PHASES = ["architect", "engineer", "builder", "decorator"]
PATTERN_HEADINGS = ["Patterns", "Excluded patterns", "Design questions"]
PATTERN_KEYS = ["id", "target", "phase", "writes", "dependencies", "schema_version"]

# Three things live under `patterns/` and are not routed patterns. A cell file
# is guidance selected by a `cell:` selector and carries no target or phase. A
# template is an output shape. `GENRE.md` is the genre brief itself, injected
# into every bundle. Everything else under `patterns/` must be a pattern, so a
# malformed one is an error rather than a file quietly skipped.
UNROUTED_DIRS = ("cells", "templates")
UNROUTED_FILES = ("GENRE.md",)

RE_PATTERN_ID = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)*$")
RE_CELL = re.compile(r"^(SAFE|WILD|DANGEROUS)_(LOW|MEDIUM|HIGH)$")
RE_VARIABLE = re.compile(r"\$\{([A-Z_]+)\}")

# Filled from command arguments before resolution (SPEC.md section 7.4).
VARIABLES = ["REGION_CODE", "LOCATION_CODE", "CONTAINER_ID", "CELL"]

SELECTOR_FORMS = [
    "table:S-XXX",
    "table:T-XXX",
    "region:R##",
    "container:<id>",
    "siblings:location:R##",
    "cell:<TYPE>_<WEIGHT>",
    "config",
]


class SelectorError(DocError):
    """A dependency selector is not one of the seven forms."""


@dataclass(frozen=True)
class Selector:
    """One parsed dependency selector."""

    kind: str  # table | region | container | siblings | cell | config
    value: str
    raw: str

    @property
    def has_variable(self) -> bool:
        return bool(RE_VARIABLE.search(self.raw))


def parse_selector(raw: str) -> Selector:
    """Parse one selector. A `${VAR}` value is left unchecked until it is filled."""
    text = raw.strip()
    if not text:
        raise SelectorError("empty selector")
    if text == "config":
        return Selector("config", "", text)

    head, _, value = text.partition(":")
    if not value:
        raise SelectorError(
            f"{raw!r} is not a selector. The seven forms are: {', '.join(SELECTOR_FORMS)}."
        )

    if head == "siblings":
        scale, _, code = value.partition(":")
        if scale != "location":
            raise SelectorError(f"{raw!r} is not a selector. Only siblings:location:R## exists.")
        value = code

    kind = {"table": "table", "region": "region", "container": "container",
            "siblings": "siblings", "cell": "cell"}.get(head)
    if kind is None:
        raise SelectorError(
            f"{raw!r} is not a selector. The seven forms are: {', '.join(SELECTOR_FORMS)}."
        )

    selector = Selector(kind, value, text)
    if not selector.has_variable:
        check_selector_value(selector)
    return selector


def check_selector_value(selector: Selector) -> None:
    """Check a selector's value once every variable in it has been filled."""
    value = selector.value
    if selector.kind == "table" and value not in S_TABLES and value not in T_TABLES:
        raise SelectorError(f"{value} is not in the table catalogue")
    if selector.kind in {"region", "siblings"} and not RE_REGION_CODE.match(value):
        raise SelectorError(f"{value} is not a region code such as R03")
    if selector.kind == "container" and not RE_SLUG.match(value):
        raise SelectorError(f"container id {value!r} is not a lowercase slug")
    if selector.kind == "cell" and not RE_CELL.match(value):
        raise SelectorError(f"{value} is not a cell such as WILD_HIGH")


def substitute(text: str, variables: dict[str, str]) -> str:
    """Fill `${VAR}` from ``variables``. An unknown name is left in place."""
    return RE_VARIABLE.sub(
        lambda match: variables.get(match.group(1), match.group(0)), text
    )


@dataclass
class Pattern:
    """One pattern file: the frontmatter the router reads, and the body a model reads."""

    doc: Doc

    @property
    def path(self) -> Path:
        return self.doc.path

    @property
    def relpath(self) -> str:
        return self.doc.relpath

    @property
    def id(self) -> str:
        return str(self.doc.fm.get("id", ""))

    @property
    def target(self) -> str:
        return str(self.doc.fm.get("target", ""))

    @property
    def phase(self) -> str:
        return str(self.doc.fm.get("phase", ""))

    @property
    def writes(self) -> list[str]:
        value = self.doc.fm.get("writes") or []
        return [str(item) for item in value] if isinstance(value, list) else []

    @property
    def dependencies(self) -> list[str]:
        value = self.doc.fm.get("dependencies") or []
        return [str(item) for item in value] if isinstance(value, list) else []

    @property
    def output_template(self) -> str:
        return str(self.doc.fm.get("output_template", "") or "")

    def selectors(self, variables: dict[str, str] | None = None) -> list[Selector]:
        """Parsed dependencies, with variables filled when they are supplied."""
        parsed: list[Selector] = []
        for raw in self.dependencies:
            filled = substitute(raw, variables) if variables else raw
            selector = parse_selector(filled)
            if variables and selector.has_variable:
                name = RE_VARIABLE.search(selector.raw).group(1)
                raise SelectorError(
                    f"{selector.raw!r} still carries ${{{name}}}. "
                    f"Supply it with --var {name}=<value>."
                )
            parsed.append(selector)
        return parsed


def pattern_errors(pattern: Pattern, root: Path | None = None) -> list[str]:
    """Everything wrong with a pattern's frontmatter and body shape.

    The router refuses to write an index from a broken pattern, and
    `resolve_deps.py` refuses to bundle one, so both ask here.
    """
    root = root or REPO_ROOT
    problems: list[str] = []
    fm = pattern.doc.fm

    for key in PATTERN_KEYS:
        if key not in fm:
            problems.append(f"carries no {key!r} key")
    if not RE_PATTERN_ID.match(pattern.id):
        problems.append(f"id {pattern.id!r} is not a dotted lowercase name such as "
                        f"location.builder.fields")
    if pattern.target not in PATTERN_TARGETS:
        problems.append(f"target {pattern.target!r} is not one of {', '.join(PATTERN_TARGETS)}")
    if pattern.phase not in PATTERN_PHASES:
        problems.append(f"phase {pattern.phase!r} is not one of {', '.join(PATTERN_PHASES)}")
    for key in ("writes", "dependencies"):
        if key in fm and not isinstance(fm[key], list):
            problems.append(f"{key!r} is not a list")
    if fm.get("schema_version") != SCHEMA_VERSION:
        problems.append(f"schema_version is not {SCHEMA_VERSION}")

    for raw in pattern.dependencies:
        try:
            parse_selector(raw)
        except SelectorError as exc:
            problems.append(str(exc))

    if pattern.output_template:
        if not (root / PATTERNS_DIR / pattern.output_template).exists():
            problems.append(f"output_template {pattern.output_template!r} does not exist")

    for heading in PATTERN_HEADINGS:
        if pattern.doc.section(heading) is None:
            problems.append(f"carries no {heading!r} heading")

    return problems


def is_pattern_file(path: Path, root: Path) -> bool:
    relative = path.relative_to(root / PATTERNS_DIR)
    if relative.parts[0] in UNROUTED_DIRS:
        return False
    return relative.name not in UNROUTED_FILES


def load_patterns(root: Path | None = None) -> tuple[list[Pattern], list[tuple[Path, str]]]:
    """Every pattern under ``patterns/``, and the files that could not be read."""
    root = root or REPO_ROOT
    directory = root / PATTERNS_DIR
    patterns: list[Pattern] = []
    errors: list[tuple[Path, str]] = []
    if not directory.is_dir():
        return patterns, errors
    for path in sorted(directory.rglob("*.md")):
        if not is_pattern_file(path, root):
            continue
        try:
            patterns.append(Pattern(read_doc(path, "pattern")))
        except (DocError, OSError) as exc:
            errors.append((path, str(exc)))
    return patterns, errors


def find_pattern(pattern_id: str, root: Path | None = None) -> Pattern:
    patterns, errors = load_patterns(root)
    for pattern in patterns:
        if pattern.id == pattern_id:
            return pattern
    for path, message in errors:
        if path.stem == pattern_id.split(".")[-1]:
            raise DocError(f"{path} could not be read: {message}")
    known = ", ".join(sorted(p.id for p in patterns)) or "none"
    raise DocError(f"no pattern with id {pattern_id!r}. Known: {known}.")


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

    def table_by_section(self) -> dict[str, str]:
        """Every name a `(SECTION, key)` mark may use, folded to its table code.

        A mark names its table either by the catalogue name or by the code, so
        both forms are indexed here rather than in each caller.
        """
        index: dict[str, str] = {}
        for code, doc in self.tables.items():
            index[normalise_key(str(doc.fm.get("name", "")))] = code
            index[normalise_key(code)] = code
        index.pop("", None)
        return index

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


def resolve_entry(rows: list[dict[str, str]], key: str) -> dict[str, str] | None:
    """The row a `(SECTION, key)` mark names, or ``None``.

    A mark keys a row either by its entry ID or by the leading text of one of
    its cells, which is how `(BESTIARY, Fen-wight)` reaches the row whose entry
    opens with that name. Validation asks whether this returns a row and the
    build asks which row it is, so the rule lives here rather than in either.
    """
    want = normalise_key(key)
    if not want:
        return None
    for row in rows:
        if normalise_key(row.get("ID", "")) == want:
            return row
        for header, value in row.items():
            if header == "ID":
                continue
            lead = re.split(r"[.,:;\u2014\u2013(]", value, maxsplit=1)[0]
            if normalise_key(lead) == want:
                return row
    return None


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
