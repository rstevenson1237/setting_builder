#!/usr/bin/env python3
"""The read set for one location, assembled and printed as one stream.

A 4c session used to open a dozen files and walk the pattern tree itself,
carrying every branch it did not take. This walks the tree once, resolves what
is arithmetic - which genre entry each drawn line gets, whether each rated line
fires here, per `tools/draw.py` - and prints what is left: the contract with its
answers already in it, the two levels above this room, and the format to write
it in. Nothing it prints is a file the session then has to go and read, and
nothing it leaves out is a file the session may go and read instead.

Three things are deliberately absent. A sibling location never appears, because
a room written against its neighbours' prose converges on them. A genre list
never appears, only the entry drawn from it, because a list in context is a menu
and a menu gets shopped. A registry appears only as the names a citation may
use, because what a name means is written at 4d, with every location that cites
it in view.

`GENRE.md` and `STYLE.md` are not printed either, and for the opposite reason:
`CLAUDE.md` requires them re-read at every generation step, so they are open
already.

Usage: python3 tools/context.py 4c CODE [--reroll SLOT=N ...] [--words]

  CODE          a location code (`D.5`)
  --reroll      move one draw on. The key is the file its line sits under plus
                the bracket printed beside it - `--reroll dangerous/Door.md#2=1`,
                or `dangerous/Door.md#2@D.1=1` for one exit's. Repeatable.
  --words       print the stream's word count instead of the stream

Exits 1 where the code names no location in a region that has reached 4a.
"""
from __future__ import annotations

import re
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import site_common as sc  # noqa: E402
from draw import (  # noqa: E402
    DrawError,
    draw,
    facet_of,
    fires,
    list_entries,
    list_path,
    roll,
)
from validate_setting import (  # noqa: E402
    EDGE_KINDS,
    LOC_NODE_RE,
    PATTERNS,
    ROOT,
    SETTING,
    SPEC_RATE_RE,
    line_pattern_cites,
    list_cites,
    parse_mmd_edges,
    procedures_conditions,
    read_set_graph,
    rel,
    spec_fenced_blocks,
    spec_logical_lines,
)

TEMPLATES = ROOT / "templates"
EXEMPLARS = ROOT / "style" / "exemplars" / "location"

# A location's class file, from its rating and its stub's weight. The same map
# templates/Location.md's Context section states, which is where a reader looks
# to see why a given file is the entry point.
ENTRY_FILES = {
    ("SAFE", None): "safe/Settlement.md",
    ("WILD", "landmark"): "wild/Landmark.md",
    ("WILD", "hidden"): "wild/Hidden.md",
    ("WILD", "secret"): "wild/Secret.md",
    ("DANGEROUS", "high"): "dangerous/High.md",
    ("DANGEROUS", "medium"): "dangerous/Medium.md",
    ("DANGEROUS", "low"): "dangerous/Low.md",
}

# A block header may scope its block to something the location has several of.
# The only scope so far is the exit, and `dangerous/Door.md` declares it in its
# own header, so the block is resolved once per exit the diagram drew.
EXIT_SCOPE_RE = re.compile(r'-\s*every exit\s*$')

RATE_PCT_RE = re.compile(r'^(\d+)%$')


class ContextError(Exception):
    pass


# ---------------------------------------------------------------------------
# What this location is, read off what 3a to 4b already wrote
# ---------------------------------------------------------------------------

