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

Usage: python3 tools/validate_setting.py
Exits 1 if any error is found, 0 otherwise (warnings never fail the run).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETTING = ROOT / "setting"
PATTERNS = ROOT / "patterns"

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
        check_read_at_steps(diag, path, text)


# ---------------------------------------------------------------------------
# patterns/*/*.md - section structure
#
# One skeleton, no declared tiers: Provides / Read at / Spec / Design
# patterns / Constraints. A Spec line either points to another pattern file
# or states a question the generator answers, which makes the library one
# tree - a file with outgoing citations is a classifier and a file without
# them is a leaf, and that is read off the citations rather than asserted
# anywhere. "Design questions" used to be a separate heading for a leaf
# file's own contract; it was the same grammar as a Spec and on the same
# side of the neutral/compiled split, so it was folded back in.
#
# "## Design patterns" stays optional: it is the per-build compiled content
# (STEPS.md step 1b), and most files legitimately have none.
#
# patterns/setting/Genre.md carries extra sections - it is an interactive
# elicitation procedure and those sections are the procedure.
# ---------------------------------------------------------------------------


def check_pattern_sections(diag: Diagnostics, path, text: str):
    has = lambda h: f"\n## {h}\n" in text or text.startswith(f"## {h}\n")
    for required in ("Provides", "Read at", "Spec"):
        if not has(required):
            diag.error(path, f"missing a '## {required}' section - every patterns/*/*.md "
                              f"file carries one")
    if has("Design questions"):
        diag.error(path, "carries a '## Design questions' section, which was folded into "
                          "'## Spec' - a Spec line either cites a file or states a question")



# ---------------------------------------------------------------------------
# patterns/*/*.md - "## Read at" names real STEPS.md steps
#
# STEPS.md is the authority on build order, so a Read at citing a step that
# does not exist there is stale. This check exists because a phase-2 renumber
# once left eight setting/ patterns pointing a step too far down, three of
# them at a "2i" that had stopped existing entirely.
# ---------------------------------------------------------------------------

STEP_ID_RE = re.compile(r'\b([1-9][0-9]*[a-z])\b')
STEPS_MD = ROOT / "STEPS.md"


def known_step_ids():
    if not STEPS_MD.exists():
        return None
    ids = set()
    for line in STEPS_MD.read_text().splitlines():
        m = re.match(r'\s*-\s+([1-9][0-9]*[a-z])\.\s', line)
        if m:
            ids.add(m.group(1))
    return ids or None


_STEP_IDS = None


def check_read_at_steps(diag: Diagnostics, path, text: str):
    global _STEP_IDS
    if _STEP_IDS is None:
        _STEP_IDS = known_step_ids()
    if not _STEP_IDS:
        return
    m = re.search(r'\n## Read at\n(.*?)(?=\n## )', text, re.S)
    if not m:
        return
    cited = set(STEP_ID_RE.findall(m.group(1)))
    if not cited:
        diag.warn(path, "'## Read at' names no STEPS.md step - state which step reads "
                         "this file, so step coverage can be audited")
        return
    for step in sorted(cited - _STEP_IDS):
        diag.error(path, f"'## Read at' cites step {step}, which STEPS.md does not define")


# ---------------------------------------------------------------------------
# patterns/*/*.md - "## Read at" declares a reach mode, and drawn modes are
# actually drawn
#
# Reach mode is how a file is arrived at, declared as the first thing in
# "## Read at". Four modes are drawn by another file's Spec - second pass,
# kind, ingredient, conditional - and "entry" is the fifth: a file a STEPS.md
# step reads directly, which nothing draws. A file claiming a drawn mode and
# cited by no other file's Spec is orphaned from the graph: nothing reaches
# it, so nothing guarantees it is ever read. That is the failure this check
# exists for - four files were orphaned that way before, and the fix held
# only because someone remembered to look.
#
# Edges are read from the Spec's FENCED BLOCKS ONLY. Prose under the block
# cites pattern files freely - setting/Truths.md names three - and counting
# those would make half the leaves in the library look like classifiers.
# ---------------------------------------------------------------------------

DRAWN_MODES = ("second pass", "kind", "ingredient", "conditional")
VALID_MODES = DRAWN_MODES + ("entry",)
MODE_RE = re.compile(r'\*\*Mode:\s*([^.*]+?)\s*\.\*\*')


