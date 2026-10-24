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


def holds(node: str) -> tuple[str, ...]:
    """The nodes a node's children may be, by its `one-of`."""
    return tuple(next((c.args for c in GRAMMAR[node].children if c.name == "one-of"), ()))


TOP = holds("fence")
LINES = holds("step")                     # the read, run and field lines a step adds
LENGTH_UNITS = tuple(c.name for c in GRAMMAR["field"].children if c.args[:1] == ["length"])


def members(node: str) -> dict[str, kdl.Node]:
    """A node's properties as Template_Schema.md defines them: every member but its `arg=`."""
    g = GRAMMAR[node]
    return {c.name: c for c in g.children if c.name not in ("one-of", g.props.get("arg"))}


# -- patterns: a line as written, each [name] a field ------------------------------------

FIELD_RE = re.compile(r"\[([^\]]+)\]")


def slug(name: str) -> str:
    return re.sub(r"\W+", "_", name).strip("_").lower()


def pattern_re(pattern: str) -> re.Pattern:
    """A pattern as a regex: each [name] a group named for it, matching any text (or none,
    where it ends the line), and the literal text between them as written, its spaces any
    run of whitespace."""
    parts, out, seen = FIELD_RE.split(pattern), "", set()
    for i, part in enumerate(parts):
        if i % 2:
            name = slug(part)
            while name in seen:
                name += "_"
            seen.add(name)
            last = not "".join(parts[i + 1:]).strip()
            out += f"(?P<{name}>.*?)" if last else f"(?P<{name}>.+?)"
        else:
            out += r"\s*".join(re.escape(w) for w in re.split(r"\s+", part)) if part.strip() else (r"\s*" if part else "")
    return re.compile("^" + out + r"\s*$")


def literal_head(pattern: str) -> str:
    """The literal text a pattern opens with, before its first field."""
    return FIELD_RE.split(pattern)[0].strip()


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

    @property
    def format(self) -> list[kdl.Node]:
        return next((n.children for n in self.nodes if n.name == "format"), [])

    def line(self, name: str) -> kdl.Node | None:
        """A format line by name."""
        return next((n for n in self.format if n.name == "line" and n.args and str(n.args[0]) == name), None)

    def pattern(self, name: str) -> re.Pattern:
        return pattern_re(str(self.line(name).props["pattern"]))

    @property
    def cites(self) -> list[kdl.Node]:
        return [n for n in self.nodes if n.name == "cite"]

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


def member(name: str, schema: tb.Schema) -> tb.Member | None:
    """The member a Table.Field or Node.member names, in any rating."""
    head, _, name = name.partition(".")
    ms = schema.fields.get(head) or next((f.nodes[head] for f in schema.folders.values() if head in f.nodes), [])
    return next((m for m in ms if m.name == name), None)


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
        return None if x[6:].split(".")[0] in brief_names() else f"{x!r} names no BRIEF.md line"
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
        typ, items = m.args[0], ENUMS.get(m.args[0]) or list(schema.setting_enums.get(m.args[0], {})) or None
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

    def walk(n: kdl.Node, allowed: tuple[str, ...], within: str):
        nonlocal out
        if n.name not in allowed:
            out.append(f"line {n.line}: {within} holds {', '.join(allowed)} lines, not {n.name!r}")
            return
        out += line_problems(n, schema)
        for c in n.children:
            walk(c, holds(n.name), n.name)

    for n in t.nodes:
        walk(n, TOP, "a fence")
        if n.name == "step" and (sid := str(n.args[0]) if n.args else "") not in steps:
            out.append(f"line {n.line}: step {sid!r} is no STEPS.md step")
    for n in t.format:
        for k in ("when", "each"):
            if k in n.props and (p := source_problem(str(n.props[k]), schema, set())):
                out.append(f"line {n.line}: {n.name} {k}: {p}")
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
        if "items" in n.props and (m := member(arg, schema)) and m.out != "bullets":
            out.append(f"{where} {arg}: items lengths a list, and it is set down as {m.out}")
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