class Stub:
    def __init__(self, code: str):
        m = re.fullmatch(r'([A-Z]+)\.(\d+)', code.strip())
        if not m:
            raise ContextError(f"{code}: not a location code, which is like D.5")
        self.code, self.region, self.num = code.strip(), m.group(1), int(m.group(2))
        gaz = sc.parse_regions_gazetteer()
        if self.region not in gaz:
            raise ContextError(f"{code}: region {self.region} is not in "
                               f"setting/region/Regions.md - STEPS.md step 3a first")
        self.region_name = gaz[self.region]["name"]
        self.rating = gaz[self.region]["rating"]
        self.die = gaz[self.region].get("die", "")
        stubs = sc.parse_locations_gazetteer(self.region)
        if self.num not in stubs:
            raise ContextError(f"{code}: no such stub in setting/region/{self.region}/"
                               f"Locations.md - STEPS.md step 4a first")
        stub = stubs[self.num]
        self.name = stub["name"]
        self.weight = stub.get("weight") or None
        self.tags = stub.get("tags", "")
        self.block = self.purpose = None
        self.exits = self._exits()

    @property
    def known(self) -> list:
        """What is already settled about this room that a faceted list names.

        Its block's purpose is one: `purposes` is faceted by the same eight
        words `patterns/region/Dangerous.md` gives a block, so a room in a
        block for believing draws a purpose for believing.
        """
        return [self.purpose] if self.purpose else []

    @property
    def entry_file(self) -> str:
        key = (self.rating, self.weight)
        if key not in ENTRY_FILES:
            raise ContextError(f"{self.code}: a {self.rating} stub carrying "
                               f"{self.weight!r} names no class file")
        return ENTRY_FILES[key]

    def _exits(self) -> list[dict]:
        """Every edge the diagrams draw at this location, far end named.

        The far end is a name, never its entry: a room written with its
        neighbours' prose in context converges on them.
        """
        rdir = SETTING / "region" / self.region
        if not rdir.exists():
            return []
        # Every region's stubs, since a block diagram may name a far end in
        # another region and a bare code tells the generator nothing.
        names = {}
        for rcode in sc.parse_regions_gazetteer():
            for num, stub in sc.parse_locations_gazetteer(rcode).items():
                names[f"{rcode}.{num}"] = stub["name"]
        out: list[dict] = []
        for path in sorted(rdir.glob("*.mmd")):
            text = path.read_text()
            _, edges, _ = parse_mmd_edges(text, LOC_NODE_RE)
            touching = [e for e in edges if self.code in (e[0], e[3])]
            if touching and path.stem != "Connections":
                self.block, self.purpose = block_header(text)
            for a, typ, label, b in touching:
                far = b if a == self.code else a
                kind = label.strip() or EDGE_KINDS.get(typ, "open")
                note = ""
                if typ == "-->":
                    note = " (one-way, out of here)" if a == self.code \
                        else " (one-way, into here)"
                # A cross-block edge is declared in both blocks' diagrams, per
                # STEPS.md 4b, so the same exit is met twice and is one exit.
                if any(e["far"] == far and e["kind"] == kind for e in out):
                    continue
                # An edge's label is read first and its arrow second: `vertical`
                # is a label and `secret` is an arrow, and both name a facet of
                # the list a door draws from.
                out.append({"far": far, "name": names.get(far, far), "kind": kind,
                            "facets": [kind, EDGE_KINDS.get(typ, "open")],
                            "note": note})
        return out


def block_header(text: str) -> tuple[str | None, str | None]:
    """A block diagram's own name and purpose, per templates/Block_Connections.mmd."""
    fields = dict(re.findall(r'^(Block|Purpose):\s*(.+?)\s*$', text, re.M))
    if "Block" not in fields:
        return None, None
    purpose = fields.get("Purpose", "").strip()
    return (f"{fields['Block']} - {purpose}" if purpose else fields["Block"],
            purpose.lower() or None)


# ---------------------------------------------------------------------------
# The contract, resolved
#
# Four things a generator would otherwise decide are settled here, and each is
# settled the same way: from the location's own code, per tools/draw.py.
#
#   a rate       - whether a rated line appears in this room at all
#   a draw       - which entry of a cited list it gets
#   a kind       - which alternative an `{a | b | c}` line takes, and so which
#                  one of its files is in context rather than all of them
#   a condition  - whether a line conditional on something already drawn
#                  applies: `Guarded:`, or `where the challenge is an
#                  encounter`, is in the room where that was what was drawn,
#                  and nowhere else
#
# A line that did not fire keeps its first line and loses its detail, because
# the conditions some of them carry ("where this room has one mundane exit")
# are still read by the generator. What it does not keep is its files: an
# undrawn treasure takes its whole contract, and everything that contract
# draws, out of context, and that is where the read set actually shrinks.
#
# Where a rule cannot be applied safely it is not applied: an alternation whose
# alternatives do not pair one-to-one with its citations is left whole, and a
# condition naming nothing the block drew is left in. Every failure is toward
# printing more, never toward printing a resolution that is wrong.
# ---------------------------------------------------------------------------

