#!/usr/bin/env python3
"""Corpus metrics: what the framework costs, what it has produced, and how it reads.

Ten readings, printed in one report:

  CORPUS    locations and words in setting/region/*/[0-9]*.md
  FEATURES  words, segments and sentences per Feature line
  CARRY     the prose a location's tables hold against its write-up: how many of the
            table's words the write-up carries, how much longer it is, and the
            location tags it carries
  HEADCOUNT every faction's and creature's count summed over the rooms that hold it
  RECURRENCE the registry entries the rooms hold in none, or in one location
  FRAMES    the Feature openings and endings two or more rooms share
  TELLS     the four prose tells, counted
  MIX       per region, what its tables hold by kind - connections, challenges,
            hazard damage, reward contents - and its stubs, missing and stale
            write-ups
  BUDGET    framework words against setting words
  READ SET  words in context per step 5b write-up

Nothing here judges. A tell is a candidate a reader looks at, the read-set
figure is an arithmetic sum of what templates/region/Location.md's Context section
names, and neither carries a threshold - `tools/validate_setting.py` is where
a rule with a pass and a fail lives. This file exists so a change to the
framework can be shown to have moved something, rather than asserted to have.

The Feature parsing, the read-set graph and the stopword list are imported
from the validator rather than restated, so a change to the Feature grammar
reaches this report without a second edit.

Usage: python3 tools/metrics.py [--tells [PATH] | --carry [CODE]]

  (no argument)  the full report over this repository
  --carry        every location's dropped table words, or one location's or region's
  --tells        every tell hit listed with its file and line, not just counted
  --tells PATH   the same, over a file or directory outside setting/ - which is
                 how a control arm in fixtures/ is read with the instrument the
                 setting is read with
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kdl  # noqa: E402
from validate_setting import (  # noqa: E402
    CITATION_RE,
    FEATURE_RE,
    PATTERNS,
    ROOT,
    _summary_tokens,
    feature_segments,
    read_set,
)

REGION = ROOT / "setting" / "region"
LOCATION_GLOB = "*/[0-9]*.md"
SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')


def words(text: str) -> int:
    """Whitespace tokens, which is what `wc -w` counts."""
    return len(text.split())


def file_words(path: Path) -> int:
    return words(path.read_text())


def tree_words(paths) -> tuple[int, int]:
    paths = list(paths)
    return len(paths), sum(file_words(p) for p in paths)


# ---------------------------------------------------------------------------
# The four tells
#
# Each is a shape with a documented history in this repository, and each is
# stated as the rule it is checking rather than as a bare pattern, because a
# tell whose rule is not written down drifts into a preference.
#
# Precision is uneven and deliberately so. "rather than" is exact. The other
# three over-report: they flag the shape a failure takes, and whether a given
# hit is that failure is a reading. Calibration is the number each returned on
# the corpus before PR #41 rewrote it against the number it returns now - a tell
# that did not move across a rewrite aimed at it is measuring the wrong thing.
# ---------------------------------------------------------------------------

# 1. The trailing-clause tell. PR #41 found "rather than" in 61 of 206 Features
#    and closed the Feature's punctuation to remove the slot it hung in. It is
#    a contrast, not an error - what it measures is how much of the line is
#    spent qualifying rather than naming.
RATHER_RE = re.compile(r'\brather than\b', re.I)

# 2. The absence claim. GENRE.md: a claim about absence across time or space is
#    one no party can check and no referee can adjudicate. Its shape is a
#    negative or exclusive quantifier reaching for a scope - "nobody has moved
#    it in years", "matching nothing else here" - or one of the exclusivity
#    idioms, which carry the reach in themselves. Local negatives ("no rail
#    marks the edge") carry no reach and do not fire.
ABSENCE_NEG_RE = re.compile(
    r'\b(nothing|nobody|no one|no-one|none|never|nowhere|not once|no longer)\b', re.I)
ABSENCE_REACH_RE = re.compile(
    r'\b(anywhere|elsewhere|else|in living memory|in years|for generations|'
    r'for centuries|ever|since|longer than|of its kind)\b', re.I)
ABSENCE_IDIOM_RE = re.compile(
    r'\b(the only|only one|matching nothing|unlike anything)\b', re.I)

# 3. The conclusion tell. GENRE.md's third test: state what is true and visible,
#    never what the players will conclude. These are the connectives a written
#    conclusion arrives on - the room's mechanic read off the page for the
#    reader after it has already been stated.
CONCLUSION_RE = re.compile(
    r'\b(which is (?:why|how|what)|the reason\b|proof\b|recognis|recogniz|'
    r'unmistakab|obviously|clearly|evidently|meaning that|means that|'
    r'explains\b|suggest|implie|implying|'
    r'will (?:find|know|realise|realize|notice|understand|remember)|'
    r'enough to tell|tells anyone|anyone can tell|the clue that|'
    r'so that anyone|is how anyone)', re.I)

# 4. The gloss: a term carrying its own definition. Its shape is the label naming a thing and
#    the line's opening segment naming it again to define it - D.18's
#    "**Corbelled Ceiling:** The ceiling steps inward in courses rather than
#    arching", the word in the label and then nine words glossing it. Detected as
#    a determiner-opened first segment echoing a significant word of its own
#    label, which is the shape and over-reports it: a line that opens by naming
#    the object it is about ("**Sealed Letter:** A letter from the western heir")
#    has the shape without paying twice, and is why this is the loosest of the
#    four.
GLOSS_OPENER_RE = re.compile(r'^(the|a|an|its|this)\b', re.I)


class Tell:
    def __init__(self, key: str, rule: str):
        self.key, self.rule = key, rule
        self.hits: list[tuple[Path, int, str]] = []

    def hit(self, path: Path, lineno: int, quote: str):
        self.hits.append((path, lineno, quote))

    def __len__(self):
        return len(self.hits)


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def count_tells(paths: list[Path]) -> list[Tell]:
    """The four tells over any markdown - a location file, an arm's output, a brief."""
    rather = Tell("rather than", "the trailing clause, per PR #41")
    absence = Tell("absence claim", "absence across time or space")
    conclusion = Tell("conclusion tell", "the players' conclusion written down, per STYLE.md")
    gloss = Tell("gloss", "a term carrying its own definition")

    for path in paths:
        for lineno, raw in enumerate(path.read_text().splitlines(), 1):
            line = raw.strip()
            if not line:
                continue
            prose = CITATION_RE.sub("", line)

            for m in RATHER_RE.finditer(prose):
                rather.hit(path, lineno, prose[max(0, m.start() - 40):m.end() + 40].strip())

            for sentence in SENTENCE_SPLIT_RE.split(prose):
                if ABSENCE_IDIOM_RE.search(sentence) or (
                        ABSENCE_NEG_RE.search(sentence) and ABSENCE_REACH_RE.search(sentence)):
                    absence.hit(path, lineno, sentence.strip())

            for m in CONCLUSION_RE.finditer(prose):
                conclusion.hit(path, lineno, prose[max(0, m.start() - 40):m.end() + 40].strip())

            fm = FEATURE_RE.match(line)
            if fm and fm.group(1).strip() != "Exits":
                label, body = fm.group(1).strip(), fm.group(2).strip()
                segs = feature_segments(body)
                first = re.sub(r"'s\b", "", segs[0].lower()) if segs else ""
                if first and GLOSS_OPENER_RE.match(first):
                    echoed = sorted(t for t in _summary_tokens(label)
                                    if re.search(r'\b' + re.escape(t), first))
                    if echoed:
                        gloss.hit(path, lineno, f"{label} -> {segs[0]}")

    return [rather, absence, conclusion, gloss]


