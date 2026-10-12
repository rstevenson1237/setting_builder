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
    joins: dict[str, tuple[set[str], str | None]] = field(default_factory=dict)


def bounds(rate) -> tuple[int, int] | None:
    s = str(rate)
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
                files = {c.name: c.args for c in n.children if c.name not in ("rate", "join")}
                rates = {a: {f: bounds(r) for f, r in c.props.items()}
                         for c in n.children if c.name == "rate" for a in c.args}
                joins = {c.args[0]: (set(c.args[1:]), c.props.get("gate"))
                         for c in n.children if c.name == "join" and c.args}
                self.folders[name] = Folder(n.props.get("type", ""), files, rates, joins)
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
                        p(f"folder {name}: rate {item} {stem} is not a file and a count or range")
            for item, (to, gate) in f.joins.items():
                for t in {item} | to:
                    if t not in self.enums.get(f.type, {}):
                        p(f"folder {name}: join names {t!r}, which {f.type} does not hold")
                if gate and gate not in self.nodes:
                    p(f"folder {name}: join gate {gate!r} is not a node")
            if f.joins and "Connections" not in f.files:
                p(f"folder {name}: join without a Connections file")


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
        """Yield (severity, path, message) for every region, then for the keys between them."""
        for r in self.regions.values():
            yield from self._check_region(r)
        yield from self._check_keys()

    def _check_keys(self):
        """Every lock has its key placed, every key its lock, and no key lies behind the lock
        it opens. Locks are placed first and keys for them after, so a lock waiting on its
        key is owed to 5d, and a key with no lock is an error."""
        locks, keys = {}, {}
        for r in self.regions.values():
            for stem, entries in r.files.items():
                for n in entries:
                    for c in n.children:
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
                                                       f"placed yet - owed to step 5d")
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
        if code is None or not CODE_RE.fullmatch(str(code)) or not str(code).startswith(r.code + "."):
            yield "error", f"{n.name} opens with {n.args} - an entry opens with one {r.code} location code"
        elif stem != "Locations" and code not in r.locations():
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
        members = self.schema.nodes[n.name]
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
        """Each edge within the region joins types its folder's join lines allow, and the
        way into a gated type carries its gate."""
        types = {c: n.props.get("type") for c, n in r.locations().items()}
        ways = {(n.args[0], n.props.get("to")): n for n in r.files.get("Connections", []) if n.args}
        for a, b in r.edges:
            if a not in types or b not in types:
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


# -- BRIEF.md's targets --------------------------------------------------------
#
#   target Node.member Value="N%" ...   share of Node entries whose member is each Value
#   target Node.Child "N%"              share of Node entries holding that one-of child
#   target Node [of=Type] "N%"          share of locations (of that type) holding a Node
#   target Node count=N                 how many Node entries
#
# each scoped by rating= and region=, the narrowest applying to a region winning.

BRIEF = ROOT / "BRIEF.md"


@dataclass
class Target:
    node: kdl.Node
    path: str
    form: str                      # "values", "child", "presence" or "count"
    shares: dict[str, int]
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


