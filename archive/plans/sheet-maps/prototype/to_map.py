"""A WILD region's Locations and Stops as an artgen local terrain map, north up."""
import sys, subprocess, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))     # the setting_builder checkout this file is in
import site_common as sc
code, game, yd = sys.argv[1], sys.argv[2], float(sys.argv[3])   # yards per cell
pos, _ = sc.positions(code)
locs = sc.parse_locations_gazetteer(code)
stops = sc.route_stops(code)
pts = list(pos.values()) + [s[1] for v in stops.values() for s in v if s[1]] + [(0, 0, 0)]
x0 = min(p[0] for p in pts); y1 = max(p[1] for p in pts)
M = 4
cols = round((max(p[0] for p in pts) - x0) / yd) + 2 * M
rows = round((y1 - min(p[1] for p in pts)) / yd) + 2 * M
def c(p): return round((p[0] - x0) / yd + M, 1), round((y1 - p[1]) / yd + M, 1)
d = code.lower(); shutil.rmtree(f"{game}/art/maps/{d}", ignore_errors=True)
def run(*a): subprocess.run(["node", "tools/artgen/artgen.js", "map", *map(str, a)], cwd=game, check=True, stdout=subprocess.DEVNULL)
name = sc.parse_regions_gazetteer()[code]["name"]
run("new", d, "--preset", "local", "--size", f"{cols}x{rows}", "--grid", "none", "--title", f"{code} {name}", "--seed", 7)
run("set", d, "--per-cell", yd, "--unit", "yd")
for extra in sys.argv[4:]: run(*extra.split("|"))           # hand edits: terrain shaping the tables can't give
SYM = {"Lair": "skull", "Ruin": "ruin", "Hidden": "poi", "Secret": "treasure", "Natural": "cave", "Landmark": "poi"}
for cd, p in pos.items():
    n = locs[int(cd.split(".")[1])]
    if n["weight"] == "route": continue
    x, y = c(p)
    run("symbol", d, SYM.get(n["weight"].title(), "poi"), "--at", f"{x},{y}", "--scale", 0.6)
    run("label", d, f"{cd} {n['name']}", "--at", f"{x + (1.2 if p[0] >= 0 else -1.2)},{y}", "--kind", "place", "--size", 0.5)
for route, ss in stops.items():
    path = [(0, 0, 0)] + [s[1] for s in ss if s[1]]
    path.sort(key=lambda p: -p[1] if False else p[1])
    run("edit", d, "road", "--points", ",".join(f"{a},{b}" for a, b in map(c, path)))
run("render", d, "--theme", "both", "--format", "png", "--out", "out")
print(cols, rows, c((0, 0, 0)))