# ---------------------------------------------------------------------------
# Features
#
# Two word counts, because two are in use. The headline counts the Feature body
# with its citation, which is the figure PR #41 reported (22.3 against 42.8) and
# the one a later run has to be comparable with. The prose figure strips the
# citation, leaving the prose alone - a
# citation is machinery, and feature_segments() drops it before counting.
# ---------------------------------------------------------------------------


def location_files(root: Path = REGION) -> list[Path]:
    return sorted(root.glob(LOCATION_GLOB)) if root.exists() else []


def features(paths: list[Path]) -> list[tuple[Path, str, str]]:
    out = []
    for path in paths:
        for line in path.read_text().splitlines():
            m = FEATURE_RE.match(line.strip())
            if m and m.group(1).strip() != "Exits":
                out.append((path, m.group(1).strip(), m.group(2).strip()))
    return out


def mean(xs) -> float:
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def report_corpus(locs: list[Path]) -> None:
    print("CORPUS")
    if not locs:
        print("  no location files under setting/region/ - nothing generated yet\n")
        return
    regions = sorted({p.parent.name for p in locs})
    total = sum(file_words(p) for p in locs)
    print(f"  regions            : {len(regions)} ({', '.join(regions)})")
    print(f"  keyed locations    : {len(locs)}")
    print(f"  words              : {total:,}")
    print(f"  words per location : {total / len(locs):.0f}")
    for r in regions:
        rl = [p for p in locs if p.parent.name == r]
        print(f"    {r}: {len(rl):2d} locations, {sum(file_words(p) for p in rl):6,} words")
    print()


