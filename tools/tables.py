"""Location tables: patterns/*_Schema.md loaded, every region's tables read and checked
against its rating's schema, and one location's entries gathered."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import kdl

ROOT = Path(__file__).resolve().parent.parent
SETTING = ROOT / "setting"
PATTERNS = ROOT / "patterns"
SHARED = ("Common", "Setting", "Region")   # the shared schemas, widest first; every other is a rating's

CODE_RE = re.compile(r"([A-Z]+)\.(\d+)")
BLOCK_RE = re.compile(r"([A-Z]+)\.([a-z]+)")
RANGE_RE = re.compile(r"(\d+)(?:-(\d+))?")
PERCENT_RE = re.compile(r"(\d+)%")
SHARE_RE = re.compile(r"(<=)?(\d+)%")        # "N%" at least that share of entries, "<=N%" at most
COUNT_RE = re.compile(r"(\d+)(?:-(\d+)|(\+))?")   # N exactly, "N-M", "N+" at least
OPEN = 10 ** 9
FEET_RE = re.compile(r"-?\d+")
DISTANCE_RE = re.compile(r"(\d+(?:\.\d+)?) (\w+)")
MMD_NODE_RE = re.compile(r'(\w+)\["([A-Z]+\.\d+)[^"]*"\]')
MMD_EDGE_RE = re.compile(r'(\w+)(?:\["[^"]*"\])?\s*(?:---|-->|-\.-)(?:\|[^|]*\|)?\s*(\w+)')


@dataclass
class Member:
    name: str
    type: str = ""
    arg: str | None = None
    opt: bool = False
    is_list: bool = False
    n: int | None = None
    nodes: list[str] = field(default_factory=list)
    args: list[str] = field(default_factory=list)      # every table an entry member names
    props: dict = field(default_factory=dict)          # range=, count=, bonus=
    none: bool = False


@dataclass
class Folder:
    """One rating's tables, with the enums and nodes its schema sees: its own over the
    shared schemas'. Its seed and brief are its `region` in Region_Schema.md."""
    type: str
    files: dict[str, list[str]]
    joins: dict[str, tuple[set[str], str | None]]
    top: set[str]
    path: Path
    enums: dict[str, dict] = field(default_factory=dict)
    nodes: dict[str, list[Member]] = field(default_factory=dict)
    rates: dict[str, dict[str, tuple[int, int]]] = field(default_factory=dict)
    seed: list[Member] = field(default_factory=list)    # setting/region/[Code].md's fields
    brief: list[Member] = field(default_factory=list)   # setting/region/[Code]/Brief.md's
    region_path: Path | None = None                     # the schema holding seed and brief