def declared_modes(text: str):
    m = re.search(r'\n## Read at\n(.*?)(?=\n## )', text, re.S)
    if not m:
        return None
    d = MODE_RE.search(m.group(1).strip())
    if not d or not m.group(1).strip().startswith("**Mode:"):
        return None
    return [s.strip() for s in d.group(1).split(",") if s.strip()]


# A logical Spec line opens with its rate in the left margin and runs until the
# next one does - continuation lines are indented further, and a citation list
# routinely wraps onto them. Grouping physically would split every wrapped draw
# away from the rate that governs it.
SPEC_RATE_RE = re.compile(r'^ {2}(1|\d+%|liner note|working|central)\s')
BRACE_RE = re.compile(r'\{([^}]*)\}')


def spec_draws(text: str, rel: str):
    """Every draw in this file's Spec fenced blocks, with the shape of its line.

    Yields (target, rate, n_alts, n_cited): the file drawn, the rate token
    governing it, how many alternatives the line offers in braces, and how many
    pattern files that one line cites.
    """
    m = re.search(r'\n## Spec\n(.*?)(?=\n## (?:Design patterns|Constraints)\n)', text, re.S)
    if not m:
        return
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
            targets = {f"{folder}/{fname}"
                       for prefixed, folder, fname in PATTERN_CITE_RE.findall(line)
                       if f"{folder}/{fname}" != rel
                       and not (folder == "setting" and not prefixed)}
            if not targets:
                continue
            braces = BRACE_RE.search(line)
            n_alts = len(braces.group(1).split("|")) if braces else 0
            rate = SPEC_RATE_RE.match(chunk[0]).group(1)
            for target in sorted(targets):
                yield target, rate, n_alts, len(targets)


def spec_edges(text: str, rel: str):
    """Pattern files cited from inside this file's Spec fenced blocks."""
    return {t for t, _rate, _alts, _cited in spec_draws(text, rel)}


def check_reach_modes(diag: Diagnostics):
    if not PATTERNS.exists():
        return
    texts = {p.relative_to(PATTERNS).as_posix(): p.read_text()
             for p in sorted(PATTERNS.glob("*/*.md"))}
    drawn_by: dict[str, set] = {}
    drawn_as: dict[str, list] = {}
    for rel, text in texts.items():
        for target, rate, n_alts, n_cited in spec_draws(text, rel):
            drawn_by.setdefault(target, set()).add(rel)
            drawn_as.setdefault(target, []).append((rel, rate, n_alts, n_cited))

    for rel, text in texts.items():
        path = PATTERNS / rel
        modes = declared_modes(text)
        if modes is None:
            diag.error(path, "'## Read at' does not open with a '**Mode: ...**' "
                              f"declaration - one of {', '.join(VALID_MODES)}")
            continue
        for mode in modes:
            if mode not in VALID_MODES:
                diag.error(path, f"declares reach mode '{mode}', which is not one of "
                                  f"{', '.join(VALID_MODES)}")
        if any(m in DRAWN_MODES for m in modes) and rel not in drawn_by:
            diag.error(path, f"declares mode '{', '.join(modes)}' but no other file's "
                              f"Spec draws it - nothing reaches this file, so nothing "
                              f"guarantees it is ever read")
            continue

        shapes = drawn_as.get(rel, [])
        if "second pass" in modes and not any(rate == "1" for _s, rate, _a, _c in shapes):
            where = ", ".join(sorted(f"{s} at {rate}" for s, rate, _a, _c in shapes))
            diag.error(path, "declares mode 'second pass' - every output, "
                             "unconditionally - but is drawn only at a rate: "
                             f"{where}. A second-pass file needs at least one "
                             "mandatory draw, or it is an ingredient")
        if "conditional" in modes:
            uncond = sorted(s for s, rate, _a, _c in shapes if rate == "1")
            if uncond:
                diag.error(path, "declares mode 'conditional' - triggered by content "
                                 f"already generated - but {', '.join(uncond)} draws it "
                                 "at rate 1. A conditional drawn unconditionally is "
                                 "mandatory, which is an ingredient")
        if "kind" in modes and not any(alts > 1 and cited > 1
                                       for _s, _rate, alts, cited in shapes):
            diag.error(path, "declares mode 'kind' - exactly one of N, mutually "
                             "exclusive - but no line draws it as a choice among "
                             "siblings. A kind needs a '{a | b | c}' line citing the "
                             "alternatives; drawn alone it is an ingredient")


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
# STEPS.md step 1b's compile list vs. the tree
#
# Step 1b rewrites the "## Design patterns" section of every pattern file
# that carries one - that section is the per-build compiled content, and a
# Spec is never rewritten. So the compile list and the set of files carrying
# the section are the same set, stated twice, and they drift apart silently:
# the list once named 18 files while saying "every other tier-2 element
# file", leaving fifteen carrying patterns nobody compiled and two
# (Environmental, Residual) carrying none at all. This checks both
# directions. Which files earn patterns is a reach-mode judgement and stays
# a human decision - this only holds STEPS.md and the tree to the same
# answer once that decision is made.
# ---------------------------------------------------------------------------

