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
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import kdl
import tables as tb

ROOT = Path(__file__).resolve().parent.parent
SETTING = ROOT / "setting"

maps_fit_site, maps_fit_pdf = "720x560px", "110x150mm"
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
    fields: list[tuple[str, str]]  # per a rating schema's seed and brief; `- ` items one per line
    tables: list[tuple[str, list[tuple[int, str]]]]
    locations: dict[int, Location] = field(default_factory=dict)

@dataclass
class Entry:
    title: str
    fields: list[tuple[str, str]]     # (label, value), the schema's order, empty values left out


@dataclass
class SettingTable:
    """One table of Setting_Schema.md, read through the schema: what a page and the PDF
    both render, so neither holds a field list of its own."""
    name: str
    kind: str                         # entry, roll or doc
    members: list                     # tables.Member, in the schema's order
    entries: list[Entry]
    heading: str = ""                 # the file's first line
    intro: str = ""                   # prose between that line and the first entry

    @property
    def slug(self) -> str:
        return slugify(self.name)

    @property
    def page(self) -> str:
        """Tables whose names differ only by a numeral share a page: Treasure I-V."""
        return slugify(re.sub(r" [IVX]+$", "", self.name))


@dataclass
class ProseFile:
    """A setting file no table describes, such as Procedures.md."""
    slug: str
    title: str
    text: str


@dataclass
class Setting:
    name: str = ""
    tagline: str = ""
    outline: str = ""
    tables: list[SettingTable] = field(default_factory=list)
    prose: list[ProseFile] = field(default_factory=list)
    regions: dict[str, Region] = field(default_factory=dict)
    region_order: list[str] = field(default_factory=list)
    top_connections: str = ""

    # lookup helpers, filled in after parsing
    all_locations: dict[str, Location] = field(default_factory=dict)

    def table(self, name: str) -> SettingTable | None:
        return next((t for t in self.tables if t.name == name), None)

    def pages(self) -> dict[str, list[SettingTable]]:
        """Page slug -> its tables, in schema order."""
        out: dict[str, list[SettingTable]] = {}
        for t in self.tables:
            out.setdefault(t.page, []).append(t)
        return out

    def entry_titles(self, name: str) -> set[str]:
        t = self.table(name)
        return {e.title for e in t.entries} if t else set()


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# The two generic shapes every setting-level table-like file takes. A table file is `## [Name]` headings over pipe tables;
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
    for i, raw in enumerate(path.read_text().splitlines() if path.exists() else [], 1):
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


def read_records(path: Path, level: int = 3) -> list[Record]:
    """Every `### [Name]` record in a file (`## ` at level 2); a line that opens no field
    continues the field above it, since every setting/ file is hard-wrapped. A `- ` item
    stays a line of its own."""
    out: list[Record] = []
    cur = None
    head = "#" * level + " "
    for i, raw in enumerate(path.read_text().splitlines() if path.exists() else [], 1):
        s = raw.strip()
        if s.startswith(head):
            cur = Record(s[len(head):].strip(), [], i)
            out.append(cur)
            continue
        if not s or s.startswith("#") or cur is None:
            continue
        m = _FIELD_RE.match(s)
        if m:
            cur.fields.append((m.group(1).strip(), m.group(2).strip()))
        elif cur.fields:
            label, val = cur.fields[-1]
            cur.fields[-1] = (label, (val + ("\n" if s.startswith("- ") else " ") + s).strip())
    return out


LOC_CODE_TOKEN_RE = re.compile(r"\b[A-Z]+\.\d+\b")


def parse_setting() -> tuple[str, str, str]:
    path = SETTING / "Setting.md"
    lines = [l for l in (path.read_text().splitlines() if path.exists() else [])
             if l.strip() and not l.startswith("Form:")]
    if not lines:
        return "", "", ""
    name = lines[0].strip()
    rest = lines[1:]
    tagline = ""
    if rest and not rest[0].strip().startswith("*"):
        tagline, rest = rest[0].strip(), rest[1:]
    outline = " ".join(l.strip() for l in rest).strip()
    outline = outline.strip("*").strip()
    return name, tagline, outline



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


_SCHEMA = None


def schema():
    """patterns/ read once: what every page and the PDF are drawn from."""
    global _SCHEMA
    if _SCHEMA is None:
        _SCHEMA = tb.Schema()
    return _SCHEMA


def region_labels() -> list[str]:
    """Every field of any rating's seed and brief, in the order they render. `Tables` is
    drawn separately, as roll tables."""
    out: list[str] = []
    for f in schema().folders.values():
        for m in f.seed + f.brief:
            if m.name != "Tables" and m.name not in out:
                out.append(m.name)
    return out


TABLE_HEAD_RE = re.compile(r"^(?:d\d+\s+\S|[A-Z][^.]*[^.\s]$)")


