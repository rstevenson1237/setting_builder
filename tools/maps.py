#!/usr/bin/env python3
"""Maps from the setting's tables, drawn by artgen (tools/artgen).

  python3 tools/maps.py place [--brief PATH] [--setting DIR]
  python3 tools/maps.py ground [--brief PATH] [--setting DIR]
  python3 tools/maps.py pack REGION [--seed N] [--again]
  python3 tools/maps.py draw [--brief PATH] [--setting DIR] [--out DIR] [--fit WxH[mm|px]]

place    Reads BRIEF.md's `sheet` lines and each region's `ground` and `place` lines, puts
         each region's way in on the sheets that list it - centred where no `place` names
         it, and keeping its placed locations on the sheet - gives it an area reaching its
         farthest location, and asks artgen for terrain meeting its ground at the way in
         and at each location, where no other region's ground meets it - on a sheet in
         miles, over one outline round them all, each Route a road through its stops, and
         no snow or desert. Every location is a keyed mark on its home sheet; one a
         DANGEROUS region opens from is a cave mouth keyed with that region too. Writes
         `setting/[Sheet].json` per sheet and `setting/Sheets.md`. A request that cannot be
         met is reported by its BRIEF.md line, and exits 1.
ground   Reads each placed region's ground back from its home sheet and writes its
         `Ground.md`: the region's way in and terrain, the rivers, roads and hills in its
         area, and, once its Locations.md exists, the ground at each location. Run again
         after the locations are written. A location with no bearing and distance, or north
         and east, from the way in is listed and left out.
pack     Packs each block of a DANGEROUS region into a square (tools/pack.py) and routes a passage
         for every way (tools/route.py), keeping each way's direction as its rooms lie, or else as its
         bearing says. Writes each room's `east` and `north` from the block's centre, the block's
         `footprint` and `router`, and takes the bearing and distance off each way within the block.
         A block already packed whose ways all route is left as it lies; --again repacks it. A seed
         fixes the result.
draw     Builds each block's map, `setting/region/[Code]/[Block].json`, never committed, from its tables - a
         DANGEROUS block's a dungeon, a SAFE block's a settlement walled round its locations
         on its home sheet, a WILD block's the same unwalled unless it states a wall - and with --out renders every sheet and block to SVG there.
         Region maps and location cuts (`region_svg`, `cut_svg`) are paused.
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import json
import math
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kdl                      # noqa: E402,F401
import site_common as sc        # noqa: E402
import tables                   # noqa: E402

ARTGEN = Path(__file__).resolve().parent / "artgen" / "artgen-maps.js"
FEET = {"feet": 1, "yards": 3, "miles": 5280}
UNIT = {"feet": "ft", "yards": "yd", "miles": "mi"}
SQUARES_PER_LOCATION = 4        # the ground one location needs, in squares, before its locations exist
MARK = {"Ruin": "ruin", "Lair": "camp", "Gate": "gate"}   # a location's symbol by type, else a point
LOCATION_GROUND = 1.5           # squares round a location its region's ground must cover
BLEND = 4                       # squares over which a region's ground fades into the country round it
GROUND_SHARE = 0.8              # the share of its area a region's ground must cover
WALLED_SHARE = 0.95             # and of the ground inside its walls
SEPARATION = 0.6                # two areas' centres lie at least this much of their radii apart
BEARING_SLACK = 15              # degrees either side of a compass point
SYNCED_MAP = ("edits", "require", "overlay")   # kept by artgen's map sync, hand entries and all
REGIONAL = {"land": "inland", "sea": 0.0, "moisture": 0.6, "roughness": 0.3, "relief": 0.2, "rivers": 2,
            "simplify": 3, "feature": 40}  # broad country, few rivers and no sea, for a sheet in miles
TEMPERED = {"snow": "rock", "desert": "scrub"}   # what a sheet in miles draws in their place
TEMPER_STEP = 3                 # squares between the points a sheet's ground is tempered at
TEMPER_TRIES = 3
SEEDS = 8                       # terrain seeds tried before a requirement is called unmet
LOCAL_SQUARE_FEET = 60          # a sheet this fine or finer draws as a local map
MARK_GAP = 2                    # squares between two ways in


def feet(text: str) -> float:
    """A `distance` value, "200 yards", in feet."""
    n, unit = str(text).split()
    return float(n) * FEET[unit]


class Sheet:
    def __init__(self, name: str, node: kdl.Node):
        self.name, self.node = name, node
        self.square = feet(node.props["square"])
        w, h, unit = str(node.props["extent"]).replace(" by ", " ").split()
        self.cols, self.rows = round(float(w) * FEET[unit] / self.square), round(float(h) * FEET[unit] / self.square)
        self.codes = str(node.props["regions"]).split()
        self.unit = str(node.props["square"]).split()[1]
        self.per_cell = float(str(node.props["square"]).split()[0])
        self.at: dict[str, tuple[int, int]] = {}
        self.seed = 0


class Request:
    """One `place` line: region `code` lies `bearing` of `of`, `lo` to `hi` squares from it."""

    def __init__(self, code: str, node: kdl.Node, square: float):
        self.code, self.node, self.of = code, node, str(node.args[0])
        compass = list(tables.Schema().setting_enums["Compass"])
        self.angle = compass.index(str(node.args[1])) * 22.5
        m = tables.SPAN_RE.fullmatch(str(node.args[2]))
        unit = FEET[m.group(3)] / square
        self.lo = float(m.group(1)) * unit
        self.hi = float(m.group(2) or m.group(1)) * unit

    def miss(self, a: tuple[float, float], b: tuple[float, float]) -> float:
        """Squares by which region `code` at a misses its place from `of` at b."""
        dx, dy = a[0] - b[0], a[1] - b[1]
        d = math.hypot(dx, dy)
        slack = max(1.0, 0.1 * self.hi)
        far = max(0.0, self.lo - slack - d, d - self.hi - slack)
        if d < 1e-9:
            return far + self.lo + 1
        off = abs((math.degrees(math.atan2(dx, -dy)) - self.angle + 180) % 360 - 180)
        return far + d * math.radians(max(0.0, off - BEARING_SLACK))

    def strain(self, a: tuple[float, float], b: tuple[float, float]) -> float:
        """Squares between region `code` at a and the middle of its place from `of` at b."""
        d = (self.lo + self.hi) / 2
        r = math.radians(self.angle)
        return math.dist(a, (b[0] + d * math.sin(r), b[1] - d * math.cos(r)))

    def said(self, a, b) -> str:
        dx, dy = a[0] - b[0], a[1] - b[1]
        return f"{math.hypot(dx, dy):.1f} squares at {math.degrees(math.atan2(dx, -dy)) % 360:.0f} degrees"


def solve(sheet: Sheet, radius: dict[str, float], requests: list[Request],
          spread: dict[str, list[tuple[float, float]]]) -> list[str]:
    """Positions for sheet.codes, in sheet.at, meeting every request, keeping the areas
    apart and every located place on the sheet. A region no request names is centred.
    Returns what is unmet, empty when all is met."""
    rng = random.Random(1)
    codes = sheet.codes
    reach = {c: [p for p in spread.get(c, [])] + [(sx * radius[c], sy * radius[c]) for sx in (-1, 1) for sy in (-1, 1)]
             for c in codes}
    lo = {c: (-min(p[0] for p in reach[c]), -min(p[1] for p in reach[c])) for c in codes}
    hi = {c: (sheet.cols - 1 - max(p[0] for p in reach[c]), sheet.rows - 1 - max(p[1] for p in reach[c])) for c in codes}

    def clamp(code, x, y):
        (x0, y0), (x1, y1) = lo[code], hi[code]
        return (min(max(x, x0), x1) if x0 <= x1 else (x0 + x1) / 2, min(max(y, y0), y1) if y0 <= y1 else (y0 + y1) / 2)

    def cost(at):
        at = {c: (round(x), round(y)) for c, (x, y) in at.items()}   # judged as it will be written
        c = sum(q.miss(at[q.code], at[q.of]) for q in requests)
        for i, a in enumerate(codes):
            for b in codes[i + 1:]:
                gap = max(SEPARATION * (radius[a] + radius[b]), MARK_GAP)
                c += max(0.0, gap - math.dist(at[a], at[b]))
        return c

    best, best_cost = None, math.inf
    for _ in range(12):
        at = {c: clamp(c, rng.uniform(0, sheet.cols), rng.uniform(0, sheet.rows)) for c in codes}
        now = cost(at)
        for step in range(6000):
            heat = max(0.2, (1 - step / 6000) * max(sheet.cols, sheet.rows) / 4)
            c = rng.choice(codes)
            old = at[c]
            at[c] = clamp(c, old[0] + rng.gauss(0, heat), old[1] + rng.gauss(0, heat))
            new = cost(at)
            if new <= now or rng.random() < math.exp((now - new) / max(0.05, heat / 10)):
                now = new
            else:
                at[c] = old
        if now < best_cost:
            best, best_cost = dict(at), now
        if now < 1e-6:
            break
    for c in codes:
        if not any(c in (q.code, q.of) for q in requests):
            best[c] = ((lo[c][0] + hi[c][0]) / 2, (lo[c][1] + hi[c][1]) / 2)
    at = {c: (round(x), round(y)) for c, (x, y) in best.items()}
    strain = lambda at: sum(q.strain(at[q.code], at[q.of]) for q in requests)
    moved = True
    while moved:                                  # then square by square toward each place's middle
        moved = False
        for c in codes:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                was, now = at[c], (at[c][0] + dx, at[c][1] + dy)
                if clamp(c, *now) != now:
                    continue
                before = (cost(at), strain(at))
                at[c] = now
                if cost(at) <= before[0] and strain(at) < before[1] - 1e-9:
                    moved = True
                else:
                    at[c] = was
    sheet.at = at
    out = []
    for c in codes:
        if lo[c][0] > hi[c][0] or lo[c][1] > hi[c][1]:
            out.append(f"{c}'s locations do not fit on {sheet.name}")
    for q in requests:
        if q.miss(sheet.at[q.code], sheet.at[q.of]) > 0.5:
            out.append(f"line {q.node.line}: region {q.code} place {q.of} {q.node.args[1]} "
                       f"{q.node.args[2]!r} is unmet on {sheet.name}: "
                       f"{q.said(sheet.at[q.code], sheet.at[q.of])}")
    for i, a in enumerate(codes):
        for b in codes[i + 1:]:
            if math.dist(sheet.at[a], sheet.at[b]) < max(SEPARATION * (radius[a] + radius[b]), MARK_GAP) - 0.5:
                lines = [str(q.node.line) for q in requests if {q.code, q.of} == {a, b}]
                out.append(f"{'line ' + ', '.join(lines) + ': ' if lines else ''}{a} and {b} cannot lie apart "
                           f"on {sheet.name}: their places leave no room")
    return out


def artgen(*args) -> subprocess.CompletedProcess:
    """One artgen call. Its output goes through a file: on a pipe, node cuts it at 64 KB."""
    with tempfile.TemporaryFile("w+") as out:
        done = subprocess.run(["node", str(ARTGEN), *map(str, args)], stdout=out, stderr=subprocess.PIPE, text=True)
        out.seek(0)
        return subprocess.CompletedProcess(done.args, done.returncode, out.read(), done.stderr)


def map_file(sheet: Sheet, seed: int, regions: dict, radius: dict, home: dict, spread: dict,
             marks: list[tuple[float, float, str, str]], walled: dict[str, list[float]],
             routes: dict[str, list[list[tuple[float, float]]]]) -> dict:
    local = sheet.square <= LOCAL_SQUARE_FEET
    circles = []                                  # (id, x, y, r, terrain): each area's ground
    for code in sheet.codes:
        ground = next((c for c in regions[code].children if c.name == "ground"), None)
        if home[code] == sheet.name and ground:
            x, y = sheet.at[code]
            circles.append((f"{code}-ground", x, y, radius[code], str(ground.args[0])))
            circles += [(f"{code}-ground-{i + 1}", round(x + dx, 1), round(y + dy, 1), LOCATION_GROUND, str(ground.args[0]))
                        for i, (dx, dy) in enumerate(p for p in spread.get(code, []) if math.hypot(*p) > radius[code])]
    clash = lambda a: any(b[4] != a[4] and math.dist(a[1:3], b[1:3]) < a[3] + b[3] + 2 for b in circles)
    m = {"id": sheet.name, "version": 1, "preset": "local" if local else "regional", "seed": seed,
         "cols": sheet.cols, "rows": sheet.rows, "grid": {"type": "square", "size": 1, "coords": False},
         "scale": {"perCell": sheet.per_cell, "unit": UNIT[sheet.unit]},
         "edits": [], "overlay": {"labels": [], "symbols": []}, "require": []}
    if not local:
        m["topo"] = {"maxElevation": 600, "interval": 50, "majorEvery": 4, "unit": "ft", "labels": False}
        m["gen"] = dict(REGIONAL)
    for code in sheet.codes:
        x, y = sheet.at[code]
        area = home[code] == sheet.name
        rating = str(regions[code].props.get("rating", "")).upper()
        m["overlay"]["symbols"].append({"kind": "castle" if rating == "SAFE" else "poi", "x": x, "y": y,
                                        "origin": "tables"})
        far = [p for p in spread.get(code, []) if math.hypot(*p) > radius[code]] if area else []
        lx, ly = (x + sum(p[0] for p in far) / len(far), y + sum(p[1] for p in far) / len(far)) if far else (x + 1.2, y)
        m["overlay"]["labels"].append({"text": code, "x": round(lx, 1),
                                       "y": round(ly, 1), "kind": "region" if area else "place", "origin": "tables"})
    for code, lines in routes.items():            # on a sheet in miles, a Route a road through its stops
        for i, line in enumerate(lines):
            m["require"].append({"id": f"{code}-route-{i + 1}", "kind": "path", "path": "road", "origin": "tables",
                                 "points": [round(v, 1) for p in line for v in p], "tolerance": 1})
    for x, y, kind, label in marks:
        m["overlay"]["symbols"].append({"kind": kind, "x": x, "y": y, "origin": "tables"})
        m["overlay"]["labels"].append({"text": label, "x": round(x + 0.8, 1), "y": y, "kind": "place", "origin": "tables"})
    for code, (w, n, e, south) in walled.items():  # inside a region's walls, its own ground and no river
        x, y = sheet.at[code]
        ground = next((c for c in regions[code].children if c.name == "ground"), None)
        poly = [round(v, 1) for p in ((w, n), (e, n), (e, south), (w, south)) for v in (x + p[0] / sheet.square, y + p[1] / sheet.square)]
        if ground:
            m["require"].append({"id": f"{code}-walls", "kind": "terrain", "origin": "tables", "area": {"poly": poly},
                                 "terrain": str(ground.args[0]), "share": WALLED_SHARE})
        m["require"].append({"id": f"{code}-walls-clear", "kind": "clear", "origin": "tables", "area": {"poly": poly}})
    if not local:                                 # on a sheet in miles, one outline round the way in and every location
        for code in dict.fromkeys(c[0].split("-")[0] for c in circles):   # in the sheet's order: a later one wins
            own = [c for c in circles if c[0].split("-")[0] == code]
            m["require"].append({"id": f"{code}-ground", "kind": "terrain", "origin": "tables", "terrain": own[0][4],
                                 "area": {"poly": hull([(x + LOCATION_GROUND * 2 * math.cos(a * math.pi / 4),
                                                         y + LOCATION_GROUND * 2 * math.sin(a * math.pi / 4))
                                                        for _, x, y, *_ in own for a in range(8)])},
                                 "share": GROUND_SHARE, "blend": BLEND})
        circles = []
    for c in circles:                             # a location's ground yields where another region's meets it
        if c[0].endswith("-ground") or not clash(c):
            m["require"].append({"id": c[0], "kind": "terrain", "origin": "tables", "area": {"circle": list(c[1:4])},
                                 "terrain": c[4], "share": GROUND_SHARE})
    return m


def hull(points: list[tuple[float, float]]) -> list[float]:
    """The convex hull of points, as x,y pairs flattened."""
    pts = sorted(set((round(x, 1), round(y, 1)) for x, y in points))
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return [v for p in lower[:-1] + upper[:-1] for v in p]


def temper(file: Path) -> None:
    """Asks for rock where a sheet in miles draws snow, and scrub where it draws desert, until
    it draws neither: artgen tops every such sheet's highest ground with snow, and a borderland's
    hills carry none."""
    m = json.loads(file.read_text())
    grid = [(x + 0.5, y + 0.5) for y in range(0, m["rows"], TEMPER_STEP) for x in range(0, m["cols"], TEMPER_STEP)]
    for _ in range(TEMPER_TRIES):
        done = artgen("map", "facts", "--file", file, "--json", "--at", *[f"{x},{y}" for x, y in grid])
        points = json.loads(done.stdout).get("points", []) if done.stdout.startswith("{") else []
        found = [(p, TEMPERED[t["terrain"]]) for p, t in zip(grid, points) if t["terrain"] in TEMPERED]
        if not found:
            return
        n = len([r for r in m["require"] if r["id"].startswith(f"{m['id']}-temper")])
        m["require"][:0] = [{"id": f"{m['id']}-temper-{n + i + 1}", "kind": "terrain", "origin": "tables", "terrain": t,
                             "area": {"circle": [x, y, TEMPER_STEP]}, "share": 0.5, "blend": TEMPER_STEP}
                            for i, ((x, y), t) in enumerate(found)]
        file.write_text(json.dumps(m, indent=1))


def draw_sheet(sheet: Sheet, target: Path, build) -> tuple[list[str], int]:
    """Writes the sheet's map file with the first seed meeting every requirement, else the
    seed missing fewest. Returns what is unmet, and the seed."""
    kept = json.loads(target.read_text()) if target.exists() else None
    first = kept["seed"] if kept else 1
    seeds = [first] + [s for s in range(1, SEEDS + 1) if s != first]
    best = None
    with tempfile.TemporaryDirectory() as tmp:
        for seed in seeds:
            fresh = Path(tmp) / f"{sheet.name}.json"
            fresh.write_text(json.dumps(build(seed), indent=1))
            if kept:
                joined = Path(tmp) / "joined.json"
                built = json.loads(fresh.read_text())    # what sync leaves alone follows the tables too
                joined.write_text(json.dumps({**kept, **{k: v for k, v in built.items() if k not in SYNCED_MAP}}))
                done = artgen("map", "sync", "--file", joined, "--from", fresh, "--origin", "tables")
                if done.returncode:
                    return [f"artgen cannot sync {sheet.name}: {done.stderr.strip() or done.stdout.strip()}"], seed
                fresh = joined
            if sheet.square > LOCAL_SQUARE_FEET:
                temper(fresh)
            done = artgen("map", "check", "--file", fresh, "--json")
            report = json.loads(done.stdout) if done.stdout.strip().startswith("{") else None
            if report is None:
                return [f"artgen cannot read {sheet.name}: {(done.stderr or done.stdout).strip()}"], seed
            errors = [f"{e['path']}: {e['message']}" for e in report["errors"]]
            unmet = errors + [r["text"] for r in report["requirements"] if not r["met"]]
            if best is None or len(unmet) < len(best[0]):
                best = (unmet, seed, fresh.read_text())
            if not unmet:
                break
        target.write_text(best[2])
    return best[0], best[1]


def place(brief_path: Path, setting: Path) -> int:
    schema = tables.Schema(brief=brief_path)
    brief = tables.Brief(schema, brief_path)
    if brief.problems:
        for p in brief.problems:
            print(f"BRIEF.md: {p}")
        return 1
    if not brief.sheets:
        print("BRIEF.md asks for no sheets.")
        return 0
    sheets = {n: Sheet(n, node) for n, node in brief.sheets.items()}
    home = {}
    for code in brief.regions:
        on = [s for s in sheets.values() if code in s.codes]
        if on:
            home[code] = min(on, key=lambda s: s.square).name
    radius = {}
    for code, node in brief.regions.items():
        n = tables.bounds(node.props.get("locations", 1))[1]
        radius[code] = max(3, math.ceil(math.sqrt(SQUARES_PER_LOCATION * n / math.pi)))
    world = world_for(setting) if (setting / "region" / "Regions.md").exists() else None
    unmet, table = [], []
    for sheet in sheets.values():
        rad = {c: (radius[c] if home[c] == sheet.name else 0) for c in sheet.codes}
        spread = {c: located(world, c, sheet.square) for c in sheet.codes if home[c] == sheet.name}
        area = {c: max([rad[c]] + [math.ceil(math.hypot(*p)) + 1 for p in spread.get(c, [])]) if rad[c] else 0
                for c in sheet.codes}
        asks = [Request(c, p, sheet.square) for c in sheet.codes
                for p in brief.regions[c].children if p.name == "place" and str(p.args[0]) in sheet.codes]
        unmet += solve(sheet, rad, asks, spread)
        target = setting / f"{sheet.name}.json"
        marks = location_marks(world, sheet, home) if world else []
        walled = {c: box for c in sheet.codes if home[c] == sheet.name and world and c in world.regions
                  and world.regions[c].rating.upper() == "SAFE"
                  for b in drawn_blocks(world.regions[c]).values() if (box := enclosure(world.regions[c], b)[2])}
        routes = {c: lines for c in sheet.codes if sheet.square > LOCAL_SQUARE_FEET and home[c] == sheet.name
                  and world and c in world.regions and (lines := route_lines(world.regions[c], sheet))}
        problems, sheet.seed = draw_sheet(sheet, target, lambda seed, s=sheet: map_file(
            s, seed, brief.regions, rad, home, spread, marks, walled, routes))
        for p in problems:
            ground = brief.regions.get(p.split("-")[0])
            node = next((c for c in ground.children if c.name == "ground"), None) if ground else None
            unmet.append(f"{'line ' + str(node.line) + ': ' if node else ''}{sheet.name}: {p}")
        for code in sheet.codes:
            x, y = sheet.at[code]
            table.append(f"| {sheet.name} {code} | {sheet.name} | {code} | {x},{y} | "
                         f"{'circle, radius ' + str(area[code]) + ' squares' if area[code] else 'mark'} |")
    title = "Sheets"
    if (reg := setting / "region" / "Regions.md").exists():
        first = reg.read_text().splitlines()[0]
        title = "Sheets of " + first.split(" of ", 1)[1] if " of " in first else title
    (setting / "Sheets.md").write_text(
        f"{title}\n\n| Name | Sheet | Region | Way in | Area |\n|---|---|---|---|---|\n" + "\n".join(table) + "\n")
    for u in unmet:
        print(f"UNMET: {u}")
    print(f"{len(sheets)} sheet(s) placed, {len(unmet)} request(s) unmet")
    return 1 if unmet else 0


def compass(dx: float, dy: float) -> str:
    """The Compass point of a displacement on a sheet, north being up."""
    points = list(tables.Schema().setting_enums["Compass"])
    return points[round((math.degrees(math.atan2(dx, -dy)) % 360) / 22.5) % 16]


def said(ft: float) -> str:
    """A length as a `distance` value, in the unit it reads best in."""
    if ft >= 4800:
        n, unit = round(ft / 5280 * 2) / 2, "miles"
    elif ft >= 600:
        n, unit = round(ft / 3 / 10) * 10, "yards"
    else:
        n, unit = max(10, round(ft / 10) * 10), "feet"
    return f"{n:g} {unit}"


def offset(node: kdl.Node) -> tuple[float, float] | None:
    """A location's (east, north) in feet from its region's way in, or None when it states
    no bearing and distance, or north and east."""
    p = node.props
    if str(p.get("at", "")) == "way in":
        return 0.0, 0.0
    num = lambda v: (-1 if str(v).startswith("-") else 1) * feet(str(v).lstrip("-"))
    try:
        if "bearing" in p and "distance" in p:
            a = list(tables.Schema().setting_enums["Compass"]).index(str(p["bearing"])) * 22.5
            d = num(p["distance"])
            return d * math.sin(math.radians(a)), d * math.cos(math.radians(a))
        if "north" in p or "east" in p:
            return num(p["east"]) if "east" in p else 0.0, num(p["north"]) if "north" in p else 0.0
    except (ValueError, KeyError):
        return None
    return None


def way(world, a: str, b: str) -> tuple[str, str] | None:
    """Where the way from location a to b runs, as (Compass point, distance): the wall it leaves
    a packed room by and its walk to the next room, else its Connection's bearing and distance."""
    region = world.regions.get(a.split(".")[0])
    if region is None:
        return None
    if region.rating.upper() == "DANGEROUS":
        import dungeon
        if (w := dungeon.walks(region.code).get((a, b))):
            return w[0], f"{w[1]} feet"
    n = next((n for n in region.files.get("Connections", []) if n.args and str(n.args[0]) == a
              and str(n.props.get("to")) == b and "bearing" in n.props and "distance" in n.props), None)
    return (str(n.props["bearing"]), str(n.props["distance"])) if n else None