# An alternation pairing one file per alternative - `{trap | environmental |
# residual}` and its three citations - is a Kind, and a Kind chosen freely is
# the first plausible one. Where the braces carry their own rates it is drawn
# against them, and where they do not it is drawn evenly.
ALT_RE = re.compile(r'\{([^{}]*\|[^{}]*)\}')
ALT_WEIGHT_RE = re.compile(r'^(.*?)\s+(\d+)%$')
# A rung of a tier ladder - `the first of these that hits, and nothing below
# it` - nested inside its parent line.
NESTED_RATE_RE = re.compile(r'^ {8,}(\d+)%\s{2,}\S')
# A line opening with one capitalised word and a colon is conditional on that
# word having been drawn: `Warded:`, `Hidden:`, `Guarded:`. So is a line naming
# what it depends on in a `where the X is Y` clause, which is how the same
# condition is written where it does not open the line.
LABEL_RE = re.compile(r'^([A-Z][a-z]+):\s')
WHERE_RE = re.compile(r'\bwhere the [a-z]+ (?:is|was) (?:an? |the )?'
                      r'([a-z][a-z ]*?)(?=\s{2,}|[,.]|$)')


def line_body(phys: str) -> str:
    m = SPEC_RATE_RE.match(phys)
    return phys[m.end():].strip() if m else phys.strip()


def alternatives(line_text: str) -> list[tuple[str, int | None]]:
    """`{a | b 20% | c}` as (alternative, weight or None), in its own order."""
    m = ALT_RE.search(line_text)
    if not m:
        return []
    out = []
    for raw in m.group(1).split("|"):
        w = ALT_WEIGHT_RE.match(" ".join(raw.split()))
        out.append((w.group(1), int(w.group(2))) if w else (" ".join(raw.split()), None))
    return out


@lru_cache(maxsize=None)
def facets_of(name: str) -> frozenset:
    """A list's facets, where every entry carries one and they repeat.

    A list whose entries are all distinct prefixes is not faceted - it is a
    list of phrases that happen to hold a dash.
    """
    try:
        entries = list_entries(list_path(name))
    except DrawError:
        return frozenset()
    facets = [facet_of(e)[0] for e in entries]
    if not entries or not all(facets) or len(set(facets)) >= len(entries):
        return frozenset()
    return frozenset(facets)


class Draw:
    def __init__(self, name, facet, number, total, text, key):
        self.name, self.facet, self.number = name, facet, number
        self.total, self.text, self.key = total, text, key

    def __str__(self) -> str:
        slot = f"{self.name}:{self.facet}" if self.facet else self.name
        return f"{slot} {self.number}/{self.total}: {self.text}"


class Run:
    """One Spec line, resolved for one slot - the room, or one of its exits."""

    def __init__(self, key):
        self.key, self.kept, self.dropped_by = key, True, None
        self.kind, self.inherited = None, False
        self.draws: list[Draw] = []
        self.nested: dict[int, bool] = {}
        self.walk: list[str] = []


class Line:
    def __init__(self, rate, physical, runs, per_exit):
        self.rate, self.physical = rate, physical
        self.runs, self.per_exit = runs, per_exit   # runs: one per slot

    @property
    def text(self) -> str:
        return "\n".join(self.physical)

    @property
    def kept(self) -> bool:
        return any(r.kept for r in self.runs) if self.runs else True

    @property
    def marker(self) -> str:
        """`+` or `-` only where something was settled: a rate, or a condition."""
        if not self.runs or self.rate is None:
            return " "
        if not RATE_PCT_RE.match(self.rate) \
                and not any(r.dropped_by for r in self.runs):
            return " "
        return "+" if self.kept else "-"

    def nested_marker(self, i: int) -> str:
        for run in self.runs:
            if i in run.nested:
                return "+" if run.nested[i] else "-"
        return " "


class ResolvedFile:
    def __init__(self, rel_path, blocks, prose, constraint_text):
        self.rel, self.blocks = rel_path, blocks
        self.prose, self.constraints = prose, constraint_text

    def edges(self) -> set:
        """What a line that applies here opens, and nothing a dropped one does."""
        return {f for block in self.blocks for line in block
                for run in line.runs if run.kept for f in run.walk}


def draw_list(code: str, name: str, key: str, known: list, rerolls: dict) -> Draw:
    """One list draw, filtered by anything already decided that names a facet.

    A faceted list is filtered by something the contract already settled, per
    patterns/SPEC.md. What this location already has settled is its block's
    purpose and, inside an exit-scoped block, the kind of edge the diagram drew.
    """
    facets = facets_of(name)
    facet = next((k for k in known if k in facets), None)
    number, total, text = draw(code, name, facet, key, rerolls.get(key, 0))
    return Draw(name, facet, number, total, text, key)


