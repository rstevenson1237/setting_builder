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
    fields: list[tuple[str, str]]  # Overview/Ambiance/Layout/Features/Dangers/Creatures/Secrets/Treasure
    table_label: str
    table_rows: list[tuple[int, str]]
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
    tags: str = ""
    outline: str = ""
    history: list[tuple[str, str]] = field(default_factory=list)
    truths: list[str] = field(default_factory=list)
    rumours: list[tuple[int, str, str]] = field(default_factory=list)
    bestiary: list[dict] = field(default_factory=list)
    factions: list[dict] = field(default_factory=list)
    treasure: dict[str, list[tuple[int, str, str, str]]] = field(default_factory=dict)
    lore: list[RegistryEntry] = field(default_factory=list)
    keys: list[RegistryEntry] = field(default_factory=list)
    named_creatures: list[RegistryEntry] = field(default_factory=list)
    unique_treasures: list[RegistryEntry] = field(default_factory=list)
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

def parse_setting() -> tuple[str, str, str]:
    text = (SETTING / "Setting.md").read_text()
    lines = [l for l in text.splitlines() if l.strip()]
    m = re.match(r"^(.+?)\s+\*(.+)\*\s*$", lines[0].strip())
    name, tags = (m.group(1).strip(), m.group(2).strip()) if m else (lines[0].strip(), "")
    outline = " ".join(l.strip() for l in lines[1:]).strip()
    outline = outline.strip("*").strip()
    return name, tags, outline


def parse_history() -> list[tuple[str, str]]:
    text = (SETTING / "History.md").read_text()
    entries = []
    for line in text.splitlines()[1:]:
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(.+? ago)\s*[-–]\s*(.+)$", line)
        if m:
            entries.append((m.group(1).strip(), m.group(2).strip()))
        else:
            entries.append(("", line))
    return entries


def parse_truths() -> list[str]:
    text = (SETTING / "Truths.md").read_text()
    return [l.strip()[2:].strip() for l in text.splitlines() if l.strip().startswith("- ")]


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


def parse_rumours() -> list[tuple[int, str, str]]:
    rows = parse_table_rows(SETTING / "Rumours.md")
    out = []
    for cells in rows:
        if len(cells) < 3:
            continue
        try:
            n = int(cells[0])
        except ValueError:
            continue
        out.append((n, cells[1], cells[2]))
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


BESTIARY_HEADER_RE = re.compile(r"^(.+?)\s+\((.+?)\)\s*-\s*AD:\s*(.+)$")


def parse_bestiary() -> list[dict]:
    text = (SETTING / "Bestiary.md").read_text()
    blocks = re.split(r"\n\s*\n", text.strip())
    out = []
    for block in blocks[1:]:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        m = BESTIARY_HEADER_RE.match(lines[0])
        if not m:
            continue
        name, kind, ad = m.groups()
        desc = ""
        for l in lines[1:]:
            if l.lower().startswith("description:"):
                desc = l.split(":", 1)[1].strip()
        out.append({"name": name.strip(), "kind": kind.strip(), "ad": ad.strip(), "description": desc})
    return out


def parse_factions() -> list[dict]:
    text = (SETTING / "Factions.md").read_text()
    blocks = re.split(r"\n\s*\n", text.strip())
    out = []
    for block in blocks[1:]:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        m = re.match(r"^(.+?)\s*-\s*AD:\s*(.+)$", lines[0])
        name, ad = (m.group(1).strip(), m.group(2).strip()) if m else (lines[0], "")
        fields = []
        for l in lines[1:]:
            fm = re.match(r"^-\s*([^:]+):\s*(.+)$", l)
            if fm:
                fields.append((fm.group(1).strip(), fm.group(2).strip()))
        out.append({"name": name, "ad": ad, "fields": fields})
    return out


REGISTRY_MARKERS = {
    "lore": "found at",
    "keys": "found at",
    "named_creatures": "appears at",
    "unique_treasures": "found at",
}
REGISTRY_FILES = {
    "lore": "Lore.md",
    "keys": "Keys.md",
    "named_creatures": "NamedCreatures.md",
    "unique_treasures": "UniqueTreasures.md",
}