COMPILE_LIST_RE = re.compile(r'^\s*-\s+1b\..*?\*\*Compile list\*\*(.*)$', re.M)


def check_compile_list(diag: Diagnostics):
    if not STEPS_MD.exists() or not PATTERNS.exists():
        return
    m = COMPILE_LIST_RE.search(STEPS_MD.read_text())
    if not m:
        diag.warn(STEPS_MD, "step 1b names no '**Compile list**' - step 1b's compiled "
                             "files cannot be checked against the tree without one")
        return
    listed = {f"{folder}/{fname}"
              for _, folder, fname in PATTERN_CITE_RE.findall(m.group(1))}
    carrying = {p.relative_to(PATTERNS).as_posix()
                for p in sorted(PATTERNS.glob("*/*.md"))
                if "\n## Design patterns\n" in p.read_text()}
    for rel in sorted(listed - carrying):
        diag.error(STEPS_MD, f"step 1b's compile list names {rel}, which carries no "
                              f"'## Design patterns' section - step 1b would have "
                              f"nothing to compile into it")
    for rel in sorted(carrying - listed):
        diag.error(STEPS_MD, f"patterns/{rel} carries '## Design patterns' but is not on "
                              f"step 1b's compile list - its examples would never be "
                              f"recompiled for a new setting")


# ---------------------------------------------------------------------------
# Regions.md / setting/region/Connections.mmd
# ---------------------------------------------------------------------------

REGION_RE = re.compile(r'^([A-Z]+) (.+?) - (SAFE|WILD|DANGEROUS), (d\d+)\s*$')
REGION_TAGS_LINE_RE = re.compile(r'^Tags: see (setting/region/[A-Z]+/Tags\.md)\s*$')


def parse_regions(diag: Diagnostics):
    path = SETTING / "region" / "Regions.md"
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return {}
    lines = path.read_text().splitlines()
    regions: dict[str, dict] = {}
    order: list[str] = []
    i, n = 0, len(lines)
    while i < n and not lines[i].strip():
        i += 1
    if i < n and lines[i].strip().lower().startswith("regional gazetteer"):
        i += 1
    while i < n:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        m = REGION_RE.match(line)
        if not m:
            diag.error(path, f"line {i + 1}: expected a region header line (Code Name - RATING, dN), got {line!r}")
            i += 1
            continue
        code, name, rating, die = m.groups()
        if code in regions:
            diag.error(path, f"line {i + 1}: duplicate region code {code}")
        regions[code] = {"name": name.strip(), "rating": rating, "die": die}
        order.append(code)
        i += 1
        if REGION_TAGS_LINE_RE.match(lines[i].strip() if i < n else ""):
            tags_path = SETTING / "region" / code / "Tags.md"
            if not tags_path.exists():
                diag.warn(path, f"region {code}: setting/region/{code}/Tags.md referenced but missing - not built yet")
            i += 1
        else:
            diag.error(path, f"region {code}: missing 'Tags: see setting/region/{code}/Tags.md' line")
        if i < n and lines[i].strip():
            i += 1  # the one-sentence overview line; presence is enough
        else:
            diag.error(path, f"region {code}: missing one-sentence overview line")

    expected = [index_to_code(idx) for idx in range(len(order))]
    if order != expected:
        diag.error(path, f"region codes not a plain A-Z progression: found {order}, expected {expected}")
    return regions