def location_marks(world, sheet: Sheet, home: dict) -> list[tuple[float, float, str, str]]:
    """Each location on its home sheet as a keyed mark; where a DANGEROUS region opens from
    one, a cave mouth keyed with that region's code too."""
    opens: dict[str, list[str]] = {}
    for region in world.regions.values():
        if region.rating.upper() == "DANGEROUS":
            for n in region.files.get("Connections", []):
                if n.args and str(n.props.get("to", "")).split(".")[0] != region.code:
                    opens.setdefault(str(n.props["to"]), []).append(region.code)
    out = []
    for code in sheet.codes:
        if home.get(code) != sheet.name or code not in world.regions:
            continue
        x0, y0 = sheet.at[code]
        for loc, node in world.regions[code].locations().items():
            if (o := offset(node)) is None:
                continue
            kind = "cave-mouth" if loc in opens else MARK.get(str(node.props.get("type")), "poi")
            label = " ".join([loc] + sorted(set(opens.get(loc, []))))
            out.append((round(x0 + o[0] / sheet.square, 1), round(y0 - o[1] / sheet.square, 1), kind, label))
    return out


def route_lines(region, sheet: Sheet) -> list[list[tuple[float, float]]]:
    """Each Route of a region as squares on its sheet: from the way in through its stops in
    order. A route with fewer than two placed points is left out."""
    x, y = sheet.at[region.code]
    lines: dict[str, list[tuple[float, float]]] = {}
    for n in region.files.get("Stops", []):
        if n.args and (o := offset(n)) is not None:
            lines.setdefault(str(n.args[0]), [(x, y)]).append((x + o[0] / sheet.square, y - o[1] / sheet.square))
    return [line for line in lines.values() if len(line) > 1]


