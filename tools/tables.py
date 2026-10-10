"""Location tables: patterns/Schema.md loaded, every region's tables read and checked
against it, and one location's entries gathered."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import kdl

ROOT = Path(__file__).resolve().parent.parent
SETTING = ROOT / "setting"
SCHEMA = ROOT / "patterns" / "Schema.md"

CODE_RE = re.compile(r"([A-Z]+)\.(\d+)")
RANGE_RE = re.compile(r"(\d+)(?:-(\d+))?")
PERCENT_RE = re.compile(r"(\d+)%")
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


@dataclass
class Folder:
    type: str
    files: dict[str, list[str]]
    rates: dict[str, dict[str, tuple[int, int]]]


def bounds(rate) -> tuple[int, int] | None:
    s = str(rate)
    if m := PERCENT_RE.fullmatch(s):
        return (0, 1) if int(m.group(1)) <= 100 else None
    if m := RANGE_RE.fullmatch(s):
        lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
        return (lo, hi) if lo <= hi else None
    return None


class Schema:
    def __init__(self, path: Path = SCHEMA):
        self.path, self.problems = path, []
        self.words, self.values, self.tables = {}, set(), {}
        self.enums, self.nodes, self.folders = {}, {}, {}
        try:
            top = kdl.fenced(path.read_text())
        except (OSError, SyntaxError) as e:
            self.problems.append(str(e))
            return
        for n in top:
            name = n.args[0] if n.args else None
            if n.name == "value":
                self.values.add(name)
                if "words" in n.props:
                    self.words[name] = n.props["words"]
            elif n.name == "table":
                self.tables[name] = (n.args[1], n.props["file"])
            elif n.name == "enum":
                items = {a: None for a in n.args[1:]}
                for g in n.children:
                    items.update({a: g.name for a in g.args})
                self.enums[name] = items
            elif n.name == "node":
                self.nodes[name] = [self._member(c) for c in n.children]
            elif n.name == "folder":
                files = {c.name: c.args for c in n.children if c.name != "rate"}
                rates = {c.args[0]: {f: bounds(r) for f, r in c.props.items()}
                         for c in n.children if c.name == "rate"}
                self.folders[name] = Folder(n.props.get("type", ""), files, rates)
            else:
                self.problems.append(f"line {n.line}: unknown schema node {n.name!r}")
        self._resolve()

    @staticmethod
    def _member(c) -> Member:
        flags = {"opt", "list"}
        if c.name == "one-of":
            return Member("one-of", opt="opt" in c.args, nodes=[a for a in c.args if a not in flags])
        rest = [a for a in c.args[1:] if a not in flags]
        return Member(c.name, c.args[0], rest[0] if rest else None, "opt" in c.args,
                      "list" in c.args, c.props.get("n"))

    def _resolve(self):
        p = self.problems.append
        for node, members in self.nodes.items():
            for m in members:
                for child in m.nodes:
                    if child not in self.nodes:
                        p(f"{node}: one-of names unknown node {child!r}")
                if m.name == "one-of":
                    continue
                if m.type not in self.values and m.type not in self.enums:
                    p(f"{node}.{m.name}: unknown type {m.type!r}")
                if m.type == "entry" and m.arg not in self.tables:
                    p(f"{node}.{m.name}: unknown table {m.arg!r}")
                if m.type == "pull" and not set(self.enums.get(m.arg, {"?": 0})) <= set(self.tables):
                    p(f"{node}.{m.name}: {m.arg!r} is not an enum of tables")
        for name, f in self.folders.items():
            if f.type not in self.enums:
                p(f"folder {name}: unknown type enum {f.type!r}")
            for stem, nodes in f.files.items():
                for n in nodes:
                    if n not in self.nodes:
                        p(f"folder {name}: {stem} holds unknown node {n!r}")
            for item, rates in f.rates.items():
                if item not in self.enums.get(f.type, {}):
                    p(f"folder {name}: rate for {item!r}, which {f.type} does not hold")
                for stem, b in rates.items():
                    if stem not in f.files or b is None:
                        p(f"folder {name}: rate {item} {stem} is not a file and a count, range or percent")


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
        """Yield (severity, path, message) for every region."""
        for r in self.regions.values():
            yield from self._check_region(r)

    def _check_region(self, r: Region):
        for path, msg in r.syntax:
            yield "error", path, msg
        if r.folder is None:
            yield "warning", r.dir, f"{r.rating} has no folder in {self.schema.path.name}"
            return
        for path in sorted(r.dir.glob("*.md")):
            if not path.stem.isdigit() and path.stem not in r.folder.files:
                yield "error", path, f"is neither a location file nor one of {', '.join(r.folder.files)}"
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
        yield from self._check_diagram(r)

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
        if code is None or not CODE_RE.fullmatch(str(code)) or not str(code).startswith(r.code + "."):
            yield "error", f"{n.name} opens with {n.args} - an entry opens with one {r.code} location code"
        elif stem != "Locations" and code not in r.locations():
            yield "error", f"{n.name} names {code}, which Locations.md does not hold"
        yield from self._check_node(r, n)

    def _check_node(self, r: Region, n: kdl.Node):
        members = self.schema.nodes[n.name]
        if not n.props and not n.children:
            yield "error", f"{n.name} is empty"
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
                    yield "warning", f"{n.name} lacks {' | '.join(m.nodes)}"
            elif m.name in n.props:
                for msg in self._check_value(r, m, n.props[m.name]):
                    yield msg[0], f"{n.name} {m.name}: {msg[1]}"
            elif not m.opt:
                yield "warning", f"{n.name} lacks {m.name}"
        allowed = {c for m in members for c in m.nodes}
        for c in n.children:
            if c.name not in allowed:
                yield "error", f"{n.name} cannot hold {c.name!r}"
            elif c.args:
                yield "error", f"{c.name} inside {n.name} takes no arguments"
            else:
                yield from self._check_node(r, c)

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
                if b is None or "%" in s:
                    yield "error", f"{s!r} is not N or N-M"
            elif m.type == "percent":
                if not PERCENT_RE.fullmatch(s) or int(s[:-1]) > 100:
                    yield "error", f"{s!r} is not a percentage"
            elif m.type == "location":
                if s not in self.codes:
                    yield "error", f"{s!r} is not a location code"
            elif m.type == "kind":
                if s not in self.schema.enums[r.folder.type]:
                    yield "error", f"{s!r} is not one of {', '.join(self.schema.enums[r.folder.type])}"
            elif m.type == "entry":
                yield from self._check_title(m.arg, s)
            elif m.type == "pull":
                table, _, title = s.partition(": ")
                if table not in self.schema.enums[m.arg]:
                    yield "error", f"{s!r} names no table in {m.arg}"
                elif (self.schema.tables[table][0] == "entry") != bool(title):
                    yield "error", (f"{s!r} - {table} is pulled as 'Table: Title'"
                                    if self.schema.tables[table][0] == "entry"
                                    else f"{s!r} - {table} is pulled by its name alone")
                elif title:
                    yield from self._check_title(table, title)
            elif s not in self.schema.enums[m.type]:
                yield "error", f"{s!r} is not one of {', '.join(self.schema.enums[m.type])}"

    def _check_title(self, table: str, title: str):
        have = self.titles(table)
        file = self.schema.tables[table][1]
        if have is None:
            yield "warning", f"{title!r} - {file} is not built yet"
        elif title not in have:
            yield "warning", f"{title!r} is not on {file} yet"

    def _check_rates(self, r: Region):
        rated = {s for rates in r.folder.rates.values() for s in rates}
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
        if "Connections" not in r.folder.files:
            return
        path = r.dir / "Connections.md"
        for n in r.files.get("Connections", []):
            to = n.props.get("to")
            if n.args and to and frozenset((n.args[0], to)) not in self.edges:
                yield "error", path, f"line {n.line}: {n.args[0]} to {to} is on no Connections.mmd"
        for a, b in r.edges:
            for near, far in ((a, b), (b, a)):
                if near.startswith(r.code + ".") and (near, far) not in self.connections:
                    yield "warning", path, f"{near} has no Connection to {far} yet"

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