TOP_NODE_RE = re.compile(r'(\w+)\["([A-Z]+) - (.*?)"\]')
LOC_NODE_RE = re.compile(r'(\w+)\["([A-Z]+\.\d+) (.*?)"\]')
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

LOC_GAZ_RE = re.compile(r'^([A-Z]+)\.(\d+) (.+?)(?: \((low|medium|high|landmark|hidden|secret)\))? - \*(.+)\*\s*$')

DANGEROUS_WEIGHTS = {"low", "medium", "high"}
WILD_CLASSIFICATIONS = {"landmark", "hidden", "secret"}


def check_weight_tag(diag: Diagnostics, path, lineno_or_none, rating: str, code: str, weight):
    label = f"line {lineno_or_none}: " if lineno_or_none is not None else ""
    if rating == "DANGEROUS":
        if not weight:
            diag.error(path, f"{label}DANGEROUS region location {code} is missing a (low/medium/high) weight")
        elif weight not in DANGEROUS_WEIGHTS:
            diag.error(path, f"{label}DANGEROUS region location {code} has {weight!r}, but DANGEROUS regions use low/medium/high")
    elif rating == "WILD":
        if not weight:
            diag.error(path, f"{label}WILD region location {code} is missing a (landmark/hidden/secret) classification")
        elif weight not in WILD_CLASSIFICATIONS:
            diag.error(path, f"{label}WILD region location {code} has {weight!r}, but WILD regions use landmark/hidden/secret")
    elif weight:
        diag.error(path, f"{label}{rating} region location {code} should not carry a weight/classification tag")


def parse_locations_gazetteer(diag: Diagnostics, region_code: str, rating: str, path: Path):
    if not path.exists():
        diag.warn(path, "missing Locations.md - not built yet")
        return {}
    lines = path.read_text().splitlines()
    locs: dict[int, dict] = {}
    order: list[int] = []
    for lineno, raw in enumerate(lines, 1):
        s = raw.strip()
        if not s or s.lower().startswith("locations of"):
            continue
        m = LOC_GAZ_RE.match(s)
        if not m:
            diag.error(path, f"line {lineno}: does not match Location_Gazetteer.md format: {s!r}")
            continue
        rcode, num_s, name, weight, tags = m.groups()
        num = int(num_s)
        if rcode != region_code:
            diag.error(path, f"line {lineno}: entry code {rcode} does not match region folder {region_code}")
        check_weight_tag(diag, path, lineno, rating, f"{rcode}.{num}", weight)
        if num in locs:
            diag.error(path, f"line {lineno}: duplicate location number {num}")
        locs[num] = {"name": name.strip(), "weight": weight, "tags": tags.strip()}
        order.append(num)
    expected = list(range(1, len(order) + 1))
    if sorted(order) != expected:
        diag.error(path, f"location numbers are not a clean 1..N sequence: found {sorted(order)}, expected {expected}")
    return locs


def check_region_connections(diag: Diagnostics, region_code: str, region_locs: dict, all_locations: dict, path: Path):
    if not path.exists():
        diag.warn(path, "missing Connections.mmd - not built yet")
        return []
    text = path.read_text()
    id_to_code, edges, unresolved = parse_mmd_edges(text, LOC_NODE_RE)
    for u in sorted(unresolved):
        diag.error(path, f"edge references node id {u!r} with no bracketed definition")
    codes_in_graph = set(id_to_code.values())
    for num in region_locs:
        code = f"{region_code}.{num}"
        if code not in codes_in_graph:
            diag.warn(path, f"location {code} has no node in this region's Connections graph yet")
    for code in codes_in_graph:
        if code not in all_locations:
            diag.error(path, f"node references unknown location code {code}")
    return edges


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