def report_features(locs: list[Path]) -> None:
    print("FEATURES")
    feats = features(locs)
    if not feats:
        print("  no Feature lines\n")
        return
    full = [words(b) for _, _, b in feats]
    prose = [words(CITATION_RE.sub("", b)) for _, _, b in feats]
    segs = [len(feature_segments(b)) for _, _, b in feats]
    sents = [len([s for s in SENTENCE_SPLIT_RE.split(CITATION_RE.sub("", b).strip()) if s])
             for _, _, b in feats]
    longest = max(feats, key=lambda f: words(f[2]))
    print(f"  Features           : {len(feats)}")
    print(f"  words per Feature  : mean {mean(full):.1f}, max {max(full)} "
          f"(body with citation)")
    print(f"  prose words        : mean {mean(prose):.1f}, max {max(prose)} "
          f"(citation stripped)")
    print(f"  segments           : mean {mean(segs):.1f}, max {max(segs)}")
    print(f"  sentences          : mean {mean(sents):.2f}, max {max(sents)}")
    print(f"  longest            : {rel(longest[0])} '{longest[1]}'")
    print()


# -- CARRY ----------------------------------------------------------------------
#
# A write-up connects the details its tables hold into features a referee can run. The
# table's prose is every free-text member of the location's own entries - a Dressing's
# obvious and layout, a Reward's container, a Secret's trigger and tell, a Person's role
# - leaving out what the header, the Exits and the citations carry mechanically. A table
# word is carried when the write-up holds the same word, singular or plural, in any
# tense; the rest are dropped. Synonyms read as dropped: the figure is a prompt to look
# at what a write-up left behind, not a verdict that it should have kept it.

CARRY_SKIP_NODES = {"Location"}
CARRY_SKIP_MEMBERS = {"at", "orientation", "to", "one-of"}
CARRY_STOPWORDS = frozenset("""
the a an of to in on at by for with from that which it its is are was were be and or but as
into onto over under up down out off no not this these those their them they there here has
have had do does did than then so if when where while one two three four five six seven
eight nine ten itself themselves another only some each every any all both
""".split())


def stem(word: str) -> str:
    w = re.sub(r"'s$", "", word)
    for suffix, repl in (("ies", "y"), ("ing", ""), ("ed", ""), ("es", ""), ("s", "")):
        if w.endswith(suffix) and len(w) - len(suffix) >= 3 and not w.endswith("ss"):
            return w[:len(w) - len(suffix)] + repl
    return w


def content_stems(text: str) -> list[str]:
    return [stem(w) for w in re.findall(r"[a-z][a-z'-]+", text.lower())
            if len(w) > 2 and w not in CARRY_STOPWORDS]


def table_prose(setting, code: str) -> str:
    """The free text of the location's own entries, as the schema types it."""
    region = setting.regions[code.split(".")[0]]
    out = []
    own, _ = setting.entries_at(code)
    for _, entry in own:
        for node in kdl.walk([entry]):
            if node.name in CARRY_SKIP_NODES:
                continue
            for m in region.folder.nodes.get(node.name, []):
                if (m.name not in CARRY_SKIP_MEMBERS and node.props.get(m.name) is not None
                        and (m.type in setting.schema.words or m.type == "text")):
                    out.append(str(node.props[m.name]))
    return "\n".join(out)


