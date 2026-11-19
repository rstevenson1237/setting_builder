#!/usr/bin/env python3
"""Maps from the setting's tables, drawn by artgen (tools/artgen).

  python3 tools/maps.py place [--brief PATH] [--setting DIR]
  python3 tools/maps.py ground [--brief PATH] [--setting DIR]
  python3 tools/maps.py draw [--brief PATH] [--setting DIR] [--out DIR] [--fit WxH[mm|px]]

place    Reads BRIEF.md's `sheet` lines and each region's `ground` and `place` lines, puts
         each region's way in on the sheets that list it - centred where no `place` names
         it, and keeping its placed locations on the sheet - gives it an area reaching its
         farthest location, and asks artgen for terrain meeting its ground at the way in
         and at each location, where no other region's ground meets it - on a sheet in
         miles, over one outline round them all, each Route a road through its stops, and
         no snow or desert; on a sheet with a `ground`, that terrain wherever no region's reaches,
         and no river; on a sheet with land=island, one island artgen generates, each region's way
         in on its land and its ground over its share of it, half a square in from the coast. Every location is a keyed mark on its home sheet; one a
         DANGEROUS region opens from is a cave mouth keyed with that region too. Writes
         `setting/[Sheet].json` per sheet and `setting/Sheets.md`, each region's area as its
         outline in Regions.md and a WILD region's ground height as its elevation, and the place
         of each region its sheet or joins now give (tools/space.py settle). A request that cannot be met is reported by its BRIEF.md
         line, and exits 1.
ground   Reads each placed region's ground back from its home sheet and writes its
         `Ground.md`: the region's way in and terrain, the rivers, roads and hills in its
         area, and, once its Locations.md exists, the ground at each location. Run again
         after the locations are written. A location with no bearing and distance, or xyz, from
         the way in is listed and left out.
draw     Builds each block's map, `setting/region/[Code]/[Block].json`, never committed, from its tables - a
         DANGEROUS block's a dungeon, from its approved plan, a SAFE block's a settlement walled round its locations
         on its home sheet, a WILD block's the same unwalled unless it states a wall, with an approved design's streets
         and fabric and any block of another region through its ground - and with --out renders every sheet and block to SVG there.
         A DANGEROUS block's map draws what its rooms hold, and its legend (`furnish`).
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
import space                    # noqa: E402
import tables                   # noqa: E402

ARTGEN = Path(__file__).resolve().parent / "artgen" / "artgen-maps.js"
BUILD = hashlib.sha256(ARTGEN.read_bytes()).hexdigest()   # the build itself: VERSION outlives many builds
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
ISLAND = {**REGIONAL, "land": "island", "sea": 0.55, "moisture": 0.8, "roughness": 0.4, "relief": 0.5, "rivers": 3, "feature": 8}   # a sheet with land=island: the sea round one island
ISLAND_STEP = 2                 # an island's land is read, and shared among its regions, in squares this many to a sheet's square
ISLAND_BLEND = 2                # squares over which a region's ground fades, inside an island's coast
BORDER_WAVE = 0.3              # how far a border between two regions on an island wanders, as a share of their reach
BORDER_WARP = 2.5               # and how far, in squares, the ground is pushed about before it is shared, so no border runs straight
HEADROOM = 1.25                 # the highest ground a sheet draws, over the highest a region's ground asks for
CONTOURS = 20                   # contour lines from sea level to a raised sheet's highest ground
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
        self.ground = str(node.props["ground"]) if "ground" in node.props else None   # wherever no region's ground reaches
        self.land = str(node.props["land"]) if "land" in node.props else None        # island: artgen's coast, the regions within it
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
          spread: dict[str, list[tuple[float, float]]], land: set | None = None) -> list[str]:
    """Positions for sheet.codes, in sheet.at, meeting every request, keeping the areas
    apart and every located place on the sheet - and, given an island's land, its way in,
    its located places and most of its area on it. A region no request names is centred.
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
        if land is not None:
            for code in codes:
                x, y = at[code]
                c += sum(4 for dx, dy in [(0, 0)] + spread.get(code, []) if not on_land(land, x + dx, y + dy))
                c += sum(0.5 for k in range(8) if not on_land(land, x + 0.7 * radius[code] * math.cos(k * math.pi / 4),
                                                              y + 0.7 * radius[code] * math.sin(k * math.pi / 4)))
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
        if land is None and not any(c in (q.code, q.of) for q in requests):
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
    if land is not None:
        out += [f"{c}'s way in is in the sea on {sheet.name}" for c in codes if not on_land(land, *sheet.at[c])]
    return out


def on_land(land: set, x: float, y: float) -> bool:
    """A point of the sheet on an island's land, read in ISLAND_STEP squares."""
    return (math.floor(x * ISLAND_STEP), math.floor(y * ISLAND_STEP)) in land


def land_cells(sheet: Sheet, seed: int) -> set[tuple[int, int]]:
    """The land of an island sheet at a seed, before any region asks for its ground, in ISLAND_STEP squares."""
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / f"{sheet.name}.json"
        base.write_text(json.dumps({"id": sheet.name, "version": 1, "preset": "regional", "seed": seed,
                                    "cols": sheet.cols, "rows": sheet.rows, "gen": dict(ISLAND),
                                    "topo": {"maxElevation": 600, "interval": 50, "majorEvery": 4, "unit": "ft"},
                                    "edits": [], "require": [], "overlay": {"labels": [], "symbols": []}}))
        cells = [(x, y) for y in range(sheet.rows * ISLAND_STEP) for x in range(sheet.cols * ISLAND_STEP)]
        got = facts(base, "--at", *[f"{(x + 0.5) / ISLAND_STEP:g},{(y + 0.5) / ISLAND_STEP:g}" for x, y in cells])["points"]
    return {c for c, p in zip(cells, got) if p["terrain"] not in ("water", "deep")}


