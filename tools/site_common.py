"""Shared parsing and inline-rendering helpers for the setting web view / PDF builders.

Reads the same setting/ files tools/validate_setting.py validates, using
compatible parsing rules, and turns them into a plain data model plus an
inline markdown-ish -> HTML renderer that auto-links location codes,
Lore/Keys/Named Creature/Unique Treasure/Treasure citations, region
references, and Bestiary creature mentions.

Both tools/build_site.py (multi-page HTML) and tools/build_pdf.py (single
combined PDF) build on top of this module so the two outputs stay in sync.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETTING = ROOT / "setting"

ARTICLES = ("the ", "a ", "an ")


def strip_article(name: str) -> str:
    n = name.strip()
    low = n.lower()
    for a in ARTICLES:
        if low.startswith(a):
            return n[len(a):].strip()
    return n


def slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[’']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Location:
    region: str
    num: int
    name: str
    weight: str | None
    tags: str
    player_summary: str
    referee_notes: str
    features: list[tuple[str, str]]  # (label, body)
    exits_raw: str
    exits: list[tuple[str, str, str]]  # (approach text, code, name)

    @property
    def code(self) -> str:
        return f"{self.region}.{self.num}"


@dataclass
class Region:
    code: str
    name: str
    rating: str
    die: str
    tags: str
    gazetteer_blurb: str
    fields: list[tuple[str, str]]  # per patterns/region/*.md; `- ` items one per line
    tables: list[tuple[str, list[tuple[int, str]]]]
    locations: dict[int, Location] = field(default_factory=dict)


@dataclass
class RegistryEntry:
    title: str
    typetag: str
    body: str
    locations: list[str]


@dataclass
class Setting:
    name: str = ""
    tagline: str = ""
    outline: str = ""
    history: list[tuple[str, str, str]] = field(default_factory=list)
    truths: list[str] = field(default_factory=list)
    rumours: list[tuple[int, str, str, str]] = field(default_factory=list)
    bestiary: list[dict] = field(default_factory=list)
    factions: list[dict] = field(default_factory=list)
    faction_notes: list[str] = field(default_factory=list)
    treasure: dict[str, list[tuple[int, str, str, str]]] = field(default_factory=dict)
    lore: list[RegistryEntry] = field(default_factory=list)
    keys: list[RegistryEntry] = field(default_factory=list)
    named_creatures: list[RegistryEntry] = field(default_factory=list)
    unique_treasures: list[RegistryEntry] = field(default_factory=list)
    quests: list[RegistryEntry] = field(default_factory=list)
    regions: dict[str, Region] = field(default_factory=dict)
    region_order: list[str] = field(default_factory=list)
    top_connections: str = ""

    # lookup helpers, filled in after parsing
    all_locations: dict[str, Location] = field(default_factory=dict)
    bestiary_names: set = field(default_factory=set)


TREASURE_TITLES = {
    "I": "Treasure Table I - Scavenged Loot",
    "II": "Treasure Table II - Equipment and Armaments",
    "III": "Treasure Table III - Gems and Jewelry",
    "IV": "Treasure Table IV - Luxury and Trade Goods",
    "V": "Treasure Table V - Treasure Cache",
}
TREASURE_FILES = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------



def join_wrapped(lines: list[str]) -> list[str]:
    """Rejoin hard-wrapped source lines into logical lines.

    Every `setting/` file is hard-wrapped at ~95 columns, so a parser that
    matches line by line silently drops every continuation. A new logical line
    starts at a list bullet, a numbered row, a `Field:` label, or a table row;
    anything else continues the line above it. Callers that match their own
    entry shape pass `starts` instead - see `parse_region_overview`.
    """
    out: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if not out or _STARTS_LOGICAL_RE.match(line):
            out.append(line)
        else:
            out[-1] += " " + line
    return out


_STARTS_LOGICAL_RE = re.compile(
    r"^(?:[-*+]\s|\d+[.)]\s|\||#|```|[A-Z][A-Za-z ]{0,24}:\s)"
)



# ---------------------------------------------------------------------------
# The two generic shapes every table-like file takes (patterns/SPEC.md's How a
# Spec becomes tables). A table file is `## [Name]` headings over pipe tables;
# a record file is `### [Name]` headings over `Field: value` lines. Every
# parser below reads one of these two shapes rather than a format of its own.
# ---------------------------------------------------------------------------

@dataclass
class Table:
    name: str                 # the `## ` heading above it, or "" for none
    header: list[str]
    rows: list[list[str]]
    lines: list[int]          # 1-based source line of each row
    header_line: int

    def dicts(self) -> list[dict[str, str]]:
        return [dict(zip(self.header, r)) for r in self.rows]


_SEP_CELL_RE = re.compile(r"^:?-{2,}:?$")


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def read_tables(path: Path) -> list[Table]:
    """Every pipe table in a file, each under the nearest `## ` heading above it."""
    tables: list[Table] = []
    name, cur = "", None
    for i, raw in enumerate(path.read_text().splitlines(), 1):
        s = raw.strip()
        if s.startswith("## "):
            name, cur = s[3:].strip(), None
            continue
        if not s.startswith("|"):
            cur = None
            continue
        cells = split_row(s)
        if cur is None:
            cur = Table(name, cells, [], [], i)
            tables.append(cur)
        elif all(_SEP_CELL_RE.match(c) for c in cells if c):
            continue
        else:
            cur.rows.append(cells)
            cur.lines.append(i)
    return tables


def table_named(path: Path, name: str) -> Table | None:
    return next((t for t in read_tables(path) if t.name == name), None)


@dataclass
class Record:
    name: str
    fields: list[tuple[str, str]]
    line: int

    def get(self, label: str, default: str = "") -> str:
        return next((v for k, v in self.fields if k == label), default)

    def labels(self) -> list[str]:
        return [k for k, _ in self.fields]


_FIELD_RE = re.compile(r"^([A-Z][A-Za-z' ]{0,30}):\s*(.*)$")


def read_records(path: Path) -> list[Record]:
    """Every `### [Name]` record in a file; a line that opens no field continues
    the field above it, since every setting/ file is hard-wrapped."""
    out: list[Record] = []
    cur = None
    for i, raw in enumerate(path.read_text().splitlines(), 1):
        s = raw.strip()
        if s.startswith("### "):
            cur = Record(s[4:].strip(), [], i)
            out.append(cur)
            continue
        if not s or s.startswith("#") or cur is None:
            continue
        m = _FIELD_RE.match(s)
        if m:
            cur.fields.append((m.group(1).strip(), m.group(2).strip()))
        elif cur.fields:
            label, val = cur.fields[-1]
            cur.fields[-1] = (label, (val + " " + s).strip())
    return out


LOC_CODE_TOKEN_RE = re.compile(r"\b[A-Z]+\.\d+\b")


def parse_setting() -> tuple[str, str, str]:
    text = (SETTING / "Setting.md").read_text()
    lines = [l for l in text.splitlines() if l.strip()]
    name = lines[0].strip()
    rest = lines[1:]
    tagline = ""
    if rest and not rest[0].strip().startswith("*"):
        tagline, rest = rest[0].strip(), rest[1:]
    outline = " ".join(l.strip() for l in rest).strip()
    outline = outline.strip("*").strip()
    return name, tagline, outline


# Authoring markers that step 5c is meant to replace. They are not content and
# must not reach a reader; a build that still shows them is showing the build's
# own TODO list.
PENDING_MARKER_RE = re.compile(r"\s*[-\u2013\u2014]?\s*\[pending\s+\w+\]", re.IGNORECASE)


def _unpend(text: str) -> str:
    return PENDING_MARKER_RE.sub("", text).strip().rstrip("-\u2013\u2014 ").strip()


def parse_history() -> list[tuple[str, str, str]]:
    """Returns (when, event, left) per record. `left` carries its codes, since
    the Left line is a handle in the present rather than part of the event."""
    entries = []
    for r in read_records(SETTING / "History.md"):
        left = _unpend(r.get("Left"))
        codes = _unpend(r.get("Codes"))
        if left and codes:
            left = f"{left} - {codes}"
        entries.append((r.get("When"), _unpend(r.get("Event")), left))
    return entries


def parse_truths() -> list[str]:
    """One string per Truths.md row: the truth in bold, then its handle and codes."""
    t = table_named(SETTING / "Truths.md", "") or next(iter(read_tables(SETTING / "Truths.md")), None)
    out = []
    for d in (t.dicts() if t else []):
        line = f"**{d.get('Truth', '').strip()}**"
        handle, codes = _unpend(d.get("Handle", "")), _unpend(d.get("Codes", ""))
        if handle:
            line += f" Handle: {handle}" + (f" - {codes}" if codes else "")
        out.append(line)
    return out


def parse_table_rows(path: Path) -> list[list[str]]:
    text = path.read_text()
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or cells[0] in ("#",) or set(cells[0]) <= {"-"}:
            continue
        rows.append(cells)
    return rows


def parse_rumours() -> list[tuple[int, str, str, str]]:
    """Returns (number, rumour, mark, settled).

    `settled` is templates/setting/Rumours.md's Settled at column - where a party finds
    what confirms, denies or corrects the lead, and for a partial entry which
    half is false. It is referee-side exactly as the mark is, and empty for a
    table written before the column existed.
    """
    rows = parse_table_rows(SETTING / "Rumours.md")
    out = []
    for cells in rows:
        if len(cells) < 3:
            continue
        try:
            n = int(cells[0])
        except ValueError:
            continue
        out.append((n, cells[1], cells[2], cells[3] if len(cells) > 3 else ""))
    return out


def parse_treasure(roman: str) -> list[tuple[int, str, str, str]]:
    idx = TREASURE_FILES[roman]
    rows = parse_table_rows(SETTING / f"Treasure{idx}.md")
    out = []
    for cells in rows:
        if len(cells) < 4:
            continue
        try:
            n = int(cells[0])
        except ValueError:
            continue
        out.append((n, cells[1], cells[2], cells[3]))
    return out


# An entry may carry more than one Special line - several are expected at 8 AD
# and above - and each becomes its own field, so they render as separate
# abilities rather than one run-on paragraph.
BESTIARY_SUBFIELD_LABELS = ["Description", "Range", "Sign", "Disposition", "Special"]


def parse_bestiary() -> list[dict]:
    out = []
    for r in read_records(SETTING / "Bestiary.md"):
        ma = r.get("MA")
        out.append({
            "name": r.name, "kind": r.get("Type"),
            "ad": r.get("AD") + (f" [MA: {ma}]" if ma else ""),
            "description": r.get("Description"),
            "fields": [(k, v) for k, v in r.fields if k in BESTIARY_SUBFIELD_LABELS],
        })
    return out


def parse_factions() -> tuple[list[dict], list[str]]:
    """Factions.md's records. A note on how factions relate is not a record and
    has no place in the file, so the notes list is always empty."""
    out = []
    for r in read_records(SETTING / "Factions.md"):
        out.append({"name": r.name, "ad": r.get("AD"),
                    "fields": [(k, v) for k, v in r.fields if k != "AD"]})
    return out, []


REGISTRY_FILES = {
    "lore": "Lore.md",
    "keys": "Keys.md",
    "named_creatures": "NamedCreatures.md",
    "unique_treasures": "UniqueTreasures.md",
    "quests": "Quests.md",
}
# The pipe-table registries; the rest are record files. Per kind: the column or
# field giving the entry's type tag, and those naming its locations.
REGISTRY_TABLES = {"keys", "quests"}
REGISTRY_TYPETAG = {"lore": "Form", "keys": "Form", "named_creatures": "Type",
                    "unique_treasures": "", "quests": "Ask"}
REGISTRY_PLACES = {
    "lore": ("Found at",),
    "keys": ("Found at", "Opens"),
    "named_creatures": ("Appears at",),
    "unique_treasures": ("Found at",),
    "quests": ("Given at", "Resolved at"),
}


def parse_field_lines(text: str) -> list[tuple[str, str]]:
    """Parse "- Label: value" lines - an entry's body as parse_registry writes
    it - into ordered (label, value) pairs."""
    fields = []
    for l in text.splitlines():
        m = re.match(r"^-\s*([^:]+):\s*(.+)$", l.strip())
        if m:
            fields.append((m.group(1).strip(), m.group(2).strip()))
    return fields


def registry_entries(kind: str) -> list[tuple[str, list[tuple[str, str]], int]]:
    """(title, ordered fields, source line) per entry, from either shape."""
    path = SETTING / REGISTRY_FILES[kind]
    if kind in REGISTRY_TABLES:
        tables = read_tables(path)
        if not tables:
            return []
        t = tables[0]
        out = []
        for row, line in zip(t.rows, t.lines):
            pairs = list(zip(t.header, row))
            title = pairs[0][1] if pairs else ""
            out.append((title, pairs[1:], line))
        return out
    return [(r.name, r.fields, r.line) for r in read_records(path)]


def parse_registry(kind: str) -> list[RegistryEntry]:
    out = []
    tag_label = REGISTRY_TYPETAG[kind]
    places = REGISTRY_PLACES[kind]
    for title, fields, _line in registry_entries(kind):
        typetag = next((v for k, v in fields if k == tag_label), "") if tag_label else ""
        codes: list[str] = []
        for k, v in fields:
            if k in places:
                codes += [c for c in LOC_CODE_TOKEN_RE.findall(v) if c not in codes]
        body = "\n".join(f"- {k}: {v}" for k, v in fields
                         if k != tag_label and k not in places and v)
        out.append(RegistryEntry(title=title, typetag=typetag, body=body, locations=codes))
    return out


def parse_regions_gazetteer() -> dict[str, dict]:
    path = SETTING / "region" / "Regions.md"
    tables = read_tables(path)
    out: dict[str, dict] = {}
    for d in (tables[0].dicts() if tables else []):
        code = d.get("Code", "").strip()
        if not code:
            continue
        out[code] = {"name": d.get("Name", "").strip(), "rating": d.get("Rating", "").strip(),
                     "die": d.get("Die", "").strip(), "tags": "",
                     "gloss": d.get("Gloss", "").strip(), "blurb": d.get("Tag line", "").strip()}
    return out


# Follows templates/region/Region.md's own field order. Five of these are
# rating-specific - Architecture (DANGEROUS), People and Situation (SAFE),
# Terrain and Foraging (WILD) - and Factions is asked of every rating. All six
# were being parsed into nothing, so the rating-specific half of every Region
# Overview never reached the web view or the PDF.
REGION_FIELD_LABELS = [
    "Overview", "Approach", "People", "Services", "Law", "Terrain", "Conditions",
    "Inhabitants", "Alarm", "Places", "Situation", "Loot", "Secrets", "Compositions",
]
TABLE_HEAD_RE = re.compile(r"^d\d+\s+\S")


def _field_text(block: list[str]) -> str:
    """A field's lines, rejoined: `- ` items stay one per line, prose is one line."""
    items: list[str] = []
    prose: list[str] = []
    for raw in block:
        line = raw.strip()
        if line.startswith("- "):
            items.append(line)
        elif items:
            items[-1] += " " + line
        else:
            prose.append(line)
    return "\n".join(([" ".join(prose)] if prose else []) + items).strip()


