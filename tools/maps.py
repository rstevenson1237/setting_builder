#!/usr/bin/env python3
"""Maps from the setting's tables, drawn by artgen (tools/artgen).

  python3 tools/maps.py place [--brief PATH] [--setting DIR]
  python3 tools/maps.py ground [--brief PATH] [--setting DIR]

place    Reads BRIEF.md's `sheet` lines and each region's `ground` and `place` lines, puts
         each region's way in on the sheets that list it, gives it an area, and asks artgen
         for terrain meeting the ground each area requires. Writes `setting/[Sheet].json`
         per sheet and `setting/Sheets.md`. A request that cannot be met is reported by its
         BRIEF.md line, and exits 1.
ground   Reads each placed region's ground back from its home sheet and writes its
         `Ground.md`: the region's way in and terrain, the rivers, roads and hills in its
         area, and, once its Locations.md exists, the ground at each location. Run again
         after the locations are written. A location with no bearing and distance, or north
         and east, from the way in is listed and left out.
"""
from __future__ import annotations

import argparse
import json
import math
import random
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
SQUARES_PER_LOCATION = 4        # the ground one location needs, in squares
GROUND_SHARE = 0.8              # the share of its area a region's ground must cover
SEPARATION = 0.6                # two areas' centres lie at least this much of their radii apart
BEARING_SLACK = 15              # degrees either side of a compass point
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

    def said(self, a, b) -> str:
        dx, dy = a[0] - b[0], a[1] - b[1]
        return f"{math.hypot(dx, dy):.1f} squares at {math.degrees(math.atan2(dx, -dy)) % 360:.0f} degrees"


def solve(sheet: Sheet, radius: dict[str, float], requests: list[Request]) -> list[str]:
    """Positions for sheet.codes, in sheet.at, meeting every request and keeping the areas
    apart. Returns what is unmet, empty when all is met."""
    rng = random.Random(1)
    codes = sheet.codes

    def clamp(code, x, y):
        r = radius[code] + 1
        return (min(max(x, r), sheet.cols - 1 - r), min(max(y, r), sheet.rows - 1 - r))

    def cost(at):
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
    sheet.at = {c: (round(x), round(y)) for c, (x, y) in best.items()}
    out = []
    for q in requests:
        if q.miss(sheet.at[q.code], sheet.at[q.of]) > 0.5:
            out.append(f"line {q.node.line}: region {q.code} place {q.of} {q.node.args[1]} "
                       f"{q.node.args[2]!r} is unmet on {sheet.name}: "
                       f"{q.said(sheet.at[q.code], sheet.at[q.of])}")
    for i, a in enumerate(codes):
        for b in codes[i + 1:]:
            if math.dist(sheet.at[a], sheet.at[b]) < max(SEPARATION * (radius[a] + radius[b]), MARK_GAP) - 0.5:
                out.append(f"{a} and {b} cannot lie apart on {sheet.name}: their places leave no room")
    return out


def artgen(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["node", str(ARTGEN), *map(str, args)], capture_output=True, text=True)


def map_file(sheet: Sheet, seed: int, names: dict, regions: dict, radius: dict, home: dict) -> dict:
    local = sheet.square <= LOCAL_SQUARE_FEET
    m = {"id": sheet.name, "version": 1, "preset": "local" if local else "regional", "seed": seed,
         "cols": sheet.cols, "rows": sheet.rows, "grid": {"type": "square", "size": 1, "coords": not local},
         "scale": {"perCell": sheet.per_cell, "unit": UNIT[sheet.unit]},
         "edits": [], "overlay": {"labels": [], "symbols": []}, "require": []}
    if not local:
        m["topo"] = {"maxElevation": 600, "interval": 50, "majorEvery": 4, "unit": "ft", "labels": False}
    for code in sheet.codes:
        x, y = sheet.at[code]
        area = home[code] == sheet.name
        rating = str(regions[code].props.get("rating", "")).upper()
        m["overlay"]["symbols"].append({"kind": "castle" if rating == "SAFE" else "poi", "x": x, "y": y,
                                        "origin": "tables"})
        m["overlay"]["labels"].append({"text": f"{code} {names.get(code, '')}".strip(), "x": x + 1.2,
                                       "y": y, "kind": "region" if area else "place", "origin": "tables"})
        ground = next((c for c in regions[code].children if c.name == "ground"), None)
        if area and ground:
            m["require"].append({"id": f"{code}-ground", "kind": "terrain", "origin": "tables",
                                 "area": {"circle": [x, y, radius[code]]},
                                 "terrain": str(ground.args[0]), "share": GROUND_SHARE})
    return m


