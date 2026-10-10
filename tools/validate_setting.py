#!/usr/bin/env python3
"""Structural validator for patterns/*/*.md and setting/ content.

Two independent checks: patterns/*/*.md's own citation format and Constraints
heading (runs unconditionally, regardless of what setting/ holds), and
generated content against the formats in templates/, the location graphs in
Connections.mmd files, and the cross-file registry constraints described in
STEPS.md (Lore/Keys/NamedCreatures/UniqueTreasures).

This is a structural linter, not a genre/content reviewer - it cannot judge
whether a Feature reads as "situations not authored plots" or whether magic
stays rare per GENRE.md. That judgment still belongs to whoever (or
whichever model) drafts and reviews the content by hand.

A file that is simply missing - a region, a location, a setting-level
document not built yet - is a warning, not an error: this validator is meant
to run against a build in progress, not just a finished one. Errors are
reserved for content that exists but is wrong (malformed, inconsistent with
something else that exists, or an unresolved/malformed citation).

Usage: python3 tools/validate_setting.py [--pending [REGION] | --location CODE | --read-set [STEP]]
Exits 1 if any error is found, 0 otherwise (warnings never fail the run).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import kdl  # noqa: E402
import site_common as sc  # noqa: E402  - the two generic readers live there
import tables  # noqa: E402

SETTING = ROOT / "setting"
PATTERNS = ROOT / "patterns"
STEPS_MD = ROOT / "STEPS.md"

ARTICLES = ("the ", "a ", "an ")


class Diagnostics:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path, msg):
        self.errors.append(f"{rel(path)}: {msg}")

    def warn(self, path, msg):
        self.warnings.append(f"{rel(path)}: {msg}")


def rel(p):
    try:
        return str(Path(p).relative_to(ROOT))
    except ValueError:
        return str(p)


def strip_article(name: str) -> str:
    n = name.strip()
    low = n.lower()
    for a in ARTICLES:
        if low.startswith(a):
            return n[len(a):].strip()
    return n


def names_match(a: str, b: str) -> bool:
    return strip_article(a).lower() == strip_article(b).lower()


def index_to_code(i: int) -> str:
    """0 -> A, 25 -> Z, 26 -> AA, ... (bijective base-26, matches Region_Gazetteer.md)."""
    i += 1
    s = ""
    while i > 0:
        i, rem = divmod(i - 1, 26)
        s = chr(65 + rem) + s
    return s


# ---------------------------------------------------------------------------
# patterns/*/*.md - citation format and Constraints heading
#
# Independent of setting/ content: this runs unconditionally, even on a fresh
# checkout with nothing generated yet. Citation grammar, decided when this
# check was added: a reference to another patterns/ file inside region/,
# safe/, wild/, or dangerous/ is always written bare as "folder/File.md" -
# never with a "patterns/" prefix, never bare of its folder - since none of
# those four folders share a filename with anything under setting/. A
# reference to a patterns/setting/*.md file is the one exception and always
# keeps the "patterns/" prefix, because a bare "setting/File.md" is reserved
# for the generated content file of the same name and is not checked here.
# ---------------------------------------------------------------------------

PATTERN_FOLDERS = ("setting", "region", "safe", "wild", "dangerous")
# The one pattern file outside the five folders: the tree's root, per
# patterns/SPEC.md's "The root".
PATTERN_ROOT_KEY = "Genre.md"
PATTERN_ROOT = PATTERNS / PATTERN_ROOT_KEY
# The lookbehind keeps this from misreading the tail of a longer, correct
# content path like "setting/region/Regions.md" as a bare two-segment
# "region/Regions.md" pattern citation - a real bug caught in this check's
# own first draft.
PATTERN_CITE_RE = re.compile(
    r'(?<!/)\b(patterns/)?(' + '|'.join(PATTERN_FOLDERS) + r')/([A-Za-z]+\.md)\b'
)
BARE_KIND_ARROW_RE = re.compile(r'->\s*([A-Z][A-Za-z]*\.md)\b')


def check_pattern_files(diag: Diagnostics):
    if not PATTERNS.exists():
        return
    pattern_files = sorted(p for p in PATTERNS.glob("*/*.md") if p.name != ".gitkeep")
    known = {p.relative_to(PATTERNS).as_posix() for p in pattern_files}
    if PATTERN_ROOT.exists():
        pattern_files.append(PATTERN_ROOT)
    else:
        diag.warn(PATTERN_ROOT, "missing - the pattern tree has no root, so reachability is "
                                "walked from the generation templates alone")
    for path in pattern_files:
        text = path.read_text()
        rel_key = path.relative_to(PATTERNS).as_posix()
        if "## Constraints" not in text:
            diag.error(path, "missing a '## Constraints' section - every patterns/*/*.md "
                              "file ends with one, even if its body is still empty")
        for m in PATTERN_CITE_RE.finditer(text):
            prefixed, folder, fname = m.groups()
            target = f"{folder}/{fname}"
            if target == rel_key:
                continue
            if folder == "setting":
                if not prefixed:
                    continue  # bare setting/X.md is a content reference, not a pattern citation
                if target not in known:
                    diag.error(path, f"cites patterns/{target}, which does not exist")
            else:
                if prefixed:
                    diag.error(path, f"cites patterns/{target} - citations to {folder}/ pattern "
                                      f"files are written bare, without the 'patterns/' prefix")
                    continue
                if target not in known:
                    diag.error(path, f"cites {target}, which does not exist")
        for m in BARE_KIND_ARROW_RE.finditer(text):
            diag.error(path, f"'-> {m.group(1)}' names a file with no folder - "
                              f"every citation states which patterns/ folder it points to")
        check_pattern_sections(diag, path, text)
        check_block_draws(diag, path, text)
        check_rate_notation(diag, path, text)


# ---------------------------------------------------------------------------
# patterns/*/*.md - section structure
#
# One skeleton, no declared tiers: Provides / Spec / Constraints. A Spec line
# either points to another pattern file or states a question the generator
# answers, which makes the library one tree - a file with outgoing citations
# is a classifier and a file without them is a leaf, and that is read off the
# citations rather than asserted anywhere. "Design questions" used to be a
# separate heading for a leaf file's own contract; it was the same grammar as
# a Spec, so it was folded back in.
#
# "## Design patterns" was a fourth, optional field for per-build compiled
# content - specific worked examples, kept apart from the neutral, permanent
# Spec. It is gone: a field that would have leaned on one now earns its
# precision from how the Spec question itself is phrased instead, per
# patterns/SPEC.md's governing rule. The heading is checked for and rejected
# the same way "Design questions" is, so a reintroduction is caught here
# rather than drifting back in unnoticed.
# ---------------------------------------------------------------------------


# A draw names a closed set: inline, {a | b | c}, or - when long or defined -
# by a block name in capitals, {TYPE}, listed as its own fenced block of that
# name further down the same Spec. The name has to resolve, or the generator
# is sent looking for a menu that is not there.
BLOCK_DRAW_RE = re.compile(r'\{([A-Z][A-Z0-9 ]*)\}')


def spec_blocks(text: str) -> dict[str, list[str]]:
    """Every fenced block in a pattern file's Spec, keyed by its header's name."""
    m = re.search(r'\n## Spec\n(.*?)(?=\n## Constraints\n|\Z)', text, re.S)
    out: dict[str, list[str]] = {}
    for fenced in re.findall(r'```\n?(.*?)```', m.group(1) if m else "", re.S):
        lines = fenced.strip("\n").splitlines()
        if lines:
            out[lines[0].split(" - ")[0].strip()] = lines[1:]
    return out


# A Spec line's rate is `1` or a percentage, per patterns/SPEC.md. Anything
# else in the rate column - `2`, `3-6`, `15+` - is read by this validator as a
# continuation of the line above, so the line it
# opens silently merges into its neighbour.
ODD_RATE_RE = re.compile(r'^ {2}(\d+(?:-\d+|\+)?)\s{2,}\S')


def check_rate_notation(diag: Diagnostics, path, text: str):
    blocks = spec_blocks(text)
    drawn = {n for body in blocks.values() for n in BLOCK_DRAW_RE.findall("\n".join(body))}
    for name, body in blocks.items():
        if name in drawn:
            continue    # a draw block's items are values, not rated lines
        for line in body:
            m = ODD_RATE_RE.match(line)
            if m and m.group(1) != "1":
                diag.warn(path, f"Spec line rated {m.group(1)!r} - patterns/SPEC.md allows `1` "
                                f"or a percentage, and the tools read this line as a "
                                f"continuation of the one above it: {line.strip()[:60]!r}")


def check_block_draws(diag: Diagnostics, path, text: str):
    blocks = spec_blocks(text)
    for body in blocks.values():
        for name in BLOCK_DRAW_RE.findall("\n".join(body)):
            if name not in blocks:
                diag.error(path, f"draws {{{name}}}, but its Spec has no fenced block "
                                 f"headed {name} to draw from")


def check_pattern_sections(diag: Diagnostics, path, text: str):
    has = lambda h: f"\n## {h}\n" in text or text.startswith(f"## {h}\n")
    for required in ("Provides", "Spec"):
        if not has(required):
            diag.error(path, f"missing a '## {required}' section - every patterns/*/*.md "
                              f"file carries one")
    if has("Design questions"):
        diag.error(path, "carries a '## Design questions' section, which was folded into "
                          "'## Spec' - a Spec line either cites a file or states a question")
    if has("Design patterns"):
        diag.error(path, "carries a '## Design patterns' section - per patterns/SPEC.md's "
                          "governing rule, a field that reads flat earns its precision from "
                          "how the Spec question is phrased, not from a worked example "
                          "attached to it")


# A logical Spec line opens with its rate in the left margin and runs until the
# next one does - continuation lines are indented further, and a citation list
# routinely wraps onto them. Grouping physically would split every wrapped draw
# away from the rate that governs it.
SPEC_RATE_RE = re.compile(r'^ {2}(1|\d+%|liner note|working|central)\s')


def spec_edges(text: str, rel: str):
    """Pattern files this file's Spec fenced blocks draw."""
    m = re.search(r'\n## Spec\n(.*?)(?=\n## Constraints\n)', text, re.S)
    if not m:
        return set()
    out = set()
    for fenced in re.findall(r'```(.*?)```', m.group(1), re.S):
        logical, cur = [], None
        for phys in fenced.splitlines():
            if SPEC_RATE_RE.match(phys):
                if cur:
                    logical.append(cur)
                cur = [phys]
            elif cur is not None:
                cur.append(phys)
        if cur:
            logical.append(cur)
        for chunk in logical:
            line = "\n".join(chunk)
            out |= {f"{folder}/{fname}"
                    for prefixed, folder, fname in PATTERN_CITE_RE.findall(line)
                    if f"{folder}/{fname}" != rel
                    and not (folder == "setting" and not prefixed)}
    return out


