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

import kdl
import tables as tb
import templates as tp

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
    fields: list[tuple[str, str]]  # per its rating's brief; `- ` items one per line
    tables: list[tuple[str, list[tuple[int, str]]]]
    drawn: list[tuple[str, list[str]]] = field(default_factory=list)   # per its rating's drawn
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
    out: dict[str, dict] = {}
    for n in tb.gazetteer():
        if len(n.args) != 1:
            continue
        p = {k: str(v).strip() for k, v in n.props.items()}
        out[str(n.args[0])] = {"name": p.get("name", ""), "rating": p.get("rating", ""), "die": p.get("die", ""),
                               "tags": "", "gloss": p.get("gloss", ""), "blurb": p.get("tag", ""),
                               "joins": [j.strip() for j in p.get("joins", "").split(",") if j.strip()]}
    return out


_SCHEMA = None


def schema():
    """patterns/ read once: what every page and the PDF are drawn from."""
    global _SCHEMA
    if _SCHEMA is None:
        _SCHEMA = tb.Schema()
    return _SCHEMA


def region_labels() -> list[str]:
    """Every field of any rating's brief, in the order they render. `Tables` is
    drawn separately, as roll tables."""
    out: list[str] = []
    for f in schema().folders.values():
        for m in f.brief:
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
    """One brief field's text, as the site reads it."""
    fields: list[tuple[str, str]] = []
    _parse_region_fields(lines, fields, [])
    return dict(fields).get(label, "")


def parse_region_overview(code: str, gaz: dict) -> Region:
    """The region's brief, and what is drawn from its tables beside it, as one run sheet."""
    fields: list[tuple[str, str]] = []
    tables: list[tuple[str, list[tuple[int, str]]]] = []
    brief = SETTING / "region" / f"{code}.md"
    if brief.exists():
        _parse_region_fields(brief.read_text().splitlines()[1:], fields, tables)
    info = gaz[code]
    return Region(
        code=code, name=info["name"], rating=info["rating"], die=info["die"], tags=info["tags"],
        gazetteer_blurb=info["blurb"], fields=fields, tables=tables, drawn=drawn(code),
    )


# -- what is drawn from a region's tables beside its brief --------------------------------
#
# Each section is a list of lines in the citation forms render_inline links, one entry a
# line, so nothing in it is said twice and none of it goes stale.

_TABLES: tb.Setting | None = None


def region_tables() -> tb.Setting:
    global _TABLES
    if _TABLES is None:
        _TABLES = tb.Setting({c: r["rating"] for c, r in parse_regions_gazetteer().items()}, schema())
    return _TABLES


def _also(*parts) -> str:
    return "; ".join(p for p in parts if p)


def _reaction(v) -> tuple[str, str]:
    head, _, rest = str(v or "").partition(" - ")
    return head, rest


def _who(n) -> str:
    """An Encounter's or People entry's occupant, as a citation."""
    if n.name == "Creature" or "bestiary" in n.props:
        return f"{n.props.get('count', '')} {n.props.get('bestiary')}".strip()
    if "named" in n.props:
        return f"(Named Creature: {n.props['named']}), {n.props.get('presence', '')} of the time".rstrip(", ")
    return f"{n.props.get('present', '')} of (Faction: {n.props.get('faction')})".strip()


def _inhabitants(r, setting) -> list[str]:
    out = []
    for stem in ("People", "Garrison", "Challenges"):
        for n in r.files.get(stem, []):
            at = n.args[0] if n.args else ""
            p = n.props
            if n.name == "Person":
                quest = f"gives (Quest: {p['quest']})" if p.get("quest") else ""
                member = f"(Faction: {p['member']})" if p.get("member") else ""
                out.append(f"{at} **{p.get('name')}**, {p.get('role')}{' ' + member if member else ''} - "
                           + _also(f"wants {p.get('wants')}", f"knows {p.get('knows')}", quest))
            elif n.name in ("NamedCreature", "Faction"):
                out.append(f"{at} {_who(n)}" + (f" - {p['members']}" if p.get("members") else ""))
            elif n.name == "Garrison":
                out.append(f"{at} {_who(n)} under arms - {p.get('members')}; {p.get('call')} brings them within {p.get('within')}")
            elif n.name == "Encounter":
                kid = next((c for c in n.children if c.name in ("Creature", "NamedCreature", "Faction")), None)
                head, rest = _reaction(p.get("reaction"))
                if kid is not None and kid.name == "Creature":
                    who = f"({head}, {kid.props.get('count')}, Bestiary : {kid.props.get('bestiary')})"
                else:
                    who = f"{_who(kid) if kid is not None else ''}, {head}"
                out.append(f"{at} {who} - " + _also(p.get("doing"), rest, p.get("want") and f"wants {p['want']}",
                                                     p.get("know") and f"knows {p['know']}"))
    return out