def located(world, code: str, square: float) -> list[tuple[float, float]]:
    """Each placed location of a region as squares east and south of its way in."""
    region = world.regions.get(code) if world else None
    out = []
    for node in (region.locations().values() if region else []):
        if (o := offset(node)) is not None:
            out.append((o[0] / square, -o[1] / square))
    return out


def read_only(file: Path, *args) -> subprocess.CompletedProcess:
    """An artgen call that reads a map and changes nothing. Generating the ground takes
    seconds, so the answer is kept under .maps-cache, keyed by the map file and the call."""
    key = hashlib.sha256("\0".join([file.read_text(), ARTGEN.parent.joinpath("VERSION").read_text(),
                                    *map(str, args)]).encode()).hexdigest()
    kept = CACHE / f"{key}.json"
    if kept.exists():
        return subprocess.CompletedProcess(args, *json.loads(kept.read_text()))
    done = artgen(*args, "--file", file, "--json")
    if done.returncode in (0, 1) and done.stdout.strip().startswith("{"):
        CACHE.mkdir(exist_ok=True)
        kept.write_text(json.dumps([done.returncode, done.stdout, done.stderr]))
    return done


def facts(file: Path, *args) -> dict:
    done = read_only(file, "map", "facts", *args)
    if done.returncode or not done.stdout.strip():
        raise SystemExit(f"artgen cannot read {file.name}: {(done.stderr or done.stdout).strip()}")
    return json.loads(done.stdout)