def check_location_file(diag, path, region_code, num, stub, rating, all_locations,
                         mundane_edges, hidden_edges, citations):
    text = path.read_text()
    lines = text.splitlines()
    if not lines or not lines[0].strip():
        diag.error(path, "file is empty or missing its header line")
        return

    m = LOC_HEADER_RE.match(lines[0].strip())
    if not m:
        diag.error(path, f"header line does not match Location.md format: {lines[0]!r}")
        return
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
    if len([t for t in htags.split(",") if t.strip()]) != 2:
        diag.warn(path, f"header carries {htags.strip()!r} - expected exactly two tags, one from setting/Tags.md and one from the region's own Tags.md")

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
    idx += 1

    features = []
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
            low = label.strip().lower()
            if low.startswith(ARTICLES):
                diag.error(path, f"Feature label '{label}' starts with a leading article")

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

BLOCK_NODE_RE = re.compile(r'(\w+)\["([^".]+)"\]')
BLOCK_HEADER_RE = re.compile(r'^(Block|Purpose|Region|Rooms|Locations):\s*(.+?)\s*$', re.M)
PURPOSE_FAMILIES = {"keeping", "working", "living", "holding",
                    "meeting", "believing", "dying", "moving"}


def parse_block_files(diag: Diagnostics, region_code: str, rdir: Path, all_locations: dict):
    """Every [Block Name].mmd in a region folder: header, nodes and typed edges."""
    blocks: dict[str, dict] = {}
    if not rdir.is_dir():
        return blocks
    for path in sorted(rdir.glob("*.mmd")):
        if path.name == "Connections.mmd":
            continue
        text = path.read_text()
        head = {k: v for k, v in BLOCK_HEADER_RE.findall(text)}
        name = head.get("Block") or path.stem
        if "Block" not in head:
            diag.error(path, "block diagram has no 'Block:' header line")
        purpose = (head.get("Purpose") or "").strip().lower()
        if purpose and purpose not in PURPOSE_FAMILIES:
            diag.error(path, f"Purpose {head.get('Purpose')!r} is not one of "
                             f"dangerous/Dressing.md's families: {', '.join(sorted(PURPOSE_FAMILIES))}")
        elif not purpose:
            diag.warn(path, "block diagram has no 'Purpose:' header line - a block is a functional quarter")
        id_to_code, edges, unresolved = parse_mmd_edges(text, LOC_NODE_RE)
        for u in sorted(unresolved):
            diag.error(path, f"edge references node id {u!r} with no bracketed definition")
        for code in id_to_code.values():
            if code not in all_locations:
                diag.error(path, f"node references unknown location code {code}")
        for m in TOP_NODE_RE.finditer(text):
            diag.error(path, f"node {m.group(2)!r} is a region, not a location - "
                             f"a location never connects to a region")
        members = set(re.findall(r'[A-Z]+\.\d+', head.get("Locations", "")))
        if not members:
            diag.error(path, "block diagram has no 'Locations:' header line - membership must be "
                             "explicit, because a cross-block edge puts the far location's node in "
                             "this file too and appearance alone cannot say which block owns it")
        for code in sorted(members - set(id_to_code.values())):
            diag.error(path, f"Locations names {code}, which has no node in this diagram")
        for code in sorted(members):
            if code not in all_locations:
                diag.error(path, f"Locations names unknown location code {code}")
        blocks[name] = {"path": path, "purpose": purpose, "members": members,
                        "codes": set(id_to_code.values()), "edges": edges}
    return blocks


def check_block_purposes(diag: Diagnostics, region_code: str, blocks: dict):
    seen: dict[str, str] = {}
    for name, b in blocks.items():
        if not b["purpose"]:
            continue
        if b["purpose"] in seen:
            diag.warn(b["path"], f"purpose family {b['purpose']!r} is already used by block "
                                 f"{seen[b['purpose']]!r} in region {region_code} - per "
                                 f"patterns/region/Dangerous.md no two blocks share a family")
        else:
            seen[b["purpose"]] = name