def carry(setting) -> dict[str, dict]:
    """Per written location: the table's prose words, the write-up's words, and the table's
    content words the write-up carries and drops, each once."""
    out = {}
    for r in setting.regions.values():
        for code in r.locations():
            path = r.dir / f"{code.split('.')[1]}.md"
            if not path.exists():
                continue
            prose = table_prose(setting, code)
            text = path.read_text()
            held = set(content_stems(text)) | {stem(w) for w in re.findall(r"[a-z]+", text.lower())}
            tags = [t.strip() for t in str(r.locations()[code].props.get("tags", "")).split(",") if t.strip()]
            seen, kept, dropped = set(), [], []
            for w in re.findall(r"[a-z][a-z'-]+", prose.lower()):
                st = stem(w)
                if len(w) <= 2 or w in CARRY_STOPWORDS or st in seen:
                    continue
                seen.add(st)
                (kept if st in held else dropped).append(w)
            out[code] = {"table": words(prose), "writeup": file_words(path),
                         "kept": kept, "dropped": dropped,
                         "tags": [(t, any(stem(w) in held for w in re.findall(r"[a-z]+", t.lower())
                                          if len(w) > 2 and w not in CARRY_STOPWORDS)) for t in tags]}
    return out


def load_setting():
    import tables
    from validate_setting import Diagnostics, parse_regions
    regions = parse_regions(Diagnostics())
    return tables.Setting({c: i["rating"] for c, i in regions.items()})


def report_carry(setting) -> None:
    print("CARRY")
    rows = carry(setting)
    if not rows:
        print("  no written locations - nothing to compare\n")
        return
    def line(label, rs):
        t, w = sum(r["table"] for r in rs), sum(r["writeup"] for r in rs)
        k, d = sum(len(r["kept"]) for r in rs), sum(len(r["dropped"]) for r in rs)
        grow = f"{w / t:4.1f}x" if t else "   -"
        share = f"{100 * d // (k + d)}%" if k + d else "-"
        tags = [c for r in rs for _, c in r["tags"]]
        print(f"  {label:12s} table {t:5,} words, write-up {w:6,}, {grow} longer; "
              f"dropped {d} of {k + d} table words ({share}); tags carried {sum(tags)} of {len(tags)}")
    line("all", list(rows.values()))
    for code in setting.regions:
        rs = [r for c, r in rows.items() if c.split(".")[0] == code]
        if rs:
            line(code, rs)
    worst = sorted(rows.items(), key=lambda x: (-len(x[1]["dropped"]), x[0]))[:5]
    print("  most dropped:")
    for code, r in worst:
        print(f"    {code:6s} {len(r['dropped'])} of {len(r['kept']) + len(r['dropped'])}: "
              f"{', '.join(r['dropped'])}")
    lost = [(c, [t for t, ok in r["tags"] if not ok]) for c, r in rows.items()
            if any(not ok for _, ok in r["tags"])]
    if lost:
        print("  tags dropped: " + "; ".join(f"{c} {', '.join(ts)}" for c, ts in lost))
    print()


def list_carry(setting, only: str | None) -> int:
    rows = {c: r for c, r in carry(setting).items()
            if not only or c == only or c.split(".")[0] == only}
    if not rows:
        print(f"{only or 'setting'}: no written locations")
        return 1
    for code, r in rows.items():
        grow = f"{r['writeup'] / r['table']:.1f}x" if r["table"] else "-"
        print(f"{code}  table {r['table']} words, write-up {r['writeup']} ({grow})")
        print(f"  carried: {', '.join(r['kept']) or '-'}")
        print(f"  dropped: {', '.join(r['dropped']) or '-'}")
        print(f"  tags   : {', '.join(t + ('' if ok else ' (dropped)') for t, ok in r['tags']) or '-'}")
    return 0


# -- HEADCOUNT ------------------------------------------------------------------
#
# What a faction's or creature's prose says it numbers is the writer's to compare with
# this: the counts its rooms hold, summed, with the rooms they sit in. A range counts at
# both ends.