def entries_allowed(want, of: int | None = None) -> tuple[int, int] | None:
    """The entry counts a target value allows, or None where it is no value. A share is
    taken of `of` entries, a floor rounded down and a ceiling rounded up, so a small
    region owes nothing it cannot hold whole and overshooting a floor is always met."""
    s = str(want)
    if m := SHARE_RE.fullmatch(s):
        if of is None:
            return None
        n = int(m.group(2))
        return (0, -(-n * of // 100)) if m.group(1) else (n * of // 100, OPEN)
    if m := COUNT_RE.fullmatch(s):
        lo = int(m.group(1))
        hi = OPEN if m.group(3) else int(m.group(2) or lo)
        return (lo, hi) if lo <= hi else None
    return None


def bounds(rate) -> tuple[int, int] | None:
    s = str(rate)
    if m := RANGE_RE.fullmatch(s):
        lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
        return (lo, hi) if lo <= hi else None
    return None


class Schema:
    """patterns/*_Schema.md: the shared Common, Setting and Region schemas, then one per
    rating holding its folder, each a scope over the ones before it. Region_Schema.md
    gives each folder its seed and brief; BRIEF.md's node for its rating, its rates."""

    def __init__(self, root: Path = PATTERNS, brief: Path | None = None):
        self.problems: list[tuple[Path, str]] = []
        self.brief_problems: list[str] = []
        self.words, self.values, self.tables, self.folders = {}, set(), {}, {}
        self.fields: dict[str, list[Member]] = {}       # a setting table's fields
        self.table_props: dict[str, dict] = {}
        self.setting_enums: dict[str, dict] = {}
        self.regions: dict[str, tuple[Path, dict[str, list[Member]]]] = {}
        shared: tuple[dict, dict] = ({}, {})
        for path in (root / f"{n}_Schema.md" for n in SHARED):
            self._read(path, *shared)
        self.setting_enums = dict(shared[0])
        self._resolve_fields()
        for path in sorted(set(root.glob("*_Schema.md")) - {root / f"{n}_Schema.md" for n in SHARED}):
            enums, nodes = dict(shared[0]), dict(shared[1])
            for f in self._read(path, enums, nodes):
                f.enums, f.nodes = enums, nodes
        for name, (path, parts) in self.regions.items():
            if f := self.folders.get(name):
                f.seed, f.brief, f.region_path = parts.get("seed", []), parts.get("brief", []), path
            else:
                self.problems.append((path, f"region {name!r} has no folder"))
        for name, f in self.folders.items():
            if f.region_path is None:
                self.problems.append((f.path, f"folder {name}: no region in Region_Schema.md"))
        try:
            for n in brief_nodes(brief or BRIEF):
                if f := self.folders.get(n.name.title()):
                    for c in n.children:
                        if c.name == "rate":
                            f.rates.update({a: {s: bounds(r) for s, r in c.props.items()} for a in c.args})
        except SyntaxError as e:
            self.brief_problems.append(str(e))
        self._resolve()

    def _read(self, path: Path, enums: dict, nodes: dict) -> list[Folder]:
        """One schema file into the scope given; a name it defines shadows a wider one."""
        p = lambda n, msg: self.problems.append((path, f"line {n.line}: {msg}"))
        try:
            top = kdl.fenced(path.read_text())
        except (OSError, SyntaxError) as e:
            self.problems.append((path, str(e)))
            return []
        folders, own = [], set()
        for n in top:
            name = n.args[0] if n.args else None
            if n.name in ("enum", "node", "folder", "region"):
                if (n.name, name) in own:
                    p(n, f"{n.name} {name!r} is defined twice")
                own.add((n.name, name))
            if n.name == "value":
                self.values.add(name)
                if "words" in n.props:
                    self.words[name] = n.props["words"]
            elif n.name == "table":
                self.tables[name] = (n.args[1], n.props["file"])
                self.table_props[name] = n.props
                if n.children:
                    self.fields[name] = [self._member(c) for c in n.children]
                elif "as" in n.props:
                    self.fields[name] = self.fields.get(n.props["as"], [])
            elif n.name == "enum":
                items = {a: None for a in n.args[1:]}
                for g in n.children:
                    items.update({a: g.name for a in g.args})
                enums[name] = items
            elif n.name == "node":
                nodes[name] = [self._member(c) for c in n.children]
            elif n.name == "folder" and path.stem.split("_")[0] not in SHARED:
                files = {c.name: c.args for c in n.children if c.name not in ("join", "top")}
                joins = {c.args[0]: (set(c.args[1:]), c.props.get("gate"))
                         for c in n.children if c.name == "join" and c.args}
                top = {a for c in n.children if c.name == "top" for a in c.args}
                f = Folder(n.props.get("type", ""), files, joins, top, path)
                self.folders[name] = f
                folders.append(f)
            elif n.name == "region":
                for c in n.children:
                    if c.name not in ("seed", "brief"):
                        p(c, f"region {name}: {c.name!r} is not seed or brief")
                self.regions[name] = (path, {c.name: [self._member(m) for m in c.children]
                                             for c in n.children})
            else:
                p(n, f"{n.name!r} is not a schema node here")
        return folders

    @staticmethod
    def _member(c) -> Member:
        flags = {"opt", "list", "none"}
        if c.name == "one-of":
            return Member("one-of", opt="opt" in c.args, nodes=[a for a in c.args if a not in flags])
        rest = [a for a in c.args[1:] if a not in flags]
        return Member(c.name, c.args[0] if c.args else "", rest[0] if rest else None, "opt" in c.args,
                      "list" in c.args, c.props.get("n"), [], rest, c.props, "none" in c.args)

    def _resolve_fields(self):
        """Every setting table's fields name a value, an enum or tables that exist."""
        path = PATTERNS / "Setting_Schema.md"
        for name, fields in self.fields.items():
            for m in fields:
                if m.type not in self.values and m.type not in self.setting_enums:
                    self.problems.append((path, f"{name}.{m.name}: unknown type {m.type!r}"))
                for t in (m.args if m.type == "entry" else []):
                    if t not in self.tables:
                        self.problems.append((path, f"{name}.{m.name}: unknown table {t!r}"))

    def _resolve(self):
        path = PATTERNS / "Setting_Schema.md"
        for table, fields in self.fields.items():
            for m in fields:
                node = m.props.get("from")
                if node and not any(names_table(f, node, table) for f in self.folders.values()):
                    self.problems.append((path, f"{table}.{m.name}: from={node} is no node naming {table}"))
        seen = set()
        for name, f in self.folders.items():
            def p(msg, f=f):
                if (f.path, msg) not in seen:
                    seen.add((f.path, msg))
                    self.problems.append((f.path, msg))
            # every node the folder's files can hold, through one-of children
            todo = [n for ns in f.files.values() for n in ns]
            reach = set()
            while todo:
                node = todo.pop()
                if node in reach:
                    continue
                reach.add(node)
                if node not in f.nodes:
                    p(f"folder {name}: holds unknown node {node!r}")
                    continue
                for m in f.nodes[node]:
                    todo += m.nodes
                    if m.name == "one-of":
                        continue
                    if m.type not in self.values and m.type not in f.enums:
                        p(f"{node}.{m.name}: unknown type {m.type!r}")
                    if m.type == "entry" and m.arg not in self.tables:
                        p(f"{node}.{m.name}: unknown table {m.arg!r}")
                    if m.type == "pull" and not set(f.enums.get(m.arg, {"?": 0})) <= set(self.tables):
                        p(f"{node}.{m.name}: {m.arg!r} is not an enum of tables")
            if f.type not in f.enums:
                p(f"folder {name}: unknown type enum {f.type!r}")
            for m in f.seed + f.brief:
                if m.type not in self.values and m.type not in f.enums:
                    p(f"folder {name}: seed or brief field {m.name}: unknown type {m.type!r}")
            # A group of the type enum names every item in it.
            groups = {}
            for item, g in f.enums.get(f.type, {}).items():
                groups.setdefault(g, set()).add(item)
            grow = lambda names: {x for n in names for x in groups.get(n, {n})}
            f.rates = {i: r for item, r in f.rates.items() for i in grow([item])}
            f.top = grow(f.top)
            f.joins = {i: (grow(to), gate) for item, (to, gate) in f.joins.items() for i in grow([item])}
            for item, rates in f.rates.items():
                if item not in f.enums.get(f.type, {}):
                    self.brief_problems.append(f"{name.lower()}: rate for {item!r}, which {f.type} does not hold")
                for stem, b in rates.items():
                    if stem not in f.files or b is None:
                        self.brief_problems.append(f"{name.lower()}: rate {item} {stem} is not a table file and a count or range")
            for t in f.top:
                if t not in f.enums.get(f.type, {}):
                    p(f"folder {name}: top names {t!r}, which {f.type} does not hold")
            for item, (to, gate) in f.joins.items():
                for t in {item} | to:
                    if t not in f.enums.get(f.type, {}):
                        p(f"folder {name}: join names {t!r}, which {f.type} does not hold")
                if gate and gate not in f.nodes:
                    p(f"folder {name}: join gate {gate!r} is not a node")
            if f.joins and "Connections" not in f.files:
                p(f"folder {name}: join without a Connections file")


def names_table(f: Folder, node: str, table: str) -> bool:
    """A folder's node has a member naming entries on the table: an entry, or a pull of it."""
    return any(m.type == "entry" and m.arg == table
               or m.type == "pull" and table in f.enums.get(m.arg, {})
               for m in f.nodes.get(node, []))


def titles(path: Path) -> set[str] | None:
    """A setting table's entry titles: its ### headings, else its first column."""
    if not path.exists():
        return None
    text = path.read_text()
    heads = set(re.findall(r"^### (.+?)\s*$", text, re.M))
    if heads:
        return heads
    rows = [l for l in text.splitlines() if l.strip().startswith("|")]
    return {l.strip().strip("|").split("|")[0].strip() for l in rows[2:]}


# -- the setting files ---------------------------------------------------------
#
# Each setting table with fields in Setting_Schema.md is read as records (`### Title`,
# `## ` where heading=2, then `Field: value` lines) or as the first pipe table, and every
# entry's fields are checked against it. An empty field is a stub, still to be written.

DICE_RE = re.compile(r"(\d+)d6(?:\s*([+-])\s*(\d+))?")
PLACE_RE = re.compile(r"[A-Z]+\.\d+(?:\s*,\s*[A-Z]+\.\d+)*\b")


def setting_entries(schema: Schema, name: str) -> list[tuple[str, int, dict[str, str]]] | None:
    """(title, line, fields) for every entry of one setting file, or None if it is unbuilt."""
    import site_common as sc
    path = ROOT / schema.tables[name][1]
    if not path.exists():
        return None
    level = int(schema.table_props[name].get("heading", 3))
    if re.search(rf"^{'#' * level} ", path.read_text(), re.M):
        return [(r.name, r.line, dict(r.fields)) for r in sc.read_records(path, level)]
    ts = sc.read_tables(path)
    if not ts:
        return []
    return [(row[0] if row else "?", line, dict(zip(ts[0].header, row)) | {"": len(row) - len(ts[0].header)})
            for row, line in zip(ts[0].rows, ts[0].lines)]


def check_setting_files(schema: Schema, codes: set[str]):
    """Yield (severity, path, line, message) for every setting file entry against its
    table's fields; severity "stub" is an empty field still to be written."""
    for name, fields in schema.fields.items():
        entries = setting_entries(schema, name)
        if not entries:
            continue
        path = ROOT / schema.tables[name][1]
        known = {m.name for m in fields}
        seen = set()
        for title, line, values in entries:
            if title in seen:
                yield "error", path, line, f"{title} is a title used twice"
            seen.add(title)
            if values.pop("", 0):
                yield "error", path, line, f"{title}: its row has a different number of cells from the header"
            for k in values:
                if k not in known:
                    yield "error", path, line, f"{title} carries {k!r}, which {name} has no field for"
            empty = [m.name for m in fields if not values.get(m.name, "").strip() and not m.opt]
            if empty:
                yield "stub", path, line, f"stub - {title}: {', '.join(empty)} still empty"
            for m in fields:
                v = values.get(m.name, "").strip()
                if v:
                    checks = check_relations(schema, name, title, v) if m.type == "relation" \
                        else check_field(schema, m, v, codes)
                    for msg in checks:
                        yield "error", path, line, f"{title} {m.name}: {msg}"


RELATION_RE = re.compile(r"- (.+?) - (\w+)\b")


def check_relations(schema: Schema, table: str, title: str, v: str):
    """Yield what is wrong with a Relations field: one `- [Faction] - [Relation]` line for
    every other entry of its table, once each."""
    levels = schema.setting_enums["Relation"]
    others = (titles(ROOT / schema.tables[table][1]) or set()) - {title}
    seen = []
    for line in (l for l in v.split("\n") if l.startswith("- ")):
        m = RELATION_RE.match(line)
        if not m:
            yield f"{line[:30]!r} is not '- [Faction] - [Relation]'"
            continue
        name, level = m.groups()
        if name == title:
            yield "lists itself"
        elif name not in others:
            yield f"{name!r} is on no {table} entry"
        if level not in levels:
            yield f"{level!r} is not one of {', '.join(levels)}"
        seen.append(name)
    for name in sorted(others):
        if seen.count(name) != 1:
            yield f"{name!r} is listed {seen.count(name)} times, not once"


LANGUAGE = SETTING / "Language.md"
BEING_FORMS = ("common", "family", "epithet", "tongue")
PLACE_FORMS = ("common", "tongue")
EPITHET_RE = re.compile(r".\s(?:the|son of|daughter of|of)\s.", re.I)
COINAGE_RE = re.compile(r"(.+?) = (.+?) - (.+)")


def coinages(path: Path = LANGUAGE) -> tuple[dict[str, tuple[str, str]], list[str]]:
    """Every tongue's `Coined here`: lowercased noun -> (tongue, noun), and what is wrong with
    the lines. A line is `- Noun = root + root - what it means`, each part a root or an
    affix of its own tongue."""
    import site_common as sc
    if not path.exists():
        return {}, []
    known, problems = {}, []
    for r in sc.read_records(path, 2):
        roots = {l[2:].split(" - ")[0].strip().lower()
                 for l in r.get("Roots").split("\n") if l.startswith("- ")}
        affixes = {a.split(" - ")[0].strip().lower() for a in r.get("Affixes").split(";") if a.strip()}
        for line in (l for l in r.get("Coined here").split("\n") if l.strip()):
            m = COINAGE_RE.fullmatch(line.removeprefix("- ").strip())
            if not m:
                problems.append(f"{r.name}: {line!r} is not '- Noun = root + root - what it means'")
                continue
            noun, parts = m.group(1).strip(), [x.strip().lower() for x in m.group(2).split(" + ")]
            for x in parts:
                if x not in roots | affixes:
                    problems.append(f"{r.name}: {noun} is built from {x!r}, which is no root or affix of its tongue")
            known[noun.lower()] = (r.name, noun)
    return known, problems


def tongues_alike(path: Path = LANGUAGE) -> list[str]:
    """What two tongues share that no two may: a syllable shape or a consonant inventory."""
    import site_common as sc
    if not path.exists():
        return []
    seen, out = {}, []
    for r in sc.read_records(path, 2):
        for field, key in (("Syllable", " ".join(r.get("Syllable").lower().split())),
                           ("Consonants", frozenset(c.strip().lower()
                                                    for c in r.get("Consonants").split(",") if c.strip()))):
            if key and (field, key) in seen:
                out.append(f"{r.name} and {seen[field, key]} have the same {field.lower()} - no two tongues do")
            else:
                seen[field, key] = r.name
    return out


def unit_problem(typ: str, v: str, enums: dict) -> str | None:
    """What is wrong with a `feet` or `distance` value, or None where it reads."""
    if typ == "feet":
        return None if FEET_RE.fullmatch(v) else f"{v!r} is not a whole number of feet"
    m = DISTANCE_RE.fullmatch(v)
    units = enums.get("Distance_Unit", {})
    if not m or m.group(2) not in units:
        return f"{v!r} is not a number then {' | '.join(units)}"
    return None


def _opens_with(v: str, items) -> bool:
    low = v.lower()
    return any(low.startswith(i.lower()) and low[len(i):len(i) + 1] in ("", " ", ".", ",", ";", ":")
               for i in items)


def check_field(schema: Schema, m: Member, v: str, codes: set[str], enums: dict | None = None):
    """Yield what is wrong with one field's value. An enum field opens with an item; a
    list enum lists items before any ` - `."""
    enums = schema.setting_enums if enums is None else enums
    if m.none and _opens_with(v, ["none"]):
        return
    if m.type in enums:
        items = enums[m.type]
        if m.is_list:
            for x in (i.strip() for i in v.split(" - ")[0].split(",")):
                if x not in items:
                    yield f"{x!r} is not one of {', '.join(items)}"
        elif not _opens_with(v, items):
            yield f"{v[:30]!r} does not open with one of {', '.join(items)}"
    elif m.type == "number":
        b, want = bounds(v), bounds(m.props.get("range", ""))
        if b is None:
            yield f"{v!r} is not N or N-M"
        elif want and not (want[0] <= b[0] and b[1] <= want[1]):
            yield f"{v} is outside {m.props['range']}"
    elif m.type in ("feet", "distance"):
        if msg := unit_problem(m.type, v, enums):
            yield msg
    elif m.type == "dice":
        d = DICE_RE.fullmatch(v)
        if not d:
            yield f"{v!r} is not Nd6 or Nd6+M"
            return
        count, bonus = int(d.group(1)), int(d.group(3) or 0) * (-1 if d.group(2) == "-" else 1)
        if (c := bounds(m.props.get("count", ""))) and not c[0] <= count <= c[1]:
            yield f"{count} dice is outside {m.props['count']}"
        lo, _, hi = str(m.props.get("bonus", "")).partition("..")
        if hi and not int(lo) <= bonus <= int(hi):
            yield f"bonus {bonus:+d} is outside {lo}..{hi}"
    elif m.type == "place":
        p = PLACE_RE.match(v)
        if not p:
            yield f"{v[:30]!r} opens with no location code" + (" or none" if m.none else "")
        else:
            for c in re.findall(r"[A-Z]+\.\d+", p.group(0)):
                if c not in codes:
                    yield f"{c} is not a location"
    elif m.type == "entry":
        for x in ([i.strip() for i in v.split(",")] if m.is_list else [v]):
            have = set().union(*(titles(ROOT / schema.tables[t][1]) or set() for t in m.args))
            if x not in have:
                yield f"{x!r} is on none of {', '.join(m.args)}"
    elif m.type in schema.words and len(v.split()) > schema.words[m.type]:
        yield f"{len(v.split())} words - a {m.type} is at most {schema.words[m.type]}"


@dataclass
class Region:
    code: str
    rating: str
    dir: Path
    folder: Folder | None
    files: dict[str, list] = field(default_factory=dict)
    syntax: list[tuple[Path, str]] = field(default_factory=list)
    diagram: Path | None = None
    nodes: dict[str, str] = field(default_factory=dict)
    edges: list[tuple[str, str]] = field(default_factory=list)
    unresolved: set[str] = field(default_factory=set)

    def locations(self) -> dict[str, kdl.Node]:
        return {n.args[0]: n for n in self.files.get("Locations", []) if n.args}


class Setting:
    """Every region's tables and diagram, read once."""

    def __init__(self, regions: dict[str, str], schema: Schema | None = None):
        self.schema = schema or Schema()
        self.regions = {code: self._read(code, rating) for code, rating in regions.items()}
        self.codes = {c for r in self.regions.values() for c in r.locations()}
        self.connections = {(n.args[0], n.props.get("to")) for r in self.regions.values()
                            for n in r.files.get("Connections", []) if n.args}
        self.edges = {frozenset(e) for r in self.regions.values() for e in r.edges}
        self._titles: dict[str, set | None] = {}

    def _read(self, code: str, rating: str) -> Region:
        rdir = SETTING / "region" / code
        r = Region(code, rating, rdir, self.schema.folders.get(rating.title()))
        for stem in (r.folder.files if r.folder else ["Locations"]):
            path = rdir / f"{stem}.md"
            if path.exists():
                try:
                    r.files[stem] = kdl.fenced(path.read_text())
                except SyntaxError as e:
                    r.syntax.append((path, str(e)))
        mmd = rdir / "Connections.mmd"
        if mmd.exists():
            r.diagram = mmd
            for line in mmd.read_text().splitlines():
                line = line.split("%%")[0]
                for m in MMD_NODE_RE.finditer(line):
                    r.nodes[m.group(1)] = m.group(2)
                for m in MMD_EDGE_RE.finditer(line):
                    r.edges.append((m.group(1), m.group(2)))
            r.unresolved = {i for e in r.edges for i in e if i not in r.nodes}
            r.edges = [(r.nodes[a], r.nodes[b]) for a, b in r.edges
                       if a in r.nodes and b in r.nodes]
        return r

    def titles(self, table: str) -> set | None:
        if table not in self._titles:
            self._titles[table] = titles(ROOT / self.schema.tables[table][1])
        return self._titles[table]

    # -- checks -------------------------------------------------------------

    def check(self):
        """Yield (severity, path, message) for every region, then for the keys between them,
        then for the setting entries the tables place."""
        for r in self.regions.values():
            yield from self._check_region(r)
        yield from self._check_keys()
        yield from self._check_placements()
        yield from self._check_names()

    def placements(self) -> dict[tuple[str, str, str], set[str]]:
        """(table, title, place field) -> the locations whose entries name that setting
        entry through the node the field's from= names."""
        out: dict[tuple[str, str, str], set[str]] = {}
        froms = {(table, m.props["from"]): m.name for table, fields in self.schema.fields.items()
                 for m in fields if "from" in m.props}
        for r in self.regions.values():
            if r.folder is None:
                continue
            for entries in r.files.values():
                for n in entries:
                    code = n.args[0] if n.args else None
                    for node in kdl.walk([n]):
                        for m in r.folder.nodes.get(node.name, []):
                            v = node.props.get(m.name)
                            if v is None or m.type not in ("entry", "pull"):
                                continue
                            for item in ([x.strip() for x in str(v).split(",")] if m.is_list else [str(v)]):
                                table, _, title = item.partition(": ") if m.type == "pull" else (m.arg, "", item)
                                if f := froms.get((table, node.name)):
                                    out.setdefault((table, title, f), set()).add(code)
        return out

    def _check_placements(self):
        """Every place field with a from= against the tables, both ways, each owed to 5a: a
        location the tables place an entry at, to its field; a location the field names and
        no entry there holds, to a stub there."""
        placed = self.placements()
        for table, fields in self.schema.fields.items():
            fields = [m for m in fields if "from" in m.props]
            entries = setting_entries(self.schema, table) if fields else None
            if entries is None:
                continue
            path = ROOT / self.schema.tables[table][1]
            for title, line, values in entries:
                for m in fields:
                    listed = set(re.findall(r"[A-Z]+\.\d+", values.get(m.name, "")))
                    held = placed.get((table, title, m.name), set())
                    for c in sorted(held - listed):
                        yield "warning", path, (f"line {line}: {title} {m.name} lacks {c}, where a "
                                                f"{m.props['from']} names it - owed to step 5a")
                    for c in sorted(listed - held):
                        yield "warning", path, (f"line {line}: {title} {m.name} names {c}, where no "
                                                f"{m.props['from']} names it yet - owed to step 5a")

    def _check_names(self):
        """Every name a schema gives a form is that form, and every coinage a tongue records
        is in one. A being is named in any of four forms: a tongue name is a recorded
        coinage, a family name ends in one, an epithet reads "X the Y", "X son of Y" or "X of
        Y", and a common name holds none. A place is common or tongue. A location's name
        carries no form: it may point at a coinage and never coins one."""
        known, problems = coinages()
        for msg in problems + tongues_alike():
            yield "error", LANGUAGE, msg
        used: set[str] = set()
        has = lambda name: [n for n in known if re.search(rf"\b{re.escape(n)}\b", name, re.I)]
        for path, where, name, form, allowed in self.names():
            if form is None:
                used.update(has(name))
                continue
            if form not in allowed:
                yield "error", path, f"{where}: {name!r} is {form!r}, but its kind is named {' or '.join(allowed)}"
                continue
            base = re.sub(r"^(?:the|a|an)\s+", "", name, flags=re.I)
            words = name.split()
            if form == "tongue":
                if base.lower() in known:
                    used.add(base.lower())
                else:
                    yield "error", path, f"{where}: {name!r} is a tongue name no tongue records in Coined here - record it in Language.md first"
            elif form == "family":
                tails = [" ".join(words[i:]).lower() for i in range(1, len(words))]
                hit = next((t for t in tails if t in known), None)
                if hit:
                    used.add(hit)
                else:
                    yield "error", path, (f"{where}: {name!r} is a family name but does not end in a "
                                          f"coinage Coined here records, after a common name - record it in Language.md first")
            elif form == "epithet":
                if not EPITHET_RE.search(name):
                    yield "error", path, f"{where}: {name!r} is not 'X the Y', 'X son of Y' or 'X of Y'"
            elif form == "common":
                for noun in has(name):
                    yield "error", path, f"{where}: {name!r} holds the coinage {noun!r} - it is not a common name"
        for noun, (tongue, shown) in sorted(known.items()):
            if noun not in used:
                yield "warning", LANGUAGE, (f"{tongue}: {shown} is recorded, but no name uses it - "
                                            f"give a name its form or cut it")

    def names(self):
        """(path, where, name, form, forms allowed) for every name the build holds: a being's
        in a schema field, a place's in the setting's title or the gazetteer, and a
        location's with no form, which may only point at a coinage."""
        out = []
        for r in self.regions.values():
            if r.folder is None:
                continue
            for stem, entries in r.files.items():
                for n in entries:
                    for node in kdl.walk([n]):
                        ms = r.folder.nodes.get(node.name, [])
                        if "name" not in node.props:
                            continue
                        path, where, name = r.dir / f"{stem}.md", f"line {node.line}", str(node.props["name"])
                        if f := next((m for m in ms if m.type == "Name_Form"), None):
                            if node.props.get(f.name):
                                out.append((path, where, name, str(node.props[f.name]), BEING_FORMS))
                        elif node.name == "Location":
                            out.append((path, where, name, None, ()))
        import site_common as sc
        gaz = SETTING / "region" / "Regions.md"
        for t in sc.read_tables(gaz)[:1] if gaz.exists() else []:
            for d, line in zip(t.dicts(), t.lines):
                if d.get("Name") and d.get("Form"):
                    out.append((gaz, f"line {line}", d["Name"], d["Form"].split()[0], PLACE_FORMS))
        sfile = SETTING / "Setting.md"
        if sfile.exists():
            lines = [l.strip() for l in sfile.read_text().splitlines() if l.strip()]
            form = next((l[5:].strip() for l in lines if l.startswith("Form:")), "")
            if lines and form:
                out.append((sfile, "line 1", lines[0], form.split()[0], PLACE_FORMS))
        for table, fields in self.schema.fields.items():
            f = next((m for m in fields if m.type == "Name_Form"), None)
            for title, line, values in (setting_entries(self.schema, table) or []) if f else []:
                if values.get(f.name, "").strip():
                    out.append((ROOT / self.schema.tables[table][1], f"line {line}", title,
                                values[f.name].split()[0].rstrip(".,;:"), BEING_FORMS))
        return out

    def _check_keys(self):
        """Every lock has its key placed, every key its lock, and no key lies behind the lock
        it opens. Locks are written first and keys for them after, so a lock waiting on its
        key is owed to 5a, and a key with no lock is an error."""
        locks, keys = {}, {}
        for r in self.regions.values():
            for stem, entries in r.files.items():
                for n in entries:
                    for c in kdl.walk([n]):
                        if c.name == "Lock" and "key" in c.props:
                            locks.setdefault(c.props["key"], []).append((r, stem, n))
                    table, _, title = str(n.props.get("contents", "")).partition(": ")
                    if n.name == "Reward" and table == "Keys" and title:
                        keys.setdefault(title, []).append((r, stem, n))
        for title, held in sorted(keys.items()):
            for r, stem, n in held:
                path = r.dir / f"{stem}.md"
                if title not in locks:
                    yield "error", path, (f"line {n.line}: {title!r} is placed, but no Lock names it - "
                                          f"a key is placed only for a lock already placed")
                elif any(m is n for _, _, m in locks[title]):
                    yield "error", path, f"line {n.line}: {title!r} is locked inside itself"
        for title, placed in sorted(locks.items()):
            if title not in keys:
                r, stem, n = placed[0]
                yield "warning", r.dir / f"{stem}.md", (f"line {n.line}: Lock {title!r} has no key "
                                                       f"placed yet - owed to step 5a")
                continue
            for r, stem, n in keys[title]:
                if self._behind(r, title, n.args[0] if n.args else None):
                    yield "error", r.dir / f"{stem}.md", (
                        f"line {n.line}: {title!r} lies behind the lock it opens - it cannot be "
                        f"reached from {', '.join(self._entrances(r))} without it")

    def _entrances(self, r: Region) -> list[str]:
        """The region's rooms touching another region, or else its first room."""
        own = set(r.locations())
        outside = {c for a, b in r.edges for c in (a, b) if c not in own}
        ways_in = sorted({c for a, b in r.edges for c in (a, b)
                          if c in own and ({a, b} & outside)})
        return ways_in or sorted(own, key=lambda c: int(c.split(".")[1]))[:1]

    def _behind(self, r: Region, title: str, code: str | None) -> bool:
        if code is None or code not in r.locations():
            return False
        locked = {frozenset((n.args[0], n.props.get("to"))) for n in r.files.get("Connections", [])
                  if n.args and any(c.name == "Lock" and c.props.get("key") == title
                                    for c in n.children)}
        adj: dict[str, set] = {}
        for a, b in r.edges:
            if frozenset((a, b)) not in locked:
                adj.setdefault(a, set()).add(b)
                adj.setdefault(b, set()).add(a)
        seen, todo = set(self._entrances(r)), list(self._entrances(r))
        while todo:
            for nxt in adj.get(todo.pop(), ()):
                if nxt not in seen:
                    seen.add(nxt)
                    todo.append(nxt)
        return code not in seen

    def _check_region(self, r: Region):
        for path, msg in r.syntax:
            yield "error", path, msg
        if r.folder is None:
            yield "warning", r.dir, f"{r.rating} has no folder in {self.schema.path.name}"
            return
        for path in sorted(r.dir.glob("*.md")):
            if not path.stem.isdigit() and path.stem not in r.folder.files and path.stem != "Brief":
                yield "error", path, (f"is neither a location file, Brief.md, nor one of "
                                      f"{', '.join(r.folder.files)}")
        for stem in r.folder.files:
            path = r.dir / f"{stem}.md"
            if not path.exists():
                yield "warning", path, "missing - not built yet"
        yield from self._check_locations(r)
        for stem, entries in r.files.items():
            path = r.dir / f"{stem}.md"
            for n in entries:
                for sev, msg in self._check_entry(r, stem, n):
                    yield sev, path, f"line {n.line}: {msg}"
        yield from self._check_rates(r)
        if "Connections" in r.folder.files:
            yield from self._check_diagram(r)
            yield from self._check_joins(r)

    def _check_locations(self, r: Region):
        path = r.dir / "Locations.md"
        nums = []
        for n in r.files.get("Locations", []):
            m = CODE_RE.fullmatch(str(n.args[0])) if n.args else None
            if m and m.group(1) == r.code:
                nums.append(int(m.group(2)))
        if len(set(nums)) != len(nums):
            yield "error", path, "a location code is used twice"
        if sorted(nums) != list(range(1, len(nums) + 1)):
            yield "error", path, f"location numbers {sorted(nums)} are not 1..{len(nums)}"

    def _check_entry(self, r: Region, stem: str, n: kdl.Node):
        if n.name not in r.folder.files[stem]:
            yield "error", f"{stem} holds no {n.name!r} - it holds {', '.join(r.folder.files[stem])}"
            return
        if any(c.line != n.line for c in kdl.walk(n.children)):
            yield "error", f"{n.name} spans several lines - an entry is one line"
        code = n.args[0] if len(n.args) == 1 else None
        block = stem == "Blocks"
        if code is None or not (BLOCK_RE if block else CODE_RE).fullmatch(str(code)) or not str(code).startswith(r.code + "."):
            yield "error", (f"{n.name} opens with {n.args} - an entry opens with one {r.code} "
                            f"{'block id, a lower-case letter after the dot' if block else 'location code'}")
        elif stem not in ("Locations", "Blocks") and code not in r.locations():
            yield "error", f"{n.name} names {code}, which Locations.md does not hold"
        missing = list(self._check_node(r, n))
        owed = [m for m in missing if isinstance(m, str)]
        yield from (m for m in missing if not isinstance(m, str))
        if owed:
            step = "4a" if stem == "Locations" else "5a"
            yield "warning", f"{n.name} {n.args[0] if n.args else ''} is a stub owed to step {step} - lacks {', '.join(owed)}"

    def _check_node(self, r: Region, n: kdl.Node, within: str = ""):
        """Yield (severity, message) for every fault, and the name of every member not yet
        written - a bare entry is a stub, placed at 4c and filled at 5a."""
        members = r.folder.nodes[n.name]
        known = {m.name for m in members}
        for k in n.props:
            if k not in known:
                yield "error", f"{n.name} has no member {k!r}"
        for m in members:
            if m.name == "one-of":
                got = [c for c in n.children if c.name in m.nodes]
                if len(got) > 1:
                    yield "error", f"{n.name} holds {len(got)} of {' | '.join(m.nodes)} - at most one"
                elif not got and not m.opt:
                    yield within + " | ".join(m.nodes)
            elif m.name in n.props:
                for msg in self._check_value(r, m, n.props[m.name]):
                    yield msg[0], f"{n.name} {m.name}: {msg[1]}"
            elif not m.opt:
                yield within + m.name
        allowed = {c for m in members for c in m.nodes}
        for c in n.children:
            if c.name not in allowed:
                yield "error", f"{n.name} cannot hold {c.name!r}"
            elif c.args:
                yield "error", f"{c.name} inside {n.name} takes no arguments"
            else:
                yield from self._check_node(r, c, f"{within}{c.name}.")

    def _check_value(self, r: Region, m: Member, v):
        items = [x.strip() for x in str(v).split(",")] if m.is_list else [v]
        if m.n and len(items) != m.n:
            yield "error", f"{len(items)} items - expected {m.n}"
        for x in items:
            s = str(x)
            if m.type in self.schema.words:
                if not s.strip():
                    yield "error", "empty"
                elif len(s.split()) > self.schema.words[m.type]:
                    yield "error", f"{len(s.split())} words in {s!r} - a {m.type} is at most {self.schema.words[m.type]}"
            elif m.type == "number":
                b = bounds(s)
                if b is None:
                    yield "error", f"{s!r} is not N or N-M"
            elif m.type in ("feet", "distance"):
                if msg := unit_problem(m.type, s, r.folder.enums):
                    yield "error", msg
            elif m.type == "percent":
                if not PERCENT_RE.fullmatch(s) or int(s[:-1]) > 100:
                    yield "error", f"{s!r} is not a percentage"
            elif m.type == "location":
                if s not in self.codes:
                    yield "error", f"{s!r} is not a location code"
            elif m.type == "kind":
                if s not in r.folder.enums[r.folder.type]:
                    yield "error", f"{s!r} is not one of {', '.join(r.folder.enums[r.folder.type])}"
            elif m.type == "entry":
                yield from self._check_title(m.arg, s)
            elif m.type == "pull":
                table, _, title = s.partition(": ")
                if table not in r.folder.enums[m.arg]:
                    yield "error", f"{s!r} names no table in {m.arg}"
                elif (self.schema.tables[table][0] == "entry") != bool(title):
                    yield "error", (f"{s!r} - {table} is pulled as 'Table: Title'"
                                    if self.schema.tables[table][0] == "entry"
                                    else f"{s!r} - {table} is pulled by its name alone")
                elif title:
                    yield from self._check_title(table, title)
            elif s not in r.folder.enums[m.type]:
                yield "error", f"{s!r} is not one of {', '.join(r.folder.enums[m.type])}"

    def _check_title(self, table: str, title: str):
        have = self.titles(table)
        file = self.schema.tables[table][1]
        if have is None:
            yield "warning", f"{title!r} - {file} is not built yet"
        elif title not in have:
            yield "warning", f"{title!r} is not on {file} yet - owed to step 5a"

    def _check_rates(self, r: Region):
        rated = {s for rates in r.folder.rates.values() for s in rates} - {PROCEDURES}
        for code in r.locations():
            got = sum(1 for n in r.files.get(PROCEDURES, []) if n.args and n.args[0] == code)
            if got > 1:
                yield "warning", r.dir / f"{PROCEDURES}.md", f"{code} has {got} {PROCEDURES} entries - at most 1"
        for code, loc in r.locations().items():
            rates = r.folder.rates.get(loc.props.get("type"))
            if rates is None:
                continue
            for stem in sorted(rated):
                lo, hi = rates.get(stem, (0, 0))
                got = sum(1 for n in r.files.get(stem, []) if n.args and n.args[0] == code)
                if not lo <= got <= hi:
                    want = f"{lo}" if lo == hi else f"{lo}-{hi}"
                    yield "warning", r.dir / f"{stem}.md", (
                        f"{code} ({loc.props['type']}) has {got} {stem} entries - its rate is {want}")

    def _check_diagram(self, r: Region):
        if r.diagram is None:
            yield "warning", r.dir / "Connections.mmd", "missing - not built yet"
            return
        for i in sorted(r.unresolved):
            yield "error", r.diagram, f"edge names node id {i!r}, which no node defines"
        for c in sorted(set(r.nodes.values()) - self.codes):
            yield "error", r.diagram, f"node {c} is not a location"
        for c in sorted(set(r.locations()) - set(r.nodes.values())):
            yield "warning", r.diagram, f"{c} has no node yet"
        path = r.dir / "Connections.md"
        for n in r.files.get("Connections", []):
            to = n.props.get("to")
            if n.args and to and frozenset((n.args[0], to)) not in self.edges:
                yield "error", path, f"line {n.line}: {n.args[0]} to {to} is on no Connections.mmd"
        for a, b in r.edges:
            for near, far in ((a, b), (b, a)):
                if near.startswith(r.code + ".") and (near, far) not in self.connections:
                    yield "warning", path, f"{near} has no entry to {far} yet"

    def _check_joins(self, r: Region):
        """Each edge within the region joins types its folder's join lines allow, never two
        top types, and the way into a gated type carries its gate."""
        types = {c: n.props.get("type") for c, n in r.locations().items()}
        ways = {(n.args[0], n.props.get("to")): n for n in r.files.get("Connections", []) if n.args}
        for a, b in r.edges:
            if a not in types or b not in types:
                continue
            if {types[a], types[b]} <= r.folder.top:
                yield "error", r.diagram, (f"{a} ({types[a]}) connects to {b} ({types[b]}) - both are "
                                           f"reached from the region itself, so no edge is stated")
                continue
            for near, far in ((a, b), (b, a)):
                to = r.folder.joins.get(types[near], (None, None))[0]
                if to is not None and types[far] not in to:
                    yield "error", r.diagram, (f"{near} ({types[near]}) connects to {far} ({types[far]}) - "
                                               f"a {types[near]} connects only to {', '.join(sorted(to))}")
                    break
            for near, far in ((a, b), (b, a)):
                gate = r.folder.joins.get(types[near], (None, None))[1]
                way = ways.get((far, near))
                if gate and way is not None and not any(c.name == gate for c in way.children):
                    yield "error", r.dir / "Connections.md", (
                        f"line {way.line}: the way from {far} into {near} ({types[near]}) carries no {gate}")

    # -- one location ---------------------------------------------------------

    def entries_at(self, code: str) -> tuple[list, list]:
        """(file, entry) for every entry this location holds, and for every entry naming it."""
        own, named = [], []
        for r in self.regions.values():
            for stem, entries in r.files.items():
                for n in entries:
                    if n.args and n.args[0] == code:
                        own.append((f"{r.code}/{stem}", n))
                    elif any(code in [c.strip() for c in str(v).split(",")]
                             for node in kdl.walk([n]) for v in node.props.values()):
                        named.append((f"{r.code}/{stem}", n))
        return own, named


# -- BRIEF.md ------------------------------------------------------------------
#
# One kdl block: `files`, a node per schema folder (its `rate` lines are loaded by Schema),
# `setting`, and a `region` per region. A folder node's and a region node's targets are
# measured against the tables:
#
#   target Node.member Value="N%"|N ...  share, or count, of Node entries whose member is
#                                        each Value; a group of a type enum counts its items.
#                                        A share is a floor ("<=N%" a ceiling), a count exact
#                                        ("N+" a floor); a region's value replaces the rating's
#                                        value of the same key and leaves its others
#   target Node.Child "N%"               share of Node entries holding that one-of child
#   target Node [of=Type] "N%"           share of locations (of that type) holding a Node
#
# and a region's locations=N counts its Location entries. `files` and `setting` are
# measured against the setting files they govern.

BRIEF = ROOT / "BRIEF.md"
PROCEDURES = "Procedures"      # a region's own count, from its `procedure` lines, never a type's rate


def brief_nodes(path: Path = BRIEF) -> list[kdl.Node]:
    return kdl.fenced(path.read_text()) if path.exists() else []


SLICE_SETTING = ("test", "outline", "pressure")   # what a region's slice keeps of `setting`


def brief_slice(scope: str, path: Path = BRIEF) -> str | None:
    """BRIEF.md as one step reads it, None for an unknown scope. "setting": the prose,
    `files` and `setting`. A region code: the prose, its rating's node, `setting`'s
    test, outline and pressure, and its own node."""
    nodes = brief_nodes(path)
    if not nodes:
        return None
    lines = path.read_text().splitlines()
    fence = nodes[0].line - 1
    while lines[fence].strip() != "```kdl":
        fence -= 1

    def span(seq, i, stop):
        """Node i's own lines, up to the next node or line `stop`, without the blanks
        and comments between."""
        out = lines[seq[i].line - 1:seq[i + 1].line - 1 if i + 1 < len(seq) else stop]
        while out and (not out[-1].strip() or out[-1].lstrip().startswith("//")):
            out.pop()
        return out

    end = fence + 1 + next(i for i, l in enumerate(lines[fence + 1:]) if l.strip() == "```")
    chunks = {(n.name, str(n.args[0]) if n.name == "region" and n.args else None): i
              for i, n in enumerate(nodes)}
    whole = lambda name, arg=None: span(nodes, chunks[name, arg], end)
    if scope == "setting":
        keep = [whole(k) for k in ("files", "setting") if (k, None) in chunks]
    elif ("region", scope) in chunks:
        rating = str(nodes[chunks["region", scope]].props.get("rating", "")).lower()
        keep = [whole(rating)] if (rating, None) in chunks else []
        if ("setting", None) in chunks:
            node, own = nodes[chunks["setting", None]], whole("setting")
            close = node.line - 2 + len(own)       # the line of its closing brace
            keep.append([own[0]] + [l for j, c in enumerate(node.children) if c.name in SLICE_SETTING
                                    for l in span(node.children, j, close)] + [own[-1]])
        keep.append(whole("region", scope))
    else:
        return None
    body = "\n\n".join("\n".join(k) for k in keep)
    return "\n".join(lines[:fence]).rstrip() + f"\n\n```kdl\n{body}\n```\n"


@dataclass
class Target:
    node: kdl.Node
    path: str
    form: str                      # "values", "child", "presence" or "count"
    wants: dict[str, str]          # value -> "N%" share, or N or "N-M" count
    rating: str | None
    region: str | None

    def key(self):
        return (self.path, self.form, self.node.props.get("of"))

    def applies(self, r: Region) -> int:
        """-1 where it does not apply to this region, else its narrowness."""
        if self.region and self.region != r.code:
            return -1
        if self.rating and self.rating.lower() != r.rating.lower():
            return -1
        return 2 if self.region else 1 if self.rating else 0


class Brief:
    def __init__(self, schema: Schema, path: Path = BRIEF):
        self.schema, self.path, self.problems = schema, path, list(schema.brief_problems)
        self.targets, self.regions = [], {}
        self.files = self.setting = None
        try:
            nodes = brief_nodes(path)
        except SyntaxError:
            return
        folders = {f.lower(): f for f in schema.folders}
        for n in nodes:
            p = lambda msg, n=n: self.problems.append(f"line {n.line}: {msg}")
            if n.name in folders:
                for c in n.children:
                    if c.name == "target":
                        self._add(c, folders[n.name], None)
                    elif c.name != "rate":
                        p(f"{n.name} holds rate and target lines, not {c.name!r}")
            elif n.name == "region":
                code = str(n.args[0]) if n.args else ""
                rating = str(n.props.get("rating", "")).title()
                if not re.fullmatch(r"[A-Z]+", code) or rating not in schema.folders:
                    p(f"a region opens with its code and rating={' | '.join(f.upper() for f in schema.folders)}")
                    continue
                self.regions[code] = n
                for c in n.children:
                    if c.name == "target":
                        self._add(c, rating, code)
                if "locations" in n.props:
                    if bounds(n.props["locations"]) is None:
                        p("locations= is a count or range")
                    else:
                        self.targets.append(Target(n, "Location", "count",
                                                   {"": str(n.props["locations"])}, None, code))
            elif n.name in ("files", "setting"):
                setattr(self, n.name, n)
            else:
                p(f"{n.name!r} is not files, setting, region or {', '.join(folders)}")

    def _add(self, n: kdl.Node, rating: str, region: str | None):
        if t := self._read(n, rating, region):
            self.targets.append(t)

    def _read(self, n: kdl.Node, rating: str, region: str | None) -> Target | None:
        p = lambda msg: self.problems.append(f"line {n.line}: {msg}") or None
        if not n.args:
            return p("a target names a Node or Node.member")
        path, *rest = [str(a) for a in n.args]
        node, _, member = path.partition(".")
        f = self.schema.folders[rating]
        if node not in f.nodes:
            return p(f"{node!r} is not a node of {f.path.name}")
        values = {k: str(v) for k, v in n.props.items() if k != "of"}
        members = {m.name: m for m in f.nodes[node] if m.name != "one-of"}
        children = {c for m in f.nodes[node] for c in m.nodes}
        if member in members:
            if rest or not values:
                return p(f"{path} takes Value=\"N%\" shares or Value=N counts")
            allowed = self._allowed(members[member], rating)
            bad = [v for v in values if allowed is not None and v not in allowed]
            if bad:
                return p(f"{', '.join(map(repr, bad))} not a value of {path}")
            form = "values"
        elif member in children or not member:
            if values or len(rest) != 1:
                return p(f"{path} takes one \"N%\" share")
            values, form = {"": rest[0]}, "child" if member else "presence"
            of = n.props.get("of")
            if of and (member or of not in f.enums.get(f.type, {})):
                return p(f"of={of!r} is not a {rating} location type")
        else:
            return p(f"{member!r} is neither a member nor a child of {node}")
        for v, s in values.items():
            if not (SHARE_RE.fullmatch(s) or (form == "values" and entries_allowed(s) is not None)):
                return p(f"{s!r} is not a share" + (" or a count" if form == "values" else "")
                         + ': "N%" at least, "<=N%" at most')
        if sum(int(s[:-1]) for s in values.values() if PERCENT_RE.fullmatch(s)) > 100:
            return p("shares total over 100%")
        return Target(n, path, form, values, rating, region)

    def _groups(self, rating: str) -> dict[str, set]:
        out = {}
        f = self.schema.folders[rating]
        for item, g in f.enums.get(f.type, {}).items():
            out.setdefault(g, set()).add(item)
        return out

    def _allowed(self, m: Member, rating: str) -> set | None:
        f = self.schema.folders[rating]
        if m.type == "kind":
            return set(f.enums[f.type]) | set(self._groups(rating))
        if m.type in f.enums:
            return set(f.enums[m.type])
        if m.type == "pull":
            return set(f.enums.get(m.arg, {}))
        return None

    def realized(self, setting: Setting):
        """Per region, (target, label, wanted, got, of) for every target value applying to
        it; of is None where wanted is a count. A narrower target replaces a wider one's
        value of the same key, never its other values."""
        out = {}
        for r in setting.regions.values():
            best = {}
            for t in self.targets:
                rank = t.applies(r)
                for v in t.wants:
                    k = t.key() + (v,)
                    if rank >= 0 and rank >= best.get(k, (None, -1))[1]:
                        best[k] = (t, rank)
            won = {}
            for k, (t, _) in best.items():
                won.setdefault(id(t), (t, set()))[1].add(k[-1])
            out[r.code] = [row for t, vs in won.values() for row in self._measure(t, r, vs)]
        return out

    def _measure(self, t: Target, r: Region, only: set[str]):
        node, _, member = t.path.partition(".")
        entries = [n for ns in r.files.values() for top in ns for n in kdl.walk([top])
                   if n.name == node]
        if t.form == "count":
            return [(t, "count", t.wants[""], len(entries), None)]
        if t.form == "values":
            got = [str(n.props.get(member, "")).split(":")[0] for n in entries if member in n.props]
            groups = self._groups(t.rating) if t.rating in self.schema.folders else {}
            return [(t, v, s, sum(1 for g in got if g in groups.get(v, {v})),
                     len(got) if SHARE_RE.fullmatch(s) else None)
                    for v, s in t.wants.items() if v in only]
        if t.form == "child":
            got = sum(1 for n in entries if any(c.name == member for c in n.children))
            return [(t, member, t.wants[""], got, len(entries))]
        of = t.node.props.get("of")
        locs = [c for c, l in r.locations().items() if not of or l.props.get("type") == of]
        held = {n.args[0] for n in entries if n.args}
        return [(t, f"of {of}" if of else "of all", t.wants[""],
                 sum(1 for c in locs if c in held), len(locs))]

    # -- the setting files ------------------------------------------------------

    def lever(self, name: str) -> kdl.Node | None:
        """A `files` lever by name, e.g. Treasure."""
        return next((c for c in (self.files.children if self.files else []) if c.name == name), None)

    def asks(self, name: str) -> list[kdl.Node]:
        """Every `setting` line of one kind, e.g. tongue."""
        return [c for c in (self.setting.children if self.setting else []) if c.name == name]

    def setting_rows(self) -> list[tuple[str, str, str, bool]]:
        """(lever, wanted, got, off) for every files and setting lever a count can test,
        over the setting files built so far."""
        import site_common as sc
        rows = []

        def count(label, wanted, got):
            b = bounds(wanted)
            rows.append((label, str(wanted), str(got), b is None or not b[0] <= got <= b[1]))

        def shares(label, wants, got: list[str]):
            for v, s in wants.items():
                n = sum(1 for g in got if g == v)
                want = int(str(s)[:-1]) * len(got) / 100
                rows.append((f"{label} {v}", str(s), f"{n} of {len(got)}", abs(n - want) > 1))

        def table(name) -> list[dict]:
            path = SETTING / name
            ts = sc.read_tables(path) if path.exists() else []
            return ts[0].dicts() if ts else []

        def num(s) -> float | None:
            m = re.match(r"\s*(\d+)", str(s))
            return float(m.group(1)) if m else None

        if t := self.lever("Treasure"):
            tabs = {r: table(f"Treasure{i}.md") for i, r in enumerate(("I", "II", "III", "IV", "V"), 1)}
            values = {r: [v for d in ds if (v := num(d.get("Value"))) is not None] for r, ds in tabs.items()}
            for c in t.children:
                if c.name == "average":
                    for r, want in c.props.items():
                        if values.get(r):
                            mean = sum(values[r]) / len(values[r])
                            b = bounds(want)
                            rows.append((f"Treasure {r} mean", str(want), f"{mean:.0f}",
                                         b is None or not b[0] <= mean <= b[1]))
                elif c.name == "quality":
                    r = str(c.props.get("table", "II"))
                    shares(f"Treasure {r} quality", {k: v for k, v in c.props.items() if k != "table"},
                           [d.get("Quality", "").lower() for d in tabs.get(r, [])])
                elif c.name == "effect":
                    for q, s in c.props.items():
                        has = [d.get("Effect", "-").strip() not in ("-", "") for d in tabs["II"]
                               if d.get("Quality", "").lower() == q]
                        shares(f"Treasure II {q}", {"with an effect": s},
                               ["with an effect" if h else "" for h in has])
                elif c.name == "price" and "normal" in c.props:
                    base = float(c.props["normal"])
                    for q, rng in c.props.items():
                        b = bounds(str(rng).rstrip("x")) if q != "normal" else None
                        if b:
                            got = [num(d.get("Value")) / base for d in tabs["II"]
                                   if d.get("Quality", "").lower() == q and num(d.get("Value"))]
                            out = sum(1 for g in got if not b[0] <= g <= b[1])
                            rows.append((f"Treasure II {q} price", f"{rng} of {c.props['normal']}",
                                         f"{len(got) - out} of {len(got)} in range", out > 0))
            if "ceiling" in t.props:
                for r, vs in values.items():
                    if vs:
                        top = max(vs) / (sum(vs) / len(vs))
                        rows.append((f"Treasure {r} highest", f"{t.props['ceiling']}x mean",
                                     f"{top:.1f}x", top > float(t.props["ceiling"])))
        if r := self.lever("Rumours"):
            ds = table("Rumours.md")
            if ds:
                if "die" in r.props:
                    count("Rumours rows", r.props["die"], len(ds))
                marks = {k: f"{v}" for k, v in r.props.items() if k in ("T", "P", "F", "U")}
                got = [d.get("T/P/F/U", "") for d in ds]
                for k, v in marks.items():
                    count(f"Rumours marked {k}", v, sum(1 for g in got if g == k))
        records = lambda f: sc.read_records(SETTING / f) if (SETTING / f).exists() else None
        for lever, file, prop in (("Factions", "Factions.md", "count"), ("History", "History.md", "events")):
            if (n := self.lever(lever)) and prop in n.props and (rs := records(file)) is not None:
                count(f"{lever} entries", n.props[prop], len(rs))
        for lever, file in (("Quests", "Quests.md"), ("Truths", "Truths.md")):
            if (n := self.lever(lever)) and "count" in n.props and (SETTING / file).exists():
                count(f"{lever} entries", n.props["count"], len(table(file)))
        if (SETTING / "Language.md").exists():
            tongues = self._tongues(SETTING / "Language.md")
            if self.asks("tongue"):
                count("Language tongues", len(self.asks("tongue")), len(tongues))
            if n := self.lever("Language"):
                for name, (affixes, roots) in tongues.items():
                    if "affixes" in n.props:
                        count(f"Language {name} affixes", n.props["affixes"], affixes)
                    if "roots" in n.props:
                        count(f"Language {name} roots", n.props["roots"], roots)
        have = titles(SETTING / "Bestiary.md")
        for n in self.asks("bestiary"):
            for name in n.args:
                if have is not None:
                    rows.append((f"Bestiary up front {name}", "present",
                                 "present" if name in have else "missing", name not in have))
        for code, n in self.regions.items():
            people = SETTING / "region" / code / "People.md"
            if "people" in n.props and people.exists():
                count(f"{code} People", n.props["people"],
                      sum(1 for e in kdl.fenced(people.read_text()) if e.name == "Person"))
        return rows

    @staticmethod
    def _tongues(path: Path) -> dict[str, tuple[int, int]]:
        """Each `## ` tongue: how many affixes its Affixes field lists, and how many roots."""
        out, name, label, affixes, roots = {}, None, None, "", 0
        for line in path.read_text().splitlines() + ["## "]:
            if line.startswith("## "):
                if name:
                    out[name] = (len([a for a in affixes.split(";") if a.strip()]), roots)
                name, label, affixes, roots = line[3:].strip(), None, "", 0
            elif m := re.match(r"^([A-Z][A-Za-z ]*):\s*(.*)$", line):
                label = m.group(1)
                if label == "Affixes":
                    affixes = m.group(2)
            elif label == "Affixes":
                affixes += " " + line.strip()
            elif label == "Roots" and line.startswith("- "):
                roots += 1
        return out

    def procedure_problems(self, setting: Setting) -> list[str]:
        """Each region's Procedure entries against its `procedure` lines in BRIEF.md."""
        out = []
        for code, n in self.regions.items():
            r = setting.regions.get(code)
            if r is None or r.folder is None or not (r.dir / f"{PROCEDURES}.md").exists():
                continue
            asked = sum(1 for c in n.children if c.name == "procedure")
            held = len(r.files.get(PROCEDURES, []))
            if held != asked:
                out.append(f"{code} has {held} Procedure entries; BRIEF.md asks for {asked} procedure lines")
        return out

    def region_problems(self, gazetteer: dict[str, dict]) -> list[str]:
        """Each region BRIEF.md names against setting/region/Regions.md: same codes, in
        order, each with the rating and die asked for."""
        if not gazetteer or not self.regions:
            return []
        out = []
        if list(self.regions) != list(gazetteer):
            out.append(f"BRIEF.md names regions {', '.join(self.regions)}; the gazetteer holds "
                       f"{', '.join(gazetteer)}")
        for code, n in self.regions.items():
            g = gazetteer.get(code)
            for k in ("rating", "die"):
                if g and k in n.props and str(n.props[k]).upper() != str(g.get(k, "")).upper():
                    out.append(f"{code} is {k} {g.get(k)!r}; BRIEF.md asks for {n.props[k]!r}")
        return out


# -- staleness ------------------------------------------------------------------
#
# A write-up is stale when a line it was written from - its own entries, the entries
# naming it, the setting entries those name, or its region's seed - changed after the
# write-up last did. A line's time is its last commit's, read by `git blame`, or its
# file's modified time while the line is uncommitted. Without git, nothing is stale.

import os
import subprocess


class History:
    def __init__(self):
        self._blame: dict[Path, list[float] | None] = {}

    def _git(self, *args) -> str | None:
        try:
            return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                                  text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            return None

    def line_times(self, path: Path) -> list[float] | None:
        if path not in self._blame:
            out = self._git("blame", "--line-porcelain", "--", str(path.relative_to(ROOT)))
            times, uncommitted = [], False
            for line in (out or "").splitlines():
                if re.match(r"[0-9a-f]{40} ", line):
                    uncommitted = line.startswith("0" * 40)
                elif line.startswith("committer-time "):
                    times.append(path.stat().st_mtime if uncommitted else float(line.split()[1]))
            self._blame[path] = times if out is not None else None
        return self._blame[path]

    def file_time(self, path: Path) -> float | None:
        dirty = self._git("status", "--porcelain", "--", str(path.relative_to(ROOT)))
        if dirty is None:
            return None
        if dirty.strip():
            return path.stat().st_mtime
        out = self._git("log", "-1", "--format=%ct", "--", str(path.relative_to(ROOT)))
        return float(out) if out and out.strip() else path.stat().st_mtime


def record_lines(path: Path, title: str) -> range:
    """The lines of one setting entry: its table row, or its heading through to the next."""
    lines = path.read_text().splitlines()
    for i, line in enumerate(lines):
        if title in line:
            if not line.startswith("#"):
                return range(i, i + 1)
            depth = len(line) - len(line.lstrip("#"))
            end = next((j for j in range(i + 1, len(lines))
                        if lines[j].startswith("#") and len(lines[j]) - len(lines[j].lstrip("#")) <= depth),
                       len(lines))
            return range(i, end)
    return range(0)


def stale(setting: Setting, code: str, history: History) -> list[str]:
    """What changed since this location's write-up, or [] if it is fresh or unwritten."""
    region = setting.regions[code.split(".")[0]]
    writeup = region.dir / f"{code.split('.')[1]}.md"
    if not writeup.exists() or (written := history.file_time(writeup)) is None:
        return []
    deps: list[tuple[Path, range, str]] = []
    own, named = setting.entries_at(code)
    for where, n in own + named:
        rcode, stem = where.split("/")
        deps.append((setting.regions[rcode].dir / f"{stem}.md", range(n.line - 1, n.line),
                     f"{stem} {n.name} {n.args[0] if n.args else ''}".strip()))
        folder = setting.regions[rcode].folder
        for node in kdl.walk([n]):
            for m in (folder.nodes.get(node.name, []) if folder else []):
                v = node.props.get(m.name)
                if v is None or m.type not in ("entry", "pull"):
                    continue
                table, _, title = str(v).partition(": ") if m.type == "pull" else (m.arg, "", str(v))
                if title and table in setting.schema.tables:
                    path = ROOT / setting.schema.tables[table][1]
                    if path.exists():
                        deps.append((path, record_lines(path, title), f"{table}: {title}"))
    seed = SETTING / "region" / f"{region.code}.md"
    if seed.exists():
        deps.append((seed, range(0, 10 ** 6), "the region's seed"))
    changed = []
    for path, lines, what in deps:
        times = history.line_times(path)
        if times and any(times[i] > written for i in lines if i < len(times)):
            changed.append(what)
    return sorted(set(changed))


def stale_brief(region: Region, history: History) -> list[str]:
    """The table files and seed changed since the region's brief, or [] if it is fresh or
    unwritten."""
    brief = region.dir / "Brief.md"
    if not brief.exists() or (written := history.file_time(brief)) is None:
        return []
    deps = [region.dir / f"{stem}.md" for stem in region.files] + [SETTING / "region" / f"{region.code}.md"]
    return sorted(p.name for p in deps if p.exists() and any(
        tm > written for tm in history.line_times(p) or []))