def is_table_head(line: str, prev: str | None) -> bool:
    """A line opening a table: `d6 Name` for a rolled one, else a name with no full stop,
    which follows a finished row rather than a wrapped one."""
    if re.match(r"^\d+[.)]\s", line):
        return False
    if re.match(r"^d\d+\s+\S", line):
        return True
    return bool(TABLE_HEAD_RE.match(line)) and (not prev or prev.rstrip()[-1] in ".!?\")")


def _field_text(block: list[str]) -> str:
    """A field's lines, rejoined: `- ` items stay one per line, each prose paragraph is
    one line."""
    items: list[str] = []
    prose: list[list[str]] = [[]]
    for raw in block:
        line = raw.strip()
        if not line:
            if prose[-1]:
                prose.append([])
        elif line.startswith("- "):
            items.append(line)
        elif items:
            items[-1] += " " + line
        else:
            prose[-1].append(line)
    return "\n".join([" ".join(p) for p in prose if p] + items).strip()


def parse_field(lines: list[str], label: str) -> str:
    """One seed or brief field's text, as the site reads it."""
    fields: list[tuple[str, str]] = []
    _parse_region_fields(lines, fields, [])
    return dict(fields).get(label, "")


def parse_region_overview(code: str, gaz: dict) -> Region:
    """The region's seed, then its brief where it exists, as one run sheet."""
    fields: list[tuple[str, str]] = []
    tables: list[tuple[str, list[tuple[int, str]]]] = []
    seed = SETTING / "region" / f"{code}.md"
    brief = SETTING / "region" / code / "Brief.md"
    if seed.exists():
        _parse_region_fields(seed.read_text().splitlines()[1:], fields, tables)
    if brief.exists():
        _parse_region_fields(brief.read_text().splitlines(), fields, tables)
    info = gaz[code]
    return Region(
        code=code, name=info["name"], rating=info["rating"], die=info["die"], tags=info["tags"],
        gazetteer_blurb=info["blurb"], fields=fields, tables=tables,
    )


def _parse_region_fields(lines: list[str], fields: list, tables: list) -> None:
    i, n = 0, len(lines)
    while i < n:
        line = lines[i].strip()
        i += 1
        m = re.match(r"^([A-Za-z]+):\s*(.*)$", line) if line else None
        if not m:
            continue
        label, val = m.group(1), m.group(2)
        block = [val] if val.strip() else []
        while i < n and not re.match(r"^[A-Z][a-z]+:(?:\s|$)", lines[i]):
            block.append(lines[i])
            i += 1
        if label == "Tables":
            # Rows wrap like every other field, so rejoin before matching; a
            # table head opens the next table.
            rows: list[str] = []
            for raw in block:
                raw = raw.strip()
                if not raw:
                    continue
                if not rows or re.match(r"^\d+[.)]\s", raw) or is_table_head(raw, rows[-1]):
                    rows.append(raw)
                else:
                    rows[-1] += " " + raw
            for row in rows:
                rm = re.match(r"^(\d+)[.)]\s*(.+)$", row)
                if not rm:
                    tables.append((row, []))
                elif rm:
                    if not tables:
                        tables.append(("", []))
                    tables[-1][1].append((int(rm.group(1)), rm.group(2).strip()))
        elif label in region_labels():
            fields.append((label, _field_text(block)))


def field_html(text: str, render) -> str:
    """A region field: its prose as a paragraph, its `- ` items as a list."""
    prose = [l for l in text.split("\n") if l and not l.startswith("- ")]
    items = [l[2:] for l in text.split("\n") if l.startswith("- ")]
    out = "".join(f"<p>{render(p)}</p>" for p in prose)
    if items:
        out += "<ul>" + "".join(f"<li>{render(i)}</li>" for i in items) + "</ul>"
    return out


def parse_locations_gazetteer(region_code: str) -> dict[int, dict]:
    """`Locations.md`'s Location entries, keyed by location number."""
    path = SETTING / "region" / region_code / "Locations.md"
    try:
        entries = kdl.fenced(path.read_text()) if path.exists() else []
    except SyntaxError:
        entries = []
    out: dict[int, dict] = {}
    for n in entries:
        m = re.fullmatch(r"([A-Z]+)\.(\d+)", str(n.args[0])) if n.args else None
        if n.name == "Location" and m:
            out[int(m.group(2))] = {"name": n.props.get("name", ""),
                                    "weight": str(n.props.get("type", "")).lower() or None,
                                    "tags": n.props.get("tags", ""),
                                    "at": str(n.props.get("at", ""))}
    return out


