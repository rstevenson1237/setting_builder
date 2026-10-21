#!/usr/bin/env python3
"""Structural validator for the framework's read-set and setting/ content.

Two independent checks: that every step, template and schema STEPS.md names
resolves (runs unconditionally, regardless of what setting/ holds), and the
generated content against patterns/*_Schema.md and the formats in templates/,
the location graphs in Connections.md files, and the cross-file registry
constraints (Lore/Keys/NamedCreatures/UniqueTreasures).

This is a structural linter, not a genre/content reviewer - it cannot judge
whether a Feature reads as "situations not authored plots" or whether magic
stays rare per GENRE.md. That judgment still belongs to whoever (or
whichever model) drafts and reviews the content by hand.

A file that is simply missing - a region, a location, a setting-level
document not built yet - is a warning, not an error: this validator is meant
to run against a build in progress, not just a finished one. Errors are
reserved for content that exists but is wrong (malformed, inconsistent with
something else that exists, or an unresolved/malformed citation).

Usage: python3 tools/validate_setting.py [--pending [REGION] | --location CODE | --read-set [STEP]
                                         | --brief setting|REGION]
Exits 1 if any error is found, 0 otherwise (warnings never fail the run).
"""
from __future__ import annotations

import json
import math
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
# The read-set: STEPS.md -> templates/ -> patterns/*_Schema.md
#
# A step names its template(s), and a template names the schemas and steps it
# reads; each is recorded once, so every name must resolve. A review step (phase 6)
# reads what it judges rather than what it generates from.
# ---------------------------------------------------------------------------

TEMPLATES = ROOT / "templates"
# A template is cited by its path under templates/, folder included.
TEMPLATE_CITE_RE = re.compile(r'\btemplates/((?:[a-z]+/)?[A-Za-z_]+\.md)\b')
SCHEMA_CITE_RE = re.compile(r'\bpatterns/([A-Za-z_\[\]]+\.md)\b')
TEMPLATE_STEP_CITE_RE = re.compile(r'\b[Ss]tep\s+([1-9][0-9]*[a-z])\b')
STEP_BODY_RE = re.compile(r'^\s*-\s+([1-9][0-9]*[a-z])\.(.*?)(?=\n\s*-\s+[1-9][0-9]*[a-z]\.|\n[1-9]\.|\Z)',
                          re.S | re.M)


def step_bodies() -> dict[str, str]:
    """Every STEPS.md step id mapped to its own text."""
    if not STEPS_MD.exists():
        return {}
    return {m.group(1): m.group(2) for m in STEP_BODY_RE.finditer(STEPS_MD.read_text())}


def is_review(sid: str) -> bool:
    return sid[0] == "6"


def read_set() -> dict[str, tuple[set, set]]:
    """Per step, the templates it names and the schemas those templates name."""
    out = {}
    for sid, body in step_bodies().items():
        names = set(TEMPLATE_CITE_RE.findall(body))
        schemas = {f for n in names if (TEMPLATES / n).exists()
                   for f in SCHEMA_CITE_RE.findall((TEMPLATES / n).read_text())}
        out[sid] = (names, schemas)
    return out


STANDING_CONTEXT = ("GENRE.md", "STYLE.md", "BRIEF.md")
BRIEF_SLICE_RE = re.compile(r'--brief (\S+?)`')
BRIEF_SCOPES = ("setting", "[Region Code]")   # the slices a Context may name


def context_section(text: str) -> str:
    """A template's Context section."""
    m = re.search(r'^## Context\n(.*?)(?=^## )', text, re.S | re.M)
    return m.group(1) if m else ""


def check_read_set(diag: Diagnostics):
    if not STEPS_MD.exists():
        return
    bodies, steps = step_bodies(), read_set()
    for sid, (names, _) in sorted(steps.items()):
        body = bodies.get(sid, "").strip()
        if not names and "python3 tools/" not in body and not body.startswith("Retired"):
            diag.warn(STEPS_MD, f"step {sid} names no template")
        for name in sorted(names):
            if not (TEMPLATES / name).exists():
                diag.error(STEPS_MD, f"step {sid} names templates/{name}, which does not exist")
    for name in sorted({n for ns, _ in steps.values() for n in ns}):
        path = TEMPLATES / name
        if not path.exists():
            continue
        text = path.read_text()
        for sid in sorted(set(TEMPLATE_STEP_CITE_RE.findall(text)) - set(steps)):
            diag.error(path, f"cites step {sid}, which STEPS.md does not define")
        for f in sorted(set(SCHEMA_CITE_RE.findall(text))):
            if "[" not in f and not (PATTERNS / f).exists():
                diag.error(path, f"cites patterns/{f}, which does not exist")
        context = context_section(text)
        for need in STANDING_CONTEXT:
            if f"`{need}`" not in context:
                diag.error(path, f"Context does not name {need}, which every step reads")
        for scope in BRIEF_SLICE_RE.findall(context):
            if scope not in BRIEF_SCOPES:
                diag.error(path, f"Context reads BRIEF.md's slice {scope!r}; a slice is one of {', '.join(BRIEF_SCOPES)}")
        if TEMPLATE_STEP_CITE_RE.search(context) or re.search(r'^- (At|Step) ', context, re.M):
            diag.error(path, "Context is conditional on a step - one Context serves every step that cites the template")