def _procedures(r) -> list[str]:
    return [f"{n.args[0]} (Local Procedure: {n.props.get('procedure')})" for n in r.files.get("Procedures", []) if n.args]


def _services(r) -> list[str]:
    out = []
    for n in r.files.get("Purchases", []):
        p = n.props
        price = "at the listed price" if p.get("price") == "listed" else p.get("price")
        out.append(f"{n.args[0]} {p.get('item')} - {price}{' ' + p['per'] if p.get('per') else ''}"
                   + (f" ({p['limit']})" if p.get("limit") else ""))
    return out + _procedures(r)


GUARDS = {"Encounter": "watched", "Hazard": "trapped", "Mystery": "behind a mystery", "Secret": "hidden"}


def _loot(r) -> list[str]:
    brief = tb.Brief(schema())
    rolls = {k: (brief.lever(k).props.get("rolls") if brief.lever(k) else None) for k in ("Treasure", "Magic")}
    out = []
    for n in r.files.get("Rewards", []):
        table, _, title = str(n.props.get("contents", "")).partition(": ")
        die = rolls["Magic" if table == "Magic" else "Treasure"]
        what = f"({table}: {title})" if title else f"({table}, d{die})"
        guard = next((f"locked (Keys: {c.props.get('key')})" if c.name == "Lock" else GUARDS.get(c.name, "")
                      for c in n.children), "")
        out.append(f"{n.args[0]} {n.props.get('container')} - {what}{', ' + guard if guard else ''}")
    return out


def _alarm(r) -> list[str]:
    def soon(n):
        t = tb.TIME_RE.match(str(n.props.get("answers", "")))
        return (0 if t and t.group(3).startswith("Round") else 1, int(t.group(1)) if t else 0)
    out = []
    for n in sorted((n for n in r.files.get("Challenges", []) if n.name == "Encounter" and "answers" in n.props), key=soon):
        kid = next((c for c in n.children if c.name in ("Creature", "NamedCreature", "Faction")), None)
        out.append(f"{n.args[0]} {_who(kid) if kid is not None else ''} - within {n.props['answers']}")
    return out


def _leads(r) -> list[str]:
    sch, out = schema(), []
    codes = set(r.locations())
    for _title, _line, v in tb.setting_entries(sch, "Rumours") or []:
        here = [c for c in re.findall(r"[A-Z]+\.\d+", v.get("Settled at", "")) if c in codes]
        if here:
            out.append(f"Rumour {v.get('#')} ({v.get('T/P/F/U', '').split()[0] if v.get('T/P/F/U') else '?'}) - settled at {', '.join(here)}")
    givers = {str(n.props["quest"]): n for n in r.files.get("People", []) if n.props.get("quest")}
    for title, _line, v in tb.setting_entries(sch, "Quests") or []:
        here = [c for c in re.findall(r"[A-Z]+\.\d+", v.get("Points to", "")) if c in codes]
        g = givers.get(title)
        if here or g is not None:
            out.append(f"(Quest: {title}) - " + _also(g is not None and f"given by {g.props.get('name')} at {g.args[0]}",
                                                      here and f"points to {', '.join(here)}"))
    return out


def _secrets(r) -> list[str]:
    out = []
    for stem in r.files:
        for n in r.files[stem]:
            for c in n.children:
                if c.name != "Secret":
                    continue
                where = f"{n.args[0]} to {n.props['to']}" if "to" in n.props else f"{n.args[0]} {n.name}"
                p = c.props
                out.append(f"{where} - " + _also(p.get("fact"), p.get("knows") and f"known to {p['knows']}",
                                                f"shown by {p.get('tell')}", f"opened by {p.get('trigger')}",
                                                p.get("when") and f"when {p['when']}"))
    return out


