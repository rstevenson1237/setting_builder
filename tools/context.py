#!/usr/bin/env python3
"""The read set for one location, assembled and printed as one stream - and
what writing a region that way costs, against writing it in one session.

A 4c session otherwise opens a dozen files and walks the pattern tree itself,
carrying every branch it did not take and deciding every rate and draw by
feel. This walks the tree once from the location's class file, settles what is
arithmetic per `tools/draw.py` - whether each rated line fires, which item each
draw gives, which one of a paired kind's files is followed - and prints what is
left, with every line it did not take marked and not followed.

The stream is ordered for a prompt cache. Everything identical for every room
of one region comes first (the prefix); what is this room's alone comes last
(the suffix). Two things never appear: a sibling location, because a room
written against its neighbours' prose converges on them, and a registry's
content, because what a name means is 4d's.

Usage:
  python3 tools/context.py 4c CODE [--reroll KEY=N ...] [--set NAME=VALUE ...]
                                    [--words]
  python3 tools/context.py cost [REGION ...] [--harness TOKENS] [--turns K]

  4c CODE     the stream for one location (`C.5`)
  --reroll    move one draw on; the key is printed in brackets beside it
  --set       settle a draw by hand - `--set prominence=central` - where the
              template, not the unit, owns the decision (one central location
              per settlement)
  --words     print the prefix/suffix word and token split instead of the stream
  cost        the four-strategy cost model over every location already written
              in the named regions (all regions by default); see cost_report()
  --harness   tokens the host adds to every call before this stream - a system
              prompt, tool definitions, CLAUDE.md. Default 0, so the figures are
              the framework's own; set it to see how a harness moves them
  --turns     turns a single session spends per room (reads, writes, checks).
              Default 1, the floor

Exits 1 where the code names no location in a region that has reached 4a.
"""
from __future__ import annotations

import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import site_common as sc  # noqa: E402
from draw import fires, items_of, ladder, pick  # noqa: E402
from validate_setting import (  # noqa: E402
    EDGE_KINDS,
    LOC_NODE_RE,
    PATTERN_CITE_RE,
    PATTERNS,
    ROOT,
    SETTING,
    parse_mmd_edges,
    read_set_graph,
    rel,
)

TEMPLATES = ROOT / "templates"

ENTRY_FILES = {
    ("SAFE", None): "safe/Settlement.md",
    ("WILD", "landmark"): "wild/Landmark.md",
    ("WILD", "hidden"): "wild/Hidden.md",
    ("WILD", "secret"): "wild/Secret.md",
    ("DANGEROUS", "high"): "dangerous/High.md",
    ("DANGEROUS", "medium"): "dangerous/Medium.md",
    ("DANGEROUS", "low"): "dangerous/Low.md",
}

# A logical Spec line opens with its rate in the left margin - a count, a
# percentage, or a SAFE prominence - and runs until the next one does.
RATE_RE = re.compile(r'^ {2}(\d+%?|liner note|working|central)\s')
PROMINENCES = ("liner note", "working", "central")
BRACE_RE = re.compile(r'\{([^{}]*)\}', re.S)
NAMED_RE = re.compile(r'^[A-Z][A-Z ]*$')
BLOCK_HEAD_RE = re.compile(r'^([A-Z][A-Z -]*?)(?:\s+-\s+(.*?))?\s*(?:\(.*\))?\s*$')
ITEM_RE = re.compile(r'^ {2}(\S[^-]*?)\s+-\s+(.*)$')
LABEL_RE = re.compile(r'^(?:Where\s+)?([A-Z][a-z]+):\s')
WHERE_RE = re.compile(r'\bwhere (?:the|a|an) ([a-z]+) (?:is|was) (?:an? |the )?'
                      r'([a-z][a-z ]*?)(?=\s{2,}|[,.\n]|$)', re.I)
DRAWN_RE = re.compile(r'\bwhere an? ([a-z]+) was drawn\b', re.I)
COUNT_WORDS = {"TWO": 2, "THREE": 3}

# A citation this step owes a stub row or a name, not a contract: the
# setting-level artifact another step's template already wrote.
_ELSEWHERE: set | None = None


class ContextError(Exception):
    pass


def written_elsewhere() -> set:
    global _ELSEWHERE
    if _ELSEWHERE is None:
        g = read_set_graph()
        out: set = set()
        for sid, names in g["step_templates"].items():
            if sid == "4c":
                continue
            for name in names:
                out |= {f for f in g["template_roots"].get(name, set())
                        if f.startswith("setting/")}
        _ELSEWHERE = out
    return _ELSEWHERE