def check_brief_slices(diag: Diagnostics):
    """Each slice --brief prints holds its nodes as BRIEF.md does, `setting` cut to the
    lines a region's slice keeps."""
    nodes = tables.brief_nodes()
    whole = {(n.name, n.args[0] if n.name == "region" and n.args else None): n for n in nodes}
    for scope in ["setting"] + [str(n.args[0]) for n in nodes if n.name == "region" and n.args]:
        for n in kdl.fenced(tables.brief_slice(scope)):
            want = whole.get((n.name, n.args[0] if n.name == "region" and n.args else None))
            kids = want and [c for c in want.children
                             if scope == "setting" or n.name != "setting" or tables.slice_keeps(c, scope)]
            if not want or repr((n.args, n.props, n.children)) != repr((want.args, want.props, kids)):
                diag.error(tables.BRIEF, f"--brief {scope} misreads its {n.name} node")


def report_brief(scope: str) -> int:
    """BRIEF.md as a step of that scope reads it."""
    text = tables.brief_slice(scope)
    if text is None:
        codes = [str(n.args[0]) for n in tables.brief_nodes() if n.name == "region" and n.args]
        print(f"BRIEF.md has no slice {scope!r}: one of setting, {', '.join(codes)}")
        return 1
    print(text, end="")
    return 0


def report_read_set(step_filter: str | None) -> int:
    """The templates and schemas each step reads."""
    steps = read_set()
    if not steps:
        print("STEPS.md defines no steps - nothing to report.")
        return 0
    for sid, (names, schemas) in sorted(steps.items()):
        if step_filter and sid != step_filter:
            continue
        print(f"{sid}{'  (review pass)' if is_review(sid) else ''}")
        print(f"  templates : {', '.join(sorted(names)) or '(none)'}")
        print(f"  schemas   : {', '.join(sorted(schemas)) or '(none)'}")
        print()
    return 0


# ---------------------------------------------------------------------------
# Regions.md
# ---------------------------------------------------------------------------

REGION_RE = re.compile(r'^([A-Z]+) (.+?) - (SAFE|WILD|DANGEROUS), (d\d+)\s*$')


REGION_COLUMNS = ["Code", "Name", "Form", "Gloss", "Rating", "Die", "Joins", "Tag line"]
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
        regions[code] = {"name": d.get("Name", ""), "rating": rating, "die": die,
                         "joins": d.get("Joins", "").split()}
        order.append(code)
    for code, r in regions.items():
        for j in r["joins"]:
            if j == code or j not in regions:
                diag.error(path, f"region {code} joins {j}, which is {'itself' if j == code else 'no region'}")
            elif code not in regions[j]["joins"]:
                diag.error(path, f"region {code} joins {j}, which does not join {code}")
        if not r["joins"]:
            diag.error(path, f"region {code} joins no region")
    expected = [index_to_code(idx) for idx in range(len(order))]
    if order != expected:
        diag.error(path, f"region codes not a plain A-Z progression: found {order}, expected {expected}")
    return regions


# ---------------------------------------------------------------------------
# Per-region Locations.md + Connections.md
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Location files
# ---------------------------------------------------------------------------

LOC_HEADER_RE = re.compile(r'^([A-Z]+)\.(\d+) \*\*(.+?)\*\*(?: \(([^)]+)\))? - \*(.+)\*\s*$')
FEATURE_RE = re.compile(r'^\*\*([^*]+):\*\*\s*(.*)$')
EXIT_PAIR_RE = re.compile(r'->\s*([A-Z]+\.\d+)\s+([^,]+)')
EXIT_DEST_RE = re.compile(r'->\s*[A-Z]+\.\d+\s+[^,]+')

# Each placed setting table's citation label, per templates/region/Location.md.
CITE_LABELS = {"Lore": "Lore", "Keys": "Keys", "Named Creatures": "Named Creature",
               "Unique Treasures": "Unique Treasure", "Magical Tomes": "Magical Tome",
               "Hoards": "Hoard", "Local Procedures": "Local Procedure"}
TREASURE_CITE_RE = re.compile(r'\(Treasure\s+([IVX]+),\s*d\d+\)')
ROMAN_TABLES = {"I", "II", "III", "IV", "V"}


# ---------------------------------------------------------------------------
# A parenthesised group is a citation, not prose.
CITATION_RE = re.compile(r'\s*\([^()]*\)')
# feature_segments() below is used by tools/metrics.py's corpus report.
SEG_SPLIT_RE = re.compile(r'\s*(?:,|->)\s*')
LIST_ITEM_WORDS = 3


def feature_segments(body: str) -> list[str]:
    """Body split on ',' and '->', with a short-item list collapsed to one segment."""
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
# templates/region/Location.md - every bolded noun in a Player Summary appears below it
# as a Feature
#
# The summary is a promise about what the room contains, and an unkept one sends
# the referee improvising the thing the entry was supposed to hand them. Matching a summary's phrasing to a Feature is not:
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
    """A bolded noun in the Player Summary is a Feature below it."""
    joined = re.sub(r"'s\b", "", " ".join(lines).lower())
    for raw in BOLD_RE.findall(summary):
        phrase = raw.strip()
        tokens = _summary_tokens(phrase)
        if not tokens:
            continue
        if any(tok in joined for tok in tokens):
            continue
        diag.warn(path, f"Player Summary promises **{phrase}** but no Feature below it "
                        f"carries that name - the summary is a promise about "
                        f"what the room contains, and the referee improvises an unkept one")


