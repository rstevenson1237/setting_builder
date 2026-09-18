#!/usr/bin/env python3
"""Corpus metrics: what the framework costs, what it has produced, and how it reads.

Five readings, printed in one report:

  CORPUS    locations and words in setting/region/*/[0-9]*.md
  FEATURES  words and sentences per Feature line, against STYLE.md's budget
  TELLS     the four prose tells, counted
  BUDGET    framework words against setting words
  READ SET  words in context per step 4c entry point

Nothing here judges. A tell is a candidate a reader looks at, the read-set
figure is an arithmetic sum of what templates/Location.md's Context section
names, and neither carries a threshold - `tools/validate_setting.py` is where
a rule with a pass and a fail lives. This file exists so a change to the
framework can be shown to have moved something, rather than asserted to have.

The Feature parsing, the read-set graph and the stopword list are imported
from the validator rather than restated, so a change to the Feature grammar
reaches this report without a second edit.

Usage: python3 tools/metrics.py [--tells [PATH]]

  (no argument)  the full report over this repository
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

from validate_setting import (  # noqa: E402
    CITATION_RE,
    FEATURE_RE,
    PATTERNS,
    ROOT,
    _summary_tokens,
    feature_sentences,
    read_set_graph,
    spec_closure,
)

REGION = ROOT / "setting" / "region"
LOCATION_GLOB = "*/[0-9]*.md"
SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')


def words(text: str) -> int:
    """Whitespace tokens, which is what `wc -w` counts and what Part one of
    INTROSPECTIVE.md was measured with."""
    return len(text.split())


def file_words(path: Path) -> int:
    return words(path.read_text())


def tree_words(paths) -> tuple[int, int]:
    paths = list(paths)
    return len(paths), sum(file_words(p) for p in paths)


# ---------------------------------------------------------------------------
# The four tells
#
# Hard-coded here until style/tells.txt exists, per INTROSPECTIVE.md P0.1.
# Each is a shape with a documented history in this repository, and each is
# stated as the rule it is checking rather than as a bare pattern, because a
# tell whose rule is not written down drifts into a preference.
#
# Precision is uneven and deliberately so. "rather than" is exact. The other
# three over-report: they flag the shape a failure takes, and whether a given
# hit is that failure is a reading. Calibration is the number each returned on
# the corpus before PR #41 rewrote it against the number it returns now, which
# is recorded at the foot of INTROSPECTIVE.md - a tell that did not move across
# a rewrite aimed at it is measuring the wrong thing.
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

# 4. The gloss. templates/Location.md instruction 5: a precise term replaces its
#    definition and never carries one. Its shape is the label naming a thing and
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
    absence = Tell("absence claim", "absence across time or space, per GENRE.md")
    conclusion = Tell("conclusion tell", "the players' conclusion written down, per GENRE.md")
    gloss = Tell("gloss", "a term carrying its own definition, per Location.md")

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
                sents = feature_sentences(body)
                # The gloss sits in the line's opening clause, not anywhere in its
                # first sentence - a comma or a '->' ends the opening.
                opening = re.split(r',|->', sents[0])[0].strip() if sents else ""
                first = re.sub(r"'s\b", "", opening.lower())
                if first and GLOSS_OPENER_RE.match(first):
                    echoed = sorted(t for t in _summary_tokens(label)
                                    if re.search(r'\b' + re.escape(t), first))
                    if echoed:
                        gloss.hit(path, lineno, f"{label} -> {opening}")

    return [rather, absence, conclusion, gloss]


# ---------------------------------------------------------------------------
# Features
#
# Two word counts, because two are in use. The headline counts the Feature body
# with its citation, which is the figure PR #41 reported (22.3 against 42.8) and
# the one a later run has to be comparable with. The prose figure strips the
# citation, which is what the grammar in instruction 5 actually budgets - a
# citation is machinery, and feature_sentences() drops it before counting.
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
    sents = [len(feature_sentences(b)) for _, _, b in feats]
    per_sent = [words(s) for _, _, b in feats for s in feature_sentences(b)]
    longest = max(feats, key=lambda f: words(f[2]))
    print(f"  Features           : {len(feats)}")
    print(f"  words per Feature  : mean {mean(full):.1f}, max {max(full)} "
          f"(body with citation)")
    print(f"  prose words        : mean {mean(prose):.1f}, max {max(prose)} "
          f"(citation stripped)")
    print(f"  sentences          : mean {mean(sents):.2f}, max {max(sents)} "
          f"(STYLE.md budgets 4)")
    print(f"  words per sentence : mean {mean(per_sent):.1f}, max {max(per_sent)} "
          f"(STYLE.md budgets about 15, long past 20)")
    print(f"  longest            : {rel(longest[0])} '{longest[1]}'")
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


def report_budget() -> None:
    print("BUDGET")
    authorities = [ROOT / n for n in ("CLAUDE.md", "README.md", "GENRE.md", "STEPS.md")]
    layers = [
        ("authorities", [p for p in authorities if p.exists()]),
        ("templates/", sorted((ROOT / "templates").glob("*.md"))),
        ("patterns/", sorted((ROOT / "patterns").glob("SPEC.md"))
                      + sorted((ROOT / "patterns").glob("*/*.md"))),
    ]
    framework = 0
    for name, paths in layers:
        n, w = tree_words(paths)
        framework += w
        print(f"  {name:14s} : {n:4d} files, {w:7,} words")
    setting_md = sorted((ROOT / "setting").rglob("*.md"))
    n_set, w_set = tree_words(setting_md)
    print(f"  {'setting/':14s} : {n_set:4d} files, {w_set:7,} words")
    for name, glob in (("checks/", "*.md"), ("fixtures/", "**/*.md")):
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
# What one location costs to generate: the fixed context every 4c entry carries
# plus the closure of pattern files its class file reaches. The fixed half is
# templates/Location.md's own Context section, which is the authority on what a
# drafting session opens - README.md is in it because the session hook injects
# it. The variable half is walked with the graph tools/validate_setting.py
# --read-set walks, from the same entry points.
#
# The region overview is per-region, so it is reported as its own range rather
# than folded into one number that would be right for no region.
# ---------------------------------------------------------------------------

FIXED_CONTEXT = ("CLAUDE.md", "README.md", "GENRE.md", "templates/Location.md",
                 "setting/Truths.md", "setting/Procedures.md", "setting/Language.md")


def report_read_set(step: str = "4c") -> None:
    print(f"READ SET (step {step})")
    g = read_set_graph()
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

    entries: set = set()
    for name in g["step_templates"].get(step, set()):
        entries |= g["template_roots"].get(name, set())
    if not entries:
        print(f"  step {step} names no pattern entry point\n")
        return
    print(f"  {'entry point':24s} {'files':>5s} {'pattern':>8s} {'in context':>11s}")
    for e in sorted(entries):
        closure = spec_closure({e}, g["pattern_files"])
        w = sum(file_words(PATTERNS / f) for f in closure)
        print(f"  {e:24s} {len(closure):5d} {w:8,} {fixed + avg + w:11,}")
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
            paths = [target] if target.is_file() else sorted(
                p for p in target.rglob("*.md") if p.is_file())
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
    if argv:
        print(__doc__)
        return 1

    locs = location_files()
    report_corpus(locs)
    report_features(locs)
    report_tells(locs)
    report_budget()
    report_read_set()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        # The tell listing is long and is read through `head` or `less`.
        sys.exit(0)