def cites(text: str, self_rel: str) -> list[str]:
    out = []
    for prefixed, folder, fname in PATTERN_CITE_RE.findall(text):
        if folder == "setting" and not prefixed:
            continue
        f = f"{folder}/{fname}"
        if f != self_rel and f not in out:
            out.append(f)
    return out


# ---------------------------------------------------------------------------
# What this location is, read off what 3a to 4b already wrote
# ---------------------------------------------------------------------------

class Stub:
    def __init__(self, code: str):
        m = re.fullmatch(r'([A-Z]+)\.(\d+)', code.strip())
        if not m:
            raise ContextError(f"{code}: not a location code, which is like C.5")
        self.code, self.region, self.num = code.strip(), m.group(1), int(m.group(2))
        gaz = sc.parse_regions_gazetteer()
        if self.region not in gaz:
            raise ContextError(f"{code}: region {self.region} is not in "
                               f"setting/region/Regions.md")
        self.region_name = gaz[self.region]["name"]
        self.rating = gaz[self.region]["rating"]
        self.die = gaz[self.region].get("die", "")
        stubs = sc.parse_locations_gazetteer(self.region)
        if self.num not in stubs:
            raise ContextError(f"{code}: no such stub in setting/region/{self.region}/"
                               f"Locations.md")
        stub = stubs[self.num]
        self.name = stub["name"]
        self.weight = stub.get("weight") or None
        self.tags = stub.get("tags", "")
        self.block = self.basis = None
        self.exits = self._exits()

    @property
    def entry_file(self) -> str:
        key = (self.rating, self.weight if self.rating != "SAFE" else None)
        if key not in ENTRY_FILES:
            raise ContextError(f"{self.code}: a {self.rating} stub carrying "
                               f"{self.weight!r} names no class file")
        return ENTRY_FILES[key]

    def _exits(self) -> list[dict]:
        rdir = SETTING / "region" / self.region
        if not rdir.exists():
            return []
        names = {}
        for rcode in sc.parse_regions_gazetteer():
            try:
                stubs = sc.parse_locations_gazetteer(rcode)
            except FileNotFoundError:
                continue
            for num, stub in stubs.items():
                names[f"{rcode}.{num}"] = stub["name"]
        mmds = sorted(rdir.glob("*.mmd"))
        # Cross-region edges live in the neighbouring regions' diagrams too.
        for other in (SETTING / "region").glob("*/*.mmd"):
            if other.parent != rdir:
                mmds.append(other)
        out: list[dict] = []
        for path in mmds:
            text = path.read_text()
            _, edges, _ = parse_mmd_edges(text, LOC_NODE_RE)
            touching = [e for e in edges if self.code in (e[0], e[3])]
            members = re.search(r'^Locations:\s*(.+?)\s*$', text, re.M)
            if (path.parent == rdir and path.stem != "Connections" and members
                    and self.code in re.split(r'\s*,\s*', members.group(1))):
                header = dict(re.findall(r'^(Block|Basis):\s*(.+?)\s*$', text, re.M))
                self.block = header.get("Block")
                self.basis = (header.get("Basis", "").split(" - ")[0].strip().lower()
                              or None)
            for a, typ, label, b in touching:
                far = b if a == self.code else a
                kind = "vertical" if "vertical" in label else EDGE_KINDS.get(typ, "open")
                if any(e["far"] == far for e in out):
                    continue
                note = ""
                if typ == "-->":
                    note = " (one-way, out)" if a == self.code else " (one-way, in)"
                gate = label if label and "vertical" not in label else ""
                out.append({"far": far, "name": names.get(far, far), "kind": kind,
                            "note": note + (f" [{gate}]" if gate else "")})
        return out


# ---------------------------------------------------------------------------
# A pattern file's Spec, parsed into unit blocks and named draw blocks
# ---------------------------------------------------------------------------

class NamedBlock:
    """A `{NAME}` draw listed as its own fenced block further down the Spec."""

    def __init__(self, name: str, qualifier: str, items: list[tuple[str, str]]):
        self.name, self.qualifier, self.items = name, qualifier, items

    @property
    def mode(self) -> str:
        q = self.qualifier.lower()
        if "first of these that hits" in q:
            return "ladder"
        if "exactly one" in q:
            return "draw"
        return "decided"   # `by the weight of the room`, `decided per location`

    def values(self) -> list[str]:
        return [i for i, _ in self.items]

    def rungs(self) -> list[tuple[str, int | None]]:
        out = []
        for item, definition in self.items:
            m = re.match(r'\s*(\d+)%;', definition)
            out.append((item, int(m.group(1)) if m else None))
        return out