def check_location_file(diag, path, region_code, num, stub, connected, all_locations,
                         mundane_edges, hidden_edges, conditions=None):
    """connected: the location has Connections entries, so its write-up carries Exits."""
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
    if (hweight or "").lower() != (stub["weight"] or ""):
        diag.error(path, f"header type {hweight!r} does not match its Location entry's {stub['weight']!r}")
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

    check_summary_promises(diag, path, summary, feature_lines)

    if not features:
        diag.error(path, "no Feature lines found (expected at least one **Name:** line)")
    if exits_line is not None and not connected:
        diag.error(path, "has an **Exits:** line, but no Connections entry - it is reached "
                         "from the region itself")
    elif exits_line is None and connected:
        diag.error(path, "missing **Exits:** line")
    elif exits_line is not None:
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
                diag.warn(path, f"Exits lists {src} -> {code} as mundane, but its Connection entry carries a Secret - confirm this is the far side of an already-triggered secret, not a template violation")
            elif not in_mundane:
                diag.error(path, f"Exits lists {src} -> {code}, but no Connection entry runs that way")
            key = desc.lower()
            if key:
                if key in seen_desc and seen_desc[key] != code:
                    diag.warn(path, f"Exits describes both -> {seen_desc[key]} and -> {code} identically ({desc!r}) - state where each is positioned (a wall, corner, or direction) so they read as distinct")
                else:
                    seen_desc.setdefault(key, code)

    for roman in TREASURE_CITE_RE.findall(text):
        if roman not in ROMAN_TABLES:
            diag.error(path, f"Treasure citation uses unrecognized numeral {roman!r} (expected I-V)")




def check_region_edge_realization(diag: Diagnostics, regions: dict, all_loc_edges: list, all_locations: dict):
    """Both directions of the claim Regions.md's Joins column makes at 3a."""
    path = SETTING / "region" / "Regions.md"
    crossings = set()
    for a, _typ, _l, b in all_loc_edges:
        ra = all_locations.get(a, {}).get("region")
        rb = all_locations.get(b, {}).get("region")
        if ra and rb and ra != rb:
            crossings.add(frozenset((ra, rb)))
    licensed = {frozenset((a, b)) for a, r in regions.items() for b in r["joins"] if a != b}
    for pair in sorted(crossings - licensed, key=sorted):
        x, y = sorted(pair)
        diag.error(path, f"locations connect {x} to {y}, but neither region Joins the other")
    for pair in sorted(licensed - crossings, key=sorted):
        x, y = sorted(pair)
        diag.warn(path, f"{x} Joins {y}, but no location-to-location connection realizes it")


# ---------------------------------------------------------------------------
# A write-up carries the setting entries its tables place
#
# Whether an entry is placed is the tables' to say, checked against the setting files
# by tables.Setting. A write-up only follows: once fresh, it cites exactly the entries
# placed at its location, so one left out or one the tables do not hold is an error. A
# stale write-up is owed to 5b and reported by --pending instead.
# ---------------------------------------------------------------------------

def check_writeup_citations(diag: Diagnostics, setting, history):
    placed: dict[str, set] = {}
    for (table, title, _), codes in setting.placements().items():
        if table in CITE_LABELS:
            for c in codes:
                placed.setdefault(c, set()).add((CITE_LABELS[table], title))
    labels = "|".join(CITE_LABELS.values())
    for r in setting.regions.values():
        for code in r.locations():
            path = r.dir / f"{code.split('.')[1]}.md"
            if not path.exists() or tables.stale(setting, code, history):
                continue
            cited = {(m.group(1), m.group(2).strip())
                     for m in re.finditer(rf"\(({labels}):\s*([^)]+)\)", path.read_text())}
            for label, title in sorted(placed.get(code, set()) - cited):
                diag.error(path, f"its tables place ({label}: {title}), which the write-up does not cite")
            for label, title in sorted(cited - placed.get(code, set())):
                diag.error(path, f"cites ({label}: {title}), which its tables do not place here")


# ---------------------------------------------------------------------------
# Table and record files - the to-do list
#
# Every setting-level table-like file is a pipe table or a record file, so one pair of checks covers all of them. A malformed
# row or an unknown reference is an error. A stub - an empty cell, or a record
# missing a field its template writes - is the build's own to-do list, so it is
# a warning naming the step the gap is owed to.
# ---------------------------------------------------------------------------

def check_setting_files(diag: Diagnostics, schema, codes: set):
    """Every setting file against its fields in patterns/Setting_Schema.md; a stub is a
    warning."""
    for sev, path, line, msg in tables.check_setting_files(schema, codes):
        (diag.warn if sev == "stub" else diag.error)(path, f"line {line}: {msg}")


# ---------------------------------------------------------------------------
# Lightweight structural checks: treasure tables, rumours, setting docs
# ---------------------------------------------------------------------------

PRICED_RE = re.compile(r"\(([\d,]+) cn, ([\d,]+) wt\)")
TOTAL_RE = re.compile(r"([\d,]+) cn, ([\d,]+) wt")


def check_hoard_totals(diag: Diagnostics, schema):
    """A hoard's Total is the sum of the `(value cn, wt wt)` its Items state."""
    path = SETTING / "Hoards.md"
    for title, line, values in tables.setting_entries(schema, "Hoards") or []:
        items, total = values.get("Items", ""), values.get("Total", "").strip()
        if not items.strip() or not total:
            continue
        priced = [tuple(int(x.replace(",", "")) for x in m) for m in PRICED_RE.findall(items)]
        stated = TOTAL_RE.fullmatch(total)
        if not priced or not stated:
            diag.error(path, f"line {line}: {title}: Items and Total are written '(value cn, wt wt)' "
                             f"and 'value cn, wt wt'")
            continue
        want = tuple(sum(c) for c in zip(*priced))
        have = tuple(int(x.replace(",", "")) for x in stated.groups())
        if want != have:
            diag.error(path, f"line {line}: {title}: Total is {total}, its Items sum to "
                             f"{want[0]:,} cn, {want[1]:,} wt")