def ground_texts(brief_path: Path, setting: Path) -> tuple[dict[str, str], list[str], list[str]] | str:
    """Each placed region's Ground.md as `ground` would write it now, the locations off
    their sheets, and those with no position stated. A string says why it cannot."""
    schema = tables.Schema(brief=brief_path)
    brief = tables.Brief(schema, brief_path)
    sheets_md = setting / "Sheets.md"
    if brief.problems or not sheets_md.exists():
        return "; ".join(brief.problems) if brief.problems else "setting/Sheets.md is missing: run `place` first"
    sheets = {n: Sheet(n, node) for n, node in brief.sheets.items()}
    rows = sc.read_tables(sheets_md)[0].dicts()
    gazetteer = sc.parse_regions_gazetteer()
    world = tables.Setting({c: g["rating"] for c, g in gazetteer.items()})
    skipped, off, texts = [], [], {}
    for row in rows:
        code, area = row["Region"], row["Area"]
        if not area.startswith("circle"):
            continue
        sheet = sheets[row["Sheet"]]
        radius = int(area.split("radius")[1].split()[0])
        x, y = (float(v) for v in row["Way in"].split(","))
        file = setting / f"{sheet.name}.json"
        ring = ",".join(f"{x + radius * math.cos(a * math.pi / 8):.1f},{y + radius * math.sin(a * math.pi / 8):.1f}"
                        for a in range(16))
        shares = facts(file, "--area", ring)["areas"][0]["terrain"]
        lines = [f'Ground {code} sheet="{sheet.name}" square="{x:g},{y:g}" ground="'
                 + ", ".join(f"{t['terrain']} {t['share']}%" for t in shares if t["share"] >= 5) + '"']
        whole = facts(file)["features"]
        reach = radius * 1.3
        cell = sheet.square

        def seen(kind, name_points, runs):
            near = min(name_points, key=lambda p: math.dist(p, (x, y)))
            if math.dist(near, (x, y)) > reach:
                return
            e, n = (near[0] - x) * cell, -(near[1] - y) * cell
            line = f'Feature {code} kind="{kind}" bearing="{compass(e, -n)}" distance="{said(math.hypot(e, n))}"'
            if runs:
                a, b = runs
                line += f' runs="{compass(b[0] - a[0], b[1] - a[1])}"'
            return line

        for kind, key in (("river", "rivers"), ("river", "generatedRivers"), ("road", "roads")):
            for f in whole.get(key, []):
                if line := seen(kind, f["points"], (f["points"][0], f["points"][-1])):
                    lines.append(line)
        for kind, key in (("hill", "hilltops"), ("hollow", "hollows")):
            for f in sorted((f for f in whole.get(key, []) if math.dist(f["at"], (x, y)) <= reach),
                            key=lambda f: -f["height"] if kind == "hill" else f["height"])[:3]:
                lines.append(seen(kind, [f["at"]], None) + f' height="{round(f["height"])}"')
        located = world.regions[code].locations() if code in world.regions else {}
        spots = {}
        for loc, node in located.items():
            o = offset(node)
            if o is None:
                skipped.append(loc)
                continue
            px, py = x + o[0] / cell, y - o[1] / cell
            if 0 <= px < sheet.cols and 0 <= py < sheet.rows:
                spots[loc] = (px, py)
            else:
                off.append(loc)
        if spots:
            got = facts(file, "--at", *[f"{px:.1f},{py:.1f}" for px, py in spots.values()])["points"]
            for loc, pt in zip(spots, got):
                lines.append(f'At {loc} ground="{pt["terrain"]}" height="{round(pt["height"])}" slope="{pt["slope"]["band"]}"')
        texts[code] = f"# Ground of {code} {gazetteer[code]['name']}\n\n```kdl\n" + "\n".join(lines) + "\n```\n"
    return texts, off, skipped


