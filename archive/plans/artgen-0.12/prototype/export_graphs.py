"""Export each DANGEROUS block's packing inputs (as tools/dungeon.py pack_region builds them) as an artgen layout graph."""
import json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
import dungeon, maps, route, space, tables
out = Path(sys.argv[1])
world = maps.world_for(tables.SETTING)
compass = list(world.schema.setting_enums["Compass"])
CELL = 5
for code, region in world.regions.items():
    if region.rating.upper() != "DANGEROUS":
        continue
    rates = tables.Brief(world.schema).packing(code)
    dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    for bid, block in maps.blocks_of(region).items():
        members = sorted((m.strip() for m in str(block.props["locations"]).split(",")), key=route.number)
        rooms = []
        for c in members:
            d = dress[c]; fp = dungeon.footprint(d)
            r = {"id": c, "w": int(d.props["width"]) / CELL, "h": int(d.props["length"]) / CELL, "shape": fp.shape if fp.shape in ("rect", "cave", "round", "octagon", "hexagon", "poly") else "rect",
                 "label": c, "hall": str(d.props.get("shape")) == "hall", "turns": dungeon.turns(region, c, dress)}
            if fp.points: r["points"] = [v / CELL for p in fp.points for v in p]
            rooms.append(r)
        placed = {c: at for c in members if (at := space.centre(dress[c]))}
        walls = dungeon.walls_of(region, members)
        ways, seen = [], set()
        for n in region.files.get("Connections", []):
            a, b = str(n.args[0]), str(n.props.get("to"))
            if a not in members or b not in members or frozenset((a, b)) in seen: continue
            seen.add(frozenset((a, b)))
            if (a, b) in walls or (b, a) in walls:
                br = walls[a, b] if (a, b) in walls else (walls[b, a] + 180) % 360
            elif a in placed and b in placed:
                br = math.degrees(math.atan2(placed[b][0] - placed[a][0], placed[b][1] - placed[a][1])) % 360
            else:
                br = compass.index(str(n.props["bearing"])) * 22.5 if "bearing" in n.props else None
            w = {"a": a, "b": b}
            if br is not None: w["bearing"] = br
            if (a, b) in walls: w["wall"] = walls[a, b]
            ways.append(w)
        o = space.outline_value(block.props.get("outline"))
        g = {"id": f"{code}-{bid.split('.')[-1]}", "rooms": rooms, "ways": ways, "width": 2, "scale": {"perCell": CELL, "unit": "ft"},
             "fill": list(rates["fill"]), "passages": rates["passages"], "seed": 1, "tries": 12}
        if rates["detour"] is not None: g["detour"] = rates["detour"] / CELL
        if o and o[0] == "poly":
            g["footprint"] = [v for x, y in o[1] for v in (x / CELL, -y / CELL)]
        elif rates["footprint"]:
            g["footprint"] = rates["footprint"] / CELL
        (out / f"{g['id']}.json").write_text(json.dumps(g, indent=1))
        print(g["id"], len(rooms), "rooms", len(ways), "ways", "footprint", g.get("footprint") if not isinstance(g.get("footprint"), list) else "poly")