def check_treasure_tables(diag: Diagnostics, brief):
    """Each roll table numbered 1 to the rolls BRIEF.md's files node sets."""
    paths = [(SETTING / f"Treasure{i}.md", "Treasure") for i in range(1, 6)] + [(SETTING / "Magic.md", "Magic")]
    for path, lever in paths:
        if not path.exists():
            diag.warn(path, "missing - not built yet")
            continue
        n = brief.lever(lever)
        rolls = n.props.get("rolls") if n else None
        rownums = [int(x) for x in re.findall(r"^\|\s*(\d+)\s*\|", path.read_text(), re.M)]
        if isinstance(rolls, int) and rownums != list(range(1, rolls + 1)):
            diag.error(path, f"expected {rolls} rows numbered 1-{rolls}, per BRIEF.md, found {rownums}")


def check_rumours(diag: Diagnostics):
    path = SETTING / "Rumours.md"
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return
    text = path.read_text()
    rownums = [int(x) for x in re.findall(r"^\|\s*(\d+)\s*\|", text, re.M)]
    if rownums != list(range(1, len(rownums) + 1)):
        diag.error(path, f"rows are not numbered 1-{len(rownums)}: {rownums}")
    # templates/setting/Rumours.md puts Settled at after the mark, so T/P/F is no longer
    # the last cell - match it as its own cell wherever it sits in the row.
    tpf = [l for l in text.splitlines()
           if re.match(r"^\|\s*\d+\s*\|", l) and re.search(r"\|\s*[TPFU]\s*\|", l)]
    if len(tpf) != len(rownums):
        diag.warn(path, "not every rumour row carries a T/P/F/U mark")


# A stat line's AD field is "Xd6+N" per patterns/Setting_Schema.md; its Type and MA
# are fields of their own, and an MA left out is 1. The bonus is optional here so a
# partially written file still parses; its absence is a finding, not a parse failure.
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
            "ma": int(ma) if ma.isdigit() else None if ma else 1,
            "special": "Special" in r.labels(),
        })
    return out


def check_statblocks(diag: Diagnostics, path: Path, label: str, expect_special: bool):
    """The modifier and MA against their averages. patterns/Setting_Schema.md bounds each
    value; this warns only on a *systematic* absence of deviation - a file where nothing
    carries a modifier, or everything sits on its average, has not decided anything."""
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return
    blocks = [b for b in parse_statblocks(path) if b["ad"] is not None]
    if not blocks:
        return
    no_mod = no_special = 0
    for b in blocks:
        no_mod += b["mod"] is None
        if expect_special and not b["special"]:
            no_special += 1
    n = len(blocks)
    if no_mod:
        diag.warn(path, f"{no_mod}/{n} entries state no modifier - it is written on every "
                        f"entry, because its distance from the average (AD/3, rounded up) "
                        f"is what it is for")
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
        diag.warn(path, f"{no_special} entries carry no Special: line - `none` is a "
                        f"decision, silence is not")


# ---------------------------------------------------------------------------
# A region's seed, setting/region/[Code].md, and its brief, setting/region/[Code]/Brief.md
#
# Each field set is its rating's seed or brief in Region_Schema.md, in its order. A field from the other part, another rating's set, or one retired, is an
# error because the site renders only the labels it knows and would drop it.
# ---------------------------------------------------------------------------

REGION_LABEL_RE = re.compile(r'^([A-Z][a-z]+):(?:\s|$)')


def check_region_overview(diag: Diagnostics, code: str, folder):
    """A region's seed and brief against its rating's seed and brief fields."""
    if folder is None or folder.region_path is None:
        return
    seed = SETTING / "region" / f"{code}.md"
    check_region_fields(diag, seed, folder.seed, folder, 1)
    if seed.exists():
        codes = sorted(set(re.findall(rf"\b{code}\.\d+\b", seed.read_text())))
        if codes:
            diag.warn(seed, f"names {', '.join(codes)} - a seed is written before any location "
                            f"exists, and where a thing lies is the tables' and the brief's")
    brief = SETTING / "region" / code / "Brief.md"
    check_region_fields(diag, brief, folder.brief, folder, 0)


def check_inhabitants(diag: Diagnostics, setting):
    """A brief's Inhabitants names every creature, person and faction its region's
    Encounters, People and Garrison hold, and its Services every location selling or
    running something. Matched loosely - a stem, so "wolves" keeps Wolf - and so a warning."""
    for r in setting.regions.values():
        brief = r.dir / "Brief.md"
        if not brief.exists():
            continue
        lines = brief.read_text().splitlines()
        nodes = [n for ns in r.files.values() for n in ns]
        held = {str(c.props[k]): "an Encounter" for n in nodes if n.name == "Encounter"
                for c in n.children for k in ("bestiary", "named", "faction") if k in c.props}
        held |= {str(n.props[k]): n.args[0] for n in nodes for k in ("name", "named", "faction")
                 if n.name in ("Person", "NamedCreature", "Faction", "Garrison") and k in n.props}
        text = sc.parse_field(lines, "Inhabitants").lower()
        for name, where in sorted(held.items()) if text else ():
            if name.lower()[:max(3, len(name) - 1)] not in text:
                diag.warn(brief, f"Inhabitants does not name {name}, which {where} places here")
        layout = sc.parse_field(lines, "Layout")
        for n in nodes if layout else ():
            if n.name == "Location" and n.args and not re.search(rf"\b{re.escape(str(n.args[0]))}\b", layout):
                diag.warn(brief, f"Layout does not name {n.args[0]}")
        text = sc.parse_field(lines, "Services")
        sold = {str(n.args[0]) for n in nodes if n.name in ("Purchase", "Procedure")}
        for code in sorted(sold) if text else ():
            if not re.search(rf"\b{re.escape(code)}\b", text):
                diag.warn(brief, f"Services does not name {code}, which sells or runs something")