def headcount(setting) -> dict[tuple[str, str], dict]:
    import tables
    out = {}
    for r in setting.regions.values():
        for entries in r.files.values():
            for top in entries:
                code = top.args[0] if top.args else None
                for n in kdl.walk([top]):
                    if n.name == "Creature":
                        key, num = ("Bestiary", n.props.get("bestiary")), n.props.get("count")
                    elif n.name in ("Faction", "Garrison"):
                        key, num = ("Factions", n.props.get("faction")), n.props.get("present")
                    else:
                        continue
                    b = tables.bounds(str(num)) if num is not None else None
                    if key[1] is None or b is None:
                        continue
                    h = out.setdefault((key[0], str(key[1])), {"rooms": set(), "lo": 0, "hi": 0})
                    h["rooms"].add(code)
                    h["lo"] += b[0]
                    h["hi"] += b[1]
    return out


def report_headcount(setting) -> None:
    print("HEADCOUNT")
    rows = headcount(setting)
    if not rows:
        print("  no counted creatures or factions yet\n")
        return
    for table in ("Factions", "Bestiary"):
        print(f"  {table}")
        for (_, title), h in sorted(((k, v) for k, v in rows.items() if k[0] == table),
                                    key=lambda x: (-x[1]["hi"], x[0][1])):
            n = str(h["lo"]) if h["lo"] == h["hi"] else f"{h['lo']}-{h['hi']}"
            print(f"    {title:28s} {n:>7s} in {len(h['rooms'])} room(s)")
    print()


# -- RECURRENCE -----------------------------------------------------------------
#
# A registry entry the rooms hold nowhere is a stub the validator already names; one
# held in a single location is the reading here, a candidate to thicken or to cut.

REGISTRIES = ("Bestiary", "Factions", "Named Creatures", "Lore", "Keys", "Unique Treasures",
              "Magical Tomes", "Hoards", "Local Procedures")


def uses(setting) -> dict[tuple[str, str], set[str]]:
    """(table, title) -> the locations whose entries hold it."""
    out: dict[tuple[str, str], set[str]] = {}
    for r in setting.regions.values():
        if r.folder is None:
            continue
        for entries in r.files.values():
            for top in entries:
                code = top.args[0] if top.args else None
                for n in kdl.walk([top]):
                    for m in r.folder.nodes.get(n.name, []):
                        v = n.props.get(m.name)
                        if v is None or m.type not in ("entry", "pull"):
                            continue
                        for item in ([x.strip() for x in str(v).split(",")] if m.is_list else [str(v)]):
                            table, _, title = item.partition(": ") if m.type == "pull" else (m.arg, "", item)
                            out.setdefault((table, title), set()).add(code)
    return out


def report_recurrence(setting) -> None:
    print("RECURRENCE")
    held = uses(setting)
    for table in REGISTRIES:
        titles = setting.titles(table)
        if not titles:
            continue
        counts = {t: len(held.get((table, t), ())) for t in titles}
        thin = sorted((n, t) for t, n in counts.items() if n <= 1)
        body = ", ".join(f"{t} ({', '.join(sorted(held[(table, t)])) if n else 'none'})" for n, t in thin)
        print(f"  {table:18s} {len(titles):3d} entries, {len(thin)} in 0 or 1 location"
              + (f": {body}" if thin else ""))
    print()


# -- FRAMES ---------------------------------------------------------------------
#
# A room written with its siblings in view converges on them. The validator catches a
# sentence copied whole; this lists the first three and last three words that two or more
# rooms' Features share, with numbers as N. Prices and distances share endings honestly,
# so a hit is a prompt to read both rooms.

NUMBER_RE = re.compile(r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
                       r"dozen|twenty|thirty)\b")


def report_frames(locs: list[Path]) -> None:
    print("FRAMES")
    found = False
    for label, pick in (("opens", lambda t: t[:3]), ("ends", lambda t: t[-3:])):
        rooms: dict[str, set[str]] = {}
        for path, _, body in features(locs):
            toks = re.findall(r"[a-z][a-z'-]*|N", NUMBER_RE.sub("N", CITATION_RE.sub("", body).lower()))
            if len(toks) >= 5:
                rooms.setdefault(" ".join(pick(toks)), set()).add(f"{path.parent.name}.{path.stem}")
        for frame, codes in sorted(rooms.items(), key=lambda x: (-len(x[1]), x[0])):
            if len(codes) >= 2:
                found = True
                print(f"  {label:5s} \"{frame}\" in {len(codes)} rooms: {', '.join(sorted(codes))}")
    if not found:
        print("  none")
    print()