# ---------------------------------------------------------------------------
# The read-set graph: STEPS.md -> templates/ -> patterns/
#
# One direction, no back-pointers. A STEPS.md step names its template(s); a
# template names every pattern file a regeneration of its artifact requires;
# a pattern file's Spec names what it draws. Every edge is recorded in
# exactly one place, which is the property that keeps the graph in sync -
# a pattern file declaring which step reads it is a second copy of an edge
# the step and template already own, and a second copy is what drifts.
#
# Reachability is what this buys: a pattern file no generation template can
# reach is never read, so the content it describes is never generated. That
# is silent under-generation rather than a malformed file, so it warns here
# and is judged at STEPS.md step 5b, per templates/checks/Pattern_Judgement_Check.md.
#
# A phase-5 template is a review pass, and the pattern files it names are
# examples of what to review rather than inputs to a generation. They are
# excluded from the root set so an orphan cannot be masked by being cited as
# an example.
# ---------------------------------------------------------------------------

TEMPLATES = ROOT / "templates"
# A template is cited by its path under templates/, folder included
# (templates/region/Location.md), mirroring the folders of patterns/.
TEMPLATE_CITE_RE = re.compile(r'\btemplates/((?:[a-z]+/)?[A-Za-z_]+\.(?:md|mmd))\b')
# A template's pattern citations are always fully qualified - "patterns/" plus
# folder plus file. The elided form ("patterns/region/Safe.md, Wild.md") reads
# fine but hides an edge, so the graph requires the long form and the orphan
# warning is what surfaces an elision that dropped a file off the graph.
TEMPLATE_PATTERN_CITE_RE = re.compile(
    r'\bpatterns/(' + '|'.join(PATTERN_FOLDERS) + r')/([A-Za-z]+\.md)\b'
)
# The bare form is how one pattern file cites another (patterns/SPEC.md's
# citation grammar) and it is wrong in a template, where it drops the edge off
# the graph silently. "setting/" is excluded because a bare setting/X.md in a
# template is a reference to the generated content file of that name.
TEMPLATE_BARE_CITE_RE = re.compile(
    r'(?<!/)\b(' + '|'.join(f for f in PATTERN_FOLDERS if f != "setting") + r')/([A-Za-z]+\.md)\b'
)
TEMPLATE_STEP_CITE_RE = re.compile(r'\b[Ss]tep\s+([1-9][0-9]*[a-z])\b')
STEP_BODY_RE = re.compile(r'^\s*-\s+([1-9][0-9]*[a-z])\.(.*?)(?=\n\s*-\s+[1-9][0-9]*[a-z]\.|\n[1-9]\.|\Z)',
                          re.S | re.M)


def step_bodies() -> dict[str, str]:
    """Every STEPS.md step id mapped to its own text."""
    if not STEPS_MD.exists():
        return {}
    return {m.group(1): m.group(2) for m in STEP_BODY_RE.finditer(STEPS_MD.read_text())}


def spec_closure(entries: set, pattern_files: set) -> set:
    """Every pattern file reachable from these entry points by Spec edges."""
    reach, stack = set(entries), sorted(entries)
    while stack:
        cur = stack.pop()
        for target in spec_edges((PATTERNS / cur).read_text(), cur):
            if target in pattern_files and target not in reach:
                reach.add(target)
                stack.append(target)
    return reach


def read_set_graph():
    """STEPS.md -> templates -> pattern entry points -> Spec closure.

    Returns a dict of the whole graph so callers can report any layer of it:
    step_templates, template_roots, roots (generation only), reach, orphans.
    """
    bodies = step_bodies()
    step_templates = {sid: set(TEMPLATE_CITE_RE.findall(body)) for sid, body in bodies.items()}

    pattern_files = ({p.relative_to(PATTERNS).as_posix() for p in PATTERNS.glob("*/*.md")}
                     if PATTERNS.exists() else set())
    template_roots: dict[str, set] = {}
    for name in sorted({t for ts in step_templates.values() for t in ts}):
        path = TEMPLATES / name
        if not path.exists():
            continue
        template_roots[name] = {f"{folder}/{fname}"
                                for folder, fname in TEMPLATE_PATTERN_CITE_RE.findall(path.read_text())
                                if f"{folder}/{fname}" in pattern_files}

    # Roots come from generation steps only - phase 5 is review.
    roots: set = set()
    for sid, names in step_templates.items():
        if sid[0] == "5":
            continue
        for name in names:
            roots |= template_roots.get(name, set())

    reach = spec_closure(roots, pattern_files)
    # The tree's own root reaches what a build is *meant* to generate; the
    # templates reach what it actually enters. A file missing from the first
    # is outside the tree, one missing from the second is never generated.
    tree = (spec_closure({PATTERN_ROOT_KEY}, pattern_files | {PATTERN_ROOT_KEY})
            - {PATTERN_ROOT_KEY}) if PATTERN_ROOT.exists() else set(pattern_files)
    return dict(step_templates=step_templates, template_roots=template_roots,
                pattern_files=pattern_files, roots=roots, reach=reach,
                orphans=pattern_files - reach, outside_tree=pattern_files - tree)


def check_read_set_graph(diag: Diagnostics):
    if not PATTERNS.exists() or not STEPS_MD.exists():
        return
    g = read_set_graph()
    bodies = step_bodies()
    for sid, names in sorted(g["step_templates"].items()):
        if not names:
            if bodies.get(sid, "").strip().lower().startswith("retired"):
                continue
            diag.warn(STEPS_MD, f"step {sid} names no template - a step's template is what "
                                f"names the pattern files the step reads")
        for name in sorted(names):
            if not (TEMPLATES / name).exists():
                diag.error(STEPS_MD, f"step {sid} names templates/{name}, which does not exist")
    for name in sorted({n for ns in g["step_templates"].values() for n in ns}):
        path = TEMPLATES / name
        if not path.exists():
            continue
        text = path.read_text()
        for folder, fname in sorted(set(TEMPLATE_BARE_CITE_RE.findall(text))):
            if f"{folder}/{fname}" in g["pattern_files"]:
                diag.error(path, f"cites {folder}/{fname} bare - a template writes a pattern "
                                 f"citation as patterns/{folder}/{fname}, since the bare form "
                                 f"drops the edge off the read-set graph")
    known = set(g["step_templates"])
    for name in sorted({n for ns in g["step_templates"].values() for n in ns}):
        path = TEMPLATES / name
        if not path.exists():
            continue
        for sid in sorted(set(TEMPLATE_STEP_CITE_RE.findall(path.read_text())) - known):
            diag.error(path, f"cites step {sid}, which STEPS.md does not define")
    for stray in sorted(g["outside_tree"]):
        diag.warn(PATTERNS / stray, "patterns/Genre.md cannot reach this file - it is outside "
                                    "the tree, whatever a template says about it. Judged at "
                                    "STEPS.md step 5b")
    for orphan in sorted(g["orphans"]):
        diag.warn(PATTERNS / orphan, "no generation template reaches this file - nothing reads "
                                     "it, so the content it describes is never generated. "
                                     "Judged at STEPS.md step 5b")