def spec_blocks(text: str) -> tuple[list[tuple[str, list[str]]], dict[str, NamedBlock]]:
    """(unit blocks as (header, lines), named draw blocks by name)."""
    m = re.search(r'\n## Spec\n(.*?)(?=\n## Constraints\n|\Z)', text, re.S)
    if not m:
        return [], {}
    fenced = re.findall(r'```\n?(.*?)```', m.group(1), re.S)
    referenced = {n.strip() for n in BRACE_RE.findall(m.group(1)) if NAMED_RE.match(n.strip())}
    units, named = [], {}
    for block in fenced:
        lines = [l for l in block.splitlines()]
        head = next((l for l in lines if l.strip()), "")
        hm = BLOCK_HEAD_RE.match(head.strip())
        name = hm.group(1).strip() if hm else ""
        if name in referenced:
            items = [(im.group(1).strip(), im.group(2).strip())
                     for im in map(ITEM_RE.match, lines[1:]) if im]
            named[name] = NamedBlock(name, (hm.group(2) or ""), items)
        else:
            units.append((head.strip(), lines[lines.index(head) + 1:] if head else lines))
    return units, named


def logical_lines(lines: list[str]) -> list[tuple[str | None, list[str]]]:
    """Group physical lines under the rate that opens them; comments and blanks
    stand alone with no rate."""
    out: list[tuple[str | None, list[str]]] = []
    for phys in lines:
        m = RATE_RE.match(phys)
        if m:
            out.append((m.group(1), [phys]))
        elif phys.strip().startswith("--") or not phys.strip():
            out.append((None, [phys]))
        elif out and out[-1][0] is not None:
            out[-1][1].append(phys)
        else:
            out.append((None, [phys]))
    return out


def spec_prose(text: str) -> str:
    m = re.search(r'\n## Spec\n(.*?)(?=\n## Constraints\n|\Z)', text, re.S)
    return re.sub(r'```.*?```', '', m.group(1), flags=re.S).strip() if m else ""


def constraints(text: str) -> str:
    m = re.search(r'\n## Constraints\n(.*)', text, re.S)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------------------
# The contract, resolved
# ---------------------------------------------------------------------------

class Resolution:
    """What one location's walk has settled so far, shared across files."""

    def __init__(self, stub: Stub, rerolls: dict, settled: dict):
        self.stub, self.rerolls, self.settled = stub, rerolls, settled
        # What holds for the whole location: the block's basis, and a kind a
        # line fixed before the file that draws it was opened.
        self.seeds: dict[frozenset, str] = {}
        self.record: list[tuple[str, str]] = []
        self.drawn_by_file: dict[tuple[str, str], set] = {}
        if stub.basis:
            self.seeds[frozenset({"purpose", "household"})] = stub.basis
        self.lock_owed = any(
            stub.code in e.locations[1:] for e in _registry("keys"))


class Instance:
    """One reading of one pattern file. A file cited by two lines - a second
    treasure, a second name - is read twice, and draws afresh the second time."""

    def __init__(self, res: Resolution, rel_path: str, n: int, fixed: dict,
                 differ_on: str | None = None):
        self.res, self.rel, self.n = res, rel_path, n
        self.domains: dict[frozenset, str] = dict(fixed)
        self.every: set[str] = set(fixed.values())
        self.fired_names: set[str] = set(res.settled)
        # `a second treasure, of a different disposition`: the named draw this
        # reading must not repeat, and what the earlier readings drew for it.
        self.differ_on = differ_on
        self.prior: set[str] = set(res.drawn_by_file.get((rel_path, differ_on), set())) \
            if differ_on else set()

    def note_drawn(self, name: str | None, value: str) -> None:
        self.every.add(value)
        if name:
            self.res.drawn_by_file.setdefault((self.rel, name), set()).add(value)

    def inherited(self, values: frozenset) -> str | None:
        return self.domains.get(values) or self.res.seeds.get(values)

    def key(self, ordinal: int) -> str:
        return f"{self.rel}#{ordinal}" + (f"~{self.n}" if self.n > 1 else "")

    def value_of(self, word: str) -> tuple[bool, str | None]:
        """(whether a settled dimension holds `word`, what that dimension drew)."""
        low = word.lower()
        for domains in (self.domains, self.res.seeds):
            for values, drawn in domains.items():
                if low in values:
                    return True, drawn
        return False, None


def _registry(kind: str) -> list:
    try:
        return sc.parse_registry(kind)
    except FileNotFoundError:
        return []


class Out:
    """One resolved logical line, ready to print."""

    def __init__(self, marker: str, physical: list[str], notes: list[str]):
        self.marker, self.physical, self.notes = marker, physical, notes