DRAWERS = {"Inhabitants": _inhabitants, "Services": lambda r, s: _services(r), "Procedures": lambda r, s: _procedures(r),
           "Loot": lambda r, s: _loot(r), "Alarm": lambda r, s: _alarm(r), "Leads": lambda r, s: _leads(r),
           "Secrets": lambda r, s: _secrets(r)}


def drawn(code: str) -> list[tuple[str, list[str]]]:
    """Each section its rating's `drawn` names, with its lines; an empty one is left out."""
    setting = region_tables()
    r = setting.regions.get(code)
    if r is None or r.folder is None:
        return []
    return [(name, lines) for name in r.folder.drawn if (lines := DRAWERS[name](r, setting))]


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


# -- Maps, drawn by tools/maps.py ---------------------------------------------------

MapKey = tuple["Setting", "LinkResolver", str]     # what a key links with: the setting, a resolver, the page
MAP_TEXT_RE = re.compile(r"<text[^>]*>([^<]*)</text>")
MAP_LABEL_RE = re.compile(r"((?:up |down )?to )?([A-Z]+\.\d+)\b")


def map_key(svg: str, key: MapKey) -> str:
    """The key beside a drawn map: each location its labels show, linked, with its name and
    type, by region; then each location a way off the map leads to."""
    setting, resolver, page = key
    shown, leads = {}, {}
    for raw in MAP_TEXT_RE.findall(svg):
        if (m := MAP_LABEL_RE.match(html.unescape(raw).strip())) and m.group(2) in setting.all_locations:
            (leads if m.group(1) else shown)[m.group(2)] = True
    order = {c: i for i, c in enumerate(setting.region_order)}
    where = lambda code: (order.get(code.split(".")[0], len(order)), int(code.split(".")[1]))

    def item(code: str) -> str:
        loc = setting.all_locations[code]
        href = resolver.href("location", loc.region, loc.num, page)
        kind = f' <span class="map-key-type">{html.escape(loc.weight)}</span>' if loc.weight else ""
        return f'<li><a href="{href}">{code}</a> {html.escape(loc.name)}{kind}</li>'

    regions: dict[str, list[str]] = {}
    for code in sorted(shown, key=where):
        regions.setdefault(code.split(".")[0], []).append(code)
    out = []
    for r, codes in regions.items():
        head = f'<h4><a href="{resolver.href("region", r, page)}">{r} {html.escape(setting.regions[r].name)}</a></h4>' \
            if len(regions) > 1 else ""
        out.append(head + "<ul>" + "".join(map(item, codes)) + "</ul>")
    if off := sorted(set(leads) - set(shown), key=where):
        out.append("<h4>Leading off it</h4><ul>" + "".join(map(item, off)) + "</ul>")
    return f'<div class="map-key">{"".join(out)}</div>' if out else ""


def _figure(svg: str | None, caption: str, key: MapKey | None = None) -> str:
    if not svg:
        return ""
    return (f'<figure class="diagram plan-figure">{svg}<figcaption>{html.escape(caption)}</figcaption></figure>'
            + (map_key(svg, key) if key else ""))


def sheets_html(fit: str, key: MapKey | None = None) -> str:
    """Every terrain sheet whole: the play map, with its key where a link target is given."""
    import maps
    return "".join(_figure(maps.sheet_svg(f.stem, fit), f"{f.stem}, drawn from the setting's tables", key)
                   for f in sorted(SETTING.glob("*.json")))


def cut_html(code: str, num: int, fit: str) -> str:
    """Paused: no location cut is drawn (`maps.cut_svg` draws one)."""
    return ""


def drawn_html(code: str, fit: str, key: MapKey | None = None) -> str:
    """A DANGEROUS region's block maps, from its tables by artgen. Other ratings'
    region maps are paused (`maps.region_svg` draws one)."""
    import maps
    region = maps.world_for(SETTING).regions.get(code)
    if region is None:
        return ""
    return "".join(_figure(maps.block_svg(code, bid, fit), f"{bid} {b.props.get('name', '')}".strip(), key)
                   for bid, b in maps.drawn_blocks(region).items())


