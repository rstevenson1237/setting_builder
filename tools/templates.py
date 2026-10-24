"""templates/: each generation template's ```kdl fence under `## Context` - the scope it is
written for, what it writes and in what shape, and what it reads, down to the members a
field reads - checked against templates/Template_Schema.md and patterns/, and drawn as the
skeleton of what a step writes."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import kdl
import tables as tb

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
TEMPLATE_SCHEMA = TEMPLATES / "Template_Schema.md"


def _grammar() -> tuple[dict[str, list[str]], dict[str, kdl.Node]]:
    """Template_Schema.md's enums, and its nodes by name."""
    enums, nodes = {}, {}
    for n in kdl.fenced(TEMPLATE_SCHEMA.read_text()):
        if n.name == "enum" and n.args:
            enums[str(n.args[0])] = [str(a) for a in n.args[1:]]
        elif n.name == "node" and n.args:
            nodes[str(n.args[0])] = n
    return enums, nodes


ENUMS, GRAMMAR = _grammar()
STANDING = tuple(ENUMS["Standing"])
SCOPES, SHAPES, RUNS = tuple(ENUMS["Scope"]), tuple(ENUMS["Shape"]), tuple(ENUMS["Run"])
NODES = tuple(GRAMMAR)
LINES = tuple(next(c.args for c in GRAMMAR["step"].children if c.name == "one-of"))   # what a step holds
LENGTH_UNITS = tuple(c.name for c in GRAMMAR["field"].children if c.args[:1] == ["length"])


def members(node: str) -> dict[str, kdl.Node]:
    """A node's properties as Template_Schema.md defines them: every member but its `arg=`."""
    g = GRAMMAR[node]
    return {c.name: c for c in g.children if c.name not in ("one-of", g.props.get("arg"))}


LENGTH_RE = re.compile(r"(\d+)?(-(\d+)?|\+)?")
PLACEHOLDER_RE = re.compile(r"\[[^\]]+\]|\*")


@dataclass
class Template:
    path: Path
    nodes: list[kdl.Node]

    @property
    def head(self) -> kdl.Node | None:
        return next((n for n in self.nodes if n.name == "template"), None)

    def prop(self, k: str) -> str:
        return str(self.head.props.get(k, "")) if self.head else ""

    @property
    def shapes(self) -> list[str]:
        return [s.strip() for s in self.prop("shape").split(",") if s.strip()]

    def part(self, step: str | None = None) -> list[kdl.Node]:
        """The read, run and field lines a step reads: the template's own, then its step's."""
        out = [n for n in self.nodes if n.name in LINES]
        for s in self.nodes:
            if s.name == "step" and (step is None or str(s.args[0] if s.args else "") == step):
                out += s.children
        return out

    def writes(self, step: str | None = None) -> list[str]:
        s = next((n for n in self.nodes if n.name == "step" and step and n.args and str(n.args[0]) == step), None)
        return str(s.props.get("writes", "") if s is not None else self.prop("writes")).split()


def load(path: Path) -> Template | None:
    """A template's fence, or None where its Context is prose."""
    m = re.search(r"^## Context\n(.*?)(?=^## |\Z)", path.read_text(), re.S | re.M)
    if not m or "```kdl" not in m.group(1):
        return None
    return Template(path, kdl.fenced(m.group(1)))


def length(spec) -> tuple[int, int | None] | None:
    """A length as (min, max or None): `N` exactly, `N-M`, `N+` at least, `-M` at most."""
    m = LENGTH_RE.fullmatch(str(spec))
    if not m or not str(spec):
        return None
    lo, rest, hi = m.groups()
    if rest is None:
        return (int(lo), int(lo))
    if rest == "+":
        return (int(lo), None) if lo else None
    if not lo and not hi:
        return None
    lo, hi = int(lo or 0), int(hi) if hi else None
    return (lo, hi) if hi is None or lo <= hi else None


def count(text: str, unit: str) -> int:
    if unit == "words":
        return len(text.split())
    if unit == "items":
        return len(re.findall(r"^\s*- ", text, re.M))
    return len(re.findall(r"[.!?](?=\s|$)", text.strip())) or (1 if text.strip() else 0)