def exit_condition(text: str, exits: list[dict]) -> bool | None:
    """A LOW concealed-detail rate is parameterized by the room's own exits."""
    n = len(exits)
    secret = sum(1 for e in exits if e["kind"] == "secret")
    t = " ".join(text.lower().split())
    if "one mundane exit and a secret one" in t:
        return n == 2 and secret == 1
    if "exactly one exit and it is mundane" in t:
        return n == 1 and secret == 0
    if "every other exit count" in t:
        return not ((n == 2 and secret == 1) or (n == 1 and secret == 0))
    return None


def alternation_map(rel_path: str) -> list[tuple[frozenset, dict]]:
    """A file's paired kinds: each set of values, and the value each cited file
    stands for."""
    path = PATTERNS / rel_path
    if not path.exists():
        return []
    units, _ = spec_blocks(path.read_text())
    out = []
    for _, lines in units:
        for rate, physical in logical_lines(lines):
            if rate is None:
                continue
            text = "\n".join(physical)
            b = BRACE_RE.search(text)
            if not b:
                continue
            items = items_of(" ".join(b.group(1).split()))
            line_cites = cites(text, rel_path)
            if len(items) == len(line_cites) > 1:
                out.append((frozenset(i.lower() for i, _ in items),
                            {c: i.lower() for c, (i, _) in zip(line_cites, items)}))
    return out


def fixed_kinds(line_cites: list[str]) -> tuple[list[str], dict[str, dict]]:
    """A line naming a classifier and one of its own kinds has fixed that kind.

    `mechanism fixed to trap (dangerous/Hazard.md, dangerous/Trap.md)` settles
    Hazard's mechanism before Hazard is read; Trap is then reached through
    Hazard rather than read a second time beside it.
    """
    follow, fixed = list(line_cites), {}
    for parent in line_cites:
        for values, by_file in alternation_map(parent):
            for child in line_cites:
                if child != parent and child in by_file:
                    fixed.setdefault(parent, {})[values] = by_file[child]
                    if child in follow:
                        follow.remove(child)
    return follow, fixed