def pick_kind(code: str, key: str, alts: list, domains: list, state: dict,
              reroll: int) -> tuple[str, bool]:
    """Which alternative this line takes here, and whether it was inherited.

    A dimension drawn once is drawn once for the location: where another file
    has already settled `{guarded | hidden | discarded}`, this line reads that
    rather than drawing a second, contradicting answer. Within one block the
    opposite holds - a second challenge is a second thing - so a repeat there
    draws again, out of what the first one left.
    """
    values = frozenset(v.lower() for v, _ in alts)
    used = {d for vs, d in domains if vs == values and d}
    if values in state and not used:
        return state[values], True
    pool = [a for a in alts if a[0].lower() not in used] or list(alts)
    weights = [w for _, w in pool]
    chosen = pool[(roll(code, f"{key}~kind") + reroll) % len(pool)][0]
    if all(w is not None for w in weights) and sum(weights):
        value = (roll(code, f"{key}~kind") + reroll * 7) % sum(weights)
        for name, w in pool:
            if value < w:
                chosen = name
                break
            value -= w
    state[values] = chosen.lower()
    return chosen.lower(), False


def holds(label: str, domains: list) -> bool:
    """Whether a `Label:` line applies, against what this block drew.

    A label naming nothing the block settled is left alone - the block simply
    does not decide it, and dropping a line on a guess is the one failure this
    cannot recover from.
    """
    low = label.lower()
    for values, drawn in domains:
        if low in values:
            return drawn == low
    return True


@lru_cache(maxsize=None)
def alternation_map(rel_path: str) -> list[tuple[frozenset, dict]]:
    """A file's alternations, as the value each of its cited files stands for."""
    if not (PATTERNS / rel_path).exists():
        return []
    out = []
    for fenced in spec_fenced_blocks((PATTERNS / rel_path).read_text()):
        for rate, physical in spec_logical_lines(fenced):
            if rate is None:
                continue
            text = "\n".join(physical)
            alts, cites = alternatives(text), line_pattern_cites(text, rel_path)
            if len(alts) == len(cites) > 1:
                out.append((frozenset(v.lower() for v, _ in alts),
                            {c: v.lower() for c, (v, _) in zip(cites, alts)}))
    return out


def fix_kinds(cites: list, state: dict) -> None:
    """A line naming a classifier and one of its own kinds has fixed that kind.

    `mechanism fixed to trap (dangerous/Hazard.md, dangerous/Trap.md)` settles
    Hazard's mechanism before Hazard is read, so the file is drawn once here
    rather than drawing itself a second, contradicting answer.
    """
    for parent in cites:
        for values, by_file in alternation_map(parent):
            for cite in cites:
                if cite != parent and cite in by_file:
                    state.setdefault(values, by_file[cite])


def resolve_block(fenced: str, rel_path: str, code: str, known: list, slot: str,
                  rerolls: dict, state: dict, base: int) -> list[Run]:
    """One fenced block resolved for one slot, in the block's own order.

    A line's key is its position in the file, counting every block, so two
    blocks of one file never draw each other's entries.
    """
    runs: list[Run] = []
    domains: list[tuple[frozenset, str | None]] = []
    for ordinal, (rate, physical) in enumerate(spec_logical_lines(fenced), base + 1):
        if rate is None:
            runs.append(None)
            continue
        key = f"{rel_path}#{ordinal}" + (f"@{slot}" if slot else "")
        run, text = Run(key), "\n".join(physical)
        pct = RATE_PCT_RE.match(rate)
        if pct:
            run.kept, _ = fires(code, int(pct.group(1)), key, rerolls.get(key, 0))
        condition = LABEL_RE.match(line_body(physical[0])) or WHERE_RE.search(text)
        if run.kept and condition and not holds(condition.group(1), domains):
            run.kept, run.dropped_by = False, condition.group(1).lower()
        cites = line_pattern_cites(text, rel_path)
        names = sorted(list_cites(text))
        alts = alternatives(text) if not names else []
        if run.kept and not alts:
            fix_kinds(cites, state)
        if run.kept:
            for name in names:
                run.draws.append(draw_list(code, name, key, known, rerolls))
            if len(alts) > 1:
                run.kind, run.inherited = pick_kind(
                    code, key, alts, domains, state, rerolls.get(f"{key}~kind", 0))
            for i, phys in enumerate(physical):
                m = NESTED_RATE_RE.match(phys)
                if m:
                    run.nested[i], _ = fires(code, int(m.group(1)),
                                             f"{key}.{i}", rerolls.get(f"{key}.{i}", 0))
        if run.kind and len(alts) == len(cites) > 1:
            run.walk = [cites[[v.lower() for v, _ in alts].index(run.kind)]]
        elif run.kept:
            run.walk = list(cites)
        if run.kind:
            domains.append((frozenset(v.lower() for v, _ in alts), run.kind))
        for name in names:
            facets = facets_of(name)
            if facets:
                drawn = next((d.facet for d in run.draws if d.name == name), None)
                domains.append((frozenset(facets), drawn if run.kept else None))
        runs.append(run)
    return runs