def ground(brief_path: Path, setting: Path) -> int:
    made = ground_texts(brief_path, setting)
    if isinstance(made, str):
        print(made)
        return 1
    texts, off, skipped = made
    for code, text in texts.items():
        folder = setting / "region" / code
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "Ground.md").write_text(text)
    if off:
        print("NOTE: off its sheet: " + ", ".join(off))
    if skipped:
        print("NOTE: no bearing and distance, or north and east, for " + ", ".join(skipped))
    return 0



ENGINE = {"DANGEROUS": "dungeon", "SAFE": "settlement", "WILD": "settlement"}   # the artgen engine a rating's blocks draw with



def blocks_of(region) -> dict[str, kdl.Node]:
    return {str(n.args[0]): n for n in region.files.get("Blocks", []) if n.args}


def drawn_blocks(region) -> dict[str, kdl.Node]:
    """The blocks drawn for a region: a DANGEROUS region's as dungeons, a SAFE or WILD region's
    as settlements. Region and location maps are paused."""
    return blocks_of(region) if region.rating.upper() in ENGINE else {}


def block_file(region, block: kdl.Node) -> tuple[dict | None, list[str]]:
    """The artgen file for one block, by its region's rating, and what the tables leave it
    unable to draw."""
    if region.rating.upper() == "DANGEROUS":
        import dungeon
        return dungeon.block_map(region, block)
    return settlement_map(region, block)