def report_tells(locs: list[Path]) -> None:
    print("TELLS")
    feats = features(locs)
    tells = count_tells(locs)
    for t in tells:
        print(f"  {t.key:16s} : {len(t):4d}   {t.rule}")
    if feats:
        carrying = sum(1 for _, _, b in feats if RATHER_RE.search(b))
        print(f"  {'':16s}   'rather than' is in {carrying} of {len(feats)} Features")
    print()


def report_mix() -> None:
    """Per region, what its tables hold, by kind, and what the loop still owes."""
    import tables
    setting = load_setting()
    history = tables.History()
    print("MIX")
    for r in setting.regions.values():
        counts = {"connections": {}, "challenges": {}, "hazard damage": {}, "rewards": {}}
        for stem, entries in r.files.items():
            for n in entries:
                if stem == "Connections":
                    k = counts["connections"]; v = n.props.get("type", n.name)
                elif stem == "Challenges":
                    k = counts["challenges"]; v = n.name
                    if n.name == "Hazard":
                        d = n.props.get("damage", "?")
                        counts["hazard damage"][d] = counts["hazard damage"].get(d, 0) + 1
                elif n.name == "Reward":
                    k = counts["rewards"]; v = str(n.props.get("contents", "?")).split(":")[0]
                else:
                    continue
                k[v] = k.get(v, 0) + 1
        print(f"  {r.code}:")
        for label, d in counts.items():
            t = sum(d.values())
            body = ", ".join(f"{k} {v} ({100 * v // t}%)" for k, v in
                             sorted(d.items(), key=lambda x: -x[1])) if t else "none"
            print(f"     {label:14s} {t:3d} - {body}")
        stubs = sum(1 for sev, path, msg in setting.check()
                    if sev == "warning" and "stub" in msg and r.dir in Path(path).parents)
        codes = list(r.locations())
        missing = sum(1 for c in codes if not (r.dir / f"{c.split('.')[1]}.md").exists())
        stale = sum(1 for c in codes if tables.stale(setting, c, history))
        print(f"     {'owed':14s} stubs {stubs}, write-ups missing {missing}, stale {stale}")
    print()


def report_targets() -> None:
    """Each BRIEF.md target against what each region's tables hold, then each files and
    setting lever against the setting files. A value outside what it allows is
    marked; whether that matters is the 6c check's."""
    import tables
    setting = load_setting()
    print("TARGETS")
    brief = tables.Brief(setting.schema)
    for code, rows in brief.realized(setting).items():
        for t, label, wanted, got, of in rows:
            lo, hi = tables.entries_allowed(wanted, of)
            mark = "" if lo <= got <= hi else "  <- off"
            pct = f" ({100 * got // of}%, {got} of {of})" if of else ""
            print(f"  {code}: {t.path} {label} {wanted} -> {got}{pct}{mark}")
    for label, wanted, got, off in brief.setting_rows():
        print(f"  {label}: {wanted} -> {got}{'  <- off' if off else ''}")
    print()


def report_budget() -> None:
    print("BUDGET")
    authorities = [ROOT / n for n in ("CLAUDE.md", "README.md", "GENRE.md", "STEPS.md")]
    layers = [
        ("authorities", [p for p in authorities if p.exists()]),
        ("templates/", sorted((ROOT / "templates").glob("*/*.md"))),
        ("patterns/", sorted((ROOT / "patterns").glob("*.md"))
                      + sorted((ROOT / "patterns").glob("*/*.md"))),
    ]
    framework = 0
    for name, paths in layers:
        n, w = tree_words(paths)
        framework += w
        print(f"  {name:14s} : {n:4d} files, {w:7,} words")
    setting_md = sorted(p for p in (ROOT / "setting").rglob("*.md")
                         if "checks" not in p.relative_to(ROOT / "setting").parts)
    n_set, w_set = tree_words(setting_md)
    print(f"  {'setting/':14s} : {n_set:4d} files, {w_set:7,} words")
    for name, glob in (("setting/checks/", "*.md"), ("fixtures/", "**/*.md")):
        paths = sorted((ROOT / name.rstrip("/")).glob(glob))
        if paths:
            n, w = tree_words(paths)
            print(f"  {name:14s} : {n:4d} files, {w:7,} words   (neither framework nor setting)")
    tools = sorted((ROOT / "tools").glob("*.py"))
    lines = sum(len(p.read_text().splitlines()) for p in tools)
    print(f"  {'tools/':14s} : {len(tools):4d} files, {lines:7,} lines")
    print(f"  framework      : {framework:,} words")
    print(f"  setting        : {w_set:,} words")
    if w_set:
        print(f"  ratio          : {framework / w_set:.2f} words of framework "
              f"per word of setting")
    print()