# -- The plan --------------------------------------------------------------
#
# A location's `at` places it from its region's way in, and a Connection's orientation
# places the room it leads to from the room it leaves, so a region's plan is drawn from its
# tables alone: what the Layout says can be checked against it, two routes to one room
# must agree, and an artist starts from it.

COMPASS = ["north", "north-north-east", "north-east", "east-north-east",
           "east", "east-south-east", "south-east", "south-south-east",
           "south", "south-south-west", "south-west", "west-south-west",
           "west", "west-north-west", "north-west", "north-north-west"]
UNIT_YARDS = {"yard": 1, "yards": 1, "mile": 1760, "miles": 1760, "foot": 1 / 3, "feet": 1 / 3, "ft": 1 / 3}
AT_RE = re.compile(r"^(?P<point>[a-z-]+),\s*(?P<n>[\d,.]+)\s*(?P<unit>[a-z]+)(?:\s+(?P<level>up|down))?$")
OFFSET_RE = re.compile(r"^(?P<ns>[\d,.]+)\s*(?P<unit>[a-z]+)\s+(?P<nsd>north|south),\s*"
                       r"(?P<ew>[\d,.]+)\s+(?P<ewd>east|west)$")


def parse_at(at: str) -> tuple[float, float, int] | None:
    """An `at`, or a Connection's orientation, as yards east and north and levels up; None
    where it states no position."""
    at = at.strip().lower()
    num = lambda v: float(v.replace(",", ""))
    if at == "at the way in":
        return 0.0, 0.0, 0
    if (m := OFFSET_RE.match(at)) and m["unit"] in UNIT_YARDS:
        k = UNIT_YARDS[m["unit"]]
        return (num(m["ew"]) * k * (1 if m["ewd"] == "east" else -1),
                num(m["ns"]) * k * (1 if m["nsd"] == "north" else -1), 0)
    m = AT_RE.match(at)
    if not m or m["point"] not in COMPASS or m["unit"] not in UNIT_YARDS:
        return None
    d = num(m["n"]) * UNIT_YARDS[m["unit"]]
    a = math.radians(COMPASS.index(m["point"]) * 22.5)
    return d * math.sin(a), d * math.cos(a), {"up": 1, "down": -1}.get(m["level"], 0)


def positions(code: str) -> tuple[dict[str, tuple[float, float, int]], list[tuple[str, str, float]]]:
    """Each location's place, from its `at` where the region's locations have one, else by
    walking the Connections out from the room an entrance opens into; and each pair of
    rooms two routes place apart, with the yards between."""
    locs = parse_locations_gazetteer(code)
    inside = {f"{code}.{n}" for n in locs}
    pos = {c: xy for c in inside if (xy := parse_at(locs[int(c.split(".")[1])]["at"]))}
    if pos:
        return pos, []
    path = SETTING / "region" / code / "Connections.md"
    try:
        nodes = kdl.fenced(path.read_text()) if path.exists() else []
    except SyntaxError:
        nodes = []
    ways = [(str(n.args[0]), str(n.props["to"]), parse_at(str(n.props.get("orientation", ""))))
            for n in nodes if n.args and "to" in n.props]
    order = sorted(inside, key=lambda c: int(c.split(".")[1]))
    start = next((a for a, b, _ in ways if a in inside and b not in inside), order[0] if order else None)
    if start is None:
        return {}, []
    pos = {start: (0.0, 0.0, 0)}
    grew = True
    while grew:
        grew = False
        for a, b, o in ways:
            if a in pos and b in inside and b not in pos and o:
                pos[b] = (pos[a][0] + o[0], pos[a][1] + o[1], pos[a][2] + o[2])
                grew = True
    apart = {}
    for a, b, o in ways:
        if a in pos and b in pos and o:
            gap = math.dist((pos[a][0] + o[0], pos[a][1] + o[1]), pos[b][:2])
            if gap > max(10 / 3, 0.1 * math.hypot(*o[:2])):
                apart[tuple(sorted((a, b)))] = gap
    return pos, [(a, b, gap) for (a, b), gap in sorted(apart.items())]


def route_stops(code: str) -> dict[str, list[tuple[str, tuple[float, float, int] | None, str, str]]]:
    """Each Route's stops in order: its feature, its place, where its path leads, and its `at`."""
    path = SETTING / "region" / code / "Stops.md"
    try:
        nodes = kdl.fenced(path.read_text()) if path.exists() else []
    except SyntaxError:
        nodes = []
    out: dict[str, list] = {}
    for n in nodes:
        if n.name == "Stop" and n.args:
            at = str(n.props.get("at", ""))
            out.setdefault(str(n.args[0]), []).append(
                (str(n.props.get("feature", "")), parse_at(at), str(n.props.get("to", "")), at))
    return out


def _nice(x: float) -> float:
    """The round length nearest below x: 1, 2 or 5 times a power of ten."""
    p = 10 ** math.floor(math.log10(x))
    return max(f * p for f in (1, 2, 5) if f * p <= x)