def resolve_file(rel_path: str, stub: "Stub", rerolls: dict, state: dict) -> ResolvedFile:
    """One pattern file's Spec, resolved for this location.

    An exit-scoped block - `DOOR - every exit` says so in its own header - is
    resolved once per exit the diagram drew, so two exits out of one room are
    not the same door twice.
    """
    text = (PATTERNS / rel_path).read_text()
    blocks, base = [], 0
    for fenced in spec_fenced_blocks(text):
        head = fenced.splitlines()[:2]
        per_exit = stub.exits if any(EXIT_SCOPE_RE.search(h) for h in head) else []
        if per_exit:
            slots = [(ex["far"], ex["facets"] + stub.known) for ex in per_exit]
        else:
            slots = [(None, stub.known)]
        columns = [resolve_block(fenced, rel_path, stub.code, known, slot, rerolls,
                                 state, base)
                   for slot, known in slots]
        base += len(spec_logical_lines(fenced))
        lines = []
        for i, (rate, physical) in enumerate(spec_logical_lines(fenced)):
            runs = [col[i] for col in columns if col[i] is not None]
            lines.append(Line(rate, physical, runs,
                              [ex["far"] for ex in per_exit] if per_exit else []))
        blocks.append(lines)
    return ResolvedFile(rel_path, blocks, spec_prose(text), constraints(text))


def spec_prose(text: str) -> str:
    """The Spec section with its fenced blocks taken out.

    Per patterns/SPEC.md the prose under a block is only what changes a
    generator's output, so it travels with the block it qualifies.
    """
    m = re.search(r'\n## Spec\n(.*?)(?=\n## Constraints\n|\Z)', text, re.S)
    if not m:
        return ""
    return re.sub(r'```.*?```', '', m.group(1), flags=re.S).strip()


def constraints(text: str) -> str:
    m = re.search(r'\n## Constraints\n(.*)', text, re.S)
    return m.group(1).strip() if m else ""


def written_elsewhere() -> set:
    """The `patterns/setting/` files another step's template already answered.

    A 4c line citing one of these cites the artifact it produced - a Bestiary
    entry, a treasure table, a registry row - and what a location owes that
    artifact is a citation, or a stub row `templates/Location.md` states the
    shape of. The contract that wrote it belongs to the step that did. Read off
    the read-set graph rather than listed, so a new setting-level artifact
    needs no edit here.
    """
    g = read_set_graph()
    out: set = set()
    for sid, names in g["step_templates"].items():
        if sid == "4c":
            continue
        for name in names:
            out |= {f for f in g["template_roots"].get(name, set())
                    if f.startswith("setting/")}
    return out


def resolve(stub: "Stub", rerolls: dict) -> list[ResolvedFile]:
    """The class file and everything a line that applies here reaches."""
    order, seen, state = [], set(written_elsewhere()), {}
    queue = [stub.entry_file]
    while queue:
        rel_path = queue.pop(0)
        if rel_path in seen or not (PATTERNS / rel_path).exists():
            continue
        seen.add(rel_path)
        resolved = resolve_file(rel_path, stub, rerolls, state)
        order.append(resolved)
        queue.extend(sorted(resolved.edges() - seen))
    return order


def draw_record(code: str, rerolls: dict | None = None) -> list[tuple[str, str]]:
    """Every draw this location's contract made, as (key, draw).

    Arithmetic from the code alone, so it is recomputed rather than stored -
    which is what lets `tools/build_site.py` show it beside a location written
    sessions ago.
    """
    stub = Stub(code)
    rows = []
    for resolved in resolve(stub, rerolls or {}):
        for block in resolved.blocks:
            for line in block:
                for run in line.runs:
                    if run.kind:
                        rows.append((f"{run.key}~kind", f"kind: {run.kind}"))
                    rows.extend((d.key, str(d)) for d in run.draws)
    return rows