def resolve_line(inst: Instance, key: str, rate: str, physical: list[str],
                 named: dict[str, NamedBlock], exit_slot: dict | None
                 ) -> tuple[Out, list[str], dict[str, dict]]:
    """One logical line: whether it applies, what it draws, and what it opens."""
    res, rel_path = inst.res, inst.rel
    code, text = res.stub.code, "\n".join(physical)
    flat = " ".join(text.split())
    body = RATE_RE.sub("", physical[0], count=1).strip()
    notes: list[str] = []
    kept, marker = True, " "

    # the rate
    if rate.endswith("%"):
        kept, _ = fires(code, int(rate[:-1]), key, res.rerolls.get(key, 0))
        marker = "+" if kept else "-"
    elif rate in PROMINENCES:
        prom = res.settled.get("prominence")
        if prom:
            kept = prom == rate
            marker = "+" if kept else "-"

    # a condition on something already drawn, or already written
    def drop(note: str | None = None):
        nonlocal kept, marker
        kept, marker = False, "-"
        if note:
            notes.append(note)

    if kept and "lock obligation recorded against this room" in flat:
        if not res.lock_owed:
            drop("no setting/Keys.md row names this room as a lock")
        else:
            marker = "+"
    if kept:
        cond = exit_condition(flat, res.stub.exits)
        if cond is not None:
            kept, marker = cond, ("+" if cond else "-")
    if kept:
        lab = LABEL_RE.match(body)
        where = WHERE_RE.search(text)
        drawn_m = DRAWN_RE.search(text)
        not_drawn = re.match(r'([A-Za-z]+), where it was not already drawn', body)
        if lab:
            known, drawn = inst.value_of(lab.group(1))
            if known and drawn != lab.group(1).lower():
                drop(f"no {lab.group(1).lower()} here - {drawn} was drawn")
        elif not_drawn:
            if not_drawn.group(1).lower() in inst.every:
                drop(f"{not_drawn.group(1).lower()} was already drawn")
        elif drawn_m and drawn_m.group(1).upper() in named:
            if drawn_m.group(1).lower() not in inst.fired_names:
                drop(f"no {drawn_m.group(1).lower()} was drawn")
        elif where:
            known, drawn = inst.value_of(where.group(2).strip())
            if known and drawn != where.group(2).strip().lower():
                drop(f"the {where.group(1).lower()} here is {drawn}")

    if not kept:
        return Out(marker, physical[:1], notes), [], {}

    # the draws on the line, in order
    line_cites = cites(text, rel_path)
    braces = list(BRACE_RE.finditer(text))
    decided_here = re.search(r'never chosen here|read off|never re-decided', text)
    differs = re.search(r'not the kind already drawn|of a different', flat)
    count = next((n for w, n in COUNT_WORDS.items() if re.search(rf'\b{w}\b', text)), 1)
    chosen: list[str] | None = None
    for bi, bm in enumerate(braces):
        inner = " ".join(bm.group(1).split())
        bkey = f"{key}.{bi}"
        reroll = res.rerolls.get(bkey, 0)
        if NAMED_RE.match(inner):
            block = named.get(inner)
            if block is None:
                continue
            values = frozenset(v.lower() for v in block.values())
            if inner.lower() in res.settled:
                drawn = res.settled[inner.lower()]
            elif inst.inherited(values) and not differs:
                notes.append(f"{inner}: {inst.inherited(values)}   (settled earlier)")
                inst.domains[values] = inst.inherited(values)
                continue
            elif block.mode == "draw":
                exclude = set(inst.prior) if inst.differ_on == inner else set()
                if differs and values in inst.domains:
                    exclude.add(inst.domains[values])
                exclude |= {i.lower() for i, d in block.items
                            if re.search(r'\b(SAFE|WILD|DANGEROUS) only\b', d)
                            and not re.search(rf'\b{res.stub.rating} only\b', d)}
                drawn = pick(code, bkey, [(v, None) for v in block.values()], reroll,
                             exclude=exclude)
            elif block.mode == "ladder":
                drawn = ladder(code, bkey, block.rungs(), reroll)
            elif res.stub.weight and res.stub.weight in values:
                drawn = res.stub.weight          # `by the weight of the room`
            else:
                notes.append(f"{inner}: decide - {block.qualifier}")
                continue
            inst.domains[values] = drawn.lower()
            inst.note_drawn(inner, drawn.lower())
            inst.fired_names.add(inner.lower())
            definition = dict(block.items).get(drawn, "")
            notes.append(f"{inner}: {drawn} - {definition}   [{bkey}]")
            res.record.append((bkey, f"{inner}: {drawn}"))
            continue
        items = items_of(inner)
        if len(items) < 2:
            continue
        values = frozenset(i.lower() for i, _ in items)
        if exit_slot is not None and values == frozenset(
                {"open", "one-way", "secret", "vertical"}):
            inst.domains[values] = exit_slot["kind"]
            notes.append(f"kind: {exit_slot['kind']}   (the diagram's edge)")
            continue
        if values in inst.domains and not differs:
            drawn = inst.domains[values]
            notes.append(f"drew: {drawn}   (settled earlier)")
            picks = [drawn]
        elif decided_here:
            notes.append("read off what is already written - not drawn")
            continue
        else:
            exclude = {inst.domains[values]} if differs and values in inst.domains else set()
            picks = []
            for c in range(count):
                ckey = bkey if c == 0 else f"{bkey}#{c}"
                picks.append(pick(code, ckey, items, res.rerolls.get(ckey, 0),
                                  exclude=exclude | {x.lower() for x in picks}))
            notes.append(f"drew: {', '.join(picks)}   [{bkey}]")
            res.record.append((bkey, ", ".join(picks)))
        inst.domains[values] = picks[0].lower()
        for x in picks:
            inst.note_drawn(None, x.lower())
        if bi == 0 and len(items) == len(line_cites) > 1:
            chosen = [x.lower() for x in picks]
    if chosen is not None:
        first = [i.lower() for i, _ in items_of(" ".join(braces[0].group(1).split()))]
        follow = [line_cites[first.index(k)] for k in chosen if k in first]
        fixed: dict[str, dict] = {}
    else:
        follow, fixed = fixed_kinds(line_cites)
    other = re.search(r'\b(?:of|from) a different ([a-z]+)', flat)
    if other:
        fixed = {f: dict(fixed.get(f, {}), __differ__=other.group(1).upper())
                 for f in follow}
    return Out(marker, physical, notes), follow, fixed


class ResolvedFile:
    def __init__(self, inst: Instance):
        self.rel, self.n = inst.rel, inst.n
        self.blocks: list[tuple[str, list[Out]]] = []
        self.named: dict[str, NamedBlock] = {}
        self.prose = self.constraints = ""