def _offset(x: float, y: float, level: int, feet: bool) -> str:
    """A place as how far north or south, then east or west, of the way in."""
    k, unit = (3, "feet") if feet else (1, "yards")
    parts = [f"{abs(v) * k:,.0f} {unit if not i else ''}".strip() + f" {d}"
             for i, (v, d) in enumerate(((y, "north" if y >= 0 else "south"), (x, "east" if x >= 0 else "west")))
             if round(abs(v) * k)]
    return (", ".join(parts) or "at the way in") + (f", {abs(level)} level{'s' * (abs(level) > 1)} "
                                                     f"{'up' if level > 0 else 'down'}" if level else "")


def _figure(svg: str | None, caption: str) -> str:
    return f'<figure class="diagram plan-figure">{svg}<figcaption>{html.escape(caption)}</figcaption></figure>' if svg else ""


def sheets_html(fit: str) -> str:
    """Every terrain sheet whole: the play map."""
    import maps
    return "".join(_figure(maps.sheet_svg(f.stem, fit), f"{f.stem}, drawn from the setting's tables")
                   for f in sorted(SETTING.glob("*.json")))


def cut_html(code: str, num: int, fit: str) -> str:
    """A location's cut of its block's or its sheet's map."""
    import maps
    return _figure(maps.cut_svg(f"{code}.{num}", maps.world_for(SETTING), fit), f"{code}.{num} and its surroundings")


def drawn_html(code: str, fit: str) -> str:
    """A region's map, or a DANGEROUS region's block maps, drawn from its tables by artgen."""
    import maps
    world = maps.world_for(SETTING)
    region = world.regions.get(code)
    if region is None:
        return ""
    blocks = maps.blocks_of(region)
    if blocks:
        return "".join(_figure(maps.block_svg(code, bid, fit), f"{bid} {b.props.get('name', '')}".strip())
                       for bid, b in blocks.items())
    return _figure(maps.region_svg(code, fit), f"{code}, cropped from its sheet")


def map_labels() -> list[str]:
    """The label of each map a build must show: every sheet, every block, every region on a sheet."""
    import maps
    world = maps.world_for(SETTING)
    out = [f"Sheet {f.stem}" for f in sorted(SETTING.glob("*.json"))]
    for code, r in world.regions.items():
        out += [f"Map of {bid}" for bid in maps.blocks_of(r) if (r.dir / f"{bid}.json").exists()]
    return out + [f"Map of region {c}" for c in maps.sheet_rows()]