def island_areas(sheet: Sheet, land: set, radius: dict, spread: dict, seed: int) -> dict[str, list[float]]:
    """Each region's area on an island, as a poly on the sheet: the land a step in from the coast,
    each square to the region nearest it for its size - from its way in or a located place - along a
    wandering border, its largest piece."""
    inner = {(x, y) for x, y in land if all((x + dx, y + dy) in land for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    codes = [c for c in sheet.codes if radius[c]]
    rng = random.Random(seed)
    wave = {c: [(rng.uniform(-0.6, 0.6), rng.uniform(-0.6, 0.6), rng.uniform(0, 2 * math.pi)) for _ in range(3)] for c in codes}
    warp = [[(rng.uniform(-1, 1) * f, rng.uniform(-1, 1) * f, rng.uniform(0, 2 * math.pi)) for f in (0.15, 0.3, 0.6)] for _ in "xy"]
    reach = {c: [sheet.at[c]] + [(sheet.at[c][0] + dx, sheet.at[c][1] + dy) for dx, dy in spread.get(c, [])] for c in codes}

    def far(c, x, y):
        x, y = (x + BORDER_WARP * sum(math.sin(fx * x + fy * y + ph) / (i + 1) for i, (fx, fy, ph) in enumerate(warp[0])) / 1.8,
                y + BORDER_WARP * sum(math.sin(fx * x + fy * y + ph) / (i + 1) for i, (fx, fy, ph) in enumerate(warp[1])) / 1.8)
        d = min(math.dist((x, y), p) for p in reach[c]) / radius[c]
        return d * (1 + BORDER_WAVE * sum(math.sin(fx * x + fy * y + ph) for fx, fy, ph in wave[c]) / 3)

    own = {c: set() for c in codes}
    for x, y in inner:
        own[min(codes, key=lambda c: far(c, (x + 0.5) / ISLAND_STEP, (y + 0.5) / ISLAND_STEP))].add((x, y))
    out = {}
    for c in codes:
        pieces, left = [], set(own[c])
        while left:
            pieces.append(piece(left, min(left)))
            left -= pieces[-1]
        if pieces:
            most = max(pieces, key=len)
            out[c] = [v / ISLAND_STEP for v in cell_outline(unpinched(most, max(most, key=lambda q: sum(n in most for n in (
                (q[0] + 1, q[1]), (q[0] - 1, q[1]), (q[0], q[1] + 1), (q[0], q[1] - 1))))))]
    return out


def unpinched(cells: set, start: tuple[int, int]) -> set:
    """Cells with no two meeting only at a corner, so their outline is a simple poly: the lesser of
    each such pair is dropped, and what stays joined to start kept."""
    while True:
        pinch = next((((x, y), (x + dx, y + 1)) for x, y in sorted(cells) for dx in (-1, 1)
                      if (x + dx, y + 1) in cells and (x + dx, y) not in cells and (x, y + 1) not in cells), None)
        if pinch is None:
            return cells
        side = lambda q: sum((q[0] + dx, q[1] + dy) in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        drop = min((q for q in pinch if q != start), key=side)
        cells = piece(cells - {drop}, start)


def piece(cells: set, start: tuple[int, int]) -> set:
    """The squares of cells joined edge to edge to start."""
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n in cells and n not in seen:
                seen.add(n)
                todo.append(n)
    return seen


def cell_outline(cells: set) -> list[float]:
    """The outer edge of squares joined edge to edge, as x,y pairs flattened, corners only."""
    edges = {}
    for x, y in cells:
        for a, b, n in (((x, y), (x + 1, y), (x, y - 1)), ((x + 1, y), (x + 1, y + 1), (x + 1, y)),
                        ((x + 1, y + 1), (x, y + 1), (x, y + 1)), ((x, y + 1), (x, y), (x - 1, y))):
            if n not in cells:
                edges.setdefault(a, []).append(b)   # cells unpinched: one edge leaves each corner of the outer ring
    start = min(edges)
    ring, at = [start], edges[start][0]
    while at != start:
        ring.append(at)
        at = edges[at][0]
    n = len(ring)
    keep = [ring[i] for i in range(n) if (ring[i - 1][0] - ring[i][0]) * (ring[(i + 1) % n][1] - ring[i][1])
            != (ring[i - 1][1] - ring[i][1]) * (ring[(i + 1) % n][0] - ring[i][0])]
    return [v for p in keep for v in p]


def artgen(*args) -> subprocess.CompletedProcess:
    """One artgen call. Its output goes through a file: on a pipe, node cuts it at 64 KB."""
    with tempfile.TemporaryFile("w+") as out:
        done = subprocess.run(["node", str(ARTGEN), *map(str, args)], stdout=out, stderr=subprocess.PIPE, text=True)
        out.seek(0)
        return subprocess.CompletedProcess(done.args, done.returncode, out.read(), done.stderr)


def map_file(sheet: Sheet, seed: int, regions: dict, radius: dict, home: dict, spread: dict,
             marks: list[tuple[float, float, str, str]], walled: dict[str, list[float]],
             routes: dict[str, list[list[tuple[float, float]]]], areas: dict[str, list[float]] | None = None) -> dict:
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
        m["gen"] = dict(ISLAND if sheet.land == "island" else REGIONAL)
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
        half = sheet.square / 2                   # a square at least, so its ground can be measured on a sheet in miles
        cx, cy = (w + e) / 2, (n + south) / 2
        w, e = min(w, cx - half), max(e, cx + half)
        n, south = min(n, cy - half), max(south, cy + half)
        poly = [round(v, 2) for p in ((w, n), (e, n), (e, south), (w, south)) for v in (x + p[0] / sheet.square, y + p[1] / sheet.square)]
        if ground:
            m["require"].append({"id": f"{code}-walls", "kind": "terrain", "origin": "tables", "area": {"poly": poly},
                                 "terrain": str(ground.args[0]), "share": WALLED_SHARE})
        m["require"].append({"id": f"{code}-walls-clear", "kind": "clear", "origin": "tables", "area": {"poly": poly}})
    if areas is not None:                         # on an island, each region's ground over its share of the land
        m["require"] += [{"id": f"{code}-ground", "kind": "terrain", "origin": "tables", "terrain": c[4], "area": {"poly": areas[code]},
                          "share": GROUND_SHARE, "blend": ISLAND_BLEND}
                         for c in circles if c[0].endswith("-ground") and (code := c[0][:-len("-ground")]) in areas]
        circles = []
    if not local:                                 # on a sheet in miles, one outline round the way in and every location
        for code in dict.fromkeys(c[0].split("-")[0] for c in circles):   # in the sheet's order: a later one wins
            own = [c for c in circles if c[0].split("-")[0] == code]
            m["require"].append({"id": f"{code}-ground", "kind": "terrain", "origin": "tables", "terrain": own[0][4],
                                 "area": {"poly": hull([(x + LOCATION_GROUND * 2 * math.cos(a * math.pi / 4),
                                                         y + LOCATION_GROUND * 2 * math.sin(a * math.pi / 4))
                                                        for _, x, y, *_ in own for a in range(8)])},
                                 "share": GROUND_SHARE, "blend": BLEND})
        circles = []
    for r in [r for r in m["require"] if r["kind"] == "terrain" and r["id"].endswith("-ground")]:
        ground = next(c for c in regions[r["id"][:-len("-ground")]].children if c.name == "ground")
        if "height" in ground.props:              # its ground's height over the same area, the contours raised to hold it
            low, high = (feet(f"{v} {span.group(3)}") for span in [tables.SPAN_RE.fullmatch(str(ground.props["height"]))]
                         for v in (span.group(1), span.group(2) or span.group(1)))
            m["require"].append({"id": r["id"][:-len("-ground")] + "-height", "kind": "height", "origin": "tables",
                                 "area": r["area"], "low": round(low), "high": round(high), "blend": r.get("blend", BLEND)})
            if not local and high > m["topo"]["maxElevation"]:
                top = math.ceil(high * HEADROOM / 100) * 100
                m["topo"].update(maxElevation=top, interval=max(50, round(top / CONTOURS / 50) * 50), majorEvery=5)
    if sheet.ground:                              # the sheet's ground everywhere, each region's own painted over its area
        whole = {"poly": [0, 0, sheet.cols, 0, sheet.cols, sheet.rows, 0, sheet.rows]}
        m["edits"] = [{"op": "paint", "terrain": sheet.ground, "shape": whole, "origin": "tables"}]
        m["edits"] += [{"op": "paint", "terrain": r["terrain"], "shape": r["area"], "origin": "tables"}
                       for r in m["require"] if r["kind"] == "terrain"]
        m["edits"] += [{"op": "paint", "terrain": c[4], "shape": {"circle": list(c[1:4])}, "origin": "tables"}
                       for c in circles if c[0].endswith("-ground") or not clash(c)]
        m["require"] += [{"id": c[0], "kind": "terrain", "origin": "tables", "area": {"circle": list(c[1:4])},
                          "terrain": c[4], "share": GROUND_SHARE} for c in circles if c[0].endswith("-ground") or not clash(c)]
        m["require"].append({"id": f"{sheet.name}-dry", "kind": "clear", "origin": "tables", "area": whole})
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
            made = build(seed)                       # a map, or a map and what placing it left unmet
            made, placed = made if isinstance(made, tuple) else (made, [])
            fresh.write_text(json.dumps(made, indent=1))
            if kept:
                joined = Path(tmp) / "joined.json"
                built = json.loads(fresh.read_text())    # what sync leaves alone follows the tables too
                joined.write_text(json.dumps({**kept, **{k: v for k, v in built.items() if k not in SYNCED_MAP}}))
                done = artgen("map", "sync", "--file", joined, "--from", fresh, "--origin", "tables")
                if done.returncode:
                    return [f"artgen cannot sync {sheet.name}: {done.stderr.strip() or done.stdout.strip()}"], seed
                fresh = joined
            if sheet.square > LOCAL_SQUARE_FEET and not sheet.ground:
                temper(fresh)
            done = artgen("map", "check", "--file", fresh, "--json")
            report = json.loads(done.stdout) if done.stdout.strip().startswith("{") else None
            if report is None:
                return [f"artgen cannot read {sheet.name}: {(done.stderr or done.stdout).strip()}"], seed
            errors = [f"{e['path']}: {e['message']}" for e in report["errors"]]
            unmet = placed + errors + [r["text"] for r in report["requirements"] if not r["met"]]
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
    unmet, table, outlines = [], [], {}
    for sheet in sheets.values():
        rad = {c: (radius[c] if home[c] == sheet.name else 0) for c in sheet.codes}
        spread = {c: located(world, c, sheet.square) for c in sheet.codes if home[c] == sheet.name}
        area = {c: max([rad[c]] + [math.ceil(math.hypot(*p)) + 1 for p in spread.get(c, [])]) if rad[c] else 0
                for c in sheet.codes}
        asks = [Request(c, p, sheet.square) for c in sheet.codes
                for p in brief.regions[c].children if p.name == "place" and str(p.args[0]) in sheet.codes]
        target = setting / f"{sheet.name}.json"
        if sheet.land != "island":
            unmet += solve(sheet, rad, asks, spread)
        walled = {c: box for c in sheet.codes if home[c] == sheet.name and world and c in world.regions
                  and world.regions[c].rating.upper() == "SAFE"
                  for b in drawn_blocks(world.regions[c]).values() if (box := enclosure(world.regions[c], b)[2])}
        placed = {}

        def build(seed, s=sheet):                       # marks and routes stand where the regions do
            missed, areas = [], None
            if s.land == "island":                      # an island: its regions placed on the land this seed makes
                land = land_cells(s, seed)
                missed = solve(s, rad, asks, spread, land)
                areas = island_areas(s, land, rad, spread, seed)
                placed[seed] = (dict(s.at), areas)
            marks = location_marks(world, s, home) if world else []
            routes = {c: lines for c in s.codes if s.square > LOCAL_SQUARE_FEET and home[c] == s.name
                      and world and c in world.regions and (lines := route_lines(world.regions[c], s))}
            return map_file(s, seed, brief.regions, rad, home, spread, marks, walled, routes, areas), missed

        problems, sheet.seed = draw_sheet(sheet, target, build)
        if sheet.seed in placed:
            sheet.at = placed[sheet.seed][0]
        for p in problems:
            ground = brief.regions.get(p.split("-")[0])
            node = next((c for c in ground.children if c.name == "ground"), None) if ground else None
            unmet.append(f"{'line ' + str(node.line) + ': ' if node else ''}{sheet.name}: {p}")
        for code in sheet.codes:
            x, y = sheet.at[code]
            table.append(f"| {sheet.name} {code} | {sheet.name} | {code} | {x},{y} |")
            if sheet.seed in placed and code in placed[sheet.seed][1]:   # its share of the island, in feet east and north of its way in
                poly = placed[sheet.seed][1][code]
                outlines[code] = "poly " + " ".join(f"{round((px - x) * sheet.square)},{round((y - py) * sheet.square)}"
                                                    for px, py in zip(poly[0::2], poly[1::2]))
            elif area[code]:
                outlines[code] = f"circle {round(area[code] * sheet.square)}"
    title = "Sheets"
    if (reg := setting / "region" / "Regions.md").exists():
        first = reg.read_text().splitlines()[0]
        title = "Sheets of " + first.split(" of ", 1)[1] if " of " in first else title
    (setting / "Sheets.md").write_text(
        f"{title}\n\n| Name | Sheet | Region | Way in |\n|---|---|---|---|\n" + "\n".join(table) + "\n")
    if reg.exists():
        import dungeon
        lines = reg.read_text().split("\n")
        for i, line in enumerate(lines):
            if (m := re.match(r"Region (\S+) ", line)) and m[1] in outlines:
                lines[i] = line = dungeon.with_prop(line, "outline", f'"{outlines[m[1]]}"')
            ground = next((c for c in brief.regions[m[1]].children if c.name == "ground"), None) \
                if m and m[1] in brief.regions else None
            if ground is not None and "height" in ground.props and "rating=WILD" in line:   # the elevation its locations keep to
                lines[i] = dungeon.with_prop(line, "elevation", f'"{ground.props["height"]}"')
        reg.write_text("\n".join(lines))
        space.refresh()
        for line in space.settle():
            print(f"settled {line}")
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


def way(world, a: str, b: str) -> tuple[str, str] | None:
    """Where the way from location a to b runs, as (Compass point, distance): the wall it leaves
    a placed room by and its walk to the next room, else its Connection's bearing and distance."""
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


def way_said(world, a: str, b: str) -> tuple[str | None, list[str]]:
    """Where the way from location a to b leaves a's room, as the referee reads it out, and what follows it: a
    walk to the next room of its block, else its Connection's bearing and distance."""
    region = world.regions.get(a.split(".")[0])
    said, rest = None, []
    if region is not None and region.rating.upper() == "DANGEROUS":
        import dungeon
        if (w := dungeon.walks(region.code).get((a, b))):
            return w[2], [f"{w[1]} feet"]
        said = dungeon.stairs(region.code).get((a, b))
    if (at := way(world, a, b)):
        rest = list(at)
    return said, rest


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
            if (o := space.offset(world.regions[code], node)) is None:
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
        if n.args and (o := space.offset(region, n)) is not None:
            lines.setdefault(str(n.args[0]), [(x, y)]).append((x + o[0] / sheet.square, y - o[1] / sheet.square))
    return [line for line in lines.values() if len(line) > 1]


def located(world, code: str, square: float) -> list[tuple[float, float]]:
    """Each placed location of a region as squares east and south of its way in."""
    region = world.regions.get(code) if world else None
    out = []
    for node in (region.locations().values() if region else []):
        if (o := space.offset(region, node)) is not None:
            out.append((o[0] / square, -o[1] / square))
    return out


def read_only(file: Path, *args) -> subprocess.CompletedProcess:
    """An artgen call that reads a map and changes nothing. Generating the ground takes
    seconds, so the answer is kept under .maps-cache, keyed by the map file and the call."""
    key = hashlib.sha256("\0".join([file.read_text(), BUILD,
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
    gazetteer = sc.parse_regions_gazetteer()
    world = tables.Setting({c: g["rating"] for c, g in gazetteer.items()})
    skipped, off, texts = [], [], {}
    for code, row in sheet_rows(setting).items():
        sheet, radius, x, y = sheets[row["sheet"]], row["radius"], row["x"], row["y"]
        file = setting / f"{sheet.name}.json"
        ring = ",".join(f"{px:.1f},{py:.1f}" for px, py in row.get("area") or [
            (x + radius * math.cos(a * math.pi / 8), y + radius * math.sin(a * math.pi / 8)) for a in range(16)])
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
            o = space.offset(world.regions[code], node)
            if o is None:
                skipped.append(loc)
                continue
            px, py = x + o[0] / cell, y - o[1] / cell
            if 0 <= px < sheet.cols and 0 <= py < sheet.rows:
                spots[loc] = (px, py)
            else:
                off.append(loc)
        got = facts(file, "--at", f"{x:g},{y:g}", *[f"{px:.1f},{py:.1f}" for px, py in spots.values()])["points"]
        lines[0] = lines[0].replace(" ground=", f' height="{round(got[0]["height"])}" ground=', 1)
        for loc, pt in zip(spots, got[1:]):
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
        print("NOTE: no bearing and distance, or xyz, for " + ", ".join(skipped))
    return 0



ENGINE = {"DANGEROUS": "dungeon", "SAFE": "settlement", "WILD": "settlement"}   # the artgen engine a rating's blocks draw with



def blocks_of(region) -> dict[str, kdl.Node]:
    return {str(n.args[0]): n for n in region.files.get("Blocks", []) if n.args and n.name == "Block"}


def designed(region) -> set[str]:
    """The blocks of a region whose design the user has approved: their places come from step 3e."""
    return {str(n.args[0]) for n in region.files.get("Design", []) if n.name == "Design" and n.args and n.props.get("approved")}


def drawn_blocks(region) -> dict[str, kdl.Node]:
    """The blocks drawn for a region: a DANGEROUS region's as dungeons, a SAFE or WILD region's
    as settlements. Region and location maps are paused."""
    return blocks_of(region) if region.rating.upper() in ENGINE else {}


def block_file(region, block: kdl.Node) -> tuple[dict | None, list[str]]:
    """The artgen file for one block, by its region's rating, and what the tables leave it
    unable to draw."""
    if region.rating.upper() == "DANGEROUS":
        import plan
        if str(block.args[0]) in designed(region) & set(plan.plans_of(region)):
            m, problems = plan.block_map(region, block)
            if m is not None:
                furnish(region, m)
            return m, problems
        return None, []                                  # no approved plan yet: tools/design.py reports it
    return settlement_map(region, block)



# -- blocks: a SAFE region's enclosure, its buildings where its locations stand ----------

TOWN_CELLS = (5, 10, 20)        # feet to a settlement's cell, the finest that fits
MAX_TOWN = 240                  # cells across a settlement, artgen's limit
TOWN_EDGE = 12                  # cells of ground beyond the wall
WALL_GAP = 15                   # feet between the wall and the buildings it encloses
BUILDING = {"Inn": "inn", "Merchant": "shop", "Bank": "shop", "Authority": "hall"}
MYSTERY_MARK = {"Altar": "altar", "Statue": "statue", "Fountain": "fountain", "Throne": "throne"}   # a type with none draws none
HAZARD_MARK = {"Pit": "pit", "Water": "pool", "Fire/Lava": "fire", "Broken/Weak Floor": "rubble", "Ravine/Climb": "pit",
               **dict.fromkeys(("Mechanical", "Spike", "Dart", "Hammer", "Gas", "Runes", "Field", "Attack"), "trap")}
CONTAINER_MARK = {"coffin": "coffin", "sarcophag": "coffin", "tomb": "coffin", "barrel": "barrel", "crate": "crate",
                  "bones": "bones", "skull": "bones"}   # a word in a Reward's container, else a chest
NAMED = {"Chapel": "chapel", "Temple": "temple", "Shrine": "chapel", "Forge": "smithy", "Smithy": "smithy",
         "Barracks": "barracks", "Hall": "hall", "Tavern": "tavern", "Stable": "stable", "Mill": "mill",
         "Tower": "tower", "Keep": "keep", "Warehouse": "warehouse", "Manor": "manor"}   # a word in its name, over its type
WALL = ("palisade", "fence", "hedge", "drystone", "ruined")   # a word in the Block's wall, else a curtain
POSTERN = 10                    # feet: a Gate narrower than this is a postern, else a gatehouse
VOID_GROUND = "yard"            # the area a Void is drawn as: open ground, with nothing standing on it
WILD_PLACE = {"Gardens": ("area", "garden"), "Shore": ("water", "lake")}   # a word in a WILD name, over its type
BUILDING_KINDS = ("house", "cottage", "shop", "inn", "tavern", "smithy", "temple", "chapel", "hall", "barn", "stable", "mill",
                  "warehouse", "keep", "tower", "gatehouse", "barracks", "manor", "ruin")   # artgen's settlement buildings
GHOST = "square"                # the area another region's block is drawn as where it breaks this one's ground
TOWN_GROUND = {"sand": "sand", "desert": "sand", "rock": "stone", "snow": "snow"}   # a settlement's ground by its region's terrain
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
        if (o := space.offset(region, node)) is None:
            problems.append(f"{c} states no bearing and distance, or xyz")
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


@functools.lru_cache(maxsize=None)
def breaking(code: str) -> list[tuple[str, list[tuple[float, float]]]]:
    """Each block of another region that stands through this region's ground - its floor below the way in, its roof
    above, inside its outline - and its outline in feet east and north of the way in."""
    sp = space.settled()
    me = sp.things.get(code)
    here = sp.absolute(me) if me else [None]
    if None in here:
        return []
    out = []
    for t in sp.things.values():
        if t.kind != "block" or t.region == code or t.outline is None or None in (at := sp.absolute(t)):
            continue
        floor, roof = sp.reach(t)
        poly = space.polygon(t.outline, at[0] - here[0], at[1] - here[1])
        if at[2] + floor < here[2] < at[2] + roof and space.meets(poly, space.polygon(me.outline, 0.0, 0.0)):
            out.append((t.code, poly))
    return out


def region_ground(code: str) -> str | None:
    """The terrain a region's BRIEF.md `ground` line asks for."""
    node = tables.Brief(tables.Schema()).regions.get(code)
    ground = next((c for c in node.children if c.name == "ground"), None) if node else None
    return str(ground.args[0]) if ground and ground.args else None


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
         "ground": TOWN_GROUND.get(region_ground(code), "grass"), "grid": {"show": True, "size": 2, "sub": False},
         "scale": {"perCell": step, "unit": "ft"}, "numbers": False, "scaleBar": True, "compass": True,
         "furniture": {"place": "outside"}, "roads": [], "water": [], "walls": [wall] if walled else [], "buildings": [], "areas": [], "trees": [],
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
                               "label": c, "origin": "tables"})
    for v in (n for n in region.files.get("Blocks", []) if n.name == "Void" and n.args and str(n.args[0]) == bid):
        centre = space.point_of(v.props.get("xyz")) or [0.0, 0.0]
        if shape := space.outline_value(v.props.get("outline")):   # open ground: nothing stands on it
            m["areas"].append({"kind": VOID_GROUND, "points": [c for x, y in space.polygon(shape, centre[0], centre[1])
                                                              for c in cell(x, -y)],
                               "label": str(v.props.get("what", "")), "origin": "tables"})
    clear, kept = dict(at), dict(size)                    # what fabric keeps clear of
    for b, poly in breaking(code):                        # another region's block standing through this one's ground
        m["areas"].append({"kind": GHOST, "points": [v for x, y in poly for v in cell(x, -y)], "origin": "tables"})
        xs, ys = [x for x, _ in poly], [-y for _, y in poly]
        clear[b], kept[b] = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2), (max(xs) - min(xs), max(ys) - min(ys))
        x, y = cell(*clear[b])
        m["overlay"]["labels"].append({"text": b, "x": x, "y": y, "kind": "name", "origin": "tables"})
    streets = design_streets(region, bid, at)
    for kind, line in streets:                            # an approved design's streets, as its seed laid them
        m["roads"].append({"kind": kind, "points": [v for p in line for v in cell(*p)], "origin": "tables"})
    for i, b in enumerate(fabric(region, bid, clear, kept, streets)):   # and what stands between its places
        (x, y), w, h = cell(b["x"] - b["w"] / 2, b["y"] - b["h"] / 2), b["w"] / step, b["h"] / step
        if 0 <= x and x + w <= cols and 0 <= y and y + h <= rows:
            m["buildings"].append({"id": f"fabric-{i + 1}", "kind": b["kind"], "shape": "rect", "x": x, "y": y, "w": round(w, 1), "h": round(h, 1),
                                   "angle": b["angle"], "number": False, "origin": "tables"})
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


FABRIC_LOT = 30                 # feet of street front each fabric building is given
FABRIC_SIZE = (15, 25)          # feet: the least and most a fabric building's side
STREET_HALF = 10                # feet from a street's middle to its edge
SETBACK = 5                     # feet from a street's edge to the fabric along it
KEEP_CLEAR = 10                 # feet kept clear round each location


def design_layout(region, bid: str):
    """An approved SAFE or WILD design laid out at its seed: its graph and artgen's settlement file, kept under
    .maps-cache. None where the block has no approved design."""
    import design
    g = design.groups(region).get(bid)
    if not g or not g["design"].props.get("approved") or "seed" not in g["design"].props:
        return None, None
    st = design.Settle(region, bid)
    if st.graph is None:
        return None, None
    seed = int(g["design"].props["seed"])
    kept = CACHE / (hashlib.sha256((json.dumps(st.graph, sort_keys=True) + BUILD + str(seed)).encode()).hexdigest() + ".layout.json")
    if not kept.exists():
        with tempfile.TemporaryDirectory() as tmp:
            if isinstance(st.run(seed, Path(tmp)), str):
                return st, None
            CACHE.mkdir(exist_ok=True)
            kept.write_text((Path(tmp) / f"seed-{seed}.json").read_text())
    return st, json.loads(kept.read_text())


def design_streets(region, bid: str, at: dict) -> list[tuple[str, list[tuple[float, float]]]]:
    """Each street of a block's approved design, as its seed laid it: its kind, and its points in feet east and south
    of the way in, the frame `at` holds each location's place in."""
    st, f = design_layout(region, bid)
    first = st.locations[0] if st else None
    b = next((b for b in (f or {}).get("buildings", []) if b.get("id") == str(first).replace(".", "-")), None)
    if b is None or first not in at:
        return []
    k = f["scale"]["perCell"]
    cx, cy = b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
    return [(r.get("kind", "street"), [(at[first][0] + (r["points"][i] - cx) * k, at[first][1] + (r["points"][i + 1] - cy) * k)
                                       for i in range(0, len(r["points"]), 2)])
            for r in f["roads"] if r.get("origin") == "graph"]


def fabric(region, bid: str, at: dict, size: dict, streets: list) -> list[dict]:
    """The unkeyed buildings a design's `Fabric` lines stand along its streets: on each side of each street, a lot every
    FABRIC_LOT feet, built on at the line's share, from the design's seed, clear of every location and street. Each is
    its kind, its centre in feet east and south of the way in, its size, and its angle along the street."""
    import design
    g = design.groups(region).get(bid)
    lines = [n for n in (g["lines"] if g and g["design"].props.get("approved") else []) if n.name == "Fabric"]
    rng = random.Random(int(g["design"].props.get("seed", 1)) if g else 1)
    segs = [(a, b) for _, line in streets for a, b in zip(line, line[1:]) if a != b]
    near = lambda p, a, b: math.dist(p, (a[0] + (t := max(0.0, min(1.0, ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1]))
                                                                  / math.dist(a, b) ** 2))) * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    out = []
    for n in lines:
        share = float(str(n.props.get("share", "0%")).rstrip("%")) / 100
        for a, b in segs:
            run, ux, uy = math.dist(a, b), (b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b)
            for i in range(int(run // FABRIC_LOT)):
                for side in (-1, 1):
                    if rng.random() >= share:
                        continue
                    w, h = (rng.uniform(*FABRIC_SIZE) for _ in range(2))
                    d, back = (i + 0.5) * FABRIC_LOT, side * (STREET_HALF + SETBACK + h / 2)
                    c = (a[0] + ux * d - uy * back, a[1] + uy * d + ux * back)
                    r = math.hypot(w, h) / 2
                    if any(near(c, p, q) < STREET_HALF + r - 1 for p, q in segs) \
                            or any(abs(c[0] - at[k][0]) < size[k][0] / 2 + r + KEEP_CLEAR and abs(c[1] - at[k][1]) < size[k][1] / 2 + r + KEEP_CLEAR for k in at) \
                            or any(math.dist(c, (o["x"], o["y"])) < r + math.hypot(o["w"], o["h"]) / 2 for o in out):
                        continue
                    out.append({"kind": str(n.props.get("kind", "house")), "x": c[0], "y": c[1], "w": w, "h": h,
                                "angle": round(math.degrees(math.atan2(uy, ux)), 1)})
    return out


# -- what a DANGEROUS room holds, drawn where it stands ------------------------------------
# A place in a room is a part of it (`at`), a wall it stands against (`against`), or both: toward that end of the wall.
# Map cells run east in x and south in y.

TOWARD = {"north": (0, -1), "north-east": (1, -1), "east": (1, 0), "south-east": (1, 1),
          "south": (0, 1), "south-west": (-1, 1), "west": (-1, 0), "north-west": (-1, -1)}
SIDE_WORD = {"n": "north", "e": "east", "s": "south", "w": "west"}
CURVED = ("circle", "cave")     # a room with no straight walls, so no wall ends
CLEAR = 1.6                     # cells between two symbols, or a symbol and a stair or door
INSET = 1.0                     # cells from a wall to a symbol against it
LABEL_ROOM = 6                  # cells: a room no wider keeps its centre for its code


def place_said(at: str | None, against: str | None, shape: str = "rect") -> str:
    """A stated place in a room, as the referee reads it out."""
    if against and at:
        return f"against the {at} end of the {against} wall"
    if against:
        return f"in the {against} corner" if "-" in against and shape == "rect" else f"against the {against} wall"
    return "in the centre of the room" if at == "centre" else f"in the {at} part of the room"


def place_fault(at: str | None, against: str | None, shape: str = "rect") -> str | None:
    """Why a stated place has no single spelling, or None: with `against`, `at` is a point along that wall, and a
    corner or a curved room has no ends."""
    if not (at and against):
        return None
    if "-" in against or shape in CURVED:
        what = "corner" if "-" in against and shape == "rect" else "wall"
        return f"the {against} {what} of {'an' if shape[0] in 'aeiou' else 'a'} {shape} room has no ends: state `against` alone"
    ends = ("west", "east") if against in ("north", "south") else ("north", "south")
    return None if at in ends else f"the {against} wall's ends are {' and '.join(ends)}"


def wall_said(shape: str, box: dict, point, side: str | None = None, verb: str = "in") -> str:
    """Where a door or stair stands on its room's wall: a side of the room's box, and the end of it where it stands
    in an outer third of a wall at least 30 feet long; on a wall off the box, its compass point from the centre."""
    x, y = point
    near = {"w": abs(x - box["x"]), "e": abs(x - box["x"] - box["w"]), "n": abs(y - box["y"]), "s": abs(y - box["y"] - box["h"])}
    side = side or next((s for s, d in near.items() if d < 0.3), None)
    if side is None or shape in CURVED:
        cx, cy = box["x"] + box["w"] / 2, box["y"] + box["h"] / 2
        word = space.compass()[round(math.degrees(math.atan2(x - cx, cy - y)) % 360 / 45) * 2 % 16]
        return f"{verb} the {word} wall"
    along, length, start = (x, box["w"], box["x"]) if side in "ns" else (y, box["h"], box["y"])
    ends = ("west", "east") if side in "ns" else ("north", "south")
    t = (along - start) / length if length else 0.5
    end = ends[0] if t < 1 / 3 else ends[1] if t > 2 / 3 else None
    wall = f"the {SIDE_WORD[side]} wall"
    return f"{verb} the {end} end of {wall}" if end and length >= 6 else f"{verb} {wall}"


def spot(room: dict, at: str | None, against: str | None) -> tuple[float, float]:
    """A stated place as a point in a room drawn on a map file, kept on its floor."""
    x0, y0, w, h = room["x"], room["y"], room["w"], room["h"]
    cx, cy = x0 + w / 2, y0 + h / 2
    if against:
        dx, dy = TOWARD[against]
        if room["shape"] in CURVED or (room["shape"] != "rect" and dx and dy):
            k = math.hypot(dx, dy)
            px, py = cx + dx / k * (w / 2 - INSET), cy + dy / k * (h / 2 - INSET)
        else:
            inset_x, inset_y = min(INSET, w / 2), min(INSET, h / 2)
            px = cx + dx * (w / 2 - inset_x) if dx else cx
            py = cy + dy * (h / 2 - inset_y) if dy else cy
            if at:
                ax, ay = TOWARD[at]
                px, py = px + ax * w * 0.3, py + ay * h * 0.3
    elif at and at != "centre":
        dx, dy = TOWARD[at]
        inset = 0.34 if room["shape"] == "rect" else 0.30
        px, py = cx + dx * w * inset, cy + dy * h * inset
    else:
        px, py = cx, cy
    if w <= 2 or h <= 2:                                  # a room one passage wide: along its middle
        px, py = (cx, py) if w <= 2 else (px, cy)
    if pts := room.get("points"):
        poly = list(zip(pts[::2], pts[1::2]))
        for _ in range(10):                              # drawn back toward the centre until on the floor
            if space.inside((px, py), poly, 0.8):
                break
            px, py = px + (cx - px) * 0.25, py + (cy - py) * 0.25
    return round(px, 2), round(py, 2)


def held(region) -> dict[str, list[kdl.Node]]:
    """Each location's Mysteries, Hazards and Rewards, as its tables give them."""
    out: dict[str, list[kdl.Node]] = {}
    for n in region.files.get("Challenges", []) + region.files.get("Rewards", []):
        if n.args and n.name in ("Mystery", "Hazard", "Reward"):
            out.setdefault(str(n.args[0]), []).append(n)
    return out


def mark_of(n: kdl.Node) -> str | None:
    if n.name == "Mystery":
        return MYSTERY_MARK.get(str(n.props.get("type")))
    if n.name == "Hazard":
        return HAZARD_MARK.get(str(n.props.get("type")))
    words = str(n.props.get("container", "")).lower()
    return next((v for k, v in CONTAINER_MARK.items() if k in words), "chest")


def furnish(region, m: dict) -> None:
    """A DANGEROUS block's map with what its rooms hold: a trap at the door of each way holding a Hazard, then each
    Mystery, Hazard and Reward as the symbol its type names - where its `at` and `against` say, else a Mystery nearest
    the centre, a Hazard by the nearest door and a Reward farthest from every door, each clear of the rest and of a
    small room's code - and the legend. A room with no place left for one draws none."""
    import dungeon
    f = dungeon.engine("facts", m)
    rooms = {r["label"]: r for r in m["rooms"]}
    rid = {r["id"]: r["label"] for r in m["rooms"]}
    doors: dict[str, list] = {c: [] for c in rooms}
    taken: dict[str, list] = {c: [] for c in rooms}
    door_to: dict[tuple[str, str], tuple[float, float]] = {}
    for r in f.get("rooms", []):
        for d in r.get("doors", []):
            doors[r["label"]].append(tuple(d["at"]))
            if d.get("to") in rid:
                door_to.setdefault((r["label"], rid[d["to"]]), tuple(d["at"]))
        for e in r.get("exits") or []:
            taken[r["label"]].append(tuple(e["at"]))
            if (far := re.search(r"to (\S+)", e.get("text", ""))):
                door_to.setdefault((r["label"], far[1]), tuple(e["at"]))
    for x in m.get("connections", []):
        a, b = rid.get(x["a"]), rid.get(x["b"])
        if a and b:
            doors[a].append(tuple(x["at"]))
            doors[b].append(tuple(x["at"]))
            door_to.setdefault((a, b), tuple(x["at"]))
            door_to.setdefault((b, a), tuple(x["at"]))
    symbols = m["overlay"]["symbols"]
    for n in region.files.get("Connections", []):          # a trap on a way: inside its room, by its door
        a, b = (str(n.args[0]), str(n.props.get("to"))) if n.args else ("", "")
        if a in rooms and (door := door_to.get((a, b))) and any(k.name == "Hazard" for k in n.children):
            r = rooms[a]
            cx, cy = r["x"] + r["w"] / 2, r["y"] + r["h"] / 2
            k = math.dist(door, (cx, cy)) or 1
            p = (round(door[0] + (cx - door[0]) / k * CLEAR, 2), round(door[1] + (cy - door[1]) / k * CLEAR, 2))
            symbols.append({"kind": "trap", "x": p[0], "y": p[1], "origin": "tables"})
            taken[a].append(p)
    for code, items in held(region).items():
        r = rooms.get(code)
        if r is None:
            continue
        if min(r["w"], r["h"]) <= LABEL_ROOM:              # a small room's centre is its code's
            taken[code].append((r["x"] + r["w"] / 2, r["y"] + r["h"] / 2))
        stated = [n for n in items if "at" in n.props or "against" in n.props]
        ruled = sorted((n for n in items if n not in stated), key=lambda n: ("Mystery", "Hazard", "Reward").index(n.name))
        for n in stated:
            if kind := mark_of(n):
                p = spot(r, n.props.get("at"), n.props.get("against"))
                symbols.append({"kind": kind, "x": p[0], "y": p[1], "origin": "tables"})
                taken[code].append(p)
        slots = [spot(r, at, None) for at in ["centre", *TOWARD]]
        near = lambda p: min((math.dist(p, d) for d in doors[code]), default=0)
        for n in ruled:
            kind = mark_of(n)
            free = [p for p in dict.fromkeys(slots) if all(math.dist(p, q) >= CLEAR for q in taken[code] + doors[code])]
            if not kind or not free:
                continue
            if n.name == "Mystery":
                p = min(free, key=lambda p: math.dist(p, slots[0]))
            elif n.name == "Hazard":
                p = min(free, key=lambda p: (near(p), p == slots[0]))
            else:
                p = max([q for q in free if q != slots[0]] or free, key=near)
            symbols.append({"kind": kind, "x": p[0], "y": p[1], "origin": "tables"})
            taken[code].append(p)
    m["legend"] = True


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
    target, text = region.dir / f"{bid}.json", json.dumps(m, indent=1)
    if not target.exists() or target.read_text() != text:
        target.write_text(text)
    return target, tuple(problems)


def clutter(m: dict) -> list[str]:
    """What a block's map file draws twice or lays over its ground: a number badge beside a
    code, or scale, compass and title standing on the map."""
    out = []
    if (m.get("furniture") or {}).get("place") != "outside":
        out.append("the scale and compass stand on the map, not outside it")
    if m.get("numbers") is not False or any(r.get("number") not in (None, False) for r in m.get("rooms", []) + m.get("buildings", [])):
        out.append("a number badge sits beside the code that labels it")
    return out


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
            out += [f"{bid}: {d}" for d in clutter(json.loads(target.read_text()))]
            done = artgen(engine, "check", "--file", target, "--json")
            for e in json.loads(done.stdout).get("errors", []) if done.stdout.startswith("{") else []:
                out.append(f"{bid}: {e['path']}: {e['message']}")
            if engine == "dungeon":
                out += [f"{bid}: {d}" for level, d in dungeon.defects(region, block, json.loads(target.read_text())) if level == "error"]
                with tempfile.TemporaryDirectory() as tmp:
                    shown = artgen("dungeon", "render", "--file", fitted(target, BLOCK_FIT, tmp), "--format", "svg", "--fit", BLOCK_FIT,
                                   "--json", "--out", tmp)
                    for left in json.loads(shown.stdout).get("unplaced", []) if shown.stdout.startswith("{") else []:
                        out.append(f"{bid}: the note {left['text']!r} found no room on the page")
    return out


# -- renders --------------------------------------------------------------------

SITE_FIT = "720x560px"
BLOCK_FIT = "880x680px"         # a block's map on the site: the page's width, room for its codes and its legend
PDF_FIT = "110x150mm"


def own_ids(svg: str, prefix: str) -> str:
    """The svg with its ids made its own, so several can share one page."""
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    for i in ids:
        svg = svg.replace(f'id="{i}"', f'id="{prefix}-{i}"').replace(f"url(#{i})", f"url(#{prefix}-{i})") \
                 .replace(f'href="#{i}"', f'href="#{prefix}-{i}"')
    return svg


CACHE = Path(__file__).resolve().parent.parent / ".maps-cache"


def furniture_outside(svg: str) -> str:
    """A terrain map with its legend, scale bar and compass in a band under it. The map engine
    draws them over the ground and has no setting to put them elsewhere, as the dungeon and
    settlement engines do."""
    vb = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"', svg)
    if not vb:
        return svg
    x0, y0, w, h = map(float, vb.groups())
    found = []                                              # (name, start, end) of each top-level furniture group
    for name in ("legend", "scale", "compass"):
        if not (m := re.search(rf'<g id="{name}"[ >]', svg)):
            continue
        depth, at = 0, m.start()
        for t in re.finditer(r"<g[ >]|</g>", svg[at:]):
            depth += 1 if t.group().startswith("<g") else -1
            if not depth:
                found.append((name, at, at + t.end()))
                break
    if not found:
        return svg
    box = {}                                                # name -> (left, top, width, height)
    for name, a, b in found:
        part = svg[a:b]
        if name == "compass":
            c = re.search(r'<circle cx="([-\d.]+)" cy="([-\d.]+)" r="([-\d.]+)"', part)
            n = re.search(r'<text x="[-\d.]+" y="([-\d.]+)" font-size="([-\d.]+)"', part)
            cx, cy, r = map(float, c.groups())
            top = float(n.group(1)) - float(n.group(2))
            box[name] = (cx - r, top, 2 * r, cy + r - top)
        else:
            r = re.search(r'<rect x="([-\d.]+)" y="([-\d.]+)" width="([-\d.]+)" height="([-\d.]+)"', part)
            box[name] = tuple(map(float, r.groups()))
    pad = box["scale"][0] - x0 if "scale" in box else 12 * w / 560
    band = max(b[3] for b in box.values()) + 2 * pad
    paper = re.search(r'<rect [^>]*fill="(#[0-9a-f]+)"', svg[found[0][1]:]).group(1)
    left = {"scale": x0 + pad, "legend": x0 + w - pad - box.get("legend", (0, 0, 0))[2]}
    if "compass" in box:
        free = [left["scale"] + box["scale"][2] if "scale" in box else x0 + pad, left["legend"] if "legend" in box else x0 + w - pad]
        left["compass"] = (free[0] + free[1] - box["compass"][2]) / 2
    moved = "".join(f'<g transform="translate({left[n] - box[n][0]:.1f} {y0 + h + pad - box[n][1]:.1f})">{svg[a:b]}</g>'
                    for n, a, b in found)
    for _, a, b in sorted(found, reverse=True, key=lambda f: f[1]):
        svg = svg[:a] + svg[b:]
    ink = re.search(r'stroke="(#[0-9a-f]+)"', moved).group(1)
    strip = (f'<rect x="{x0}" y="{y0 + h}" width="{w}" height="{band:.1f}" fill="{paper}"/>'
             f'<path d="M{x0} {y0 + h}h{w}" stroke="{ink}" stroke-width="1.5"/>')
    svg = svg.replace("</svg>", strip + moved + "</svg>")
    svg = svg.replace(vb.group(0), f'viewBox="{x0:g} {y0:g} {w:g} {h + band:.1f}"', 1)
    return re.sub(r'(<svg [^>]*?\bheight=")([\d.]+)', lambda m: f"{m.group(1)}{float(m.group(2)) * (h + band) / h:.1f}", svg, 1)


def render(kind: str, file: Path, fit: str, *extra, label: str = "") -> str | None:
    """One render as SVG. A render takes seconds, so it is kept under .maps-cache, keyed by
    the map file, the map drawn under it, the engine and the arguments."""
    under = json.loads(file.read_text()).get("underlay")
    key = hashlib.sha256("\0".join([file.read_text(), (file.parent / under["map"]).read_text() if under else "",
                                    BUILD, kind, str(theme(kind)),
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
    if kind == "map":
        svg = furniture_outside(svg)
    name = re.sub(r"[^\w-]", "-", label or file.stem)
    svg = own_ids(svg, name)
    if label:
        svg = svg.replace("<svg ", f'<svg role="img" aria-label="{label}" ', 1)
    return svg


def look(kind: str, path: Path | None = None) -> dict[str, str]:
    """What BRIEF.md's `maps` node says of how every map of a kind is drawn - dungeon,
    settlement or terrain - and nothing for a key it leaves out."""
    path = path or tables.BRIEF
    return tables.read_looks(path)[0].get(kind, {}) if path.exists() else {}


def theme(kind: str) -> str | None:
    """The theme a sheet (kind `map`) or settlement is drawn in, None for a dungeon."""
    return look({"map": "terrain", "settlement": "settlement"}[kind]).get("theme", "color") if kind in ("map", "settlement") else None


def fitted(file: Path, fit: str, tmp: str) -> Path:
    """A dungeon file with its band of scale and legend on the side that leaves its map largest in the fit box:
    beside a map narrower than the box, below one wider."""
    m = json.loads(file.read_text())
    if (m.get("furniture") or {}).get("place") != "outside" or "cols" not in m:
        return file
    w, h = (float(v) for v in re.findall(r"[\d.]+", fit)[:2])
    beside = m["cols"] / m["rows"] < w / h and fit.endswith("px")   # a band beside a map in mm draws no map (artgen 0.14)
    m["furniture"]["side"] = "right" if beside else "bottom"
    (out := Path(tmp) / "fitted" / file.name).parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(m))
    return out


def render_fresh(kind: str, file: Path, fit: str, *extra) -> str | None:
    with tempfile.TemporaryDirectory() as tmp:
        file = fitted(file, fit, tmp) if kind == "dungeon" else file
        args = [kind, "render", "--file", file, "--format", "svg", "--fit", fit, "--out", tmp, *extra]
        if t := theme(kind):
            args += ["--theme", t]
        if artgen(*args).returncode:
            return None
        svgs = sorted(Path(tmp).glob("*.svg"))
        if not svgs:
            return None
        return svgs[0].read_text()


def sheet_rows(setting: Path = tables.SETTING) -> dict[str, dict]:
    """Per region on a sheet, its home row of Sheets.md - the finest sheet listing it - with its
    way in there and the radius of its Region's outline, in squares, and a poly outline's corners on the sheet."""
    path = setting / "Sheets.md"
    if not path.exists():
        return {}
    squares = {n: Sheet(n, node).square for n, node in tables.Brief(tables.Schema()).sheets.items()}
    outline = {str(n.args[0]): space.outline_value(n.props.get("outline")) for n in tables.gazetteer() if n.args}
    out = {}
    for d in sc.read_tables(path)[0].dicts():
        code, sheet = d["Region"], d["Sheet"]
        shape = outline.get(code)
        if sheet not in squares or not shape or shape[0] not in ("circle", "poly"):
            continue
        if code not in out or squares[sheet] < squares[out[code]["sheet"]]:
            x, y, sq = *(float(v) for v in d["Way in"].split(",")), squares[sheet]
            if shape[0] == "circle":
                out[code] = {"sheet": sheet, "x": x, "y": y, "radius": round(shape[1] / sq)}
            else:
                out[code] = {"sheet": sheet, "x": x, "y": y, "radius": math.ceil(max(math.hypot(*q) for q in shape[1]) / sq),
                             "area": [(x + e / sq, y - n / sq) for e, n in shape[1]]}
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


def block_svg(code: str, bid: str, fit: str = BLOCK_FIT, setting: Path = tables.SETTING) -> str | None:
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
            if file := built(code, bid, setting)[0]:          # the room and its parts, labelled with its code and a letter
                parts = [r["label"] for r in json.loads(file.read_text()).get("rooms", [])
                         if re.fullmatch(re.escape(loc) + "[a-z]", str(r.get("label", "")))]
                return render("dungeon", file, fit, *[a for x in [loc] + parts for a in ("--room", x)], "--margin", "2",
                              label=f"Map of {loc}")
    row = sheet_rows(setting).get(code)
    node = region.locations().get(loc)
    if not row or node is None or (o := space.offset(region, node)) is None:
        return None
    file = setting / f"{row['sheet']}.json"
    sheet = json.loads(file.read_text())
    cell = feet(f"{sheet['scale']['perCell']} {dict((v, k) for k, v in UNIT.items())[sheet['scale']['unit']]}")
    px, py = row["x"] + o[0] / cell, row["y"] - o[1] / cell
    if not (0 <= px < sheet["cols"] and 0 <= py < sheet["rows"]):
        return None
    x0, y0 = max(0, min(math.floor(px - 8), sheet["cols"] - 16)), max(0, min(math.floor(py - 8), sheet["rows"] - 16))
    return render("map", file, fit, "--crop", f"{x0},{y0},16,16cells", label=f"Map of {loc}")



def draw(brief_path: Path, setting: Path, out: Path | None, fit: str | None) -> int:
    world = world_for(setting)
    problems = write_blocks(world)
    if out:
        out.mkdir(parents=True, exist_ok=True)
        put = lambda name, svg: svg and (out / name).write_text(svg)
        for f in sorted(setting.glob("*.json")):
            if f.stem not in underlaid(setting):
                put(f"{f.stem}.svg", sheet_svg(f.stem, fit or SITE_FIT, setting))
        for code, region in world.regions.items():
            for bid in drawn_blocks(region):
                put(f"{bid}.svg", block_svg(code, bid, fit or BLOCK_FIT, setting))
    for p in problems:
        print(f"UNDRAWN: {p}")
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["place", "ground", "draw"])
    ap.add_argument("--brief", type=Path, default=tables.BRIEF)
    ap.add_argument("--setting", type=Path, default=tables.SETTING)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--fit", help=f"default {SITE_FIT} a sheet, {BLOCK_FIT} a block")
    a = ap.parse_args()
    if a.command == "draw":
        return draw(a.brief, a.setting, a.out, a.fit)
    return (place if a.command == "place" else ground)(a.brief, a.setting)


if __name__ == "__main__":
    sys.exit(main())
