#!/usr/bin/env python3
"""Structural validator for setting/ content.

Checks generated content against the formats in templates/, the location
graphs in Connections.mmd files, and the cross-file registry constraints
described in STEPS.md (Lore/Keys/NamedCreatures/UniqueTreasures).

This is a structural linter, not a genre/content reviewer - it cannot judge
whether a Feature reads as "situations not authored plots" or whether magic
stays rare per GENRE.md. That judgment still belongs to whoever (or
whichever model) drafts and reviews the content by hand.

Usage: python3 tools/validate_setting.py
Exits 1 if any error is found, 0 otherwise (warnings never fail the run).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETTING = ROOT / "setting"

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
# Regions.md / setting/region/Connections.mmd
# ---------------------------------------------------------------------------

REGION_RE = re.compile(r'^([A-Z]+) (.+?) - (SAFE|WILD|DANGEROUS), (d\d+), \*(.+)\*\s*$')


def parse_regions(diag: Diagnostics):
    path = SETTING / "region" / "Regions.md"
    if not path.exists():
        diag.error(path, "missing")
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
            diag.error(path, f"line {i + 1}: expected a region header line (Code Name - RATING, dN, *tags*), got {line!r}")
            i += 1
            continue
        code, name, rating, die, tags = m.groups()
        if code in regions:
            diag.error(path, f"line {i + 1}: duplicate region code {code}")
        regions[code] = {"name": name.strip(), "rating": rating, "die": die, "tags": tags.strip()}
        order.append(code)
        i += 1
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
EDGE_RE = re.compile(r'(\w+)(?:\[[^\]]*\])?\s*(---|-\.-|-->)\s*(\w+)(?:\[[^\]]*\])?')


def parse_mmd_edges(text: str, node_re: re.Pattern):
    id_to_code: dict[str, str] = {}
    for m in node_re.finditer(text):
        id_to_code[m.group(1)] = m.group(2)
    edges = []
    unresolved: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.split("%%")[0]
        for m in EDGE_RE.finditer(line):
            a, typ, b = m.groups()
            ca, cb = id_to_code.get(a), id_to_code.get(b)
            if ca is None:
                unresolved.add(a)
            if cb is None:
                unresolved.add(b)
            if ca and cb:
                edges.append((ca, typ, cb))
    return id_to_code, edges, unresolved


def check_top_connections(diag: Diagnostics, regions: dict):
    path = SETTING / "region" / "Connections.mmd"
    if not path.exists():
        diag.error(path, "missing")
        return
    text = path.read_text()
    id_to_code, _edges, unresolved = parse_mmd_edges(text, TOP_NODE_RE)
    for u in sorted(unresolved):
        diag.error(path, f"edge references node id {u!r} with no bracketed definition")
    codes_in_graph = set(id_to_code.values())
    for code in regions:
        if code not in codes_in_graph:
            diag.error(path, f"region {code} has no node in the region-level Connections graph")
    for code in codes_in_graph:
        if code not in regions:
            diag.error(path, f"node references unknown region code {code}")


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
        diag.error(path, "missing Locations.md")
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
        diag.error(path, "missing Connections.mmd")
        return []
    text = path.read_text()
    id_to_code, edges, unresolved = parse_mmd_edges(text, LOC_NODE_RE)
    for u in sorted(unresolved):
        diag.error(path, f"edge references node id {u!r} with no bracketed definition")
    codes_in_graph = set(id_to_code.values())
    for num in region_locs:
        code = f"{region_code}.{num}"
        if code not in codes_in_graph:
            diag.error(path, f"location {code} has no node in this region's Connections graph")
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
    hcode, hnum_s, hname, hweight, _htags = m.groups()
    if hcode != region_code or int(hnum_s) != num:
        diag.error(path, f"header code {hcode}.{hnum_s} does not match this file's location {region_code}.{num}")
    if not names_match(hname, stub["name"]):
        diag.error(path, f"header name {hname!r} does not match its Locations.md stub name {stub['name']!r}")
    if rating in ("DANGEROUS", "WILD"):
        if hweight != stub["weight"]:
            diag.error(path, f"header weight/classification {hweight!r} does not match Locations.md stub {stub['weight']!r}")
    elif hweight:
        diag.error(path, f"{rating} region location should not carry a weight/classification tag in its header")

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
    for title in NAMED_CITE_RE.findall(text):
        citations["NamedCreature"].setdefault(title.strip(), set()).add(f"{region_code}.{num}")
    for title in UNIQUE_CITE_RE.findall(text):
        citations["UniqueTreasure"].setdefault(title.strip(), set()).add(f"{region_code}.{num}")
    for roman in TREASURE_CITE_RE.findall(text):
        if roman not in ROMAN_TABLES:
            diag.error(path, f"Treasure citation uses unrecognized numeral {roman!r} (expected I-V)")


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
        diag.error(path, "missing")
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
            diag.error(path, "missing")
            continue
        text = path.read_text()
        rownums = [int(x) for x in re.findall(r"^\|\s*(\d+)\s*\|", text, re.M)]
        if rownums != list(range(1, 21)):
            diag.error(path, f"expected 20 rows numbered 1-20, found {rownums}")


def check_rumours(diag: Diagnostics):
    path = SETTING / "Rumours.md"
    if not path.exists():
        diag.error(path, "missing")
        return
    text = path.read_text()
    rownums = [int(x) for x in re.findall(r"^\|\s*(\d+)\s*\|", text, re.M)]
    if rownums != list(range(1, 21)):
        diag.error(path, f"expected 20 rows numbered 1-20, found {rownums}")
    tpf = re.findall(r"\|\s*[TPF]\s*\|\s*$", text, re.M)
    if len(tpf) != len(rownums):
        diag.warn(path, "not every rumour row carries a trailing T/P/F mark")


def check_top_level_files(diag: Diagnostics):
    for name in ("Outline.md", "Setting.md", "History.md", "Truths.md", "Bestiary.md",
                 "Factions.md", "Procedures.md", "Language.md"):
        path = SETTING / name
        if not path.exists():
            diag.error(path, "missing")
        elif not path.read_text().strip():
            diag.error(path, "file is empty")


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
        for a, typ, b in region_edges.get(code, []):
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


def main() -> int:
    if is_fresh_start():
        seeded = sorted(n for n in SEED_FILES if (SETTING / n).exists())
        if seeded:
            print(f"setting/ holds only its seeds ({', '.join(seeded)}) - nothing to validate. "
                  f"Ready for STEPS.md step 2a.")
        else:
            print("setting/ has no generated content yet - nothing to validate. "
                  "Ready for STEPS.md step 1.")
        return 0

    diag = Diagnostics()

    regions = parse_regions(diag)
    check_top_connections(diag, regions)

    region_locs: dict[str, dict] = {}
    for region_code, info in regions.items():
        gaz_path = SETTING / "region" / region_code / "Locations.md"
        region_locs[region_code] = parse_locations_gazetteer(diag, region_code, info["rating"], gaz_path)

    all_locations: dict[str, dict] = {}
    for region_code, locs in region_locs.items():
        for num, l in locs.items():
            all_locations[f"{region_code}.{num}"] = {"name": l["name"], "weight": l["weight"], "region": region_code}

    mundane_edges: set[tuple[str, str]] = set()
    hidden_edges: set[tuple[str, str]] = set()
    region_edges: dict[str, list] = {}
    for region_code, info in regions.items():
        cpath = SETTING / "region" / region_code / "Connections.mmd"
        edges = check_region_connections(diag, region_code, region_locs[region_code], all_locations, cpath)
        region_edges[region_code] = edges
        for a, typ, b in edges:
            if typ == "---":
                mundane_edges.add((a, b))
                mundane_edges.add((b, a))
            elif typ == "-->":
                mundane_edges.add((a, b))
            elif typ == "-.-":
                hidden_edges.add((a, b))
                hidden_edges.add((b, a))

    registries: dict[str, dict] = {}
    registry_paths: dict[str, Path] = {}
    for kind, path, marker in REGISTRY_KINDS:
        registries[kind] = parse_registry(diag, kind, path, marker, all_locations)
        registry_paths[kind] = path

    citations: dict[str, dict] = {kind: {} for kind, _, _ in REGISTRY_KINDS}

    for region_code, locs in region_locs.items():
        rdir = SETTING / "region" / region_code
        existing_files = {p.stem for p in rdir.glob("*.md") if p.name != "Locations.md"}
        expected_files = {str(num) for num in locs}
        for missing in sorted(expected_files - existing_files, key=lambda x: int(x)):
            diag.error(rdir, f"missing location file {missing}.md for gazetteer entry {region_code}.{missing}")
        for extra in sorted(existing_files - expected_files):
            diag.error(rdir, f"location file {extra}.md has no matching Locations.md entry")
        for num, stub in locs.items():
            fpath = rdir / f"{num}.md"
            if fpath.exists():
                check_location_file(diag, fpath, region_code, num, stub, regions[region_code]["rating"],
                                     all_locations, mundane_edges, hidden_edges, citations)

    for kind, path, _marker in REGISTRY_KINDS:
        cross_check_registry(diag, kind, path, registries[kind], citations[kind])

    check_treasure_tables(diag)
    check_rumours(diag)
    check_top_level_files(diag)

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
    sys.exit(main())