def map_labels() -> list[str]:
    """The label of each map a build must show: every sheet, and each DANGEROUS region's blocks."""
    import maps
    world = maps.world_for(SETTING)
    out = [f"Sheet {f.stem}" for f in sorted(SETTING.glob("*.json"))]
    for r in world.regions.values():
        out += [f"Map of {bid}" for bid in maps.drawn_blocks(r) if (r.dir / f"{bid}.json").exists()]
    return out


# A write-up's lines, as templates/region/Location.md's format gives them.
LOCATION = tp.load(tp.TEMPLATES / "region" / "Location.md")
LOC_HEADER_RE, FEATURE_RE = LOCATION.pattern("header"), LOCATION.pattern("feature")
LOC_CODE_FULL_RE = re.compile(r"([A-Z]+)\.(\d+)")
EXITS_HEAD = tp.literal_head(str(LOCATION.line("exits").props["pattern"]))


def index(setting: "Setting") -> list[tuple[str, list[tuple[str, dict[str, list[str]]]]]]:
    """Each entry table the region tables name: its entries in title order, each with the
    places naming it - a region's seed, then its locations, in region order - and the nodes
    there that do."""
    named, order = region_tables().namings(), {c: i for i, c in enumerate(setting.region_order)}
    where = lambda code: (order.get(code.split(".")[0], len(order)), int(code.partition(".")[2] or 0))
    out = []
    for t in (t for t in setting.tables if t.kind == "entry"):
        rows = []
        for e in sorted(t.entries, key=lambda e: strip_article(e.title).lower()):
            at: dict[str, list[str]] = {}
            for code, node in sorted(named.get((t.name, e.title), []), key=lambda h: where(h[0])):
                if node not in at.setdefault(code, []):
                    at[code].append(node)
            if at:
                rows.append((e.title, at))
        if rows:
            out.append((t.name, rows))
    return out


def index_html(setting: "Setting", resolver: "LinkResolver", page: str, heading: str = "h2") -> str:
    """The index: each entry linked, then each location naming it, linked, with the nodes
    there that name it."""
    spaced = lambda node: re.sub(r"(?<=[a-z])(?=[A-Z])", " ", node)
    out = []
    for table, rows in index(setting):
        items = []
        for title, at in rows:
            locs = []
            for code, nodes in at.items():
                region, _, num = code.partition(".")
                label = f'<span class="index-via">{", ".join(map(spaced, nodes))}</span>'
                href = resolver.href("location", region, int(num), page) if code in setting.all_locations else \
                    resolver.href("region", region, page) if not num and region in setting.regions else None
                locs.append(f'<a class="index-loc" href="{href}">{code}</a> {label}' if href else f"{code} {label}")
            items.append(f'<li><a href="{resolver.href("entry", table, title, page)}">{html.escape(title)}</a>'
                         f' - {"; ".join(locs)}</li>')
        out.append(f'<{heading}>{html.escape(table)}</{heading}><ul class="index-list">{"".join(items)}</ul>')
    return "".join(out)


def quickref() -> list[tuple[str, str]]:
    """Every d6 table a setting file's format holds, titled, its rows as written: what the
    PDF's quick reference gathers onto one page."""
    out = []
    for t in tp.load_all().values():
        tables = [n for n in t.format if n.name == "section" and n.props.get("out") == "table"]
        for path in (ROOT / w for w in t.writes() if tables and t.prop("scope") == "setting"):
            sections = tp.file_sections(path.read_text()) if path.exists() else {}
            for n in tables:
                name, body = str(n.args[0]), sections.get(str(n.args[0]), [])
                subs = {name: body} if "each" not in n.props else \
                    {f"{name}: {k}": v for k, v in tp.file_sections("\n".join(
                        l.replace("### ", "## ", 1) for l in body)).items()}
                out += [(title, "\n".join(l for l in lines if l.startswith("|")))
                        for title, lines in subs.items() if any(l.startswith("|") for l in lines)]
    return out


def line_class(name: str, base: str) -> str:
    """A write-up line's classes: its own, then its format's out=, which the stylesheets set."""
    out = LOCATION.line(name).props.get("out")
    return base + (f" {out}" if out else "")
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
    name, weight, tags = m["location_name"], m["type"], m["tags"]

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
        if s.startswith(EXITS_HEAD):
            exits_raw = s[len(EXITS_HEAD):].strip()
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