def limits(t: Template) -> list[tuple[str, str, tuple[int, int | None]]]:
    """(Table.Field, unit, length) for every length a template's field lines state."""
    return [(str(n.args[0]), u, length(n.props[u])) for n in t.part()
            if n.name == "field" and n.args for u in LENGTH_UNITS if u in n.props and length(n.props[u])]


def names(v) -> list[str]:
    return [x.strip() for x in str(v).split(",") if x.strip()]


def resolve(name: str, schema: tb.Schema) -> bool:
    """A name a field reads: a node or setting table, or one of its members or fields; a
    brief field of any rating."""
    head, _, member = name.partition(".")
    if not member:
        return head in schema.tables or any(head in f.nodes for f in schema.folders.values()) \
            or any(head == m.name for f in schema.folders.values() for m in f.brief)
    if head in schema.fields:
        return any(m.name == member for m in schema.fields[head])
    return any(m.name == member for f in schema.folders.values() for m in f.nodes.get(head, []))


def brief_names() -> set[str]:
    """Every line a BRIEF:[name] source can name: BRIEF.md's nodes and the lines they hold."""
    return {x.name for n in tb.brief_nodes() for x in [n, *n.children]}


def is_file(source: str) -> bool:
    return "/" in source or source.endswith(".md")


def source_problem(x: str, schema: tb.Schema, reads: set[str]) -> str | None:
    """What is wrong with one source a field pulls from, or None where it resolves."""
    if x.startswith("BRIEF:"):
        return None if x[6:] in brief_names() else f"{x!r} names no BRIEF.md line"
    if is_file(x):
        return None if x in reads else f"{x!r} is a file the template does not read"
    return None if resolve(x, schema) else f"{x!r} names no node, table, member, field or brief field"


def line_problems(n: kdl.Node, schema: tb.Schema) -> list[str]:
    """A line's properties against Template_Schema.md: each one it defines, every one it
    requires, and an enum's items."""
    out, defined = [], members(n.name)
    for k, v in n.props.items():
        m = defined.get(k)
        if m is None:
            out.append(f"line {n.line}: {n.name} has no {k!r} - it takes {', '.join(defined) or 'none'}")
            continue
        typ, items = m.args[0], ENUMS.get(m.args[0])
        allowed = (items or []) + (list(schema.tables) if k == "shape" else [])
        for x in (names(v) if "list" in m.args else [str(v)]) if items else []:
            if x not in allowed:
                out.append(f"line {n.line}: {n.name} {k} {x!r} is not one of {', '.join(items)}"
                           + (" nor a Setting_Schema.md table" if k == "shape" else ""))
    for k, m in defined.items():
        if "opt" not in m.args and k not in n.props:
            out.append(f"line {n.line}: {n.name} has no {k}, which it requires")
    return out


def problems(t: Template, schema: tb.Schema, steps: set[str]) -> list[str]:
    heads = [n for n in t.nodes if n.name == "template"]
    if len(heads) != 1:
        return [f"its fence holds {len(heads)} template lines - it holds one"]
    out = []
    for n in t.nodes:
        if n.name not in NODES:
            out.append(f"line {n.line}: {n.name!r} is not one of {', '.join(NODES)}")
            continue
        out += line_problems(n, schema)
        if n.name == "step":
            sid = str(n.args[0]) if n.args else ""
            if sid not in steps:
                out.append(f"line {n.line}: step {sid!r} is no STEPS.md step")
            for c in n.children:
                if c.name not in LINES:
                    out.append(f"line {c.line}: a step holds {', '.join(LINES)} lines, not {c.name!r}")
                elif c.name in NODES:
                    out += line_problems(c, schema)
    own = [n for n in t.nodes if n.name in LINES]
    groups = [own] + [own + s.children for s in t.nodes if s.name == "step"]
    seen = set()
    for group in groups:
        reads = {str(n.args[0]) for n in group if n.name == "read" and n.args}
        for n in group:
            if id(n) in seen:
                continue
            seen.add(id(n))
            out += _line_problems(n, schema, reads)
    return out