def resolve_file(inst: Instance) -> tuple[ResolvedFile, list[tuple[str, dict]]]:
    """One reading of one file: its unit blocks resolved, per exit where a block
    says `every exit`, and what its kept lines open."""
    res = inst.res
    text = (PATTERNS / inst.rel).read_text()
    units, named = spec_blocks(text)
    rf = ResolvedFile(inst)
    rf.named, rf.prose, rf.constraints = named, spec_prose(text), constraints(text)
    opened: list[tuple[str, dict]] = []
    ordinal = 0
    for head, lines in units:
        per_exit = "every exit" in head.lower()
        slots = res.stub.exits if per_exit and res.stub.exits else [None]
        outs: list[Out] = []
        start = ordinal
        for si, slot in enumerate(slots):
            ordinal = start
            if slot is not None:
                inst.domains = {}
            for rate, physical in logical_lines(lines):
                if rate is None:
                    if si == 0:
                        outs.append(Out(" ", physical, []))
                    continue
                ordinal += 1
                key = inst.key(ordinal) + (f"@{slot['far']}" if slot else "")
                out, follow, fixed = resolve_line(inst, key, rate, physical, named, slot)
                if slot is not None:
                    out.notes = [f"{slot['far']}: {n}" for n in out.notes] or \
                        ([f"{slot['far']}: not here"] if out.marker == "-" else [])
                    if si > 0:
                        out.physical = []
                outs.append(out)
                opened += [(f, fixed.get(f, {})) for f in follow]
        rf.blocks.append((head, outs))
    return rf, opened


def resolve(stub: Stub, rerolls: dict, settled: dict) -> tuple[list[ResolvedFile], Resolution]:
    """The class file, and a fresh reading of every file a kept line opens.

    A file opened by two lines is read twice; one opened again only because a
    classifier already reached it through a fixed kind is not.
    """
    res = Resolution(stub, rerolls, settled)
    order: list[ResolvedFile] = []
    readings: dict[str, int] = {}
    elsewhere = written_elsewhere()
    queue: list[tuple[str, dict]] = [(stub.entry_file, {})]
    while queue:
        rel_path, fixed = queue.pop(0)
        if rel_path in elsewhere or not (PATTERNS / rel_path).exists():
            continue
        readings[rel_path] = readings.get(rel_path, 0) + 1
        if readings[rel_path] > 3:
            continue
        fixed = dict(fixed)
        differ_on = fixed.pop("__differ__", None)
        inst = Instance(res, rel_path, readings[rel_path], fixed, differ_on)
        rf, opened = resolve_file(inst)
        order.append(rf)
        queue.extend(opened)
    return order, res


def draw_record(code: str) -> list[tuple[str, str]]:
    """Every draw this location's contract made, recomputed from the code."""
    _, res = resolve(Stub(code), {}, {})
    return res.record


# ---------------------------------------------------------------------------
# The stream
# ---------------------------------------------------------------------------

REGISTRIES = (("lore", "Lore"), ("keys", "Keys"), ("quests", "Quest"),
              ("named_creatures", "Named Creature"),
              ("unique_treasures", "Unique Treasure"))


def registry_names() -> list[tuple[str, list[str]]]:
    out = []
    try:
        out.append(("Bestiary", [b["name"] for b in sc.parse_bestiary()]))
    except FileNotFoundError:
        pass
    try:
        out.append(("Factions", [f["name"] for f in sc.parse_factions()[0]]))
    except FileNotFoundError:
        pass
    for kind, label in REGISTRIES:
        try:
            out.append((label, [e.title for e in sc.parse_registry(kind)]))
        except FileNotFoundError:
            continue
    return [(label, names) for label, names in out if names]


def recorded_against(code: str) -> list[str]:
    out = []
    for kind, label in REGISTRIES:
        try:
            entries = sc.parse_registry(kind)
        except FileNotFoundError:
            continue
        for entry in entries:
            if code in entry.locations:
                out.append(f"{label}: {entry.title}  ({' '.join(entry.locations)})")
    return out


def template_body() -> str:
    text = (TEMPLATES / "Location.md").read_text()
    m = re.search(r'\n## Instructions\n.*', text, re.S)
    return ("## Instructions" + m.group(0).split("## Instructions", 1)[1]).strip() \
        if m else text.strip()


def prefix_files(region: str) -> list[Path]:
    """What every room of one region reads identically, in a fixed order."""
    return [p for p in (ROOT / "GENRE.md", ROOT / "STYLE.md", ROOT / "BRIEF.md",
                        SETTING / "Procedures.md", SETTING / "Language.md",
                        SETTING / "Truths.md", SETTING / "region" / f"{region}.md")
            if p.exists()]


def render_prefix(region: str) -> str:
    out = [f"# Step 4c context - region {region}", "",
           "Everything above the line `## This location` is identical for every room "
           "of this region. Write the location from this stream and nothing else.", ""]
    for path in prefix_files(region):
        out += [f"## {rel(path)}", "", path.read_text().strip(), ""]
    out += [f"## The format ({rel(TEMPLATES / 'Location.md')})", "", template_body(), ""]
    return "\n".join(out)