def plan_html(code: str, name: str, fit: str = "720x560px") -> str:
    """The region's locations drawn where their tables place them, north up, with a scale
    bar, and the same places as text for a reader who cannot see the drawing."""
    if drawn := drawn_html(code, fit):
        return drawn
    locs = parse_locations_gazetteer(code)
    pos, _ = positions(code)
    if len(pos) < 2:
        return ""
    by_at = any(parse_at(l["at"]) for l in locs.values())
    routes = route_stops(code)
    every = list(pos.values()) + [xy for ss in routes.values() for _, xy, _, _ in ss if xy]
    xs, ys = [p[0] for p in every], [p[1] for p in every]
    span = max(max(xs) - min(xs), max(ys) - min(ys)) or 1
    feet = span * 3 < 600
    pad, size = span * 0.12, 340                   # drawn at its own size, so text reads the same in every plan
    k = size / (span + 2 * pad)
    w = (max(xs) - min(xs) + 2 * pad) * k + 120    # room for the labels east of the last point
    h = (max(ys) - min(ys) + 2 * pad) * k + 40
    px = lambda x: (x - min(xs) + pad) * k
    py = lambda y: (max(ys) - y + pad) * k
    points: dict[tuple[float, float], list[str]] = {}   # one label for places closer than a dot's width
    for c in sorted(pos, key=lambda c: (pos[c][:2] != (0, 0), int(c.split(".")[1]))):
        x, y, level = pos[c]
        at = next((p for p in points if math.dist((px(p[0]), py(p[1])), (px(x), py(y))) < 10), (x, y))
        points.setdefault(at, []).append(c)
    tag = lambda c: c + (f" ({'+' if pos[c][2] > 0 else ''}{pos[c][2]})" if pos[c][2] else "")
    if feet:
        bar_ft = _nice(span)                       # a third of the span, in feet
        bar, label = bar_ft / 3, f"{bar_ft:g} feet"
    elif span / 3 >= 880:
        bar_mi = _nice(span / 3 / 1760)
        bar, label = bar_mi * 1760, f"{bar_mi:g} mile{'s' * (bar_mi != 1)}"
    else:
        bar = _nice(span / 3)
        label = f"{bar:g} yards"
    place = lambda c: (locs[int(c.split(".")[1])]["at"] if by_at else _offset(*pos[c], feet))
    text = [(c, locs[int(c.split(".")[1])]["name"], place(c))
            for c in sorted(pos, key=lambda c: int(c.split(".")[1]))]
    tid, did = f"plan-{code}-title", f"plan-{code}-desc"
    out = [f'<svg class="plan" width="{w:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-labelledby="{tid} {did}" '
           f'font-family="inherit" font-size="13" fill="currentColor" stroke="currentColor">',
           f'<title id="{tid}">Plan of {html.escape(code)} {html.escape(name)}, drawn from its tables</title>',
           f'<desc id="{did}">North is up. The way in is ringed; a number after a code is the levels '
           f'above or below it; a dashed line is a route through its stops, each a numbered square. '
           + "; ".join(f"{c}: {html.escape(t)}" for c, _, t in text) + ".</desc>"]
    for c, ss in routes.items():                   # a route is a line through its stops, in order
        line = " ".join(f"{px(xy[0]):.1f},{py(xy[1]):.1f}" for _, xy, _, _ in ss if xy)
        out.append(f'<polyline points="{line}" fill="none" stroke-width="1.5" stroke-dasharray="6 4"/>'
                   + "".join(f'<rect x="{px(xy[0]) - 3:.1f}" y="{py(xy[1]) - 3:.1f}" width="6" height="6" '
                             f'fill="none" stroke-width="1.5"/>' for _, xy, _, _ in ss if xy))
    taken = [(px(p[0]) - 4, py(p[1]) - 4, px(p[0]) + 4, py(p[1]) + 4) for p in every]  # dots, then labels
    spots = [(8, -6, "start"), (8, 15, "start"), (-8, -6, "end"), (-8, 15, "end"), (0, -10, "middle"),
             (0, 22, "middle"), (8, -20, "start"), (8, 29, "start"), (-8, -20, "end"), (-8, 29, "end")]

    def spot(x: float, y: float, text_: str) -> tuple[int, int, str]:
        """The first place beside a point where its label covers no dot and no other label."""
        lw = 7 * len(text_)
        left = {"start": 0, "middle": lw / 2, "end": lw}
        box = lambda dx, dy, a: (px(x) + dx - left[a], py(y) + dy - 11, px(x) + dx - left[a] + lw, py(y) + dy + 2)
        free = lambda b: all(b[2] <= t[0] or b[0] >= t[2] or b[3] <= t[1] or b[1] >= t[3] for t in taken)
        dx, dy, anchor = next((s for s in spots if free(box(*s))), spots[0])
        taken.append(box(dx, dy, anchor))
        return dx, dy, anchor

    for (x, y), cs in points.items():
        text_ = ", ".join(tag(c) for c in cs)
        dx, dy, anchor = spot(x, y, text_)
        ring = '<circle r="9" fill="none" stroke-width="1.5"/>' if (x, y) == (0, 0) else ""
        dots = "".join(f'<circle cx="{px(pos[c][0]) - px(x):.1f}" cy="{py(pos[c][1]) - py(y):.1f}" r="4" stroke="none"/>'
                       for c in cs)
        out.append(f'<g transform="translate({px(x):.1f} {py(y):.1f})">{ring}{dots}'
                   f'<text x="{dx}" y="{dy}" text-anchor="{anchor}" stroke="none">{text_}</text></g>')
    for ss in routes.values():                      # each stop numbered in the route's order
        for i, (_, xy, _, _) in enumerate(ss, 1):
            if xy:
                dx, dy, anchor = spot(xy[0], xy[1], str(i))
                out.append(f'<text x="{px(xy[0]) + dx:.1f}" y="{py(xy[1]) + dy:.1f}" text-anchor="{anchor}" '
                           f'font-size="11" stroke="none">{i}</text>')
    y0 = h - 22
    out.append(f'<g stroke-width="2"><line x1="12" y1="{y0}" x2="{12 + bar * k:.1f}" y2="{y0}"/>'
               f'<line x1="12" y1="{y0 - 5}" x2="12" y2="{y0 + 5}"/>'
               f'<line x1="{12 + bar * k:.1f}" y1="{y0 - 5}" x2="{12 + bar * k:.1f}" y2="{y0 + 5}"/></g>'
               f'<text x="12" y="{y0 + 18}" stroke="none">{label}</text>'
               f'<g transform="translate({w - 20:.0f} 24)"><path d="M0 -14 L6 6 L0 2 L-6 6 Z" stroke="none"/>'
               f'<text x="0" y="22" text-anchor="middle" stroke="none">N</text></g></svg>')
    stop_rows = lambda c: "".join(f"<li>{html.escape(f)} - {html.escape(at)}"
                                  f"{', leads to ' + html.escape(to) if to else ''}</li>"
                                  for f, _, to, at in routes.get(c, []))
    rows = "".join(f"<li>{c} {html.escape(n)} - {html.escape(t)}"
                   + (f"<ol>{stop_rows(c)}</ol>" if c in routes else "") + "</li>" for c, n, t in text)
    how = ("at its compass point and distance from the way in" if by_at
           else "placed by walking its connections from the entrance")
    return (f'<figure class="diagram plan-figure">{"".join(out)}'
            f'<figcaption>Each location {how}.</figcaption>'
            f'<details><summary>Positions as text</summary><ul>{rows}</ul></details></figure>')