def report_read_set(step_filter: str | None) -> int:
    """The read-set for each generation step, walked from its template(s)."""
    g = read_set_graph()
    if not g["step_templates"]:
        print("STEPS.md defines no steps - nothing to report.")
        return 0
    for sid, names in sorted(g["step_templates"].items()):
        if step_filter and sid != step_filter:
            continue
        entries: set = set()
        for name in names:
            entries |= g["template_roots"].get(name, set())
        closure = spec_closure(entries, g["pattern_files"])
        print(f"{sid}{'  (review pass)' if sid[0] == '5' else ''}")
        print(f"  templates : {', '.join(sorted(names)) or '(none)'}")
        print(f"  entries   : {', '.join(sorted(entries)) or '(none)'}")
        expanded = sorted(closure - entries)
        print(f"  expanded  : {', '.join(expanded) if expanded else '(none)'}")
        print()
    print(f"{len(g['reach'])}/{len(g['pattern_files'])} pattern files reachable from "
          f"generation templates; {len(g['orphans'])} orphan(s); "
          f"{len(g['outside_tree'])} outside patterns/Genre.md's tree")
    return 0


# ---------------------------------------------------------------------------
# patterns/*/*.md - the same sentence in three or more files
#
# Prose points to where something is; it never restates what is there, because
# every copy drifts from its original and the copy is the one a reader trusts.
# See "What prose owes" in patterns/SPEC.md.
#
# Two files saying the same thing is usually deliberate - restatement across
# the three rating folders is how a trap in SAFE gets differentiated from a
# trap in DANGEROUS, and parallel files carry parallel pointers. Three or more
# is the band where it stops being parallel structure and starts being a rule
# restated, which is why the threshold sits there rather than at two.
#
# This is a warning, not an error: the judgement of whether a given repetition
# is parallel structure stays human. Run against the tree before the sweep that
# introduced it, it found 47 copies across 13 sentences - the Spec preamble in
# twelve files, the edge/question rule in seven, the compiled-content note in
# five.
# ---------------------------------------------------------------------------

DUP_MIN_WORDS = 9
DUP_MIN_FILES = 3


def _normalise_sentence(s: str) -> str:
    s = re.sub(r'`[^`]*`', 'X', s)          # a cited filename is not the prose
    s = re.sub(r'[^a-z ]', ' ', s.lower())
    return " ".join(s.split())


def check_repeated_prose(diag: Diagnostics):
    if not PATTERNS.exists():
        return
    seen: dict[str, set] = {}
    original: dict[str, str] = {}
    for path in sorted(PATTERNS.glob("*/*.md")):
        rel = path.relative_to(PATTERNS).as_posix()
        text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        for raw in re.split(r'(?<=[.!?])\s+', text):
            raw = " ".join(raw.split())
            if len(raw.split()) < DUP_MIN_WORDS:
                continue
            key = _normalise_sentence(raw)
            if not key:
                continue
            seen.setdefault(key, set()).add(rel)
            original.setdefault(key, raw)
    for key, files in sorted(seen.items()):
        if len(files) >= DUP_MIN_FILES:
            diag.warn(PATTERNS, f"the same sentence appears in {len(files)} files "
                                f"({', '.join(sorted(files))}): {original[key][:90]!r} - "
                                f"prose points to where a rule lives rather than "
                                f"restating it; see 'What prose owes' in patterns/SPEC.md")


# ---------------------------------------------------------------------------
# Regions.md / setting/region/Connections.mmd
# ---------------------------------------------------------------------------

REGION_RE = re.compile(r'^([A-Z]+) (.+?) - (SAFE|WILD|DANGEROUS), (d\d+)\s*$')


REGION_COLUMNS = ["Code", "Name", "Gloss", "Rating", "Die", "Tag line"]
RATINGS = {"SAFE", "WILD", "DANGEROUS"}


def parse_regions(diag: Diagnostics):
    path = SETTING / "region" / "Regions.md"
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return {}
    tables = sc.read_tables(path)
    if not tables:
        diag.error(path, "holds no table - templates/region/Region_Gazetteer.md writes one pipe table")
        return {}
    t = tables[0]
    missing = [c for c in REGION_COLUMNS if c not in t.header]
    if missing:
        diag.error(path, f"table lacks column(s) {', '.join(missing)}")
    regions: dict[str, dict] = {}
    order: list[str] = []
    for d, line in zip(t.dicts(), t.lines):
        code, rating, die = d.get("Code", ""), d.get("Rating", ""), d.get("Die", "")
        if code in regions:
            diag.error(path, f"line {line}: duplicate region code {code}")
        if rating not in RATINGS:
            diag.error(path, f"line {line}: region {code} has rating {rating!r} - expected SAFE, WILD or DANGEROUS")
        if die and not re.fullmatch(r"d\d+", die):
            diag.error(path, f"line {line}: region {code} has die {die!r} - expected dN")
        regions[code] = {"name": d.get("Name", ""), "rating": rating, "die": die}
        order.append(code)
    expected = [index_to_code(idx) for idx in range(len(order))]
    if order != expected:
        diag.error(path, f"region codes not a plain A-Z progression: found {order}, expected {expected}")
    return regions


TOP_NODE_RE = re.compile(r'(\w+)\["([A-Z]+) - (.*?)"\]')
EDGE_RE = re.compile(
    r'(\w+)(?:\[[^\]]*\])?\s*(---|-\.-|-->)(?:\|([^|]*)\|)?\s*(\w+)(?:\[[^\]]*\])?')
EDGE_KINDS = {"---": "open", "-->": "one-way", "-.-": "secret"}


def parse_mmd_edges(text: str, node_re: re.Pattern):
    id_to_code: dict[str, str] = {}
    for m in node_re.finditer(text):
        id_to_code[m.group(1)] = m.group(2)
    edges = []
    unresolved: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.split("%%")[0]
        for m in EDGE_RE.finditer(line):
            a, typ, label, b = m.groups()
            ca, cb = id_to_code.get(a), id_to_code.get(b)
            if ca is None:
                unresolved.add(a)
            if cb is None:
                unresolved.add(b)
            if ca and cb:
                edges.append((ca, typ, (label or "").strip(), cb))
    return id_to_code, edges, unresolved


def edge_key(a: str, typ: str, label: str, b: str):
    """Identity of an edge, direction-sensitive only where the kind is."""
    ends = (a, b) if typ == "-->" else tuple(sorted((a, b)))
    return (ends, typ, label)


def check_top_connections(diag: Diagnostics, regions: dict):
    path = SETTING / "region" / "Connections.mmd"
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return []
    text = path.read_text()
    id_to_code, top_edges, unresolved = parse_mmd_edges(text, TOP_NODE_RE)
    for u in sorted(unresolved):
        diag.error(path, f"edge references node id {u!r} with no bracketed definition")
    codes_in_graph = set(id_to_code.values())
    for code in regions:
        if code not in codes_in_graph:
            diag.warn(path, f"region {code} has no node in the region-level Connections graph yet")
    for code in codes_in_graph:
        if code not in regions:
            diag.error(path, f"node references unknown region code {code}")
    return top_edges


# ---------------------------------------------------------------------------
# Per-region Locations.md + Connections.mmd
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Location files
# ---------------------------------------------------------------------------

LOC_HEADER_RE = re.compile(r'^([A-Z]+)\.(\d+) \*\*(.+?)\*\*(?: \((low|medium|high|landmark|hidden|secret)\))? - \*(.+)\*\s*$')
FEATURE_RE = re.compile(r'^\*\*([^*]+):\*\*\s*(.*)$')
EXIT_PAIR_RE = re.compile(r'->\s*([A-Z]+\.\d+)\s+([^,]+)')
EXIT_DEST_RE = re.compile(r'->\s*[A-Z]+\.\d+\s+[^,]+')

LORE_CITE_RE = re.compile(r'\(Lore:\s*([^)]+)\)')
KEYS_CITE_RE = re.compile(r'\(Keys:\s*([^)]+)\)')
QUEST_CITE_RE = re.compile(r'\(Quest:\s*([^)]+)\)')
NAMED_CITE_RE = re.compile(r'\(Named Creature:\s*([^)]+)\)')
UNIQUE_CITE_RE = re.compile(r'\(Unique Treasure:\s*([^)]+)\)')
TREASURE_CITE_RE = re.compile(r'\(Treasure\s+([IVX]+),\s*d20\)')
ROMAN_TABLES = {"I", "II", "III", "IV", "V"}


# ---------------------------------------------------------------------------
# The Feature grammar - templates/region/Location.md instruction 5
#
# A Feature is one sentence whose only separators are "," and "->". The banned
# punctuation is the whole point: a dash, a semicolon or a second sentence is
# the slot a trailing clause hangs in, and the trailing clause is where a
# Feature explains itself, dates itself, or writes down the party's conclusion.
# Removing the slot is cheaper than judging what fills it, and unlike the prose
# heuristics elsewhere in this file it is decidable, so separators are errors.
# ---------------------------------------------------------------------------

# Every parenthesised group is stripped before the grammar is applied: a
# citation is machinery, not prose, and its own commas and colons are not the
# sentence's. Where it sits is checked separately, since instruction 5 puts it
# last and a Feature that carries prose after one has hidden a second clause
# behind the machinery.
CITATION_RE = re.compile(r'\s*\([^()]*\)')
BANNED_SEP_RE = re.compile(r'(;|(?<!\*):(?!\*)|\s[-\u2013\u2014]\s|\.\s+\S)')
# feature_segments() below is still used by tools/metrics.py's corpus report;
# the validator itself no longer caps segment count or length.
SEG_SPLIT_RE = re.compile(r'\s*(?:,|->)\s*')
LIST_ITEM_WORDS = 3


