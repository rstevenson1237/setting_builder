"""patterns/*_Schema.md and templates/Template_Schema.md as a graph of definitions: every value, enum, node, table, folder and
region, with the lines it is written in and each name on them resolved to the definition it
names; then each template, with what it reads, the fields it writes and how. The schema
explorer on patterns.html is drawn from this and nothing else."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import kdl

ROOT = Path(__file__).resolve().parent.parent
PATTERNS = ROOT / "patterns"
TEMPLATE_SCHEMA = ROOT / "templates" / "Template_Schema.md"
SHARED = ("Common", "Setting", "Region")   # widest first; every other schema is a rating's
KINDS = ("value", "enum", "node", "table", "folder", "region")
FLAGS = {"opt", "list", "none"}
COMMENT = re.compile(r'(?:"(?:[^"\\]|\\.)*"|[^"/]|/(?!/))*')   # code up to a `//` outside quotes


def stem(path: Path) -> str:
    return path.name.removesuffix("_Schema.md")


def split_comment(line: str) -> tuple[str, str]:
    code = COMMENT.match(line).group()
    return code.rstrip(), line[len(code):].lstrip("/ ").rstrip()


def paragraphs(text: str) -> list[str]:
    """Markdown prose as its paragraphs and list items, each on one line."""
    out = []
    for block in text.strip().split("\n\n"):
        items = re.split(r"\n(?=- )", block.strip())
        out += [" ".join(i.split()) for i in items if i.strip()]
    return out


def ref_id(file: str, kind: str, name: str) -> str:
    return f"{file}/{kind}/{name}"


@dataclass
class Gap:
    """The comment lines between two definitions, and where they belong."""
    section: list[str] = field(default_factory=list)   # a `// --` block: applies to the definitions after it
    trailing: str = ""                                 # touches the definition before it
    leading: str = ""                                  # touches the one after


def read_gap(lines: list[str], lo: int, hi: int, after_def: bool) -> Gap:
    """lines[lo:hi], blank lines and comment lines, split into blocks."""
    gap, block, block_after = Gap(), [], False
    for i in range(lo, hi + 1):
        text = lines[i].strip() if i < hi else ""
        if text.startswith("//"):
            if not block:
                block_after = after_def and i == lo
            block.append(text.lstrip("/ ").rstrip())
            continue
        if block:
            if block[0].startswith("-- "):
                gap.section = block
            elif block_after:
                gap.trailing = " ".join(block)
            else:
                gap.leading = " ".join(block)
            block = []
    return gap


class Graph:
    def __init__(self, root: Path = PATTERNS):
        self.problems: list[str] = []
        self.files: list[dict] = []
        self.defs: dict[str, dict] = {}
        order = [root / f"{n}_Schema.md" for n in SHARED]
        order += sorted(set(root.glob("*_Schema.md")) - set(order)) + [TEMPLATE_SCHEMA]
        self.paths = [p for p in order if p.exists()]
        where = {stem(p): p.relative_to(ROOT).as_posix() for p in self.paths}
        self.by_file: dict[str, dict[tuple[str, str], str]] = {}
        sources = {stem(p): p.read_text(encoding="utf-8") for p in self.paths}
        for name, text in sources.items():
            self._declare(name, text)
        for name, text in sources.items():
            self._read(name, text)
        for f in self.files:
            f["path"] = where[f["id"]]
        self._templates()
        for d in self.defs.values():
            src = next((t["to"] for t in d["head"] if t["t"].startswith("as=")), None)
            if src:
                d["lines"] = self.defs[src]["lines"]
        self.edges = self._edges()

    # -- pass 1: which definitions each file holds -------------------------------------

    def _declare(self, file: str, text: str):
        held = self.by_file.setdefault(file, {})
        for n in kdl.fenced(text):
            if n.name in KINDS and n.args:
                held[(n.name, n.args[0])] = ref_id(file, n.name, n.args[0])

    def scope(self, file: str) -> list[str]:
        """The files a schema sees, narrowest first."""
        seen = list(SHARED[:SHARED.index(file) + 1][::-1]) if file in SHARED else [file, *SHARED[::-1]]
        return [f for f in seen if f in self.by_file]

    def find(self, file: str, kinds: tuple[str, ...], name: str) -> str | None:
        """The id of the definition `name` names from `file`: its own, else a wider schema's.
        A setting table is named from any schema."""
        for f in self.scope(file) + (["Setting"] if "table" in kinds else []):
            for k in kinds:
                if (i := self.by_file.get(f, {}).get((k, name))):
                    return i
        return None

    def only(self, kinds: tuple[str, ...], name: str) -> str | None:
        """The one definition of that name in any schema, where a name is not scoped to the file naming it."""
        held = [i for f in self.by_file.values() for (k, n), i in f.items() if k in kinds and n == name]
        return held[0] if len(held) == 1 else None

    # -- pass 2: each definition, its lines and the names on them ------------------------

    def _read(self, file: str, text: str):
        lines = text.splitlines()
        fence = [i for i, l in enumerate(lines) if l.strip() in ("```kdl", "```")]
        start, end = fence[0] + 1, fence[1]
        top = kdl.fenced(text)
        starts = [n.line - 1 for n in top] + [end]
        intro = [p.replace("\n", " ").strip() for p in "\n".join(lines[1:fence[0]]).split("\n\n") if p.strip()]
        groups = [{"note": "", "defs": []}]
        section = ""

        def opens(gap: Gap):
            nonlocal section
            if gap.section:
                section = " ".join(gap.section).removeprefix("-- ")
                groups.append({"note": section, "defs": []})

        gap = read_gap(lines, start, starts[0], False)
        opens(gap)
        for i, n in enumerate(top):
            pending = gap.leading
            body_end = starts[i + 1] - 1
            while body_end > starts[i] and (not lines[body_end].strip() or lines[body_end].strip().startswith("//")):
                body_end -= 1
            gap = read_gap(lines, body_end + 1, starts[i + 1], True)
            doc = " ".join(x for x in (pending, split_comment(lines[starts[i]])[1], gap.trailing) if x)
            if d := self._definition(file, n, lines, body_end, doc):
                d["section"] = section
                groups[-1]["defs"].append(d["id"])
            opens(gap)
        self.files.append({"id": file, "title": lines[0].lstrip("# ").strip(), "intro": intro,
                           "groups": [g for g in groups if g["note"] or g["defs"]]})

    def _definition(self, file: str, n: kdl.Node, lines: list[str], hi: int, doc: str) -> dict | None:
        if n.name not in KINDS or not n.args:
            self.problems.append(f"{file}: line {n.line}: {n.name!r} is not a definition")
            return None
        name = n.args[0]
        d = {"id": ref_id(file, n.name, name), "kind": n.name, "name": name, "file": file,
             "line": n.line, "doc": doc, "head": [], "rows": [], "lines": []}
        self.defs[d["id"]] = d
        if n.name == "value":
            d["head"] = [{"t": str(a)} for a in n.args[1:]] + [{"t": f"{k}={v}"} for k, v in n.props.items()]
        elif n.name == "enum":
            d["rows"] = self._enum_rows(file, n, lines, hi)
        elif n.name in ("table", "node"):
            if n.name == "table":
                d["head"] = [{"t": str(n.args[1])}] + self._props(file, n.props, {"as": ("table",)})
            else:
                d["head"] = self._props(file, n.props, {})
            d["lines"] = self._fields(file, n.children, lines, hi)
        elif n.name == "folder":
            d["head"] = self._props(file, n.props, {"type": ("enum",)})
            d["lines"] = self._folder(file, n, lines, hi)
        else:
            for c in n.children:
                d["lines"] += [{"heading": c.name}] + self._fields(file, c.children, lines, hi)
            same = self.find(file, ("folder",), name) or self.only(("folder",), name)
            d["head"] = [{"t": name, "to": same}] if same else []
        return d

    def _props(self, file, props, kinds: dict) -> list[dict]:
        """`k=v` tokens; where `kinds` (or a `from=` or `gate=`) says v names a definition, a link to it."""
        out = []
        for k, v in props.items():
            want = kinds.get(k) or (("node",) if k in ("from", "gate") else None)
            to = (self.find(file, want, str(v)) or self.only(want, str(v))) if want else None
            out.append({"t": f"{k}={v}", "to": to})
        return out

    def _enum_rows(self, file: str, n: kdl.Node, lines: list[str], hi: int) -> list[dict]:
        """The items on the enum's own line, then each group, which names its items on a line of its own."""
        row = lambda group, items, comment: {"group": group, "comment": comment, "items": [
            {"t": str(a), "to": self.find(file, ("table", "node"), str(a))} for a in items]}
        rows = [row("", n.args[1:], "")] if n.args[1:] else []
        return rows + [row(c.name, c.args, self._line_comment(lines, c.line - 1, hi)) for c in n.children]

    def _line_comment(self, lines: list[str], at: int, limit: int) -> str:
        """The comment on a line, then any comment-only lines straight after it."""
        parts = [split_comment(lines[at])[1]]
        i = at + 1
        while i < limit and lines[i].strip().startswith("//"):
            parts.append(lines[i].strip().lstrip("/ ").rstrip())
            i += 1
        return " ".join(p for p in parts if p)

    def _fields(self, file: str, children, lines, limit: int) -> list[dict]:
        """A field is `Label type`, then what the type takes: the tables an `entry` names, the
        enum a `pull` names, or flags."""
        out = []
        for c in children:
            if c.name == "one-of":
                label, kinds, parts = "", ("node",), [("one-of", None)] + [(a, a) for a in c.args]
            else:
                typ = c.args[0] if c.args else ""
                follow = ("table",) if typ == "entry" else ("enum",) if typ == "pull" else ()
                label, kinds, parts = c.name, follow, [(typ, typ)] + [(a, a) for a in c.args[1:]]
            toks = []
            for i, (text, name) in enumerate(parts):
                if name is None or name in FLAGS:
                    toks.append({"t": text, "flag": True})
                    continue
                want = ("enum", "value") if label and i == 0 else kinds
                to = self.find(file, want, name) if want else None
                if want and not to:
                    self.problems.append(f"{file}: line {c.line}: {name!r} names no definition")
                toks.append({"t": text, "to": to})
            toks += self._props(file, c.props, {})
            out.append({"label": label, "parts": toks, "comment": self._line_comment(lines, c.line - 1, limit),
                        "to": next((t["to"] for t in toks if t.get("to")), None)})
        return out

    def _folder(self, file: str, n: kdl.Node, lines, limit: int) -> list[dict]:
        """Each line names the nodes its file holds; `top` and `join` name items of the type enum."""
        kind = self.find(file, ("enum",), str(n.props.get("type", "")))
        out = []
        for c in n.children:
            toks = [{"t": a, "to": kind if c.name in ("top", "join") else self.find(file, ("node",), a)} for a in c.args]
            toks += self._props(file, c.props, {})
            out.append({"label": c.name, "parts": toks, "comment": self._line_comment(lines, c.line - 1, limit),
                        "to": next((t["to"] for t in toks if t.get("to")), None)})
        return out

    # -- templates: what each reads, and the fields it writes and how ---------------------

    def _templates(self):
        import tables as tb
        import templates as tp
        import validate_setting as v
        schema, steps = tb.Schema(), v.read_set()
        groups = {}
        for path, t in tp.load_all().items():
            rel = path.relative_to(tp.TEMPLATES).as_posix()
            text = path.read_text(encoding="utf-8")
            section = lambda h: (re.search(rf"^## {h}\n(.*?)(?=^## |\Z)", text, re.S | re.M) or [None, ""])[1]
            cited = sorted(s for s, (names, _) in steps.items() if rel in names)
            d = {"id": ref_id("Templates", "template", rel.removesuffix(".md")), "kind": "template",
                 "name": path.stem, "file": "Templates", "path": path.relative_to(ROOT).as_posix(), "line": 1,
                 "doc": " ".join(section("Purpose").split()), "head": [], "rows": [], "lines": [],
                 "text": paragraphs(section("Instructions"))}
            d["head"] = [{"t": f"scope={t.prop('scope')}"}] + [{"t": f"step {s}"} for s in cited] + \
                [{"t": s, "to": self.find("Setting", ("table",), s)} for s in t.shapes]
            d["lines"] = self._template_lines(t, schema, tp)
            self.defs[d["id"]] = d
            groups.setdefault(rel.split("/")[0], []).append(d["id"])
        self.files.append({"id": "Templates", "title": "Templates", "path": "templates/", "intro": [
            "One template per artifact type: what it reads, each field it writes with its source and output, "
            "and the format of a file no schema shapes."],
            "groups": [{"note": g, "defs": ids} for g, ids in groups.items()]})

    def _source(self, x: str) -> dict:
        """A field's source, linked to the table or node it names."""
        head = x.partition(".")[0]
        return {"t": x, "to": self.find("Setting", ("table",), head) or self.only(("node",), head)
                or next((i for f in self.by_file.values() for (k, n), i in f.items() if k == "node" and n == head), None)}

    def _template_lines(self, t, schema, tp) -> list[dict]:
        line = lambda label, parts, comment="", to=None: {"label": label, "parts": parts, "comment": comment,
                                                           "to": to or next((p["to"] for p in parts if p.get("to")), None)}
        out = []
        reads = [n for n in t.part() if n.name in ("read", "run")]
        if reads:
            out.append({"heading": "Reads"})
            for n in reads:
                arg = str(n.args[0]) if n.args else ""
                parts = [{"t": arg}] if arg else [{"t": f"entries naming {n.props['naming']}",
                                                    "to": self.find("Setting", ("table",), str(n.props["naming"]))}]
                out.append(line(n.name, parts + ([{"t": f"once {n.props['once']}", "flag": True}] if "once" in n.props else []),
                                str(n.props.get("part", ""))))
        given = {str(n.args[0]): n for n in t.part() if n.name == "field" and n.args}
        fields = []
        for s in t.shapes:
            for m in schema.fields.get(s, []):
                fields.append((f"{s}.{m.name}", m))
        fields += [(k, tp.member(k, schema)) for k in given if k not in dict(fields)]
        if fields:
            out.append({"heading": "Fields"})
            for name, m in fields:
                n = given.get(name)
                parts = []
                if m is not None:
                    parts.append({"t": m.type, "to": self.find("Setting", ("enum", "value"), m.type)
                                  or self.only(("enum", "value"), m.type)})
                    parts.append({"t": f"out={m.out}", "flag": True})
                froms = tp.names(n.props.get("from", "")) if n is not None else []
                parts += [{"t": "from", "flag": True}] + [self._source(x) for x in froms] if froms \
                    else [{"t": "authored", "flag": True}]
                parts += [{"t": f"{u}={n.props[u]}", "flag": True} for u in tp.LENGTH_UNITS if n is not None and u in n.props]
                out.append(line(name.split(".", 1)[-1] if "." in name and name.split(".")[0] in t.shapes else name, parts))
        if t.format:
            out.append({"heading": "Format"})
            for n in t.format:
                p = n.props
                if n.name == "table":
                    out.append(line("table", [{"t": " | ".join(tp.names(p.get("head", "")))},
                                              {"t": f"{len(n.children)} rows", "flag": True}]))
                    continue
                parts = [{"t": f"## {n.args[0]}" if n.name == "section" else str(p["pattern"])}]
                parts += [{"t": f"{k}={p[k]}", "flag": True} for k in ("count", "out", "head", "each", "when") if k in p]
                parts += [{"t": f"- {p['item']}"}] if "item" in p else []
                out.append(line(str(n.args[0]) if n.name == "line" else "section", parts, str(p.get("hint", ""))))
        if t.cites:
            out.append({"heading": "Citations"})
            out += [line(str(n.args[0]), [{"t": str(n.props["form"])}], str(n.props.get("note", ""))) for n in t.cites]
        return out

    # -- the graph ---------------------------------------------------------------------

    def _edges(self) -> list[dict]:
        """One edge from a definition to each definition its head, items or lines name."""
        seen: set[tuple[str, str]] = set()
        for d in self.defs.values():
            toks = d["head"] + [t for r in d["rows"] for t in r["items"]] + [t for l in d["lines"] for t in l.get("parts", [])]
            seen |= {(d["id"], t["to"]) for t in toks if t.get("to") and t["to"] != d["id"]}
        return [{"from": a, "to": b} for a, b in sorted(seen)]

    def model(self) -> dict:
        return {"files": self.files, "defs": list(self.defs.values()), "edges": self.edges}