# -- blocks: a SAFE region's enclosure, its buildings where its locations stand ----------

TOWN_CELLS = (5, 10, 20)        # feet to a settlement's cell, the finest that fits
MAX_TOWN = 240                  # cells across a settlement, artgen's limit
TOWN_EDGE = 12                  # cells of ground beyond the wall
WALL_GAP = 15                   # feet between the wall and the buildings it encloses
BUILDING = {"Inn": "inn", "Merchant": "shop", "Bank": "shop", "Authority": "hall"}
NAMED = {"Chapel": "chapel", "Temple": "temple", "Shrine": "chapel", "Forge": "smithy", "Smithy": "smithy",
         "Barracks": "barracks", "Hall": "hall", "Tavern": "tavern", "Stable": "stable", "Mill": "mill",
         "Tower": "tower", "Keep": "keep", "Warehouse": "warehouse", "Manor": "manor"}   # a word in its name, over its type
WALL = ("palisade", "fence", "hedge", "drystone", "ruined")   # a word in the Block's wall, else a curtain
POSTERN = 10                    # feet: a Gate narrower than this is a postern, else a gatehouse
WILD_PLACE = {"Gardens": ("area", "garden"), "Shore": ("water", "lake")}   # a word in a WILD name, over its type
UNSIZED = 20                    # feet, a place's side where its Dressing states none


def enclosure(region, block: kdl.Node) -> tuple[dict, dict, list[float] | None, list[str]]:
    """A SAFE or WILD block's drawn locations, each at its place and with its footprint in feet east and
    south of the way in, the wall round them as west, north, east and south, running through
    each Gate, and what the tables leave unplaced. A Secret is under the ground and not drawn."""
    locs = region.locations()
    dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    problems, at, size = [], {}, {}
    for c in (m.strip() for m in str(block.props["locations"]).split(",")):
        node = locs.get(c)
        if node is None or str(node.props.get("type")) == "Secret":
            continue
        if (o := offset(node)) is None:
            problems.append(f"{c} states no bearing and distance, or north and east")
            continue
        d = dress.get(c)
        w, h = (d.props.get(k) if d else None for k in ("width", "length"))
        if w is None or h is None:
            problems.append(f"{c} states no width and length")
        at[c], size[c] = (o[0], -o[1]), (float(w or UNSIZED), float(h or UNSIZED))
    inside = [c for c in at if str(locs[c].props.get("type")) != "Gate"] or list(at)
    if not inside:
        return at, size, None, problems
    box = [min(at[c][0] - size[c][0] / 2 for c in inside) - WALL_GAP, min(at[c][1] - size[c][1] / 2 for c in inside) - WALL_GAP,
           max(at[c][0] + size[c][0] / 2 for c in inside) + WALL_GAP, max(at[c][1] + size[c][1] / 2 for c in inside) + WALL_GAP]
    for c in set(at) - set(inside):                       # the wall runs through each gate
        x, y = at[c]
        k = min(range(4), key=lambda k: abs(box[k] - (x, y)[k % 2]))
        box[k] = (x, y)[k % 2]
    return at, size, box, problems


