"""Prototype for review item 4: room contents drawn by rule, with no solver.
Each Mystery, Hazard and Reward of a room takes the symbol its type names and one of nine slots in the room
(centre and the eight compass points, set in from the walls): a Mystery the centre, a Hazard the slot nearest
the room's first door, a Reward the free slot farthest from every door. usage: symbols.py REGION OUTDIR"""
import json, math, sys
from pathlib import Path
sys.path.insert(0, "tools")
import maps, tables

MYSTERY = {"Altar": "altar", "Statue": "statue", "Fountain": "fountain", "Throne": "throne"}
HAZARD = {"Pit": "pit", "Water": "pool", "Fire/Lava": "fire", "Broken/Weak Floor": "rubble"}
CONTAINER = {"coffin": "coffin", "sarcophag": "coffin", "tomb": "coffin", "barrel": "barrel", "crate": "crate", "bones": "bones", "skull": "bones"}

code, out = sys.argv[1], Path(sys.argv[2])
region = maps.world_for(tables.SETTING).regions[code]
for bid in maps.blocks_of(region):
    file = maps.built(code, bid)[0]
    m = json.loads(file.read_text())
    box = {r["label"]: r for r in m["rooms"]}
    doors = {c: [] for c in box}
    lab = {r["id"]: r["label"] for r in m["rooms"]}
    for c in m["corridors"]:
        for e in (c["from"], c["to"]):
            if "room" in e and "port" in e:
                doors[lab[e["room"]]].append(e["port"])
    for x in m["connections"]:
        for k in ("a", "b"):
            doors[lab[x[k]]].append(x["at"])
    want = {}
    for n in region.files.get("Challenges", []) + region.files.get("Rewards", []):
        c = str(n.args[0])
        if n.name == "Mystery" and (k := MYSTERY.get(str(n.props.get("type")))):
            want.setdefault(c, []).append(("centre", k))
        elif n.name == "Hazard":
            want.setdefault(c, []).append(("door", HAZARD.get(str(n.props.get("type")), "trap")))
        elif n.name == "Reward":
            g = str(n.props.get("container", "")).lower()
            want.setdefault(c, []).append(("far", next((v for k, v in CONTAINER.items() if k in g), "chest")))
    symbols, placed, skipped = [], 0, 0
    for c, items in want.items():
        r = box.get(c)
        if r is None:
            continue
        cx, cy, w, h = r["x"] + r["w"] / 2, r["y"] + r["h"] / 2, r["w"], r["h"]
        inset = 0.30 if r["shape"] != "rect" else 0.34
        slots = {(i, j): (cx + i * w * inset, cy + j * h * inset) for i in (-1, 0, 1) for j in (-1, 0, 1)}
        if min(w, h) <= 2:                                # a passage-wide room: its long axis only
            slots = {k: v for k, v in slots.items() if (k[0] == 0 if w <= 2 else k[1] == 0)}
        near = lambda p: min((math.dist(p, d) for d in doors[c]), default=0)
        for how, kind in sorted(items, key=lambda i: ("centre", "door", "far").index(i[0])):
            free = list(slots.items())
            if not free:
                skipped += 1
                continue
            if how == "centre" and (0, 0) in slots:
                key = (0, 0)
            elif how == "door":
                key = min(free, key=lambda s: (near(s[1]), s[0] == (0, 0)))[0]
            else:
                key = max((s for s in free if s[0] != (0, 0)) or free, key=lambda s: near(s[1]))[0]
            x, y = slots.pop(key)
            symbols.append({"kind": kind, "x": round(x, 2), "y": round(y, 2)})
            placed += 1
    m["overlay"]["symbols"] = symbols
    m["legend"] = True
    f = out / f"{bid}.json"
    f.write_text(json.dumps(m))
    done = maps.artgen("dungeon", "render", "--file", f, "--format", "png", "--fit", "1400x1400px", "--out", out)
    chk = maps.artgen("dungeon", "check", "--file", f, "--json")
    errs = json.loads(chk.stdout).get("errors", []) if chk.stdout.startswith("{") else [chk.stderr]
    print(bid, "symbols", placed, "skipped", skipped, "errors", len(errs), [e.get("message") if isinstance(e, dict) else e for e in errs][:3], done.returncode)