def join_lines(setting: "Setting") -> list[str]:
    """Each pair of regions the Regional Gazetteer joins, once."""
    pairs = {}
    for code, g in parse_regions_gazetteer().items():
        for other in g["joins"]:
            pairs.setdefault(frozenset((code, other)), (code, other))
    return [f"{edge_label(a, setting)} — {edge_label(b, setting)}" for a, b in pairs.values()]


def connection_lines(code: str, setting: "Setting") -> list[str]:
    """Each way between two locations of a region, once, from its Connections.md."""
    path = SETTING / "region" / code / "Connections.md"
    seen: dict[frozenset, tuple[str, str, bool]] = {}
    for n in kdl.fenced(path.read_text()) if path.exists() else []:
        if not n.args or "to" not in n.props:
            continue
        a, b = str(n.args[0]), str(n.props["to"])
        hidden = any(c.name == "Secret" for c in n.children)
        prev = seen.get(frozenset((a, b)))
        seen[frozenset((a, b))] = (prev[0], prev[1], prev[2] or hidden) if prev else (a, b, hidden)
    return [f"{edge_label(a, setting)} — {edge_label(b, setting)}" + (" (hidden)" if hidden else "")
            for a, b, hidden in seen.values()]


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
REGION_PAREN_RE = re.compile(r'(?<![\w)])\(([A-Z]{1,2})\)(?![\w(])')   # a region code standing alone, not a pattern like (C)(C)V(C)
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


# How a flowed field reads, beyond its own words: the styling of Setting_Schema.md's flow=.
FLOW_PHRASE = {"Numbers": "found in groups of {}", "Sign": "heralded by {}"}
FLOW_JOIN = {"Sign": ", "}       # joined to the clause before it by this, not "; "
FLOW_SPLIT = {"Range"}           # each of its sentences a clause


def flow(table: str) -> list[list[str]]:
    """A table's flow=: its sentences, each the fields it is built from."""
    return [g.split() for g in str(schema().table_props.get(table, {}).get("flow", "")).split("|") if g.split()]


def flow_fields(table: str) -> list[str]:
    return [k for g in flow(table) for k in g]


def flow_prose(table: str, f: dict) -> str:
    """An entry's flowed fields as its flow's sentences, each field's words kept."""
    lc = lambda x: x[:1].lower() + x[1:]
    out = []
    for i, group in enumerate(flow(table)):
        text = ""
        for k in group:
            v = f.get(k, "").rstrip(".")
            for part in ([x.strip() for x in v.split(". ")] if k in FLOW_SPLIT else [v]) if v else []:
                part = FLOW_PHRASE.get(k, "{}").format(part)
                text = text + FLOW_JOIN.get(k, "; ") + lc(part) if text else part
        if text:
            out.append((text if i == 0 else text[:1].upper() + text[1:]) + ".")
    return " ".join(out)


def statline(table: str) -> list[str]:
    """A table's stat=: the fields set on one line under an entry's title."""
    return str(schema().table_props.get(table, {}).get("stat", "")).split()