def feature_segments(body: str) -> list[str]:
    """Body split per instruction 5, with a short-item list collapsed to one segment."""
    text = CITATION_RE.sub("", body).strip().rstrip(".")
    merged: list[str] = []
    run: list[str] = []
    for seg in (s.strip() for s in SEG_SPLIT_RE.split(text)):
        if not seg:
            continue
        if len(seg.split()) <= LIST_ITEM_WORDS:
            run.append(seg)
            continue
        if run:
            merged.append(" ".join(run))
            run = []
        merged.append(seg)
    if run:
        merged.append(" ".join(run))
    return merged


# ---------------------------------------------------------------------------
# STYLE.md - every bolded noun in a Player Summary appears below it as a Feature
#
# The summary is a promise about what the room contains, and an unkept one sends
# the referee improvising the thing the entry was supposed to hand them. The rule
# is absolute in STYLE.md, but matching a summary's phrasing to a Feature is not:
# a summary bolding "the pale residue" is kept by a Feature named "Warded
# Shelving" whose line describes that residue. So this warns rather than errors,
# and matches generously - against whole Feature lines rather than their labels
# alone, and on any one significant word - because a false positive here trains a
# reader to skim the warning list. A possessive is stripped from both sides, so
# "Stone Ward's" is kept by "Stone Ward", and the stopword list carries the words
# whose sharing proves nothing - "stone" and "old", and the qualifiers a bolded
# phrase picks up around its noun.
# ---------------------------------------------------------------------------

BOLD_RE = re.compile(r'\*\*([^*]+)\*\*')
# Words too common to make a match meaningful - a summary and a label sharing
# only "stone" or "old" have not been shown to be about the same thing.
SUMMARY_STOPWORDS = frozenset("""
the a an of to in on at by for with from that which it its is are was were be and or but as
into onto over under up down out off no not this these those their them they there here has
have had do does did than then so if when where while one two three four five six seven
eight nine ten old new great small long short high low own same other first last still
stone wall floor room place thing work water ground side end part
itself themselves except another rather only more most some each every any all both
anything nothing someone somebody anyone everything much many few little lot kind sort
""".split())


def _summary_tokens(phrase: str) -> set[str]:
    words = (re.sub(r"'s$", "", w) for w in re.findall(r"[a-z][a-z'-]+", phrase.lower()))
    return {w for w in words if len(w) > 2 and w not in SUMMARY_STOPWORDS}


def check_summary_promises(diag: Diagnostics, path: Path, summary: str, lines: list[str]):
    """Per STYLE.md, a bolded noun in the Player Summary is a Feature below it."""
    joined = re.sub(r"'s\b", "", " ".join(lines).lower())
    for raw in BOLD_RE.findall(summary):
        phrase = raw.strip()
        tokens = _summary_tokens(phrase)
        if not tokens:
            continue
        if any(tok in joined for tok in tokens):
            continue
        diag.warn(path, f"Player Summary promises **{phrase}** but no Feature below it "
                        f"carries that name - per STYLE.md the summary is a promise about "
                        f"what the room contains, and the referee improvises an unkept one")


# templates/region/Location.md instruction 2 - the sheet is raw material, the entry a
# few sentences. Warned rather than errored: length is judged, not parsed.
FEATURE_MAX_WORDS = 30
NOTES_MAX_SENTENCES = 3


def check_feature_grammar(diag: Diagnostics, path: Path, label: str, body: str):
    words = len(CITATION_RE.sub("", body).split())
    if words > FEATURE_MAX_WORDS:
        diag.warn(path, f"Feature '{label}' runs {words} words before its citation - "
                        f"templates/region/Location.md instruction 2 allows {FEATURE_MAX_WORDS}")
    last = None
    for m in CITATION_RE.finditer(body):
        last = m
    if last and body[last.end():].strip(" ."):
        diag.error(path, f"Feature '{label}' carries prose after its citation "
                         f"{last.group(0).strip()!r} - per instruction 5 of "
                         f"templates/region/Location.md a citation sits last")

    stripped = CITATION_RE.sub("", body).strip()
    sep = BANNED_SEP_RE.search(stripped)
    if sep:
        found = sep.group(0)
        what = ("a second sentence" if found.startswith(".")
                else f"{found.strip()!r}")
        diag.error(path, f"Feature '{label}' uses {what} - per instruction 5 of "
                         f"templates/region/Location.md a Feature is one sentence separated "
                         f"only by ',' and '->'")
        return
    if stripped and not body.rstrip().endswith((".", ")")):
        diag.error(path, f"Feature '{label}' does not end in a period")


def check_location_file(diag, path, region_code, num, stub, rating, all_locations,
                         mundane_edges, hidden_edges, citations, conditions=None):
    text = path.read_text()
    lines = text.splitlines()
    if not lines or not lines[0].strip():
        diag.error(path, "file is empty or missing its header line")
        return

    m = LOC_HEADER_RE.match(lines[0].strip())
    if not m:
        diag.error(path, f"header line does not match Location.md format: {lines[0]!r}")
        return
    check_treasure_citation_prose(diag, path, text)
    check_forced_damage(diag, path, text, conditions)
    hcode, hnum_s, hname, hweight, htags = m.groups()
    if hcode != region_code or int(hnum_s) != num:
        diag.error(path, f"header code {hcode}.{hnum_s} does not match this file's location {region_code}.{num}")
    if not names_match(hname, stub["name"]):
        diag.error(path, f"header name {hname!r} does not match its Locations.md stub name {stub['name']!r}")
    if rating in ("DANGEROUS", "WILD"):
        if hweight != stub["weight"]:
            diag.error(path, f"header weight/classification {hweight!r} does not match Locations.md stub {stub['weight']!r}")
    elif hweight:
        diag.error(path, f"{rating} region location should not carry a weight/classification tag in its header")
    if len([t for t in htags.split(",") if t.strip()]) != 3:
        diag.warn(path, f"header carries {htags.strip()!r} - expected exactly three tags")
    elif htags.strip().strip("*") != stub.get("tags", "").strip().strip("*"):
        diag.warn(path, f"header tags {htags.strip()!r} do not match its Locations.md stub's "
                        f"{stub.get('tags', '').strip()!r}")

    body = [l for l in lines[1:]]
    idx = 0
    while idx < len(body) and not body[idx].strip():
        idx += 1
    if idx >= len(body):
        diag.error(path, "missing Player Summary")
        return
    summary = body[idx].strip()
    if summary.startswith("*") and not summary.startswith("**"):
        diag.error(path, "Player Summary appears to be wrapped in italics - it should be plain text")
    idx += 1

    while idx < len(body) and not body[idx].strip():
        idx += 1
    if idx >= len(body):
        diag.error(path, "missing Referee Notes")
        return
    notes = body[idx].strip()
    if not (notes.startswith("*") and not notes.startswith("**") and notes.endswith("*") and not notes.endswith("**")):
        diag.error(path, "Referee Notes line is not wrapped in single-asterisk italics")
    sentences = len(re.findall(r'[.!?](?=\s|\*?$)', notes.strip("*").strip()))
    if sentences > NOTES_MAX_SENTENCES:
        diag.warn(path, f"Referee Notes run {sentences} sentences - templates/region/Location.md "
                        f"instruction 2 allows {NOTES_MAX_SENTENCES}")
    idx += 1

    features = []
    feature_lines = []
    exits_line = None
    for raw in body[idx:]:
        s = raw.strip()
        if not s:
            continue
        if s.startswith("**Exits:**"):
            exits_line = s
            continue
        fm = FEATURE_RE.match(s)
        if fm:
            label = fm.group(1)
            features.append(label)
            feature_lines.append(s)
            low = label.strip().lower()
            if low.startswith(ARTICLES):
                diag.error(path, f"Feature label '{label}' starts with a leading article")
            check_feature_grammar(diag, path, label, fm.group(2))

    check_summary_promises(diag, path, summary, feature_lines)

    if not features:
        diag.error(path, "no Feature lines found (expected at least one **Name:** line)")
    if exits_line is None:
        diag.error(path, "missing **Exits:** line")
    else:
        src = f"{region_code}.{num}"
        body = exits_line[len("**Exits:**"):].strip()
        descs = [d.strip(" ,") for d in EXIT_DEST_RE.split(body)]
        targets = EXIT_PAIR_RE.findall(body)
        seen_desc: dict[str, str] = {}
        for i, (code, name) in enumerate(targets):
            name = name.strip()
            desc = descs[i] if i < len(descs) else ""
            if code not in all_locations:
                diag.error(path, f"Exits cites unknown location code {code}")
                continue
            actual_name = all_locations[code]["name"]
            if not names_match(name, actual_name):
                diag.error(path, f"Exits names {code} as {name!r}, but its actual name is {actual_name!r}")
            in_mundane = (src, code) in mundane_edges
            in_hidden = (src, code) in hidden_edges
            if not in_mundane and in_hidden:
                # Common, legitimate pattern: the far side of an already-triggered
                # secret (a broken seal, a sprung passage) reads as a plain
                # opening even though the graph marks the connection hidden.
                # Worth a human glance, not an automatic failure.
                diag.warn(path, f"Exits lists {src} -> {code} as mundane, but the region Connections.mmd marks it hidden (-.-) - confirm this is the far side of an already-triggered secret, not a template violation")
            elif not in_mundane:
                diag.error(path, f"Exits lists {src} -> {code}, but no matching edge exists in any region's Connections.mmd")
            key = desc.lower()
            if key:
                if key in seen_desc and seen_desc[key] != code:
                    diag.warn(path, f"Exits describes both -> {seen_desc[key]} and -> {code} identically ({desc!r}) - state where each is positioned (a wall, corner, or direction) so they read as distinct")
                else:
                    seen_desc.setdefault(key, code)

    for title in LORE_CITE_RE.findall(text):
        citations["Lore"].setdefault(title.strip(), set()).add(f"{region_code}.{num}")
    for title in KEYS_CITE_RE.findall(text):
        citations["Keys"].setdefault(title.strip(), set()).add(f"{region_code}.{num}")
    for title in QUEST_CITE_RE.findall(text):
        citations["Quest"].setdefault(title.strip(), set()).add(f"{region_code}.{num}")
    for title in NAMED_CITE_RE.findall(text):
        citations["NamedCreature"].setdefault(title.strip(), set()).add(f"{region_code}.{num}")
    for title in UNIQUE_CITE_RE.findall(text):
        citations["UniqueTreasure"].setdefault(title.strip(), set()).add(f"{region_code}.{num}")
    for roman in TREASURE_CITE_RE.findall(text):
        if roman not in ROMAN_TABLES:
            diag.error(path, f"Treasure citation uses unrecognized numeral {roman!r} (expected I-V)")