def render_suffix(stub: Stub, rerolls: dict, settled: dict) -> str:
    out: list[str] = []
    w = out.append
    w(f"## This location - {stub.code} {stub.name}")
    w("")
    w(f"Write `setting/region/{stub.region}/{stub.num}.md`.")
    w("")
    w(f"{stub.code} **{stub.name}**" + (f" ({stub.weight})" if stub.weight else "")
      + f" - *{stub.tags}*")
    w(f"Region: {stub.region} {stub.region_name} - {stub.rating}"
      + (f", {stub.die}" if stub.die else ""))
    if stub.block:
        w(f"Block: {stub.block}" + (f" ({stub.basis})" if stub.basis else ""))
    w("")
    w("### Exits, as the diagrams drew them")
    w("")
    if stub.exits:
        for ex in stub.exits:
            arrow = "<-" if ex["note"].startswith(" (one-way, in)") else "->"
            w(f"  {ex['kind']:9s} {arrow} {ex['far']} {ex['name']}{ex['note']}")
        if any(ex["note"].startswith(" (one-way, in)") for ex in stub.exits):
            w("  `<-` arrives here and is no exit from this room - it is not listed under Exits")
    else:
        w("  (none drawn at 4b)")
    w("")
    names = registry_names()
    if names:
        w("### Names a citation may use")
        w("")
        for label, entries in names:
            w(f"  {label}: {', '.join(entries)}")
        owed = recorded_against(stub.code)
        if owed:
            w("")
            w("Already recorded against this room by a location written earlier:")
            for line in owed:
                w(f"  {line}")
        w("")
    w("### The contract, resolved")
    w("")
    w("A rated or conditional line is marked `+` where it applies here and `-` where "
      "it does not; a `-` line was not followed into the files it cites. `->` is what "
      "a draw gave this room. To move one on: `--reroll KEY=1`, the key in brackets.")
    w("")
    files, _ = resolve(stub, rerolls, settled)
    for rf in files:
        w(f"#### {rf.rel}" + (f" (reading {rf.n})" if rf.n > 1 else ""))
        w("")
        for head, outs in rf.blocks:
            w("```")
            if head:
                w(head)
            for o in outs:
                for i, phys in enumerate(o.physical):
                    w(f"{o.marker if i == 0 else ' '}{phys}")
                for n in o.notes:
                    w(f"        -> {n}")
            w("```")
            w("")
        for name, block in rf.named.items():
            if block.mode == "decided":
                w(f"{name} - {block.qualifier}")
                for item, definition in block.items:
                    w(f"  {item} - {definition}")
                w("")
        if rf.prose:
            w(rf.prose)
            w("")
        if rf.constraints:
            w("Constraints:")
            w("")
            w(rf.constraints)
            w("")
    return "\n".join(out)


def tokens(text: str) -> int:
    """An estimate: four characters a token. The API's count_tokens is the
    measurement; this is for comparing strategies against each other."""
    return (len(text) + 3) // 4


# ---------------------------------------------------------------------------
# The cost model
# ---------------------------------------------------------------------------

CACHE_WRITE, CACHE_READ = 1.25, 0.10   # x base input price, 5-minute TTL


def single_session_read_set(region: str, rating: str) -> str:
    """What one session writing a whole region reads once: the prefix, and every
    pattern file any of the region's class files reaches, unresolved."""
    g = read_set_graph()
    entries = {f for (r, _), f in ENTRY_FILES.items() if r == rating}
    from validate_setting import spec_closure
    files = sorted(spec_closure(entries, g["pattern_files"]) - written_elsewhere())
    parts = [render_prefix(region)]
    for f in files:
        parts.append((PATTERNS / f).read_text())
    for label in ("Locations.md",):
        p = SETTING / "region" / region / label
        if p.exists():
            parts.append(p.read_text())
    for p in sorted((SETTING / "region" / region).glob("*.mmd")):
        parts.append(p.read_text())
    return "\n".join(parts)