def _line_problems(n: kdl.Node, schema: tb.Schema, reads: set[str]) -> list[str]:
    """What is wrong with one read, run or field line's own values, given the files its
    template and step read."""
    out = []
    where = f"line {n.line}: {n.name}"
    arg = str(n.args[0]) if n.args else ""
    if n.name == "read" and "naming" in n.props:
        table = str(n.props["naming"])
        if table not in schema.tables:
            out.append(f"{where} naming {table!r}, which is no table")
        elif not any(tb.names_table(f, node, table) for f in schema.folders.values() for node in f.nodes):
            out.append(f"{where} naming {table!r}, which no region node names")
    elif n.name == "read":
        if arg in STANDING:
            out.append(f"{where} {arg} - every template reads it, so none lists it")
        elif not PLACEHOLDER_RE.search(arg) and not arg.startswith("setting/") and not (ROOT / arg).exists():
            out.append(f"{where} {arg}, which does not exist")
    elif n.name == "run" and arg.split()[0] not in RUNS:
        out.append(f"{where} {arg!r} - a run is one of {', '.join(RUNS)}")
    elif n.name == "field":
        for u in LENGTH_UNITS:
            if u in n.props and not length(n.props[u]):
                out.append(f"{where} {arg}: {u} {n.props[u]!r} is not N, N-M, N+ or -M")
        if any(u in n.props for u in LENGTH_UNITS) and "." not in arg:
            out.append(f"{where} {arg}: a length names a Table.Field")
        if not resolve(arg, schema):
            out.append(f"{where} {arg}: {arg!r} names no node, table, member, field or brief field")
        for x in names(n.props.get("from", "")):
            if (p := source_problem(x, schema, reads)):
                out.append(f"{where} {arg}: {p}")
    return out


def schemas(t: Template) -> set[str]:
    """The schemas a template reads: Common always, the ones its fence names, and those its
    shape is written in."""
    out = {"Common_Schema.md"}
    out |= {Path(str(n.args[0])).name for n in t.part() if n.name == "read" and n.args
            and str(n.args[0]).startswith("patterns/")}
    for s in t.shapes:
        out |= {"Region_Schema.md"} if s == "gazetteer" else \
            {"Region_Schema.md", "[Rating]_Schema.md"} if s in ("seed", "brief") else \
            {"Setting_Schema.md", "[Rating]_Schema.md"} if s == "tables" else {"Setting_Schema.md"}
    if any(n.name == "read" and "naming" in n.props for n in t.part()):
        out |= {"Setting_Schema.md", "[Rating]_Schema.md"}
    return out


def read_lines(t: Template, schema: tb.Schema, step: str | None = None) -> list[str]:
    """What a step reads beyond STANDING and its schemas, one line each."""
    out = []
    for n in t.part(step):
        arg = str(n.args[0]) if n.args else ""
        if n.name == "read" and "naming" in n.props:
            table = str(n.props["naming"])
            via = sorted({f"{node}.{m.name}" for f in schema.folders.values() for node, ms in f.nodes.items()
                          for m in ms if (m.type == "entry" and table in m.args)
                          or (m.type == "pull" and table in f.enums.get(m.arg, {}))})
            out.append(f"the entries naming {table}: {', '.join(via)}")
        elif n.name == "read":
            extra = [str(n.props[k]) for k in ("part",) if k in n.props]
            out.append(arg + (f" - {extra[0]}" if extra else "") + (" (once written)" if "once" in n.props else ""))
        elif n.name == "run":
            out.append(f"python3 tools/validate_setting.py {arg}")
        elif n.name == "field":
            lens = [f"{u} {n.props[u]}" for u in LENGTH_UNITS if u in n.props]
            out.append(f"{arg} <- {n.props.get('from', '')}" if "from" in n.props else f"{arg}: {', '.join(lens)}")
    return out


# -- skeletons -------------------------------------------------------------------------

def _hint(m: tb.Member) -> str:
    return f"[{m.type}{' ' + ' '.join(m.args) if m.type in ('entry', 'pull') else ''}" \
           f"{', opt' if m.opt else ''}{', list' if m.is_list else ''}]"