def title(schema: tb.Schema, name: str) -> str:
    return str(schema.table_props[name].get("title", f"{name} of [Setting Name]"))


def table_skeleton(schema: tb.Schema, name: str, preface: list[str] | None = None) -> str:
    kind, file = schema.tables[name]
    props, fields = schema.table_props[name], schema.fields.get(name, [])
    title = globals()["title"](schema, name) + ("\n\n" + "\n".join(preface) if preface else "")
    if kind == "roll" or props.get("layout") == "rows":
        head = "| " + " | ".join(m.name for m in fields) + " |"
        return "\n".join([title, "", head, "|" + "---|" * len(fields),
                          "| " + " | ".join(_hint(m) for m in fields) + " |"])
    level = "#" * int(props.get("heading", 3))
    return "\n".join([title, "", f"{level} [Title]"]
                     + [f"{m.name}:\n- {_hint(m)}" if m.out == "bullets" else f"{m.name}: {_hint(m)}" for m in fields])


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
                if m.out == "bullets":
                    items = holds.get(m.name) or ["[Location Code]"]
                    out += [f"{m.name}:"] + [f"- {i} - [...]" for i in items] + [""]
                elif m.out == "table":
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


def fill(pattern: str, hint: str | None) -> str:
    """A pattern as the skeleton shows it: its last field carries the hint."""
    if not hint:
        return pattern
    fields = list(FIELD_RE.finditer(pattern))
    last = fields[-1]
    return pattern[:last.start()] + f"[{last.group(1)} - {hint}]" + pattern[last.end():]


def table_lines(n: kdl.Node) -> list[str]:
    """A format's table, as written."""
    row = lambda cells: "| " + " | ".join(str(c) for c in cells) + " |"
    head = names(n.props.get("head", ""))
    return [row(head), "|" + "---|" * len(head)] + [row(r.args) for r in n.children if r.name == "row"]


def draw_format(t: Template) -> list[str]:
    out = []
    for n in t.format:
        p = n.props
        if n.name == "line":
            out.append(fill(str(p["pattern"]), p.get("hint")))
        elif n.name == "table":
            out += table_lines(n)
        elif n.name == "section":
            out += ["", f"## {n.args[0]}"]
            if p.get("out") == "table":
                out += ([f"### [one for each of {p['each']}]"] if "each" in p else []) + \
                       [f"| d6 | {p.get('head', '[result]')} |", "|---|---|", "| 1 | [...] |", "| ... | ... |", "| 6 | [...] |"]
            elif p.get("out") == "bullets":
                out.append("- " + str(p.get("item", "[...]")))
            else:
                out.append("[...]")
    return out


def citations(t: Template, schema: tb.Schema) -> list[str]:
    """Every citation a template's text may carry: each cite= table's, then its own cite lines."""
    out = [f"- ({p['cite']}: [Title])" for p in schema.table_props.values() if "cite" in p]
    return out + [f"- {n.props['form']}" + (f" - {n.props['note']}" if "note" in n.props else "") for n in t.cites]


def skeleton(t: Template, schema: tb.Schema, step: str | None, code: str | None = None,
             setting: tb.Setting | None = None) -> str | None:
    """What a step writes, as its schema or its format shapes it; None where neither does."""
    if not t.shapes:
        if not t.format:
            return None
        return "\n".join(draw_format(t) + (["", "Citations:"] + citations(t, schema) if t.cites else []))
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
            out.append(table_skeleton(schema, s, draw_format(t) if t.format and s == t.shapes[0] else None))
    return "\n\n".join(out)


# -- a written file against its format -------------------------------------------------

D6_ROW_RE = re.compile(r"^\|\s*([1-6])\s*\|")


def file_sections(text: str) -> dict[str, list[str]]:
    """A markdown file's `## ` sections, each the lines under its heading."""
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = out.setdefault(line[3:].strip(), [])
        elif cur is not None:
            cur.append(line)
    return out