# ---------------------------------------------------------------------------
# Blocks - a DANGEROUS region's generation batches (STEPS.md 4b/4c)
# ---------------------------------------------------------------------------


def check_region_edge_realization(diag: Diagnostics, top_path, top_edges: list,
                                  all_loc_edges: list, all_locations: dict):
    """Both directions of the claim templates/region/Connections.mmd makes at 3b."""
    crossings = set()
    for a, _typ, _l, b in all_loc_edges:
        ra = all_locations.get(a, {}).get("region")
        rb = all_locations.get(b, {}).get("region")
        if ra and rb and ra != rb:
            crossings.add(frozenset((ra, rb)))
    licensed = {frozenset((a, b)) for a, _typ, _l, b in top_edges if a != b}
    for pair in sorted(crossings - licensed, key=sorted):
        x, y = sorted(pair)
        diag.error(top_path, f"locations connect {x} to {y}, but no region-level edge licenses it")
    for pair in sorted(licensed - crossings, key=sorted):
        x, y = sorted(pair)
        diag.warn(top_path, f"region edge {x} - {y} is not yet realized by any "
                            f"location-to-location connection")


# ---------------------------------------------------------------------------
# Lore / Keys / NamedCreatures / UniqueTreasures registries
# ---------------------------------------------------------------------------

REGISTRY_KINDS = [
    ("Lore", SETTING / "Lore.md", "lore"),
    ("Keys", SETTING / "Keys.md", "keys"),
    ("Quest", SETTING / "Quests.md", "quests"),
    ("NamedCreature", SETTING / "NamedCreatures.md", "named_creatures"),
    ("UniqueTreasure", SETTING / "UniqueTreasures.md", "unique_treasures"),
]

# A Quest is two-ended by definition: a giver location and a target location.
# Anything less is a delivery with one end missing.
TWO_ENDED_KINDS = {"Quest"}


def parse_registry(diag: Diagnostics, kind: str, path: Path, sc_kind: str, all_locations: dict):
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return {}
    entries: dict[str, set] = {}
    places = sc.REGISTRY_PLACES[sc_kind]
    for title, fields, lineno in sc.registry_entries(sc_kind):
        codes = set()
        for k, v in fields:
            if k in places:
                codes |= set(sc.LOC_CODE_TOKEN_RE.findall(v))
        for c in sorted(codes):
            if c not in all_locations:
                diag.error(path, f"line {lineno}: references unknown location code {c}")
        if kind in TWO_ENDED_KINDS and len(codes) == 1:
            diag.warn(path, f"line {lineno}: {title!r} names only one location - a Quest is two-ended "
                            f"(a giver and a target), so confirm this is deliberate")
        if title in entries:
            diag.error(path, f"line {lineno}: duplicate title {title!r}")
        entries[title] = codes
    return entries


def check_key_obligations(diag: Diagnostics, path: Path, registry: dict, build_complete: bool):
    """A Keys row names where the key is found and where it opens. Until the build is
    complete an empty Opens cell is a stub like any other; after it, it is a dangling
    thread that will never be honoured."""
    if not build_complete:
        return
    for title, codes in sorted(registry.items()):
        if len(codes) < 2:
            diag.error(path, f"key {title!r} names only where it is found - every location is "
                             f"written, so the lock it owes will never be drawn")


def cross_check_registry(diag: Diagnostics, kind: str, path: Path, registry: dict, cited: dict):
    for title, codes in cited.items():
        if title not in registry:
            diag.error(path, f"a location cites ({kind}: {title}) but there is no stub row for it here")
            continue
        missing = codes - registry[title]
        if missing:
            diag.error(path, f"'{title}' is cited from {sorted(missing)} but its stub row's location(s) don't list them")
    for title in registry:
        if title not in cited:
            diag.warn(path, f"stub '{title}' has no citing Feature found in any location file")


# ---------------------------------------------------------------------------
# Table and record files - the to-do list
#
# Every table-like file is a pipe table or a record file (patterns/SPEC.md's How
# a Spec becomes tables), so one pair of checks covers all of them. A malformed
# row or an unknown reference is an error. A stub - an empty cell, or a record
# missing a field its template writes - is the build's own to-do list, so it is
# a warning naming the step the gap is owed to.
# ---------------------------------------------------------------------------

TEMPLATES_DIR = ROOT / "templates"
# The setting-level files and the step each one's gaps are owed to; the template that
# writes each is named so a record's expected fields can be read from it.
SETTING_TABLE_FILES = {
    "Keys.md": ("setting/Keys.md", "4h"),
    "Quests.md": ("setting/Quests.md", "4h"),
    "Truths.md": ("setting/Truths.md", "5c"),
}
SETTING_RECORD_FILES = {
    "Bestiary.md": ("setting/Bestiary.md", "2e"),
    "Factions.md": ("setting/Factions.md", "2f"),
    "History.md": ("setting/History.md", "5c"),
    "Lore.md": ("setting/Lore.md", "4h"),
    "NamedCreatures.md": ("setting/NamedCreatures.md", "4h"),
    "UniqueTreasures.md": ("setting/UniqueTreasures.md", "4h"),
}


def template_block(rel: str) -> str:
    path = TEMPLATES_DIR / rel
    if not path.exists():
        return ""
    text = path.read_text()
    i = text.find("## Template")
    m = re.search(r"```[^\n]*\n(.*?)```", text[i:], re.S) if i >= 0 else None
    return m.group(1) if m else ""


def template_header(rel: str) -> list[str]:
    for line in template_block(rel).splitlines():
        if line.strip().startswith("|"):
            return sc.split_row(line)
    return []


def template_fields(rel: str) -> list[str]:
    out = []
    for line in template_block(rel).splitlines():
        m = re.match(r"^([A-Z][A-Za-z' ]{0,30}):\s", line.strip())
        if m and m.group(1) not in out:
            out.append(m.group(1))
    return out


def table_stubs(path: Path, tables, step: str) -> list[tuple[str, Path, int, str]]:
    out = []
    for t in tables:
        for row, line in zip(t.rows, t.lines):
            empty = [h for h, c in zip(t.header, row) if not c.strip()]
            empty += t.header[len(row):]
            if not empty:
                continue
            key = row[0] if row else "?"
            where = f"{t.name} " if t.name else ""
            out.append((step, path, line, f"{where}{key}: {', '.join(empty)}"))
    return out


def check_table_shape(diag: Diagnostics, path: Path, tables):
    for t in tables:
        seen: set = set()
        for row, line in zip(t.rows, t.lines):
            if len(row) != len(t.header):
                diag.error(path, f"line {line}: {len(row)} cells under a {len(t.header)}-column "
                                 f"header{f' ({t.name})' if t.name else ''}")
            if "ID" in t.header:
                rid = row[t.header.index("ID")] if len(row) > t.header.index("ID") else ""
                if rid and rid in seen:
                    diag.error(path, f"line {line}: duplicate ID {rid} in {t.name or 'its table'}")
                seen.add(rid)


def collect_stubs() -> list[tuple[str, Path, int, str]]:
    """Every setting-level stub, as (owed step, file, line, what is missing)."""
    stubs = []
    for fname, (tmpl, step) in SETTING_TABLE_FILES.items():
        path = SETTING / fname
        if path.exists():
            stubs += table_stubs(path, sc.read_tables(path), step)
    for fname, (tmpl, step) in SETTING_RECORD_FILES.items():
        path = SETTING / fname
        if not path.exists():
            continue
        fields = template_fields(tmpl)
        for r in sc.read_records(path):
            have = {k for k, v in r.fields if v.strip()}
            missing = [f for f in fields if f not in have]
            if missing:
                stubs.append((step, path, r.line, f"{r.name}: {', '.join(missing)}"))
    return stubs