def parse_region_overview(code: str, gaz: dict) -> Region:
    path = SETTING / "region" / f"{code}.md"
    lines = path.read_text().splitlines()
    fields: list[tuple[str, str]] = []
    tables: list[tuple[str, list[tuple[int, str]]]] = []
    i, n = 1, len(lines)
    while i < n:
        line = lines[i].strip()
        i += 1
        m = re.match(r"^([A-Za-z]+):\s*(.*)$", line) if line else None
        if not m:
            continue
        label, val = m.group(1), m.group(2)
        block = [val] if val.strip() else []
        while i < n and lines[i].strip() and not re.match(r"^[A-Z][a-z]+:\s", lines[i]):
            block.append(lines[i])
            i += 1
        if label == "Tables":
            # Rows wrap like every other field, so rejoin before matching; a
            # `d6 ...` line opens the next table.
            rows: list[str] = []
            for raw in block:
                raw = raw.strip()
                if not rows or re.match(r"^\d+[.)]\s", raw) or TABLE_HEAD_RE.match(raw):
                    rows.append(raw)
                else:
                    rows[-1] += " " + raw
            for row in rows:
                rm = re.match(r"^(\d+)[.)]\s*(.+)$", row)
                if TABLE_HEAD_RE.match(row) and not rm:
                    tables.append((row, []))
                elif rm:
                    if not tables:
                        tables.append(("", []))
                    tables[-1][1].append((int(rm.group(1)), rm.group(2).strip()))
        elif label in REGION_FIELD_LABELS:
            fields.append((label, _field_text(block)))
    info = gaz[code]
    return Region(
        code=code, name=info["name"], rating=info["rating"], die=info["die"], tags=info["tags"],
        gazetteer_blurb=info["blurb"], fields=fields, tables=tables,
    )