def entry_card(t: SettingTable, e: Entry, render, omit: tuple[str, ...] = ()) -> tuple[str, str]:
    """An entry's title line and its field rows, its statline first: what a card and a
    citation's box both show. `omit` names fields the caller sets elsewhere."""
    enums = schema().setting_enums
    dice = next((m.name for m in t.members if m.type == "dice"), None)
    tag = next((m.name for m in t.members if m.type in enums and not m.is_list), None)
    f = dict(e.fields)
    shown = set(omit)
    title = html.escape(e.title)
    if tag and len(f.get(tag, "").split()) <= 3 and tag in f:
        title += f' <span class="typetag">({html.escape(f[tag])})</span>'
        shown.add(tag)
    stat = [k for k in statline(t.name) if f.get(k)]
    if dice and dice in f and dice not in stat:
        title += f' <span class="ad">{html.escape(dice)}: {html.escape(f[dice])}</span>'
        shown.add(dice)
    shown |= set(stat)
    line = lambda v: "; ".join(l.removeprefix("- ").strip() for l in v.splitlines() if l.strip())
    strip = " · ".join(f'<span class="stat"><b>{html.escape(k)}</b> {render(line(f[k]))}</span>' for k in stat)
    fields = e.fields
    if (flowed := flow_fields(t.name)) and flowed[0] in f:
        fields = [(flowed[0], flow_prose(t.name, f))] + [(k, v) for k, v in fields if k not in flowed]
    rows = (f'<tr class="statline"><td colspan="2">{strip}</td></tr>' if stat else "") + \
        "".join(f"<tr><th>{html.escape(k)}</th><td>{value_html(v, render)}</td></tr>"
                for k, v in fields if k not in shown)
    for m in t.members:
        if m.type == "finds" and f.get(m.name):
            cn, wt = tb.finds_total(f[m.name])
            rows += f"<tr><th>Total</th><td>{cn:,} cn, {wt:,} wt</td></tr>"
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
    if by := str(schema().table_props.get(t.name, {}).get("timeline", "")):
        return f'<div id="{anchor_id("table", t.name)}">{h}{intro}{timeline_html(t, by, render)}</div>'
    cards = []
    for e in t.entries:
        title, rows = entry_card(t, e, render)
        cards.append(f'<article class="registry-card" id="{anchor_id("entry", t.name, e.title)}">'
                     f'<h3>{title}</h3><table class="kv-table">{rows}</table></article>')
    empty = '<p class="hint">Nothing recorded yet.</p>' if not cards else ""
    return (f'<div id="{anchor_id("table", t.name)}">{h}{intro}{empty}'
            f'<div class="registry-list">{"".join(cards)}</div></div>')


def timeline_html(t: SettingTable, by: str, render) -> str:
    """A table's entries on a rail, in the file's order: each marked by its `by` field, and
    an era heading wherever the item of the enum that field opens with changes."""
    member = next((m for m in t.members if m.name == by), None)
    items = list(schema().setting_enums.get(member.type, {})) if member else []
    out, era = [], None
    for e in t.entries:
        when = dict(e.fields).get(by, "")
        now = next((i for i in items if when.startswith(i)), None)
        if now and now != era:
            out.append(f'<li class="era">{html.escape(now.capitalize())}</li>')
            era = now
        title, rows = entry_card(t, e, render, omit=(by,))
        out.append(f'<li class="registry-card" id="{anchor_id("entry", t.name, e.title)}">'
                   f'<span class="when">{render(when)}</span><h3>{title}</h3>'
                   f'<table class="kv-table">{rows}</table></li>')
    return f'<ol class="timeline">{"".join(out)}</ol>' if out else '<p class="hint">Nothing recorded yet.</p>'


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
    bare = lambda x: re.sub(r"[.;,]", "", x)    # flowed prose rejoins sentences, keeping every word
    shown_bare = bare(shown)
    problems = []
    for t in setting.tables:
        if not has_page(t.page):
            problems.append(f"{t.name}: its file has no page")
        for e in t.entries:
            for label, value in e.fields:
                v = _plain(value.replace("\n- ", " ").removeprefix("- "))
                if label in flow_fields(t.name):
                    if bare(v) not in shown_bare:
                        problems.append(f"{t.name} / {e.title} / {label}: not shown")
                elif v not in shown:
                    problems.append(f"{t.name} / {e.title} / {label}: not shown")
    for p in setting.prose:
        if not has_page(p.slug):
            problems.append(f"{p.title}: its file has no page")
    for code, r in setting.regions.items():
        rendered = {label for label, _ in r.fields}
        path = SETTING / "region" / f"{code}.md"
        for label in re.findall(r"^([A-Z][a-z]+):", path.read_text(), re.M) if path.exists() else []:
            if label != "Tables" and label not in rendered:
                problems.append(f"{path.relative_to(ROOT)}: {label} is not shown")
        for label, _ in r.drawn:
            if not re.search(rf">{label}</h[1-6]>", text):
                problems.append(f"{code}: {label} is not shown")
        for num in r.locations:
            if not has_page(f"region/{code}/{num}"):
                problems.append(f"{code}.{num}: no page")
    problems += [f"{label}: no map" for label in map_labels() if f'aria-label="{label}"' not in text]
    return problems
