#!/usr/bin/env python3
"""Corpus metrics: what the framework costs, what it has produced, and how it reads.

Six readings, printed in one report:

  CORPUS    locations and words in setting/region/*/[0-9]*.md
  FEATURES  words and sentences per Feature line, against STYLE.md's budget
  TELLS     every tell in style/tells.txt, counted
  MOTIFS    the words that have spread across regions, and the ones the
            setting-level files seed before a room is written
  BUDGET    framework words against setting words
  READ SET  words in context per step 4c entry point

Nothing here judges. A tell is a candidate a reader looks at, the read-set
figure is an arithmetic sum of what templates/Location.md's Context section
names, and neither carries a threshold - `tools/validate_setting.py` is where
a rule with a pass and a fail lives. This file exists so a change to the
framework can be shown to have moved something, rather than asserted to have.

The Feature parsing, the tell engine, the motif arithmetic, the read-set graph
and the stopword list are imported from the validator rather than restated, so a
change to the Feature grammar or to style/tells.txt reaches this report without
a second edit.

Usage: python3 tools/metrics.py [--tells [PATH]]

  (no argument)  the full report over this repository
  --tells        every tell hit listed with its file and line, not just counted
  --tells PATH   the same, over a file or directory outside setting/ - which is
                 how a control arm in fixtures/ is read with the instrument the
                 setting is read with
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_setting import (  # noqa: E402
    CITATION_RE,
    FEATURE_RE,
    LOCATION_GLOB,
    PATTERNS,
    ROOT,
    count_tells,
    feature_sentences,
    motif_excluded,
    motif_seed,
    motif_spread,
    parse_tells_file,
    read_set_graph,
    rel,
    spec_closure,
    tell_fires,
)

REGION = ROOT / "setting" / "region"
EXEMPLARS = ROOT / "style" / "exemplars" / "location"


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
# The tells
#
# The list is style/tells.txt and the engine is the validator's count_tells, so
# this file neither carries a pattern nor decides what one means. What it adds is
# the reading: every hit listed, with its file and line, over whatever corpus is
# named. Nothing here has a threshold - a tell is a candidate, per STYLE.md, and
# tools/validate_setting.py --fixtures is where a tell has a pass and a fail.
# ---------------------------------------------------------------------------

RATHER_KEY = "rather than"


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
    tells = count_tells(locs)
    if not tells:
        print("  style/tells.txt lists no tells\n")
        return
    for t in tells:
        print(f"  {t.key:16s} : {len(t):4d}   {t.rule}")
    # The share of Features carrying the trailing clause is the figure PR #41
    # reported and the one a later run is comparable with, so it is printed
    # while that tell is in the list.
    feats = features(locs)
    rather = next((t for t in tells if t.key == RATHER_KEY), None)
    if feats and rather:
        carrying = sum(1 for _, _, b in feats if tell_fires(rather, b))
        print(f"  {'':16s}   {RATHER_KEY!r} is in {carrying} of {len(feats)} Features")
    print()


# ---------------------------------------------------------------------------
# The motifs
#
# Counted, not matched, so it is the one tell with no signature - the settings
# and the rationale are style/tells.txt's, and the arithmetic is the
# validator's. What is added here is the ordered reading: the validator warns a
# word at a time, and which motifs a corpus is running on is a question about
# the list rather than about any one of them.
# ---------------------------------------------------------------------------


def report_motifs() -> None:
    print("MOTIFS")
    _tells, motif = parse_tells_file()
    if not motif.configured:
        print("  style/tells.txt states no motif thresholds\n")
        return
    excluded = motif_excluded()
    spread = motif_spread(motif, excluded)
    print(f"  spread             : {len(spread)} word(s) in {motif.regions}+ regions "
          f"and {motif.rooms}+ rooms")
    for word, rooms, regions in spread:
        print(f"    {word:18s} {len(rooms):3d} rooms across {', '.join(regions)}")
    seed = motif_seed(motif, excluded)
    print(f"  seed               : {len(seed)} word(s) at {motif.seed} or more across "
          f"setting/ and the region overviews")
    for word, count in seed:
        print(f"    {word:18s} {count:3d}")
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
# The region overview and the exemplar are both per-entry - one region of five,
# one class file of six - so each is reported as its own range rather than
# folded into one number that would be right for no location.
# ---------------------------------------------------------------------------

FIXED_CONTEXT = ("CLAUDE.md", "README.md", "GENRE.md", "STYLE.md",
                 "templates/Location.md", "setting/Truths.md",
                 "setting/Procedures.md", "setting/Language.md")


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
    exemplars = [file_words(p) for p in sorted(EXEMPLARS.glob("*.md"))] \
        if EXEMPLARS.exists() else []
    if exemplars:
        ex_avg = round(mean(exemplars))
        print(f"  {'exemplar':24s} : {min(exemplars):6,}-{max(exemplars):,} across "
              f"{len(exemplars)} classes, mean {ex_avg:,}")
    else:
        ex_avg = 0
    print(f"  {'fixed context':24s} : {fixed + avg + ex_avg:6,} "
          f"(with the mean region overview and exemplar)")
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
    report_motifs()
    report_budget()
    report_read_set()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        # The tell listing is long and is read through `head` or `less`.
        sys.exit(0)