def table_skeleton(schema: tb.Schema, name: str) -> str:
    kind, file = schema.tables[name]
    props, fields = schema.table_props[name], schema.fields.get(name, [])
    title = str(props.get("title", f"{name} of [Setting Name]"))
    if kind == "roll" or props.get("layout") == "rows":
        head = "| " + " | ".join(m.name for m in fields) + " |"
        return "\n".join([title, "", head, "|" + "---|" * len(fields),
                          "| " + " | ".join(_hint(m) for m in fields) + " |"])
    level = "#" * int(props.get("heading", 3))
    return "\n".join([title, "", f"{level} [Title]"] + [f"{m.name}: {_hint(m)}" for m in fields])


def node_line(f: tb.Folder, node: str, key: str) -> str:
    return members_line(f.nodes.get(node, []), node, key)


def members_line(members: list[tb.Member], node: str, key: str) -> str:
    return " ".join([node, key] + [f"{m.name}={_hint(m)}" for m in members if m.name != "one-of"]
                    + [f"{{ {' | '.join(m.nodes)} }}" for m in members if m.name == "one-of"])


def gazetteer_skeleton(schema: tb.Schema) -> str:
    return "\n".join(["Regional Gazetteer of [Setting Name]", "", "```kdl",
                      members_line(schema.shared_nodes.get("Region", []), "Region", "[Region Code]"), "```"])


def region_skeleton(schema: tb.Schema, shape: str, files: list[str], rating: str | None,
                    code: str | None, setting: tb.Setting | None) -> str:
    out = []
    for name, f in schema.folders.items():
        if rating and name.lower() != rating.lower():
            continue
        c = code or "[Region Code]"
        out.append(f"## {name.upper()}")
        if shape == "seed":
            counts = f.counts.get("Seed", {})
            out += ["# Seed of " + c + " [Region Name]", "", "```kdl"]
            out += [node_line(f, n, c) + (f"   // {counts[n]}" if n in counts else "   // 1+")
                    for n in f.files.get("Seed", [])] + ["```"]
        elif shape == "brief":
            holds = tb.brief_holds(setting, setting.regions[code]) if setting and code in setting.regions else {}
            out += [f"{c} [Region Name]", ""]
            for m in f.brief:
                if m.is_list:
                    items = holds.get(m.name) or ["[Location Code]"]
                    out += [f"{m.name}:"] + [f"- {i} - [...]" for i in items] + [""]
                elif m.name == "Tables":
                    out += ["Tables:", "[die, if rolled] [table name]", "1. [...]", "...", "6. [...]", ""]
                else:
                    out += [f"{m.name}: [{m.type}]", ""]
            out.append(f"Drawn beside it, never written: {', '.join(f.drawn)}")
        else:
            for stem in [s for s in f.files if s not in ("Seed", "Ground")] if files == ["*"] else files:
                if stem not in f.files:
                    continue
                key = f"{c}.[a-z]" if stem == "Blocks" else "[Location Code]"
                out += [f"# {stem} of {c} [Region Name]", "", "```kdl"] + \
                       [node_line(f, n, key) for n in f.files[stem]] + ["```", ""]
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def skeleton(t: Template, schema: tb.Schema, step: str | None, code: str | None = None,
             setting: tb.Setting | None = None) -> str | None:
    """What a step writes, as its schema shapes it; None where no schema does."""
    if not t.shapes:
        return None
    rating = setting.regions[code].rating if setting and code in setting.regions else None
    out = []
    for s in t.shapes:
        if s == "gazetteer":
            out.append(gazetteer_skeleton(schema))
        elif s in SHAPES:
            stems = [Path(w).stem for w in t.writes(step)] if s == "tables" else []
            files = stems if stems and "[Table]" not in stems else ["*"]
            out.append(region_skeleton(schema, s, files, rating, code, setting))
        else:
            out.append(table_skeleton(schema, s))
    return "\n\n".join(out)


def load_all() -> dict[Path, Template]:
    return {p: t for p in sorted(TEMPLATES.glob("*/*.md")) if (t := load(p))}