def check_sheets(diag: Diagnostics, brief):
    """The sheets BRIEF.md asks for exist as Sheets.md rows and as map files, each `place`
    and `ground` request is met, and Ground.md is what `maps.py ground` would write now."""
    import maps
    if not brief.sheets:
        return
    sheets_md, held = SETTING / "Sheets.md", {}
    if not sheets_md.exists():
        diag.warn(sheets_md, "missing - not built yet, owed to step 3b")
        return
    for d in sc.read_tables(sheets_md)[0].dicts():
        held[d["Sheet"], d["Region"]] = d
    sheets = {n: maps.Sheet(n, node) for n, node in brief.sheets.items()}
    for name, sheet in sheets.items():
        file = SETTING / f"{name}.json"
        missing = [c for c in sheet.codes if (name, c) not in held]
        if missing:
            diag.warn(sheets_md, f"sheet {name} holds no row for {', '.join(missing)} - owed to step 3b")
            continue
        if not file.exists():
            diag.warn(file, "missing - not built yet, owed to step 3b")
            continue
        for c in sheet.codes:
            sheet.at[c] = tuple(float(v) for v in held[name, c]["Way in"].split(","))
        for c in sheet.codes:
            for n in brief.regions[c].children:
                if n.name == "place" and str(n.args[0]) in sheet.codes:
                    q = maps.Request(c, n, sheet.square)
                    if q.miss(sheet.at[c], sheet.at[q.of]) > 0.5:
                        diag.error(tables.BRIEF, f"line {n.line}: region {c} place {q.of} {n.args[1]} {n.args[2]!r} "
                                                 f"is unmet on {name}: {q.said(sheet.at[c], sheet.at[q.of])}")
        done = maps.read_only(file, "map", "check")
        report = json.loads(done.stdout) if done.stdout.strip().startswith("{") else None
        if report is None:
            diag.error(file, f"artgen cannot check it: {(done.stderr or done.stdout).strip()}")
            continue
        for e in report["errors"]:
            diag.error(file, f"{e['path']}: {e['message']}")
        for r in report["requirements"]:
            if not r["met"]:
                node = next((c for c in brief.regions.get(r["id"].split("-")[0], kdl.Node("", 0)).children
                             if c.name == "ground"), None)
                diag.error(tables.BRIEF, f"{'line ' + str(node.line) + ': ' if node else ''}{r['text']}")
    made = maps.ground_texts(brief.path, SETTING)
    if isinstance(made, str):
        diag.warn(sheets_md, made)
        return
    for code, text in made[0].items():
        path = SETTING / "region" / code / "Ground.md"
        if not path.exists():
            diag.warn(path, "missing - not built yet, owed to step 3b")
        elif path.read_text() != text:
            diag.warn(path, "is not what `python3 tools/maps.py ground` writes now - owed to step 4d")


def check_places(diag: Diagnostics, setting, brief):
    """A WILD or SAFE location on a sheet states where it lies, on that sheet and, to a
    warning, inside its region's area."""
    import maps
    for code, row in maps.sheet_rows().items():
        region = setting.regions.get(code)
        if region is None:
            continue
        sheet = brief.sheets.get(row["sheet"])
        if sheet is None:
            continue
        cell = maps.feet(sheet.props["square"])
        cols, rows = maps.Sheet(row["sheet"], sheet).cols, maps.Sheet(row["sheet"], sheet).rows
        for loc, n in region.locations().items():
            o = maps.offset(n)
            path = region.dir / "Locations.md"
            if o is None:
                diag.error(path, f"{loc} states no place: bearing and distance, north and east, or at=\"way in\"")
                continue
            x, y = row["x"] + o[0] / cell, row["y"] - o[1] / cell
            if not (0 <= x < cols and 0 <= y < rows):
                diag.error(path, f"{loc} lies off the {row['sheet']} sheet")
            elif math.dist((x, y), (row["x"], row["y"])) > row["radius"]:
                diag.warn(path, f"{loc} lies outside {code}'s area on the {row['sheet']} sheet")
        for n in region.files.get("Stops", []):
            if maps.offset(n) is None:
                diag.error(region.dir / "Stops.md", f"line {n.line}: {n.args[0]}'s stop {n.props.get('feature')!r} "
                                                    f"states no place: bearing and distance, or north and east")