def field_html(text: str, render) -> str:
    """A region field: its prose as a paragraph, its `- ` items as a list."""
    prose = [l for l in text.split("\n") if l and not l.startswith("- ")]
    items = [l[2:] for l in text.split("\n") if l.startswith("- ")]
    out = "".join(f"<p>{render(p)}</p>" for p in prose)
    if items:
        out += "<ul>" + "".join(f"<li>{render(i)}</li>" for i in items) + "</ul>"
    return out


def parse_locations_gazetteer(region_code: str) -> dict[int, dict]:
    """`Locations.md`'s `## Location` table, keyed by location number."""
    t = table_named(SETTING / "region" / region_code / "Locations.md", "Location")
    out: dict[int, dict] = {}
    for d in (t.dicts() if t else []):
        m = re.fullmatch(r"([A-Z]+)\.(\d+)", d.get("Code", "").strip())
        if not m:
            continue
        out[int(m.group(2))] = {"name": d.get("Name", "").strip(),
                                "weight": d.get("Weight", "").strip() or None,
                                "tags": d.get("Tags", "").strip(),
                                "block": d.get("Block", "").strip()}
    return out


LOC_HEADER_RE = re.compile(r'^([A-Z]+)\.(\d+) \*\*(.+?)\*\*(?: \((low|medium|high|landmark|hidden|secret)\))? - \*(.+)\*\s*$')
FEATURE_RE = re.compile(r'^\*\*([^*]+):\*\*\s*(.*)$')
EXIT_DEST_RE = re.compile(r'^\s*([A-Z]+\.\d+)\s+(.*)$')