# ---------------------------------------------------------------------------
# The read set
#
# What one location costs to write up: the fixed context every 5b write-up
# carries, beside its own entries from --location. The fixed half is
# templates/region/Location.md's own Context section, which is the authority on what a
# drafting session opens - README.md is in it because the session hook injects
# it. The variable half is walked with the graph tools/validate_setting.py
# --read-set walks, from the same entry points.
#
# The region overview is per-region, so it is reported as its own range rather
# than folded into one number that would be right for no region.
# ---------------------------------------------------------------------------

FIXED_CONTEXT = ("CLAUDE.md", "README.md", "GENRE.md", "STYLE.md", "BRIEF.md",
                 "templates/region/Location.md",
                 "setting/Truths.md", "setting/Procedures.md", "setting/Language.md")


def report_read_set(step: str = "5b") -> None:
    print(f"READ SET (step {step})")
    present = [(n, ROOT / n) for n in FIXED_CONTEXT if (ROOT / n).exists()]
    fixed = sum(file_words(p) for _, p in present)
    for n, p in present:
        print(f"  {n:24s} : {file_words(p):6,}")
    overviews = {p.stem: file_words(p) for p in sorted(REGION.glob("[A-Z].md"))} \
        if REGION.exists() else {}
    if overviews:
        lo, hi = min(overviews.values()), max(overviews.values())
        avg = round(mean(overviews.values()))
        print(f"  {'region overview':24s} : {lo:6,}-{hi:,} across "
              f"{len(overviews)} regions, mean {avg:,}")
    else:
        avg = 0
    print(f"  {'fixed context':24s} : {fixed + avg:6,} (with the mean region overview)")
    print()

    names, schemas = read_set().get(step, (set(), set()))
    paths = [ROOT / "templates" / n for n in sorted(names)] + \
            [PATTERNS / f for f in sorted(schemas) if "[" not in f]
    for path in paths:
        if path.exists():
            print(f"  {str(path.relative_to(ROOT)):24s} : {file_words(path):6,}")
    w = sum(file_words(path) for path in paths if path.exists())
    print(f"  {'in context':24s} : {fixed + avg + w:6,}")
    print()


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--tells":
        # With no path this reads the same corpus the report's TELLS section
        # counts - the keyed locations, not the gazetteers and tag pools beside
        # them. A path given explicitly is taken whole, so a region tree read
        # that way is comparable only against another read the same way.
        if len(argv) > 1:
            target = Path(argv[1]).resolve()
            if not target.exists():
                print(f"{target}: no such file or directory")
                return 1
            # setting/checks/ is review output, not content, and quotes the
            # tells it reports.
            paths = [target] if target.is_file() else sorted(
                p for p in target.rglob("*.md")
                if p.is_file() and "checks" not in p.relative_to(target).parts)
        else:
            target, paths = REGION, location_files()
        if not paths:
            print(f"{rel(target)}: no markdown files")
            return 1
        print(f"TELLS over {rel(target)} ({len(paths)} file(s), "
              f"{sum(file_words(p) for p in paths):,} words)\n")
        for t in count_tells(paths):
            print(f"{t.key} - {t.rule}: {len(t)}")
            for path, lineno, quote in t.hits:
                print(f"  {rel(path)}:{lineno}  {quote}")
            print()
        return 0
    if argv and argv[0] == "--carry":
        return list_carry(load_setting(), argv[1] if len(argv) > 1 else None)
    if argv:
        print(__doc__)
        return 1

    locs = location_files()
    report_corpus(locs)
    report_features(locs)
    setting = load_setting()
    report_carry(setting)
    report_headcount(setting)
    report_recurrence(setting)
    report_frames(locs)
    report_tells(locs)
    report_mix()
    report_targets()
    report_budget()
    report_read_set()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        # The tell listing is long and is read through `head` or `less`.
        sys.exit(0)