def check_hazards(diag: Diagnostics, setting, brief):
    """A Hazard's cost follows its Test: Constitution a `wound` the setting rolls, Fate a
    `condition` Procedures.md names, Sanity neither. Its write-up cites that cost."""
    lever = brief.lever("Procedures")
    wounds = str(lever.props.get("wounds", "")).split() if lever else []
    conditions = procedures_conditions()
    count = {"Nuisance": 1, "Damaging": 2, "Lethal": 3}
    for code, region in setting.regions.items():
        for stem, entries in region.files.items():
            path = region.dir / f"{stem}.md"
            for entry in entries:
                for h in (n for n in kdl.walk([entry]) if n.name == "Hazard"):
                    where = f"{h.args[0] if h.args else entry.args[0]}"
                    test, wound, cond = (h.props.get(k) for k in ("test", "wound", "condition"))
                    cite = None
                    if test == "Constitution":
                        if not wound:
                            diag.error(path, f"Hazard {where}: a Test of Constitution costs a wound")
                        elif wound not in wounds:
                            diag.error(path, f"Hazard {where}: wound {wound!r} is not among BRIEF.md's Procedures wounds, {' '.join(wounds)}")
                        elif cond:
                            diag.error(path, f"Hazard {where}: a Test of Constitution costs a wound, not a condition")
                        else:
                            cite = f"(Test of Constitution, {count.get(h.props.get('damage'), 0)}d, {wound})"
                    elif test == "Fate":
                        if not cond:
                            diag.error(path, f"Hazard {where}: a Test of Fate costs a condition")
                        elif wound:
                            diag.error(path, f"Hazard {where}: a Test of Fate costs a condition, not a wound")
                        else:
                            if conditions is not None and cond not in conditions:
                                diag.error(path, f"Hazard {where}: condition {cond!r} is not named in Procedures.md's Conditions")
                            cite = f"(Test of Fate, {cond})"
                    elif test == "Sanity":
                        if wound or cond:
                            diag.error(path, f"Hazard {where}: a Test of Sanity costs neither wound nor condition")
                        diag.warn(path, f"Hazard {where}: a Test of Sanity is called for only by Chaos itself - confirm its source")
                        cite = f"(Test of Sanity, {count.get(h.props.get('damage'), 0)}d)"
                    writeup = region.dir / f"{entry.args[0].split('.')[1]}.md"
                    if cite and writeup.exists() and cite not in writeup.read_text():
                        diag.error(writeup, f"does not cite {cite}, which {where}'s Hazard states")


def check_blocks(diag: Diagnostics, setting):
    """Every location of a region with Blocks.md is in exactly one block with a footprint
    and a route from its entrance, no room overlaps another, and no way within a block
    climbs."""
    import maps
    for code, region in setting.regions.items():
        blocks = maps.blocks_of(region)
        if not blocks:
            continue
        path = region.dir / "Blocks.md"
        owner: dict[str, str] = {}
        for bid, block in blocks.items():
            for c in (m.strip() for m in str(block.props.get("locations", "")).split(",") if m.strip()):
                if c not in region.locations():
                    diag.error(path, f"{bid} names {c}, which Locations.md does not hold")
                elif c in owner:
                    diag.error(path, f"{c} is in blocks {owner[c]} and {bid}")
                owner[c] = bid
            _, problems = maps.block_map(region, block)
            for p in problems:
                diag.error(path, f"{bid}: {p}")
        for c in sorted(set(region.locations()) - set(owner), key=lambda c: int(c.split(".")[1])):
            diag.error(path, f"{c} is in no block")
        for n in region.files.get("Connections", []):
            a, b = str(n.args[0]), str(n.props.get("to"))
            if owner.get(a) and owner.get(a) == owner.get(b) and str(n.props.get("climb", "0")).lstrip("-") not in ("", "0"):
                diag.error(region.dir / "Connections.md", f"{a} to {b} climbs within block {owner[a]}; a way that climbs joins two blocks")


def check_reversals(diag: Diagnostics, setting):
    """The far side of a way reverses its bearing, at the same distance and the opposite climb."""
    import maps
    points = list(setting.schema.setting_enums["Compass"])
    ways = {}
    for region in setting.regions.values():
        for n in region.files.get("Connections", []):
            if n.args and "to" in n.props and "bearing" in n.props and str(n.props["bearing"]) in points:
                ways[str(n.args[0]), str(n.props["to"])] = (region, n)
    for (a, b), (region, n) in sorted(ways.items()):
        if (b, a) not in ways or a > b:
            continue
        m = ways[b, a][1]
        flip = points[(points.index(str(n.props["bearing"])) + 8) % 16]
        far = (str(m.props["bearing"]), maps.feet(str(m.props.get("distance", "0 feet"))))
        if far != (flip, maps.feet(str(n.props.get("distance", "0 feet")))):
            diag.error(region.dir / "Connections.md", f"line {n.line}: {a} to {b} is {n.props['bearing']}, "
                       f"{n.props.get('distance')}; its far side should read {flip}, {n.props.get('distance')}")
        if "climb" in n.props and "climb" in m.props and int(n.props["climb"]) != -int(m.props["climb"]):
            diag.error(region.dir / "Connections.md", f"line {n.line}: {a} to {b} climbs {n.props['climb']}, "
                       f"its far side {m.props['climb']}")


def check_marks(diag: Diagnostics, setting):
    """Every faction's Identity is shown by a Dressing `mark` in some location - the claim
    Factions.md makes upward, kept downward. Only once a region's Dressing is written."""
    path = SETTING / "Factions.md"
    names = tables.titles(path)
    dressed = [r for r in setting.regions.values() if r.files.get("Dressing")]
    if not names or not dressed:
        return
    marked = {x.strip() for r in dressed for n in r.files["Dressing"]
              for x in str(n.props.get("mark", "")).split(",") if x.strip()}
    for name in sorted(names - marked):
        diag.warn(path, f"{name}: its Identity is marked in no Dressing")