def draw(sheet: Sheet, target: Path, build) -> tuple[list[str], int]:
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
                joined.write_text(json.dumps({**kept, "seed": seed}))
                done = artgen("map", "sync", "--file", joined, "--from", fresh, "--origin", "tables")
                if done.returncode:
                    return [f"artgen cannot sync {sheet.name}: {done.stderr.strip() or done.stdout.strip()}"], seed
                fresh = joined
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
    names = {c: r["name"] for c, r in sc.parse_regions_gazetteer().items()} if (setting / "region" / "Regions.md").exists() else {}
    radius = {}
    for code, node in brief.regions.items():
        n = tables.bounds(node.props.get("locations", 1))[1]
        radius[code] = max(3, math.ceil(math.sqrt(SQUARES_PER_LOCATION * n / math.pi)))
    unmet, table = [], []
    for sheet in sheets.values():
        rad = {c: (radius[c] if home[c] == sheet.name else 0) for c in sheet.codes}
        asks = [Request(c, p, sheet.square) for c in sheet.codes
                for p in brief.regions[c].children if p.name == "place" and str(p.args[0]) in sheet.codes]
        unmet += solve(sheet, rad, asks)
        target = setting / f"{sheet.name}.json"
        problems, sheet.seed = draw(sheet, target,
                                    lambda seed, s=sheet: map_file(s, seed, names, brief.regions, rad, home))
        for p in problems:
            ground = brief.regions.get(p.split("-")[0])
            node = next((c for c in ground.children if c.name == "ground"), None) if ground else None
            unmet.append(f"{'line ' + str(node.line) + ': ' if node else ''}{sheet.name}: {p}")
        for code in sheet.codes:
            x, y = sheet.at[code]
            table.append(f"| {sheet.name} {code} | {sheet.name} | {code} | {x},{y} | "
                         f"{'circle, radius ' + str(rad[code]) + ' squares' if rad[code] else 'mark'} |")
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


def facts(file: Path, *args) -> dict:
    done = artgen("map", "facts", "--file", file, "--json", *args)
    if done.returncode or not done.stdout.strip():
        raise SystemExit(f"artgen cannot read {file.name}: {(done.stderr or done.stdout).strip()}")
    return json.loads(done.stdout)


def ground(brief_path: Path, setting: Path) -> int:
    schema = tables.Schema(brief=brief_path)
    brief = tables.Brief(schema, brief_path)
    sheets_md = setting / "Sheets.md"
    if brief.problems or not sheets_md.exists():
        print("; ".join(brief.problems) if brief.problems else "setting/Sheets.md is missing: run `place` first")
        return 1
    sheets = {n: Sheet(n, node) for n, node in brief.sheets.items()}
    rows = sc.read_tables(sheets_md)[0].dicts()
    gazetteer = sc.parse_regions_gazetteer()
    world = tables.Setting({c: g["rating"] for c, g in gazetteer.items()})
    skipped, off = [], []
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
        folder = setting / "region" / code
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "Ground.md").write_text(
            f"# Ground of {code} {gazetteer[code]['name']}\n\n```kdl\n" + "\n".join(lines) + "\n```\n")
    if off:
        print("NOTE: off its sheet: " + ", ".join(off))
    if skipped:
        print("NOTE: no bearing and distance, or north and east, for " + ", ".join(skipped))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["place", "ground"])
    ap.add_argument("--brief", type=Path, default=tables.BRIEF)
    ap.add_argument("--setting", type=Path, default=tables.SETTING)
    a = ap.parse_args()
    return (place if a.command == "place" else ground)(a.brief, a.setting)


if __name__ == "__main__":
    sys.exit(main())