def brief_value(source: str):
    """What BRIEF:[name].[property] holds, or None."""
    name, _, prop = source.removeprefix("BRIEF:").partition(".")
    n = next((c for b in tb.brief_nodes() for c in [b, *b.children] if c.name == name), None)
    return n.props.get(prop) if n is not None else None


def d6_problem(what: str, body: list[str]) -> str | None:
    rows = [int(m.group(1)) for l in body if (m := D6_ROW_RE.match(l))]
    return None if rows[:6] == [1, 2, 3, 4, 5, 6] else f"{what} is not a d6 table of rows 1-6: {rows}"


def section_problems(n: kdl.Node, body: list[str]) -> list[tuple[str, str]]:
    name, p, out = str(n.args[0]), n.props, []
    if p.get("out") == "table" and "each" in p:
        subs, cur = {}, None
        for l in body:
            if l.startswith("### "):
                cur = subs.setdefault(l[4:].strip(), [])
            elif cur is not None:
                cur.append(l)
        want = str(brief_value(str(p["each"])) or "").split()
        if list(subs) != want:
            out.append(("error", f"{name} holds {list(subs)}, {p['each']} lists {want}"))
        out += [("error", x) for k, v in subs.items() if (x := d6_problem(f"{name} / {k}", v))]
    elif p.get("out") == "table":
        out += [("error", x) for x in [d6_problem(name, body)] if x]
    elif p.get("out") == "bullets" and "item" in p:
        r = pattern_re(str(p["item"]))
        out += [("warn", f"{name}: {l!r} is not {p['item']!r}") for l in body if l.startswith("- ") and not r.match(l[2:])]
    return out


def format_problems(t: Template, text: str, schema: tb.Schema) -> list[tuple[str, str]]:
    """A written file against its template's format, line by line: a shaped file's title,
    then the format, then (unshaped) nothing more. Each is (error or warn, what): a
    bullet item off its pattern warns."""
    lines = [l.rstrip() for l in text.splitlines() if l.strip()]
    if not lines:
        return []
    out, i = [], 0
    at = lambda: repr(lines[i]) if i < len(lines) else "the end"
    if t.shapes:
        if pattern_re(title(schema, t.shapes[0])).match(lines[0]):
            i = 1
        else:
            out.append(("error", f"opens with {lines[0]!r}, not its title {title(schema, t.shapes[0])!r}"))
    for n in t.format:
        p = n.props
        if n.name == "line":
            r, count, got = pattern_re(str(p["pattern"])), p.get("count", "one"), 0
            while i < len(lines) and r.match(lines[i]) and (count == "many" or not got):
                i, got = i + 1, got + 1
            if not got and count != "optional":
                out.append(("error", f"has {at()} where its {n.args[0]} line, {p['pattern']!r}, stands"))
        elif n.name == "table":
            for want in table_lines(n):
                if i < len(lines) and lines[i].strip() == want:
                    i += 1
                else:
                    out.append(("error", f"its table runs {at()} where its format has {want!r}"))
                    break
        elif n.name == "section":
            name = str(n.args[0])
            asked = "when" not in p or brief_value(str(p["when"])) not in (None, 0, "0", "")
            ahead = next((j for j in range(i, len(lines)) if lines[j] == f"## {name}"), None)
            if ahead is not None and ahead > i:
                out.append(("error", f"has {at()} where its ## {name} section stands"))
                i = ahead
            here = ahead is not None
            if here != asked:
                out.append(("error", f"holds ## {name}, which {p['when']} does not ask for" if here
                            else f"has {at()} where its ## {name} section stands"))
            if here:
                body, i = [], i + 1
                while i < len(lines) and not lines[i].startswith("## "):
                    body.append(lines[i])
                    i += 1
                out += section_problems(n, body)
    if not t.shapes and i < len(lines):
        out.append(("error", f"holds {at()} past what its format gives"))
    return out


def load_all() -> dict[Path, Template]:
    return {p: t for p in sorted(TEMPLATES.glob("*/*.md")) if (t := load(p))}