def check_region_fields(diag: Diagnostics, path: Path, fields: list, folder, skip: int):
    if not path.exists():
        diag.warn(path, "missing - not built yet")
        return
    lines = path.read_text().splitlines()
    expected = [m.name for m in fields]
    found = [(m.group(1), l[m.end():].strip()) for l in lines[skip:] if (m := REGION_LABEL_RE.match(l))]
    labels = [k for k, _ in found]
    for label in labels:
        if label not in expected:
            diag.error(path, f"field {label!r} is not one of {', '.join(expected)}, "
                             f"per {folder.region_path.name}")
    missing = [f for f in expected if f not in labels]
    if missing:
        diag.error(path, f"missing field(s): {', '.join(missing)}")
    present = [l for l in labels if l in expected]
    if present != [f for f in expected if f in present]:
        diag.warn(path, f"fields out of {folder.region_path.name}'s order: {', '.join(present)}")
    for m in fields:
        if m.n and m.name in labels:
            paras = len(sc.parse_field(lines[skip:], m.name).split("\n"))
            if paras != m.n:
                diag.error(path, f"{m.name} holds {paras} paragraph(s) - "
                                 f"{folder.region_path.name} asks for {m.n}")
        for k, v in found:
            if k == m.name and v and m.type in folder.enums:
                for msg in tables.check_field(None, m, v, set(), folder.enums):
                    diag.error(path, f"{k}: {msg}")
    if "Tables" in labels:
        start = next(i for i, l in enumerate(lines) if l.startswith("Tables:"))
        found_tables, rows = 0, []
        prev = None
        for raw in lines[start + 1:]:
            line = raw.strip()
            if not line:
                continue
            head = sc.is_table_head(line, prev)
            prev = line
            if head:
                if found_tables:
                    rows.append(count)
                found_tables, count = found_tables + 1, 0
            elif re.match(r'^\d+[.)]\s', line) and found_tables:
                count += 1
        if found_tables:
            rows.append(count)
        if found_tables != 1:
            diag.error(path, f"Tables holds {found_tables} table(s) - "
                             f"{folder.region_path.name} asks for one")
        for n in rows:
            if n != 6:
                diag.error(path, f"the table has {n} rows - a d6 table has six")