def settlement_map(region, block: kdl.Node) -> tuple[dict | None, list[str]]:
    """The artgen settlement file for a SAFE or WILD region's block: each location a building at its
    place, with its footprint; a Market an open yard; a Gate a way through the wall drawn
    round the rest; a road out of each gate along its Way to another region. Its region's
    home sheet is the ground beneath it."""
    code, bid = region.code, str(block.args[0])
    locs = region.locations()
    at, size, box, problems = enclosure(region, block)
    if not at:
        return None, problems
    kind = lambda c: str(locs[c].props.get("type"))
    across = max(box[2] - box[0], box[3] - box[1]) + 2 * TOWN_EDGE * TOWN_CELLS[0]
    step = next((c for c in TOWN_CELLS if across / c <= MAX_TOWN), TOWN_CELLS[-1])
    gates = [c for c in at if kind(c) == "Gate"]
    inside = [c for c in at if c not in gates]
    row = sheet_rows(tables.SETTING).get(code)
    sheet = tables.SETTING / f"{row['sheet']}.json" if row else None
    ground = json.loads(sheet.read_text()) if sheet and sheet.exists() else None
    square = feet(f"{ground['scale']['perCell']} {dict((v, k) for k, v in UNIT.items())[ground['scale']['unit']]}") \
        if ground else step
    way = (row["x"] * square, row["y"] * square) if ground else (0.0, 0.0)   # the way in, in feet on the sheet
    lo = [way[0] + box[0] - TOWN_EDGE * step, way[1] + box[1] - TOWN_EDGE * step]
    hi = [way[0] + box[2] + TOWN_EDGE * step, way[1] + box[3] + TOWN_EDGE * step]
    if ground:                                            # kept on the sheet beneath it
        lo = [max(0.0, lo[0]), max(0.0, lo[1])]
        hi = [min(ground["cols"] * square, hi[0]), min(ground["rows"] * square, hi[1])]
    lo = [math.floor(v / step) * step for v in lo]
    cols, rows = (math.ceil((hi[i] - lo[i]) / step) for i in (0, 1))
    cell = lambda x, y: (round((way[0] + x - lo[0]) / step, 1), round((way[1] + y - lo[1]) / step, 1))
    wall_kind = next((k for k in WALL if k in str(block.props.get("wall", ""))), "curtain")
    towers = next((t for t in ("round", "square") if t in str(block.props.get("towers", ""))), None)
    corners = [cell(box[0], box[1]), cell(box[2], box[1]), cell(box[2], box[3]), cell(box[0], box[3])]
    wall = {"kind": wall_kind, "points": [v for p in corners for v in p], "closed": True, "origin": "tables",
            **({"towers": {"shape": towers}} if towers else {}),
            "gates": [{"at": list(cell(*at[c])), "kind": "postern" if min(size[c]) < POSTERN else "gatehouse"} for c in gates]}
    walled = region.rating.upper() != "WILD" or "wall" in block.props   # a WILD place is walled only where it says
    m = {"id": f"{code}-{bid.split('.')[-1]}", "version": 1, "kind": "castle", "seed": 1, "cols": cols, "rows": rows,
         "ground": "grass", "grid": {"show": True, "size": 2, "sub": False},
         "scale": {"perCell": step, "unit": "ft"}, "numbers": True, "scaleBar": True, "compass": True,
         "furniture": {"place": "auto"}, "roads": [], "water": [], "walls": [wall] if walled else [], "buildings": [], "areas": [], "trees": [],
         "props": [], "overlay": {"labels": [], "symbols": []}}
    if ground:
        m["underlay"] = {"map": f"../../{sheet.name}", "origin": [round(lo[0] / square, 2), round(lo[1] / square, 2)],
                         "scale": step / square}
    for c in inside:
        (x, y), (w, h) = cell(at[c][0] - size[c][0] / 2, at[c][1] - size[c][1] / 2), size[c]
        words = str(locs[c].props.get("name", "")).split()
        w, h = w / step, h / step
        rect = [x, y, x + w, y, x + w, y + h, x, y + h]
        wild = region.rating.upper() == "WILD"
        placed = next((WILD_PLACE[k] for k in words if k in WILD_PLACE), None) if wild else None
        if kind(c) == "Market" or (wild and placed is None and kind(c) == "Natural"):
            placed = ("area", "market" if kind(c) == "Market" else "scrub")
        if wild and kind(c) == "Route":                  # a way along the place's longer side
            line = [x, y + h / 2, x + w, y + h / 2] if w >= h else [x + w / 2, y, x + w / 2, y + h]
            m["roads"].append({"kind": "street", "points": line, "width": round(min(w, h), 1), "label": c, "origin": "tables"})
            continue
        if placed and placed[0] == "water":
            m["water"].append({"kind": placed[1], "points": rect, "origin": "tables"})
            m["overlay"]["labels"].append({"text": c, "x": round(x + w / 2, 1), "y": round(y + h / 2, 1), "kind": "name", "origin": "tables"})
            continue
        if placed:
            m["areas"].append({"kind": placed[1], "points": rect, "label": c, "origin": "tables"})
            continue
        word = next((NAMED[k] for k in NAMED if k in words), None)
        word = "ruin" if wild and kind(c) == "Ruin" else word
        m["buildings"].append({"id": c.replace(".", "-"), "kind": word or BUILDING.get(kind(c), "house"), "shape": "rect",
                               "x": x, "y": y, "w": round(w, 1), "h": round(h, 1),
                               "label": c, "number": int(c.split(".")[1]), "origin": "tables"})
    for c in gates:
        x, y = cell(*at[c])
        m["overlay"]["labels"].append({"text": c, "x": x, "y": round(y - 2, 1), "kind": "note", "origin": "tables"})
    compass = list(tables.Schema().setting_enums["Compass"])
    for n in region.files.get("Connections", []):        # a road out of each gate to another region
        a, b = str(n.args[0]) if n.args else "", str(n.props.get("to", ""))
        if a in gates and b.split(".")[0] != code and "bearing" in n.props:
            r = math.radians(compass.index(str(n.props["bearing"])) * 22.5)
            x, y = cell(*at[a])
            run = max(cols, rows)
            far = (min(max(x + math.sin(r) * run, 0), cols), min(max(y - math.cos(r) * run, 0), rows))
            m["roads"].append({"kind": "highway" if str(locs[a].props.get("at", "")) == "way in" else "path",
                               "points": [x, y, round(far[0], 1), round(far[1], 1)], "label": f"to {b}",
                               "origin": "tables"})
    return m, problems


@functools.cache
def world_for(setting: Path) -> tables.Setting:
    gazetteer = sc.parse_regions_gazetteer()
    return tables.Setting({c: g["rating"] for c, g in gazetteer.items()})



@functools.cache
def built(code: str, bid: str, setting: Path = tables.SETTING) -> tuple[Path | None, tuple[str, ...]]:
    """A block's map file, built from its tables as `setting/region/[Code]/[Block].json`, which
    git ignores, and written only when it changes; and what the tables leave it unable to
    draw. The file is None where nothing can be drawn."""
    region = world_for(setting).regions[code]
    m, problems = block_file(region, drawn_blocks(region)[bid])
    if m is None:
        return None, tuple(problems)
    if ENGINE[region.rating.upper()] == "dungeon":
        import dungeon
        dungeon.route_around(m)
    target, text = region.dir / f"{bid}.json", json.dumps(m, indent=1)
    if not target.exists() or target.read_text() != text:
        target.write_text(text)
    return target, tuple(problems)


def write_blocks(world, only: str | None = None) -> list[str]:
    """Each drawn block's map file. Returns what cannot be drawn."""
    import dungeon
    out = []
    for code, region in world.regions.items():
        if only and code != only:
            continue
        engine = ENGINE.get(region.rating.upper())
        for bid, block in drawn_blocks(region).items():
            target, problems = built(code, bid)
            out += [f"{bid}: {p}" for p in problems]
            if target is None:
                continue
            done = artgen(engine, "check", "--file", target, "--json")
            for e in json.loads(done.stdout).get("errors", []) if done.stdout.startswith("{") else []:
                out.append(f"{bid}: {e['path']}: {e['message']}")
            if engine == "dungeon":
                out += [f"{bid}: {d}" for d in dungeon.defects(region, block, json.loads(target.read_text())) if not d.startswith("label:")]
                with tempfile.TemporaryDirectory() as tmp:
                    shown = artgen("dungeon", "render", "--file", target, "--format", "svg", "--fit", SITE_FIT, "--json", "--out", tmp)
                    for left in json.loads(shown.stdout).get("unplaced", []) if shown.stdout.startswith("{") else []:
                        out.append(f"{bid}: the note {left['text']!r} found no room on the page")
    return out


# -- renders --------------------------------------------------------------------

SITE_FIT = "720x560px"
PDF_FIT = "110x150mm"


def own_ids(svg: str, prefix: str) -> str:
    """The svg with its ids made its own, so several can share one page."""
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    for i in ids:
        svg = svg.replace(f'id="{i}"', f'id="{prefix}-{i}"').replace(f"url(#{i})", f"url(#{prefix}-{i})") \
                 .replace(f'href="#{i}"', f'href="#{prefix}-{i}"')
    return svg


CACHE = Path(__file__).resolve().parent.parent / ".maps-cache"