LOC_HEADER_RE = re.compile(r'^([A-Z]+)\.(\d+) \*\*(.+?)\*\*(?: \(([^)]+)\))? - \*(.+)\*\s*$')
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
    """Canonical HTML id for a link target - shared by the multi-page site and the
    single-page PDF, where every target lives in one document."""
    if kind == "location":
        region, num = args
        return f"loc-{region}-{num}"
    if kind == "region":
        (code,) = args
        return f"region-{code}"
    if kind == "entry":
        table, title = args
        return f"{slugify(table)}-{slugify(title)}"
    if kind == "table":
        (name,) = args
        return slugify(name)
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

def _intro(path: Path) -> tuple[str, str]:
    """A file's first line, then the prose between it and its first heading or table."""
    lines = path.read_text().splitlines()
    head, intro = (lines[0].strip() if lines else ""), []
    for raw in lines[1:]:
        if raw.lstrip().startswith(("#", "|")):
            break
        intro.append(raw.strip())
    return head, " ".join(" ".join(intro).split())


def load_tables() -> list[SettingTable]:
    """Every table of Setting_Schema.md whose file exists, in the schema's order."""
    sch = schema()
    out = []
    for name, fields in sch.fields.items():
        entries = tb.setting_entries(sch, name)
        if entries is None:
            continue
        path = ROOT / sch.tables[name][1]
        head, intro = _intro(path)
        known = [m.name for m in fields]
        rows = []
        for title, _line, values in entries:
            values.pop("", None)
            extra = [k for k in values if k not in known]
            rows.append(Entry(title, [(k, values[k].strip()) for k in known + extra
                                      if values.get(k, "").strip()]))
        out.append(SettingTable(name, sch.tables[name][0], fields, rows, head, intro))
    return out


def load_prose() -> list[ProseFile]:
    """Setting files no table claims, beyond Setting.md itself."""
    claimed = {ROOT / f for _, f in schema().tables.values()} | {SETTING / "Setting.md"}
    return [ProseFile(slugify(p.stem), (p.read_text().splitlines() or [p.stem])[0].strip(),
                      p.read_text().split("\n", 1)[-1])
            for p in sorted(SETTING.glob("*.md")) if p not in claimed]


def load_setting() -> Setting:
    s = Setting()
    s.name, s.tagline, s.outline = parse_setting()
    s.tables = load_tables()
    s.prose = load_prose()
    s.top_connections = load_mmd(SETTING / "region" / "Connections.mmd")

    gaz = parse_regions_gazetteer()
    s.region_order = list(gaz.keys())
    for code in s.region_order:
        region = parse_region_overview(code, gaz)
        loc_stubs = parse_locations_gazetteer(code)
        for num in sorted(loc_stubs):
            if not (SETTING / "region" / code / f"{num}.md").exists():
                continue
            loc = parse_location_file(code, num)
            region.locations[num] = loc
            s.all_locations[loc.code] = loc
        s.regions[code] = region
    return s


# ---------------------------------------------------------------------------
# Inline rendering: markdown-ish text -> HTML with auto-linking
# ---------------------------------------------------------------------------

ROLL_CITE_RE = re.compile(r'\(([^(),]+),\s*(d\d+)\)')
LOC_CODE_RE = re.compile(r'\b([A-Z]{1,2})\.(\d+)\b')
REGION_PAREN_RE = re.compile(r'\(([A-Z]{1,2})\)')
BESTIARY_CITE_RE = re.compile(r'\(([^()]*?),\s*Bestiary\s*:\s*([^()]+)\)')
CODE_SPAN_RE = re.compile(r'`([^`]+)`')

_TOK_OPEN, _TOK_CLOSE = "", ""