def check_repeated_features(diag: Diagnostics, region_code: str):
    """The same Feature sentence in two rooms of one region.

    A room written with its siblings in view converges on them, and the first
    sign is a sentence copied whole. Judged at STEPS.md step 6c, which also
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
                            f"from its siblings; judged at STEPS.md step 6c")


# A Feature citing a treasure table must not also say what comes up on it.
# templates/region/Location.md states this outright;
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
# STEPS.md step 6c, per templates/checks/Setting_Judgement_Check.md.
DAMAGE_TYPES = tuple(tables.Schema().setting_enums.get("Wound_Type", {}))
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
                                 f"(Test of Constitution, Xd, Type), (Test of Sanity, Xd) "
                                 f"and (Test of Fate, Condition)")
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
                    diag.error(path, f"{cite!r} - a Test of Fate takes one Condition")
                    continue
                arg = args[0]
                if XD_RE.match(arg):
                    diag.error(path, f"{cite!r} - a Test of Fate forces no wound, so it takes "
                                     f"no Xd; use a Condition")
                elif conditions is not None and arg not in conditions:
                    diag.warn(path, f"{cite!r} - {arg!r} is not a Condition named in "
                                    f"setting/Procedures.md; add it there rather than "
                                    f"describing it in place")


PROCEDURES_SECTIONS = ("Ruleset", "Forced Dangers", "Wounds", "Madness", "Conditions", "Coin and Prices",
                       "Time and Distance", "Weather", "Encounters", "Carousing")
D6_ROW_RE = re.compile(r'^\|\s*([1-6])\s*\|', re.M)


def check_procedures(diag: Diagnostics, brief):
    """setting/Procedures.md against templates/setting/Procedures.md and BRIEF.md's Procedures
    lever: its sections in order, a six-row table for each Wound_Type listed, for Madness where
    asked for, and for Weather and Carousing."""
    path = SETTING / "Procedures.md"
    if not path.exists():
        return
    text = path.read_text()
    sections = dict(re.findall(r'^## (.+?)\n(.*?)(?=^## |\Z)', text, re.S | re.M))
    lever = brief.lever("Procedures")
    wounds = str(lever.props.get("wounds", "")).split() if lever else []
    madness = lever.props.get("madness", 0) if lever else 0
    if not sections:
        return          # a seed not yet written
    order = [s for s in re.findall(r'^## (.+)$', text, re.M)]
    want = [s for s in PROCEDURES_SECTIONS if s != "Madness" or madness]
    if order != want:
        diag.error(path, f"sections are {order}, expected {want}")
    for t in wounds:
        if t not in DAMAGE_TYPES:
            diag.error(tables.BRIEF, f"Procedures wounds names {t!r}, which is no Wound_Type")
    tables_found = dict(re.findall(r'^### (.+?)\n(.*?)(?=^##|\Z)', sections.get("Wounds", ""), re.S | re.M))
    if list(tables_found) != wounds:
        diag.error(path, f"Wounds holds {list(tables_found)}, BRIEF.md's Procedures wounds lists {wounds}")
    d6 = {**{f"Wounds / {k}": v for k, v in tables_found.items()},
          **{k: sections[k] for k in ("Madness", "Encounters", "Weather", "Carousing") if k in sections}}
    for name, body in d6.items():
        rows = [int(x) for x in D6_ROW_RE.findall(body)]
        if rows[:6] != [1, 2, 3, 4, 5, 6]:
            diag.error(path, f"{name} is not a d6 table of rows 1-6: {rows}")


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


def check_rumour_settling(diag: Diagnostics):
    """templates/setting/Rumours.md's Settled at column, filled as each rumour is
    written at 5d."""
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
    unsettled = [l for l in rows if re.search(r"pending", l, re.I)
                 or l.rstrip().endswith("||") or re.search(r"\|\s*\|\s*$", l)]
    if unsettled:
        diag.warn(path, f"{len(unsettled)}/{len(rows)} rumours are unsettled - each is written "
                        f"at 5d from the location settling it, and a rumour pointing off "
                        f"the map says none rather than being left blank")


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
# Not a check. The validator stays strict on format and relaxed on content and
# ratios, and graph shape is a design decision
# rather than a rule - SAFE wants a shallow hub, WILD a forest of trees,
# DANGEROUS a dense graph with loops and at least one divide. Reporting the shape
# gives setting/checks/SettingJudgementCheck.md something factual to judge against.
# ---------------------------------------------------------------------------

def report_topology(regions: dict, region_locs: dict, region_edges: dict, top: set) -> list[str]:
    out = []
    for code, info in regions.items():
        locs = region_locs.get(code, {})
        nodes = {f"{code}.{n}" for n in locs}
        joined = {x for a, _t, _l, b in region_edges.get(code, []) if {a, b} <= nodes for x in (a, b)}
        nodes -= top - joined
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

# Seeded at STEPS.md 1a/1b, before any setting content exists. Their presence does
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
        if (sev == "warning" or "Coined here" in msg) and (Path(path) == scope or scope in Path(path).parents):
            owed.setdefault(rel(path), []).append(msg)
    history = tables.History()
    for r in setting.regions.values():
        for code in r.locations():
            path = r.dir / f"{code.split('.')[1]}.md"
            if not (Path(path) == scope or scope in Path(path).parents):
                continue
            if not path.exists():
                owed.setdefault(rel(r.dir), []).append(f"{code} has no write-up yet")
            elif changed := tables.stale(setting, code, history):
                owed.setdefault(rel(r.dir), []).append(
                    f"{code}'s write-up is stale, owed to step 5b - changed since: {'; '.join(changed)}")
        brief = r.dir / "Brief.md"
        if Path(brief) == scope or scope in Path(brief).parents:
            if changed := tables.stale_brief(r, history):
                owed.setdefault(rel(r.dir), []).append(
                    f"Brief.md is stale, owed to step 5e - changed since: {'; '.join(changed)}")
    stubs = [] if region_filter else tables.check_setting_files(setting.schema, setting.codes)
    for sev, path, line, msg in stubs:
        if sev == "stub":
            owed.setdefault(rel(path), []).append(f"line {line}: {msg}")
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
    check_read_set(diag)
    schema = tables.Schema()
    for path, problem in schema.problems:
        diag.error(path, problem)
    brief = tables.Brief(schema)
    for problem in brief.problems:
        diag.error(tables.BRIEF, problem)
    if not brief.problems:
        check_brief_slices(diag)

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
                stub = {"name": n.props.get("name", ""), "tags": n.props.get("tags", ""),
                        "weight": str(n.props.get("type", "")).lower() or None}
                region_locs[region_code][int(m.group(2))] = stub
                all_locations[code] = {**stub, "region": region_code}
    region_edges = {rc: [(a, "---", "", b) for a, b in r.edges] for rc, r in setting.regions.items()}
    all_loc_edges = [e for edges in region_edges.values() for e in edges]
    sides = [n for r in setting.regions.values() for n in r.files.get("Connections", [])
             if n.args and "to" in n.props]
    hidden_edges = {(n.args[0], n.props["to"]) for n in sides
                    if any(c.name == "Secret" for c in n.children)}
    mundane_edges = {(n.args[0], n.props["to"]) for n in sides} - hidden_edges
    stated = {n.args[0] for n in sides}

    check_region_edge_realization(diag, regions, all_loc_edges, all_locations)

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
                check_location_file(diag, fpath, region_code, num, stub,
                                     f"{region_code}.{num}" in stated,
                                     all_locations, mundane_edges, hidden_edges, conditions)

    check_writeup_citations(diag, setting, tables.History())
    check_setting_files(diag, schema, setting.codes)
    check_hoard_totals(diag, schema)
    check_treasure_tables(diag, brief)
    check_procedures(diag, brief)
    for problem in brief.region_problems(regions):
        diag.error(tables.BRIEF, problem)
    for problem in brief.procedure_problems(setting):
        diag.warn(tables.BRIEF, problem)
    check_rumours(diag)
    check_top_level_files(diag)
    check_statblocks(diag, SETTING / "Bestiary.md", "Bestiary", expect_special=True)
    check_statblocks(diag, SETTING / "NamedCreatures.md", "Named Creature", expect_special=True)
    for region_code, info in regions.items():
        check_region_overview(diag, region_code, setting.regions[region_code].folder)
        check_repeated_features(diag, region_code)
    check_rumour_settling(diag)
    check_inhabitants(diag, setting)
    check_marks(diag, setting)
    check_sheets(diag, brief)
    check_places(diag, setting, brief)
    check_blocks(diag, setting)
    check_hazards(diag, setting, brief)
    check_reversals(diag, setting)

    # A location reached from the region itself is no part of the stated graph.
    top = {c for r in setting.regions.values() for c, n in r.locations().items()
           if r.folder is None or "Connections" not in r.folder.files
           or n.props.get("type") in r.folder.top}
    for line in report_topology(regions, region_locs, region_edges, top):
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
    if len(sys.argv) > 2 and sys.argv[1] == "--brief":
        sys.exit(report_brief(sys.argv[2]))
    if len(sys.argv) > 1 and sys.argv[1] == "--read-set":
        sys.exit(report_read_set(sys.argv[2] if len(sys.argv) > 2 else None))
    sys.exit(main())