def check_block_symmetry(diag: Diagnostics, region_code: str, blocks: dict):
    """A cross-block edge is declared in both block files, identically."""
    owner: dict[str, str] = {}
    for name, b in blocks.items():
        for code in b["members"]:
            if code in owner:
                diag.error(b["path"], f"location {code} is claimed by block {owner[code]!r} as well - "
                                      f"a location belongs to exactly one block")
            else:
                owner[code] = name
    declared: dict[tuple, set] = {}
    for name, b in blocks.items():
        for a, typ, label, c in b["edges"]:
            declared.setdefault(edge_key(a, typ, label, c), set()).add(name)
    reported = set()
    for name, b in blocks.items():
        for a, typ, label, c in b["edges"]:
            ba, bc = owner.get(a), owner.get(c)
            if ba is None or bc is None or ba == bc:
                continue
            key = edge_key(a, typ, label, c)
            here = declared.get(key, set())
            for other in (ba, bc):
                if other in blocks and other not in here and (key, other) not in reported:
                    reported.add((key, other))
                    diag.error(blocks[other]["path"],
                               f"cross-block edge {a} {typ}"
                               + (f"|{label}|" if label else "")
                               + f" {c} is declared in block {name!r} but not here - both ends "
                                 f"declare it, identically in existence, type and direction")


def check_block_connectivity(diag: Diagnostics, blocks: dict):
    for name, b in blocks.items():
        nodes = set(b["members"]) or set(b["codes"])
        if len(nodes) < 2:
            continue
        adj = {n: set() for n in nodes}
        for a, _typ, _l, c in b["edges"]:
            if a in nodes and c in nodes:
                adj[a].add(c)
                adj[c].add(a)
        seen, stack = set(), [next(iter(nodes))]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(adj[cur] - seen)
        if seen != nodes:
            diag.warn(b["path"], f"block {name!r} is not internally connected - "
                                 f"{len(nodes - seen)} location(s) reachable only through another block")


def check_low_shape_mix(diag: Diagnostics, region_code: str, region_locs: dict, edges: list, path):
    """patterns/region/Dangerous.md's LOW SHAPE MIX, measured on the assembled graph."""
    lows = {f"{region_code}.{n}" for n, l in region_locs.items() if l.get("weight") == "low"}
    if len(lows) < 5:
        return
    undirected = {frozenset((a, b)) for a, _typ, _l, b in edges if a != b}
    deg: dict[str, int] = {}
    for e in undirected:
        for n in e:
            deg[n] = deg.get(n, 0) + 1

    def cls(n):
        d = deg.get(n, 0)
        return d if d <= 3 else 4

    classes = [cls(n) for n in lows]
    non_through = sum(1 for c in classes if c != 2)
    if non_through / len(lows) < 0.60:
        diag.warn(path, f"region {region_code}: {non_through}/{len(lows)} LOW locations have a degree "
                        f"other than 2 (want 60%+). Degree is coarse - a location on a loop is degree 2 "
                        f"and reads here as a corridor, so check this against the map before acting")
    names = {0: "isolated", 1: "dead end", 2: "through-connection", 3: "branch", 4: "branch (many)"}
    for c in sorted(set(classes)):
        share = classes.count(c) / len(lows)
        if share > 1 / 3:
            diag.warn(path, f"region {region_code}: {names[c]} accounts for {share:.0%} of LOW "
                            f"locations (want no single class over a third)")


def check_region_edge_realization(diag: Diagnostics, top_path, top_edges: list,
                                  all_loc_edges: list, all_locations: dict):
    """Both directions of the claim templates/Connections.mmd makes at 3b."""
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
    ("Lore", SETTING / "Lore.md", "found at"),
    ("Keys", SETTING / "Keys.md", "found at"),
    ("Quest", SETTING / "Quests.md", "given at"),
    ("NamedCreature", SETTING / "NamedCreatures.md", "appears at"),
    ("UniqueTreasure", SETTING / "UniqueTreasures.md", "found at"),
]

# A Quest is two-ended by definition: a giver location and a target location.
# Anything less is a delivery with one end missing.
TWO_ENDED_KINDS = {"Quest"}


def parse_registry(diag: Diagnostics, kind: str, path: Path, marker: str, all_locations: dict):
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return {}
    entries: dict[str, set] = {}
    full_marker = f" - {marker} "
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        s = raw.strip()
        if not s or full_marker not in s:
            continue
        head, rest = s.split(full_marker, 1)
        if kind == "NamedCreature":
            title = head.split(" (")[0].strip()
        else:
            title = re.sub(r"\s*\(.*?\)\s*$", "", head).strip()
        codes = set(re.findall(r"[A-Z]+\.\d+", rest))
        if not codes:
            diag.error(path, f"line {lineno}: no location code found after '{marker}'")
        for c in codes:
            if c not in all_locations:
                diag.error(path, f"line {lineno}: references unknown location code {c}")
        if kind in TWO_ENDED_KINDS and len(codes) < 2:
            diag.warn(path, f"line {lineno}: {title!r} names only one location - a Quest is two-ended "
                            f"(a giver and a target), so confirm this is deliberate")
        if title in entries:
            diag.error(path, f"line {lineno}: duplicate title {title!r}")
        entries[title] = codes
    return entries