# ---------------------------------------------------------------------------
# The stream
# ---------------------------------------------------------------------------

REGISTRIES = (("lore", "Lore"), ("keys", "Keys"), ("quests", "Quest"),
              ("named_creatures", "Named Creature"),
              ("unique_treasures", "Unique Treasure"))


def registry_names() -> list[tuple[str, list[str]]]:
    out = [("Bestiary", [b["name"] for b in sc.parse_bestiary()]),
           ("Factions", [f["name"] for f in sc.parse_factions()[0]])]
    for kind, label in REGISTRIES:
        out.append((label, [e.title for e in sc.parse_registry(kind)]))
    return [(label, names) for label, names in out if names]


def recorded_against(code: str) -> list[str]:
    """Registry rows already naming this location.

    A row written by a location generated earlier is an obligation this one
    owes - a lock an earlier key named, a quest target, a creature placed here -
    and the weight file draws it at rate `1`. Its content is still 4d's.
    """
    out = []
    for kind, label in REGISTRIES:
        for entry in sc.parse_registry(kind):
            if code in entry.locations:
                where = " ".join(entry.locations)
                out.append(f"{label}: {entry.title}  ({where})")
    return out


def forced_damage_terms() -> list[str]:
    """The Types and Conditions a `(Test of ...)` citation may name.

    The grammar is `templates/Location.md`'s and the vocabulary is
    `setting/Procedures.md`'s, which is not printed here: a citation with no
    vocabulary is not a grammar, and the vocabulary is a list of names.
    """
    path = SETTING / "Procedures.md"
    if not path.exists():
        return []
    text = path.read_text()
    types = re.search(r'Type is\s+(.*?)\n\n', text, re.S)
    out = []
    if types:
        out.append("Types: " + ", ".join(
            re.findall(r'\*\*([A-Za-z]+)\*\*', types.group(1))))
    conditions = procedures_conditions()
    if conditions:
        out.append("Conditions: " + ", ".join(sorted(conditions)))
    return out


def exemplar_path(rating: str, weight: str | None) -> Path | None:
    if weight:
        exact = EXEMPLARS / f"{rating}-{weight}.md"
        if exact.exists():
            return exact
    matches = sorted(EXEMPLARS.glob(f"{rating}-*.md")) if EXEMPLARS.exists() else []
    return matches[0] if len(matches) == 1 else None


def template_body() -> str:
    """templates/Location.md from its Instructions on.

    Its Purpose and its Context are what this stream replaces: the Context
    section names the files to open, and everything it names is already here.
    """
    text = (TEMPLATES / "Location.md").read_text()
    m = re.search(r'\n## Instructions\n.*', text, re.S)
    return ("## Instructions" + m.group(0).split("## Instructions", 1)[1]).strip() \
        if m else text.strip()