def parse_exits(exits_raw: str) -> list[tuple[str, str, str]]:
    """Split a comma-separated Exits line into (approach, code, name) triples.

    An approach description may itself contain commas (e.g. "low side door,
    salt-swollen"), so this can't just split on every comma - instead it
    splits on the unambiguous "->" markers and, for each destination segment,
    peels off "CODE Name" up to the *first* comma (location names don't
    contain commas), leaving the remainder as the next exit's approach text.
    """
    if not exits_raw.strip():
        return []
    segments = exits_raw.split("->")
    if len(segments) < 2:
        return []
    approaches = [segments[0].strip().strip(",").strip()]
    dests: list[tuple[str, str]] = []
    for seg in segments[1:]:
        m = EXIT_DEST_RE.match(seg)
        if not m:
            continue
        code, remainder = m.group(1), m.group(2)
        if "," in remainder:
            name, next_app = remainder.split(",", 1)
        else:
            name, next_app = remainder, ""
        dests.append((code, name.strip()))
        approaches.append(next_app.strip().strip(",").strip())
    return [(approaches[i], dests[i][0], dests[i][1]) for i in range(len(dests))]


def parse_location_file(region_code: str, num: int) -> Location:
    path = SETTING / "region" / region_code / f"{num}.md"
    lines = path.read_text().splitlines()
    m = LOC_HEADER_RE.match(lines[0].strip())
    _hcode, _hnum, name, weight, tags = m.groups()

    body = lines[1:]
    idx = 0
    while idx < len(body) and not body[idx].strip():
        idx += 1
    summary = body[idx].strip()
    idx += 1
    while idx < len(body) and not body[idx].strip():
        idx += 1
    notes = body[idx].strip().strip("*")
    idx += 1

    features = []
    exits_raw = ""
    for raw in body[idx:]:
        s = raw.strip()
        if not s:
            continue
        if s.startswith("**Exits:**"):
            exits_raw = s[len("**Exits:**"):].strip()
            continue
        fm = FEATURE_RE.match(s)
        if fm:
            features.append((fm.group(1).strip(), fm.group(2).strip()))

    exits = parse_exits(exits_raw)

    return Location(
        region=region_code, num=num, name=name.strip(), weight=weight, tags=tags.strip(),
        player_summary=summary, referee_notes=notes, features=features,
        exits_raw=exits_raw, exits=exits,
    )