def check_key_obligations(diag: Diagnostics, path: Path, registry: dict, build_complete: bool):
    """A Keys row names where the key is found and where it opens. The second is the
    obligation; unconsumed at the close of 4c it is a dangling thread by definition."""
    for title, codes in sorted(registry.items()):
        if len(codes) >= 2:
            continue
        msg = (f"key {title!r} names only where it is found - the location it opens is the "
               f"obligation, and nothing draws a lock without it")
        if build_complete:
            diag.error(path, msg + " (every location is written, so this will never be honoured)")
        else:
            diag.warn(path, msg)


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
    tpf = re.findall(r"\|\s*[TPF]\s*\|\s*$", text, re.M)
    if len(tpf) != len(rownums):
        diag.warn(path, "not every rumour row carries a trailing T/P/F mark")


def check_tags_file(diag: Diagnostics, path: Path):
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return
    text = path.read_text()
    count = len(re.findall(r"^- \*\*.+\*\* - ", text, re.M))
    if count < 15:
        diag.warn(path, f"only {count} tags found - the pool is meant to hold ~25")


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
# gives checks/SettingJudgementCheck.md something factual to judge against.
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
SEED_FILES = {"Procedures.md", "Language.md", "Tags.md"}


def is_fresh_start() -> bool:
    """True when setting/ holds no generated content yet - seeds and .gitkeep don't count."""
    if not SETTING.exists():
        return True
    return not any(
        p.is_file() and p.name != ".gitkeep" and p.name not in SEED_FILES
        for p in SETTING.rglob("*")
    )


def report_pending(region_filter: str | None) -> int:
    """Inbound edges owed to blocks not yet written.

    A block's membership is the file its nodes are declared in, so a block that does not
    exist yet owns no locations and cannot be named. What is answerable - and what is
    actually needed before writing one - is which already-declared edges point at locations
    no block file has claimed.
    """
    diag = Diagnostics()
    regions = parse_regions(diag)
    any_out = False
    for region_code, info in regions.items():
        if region_filter and region_code != region_filter:
            continue
        if info["rating"] != "DANGEROUS":
            continue
        rdir = SETTING / "region" / region_code
        locs = parse_locations_gazetteer(diag, region_code, info["rating"], rdir / "Locations.md")
        all_locations = {f"{region_code}.{n}": {"region": region_code} for n in locs}
        blocks = parse_block_files(Diagnostics(), region_code, rdir, all_locations)
        placed = {c for b in blocks.values() for c in b["members"]}
        inbound: dict[str, list] = {}
        for name, b in blocks.items():
            for a, typ, label, c in b["edges"]:
                for near, far in ((a, c), (c, a)):
                    if near in b["members"] and far not in placed:
                        inbound.setdefault(far, []).append(
                            f"{near} {typ}" + (f"|{label}|" if label else "") + f" {far}  (from block {name!r})")
        unplaced = sorted(f"{region_code}.{n}" for n in locs if f"{region_code}.{n}" not in placed)
        if not inbound and not unplaced:
            continue
        any_out = True
        print(f"{region_code} {info['name']}")
        print(f"  blocks written: {', '.join(sorted(blocks)) or '(none)'}")
        if inbound:
            print("  edges owed to locations no block has claimed:")
            for far in sorted(inbound):
                for line in inbound[far]:
                    print(f"    {line}")
        if unplaced:
            print(f"  locations in no block yet: {', '.join(unplaced)}")
        print()
    if not any_out:
        print("Nothing pending: every location sits in a block and no edge points outside one.")
    return 0