def check_tables(diag: Diagnostics):
    for fname, (tmpl, _step) in SETTING_TABLE_FILES.items():
        path = SETTING / fname
        if not path.exists():
            continue
        tables = sc.read_tables(path)
        check_table_shape(diag, path, tables)
        want = template_header(tmpl)
        if tables and want and tables[0].header != want:
            diag.error(path, f"columns {tables[0].header} differ from templates/{tmpl}'s {want}")
    for fname, (tmpl, _step) in SETTING_RECORD_FILES.items():
        path = SETTING / fname
        if not path.exists():
            continue
        fields = set(template_fields(tmpl))
        for r in sc.read_records(path):
            for k in r.labels():
                if fields and k not in fields:
                    diag.error(path, f"line {r.line}: {r.name} carries field {k!r}, which "
                                     f"templates/{tmpl} does not write")
    for step, path, line, what in collect_stubs():
        diag.warn(path, f"line {line}: stub owed to step {step} - {what}")


# ---------------------------------------------------------------------------
# Lightweight structural checks: treasure tables, rumours, setting docs
# ---------------------------------------------------------------------------

def check_treasure_tables(diag: Diagnostics):
    for i in range(1, 6):
        path = SETTING / f"Treasure{i}.md"
        if not path.exists():
            diag.warn(path, "missing - not built yet")
            continue
        text = path.read_text()
        rownums = [int(x) for x in re.findall(r"^\|\s*(\d+)\s*\|", text, re.M)]
        if rownums != list(range(1, 21)):
            diag.error(path, f"expected 20 rows numbered 1-20, found {rownums}")


def check_rumours(diag: Diagnostics):
    path = SETTING / "Rumours.md"
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return
    text = path.read_text()
    rownums = [int(x) for x in re.findall(r"^\|\s*(\d+)\s*\|", text, re.M)]
    if rownums != list(range(1, 21)):
        diag.error(path, f"expected 20 rows numbered 1-20, found {rownums}")
    # templates/setting/Rumours.md puts Settled at after the mark, so T/P/F is no longer
    # the last cell - match it as its own cell wherever it sits in the row.
    tpf = [l for l in text.splitlines()
           if re.match(r"^\|\s*\d+\s*\|", l) and re.search(r"\|\s*[TPFU]\s*\|", l)]
    if len(tpf) != len(rownums):
        diag.warn(path, "not every rumour row carries a T/P/F/U mark")


def bestiary_types() -> set[str]:
    """The TYPE draw block in patterns/setting/Bestiary.md's Spec, lower-cased.

    Read from the pattern rather than copied here, so the closed set has one
    owner and a rename there cannot leave a stale copy behind.
    """
    path = PATTERNS / "setting" / "Bestiary.md"
    if not path.exists():
        return set()
    items = spec_blocks(path.read_text()).get("TYPE", [])
    return {ln.split(" - ")[0].strip().lower() for ln in items if ln.strip()}

# A stat line's AD field is "Xd6+N" per patterns/setting/Bestiary.md; its Type and MA
# are fields of their own. The bonus and MA are optional here so a partially written
# file still parses; both are reported as findings rather than as parse failures.
AD_RE = re.compile(r"^(?P<ad>\d+)d6\s*(?P<mod>[+-]\s*\d+)?$")


def parse_statblocks(path: Path):
    """Every creature record in a Bestiary or NamedCreatures file."""
    out = []
    for r in sc.read_records(path):
        ad_raw = r.get("AD").strip()
        m = AD_RE.match(ad_raw)
        ma = r.get("MA").strip()
        mod = m.group("mod") if m else None
        out.append({
            "name": r.name, "type": r.get("Type").strip(), "ad_raw": ad_raw,
            "ad": int(m.group("ad")) if m else None,
            "mod": int(mod.replace(" ", "")) if mod else None,
            "ma": int(ma) if ma.isdigit() else None,
            "special": "Special" in r.labels(),
        })
    return out


