"""A DANGEROUS region's tables as artgen dungeon commands: rooms at the places
site_common.positions() gives, links from Connections, doors from type/Secret/Lock."""
import sys, subprocess
sys.path.insert(0, "/home/user/setting_builder/tools")
import site_common as sc, kdl

code, game = sys.argv[1], sys.argv[2]
sizes = dict(a.split("=") for a in sys.argv[3:])        # e.g. F.5=3x3 (cells of 5 ft) from the Brief's prose
CELL = 5 / 3                                             # yards per cell
pos, _ = sc.positions(code)
locs = sc.parse_locations_gazetteer(code)
xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
x0, y1 = min(xs), max(ys)
M = 4
def cell(p): return round((p[0] - x0) / CELL) + M, round((y1 - p[1]) / CELL) + M
w = round((max(xs) - x0) / CELL) + 2 * M; h = round((y1 - min(ys)) / CELL) + 2 * M
A = ["node", "tools/artgen/artgen.js"]
def run(*a): subprocess.run(A + list(a), cwd=game, check=True, stdout=subprocess.DEVNULL)
d = code.lower()
import shutil; shutil.rmtree(f"{game}/art/dungeons/{d}", ignore_errors=True)
run("dungeon", "new", d, "--empty", "--size", f"{w}x{h}", "--title", f"{code} {sc.parse_regions_gazetteer()[code]['name']}".strip())
rid = {}
for i, c in enumerate(sorted(pos, key=lambda c: int(c.split('.')[1])), 1):
    sw, sh = map(int, sizes.get(c, "4x4").split("x"))
    cx, cy = cell(pos[c])
    run("dungeon", "room", d, "add", "rect",
        "--at", f"{cx - sw // 2},{cy - sh // 2}", "--size", f"{sw}x{sh}",
        "--label", f"{c} {locs[int(c.split('.')[1])]['name']}", "--number", c.split(".")[1], "--room-id", f"r{i}")
    rid[c] = f"r{i}"
nodes = kdl.fenced((sc.SETTING / "region" / code / "Connections.md").read_text())
seen = set(); traps = []
DOOR = {"Open": "none", "Crude": "none"}
for n in nodes:
    a, b = str(n.args[0]), str(n.props["to"])
    kids = {k.name for k in n.children}
    door = "locked" if "Lock" in kids else "secret" if "Secret" in kids else DOOR.get(str(n.props.get("type")), "door")
    if "Hazard" in kids: traps.append((a, b))
    key = tuple(sorted((a, b)))
    if a in rid and b in rid:
        if key in seen: continue
        seen.add(key)
        run("dungeon", "link", d, rid[a], rid[b], "--doors", f"{door},none")
    elif a in rid:                                       # a way out of the region: corridor to the map edge
        o = sc.parse_at(str(n.props.get("orientation", ""))) or (0, 0, 0)
        tx, ty = cell((pos[a][0] + o[0], pos[a][1] + o[1]))
        tx, ty = min(max(tx, 1), w - 2), min(max(ty, 1), h - 2)
        run("dungeon", "link", d, rid[a], f"{tx},{ty}", "--doors", f"{door},none")
        run("dungeon", "label", d, f"to {b}", "--at", f"{tx},{ty - 1}", "--kind", "note")
for a, b in traps:
    if a in pos and b in pos:
        (ax, ay), (bx, by) = cell(pos[a]), cell(pos[b])
        run("dungeon", "symbol", d, "trap", "--at", f"{(ax + bx) / 2},{(ay + by) / 2}")
run("dungeon", "fit", d)
run("dungeon", "render", d, "--format", "both", "--out", "out")
print(d, w, h, pos)