def render(kind: str, file: Path, fit: str, *extra, label: str = "") -> str | None:
    """One render as SVG. A render takes seconds, so it is kept under .maps-cache, keyed by
    the map file, the map drawn under it, the engine and the arguments."""
    under = json.loads(file.read_text()).get("underlay")
    key = hashlib.sha256("\0".join([file.read_text(), (file.parent / under["map"]).read_text() if under else "",
                                    ARTGEN.parent.joinpath("VERSION").read_text(), kind,
                                    fit, *map(str, extra)]).encode()).hexdigest()
    kept = CACHE / f"{key}.svg"
    if kept.exists():
        svg = kept.read_text()
    else:
        svg = render_fresh(kind, file, fit, *extra)
        if svg is None:
            return None
        CACHE.mkdir(exist_ok=True)
        kept.write_text(svg)
    name = re.sub(r"[^\w-]", "-", label or file.stem)
    svg = own_ids(svg, name)
    if label:
        svg = svg.replace("<svg ", f'<svg role="img" aria-label="{label}" ', 1)
    return svg


def render_fresh(kind: str, file: Path, fit: str, *extra) -> str | None:
    with tempfile.TemporaryDirectory() as tmp:
        args = [kind, "render", "--file", file, "--format", "svg", "--fit", fit, "--out", tmp, *extra]
        if kind in ("map", "settlement"):
            args += ["--theme", "color"]
        if artgen(*args).returncode:
            return None
        svgs = sorted(Path(tmp).glob("*.svg"))
        if not svgs:
            return None
        return svgs[0].read_text()


def sheet_rows(setting: Path = tables.SETTING) -> dict[str, dict]:
    """Per region on a sheet, its home row of Sheets.md: sheet, way in and area radius."""
    path = setting / "Sheets.md"
    if not path.exists():
        return {}
    out = {}
    for d in sc.read_tables(path)[0].dicts():
        if d["Area"].startswith("circle"):
            x, y = (float(v) for v in d["Way in"].split(","))
            out[d["Region"]] = {"sheet": d["Sheet"], "x": x, "y": y, "radius": int(d["Area"].split("radius")[1].split()[0])}
    return out


def underlaid(setting: Path = tables.SETTING) -> set[str]:
    """The sheets drawn under a settlement, and so not drawn alone."""
    out = set()
    for code, region in world_for(setting).regions.items():
        for bid in drawn_blocks(region) if ENGINE.get(region.rating.upper()) == "settlement" else ():
            if (f := built(code, bid, setting)[0]) and (under := json.loads(f.read_text()).get("underlay")):
                out.add(Path(under["map"]).stem)
    return out


def sheet_svg(name: str, fit: str = SITE_FIT, setting: Path = tables.SETTING) -> str | None:
    file = setting / f"{name}.json"
    return render("map", file, fit, label=f"Sheet {name}") if file.exists() else None


def region_svg(code: str, fit: str = SITE_FIT, setting: Path = tables.SETTING) -> str | None:
    """A region's map: its home sheet cropped to its area and a margin."""
    row = sheet_rows(setting).get(code)
    file = setting / f"{row['sheet']}.json" if row else None
    if not file or not file.exists():
        return None
    cols, rows = (json.loads(file.read_text())[k] for k in ("cols", "rows"))
    r = row["radius"] + 3
    x0, y0 = max(0, math.floor(row["x"] - r)), max(0, math.floor(row["y"] - r))
    x1, y1 = min(cols, math.ceil(row["x"] + r)), min(rows, math.ceil(row["y"] + r))
    return render("map", file, fit, "--crop", f"{x0},{y0},{x1 - x0},{y1 - y0}cells", label=f"Map of region {code}")


def block_svg(code: str, bid: str, fit: str = SITE_FIT, setting: Path = tables.SETTING) -> str | None:
    file = built(code, bid, setting)[0]
    engine = ENGINE.get(world_for(setting).regions[code].rating.upper(), "dungeon")
    return render(engine, file, fit, label=f"Map of {bid}") if file else None


def cut_svg(loc: str, world, fit: str = SITE_FIT, setting: Path = tables.SETTING) -> str | None:
    """A location's cut: its room and doors from its block's map, or the stretch of its home
    sheet round its mark."""
    code = loc.split(".")[0]
    region = world.regions.get(code)
    if region is None:
        return None
    for bid, block in blocks_of(region).items():
        if loc in [m.strip() for m in str(block.props["locations"]).split(",")]:
            if file := built(code, bid, setting)[0]:
                return render("dungeon", file, fit, "--room", loc, "--margin", "2", label=f"Map of {loc}")
    row = sheet_rows(setting).get(code)
    node = region.locations().get(loc)
    if not row or node is None or (o := offset(node)) is None:
        return None
    file = setting / f"{row['sheet']}.json"
    sheet = json.loads(file.read_text())
    cell = feet(f"{sheet['scale']['perCell']} {dict((v, k) for k, v in UNIT.items())[sheet['scale']['unit']]}")
    px, py = row["x"] + o[0] / cell, row["y"] - o[1] / cell
    if not (0 <= px < sheet["cols"] and 0 <= py < sheet["rows"]):
        return None
    x0, y0 = max(0, min(math.floor(px - 8), sheet["cols"] - 16)), max(0, min(math.floor(py - 8), sheet["rows"] - 16))
    return render("map", file, fit, "--crop", f"{x0},{y0},16,16cells", label=f"Map of {loc}")



def draw(brief_path: Path, setting: Path, out: Path | None, fit: str) -> int:
    world = world_for(setting)
    problems = write_blocks(world)
    if out:
        out.mkdir(parents=True, exist_ok=True)
        put = lambda name, svg: svg and (out / name).write_text(svg)
        for f in sorted(setting.glob("*.json")):
            if f.stem not in underlaid(setting):
                put(f"{f.stem}.svg", sheet_svg(f.stem, fit, setting))
        for code, region in world.regions.items():
            for bid in drawn_blocks(region):
                put(f"{bid}.svg", block_svg(code, bid, fit, setting))
    for p in problems:
        print(f"UNDRAWN: {p}")
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["place", "ground", "pack", "draw"])
    ap.add_argument("region", nargs="?", help="pack: the region code")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--again", action="store_true", help="pack: repack a block already packed")
    ap.add_argument("--brief", type=Path, default=tables.BRIEF)
    ap.add_argument("--setting", type=Path, default=tables.SETTING)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--fit", default=SITE_FIT)
    a = ap.parse_args()
    if a.command == "draw":
        return draw(a.brief, a.setting, a.out, a.fit)
    if a.command == "pack":
        import dungeon
        return dungeon.pack_region(a.region, a.seed, a.again)
    return (place if a.command == "place" else ground)(a.brief, a.setting)


if __name__ == "__main__":
    sys.exit(main())