def cite_attrs(kind: str, table: str, title: str = "", die: str = "", count: str = "") -> str:
    """The attributes that let the site open a citation as a box below it (see app.js)."""
    data = {"cite": kind, "table": table, "title": title, "die": die, "count": count}
    return ' class="cite"' + "".join(f' data-{k}="{html.escape(v)}"' for k, v in data.items() if v)


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
        # `(Table: Title)` for an entry table, by its name or the name less a final "s";
        # `(Table, dN)` for a roll table, by its name.
        cites = {}
        for t in setting.tables:
            if t.kind == "roll":
                continue
            cites[t.name.lower()] = t
            if t.name.endswith("s"):
                cites[t.name[:-1].lower()] = t

        def cite_sub(m):
            t = cites.get(m.group(1).strip().lower())
            title = m.group(2).strip()
            if t and any(e.title == title for e in t.entries):
                href = resolver.href("entry", t.name, title, current_page)
                return protect(f"({html.escape(m.group(1), quote=False)}: <a href=\"{href}\"{cite_attrs('entry', t.name, title)}>"
                               f"{html.escape(title, quote=False)}</a>)")
            return m.group(0)
        s = re.sub(r'\(([A-Z][A-Za-z ]*):\s*([^)]+)\)', cite_sub, s)

        def roll_sub(m):
            t = setting.table(m.group(1).strip())
            if not t or t.kind != "roll":
                return m.group(0)
            href = resolver.href("table", t.name, current_page)
            return protect(f"(<a href=\"{href}\"{cite_attrs('roll', t.name, die=m.group(2)[1:])}>"
                           f"{html.escape(t.name, quote=False)}</a>, {m.group(2)})")
        s = ROLL_CITE_RE.sub(roll_sub, s)

        def bestiary_sub(m):
            prefix, title = m.group(1).strip(), m.group(2).strip()
            href = (resolver.href("entry", "Bestiary", title, current_page)
                    if title in setting.entry_titles("Bestiary") else None)
            if href:
                count = prefix.rsplit(",", 1)[-1].strip()
                attrs = cite_attrs("creature", "Bestiary", title, count=count if re.fullmatch(r"\d+(-\d+)?", count) else "")
                linked = f"<a href=\"{href}\"{attrs}>{html.escape(title, quote=False)}</a>"
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


# ---------------------------------------------------------------------------
# Setting tables and prose files, drawn the same way into the site and the PDF
# ---------------------------------------------------------------------------

def value_html(value: str, render) -> str:
    """A field's value: prose as a paragraph, `- ` lines as a list."""
    lines = value.split("\n")
    prose = [l for l in lines if not l.startswith("- ")]
    items = [l[2:] for l in lines if l.startswith("- ")]
    if not items:
        return render(value)
    out = f"<p>{render(' '.join(prose))}</p>" if prose else ""
    return out + "<ul>" + "".join(f"<li>{render(i)}</li>" for i in items) + "</ul>"


def entry_card(t: SettingTable, e: Entry, render) -> tuple[str, str]:
    """An entry's title line and its field rows: what a card and a citation's box both show."""
    enums = schema().setting_enums
    dice = next((m.name for m in t.members if m.type == "dice"), None)
    tag = next((m.name for m in t.members if m.type in enums and not m.is_list), None)
    f = dict(e.fields)
    shown = set()
    title = html.escape(e.title)
    if tag and len(f.get(tag, "").split()) <= 3 and tag in f:
        title += f' <span class="typetag">({html.escape(f[tag])})</span>'
        shown.add(tag)
    if dice and dice in f:
        title += f' <span class="ad">{html.escape(dice)}: {html.escape(f[dice])}</span>'
        shown.add(dice)
    rows = "".join(f"<tr><th>{html.escape(k)}</th><td>{value_html(v, render)}</td></tr>"
                   for k, v in e.fields if k not in shown)
    return title, rows


def cite_data(setting: Setting, render) -> dict:
    """What a citation opens, by table: an entry table's cards, a roll table's rows by number.
    `render` draws a field's text with links relative to the site root."""
    out: dict = {"entry": {}, "roll": {}}
    dice = lambda t: next((m.name for m in t.members if m.type == "dice"), None)
    for t in setting.tables:
        if t.kind == "roll":
            rows = {}
            for e in t.entries:
                f = dict(e.fields)
                body = "".join(f"<tr><th>{html.escape(k)}</th><td>{value_html(v, render)}</td></tr>"
                               for k, v in e.fields if k != "#")
                rows[f.get("#", "")] = f'<table class="kv-table">{body}</table>'
            out["roll"][t.name] = rows
        elif t.kind == "entry":
            cards = {}
            for e in t.entries:
                title, rows = entry_card(t, e, render)
                card = {"html": f'<h4>{title}</h4><table class="kv-table">{rows}</table>'}
                if d := dice(t):
                    card["ad"] = dict(e.fields).get(d, "")
                f = dict(e.fields)
                if f.get("Kind", "").startswith("table") and "\n- " in "\n" + f.get("Results", ""):
                    card["roll"] = True            # a procedure that is a table: the box can roll it
                cards[e.title] = card
            out["entry"][t.name] = cards
    return out