NODE_RE = re.compile(r'(\w+)\["([A-Z]+(?:\.\d+)?) (.*?)"\]')
# Matches validate_setting.EDGE_RE, labelled edges included. Without the
# optional |label| group a vertical or gated edge - `D6 ---|vertical| D9` - is
# dropped silently, so the PDF's text edge list loses exactly the connections
# that carry the most information.
EDGE_RE = re.compile(
    r'(\w+)(?:\[[^\]]*\])?\s*(---|-\.-|-->)(?:\|([^|]*)\|)?\s*(\w+)(?:\[[^\]]*\])?')


def load_mmd(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def anchor_id(kind: str, *args) -> str:
    """Canonical HTML id for a link target - shared by the multi-page site
    (used on the registry/treasure/bestiary pages that hold several
    entries) and the single-page PDF (used for every target, since
    everything lives in one document there)."""
    if kind == "location":
        region, num = args
        return f"loc-{region}-{num}"
    if kind == "region":
        (code,) = args
        return f"region-{code}"
    if kind in ("lore", "keys", "named_creatures", "unique_treasures", "quests"):
        (title,) = args
        return f"{kind}-{slugify(title)}"
    if kind == "treasure":
        (roman,) = args
        return f"treasure-{roman}"
    if kind == "bestiary":
        (name,) = args
        return f"bestiary-{slugify(name)}"
    raise ValueError(f"unknown link kind {kind!r}")


def edge_label(code: str, setting: "Setting") -> str:
    if "." in code:
        loc = setting.all_locations.get(code)
        return f"{code} {loc.name}" if loc else code
    region = setting.regions.get(code)
    return f"{code} {region.name}" if region else code


def describe_edges(mmd_text: str, setting: "Setting") -> list[str]:
    """Human-readable connection lines for contexts (like a PDF) that can't
    render the mermaid graph itself."""
    lines = []
    for a, typ, label, b in mmd_edges_by_code(mmd_text):
        la, lb = edge_label(a, setting), edge_label(b, setting)
        note = f" [{label}]" if label else ""
        if typ == "---":
            lines.append(f"{la} — {lb}{note}")
        elif typ == "-.-":
            lines.append(f"{la} ⤳ {lb} (hidden){note}")
        elif typ == "-->":
            lines.append(f"{la} → {lb} (one-way){note}")
    return lines


def mmd_edges_by_code(text: str) -> list[tuple[str, str, str, str]]:
    """Return (code_a, edge_type, label, code_b) using the ["CODE Name"] node labels."""
    id_to_code: dict[str, str] = {}
    for m in NODE_RE.finditer(text):
        id_to_code[m.group(1)] = m.group(2)
    edges = []
    for raw_line in text.splitlines():
        line = raw_line.split("%%")[0]
        for m in EDGE_RE.finditer(line):
            a, typ, label, b = m.groups()
            ca, cb = id_to_code.get(a), id_to_code.get(b)
            if ca and cb:
                edges.append((ca, typ, (label or "").strip(), cb))
    return edges


# ---------------------------------------------------------------------------
# Top-level load
# ---------------------------------------------------------------------------

def load_setting() -> Setting:
    s = Setting()
    s.name, s.tagline, s.outline = parse_setting()
    s.history = parse_history()
    s.truths = parse_truths()
    s.rumours = parse_rumours()
    s.bestiary = parse_bestiary()
    s.factions, s.faction_notes = parse_factions()
    for roman in ("I", "II", "III", "IV", "V"):
        s.treasure[roman] = parse_treasure(roman)
    s.lore = parse_registry("lore")
    s.keys = parse_registry("keys")
    s.named_creatures = parse_registry("named_creatures")
    s.unique_treasures = parse_registry("unique_treasures")
    s.quests = parse_registry("quests")
    s.top_connections = load_mmd(SETTING / "region" / "Connections.mmd")

    gaz = parse_regions_gazetteer()
    s.region_order = list(gaz.keys())
    for code in s.region_order:
        region = parse_region_overview(code, gaz)
        loc_stubs = parse_locations_gazetteer(code)
        for num in sorted(loc_stubs):
            loc = parse_location_file(code, num)
            region.locations[num] = loc
            s.all_locations[loc.code] = loc
        s.regions[code] = region

    s.bestiary_names = {b["name"] for b in s.bestiary}
    return s


# ---------------------------------------------------------------------------
# Inline rendering: markdown-ish text -> HTML with auto-linking
# ---------------------------------------------------------------------------

CITE_PATTERNS = [
    ("lore", re.compile(r'\(Lore:\s*([^)]+)\)')),
    ("keys", re.compile(r'\(Keys:\s*([^)]+)\)')),
    ("named_creatures", re.compile(r'\(Named Creature:\s*([^)]+)\)')),
    ("unique_treasures", re.compile(r'\(Unique Treasure:\s*([^)]+)\)')),
    ("quests", re.compile(r'\(Quest:\s*([^)]+)\)')),
]
TREASURE_CITE_RE = re.compile(r'\(Treasure\s+([IVX]+),\s*d20\)')
LOC_CODE_RE = re.compile(r'\b([A-Z]{1,2})\.(\d+)\b')
REGION_PAREN_RE = re.compile(r'\(([A-Z]{1,2})\)')
BESTIARY_CITE_RE = re.compile(r'\(([^()]*?),\s*Bestiary\s*:\s*([^()]+)\)')
CODE_SPAN_RE = re.compile(r'`([^`]+)`')

_TOK_OPEN, _TOK_CLOSE = "", ""


class LinkResolver:
    """Resolves a (kind, *args) target into an href, relative to a given page."""

    def href(self, kind: str, *args) -> str | None:
        raise NotImplementedError


def render_inline(text: str, setting: Setting, resolver: LinkResolver, current_page: str,
                   skip_location: str | None = None, no_links: bool = False) -> str:
    """Render markdown-ish text to HTML with auto-linking.

    Pass no_links=True when this text will itself sit inside another <a> (a
    card or row that is already a whole-element link) - HTML forbids nested
    interactive elements, and browsers respond by silently closing the outer
    anchor early, breaking the surrounding layout. no_links keeps the
    bold/italic/code formatting but skips every substitution that would
    otherwise emit a link.
    """
    if not text:
        return ""
    tokens: list[str] = []

    def protect(html_piece: str) -> str:
        tokens.append(html_piece)
        return f"{_TOK_OPEN}{len(tokens) - 1}{_TOK_CLOSE}"

    s = html.escape(text, quote=False)

    def code_sub(m):
        return protect(f"<code>{m.group(1)}</code>")
    s = CODE_SPAN_RE.sub(code_sub, s)

    if not no_links:
        for kind, pattern in CITE_PATTERNS:
            label = {"lore": "Lore", "keys": "Keys", "named_creatures": "Named Creature",
                      "unique_treasures": "Unique Treasure", "quests": "Quest"}[kind]
            titles = {e.title for e in getattr(setting, kind)}

            def cite_sub(m, kind=kind, label=label, titles=titles):
                title = m.group(1).strip()
                href = resolver.href(kind, title, current_page) if title in titles else None
                if href:
                    return protect(f"({label}: <a href=\"{href}\">{html.escape(title, quote=False)}</a>)")
                return m.group(0)
            s = pattern.sub(cite_sub, s)

        def treasure_sub(m):
            roman = m.group(1)
            if roman not in TREASURE_TITLES:
                return m.group(0)
            href = resolver.href("treasure", roman, current_page)
            return protect(f"(<a href=\"{href}\">Treasure {roman}</a>, d20)")
        s = TREASURE_CITE_RE.sub(treasure_sub, s)

        def bestiary_sub(m):
            prefix, title = m.group(1).strip(), m.group(2).strip()
            href = resolver.href("bestiary", title, current_page) if title in setting.bestiary_names else None
            if href:
                linked = f"<a href=\"{href}\">{html.escape(title, quote=False)}</a>"
                return protect(f"({html.escape(prefix, quote=False)}, Bestiary: {linked})")
            return m.group(0)
        s = BESTIARY_CITE_RE.sub(bestiary_sub, s)

        def loc_sub(m):
            region, num = m.group(1), m.group(2)
            code = f"{region}.{num}"
            if code not in setting.all_locations or code == skip_location:
                return m.group(0)
            href = resolver.href("location", region, int(num), current_page)
            return protect(f"<a href=\"{href}\">{code}</a>")
        s = LOC_CODE_RE.sub(loc_sub, s)

        def region_paren_sub(m):
            code = m.group(1)
            if code not in setting.regions:
                return m.group(0)
            href = resolver.href("region", code, current_page)
            return protect(f"(<a href=\"{href}\">{code}</a>)")
        s = REGION_PAREN_RE.sub(region_paren_sub, s)

    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)

    def restore(m):
        return tokens[int(m.group(1))]
    s = re.sub(f"{_TOK_OPEN}(\\d+){_TOK_CLOSE}", restore, s)
    return s