def check_statblocks(diag: Diagnostics, path: Path, label: str, expect_special: bool):
    """patterns/setting/Bestiary.md's AD ladder, modifier and MA scaling.

    Content, not format, so almost everything here is a warning: the averages
    exist to be deviated from, and a single entry off its average is the field
    doing its job. What is worth an error is a value outside the declared
    range, and what is worth a warning is a *systematic* absence of deviation -
    a file where nothing carries a modifier has not decided anything.
    """
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return
    blocks = parse_statblocks(path)
    types = bestiary_types()
    for b in blocks:
        if b["ad_raw"] and b["ad"] is None:
            diag.error(path, f"{b['name']}: AD {b['ad_raw']!r} is not written Xd6+N")
    blocks = [b for b in blocks if b["ad"] is not None]
    if not blocks:
        return
    no_mod = no_ma = no_special = 0
    for b in blocks:
        if types and b["type"] and b["type"].lower() not in types:
            diag.error(path, f"{b['name']}: type {b['type']!r} is not in "
                             f"patterns/setting/Bestiary.md's TYPE draw")
        if not 1 <= b["ad"] <= 18:
            diag.error(path, f"{b['name']}: AD {b['ad']} is outside the 1-18 range")
        if b["mod"] is None:
            no_mod += 1
        elif not -2 <= b["mod"] <= 6:
            diag.error(path, f"{b['name']}: modifier {b['mod']:+d} is outside the -2..+6 range")
        if b["ma"] is None:
            no_ma += 1
        elif not 1 <= b["ma"] <= 6:
            diag.error(path, f"{b['name']}: MA {b['ma']} is outside the 1-6 range")
        if expect_special and b["ad"] >= 4 and not b["special"]:
            no_special += 1
    n = len(blocks)
    if no_mod:
        diag.warn(path, f"{no_mod}/{n} entries state no modifier - it is written on every "
                        f"entry, because its distance from the average (AD/3, rounded up) "
                        f"is what it is for")
    if no_ma:
        diag.warn(path, f"{no_ma}/{n} entries state no MA - it is written on every entry, "
                        f"because its distance from the average (AD/4, rounded up) is what "
                        f"it is for")
    # A file that sits exactly on both averages every time has thrown the
    # fields away just as surely as one that omits them.
    rated = [b for b in blocks if b["mod"] is not None]
    if len(rated) >= 4 and all(b["mod"] == -(-b["ad"] // 3) for b in rated):
        diag.warn(path, "every modifier sits exactly on its average - deviation is the "
                        "information the field carries")
    rated = [b for b in blocks if b["ma"] is not None]
    if len(rated) >= 4 and all(b["ma"] == -(-b["ad"] // 4) for b in rated):
        diag.warn(path, "every MA sits exactly on its average - deviation is the "
                        "information the field carries")
    if no_special:
        diag.warn(path, f"{no_special} entries at 4+ AD carry no Special: line - a "
                        f"special ability is expected more often at 4 AD and above, "
                        f"and several at 8 and above; `none` is a decision, silence "
                        f"is not")


# ---------------------------------------------------------------------------
# setting/region/[Code].md - the Region Overview's field set, per rating
#
# The field set is patterns/region/*.md's; the order and the two tables are
# templates/region/Region.md's. A field from another rating's set, or one retired, is
# an error because the site renders only the labels it knows and would drop it.
# ---------------------------------------------------------------------------

REGION_FIELDS = {
    "SAFE": ["Overview", "Approach", "People", "Services", "Law", "Places", "Situation",
             "Secrets", "Compositions", "Tables"],
    "WILD": ["Overview", "Approach", "Terrain", "Inhabitants", "Places", "Situation",
             "Loot", "Secrets", "Compositions", "Tables"],
    "DANGEROUS": ["Overview", "Approach", "Conditions", "Inhabitants", "Alarm", "Places",
                  "Situation", "Loot", "Secrets", "Compositions", "Tables"],
}
REGION_LABEL_RE = re.compile(r'^([A-Z][a-z]+):(?:\s|$)')


def check_region_overview(diag: Diagnostics, code: str, rating: str):
    path = SETTING / "region" / f"{code}.md"
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return
    lines = path.read_text().splitlines()
    labels = [m.group(1) for m in map(REGION_LABEL_RE.match, lines[1:]) if m]
    expected = REGION_FIELDS[rating]
    for label in labels:
        if label not in expected:
            diag.error(path, f"field {label!r} is not in a {rating} overview's set "
                             f"({', '.join(expected)}), per patterns/region/")
    missing = [f for f in expected if f not in labels]
    if missing:
        diag.error(path, f"missing field(s): {', '.join(missing)}")
    present = [l for l in labels if l in expected]
    if present != [f for f in expected if f in present]:
        diag.warn(path, f"fields out of templates/region/Region.md's order: {', '.join(present)}")
    if "Tables" in labels:
        start = next(i for i, l in enumerate(lines) if l.startswith("Tables:"))
        tables, rows = 0, []
        for raw in lines[start + 1:]:
            line = raw.strip()
            if re.match(r'^d\d+\s', line) and not re.match(r'^\d+[.)]', line):
                if tables:
                    rows.append(count)
                tables, count = tables + 1, 0
            elif re.match(r'^\d+[.)]\s', line) and tables:
                count += 1
        if tables:
            rows.append(count)
        if tables != 2:
            diag.error(path, f"Tables holds {tables} table(s) opened by a `d6 ...` line - "
                             f"templates/region/Region.md asks for two")
        for i, n in enumerate(rows, 1):
            if n != 6:
                diag.error(path, f"table {i} has {n} rows - a d6 table has six")


def check_repeated_features(diag: Diagnostics, region_code: str):
    """The same Feature sentence in two rooms of one region.

    A room written with its siblings in view converges on them, and the first
    sign is a sentence copied whole. Judged at STEPS.md step 5c, which also
    reads for the near-repeats a string match cannot see.
    """
    rdir = SETTING / "region" / region_code
    seen: dict[str, list[str]] = {}
    for path in sorted(rdir.glob("[0-9]*.md"), key=lambda p: int(p.stem)):
        for line in path.read_text().splitlines():
            m = FEATURE_RE.match(line.strip())
            if not m or m.group(1).strip() == "Exits":
                continue
            body = " ".join(m.group(2).split())
            if len(body.split()) >= 8:
                seen.setdefault(body, []).append(f"{region_code}.{path.stem}")
    for body, codes in seen.items():
        if len(codes) > 1:
            diag.warn(rdir, f"the same Feature sentence in {len(codes)} rooms "
                            f"({', '.join(codes)}): {body[:70]!r}... - a room written "
                            f"from its siblings; judged at STEPS.md step 5c")


# A Feature citing a treasure table must not also say what comes up on it.
# patterns/dangerous/Treasure.md and wild/Treasure.md both state this outright;
# it is a prose rule, so this is a heuristic and a warning - it flags a stated
# price, a stated count, or a value judgement sitting in the same Feature as
# the citation, and a human decides.
# "a single coping stone" is the container and legal; "a single old coin" is the
# contents and is not. Nothing in the text distinguishes them except the noun,
# so the container vocabulary is excluded by name rather than guessed at.
_CONTAINER_NOUNS = (r"stone|slab|panel|block|course|case|chest|coffer|niche|cavity"
                    r"|alcove|jar|urn|pot|sack|pack|bag|crack|seam|socket|shelf|drawer")
TREASURE_TELL_RE = re.compile(
    r"\b(?:worth (?:little|its|a|nothing|stooping)|nothing more|barely worth"
    r"|a single (?!(?:\w+\s+){0,2}(?:" + _CONTAINER_NOUNS + r")\b)\w+"
    r"|a handful of|a scatter of|odds and ends"
    r"|\d+\s*cn\b)", re.I)


# A hazard states what it forces in one of three expressions, per
# setting/Procedures.md and templates/region/Location.md's Citations section. The
# grammar is fixed, so a malformed one is a format error like any other
# citation. Which Conditions exist is content and varies per setting, so an
# unrecognised Condition name only warns - Procedures.md is where a missing one
# is added, and a partial build may not have that section yet.
#
# There is deliberately no check that a hazard HAS an expression. Nothing in a
# location file marks a Feature as a hazard - secrets, containers and hidden
# exits all carry the same trigger arrow - so the only available test would
# guess from the prose, and a warning that fires on every legitimate secret is
# a warning nobody reads. A hazard written with no stated cost is caught at
# STEPS.md step 5, per templates/checks/Setting_Judgement_Check.md.
DAMAGE_TYPES = ("Piercing", "Crushing", "Poison", "Fire", "Frost", "Blast")
ANY_TEST_CITE_RE = re.compile(r'\(Test of [^)]*\)?')
TEST_CITE_RE = re.compile(r'\(Test of (Constitution|Sanity|Fate),\s*([^()]+)\)')
XD_RE = re.compile(r'^(\d+)d$')
CONDITION_NAME_RE = re.compile(r'^- \*\*([^*]+)\*\* - ', re.M)


def procedures_conditions() -> set[str] | None:
    """Condition names from setting/Procedures.md, or None if unreadable."""
    path = SETTING / "Procedures.md"
    if not path.exists():
        return None
    m = re.search(r'\n## Conditions\n(.*?)(?=\n## |\Z)', path.read_text(), re.S)
    if not m:
        return None
    return {n.strip() for n in CONDITION_NAME_RE.findall(m.group(1))}


def check_forced_damage(diag: Diagnostics, path: Path, text: str, conditions):
    for raw in text.splitlines():
        for loose in ANY_TEST_CITE_RE.finditer(raw):
            cite = loose.group(0)
            m = TEST_CITE_RE.match(cite)
            if not m:
                diag.error(path, f"{cite!r} is not a forced-damage expression - "
                                 f"templates/region/Location.md allows only "
                                 f"(Test of Constitution, Xd, Type), (Test of Sanity, Xd), "
                                 f"(Test of Fate, Condition) and (Test of Fate, Impact)")
                continue
            test, args = m.group(1), [a.strip() for a in m.group(2).split(",")]
            if test == "Constitution":
                if len(args) != 2:
                    diag.error(path, f"{cite!r} - a Test of Constitution takes Xd and a damage Type")
                    continue
                xd, dtype = args
                _check_xd(diag, path, cite, xd)
                if dtype not in DAMAGE_TYPES:
                    diag.error(path, f"{cite!r} - {dtype!r} is not a damage Type; "
                                     f"setting/Procedures.md names {', '.join(DAMAGE_TYPES)}")
            elif test == "Sanity":
                if len(args) != 1:
                    diag.error(path, f"{cite!r} - a Test of Sanity takes Xd and nothing else; "
                                     f"a madness has no Type")
                    continue
                _check_xd(diag, path, cite, args[0])
            else:  # Fate
                if len(args) != 1:
                    diag.error(path, f"{cite!r} - a Test of Fate takes one Condition, or Impact")
                    continue
                arg = args[0]
                if XD_RE.match(arg):
                    diag.error(path, f"{cite!r} - a Test of Fate forces no wound, so it takes "
                                     f"no Xd; use a Condition or Impact")
                elif arg != "Impact" and conditions is not None and arg not in conditions:
                    diag.warn(path, f"{cite!r} - {arg!r} is not a Condition named in "
                                    f"setting/Procedures.md; add it there rather than "
                                    f"describing it in place")


def _check_xd(diag: Diagnostics, path: Path, cite: str, xd: str):
    m = XD_RE.match(xd)
    if not m:
        diag.error(path, f"{cite!r} - {xd!r} is not a count of Tests; write 1d, 2d or 3d")
        return
    if not 1 <= int(m.group(1)) <= 3:
        diag.error(path, f"{cite!r} - {xd!r} is outside 1d-3d; per setting/Procedures.md "
                         f"3d is already lethal to all but the strongest")


def check_treasure_citation_prose(diag: Diagnostics, path: Path, text: str):
    for line in text.splitlines():
        if not TREASURE_CITE_RE.search(line):
            continue
        m = TREASURE_TELL_RE.search(line)
        if m:
            diag.warn(path, f"a Feature citing a treasure table also describes or prices "
                            f"what is found ({m.group(0)!r}) - the roll decides the "
                            f"contents, and naming them contradicts whatever comes up")


def check_registry_floors(diag: Diagnostics, registries: dict, build_complete: bool):
    """A setting with no keys and no named creatures passes every other check.

    Nothing requires either registry to hold anything, so a run that quietly
    never drew one produces an empty file and no finding. Both are the
    mechanisms that make a set of regions a network rather than a list, so an
    empty one at the close of the build is a result worth seeing.
    """
    if not build_complete:
        return
    # Keys of REGISTRY_KINDS, not filenames - "NamedCreature" is singular there.
    for kind, filename in (("Keys", "Keys.md"), ("NamedCreature", "NamedCreatures.md")):
        if not registries.get(kind):
            path = SETTING / filename
            diag.warn(path, f"no {kind} rows at the close of the build - check this is a "
                            f"decision and not a draw that never fired, per "
                            f"patterns/dangerous/Treasure.md's rates")


def check_rumour_settling(diag: Diagnostics, build_complete: bool):
    """templates/setting/Rumours.md's Settled at column, filled at 5c.

    Before the build is complete a pending marker is the correct state, so this
    only reports once every location exists.
    """
    path = SETTING / "Rumours.md"
    if not path.exists():
        return
    text = path.read_text()
    rows = [l for l in text.splitlines()
            if re.match(r"^\|\s*\d+\s*\|", l)]
    if not rows:
        return
    if not re.search(r"\|\s*Settled at\s*\|", text, re.I):
        diag.warn(path, "no 'Settled at' column - every rumour records where it is "
                        "confirmed, denied or corrected, per templates/setting/Rumours.md")
        return
    if not build_complete:
        return
    unsettled = [l for l in rows if re.search(r"pending", l, re.I)
                 or l.rstrip().endswith("||") or re.search(r"\|\s*\|\s*$", l)]
    if unsettled:
        diag.warn(path, f"{len(unsettled)}/{len(rows)} rumours are still unsettled - step "
                        f"5c fills the column against the locations actually built, and a "
                        f"rumour pointing off the map says so rather than being left blank")


def check_top_level_files(diag: Diagnostics):
    for name in ("Setting.md", "History.md", "Truths.md", "Bestiary.md",
                 "Factions.md", "Procedures.md", "Language.md"):
        path = SETTING / name
        if not path.exists():
            diag.warn(path, "missing - not built yet")
        elif not path.read_text().strip():
            diag.warn(path, "file is empty - not filled in yet")


# ---------------------------------------------------------------------------
# Topology report
#
# Not a check. Per CLAUDE.md's validation posture the validator stays strict on
# format and relaxed on content and ratios, and graph shape is a design decision
# rather than a rule - SAFE wants a shallow hub, WILD a forest of trees,
# DANGEROUS a dense graph with loops and at least one divide. Reporting the shape
# gives setting/checks/SettingJudgementCheck.md something factual to judge against.
# ---------------------------------------------------------------------------

def report_topology(regions: dict, region_locs: dict, region_edges: dict) -> list[str]:
    out = []
    for code, info in regions.items():
        locs = region_locs.get(code, {})
        nodes = {f"{code}.{n}" for n in locs}
        if not nodes:
            continue
        adj = {n: set() for n in nodes}
        undirected = set()
        for a, typ, _lbl, b in region_edges.get(code, []):
            if a in nodes and b in nodes:
                adj[a].add(b)
                adj[b].add(a)
                undirected.add(frozenset((a, b)))
        E, V = len(undirected), len(nodes)

        seen, comps = set(), 0
        for n in nodes:
            if n in seen:
                continue
            comps += 1
            stack = [n]
            while stack:
                cur = stack.pop()
                if cur in seen:
                    continue
                seen.add(cur)
                stack.extend(adj[cur] - seen)

        cycles = E - V + comps
        dead_ends = sorted(n for n in nodes if len(adj[n]) == 1)
        isolated = sorted(n for n in nodes if not adj[n])

        shape = "tree" if cycles == 0 else f"{cycles} independent loop(s)"
        if comps > 1:
            shape += f", {comps} disconnected components"
        out.append(
            f"{code} ({info['rating']}, {info.get('die', '?')}): {V} locations, {E} edges, "
            f"{shape}; {len(dead_ends)} dead end(s)"
            + (f"; ISOLATED: {', '.join(isolated)}" if isolated else "")
        )
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# Seeded at STEPS.md 1b/1c, before any setting content exists. Their presence does
# not mean a setting has been generated.
SEED_FILES = {"Procedures.md", "Language.md"}


def is_fresh_start() -> bool:
    """True when setting/ holds no generated content yet - seeds and .gitkeep don't count."""
    if not SETTING.exists():
        return True
    return not any(
        p.is_file() and p.name != ".gitkeep" and p.name not in SEED_FILES
        for p in SETTING.rglob("*")
    )


def report_pending(region_filter: str | None) -> int:
    """Every gap still owed: each region's table warnings, then every setting-level stub."""
    regions = parse_regions(Diagnostics())
    setting = tables.Setting({c: i["rating"] for c, i in regions.items()})
    scope = SETTING / "region" / region_filter if region_filter else SETTING
    owed: dict[str, list[str]] = {}
    for sev, path, msg in setting.check():
        if sev == "warning" and (Path(path) == scope or scope in Path(path).parents):
            owed.setdefault(rel(path), []).append(msg)
    for step, path, line, what in ([] if region_filter else collect_stubs()):
        owed.setdefault(rel(path), []).append(f"line {line}: stub owed to step {step} - {what}")
    for path in sorted(owed):
        print(path)
        for msg in owed[path]:
            print(f"  {msg}")
    if not owed:
        print("Nothing pending.")
    return 0


def report_location(code: str) -> int:
    """Every entry the location holds, then every entry naming it."""
    regions = parse_regions(Diagnostics())
    setting = tables.Setting({c: i["rating"] for c, i in regions.items()})
    if code not in setting.codes:
        print(f"{code} is not a location")
        return 1
    own, named = setting.entries_at(code)
    for where, n in own:
        print(f"{where}: {kdl.dump(n)}")
    if named:
        print("\nNamed by:")
        for where, n in named:
            print(f"{where}: {kdl.dump(n)}")
    return 0


def main() -> int:
    diag = Diagnostics()
    check_pattern_files(diag)
    check_read_set_graph(diag)
    check_repeated_prose(diag)
    for problem in tables.Schema().problems:
        diag.error(tables.SCHEMA, problem)

    if is_fresh_start():
        seeded = sorted(n for n in SEED_FILES if (SETTING / n).exists())
        if seeded:
            print(f"setting/ holds only its seeds ({', '.join(seeded)}) - nothing to validate yet. "
                  f"Ready for STEPS.md step 2a.")
        else:
            print("setting/ has no generated content yet - nothing to validate yet. "
                  "Ready for STEPS.md step 1.")
        for w in diag.warnings:
            print(f"WARNING: {w}")
        for e in diag.errors:
            print(f"ERROR: {e}")
        if diag.errors or diag.warnings:
            print(f"\n{len(diag.errors)} error(s), {len(diag.warnings)} warning(s) (patterns/ only - "
                  f"setting/ itself is a fresh start)")
        return 1 if diag.errors else 0

    regions = parse_regions(diag)
    top_path = SETTING / "region" / "Connections.mmd"
    top_edges = check_top_connections(diag, regions)

    setting = tables.Setting({c: i["rating"] for c, i in regions.items()})
    for sev, path, msg in setting.check():
        (diag.error if sev == "error" else diag.warn)(path, msg)
    region_locs: dict[str, dict] = {}
    all_locations: dict[str, dict] = {}
    for region_code, r in setting.regions.items():
        region_locs[region_code] = {}
        for code, n in r.locations().items():
            m = tables.CODE_RE.fullmatch(code)
            if m and m.group(1) == region_code:
                stub = {"name": n.props.get("name", ""),
                        "weight": str(n.props.get("type", "")).lower() or None}
                region_locs[region_code][int(m.group(2))] = stub
                all_locations[code] = {**stub, "region": region_code}
    region_edges = {rc: [(a, "---", "", b) for a, b in r.edges] for rc, r in setting.regions.items()}
    all_loc_edges = [e for edges in region_edges.values() for e in edges]
    mundane_edges = {(a, b) for a, _t, _l, b in all_loc_edges} | {(b, a) for a, _t, _l, b in all_loc_edges}
    hidden_edges: set[tuple[str, str]] = set()

    check_region_edge_realization(diag, top_path, top_edges, all_loc_edges, all_locations)

    registries: dict[str, dict] = {}
    registry_paths: dict[str, Path] = {}
    for kind, path, marker in REGISTRY_KINDS:
        registries[kind] = parse_registry(diag, kind, path, marker, all_locations)
        registry_paths[kind] = path

    citations: dict[str, dict] = {kind: {} for kind, _, _ in REGISTRY_KINDS}

    conditions = procedures_conditions()
    for region_code, locs in region_locs.items():
        rdir = SETTING / "region" / region_code
        # A location file is numbered; the region's table files sit beside them.
        existing_files = {p.stem for p in rdir.glob("[0-9]*.md")}
        expected_files = {str(num) for num in locs}
        for missing in sorted(expected_files - existing_files, key=lambda x: int(x)):
            diag.warn(rdir, f"missing location file {missing}.md for gazetteer entry {region_code}.{missing} - not written yet")
        for extra in sorted(existing_files - expected_files):
            diag.error(rdir, f"location file {extra}.md has no matching Locations.md entry")
        for num, stub in locs.items():
            fpath = rdir / f"{num}.md"
            if fpath.exists():
                check_location_file(diag, fpath, region_code, num, stub, regions[region_code]["rating"],
                                     all_locations, mundane_edges, hidden_edges, citations,
                                     conditions)

    build_complete = not any(
        not (SETTING / "region" / rc / f"{num}.md").exists()
        for rc, locs in region_locs.items() for num in locs
    )
    check_key_obligations(diag, SETTING / "Keys.md", registries.get("Keys", {}), build_complete)

    for kind, path, _marker in REGISTRY_KINDS:
        cross_check_registry(diag, kind, path, registries[kind], citations[kind])

    check_tables(diag)
    check_treasure_tables(diag)
    check_rumours(diag)
    check_top_level_files(diag)
    check_statblocks(diag, SETTING / "Bestiary.md", "Bestiary", expect_special=True)
    check_statblocks(diag, SETTING / "NamedCreatures.md", "Named Creature", expect_special=True)
    for region_code, info in regions.items():
        check_region_overview(diag, region_code, info["rating"])
        check_repeated_features(diag, region_code)
    check_registry_floors(diag, registries, build_complete)
    check_rumour_settling(diag, build_complete)

    for line in report_topology(regions, region_locs, region_edges):
        print(f"TOPOLOGY: {line}")
    if regions:
        print()

    for w in diag.warnings:
        print(f"WARNING: {w}")
    for e in diag.errors:
        print(f"ERROR: {e}")

    print(f"\n{len(diag.errors)} error(s), {len(diag.warnings)} warning(s)")
    return 1 if diag.errors else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--pending":
        sys.exit(report_pending(sys.argv[2] if len(sys.argv) > 2 else None))
    if len(sys.argv) > 2 and sys.argv[1] == "--location":
        sys.exit(report_location(sys.argv[2]))
    if len(sys.argv) > 1 and sys.argv[1] == "--read-set":
        sys.exit(report_read_set(sys.argv[2] if len(sys.argv) > 2 else None))
    sys.exit(main())