def table_html(t: SettingTable, render, title: str = "", heading: str = "h2") -> str:
    """One table, every field its schema names. A roll table is a table; an entry table
    is a card per entry, its dice and its first enum field set in the title. `title` heads a
    table sharing its page with others."""
    h = f"<{heading}>{html.escape(title)}</{heading}>" if title else ""
    intro = f'<p class="hint">{html.escape(t.intro)}</p>' if t.intro else ""
    if t.kind == "roll":
        cols = [m.name for m in t.members]
        head = "".join(f"<th>{html.escape(c)}</th>" for c in cols)
        rows = "".join(
            "<tr>" + "".join(
                f'<td class="num">{html.escape(dict(e.fields).get(c, ""))}</td>' if c == "#"
                else f"<td>{render(dict(e.fields).get(c, ''))}</td>" for c in cols) + "</tr>"
            for e in t.entries)
        return (f'<div id="{anchor_id("table", t.name)}">{h}{intro}<div class="table-scroll">'
                f'<table class="data-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody>'
                f'</table></div></div>')
    cards = []
    for e in t.entries:
        title, rows = entry_card(t, e, render)
        cards.append(f'<article class="registry-card" id="{anchor_id("entry", t.name, e.title)}">'
                     f'<h3>{title}</h3><table class="kv-table">{rows}</table></article>')
    empty = '<p class="hint">Nothing recorded yet.</p>' if not cards else ""
    return (f'<div id="{anchor_id("table", t.name)}">{h}{intro}{empty}'
            f'<div class="registry-list">{"".join(cards)}</div></div>')


def prose_html(text: str, render) -> str:
    """A prose setting file: `##` and `###` headings, `- ` items, pipe tables, paragraphs."""
    out, para, items, rows = [], [], [], []

    def flush():
        nonlocal para, items, rows
        if para:
            out.append(f"<p>{render(' '.join(para))}</p>")
        if items:
            out.append("<ul>" + "".join(f"<li>{render(i)}</li>" for i in items) + "</ul>")
        if rows:
            head, *body = rows
            out.append('<div class="table-scroll"><table class="data-table"><thead><tr>'
                       + "".join(f"<th>{html.escape(c)}</th>" for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{render(c)}</td>" for c in r) + "</tr>"
                                 for r in body) + "</tbody></table></div>")
        para, items, rows = [], [], []

    for raw in text.splitlines():
        line = raw.strip()
        if m := re.match(r"^(#{2,3}) (.+)$", line):
            flush()
            out.append(f"<h{len(m.group(1)) + 1}>{html.escape(m.group(2))}</h{len(m.group(1)) + 1}>")
        elif line.startswith("|"):
            if not (para or items):
                cells = split_row(line)
                if not all(_SEP_CELL_RE.match(c) for c in cells if c):
                    rows.append(cells)
        elif line.startswith("- "):
            if para or rows:
                flush()
            items.append(line[2:])
        elif not line:
            flush()
        elif items:
            items[-1] += " " + line
        else:
            para.append(line)
    flush()
    return "".join(out)


# -- keeping the display in step with the schema ----------------------------------------

def _plain(s: str) -> str:
    s = re.sub(r"</?(?:a|em|strong|code|span|b|i)\b[^>]*>", "", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return " ".join(html.unescape(s).replace("*", "").replace("`", "").lower().split())


def coverage(setting: Setting, text: str, has_page) -> list[str]:
    """What the schema and the files hold that a rendering does not show. `text` is every
    page together, or the whole PDF; `has_page(slug)` says whether a table's page exists."""
    shown = _plain(text)
    problems = []
    for t in setting.tables:
        if not has_page(t.page):
            problems.append(f"{t.name}: its file has no page")
        for e in t.entries:
            for label, value in e.fields:
                if _plain(value.replace("\n- ", " ").removeprefix("- ")) not in shown:
                    problems.append(f"{t.name} / {e.title} / {label}: not shown")
    for p in setting.prose:
        if not has_page(p.slug):
            problems.append(f"{p.title}: its file has no page")
    for code, r in setting.regions.items():
        rendered = {label for label, _ in r.fields}
        for path in (SETTING / "region" / f"{code}.md", SETTING / "region" / code / "Brief.md"):
            for label in re.findall(r"^([A-Z][a-z]+):", path.read_text(), re.M) if path.exists() else []:
                if label != "Tables" and label not in rendered:
                    problems.append(f"{path.relative_to(ROOT)}: {label} is not shown")
        for num in r.locations:
            if not has_page(f"region/{code}/{num}"):
                problems.append(f"{code}.{num}: no page")
    problems += [f"{label}: no map" for label in map_labels() if f'aria-label="{label}"' not in text]
    return problems