def parse_registry(kind: str) -> list[RegistryEntry]:
    path = SETTING / REGISTRY_FILES[kind]
    marker = REGISTRY_MARKERS[kind]
    full_marker = f" - {marker} "
    text = path.read_text()
    blocks = re.split(r"\n\s*\n", text.strip())
    out = []
    for block in blocks[1:]:
        lines = [l for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        head_line = lines[0].strip()
        if full_marker not in head_line:
            continue
        head, rest = head_line.split(full_marker, 1)
        tm = re.search(r"\(([^)]*)\)\s*$", head)
        typetag = tm.group(1) if tm else ""
        if kind == "named_creatures":
            title = head.split(" (")[0].strip()
        else:
            title = re.sub(r"\s*\(.*?\)\s*$", "", head).strip()
        codes = re.findall(r"[A-Z]+\.\d+", rest)
        body = "\n".join(l.strip() for l in lines[1:]).strip()
        out.append(RegistryEntry(title=title, typetag=typetag, body=body, locations=codes))
    return out


REGION_RE = re.compile(r'^([A-Z]+) (.+?) - (SAFE|WILD|DANGEROUS), (d\d+), \*(.+)\*\s*$')


def parse_regions_gazetteer() -> dict[str, dict]:
    path = SETTING / "region" / "Regions.md"
    lines = path.read_text().splitlines()
    out: dict[str, dict] = {}
    order: list[str] = []
    i, n = 0, len(lines)
    while i < n and not lines[i].strip():
        i += 1
    if i < n and lines[i].strip().lower().startswith("regional gazetteer"):
        i += 1
    while i < n:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        m = REGION_RE.match(line)
        if m:
            code, name, rating, die, tags = m.groups()
            blurb = ""
            if i + 1 < n and lines[i + 1].strip():
                blurb = lines[i + 1].strip()
                i += 1
            out[code] = {"name": name.strip(), "rating": rating, "die": die, "tags": tags.strip(), "blurb": blurb}
            order.append(code)
        i += 1
    return out


REGION_FIELD_LABELS = ["Overview", "Ambiance", "Layout", "Features", "Dangers", "Creatures", "Secrets", "Treasure"]


def parse_region_overview(code: str, gaz: dict) -> Region:
    path = SETTING / "region" / f"{code}.md"
    text = path.read_text()
    lines = text.splitlines()
    fields: list[tuple[str, str]] = []
    table_label = ""
    table_rows: list[tuple[int, str]] = []
    i = 1
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        m = re.match(r"^([A-Za-z]+):\s*(.*)$", line)
        if not m:
            continue
        label, val = m.group(1), m.group(2)
        if label == "Tables":
            table_label = val.strip()
            while i < n and lines[i].strip():
                rm = re.match(r"^(\d+)\.\s*(.+)$", lines[i].strip())
                if rm:
                    table_rows.append((int(rm.group(1)), rm.group(2).strip()))
                i += 1
        elif label in REGION_FIELD_LABELS:
            fields.append((label, val.strip()))
    info = gaz[code]
    return Region(
        code=code, name=info["name"], rating=info["rating"], die=info["die"], tags=info["tags"],
        gazetteer_blurb=info["blurb"], fields=fields, table_label=table_label, table_rows=table_rows,
    )


LOC_GAZ_RE = re.compile(r'^([A-Z]+)\.(\d+) (.+?)(?: \((low|medium|high)\))? - \*(.+)\*\s*$')


def parse_locations_gazetteer(region_code: str) -> dict[int, dict]:
    path = SETTING / "region" / region_code / "Locations.md"
    out: dict[int, dict] = {}
    for raw in path.read_text().splitlines():
        s = raw.strip()
        if not s or s.lower().startswith("locations of"):
            continue
        m = LOC_GAZ_RE.match(s)
        if not m:
            continue
        rcode, num_s, name, weight, tags = m.groups()
        out[int(num_s)] = {"name": name.strip(), "weight": weight, "tags": tags.strip()}
    return out


LOC_HEADER_RE = re.compile(r'^([A-Z]+)\.(\d+) \*\*(.+?)\*\*(?: \((low|medium|high)\))? - \*(.+)\*\s*$')
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
EDGE_RE = re.compile(r'(\w+)(?:\[[^\]]*\])?\s*(---|-\.-|-->)\s*(\w+)(?:\[[^\]]*\])?')


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
    if kind in ("lore", "keys", "named_creatures", "unique_treasures"):
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
    for a, typ, b in mmd_edges_by_code(mmd_text):
        la, lb = edge_label(a, setting), edge_label(b, setting)
        if typ == "---":
            lines.append(f"{la} — {lb}")
        elif typ == "-.-":
            lines.append(f"{la} ⤳ {lb} (hidden)")
        elif typ == "-->":
            lines.append(f"{la} → {lb} (one-way)")
    return lines


def mmd_edges_by_code(text: str) -> list[tuple[str, str, str]]:
    """Return (code_a, edge_type, code_b) using the ["CODE Name"] node labels."""
    id_to_code: dict[str, str] = {}
    for m in NODE_RE.finditer(text):
        id_to_code[m.group(1)] = m.group(2)
    edges = []
    for raw_line in text.splitlines():
        line = raw_line.split("%%")[0]
        for m in EDGE_RE.finditer(line):
            a, typ, b = m.groups()
            ca, cb = id_to_code.get(a), id_to_code.get(b)
            if ca and cb:
                edges.append((ca, typ, cb))
    return edges


# ---------------------------------------------------------------------------
# Top-level load
# ---------------------------------------------------------------------------

def load_setting() -> Setting:
    s = Setting()
    s.name, s.tags, s.outline = parse_setting()
    s.history = parse_history()
    s.truths = parse_truths()
    s.rumours = parse_rumours()
    s.bestiary = parse_bestiary()
    s.factions = parse_factions()
    for roman in ("I", "II", "III", "IV", "V"):
        s.treasure[roman] = parse_treasure(roman)
    s.lore = parse_registry("lore")
    s.keys = parse_registry("keys")
    s.named_creatures = parse_registry("named_creatures")
    s.unique_treasures = parse_registry("unique_treasures")
    s.top_connections = load_mmd(SETTING / "Connections.mmd")

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
]
TREASURE_CITE_RE = re.compile(r'\(Treasure\s+([IVX]+),\s*d20\)')
LOC_CODE_RE = re.compile(r'\b([A-Z]{1,2})\.(\d+)\b')
REGION_PAREN_RE = re.compile(r'\(([A-Z]{1,2})\)')
BESTIARY_MENTION_RE = re.compile(r"([A-Z][A-Za-z'\-]*(?:\s+[A-Z][A-Za-z'\-]*){0,3})\s*\(Bestiary\)")
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
                      "unique_treasures": "Unique Treasure"}[kind]
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
            words = m.group(1).split()
            # A leading determiner/number ("A Coastal Bandit", "Two Drowned Skeletons")
            # isn't part of the creature's own name - try shrinking from the left
            # until the remaining phrase (or its singular) matches a Bestiary entry.
            for start in range(len(words)):
                phrase = " ".join(words[start:])
                candidates = [phrase, phrase[:-1] if phrase.endswith("s") else None]
                found = next((c for c in candidates if c and c in setting.bestiary_names), None)
                if found:
                    prefix = html.escape(" ".join(words[:start]), quote=False)
                    prefix = f"{prefix} " if prefix else ""
                    href = resolver.href("bestiary", found, current_page)
                    linked = f"<a href=\"{href}\">{html.escape(phrase, quote=False)}</a>"
                    return protect(f"{prefix}{linked} (Bestiary)")
            return m.group(0)
        s = BESTIARY_MENTION_RE.sub(bestiary_sub, s)

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