def render(stub: Stub, rerolls: dict) -> str:
    out: list[str] = []
    w = out.append
    w(f"# Step 4c context - {stub.code} {stub.name}")
    w("")
    w(f"Write `setting/region/{stub.region}/{stub.num}.md` from what follows and nothing "
      f"else. Everything the class contract cites is already below, resolved: open no "
      f"further file. `GENRE.md` and `STYLE.md` are read beside this, per `CLAUDE.md`.")
    w("")

    w("## The stub")
    w("")
    w(f"{stub.code} **{stub.name}**"
      + (f" ({stub.weight})" if stub.weight else "") + f" - *{stub.tags}*")
    w(f"Region: {stub.region} {stub.region_name} - {stub.rating}"
      + (f", {stub.die}" if stub.die else ""))
    if stub.block:
        w(f"Block: {stub.block}")
    w("")
    w("## Its exits, as the diagram drew them")
    w("")
    if stub.exits:
        for ex in stub.exits:
            w(f"  {ex['kind']:9s} -> {ex['far']} {ex['name']}{ex['note']}")
        w("")
        w("A far end is a name here and nothing more. An exit leaving the map is written "
          "per the template and is not in the diagram.")
    else:
        w("  (none drawn at 4b)")
    w("")

    brief = SETTING / "region" / f"{stub.region}.brief.md"
    if brief.exists():
        w(f"## The brief ({rel(brief)})")
        w("")
        w(brief.read_text().strip())
        w("")

    overview = SETTING / "region" / f"{stub.region}.md"
    if overview.exists():
        w(f"## The region ({rel(overview)})")
        w("")
        w(overview.read_text().strip())
        w("")

    truths = SETTING / "Truths.md"
    if truths.exists():
        w(f"## The setting's truths ({rel(truths)})")
        w("")
        w(truths.read_text().strip())
        w("")

    names = registry_names()
    if names:
        w("## Names a citation may use")
        w("")
        w("A citation names one of these, or registers a new stub row - the name and "
          "this location, in the matching `setting/` file. What the name means is "
          "written at 4d.")
        w("")
        for label, entries in names:
            w(f"  {label}: {', '.join(entries)}")
        for line in forced_damage_terms():
            w(f"  {line}")
        w("")
        owed = recorded_against(stub.code)
        if owed:
            w("Already recorded against this room, by a location written earlier:")
            w("")
            for line in owed:
                w(f"  {line}")
            w("")

    w("## The contract, resolved")
    w("")
    w("Every line that applies to this room, with what it drew already in it. A rated "
      "line is marked `+` where it fired here and `-` where it did not, and a line "
      "marked `-` was not followed into the files it cites, which is why they are not "
      "below. To move one draw on, give `--reroll` the file it sits under and the key "
      "in brackets: `--reroll dangerous/Door.md#2@D.1=1`.")
    w("")
    for resolved in resolve(stub, rerolls):
        w(f"### {resolved.rel}")
        w("")
        for block in resolved.blocks:
            w("```")
            for line in block:
                if not line.physical:
                    continue
                w(f"{line.marker} {line.physical[0]}")
                if not line.kept:
                    run = line.runs[0] if line.runs else None
                    if run is not None and run.dropped_by:
                        w(f"      -> no {run.dropped_by} drawn here")
                    continue
                for i, extra in enumerate(line.physical[1:], 1):
                    w(f"{line.nested_marker(i)} {extra}")
                if line.per_exit:
                    rated = bool(RATE_PCT_RE.match(line.rate or ""))
                    for far, run in zip(line.per_exit, line.runs):
                        parts = ([f"kind {run.kind}"] if run.kind else []) + \
                            [f"{d.number}/{d.total} {d.text}" for d in run.draws]
                        tag = run.key[len(resolved.rel):]
                        if not run.kept:
                            if rated:
                                w(f"      -> {far}: not here   [{tag}]")
                        elif parts:
                            w(f"      -> {far}: {'; '.join(parts)}   [{tag}]")
                        elif rated:
                            w(f"      -> {far}: here   [{tag}]")
                    continue
                for run in line.runs:
                    if run.kind:
                        w(f"      -> kind: {run.kind}"
                          + ("   (settled earlier)" if run.inherited
                             else f"   [{run.key[len(resolved.rel):]}~kind]"))
                    for d in run.draws:
                        w(f"      -> {d}   [{d.key[len(resolved.rel):]}]")
            w("```")
            w("")
        if resolved.prose:
            w(resolved.prose)
            w("")
        if resolved.constraints:
            w("**Constraints**")
            w("")
            w(resolved.constraints)
            w("")

    ex = exemplar_path(stub.rating, stub.weight)
    if ex:
        w(f"## The register, on a page ({rel(ex)})")
        w("")
        w(ex.read_text().strip())
        w("")

    w(f"## The format ({rel(TEMPLATES / 'Location.md')})")
    w("")
    w(template_body())
    w("")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    rerolls: dict = {}
    words_only = False
    args: list[str] = []
    i = 0
    while i < len(argv):
        if argv[i] == "--words":
            words_only = True
        elif argv[i] == "--reroll":
            if i + 1 >= len(argv) or "=" not in argv[i + 1]:
                print("--reroll takes KEY=N, with the key printed beside the draw")
                return 1
            key, _, n = argv[i + 1].rpartition("=")
            rerolls[key] = int(n)
            i += 1
        else:
            args.append(argv[i])
        i += 1
    if len(args) != 2 or args[0] != "4c":
        print(__doc__)
        return 1
    try:
        stream = render(Stub(args[1]), rerolls)
    except (ContextError, DrawError) as e:
        print(f"context.py: {e}")
        return 1
    print(f"{len(stream.split()):,}" if words_only else stream)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)