def cost_report(regions: list[str], harness: int, turns: int) -> str:
    gaz = sc.parse_regions_gazetteer()
    out = [f"COST MODEL - input tokens in base-price units (estimate: 4 chars/token)",
           f"  harness per call {harness:,}; cache write x{CACHE_WRITE}, read x{CACHE_READ};"
           f" single-session turns per room {turns}",
           "  Output tokens are the same under every strategy and are left out.", ""]
    grand = [0.0, 0.0, 0.0, 0.0]
    for code in regions:
        rdir = SETTING / "region" / code
        rooms = sorted((int(p.stem) for p in rdir.glob("[0-9]*.md")))
        if not rooms:
            continue
        rating = gaz[code]["rating"]
        prefix = tokens(render_prefix(code))
        suffixes, outputs = [], []
        for num in rooms:
            stub = Stub(f"{code}.{num}")
            suffixes.append(tokens(render_suffix(stub, {}, {})))
            outputs.append(tokens((rdir / f"{num}.md").read_text()) + 60)
        read_set = tokens(single_session_read_set(code, rating))

        # A: one session, the whole read set once, every room written in turn.
        a, ctx = 0.0, harness + read_set
        a += ctx * CACHE_WRITE
        for o in outputs:
            for _ in range(turns):
                a += ctx * CACHE_READ + o / turns * CACHE_WRITE
                ctx += o / turns
        a_final_ctx = ctx
        # B: a fresh call per room, nothing cached.
        b = sum(harness + prefix + s for s in suffixes)
        # C: a fresh call per room, harness and prefix cached, called in sequence.
        c = (harness + prefix) * CACHE_WRITE + (harness + prefix) * CACHE_READ * (len(rooms) - 1)
        c += sum(suffixes)
        # D: one session, the prefix once, each room's resolved contract fed in
        # as its turn - the session grows by contract and room, never by the
        # unresolved library.
        d, ctx = (harness + prefix) * CACHE_WRITE, harness + prefix
        for s, o in zip(suffixes, outputs):
            d += ctx * CACHE_READ + (s + o) * CACHE_WRITE
            ctx += s + o
        grand = [g + v for g, v in zip(grand, (a, b, c, d))]
        med = statistics.median(suffixes)
        out += [f"{code} {gaz[code]['name']} ({rating}, {len(rooms)} rooms)",
                f"  prefix {prefix:,} tok, suffix median {med:,.0f} (min {min(suffixes):,}, "
                f"max {max(suffixes):,}), room output median "
                f"{statistics.median(outputs):,.0f}",
                f"  single-session read set {read_set:,} tok; context at the last room "
                f"{a_final_ctx:,.0f}",
                f"  A one session, library read once      {a:>12,.0f}",
                f"  B fresh stream per room, no cache      {b:>12,.0f}   "
                f"({b / a:.1f}x A)",
                f"  C fresh stream per room, prefix cached {c:>12,.0f}   "
                f"({c / a:.1f}x A)",
                f"  D one session, contracts fed per room  {d:>12,.0f}   "
                f"({d / a:.1f}x A)", ""]
    if sum(grand):
        a, b, c, d = grand
        out += ["ALL", f"  A {a:,.0f}   B {b:,.0f} ({b / a:.1f}x)   C {c:,.0f} ({c / a:.1f}x)"
                f"   D {d:,.0f} ({d / a:.1f}x)"]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    rerolls: dict = {}
    settled: dict = {}
    words_only = False
    harness, turns = 0, 1
    args: list[str] = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--words":
            words_only = True
        elif a in ("--reroll", "--set") and i + 1 < len(argv) and "=" in argv[i + 1]:
            k, _, v = argv[i + 1].rpartition("=")
            if a == "--reroll":
                rerolls[k] = int(v)
            else:
                settled[k.lower()] = v.lower()
            i += 1
        elif a in ("--harness", "--turns") and i + 1 < len(argv) and argv[i + 1].isdigit():
            if a == "--harness":
                harness = int(argv[i + 1])
            else:
                turns = max(1, int(argv[i + 1]))
            i += 1
        else:
            args.append(a)
        i += 1
    try:
        if args and args[0] == "cost":
            regions = args[1:] or list(sc.parse_regions_gazetteer())
            print(cost_report(regions, harness, turns))
            return 0
        if len(args) != 2 or args[0] != "4c":
            print(__doc__)
            return 1
        stub = Stub(args[1])
        prefix, suffix = render_prefix(stub.region), render_suffix(stub, rerolls, settled)
        unknown = [k for k in rerolls if f"[{k}]" not in suffix]
        if unknown:
            raise ContextError(f"--reroll names no draw in {stub.code}'s stream: "
                               f"{', '.join(unknown)} - use the key exactly as printed "
                               "in brackets")
        if words_only:
            print(f"prefix {len(prefix.split()):,} words / {tokens(prefix):,} tok; "
                  f"suffix {len(suffix.split()):,} words / {tokens(suffix):,} tok")
        else:
            print(prefix + "\n" + suffix)
    except ContextError as e:
        print(f"context.py: {e}")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)