class Targets:
    def __init__(self, schema: Schema, path: Path = BRIEF):
        self.schema, self.path, self.problems, self.targets = schema, path, [], []
        try:
            nodes = kdl.fenced(path.read_text()) if path.exists() else []
        except SyntaxError as e:
            self.problems.append(str(e))
            return
        for n in nodes:
            if n.name != "target":
                self.problems.append(f"line {n.line}: {n.name!r} is not a target")
            elif t := self._read(n):
                self.targets.append(t)

    def _read(self, n: kdl.Node) -> Target | None:
        p = lambda msg: self.problems.append(f"line {n.line}: {msg}") or None
        if not n.args:
            return p("a target names a Node or Node.member")
        path, *rest = [str(a) for a in n.args]
        node, _, member = path.partition(".")
        if node not in self.schema.nodes:
            return p(f"{node!r} is not a node of patterns/Schema.md")
        rating, region = n.props.get("rating"), n.props.get("region")
        if rating and rating not in self.schema.folders:
            return p(f"rating={rating!r} is not a folder of patterns/Schema.md")
        values = {k: v for k, v in n.props.items() if k not in ("rating", "region", "of", "count")}
        members = {m.name: m for m in self.schema.nodes[node] if m.name != "one-of"}
        children = {c for m in self.schema.nodes[node] for c in m.nodes}
        if "count" in n.props:
            if member or values or rest or bounds(n.props["count"]) is None:
                return p("count= takes a bare Node and a count or range")
            return Target(n, path, "count", {}, rating, region)
        if member in members:
            if rest or not values:
                return p(f"{path} takes Value=\"N%\" shares")
            allowed = self._allowed(members[member], rating)
            bad = [v for v in values if allowed is not None and v not in allowed]
            if bad:
                return p(f"{', '.join(map(repr, bad))} not a value of {path}")
            form = "values"
        elif member in children or not member:
            if values or len(rest) != 1:
                return p(f"{path} takes one \"N%\" share")
            values, form = {"": rest[0]}, "child" if member else "presence"
            if member and "of" in n.props:
                return p("of= applies to a bare Node")
            of = n.props.get("of")
            if of and not any(of in self.schema.enums.get(f.type, {})
                              for f in self.schema.folders.values()):
                return p(f"of={of!r} is not a location type")
        else:
            return p(f"{member!r} is neither a member nor a child of {node}")
        shares = {}
        for v, s in values.items():
            m = PERCENT_RE.fullmatch(str(s))
            if not m:
                return p(f"{s!r} is not a percentage")
            shares[v] = int(m.group(1))
        if sum(shares.values()) > 100:
            return p(f"shares total {sum(shares.values())}%")
        return Target(n, path, form, shares, rating, region)

    def _allowed(self, m: Member, rating: str | None) -> set | None:
        if m.type == "kind":
            folders = [self.schema.folders[rating]] if rating else self.schema.folders.values()
            return {v for f in folders for v in self.schema.enums.get(f.type, {})}
        if m.type in self.schema.enums:
            return set(self.schema.enums[m.type])
        if m.type == "pull":
            return set(self.schema.enums.get(m.arg, {}))
        return None

    def realized(self, setting: Setting):
        """Per region, (target, label, wanted, got, of) for every target applying to it."""
        out = {}
        for r in setting.regions.values():
            best = {}
            for t in self.targets:
                rank = t.applies(r)
                if rank >= 0 and rank >= best.get(t.key(), (None, -1))[1]:
                    best[t.key()] = (t, rank)
            rows = []
            for t, _ in best.values():
                rows += self._measure(t, r)
            out[r.code] = rows
        return out

    def _measure(self, t: Target, r: Region):
        node, _, member = t.path.partition(".")
        entries = [n for ns in r.files.values() for top in ns for n in kdl.walk([top])
                   if n.name == node]
        if t.form == "count":
            return [(t, "count", str(t.node.props["count"]), len(entries), None)]
        if t.form == "values":
            got = [str(n.props.get(member, "")).split(":")[0] for n in entries
                   if member in n.props]
            return [(t, v, s, sum(1 for g in got if g == v), len(got)) for v, s in t.shares.items()]
        if t.form == "child":
            got = sum(1 for n in entries if any(c.name == member for c in n.children))
            return [(t, member, t.shares[""], got, len(entries))]
        of = t.node.props.get("of")
        locs = [c for c, l in r.locations().items() if not of or l.props.get("type") == of]
        held = {n.args[0] for n in entries if n.args}
        return [(t, f"of {of}" if of else "of all", t.shares[""],
                 sum(1 for c in locs if c in held), len(locs))]


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
        for node in kdl.walk([n]):
            for m in setting.schema.nodes.get(node.name, []):
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