def main() -> int:
    diag = Diagnostics()
    check_pattern_files(diag)
    check_compile_list(diag)
    check_reach_modes(diag)
    check_repeated_prose(diag)

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

    region_locs: dict[str, dict] = {}
    for region_code, info in regions.items():
        check_tags_file(diag, SETTING / "region" / region_code / "Tags.md")
        gaz_path = SETTING / "region" / region_code / "Locations.md"
        region_locs[region_code] = parse_locations_gazetteer(diag, region_code, info["rating"], gaz_path)

    all_locations: dict[str, dict] = {}
    for region_code, locs in region_locs.items():
        for num, l in locs.items():
            all_locations[f"{region_code}.{num}"] = {"name": l["name"], "weight": l["weight"], "region": region_code}

    mundane_edges: set[tuple[str, str]] = set()
    hidden_edges: set[tuple[str, str]] = set()
    region_edges: dict[str, list] = {}
    all_loc_edges: list = []
    for region_code, info in regions.items():
        rdir = SETTING / "region" / region_code
        cpath = rdir / "Connections.mmd"
        if info["rating"] == "DANGEROUS":
            # Connections.mmd is the block-existence tier; the typed location edges
            # live one file per block.
            blocks = parse_block_files(diag, region_code, rdir, all_locations)
            check_block_purposes(diag, region_code, blocks)
            check_block_symmetry(diag, region_code, blocks)
            check_block_connectivity(diag, blocks)
            edges = []
            for b in blocks.values():
                edges.extend(b["edges"])
            if not blocks:
                diag.warn(rdir, "DANGEROUS region has no block diagrams yet")
            placed = {c for b in blocks.values() for c in b["members"]}
            for num in region_locs[region_code]:
                code = f"{region_code}.{num}"
                if code not in placed:
                    diag.warn(rdir, f"location {code} appears in no block diagram yet")
            check_low_shape_mix(diag, region_code, region_locs[region_code], edges, rdir)
        else:
            edges = check_region_connections(diag, region_code, region_locs[region_code],
                                             all_locations, cpath)
        region_edges[region_code] = edges
        all_loc_edges.extend(edges)
        for a, typ, _lbl, b in edges:
            if typ == "---":
                mundane_edges.add((a, b))
                mundane_edges.add((b, a))
            elif typ == "-->":
                mundane_edges.add((a, b))
            elif typ == "-.-":
                hidden_edges.add((a, b))
                hidden_edges.add((b, a))

    check_region_edge_realization(diag, top_path, top_edges, all_loc_edges, all_locations)

    registries: dict[str, dict] = {}
    registry_paths: dict[str, Path] = {}
    for kind, path, marker in REGISTRY_KINDS:
        registries[kind] = parse_registry(diag, kind, path, marker, all_locations)
        registry_paths[kind] = path

    citations: dict[str, dict] = {kind: {} for kind, _, _ in REGISTRY_KINDS}

    NON_LOCATION_FILES = {"Locations.md", "Tags.md"}
    for region_code, locs in region_locs.items():
        rdir = SETTING / "region" / region_code
        existing_files = {p.stem for p in rdir.glob("*.md") if p.name not in NON_LOCATION_FILES}
        expected_files = {str(num) for num in locs}
        for missing in sorted(expected_files - existing_files, key=lambda x: int(x)):
            diag.warn(rdir, f"missing location file {missing}.md for gazetteer entry {region_code}.{missing} - not written yet")
        for extra in sorted(existing_files - expected_files):
            diag.error(rdir, f"location file {extra}.md has no matching Locations.md entry")
        for num, stub in locs.items():
            fpath = rdir / f"{num}.md"
            if fpath.exists():
                check_location_file(diag, fpath, region_code, num, stub, regions[region_code]["rating"],
                                     all_locations, mundane_edges, hidden_edges, citations)

    build_complete = not any(
        not (SETTING / "region" / rc / f"{num}.md").exists()
        for rc, locs in region_locs.items() for num in locs
    )
    check_key_obligations(diag, SETTING / "Keys.md", registries.get("Keys", {}), build_complete)

    for kind, path, _marker in REGISTRY_KINDS:
        cross_check_registry(diag, kind, path, registries[kind], citations[kind])

    check_treasure_tables(diag)
    check_rumours(diag)
    check_top_level_files(diag)
    check_tags_file(diag, SETTING / "Tags.md")

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
    sys.exit(main())
