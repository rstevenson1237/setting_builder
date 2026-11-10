"""A DANGEROUS block: its map, its passages, its packing, and what is wrong with it.

block_map    the artgen dungeon file for a block, from its Dressing, Connections and Blocks
passages     a packed block's ways as its map draws them, from `artgen dungeon facts`
pack_region  `python3 tools/maps.py pack`: a region's blocks laid out by `artgen dungeon layout`,
             and the positions written to its tables
problems     what is wrong with a block, for the validator
"""
from __future__ import annotations

import functools
import hashlib
import json
import math
import re
import tempfile
from pathlib import Path

import kdl
import maps
import space
import tables
from maps import BUILD, CACHE, UNSIZED, artgen, blocks_of, built, feet, world_for

DOOR = {"Open": None, "Archway": None, "Broken": None, "Crude": None, "Lift": None, "Chute": None, "Iron": "portcullis"}
GAP = {"Archway": "arch"}       # a doorless way through a shared wall, else open
DRAWN = {"rect": "rect", "cave": "cave", "round": "circle", "octagon": "octagon", "hexagon": "hexagon"}   # artgen's shape, else a poly
CUT = 1 / (2 + math.sqrt(2))   # an octagon's corner cut, a share of its shorter side: regular when square
APART = 10                      # feet two routes to one room may disagree by
EDGE = 6                        # cells of map beyond the rooms, for the ways out of it
EXIT = 4                        # cells a way out of the block runs past its room's wall
MAX_CELLS = 150
CELLS = (5, 10, 20)             # feet to a cell, the finest that fits the block
ROUTED_CELLS = (5, 10)          # feet to a cell, where its passages are routed
ROUTED_WALL = 2.5               # a routed block's wall stroke, so a wall between two floors reads as one, its rock hatched
LATTICE = 10                    # feet: a passage's width, and the grid a packed block's rooms lie on


def number(code: str) -> int:
    return int(code.split(".")[1])


def footprint(d: kdl.Node | None) -> tuple[str, list[tuple[float, float]] | None]:
    """A room's shape from its Dressing, and a poly's points in feet east and south of its centre:
    its own poly outline, else its shape."""
    p = d.props if d is not None else {}
    o = space.outline_value(p.get("outline"))
    if o and o[0] == "poly":
        return "poly", [(a, -b) for a, b in o[1]]
    shape = str(p.get("shape", "rect"))
    return ("rect" if shape == "hall" else shape), None


DIRECTION = re.compile(r"\b(north|south|east|west)", re.I)


def turns(region, c: str, dress: dict) -> bool:
    """Whether the packer may turn or mirror a room: nothing about it names a direction - its
    Dressing, its write-up, a wall a way of its names, a room set against it or it against one -
    and it is no hexagon, whose flat walls run north and south."""
    d = dress[c]
    page = region.dir / f"{c.split('.')[1]}.md"
    words = " ".join(str(v) for v in d.props.values()) + (page.read_text() if page.exists() else "")
    walled = any(str(n.args[0]) == c and "wall" in n.props for n in region.files.get("Connections", []) if n.args)
    held = "against" in d.props or any((space.anchor_of(e.props.get("against")) or ("",))[0] == c for e in dress.values())
    return not (DIRECTION.search(words) or walled or held or str(d.props.get("shape")) == "hexagon")


def rocks_of(region, bid: str) -> list[kdl.Node]:
    return [n for n in region.files.get("Blocks", []) if n.name == "Rock" and n.args and str(n.args[0]) == bid]


def area(poly: list[tuple[float, float]]) -> float:
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))) / 2


def shift_of(dress: dict, members: list[str]) -> tuple[float, float]:
    """How far east and south a packed block's rooms move, from its centre with y running south,
    to stand their corners on the lattice."""
    d = dress[members[0]]
    x, y = space.centre(d)
    return ((float(d.props["width"]) / 2 - x) % LATTICE, (float(d.props["length"]) / 2 + y) % LATTICE)


def engine(command: str, m: dict, *args: str) -> dict:
    """`artgen dungeon facts` or `check` of a map file, as JSON; kept under .maps-cache."""
    key = hashlib.sha256((" ".join((command, *args)) + json.dumps(m, sort_keys=True) + BUILD).encode()).hexdigest()
    kept = CACHE / f"{key}.{command}.json"
    if kept.exists():
        return json.loads(kept.read_text())
    with tempfile.TemporaryDirectory() as tmp:
        (file := Path(tmp) / "block.json").write_text(json.dumps(m))
        done = artgen("dungeon", command, "--file", file, "--json", *args)
    out = json.loads(done.stdout) if done.stdout.startswith("{") else {}
    CACHE.mkdir(exist_ok=True)
    kept.write_text(json.dumps(out))
    return out


def walls_of(region, members) -> dict[tuple[str, str], float]:
    """The wall each way within a block names at the room it leaves, as a bearing in degrees."""
    compass = space.compass()
    return {(str(n.args[0]), str(n.props["to"])): compass.index(str(n.props["wall"])) * 22.5
            for n in region.files.get("Connections", [])
            if n.args and str(n.args[0]) in members and str(n.props.get("to")) in members and str(n.props.get("wall")) in compass}


def facing(dx: float, dy: float) -> str:
    """The wall, n, e, s or w, facing a displacement in cells, y running south."""
    return ("e" if dx > 0 else "w") if abs(dx) > abs(dy) else ("s" if dy > 0 else "n")


LOOK_STYLE = {"hatch": "hatch", "rock": "rock", "numbers": "numbers", "doors": "doors", "preset": "preset"}
LOOK_PALETTE = {"rock-color": "rock", "floor": "floor", "ink": "ink", "grid": "grid", "wall-color": "wall"}


def looked(style: dict) -> dict:
    """A block's style with BRIEF.md's dungeon look over it. A preset fills what the look leaves
    unset, so the hatch, band and wall this module draws by default give way to it."""
    want = maps.look("dungeon")
    if "preset" in want:
        for k in ("hatch", "band", "wall"):
            if k not in want:
                style.pop(k, None)
    style.update({LOOK_STYLE[k]: v for k, v in want.items() if k in LOOK_STYLE})
    if "wall" in want:
        style["wall"] = float(want["wall"])
    if palette := {LOOK_PALETTE[k]: v for k, v in want.items() if k in LOOK_PALETTE}:
        style["palette"] = palette
    return style


def block_map(region, block: kdl.Node) -> tuple[dict | None, list[str]]:
    """The artgen dungeon file for one block of a region, and what the tables leave it
    unable to draw."""
    code, bid = region.code, str(block.args[0])
    members = [m.strip() for m in str(block.props["locations"]).split(",")]
    dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    ways = [n for n in region.files.get("Connections", []) if n.args and "to" in n.props]
    problems, compass = [], list(tables.Schema().setting_enums["Compass"])

    def step(n):
        if "bearing" not in n.props or "distance" not in n.props:
            return None
        a = compass.index(str(n.props["bearing"])) * 22.5
        d = feet(str(n.props["distance"]))
        return d * math.sin(math.radians(a)), -d * math.cos(math.radians(a))
    leaving = {str(n.args[0]) for n in ways if str(n.props["to"]) not in members and str(n.args[0]) in members}
    entrance = min(leaving or members, key=lambda c: int(c.split(".")[1]))
    stated = {c: (at[0], -at[1]) for c in members if (at := space.centre(dress.get(c)))}
    if stated and len(stated) != len(members):
        problems.append("some rooms state xyz and others do not")
    at, queue, told = ({c: stated[c] for c in members}, [], set()) if len(stated) == len(members) \
        else ({entrance: (0.0, 0.0)}, [entrance], set())
    for a in queue:                                      # rooms placed by walking orientations
        for n in ways:
            x, y = str(n.args[0]), str(n.props["to"])
            if x == a and y in members and (v := step(n)):
                far, sign = y, 1
            elif y == a and x in members and (v := step(n)):
                far, sign = x, -1
            else:
                continue
            spot = (at[a][0] + sign * v[0], at[a][1] + sign * v[1])
            if far not in at:
                at[far] = spot
                queue.append(far)
            elif math.dist(at[far], spot) > APART and (key := frozenset((a, far))) not in told:
                told.add(key)
                problems.append(f"the ways to {far} place it {math.dist(at[far], spot):.0f} feet apart")
    for c in members:
        if c not in at:
            problems.append(f"{c} is reached from {entrance} by no Connection with a bearing and distance")
    if not at:
        return None, problems
    size = {}
    for c in at:
        d = dress.get(c)
        w = d.props.get("width") if d else None
        h = d.props.get("length") if d else None
        if w is None or h is None:
            problems.append(f"{c} states no width and length")
        size[c] = (float(w or UNSIZED), float(h or UNSIZED), footprint(d))
    routed = len(stated) == len(members) and bool(members)
    if routed:                                           # corners on the lattice the passages are routed on
        shift = shift_of(dress, members)
        at = {c: (at[c][0] + shift[0], at[c][1] + shift[1]) for c in at}
        for c in at:
            if any(abs((at[c][k] - size[c][k] / 2) / LATTICE - round((at[c][k] - size[c][k] / 2) / LATTICE)) > 1e-6
                   for k in (0, 1)):
                problems.append(f"{c} does not lie on the {LATTICE}-foot lattice")
    square = lambda c: size[c][2][0] in ("rect", "cave")
    for i, a in enumerate(list(at)):                     # a packed block's other shapes are left to artgen's check
        for b in list(at)[i + 1:]:
            if all(abs(at[a][k] - at[b][k]) < (size[a][k] + size[b][k]) / 2 - APART / 5 for k in (0, 1)) \
                    and (not routed or square(a) and square(b)):
                problems.append(f"{a} and {b} overlap")
    lo = [min(at[c][i] - size[c][i] / 2 for c in at) for i in (0, 1)]
    hi = [max(at[c][i] + size[c][i] / 2 for c in at) for i in (0, 1)]
    fits = ROUTED_CELLS if routed else CELLS
    cell = next((f for f in fits if max(hi[i] - lo[i] for i in (0, 1)) / f + 2 * EDGE <= MAX_CELLS), fits[-1])
    cols, rows = (max(4, math.ceil((hi[i] - lo[i]) / cell) + 2 * EDGE) for i in (0, 1))
    cx = lambda c: (at[c][0] - lo[0]) / cell + EDGE
    cy = lambda c: (at[c][1] - lo[1]) / cell + EDGE
    to_cell = lambda x, y: [round((x - lo[0]) / cell + EDGE, 2), round((y - lo[1]) / cell + EDGE, 2)]   # feet east, south
    rid = lambda c: c.replace(".", "-")
    m = {"id": f"{code}-{bid.split('.')[-1]}", "version": 2 if routed else 1, "seed": 1, "cols": cols, "rows": rows,
         "gen": {"rooms": 1, "minSize": 3, "maxSize": 8, "caves": 0, "round": 0, "loops": 0, "doors": 0,
                 "corridorWidth": 1, "spacing": 2, "entrance": False},
         "grid": {"show": True, "size": 2, "sub": True, "clip": "floor"},
         "style": {"hatch": "band", "band": 0.9, "wall": 1}, "scale": {"perCell": cell, "unit": "ft"},
         "numbers": False, "scaleBar": True, "compass": False, "furniture": {"place": "outside"},
         "rooms": [], "corridors": [], "connections": [], "overlay": {"labels": [], "symbols": []}}
    if routed:
        m["style"].update(wall=ROUTED_WALL, hatch="full")
    m["style"] = looked(m["style"])
    for c in at:
        w, h, (shape, pts) = size[c]
        drawn = DRAWN.get(shape, "poly")
        m["rooms"].append({"id": rid(c), "shape": drawn, "x": round(cx(c) - w / 2 / cell, 2),
                           "y": round(cy(c) - h / 2 / cell, 2), "w": max(1, round(w / cell, 2)),
                           "h": max(1, round(h / cell, 2)), "label": c, "number": False, "origin": "tables",
                           **({"cut": round(CUT, 4)} if drawn == "octagon" else {})})
        if drawn == "poly":
            m["rooms"][-1]["points"] = [v for x, y in space.shape_outline(shape, w, h, pts)
                                        for v in to_cell(at[c][0] + x, at[c][1] + y)]

    def door(n):
        kids = {k.name for k in n.children}
        if "Lock" in kids:
            return "locked"
        if "Secret" in kids:
            return "secret"
        return DOOR.get(str(n.props.get("type")), "door")

    def strongest(*ends):
        """The one door a shared wall draws for a way, from either side's entry: a lock, then a
        secret, then whatever the first side states."""
        got = [e for e in ends if e]
        return next((e for k in ("locked", "secret") for e in got if e[0] == k), got[0])

    def opening(kind):
        """A corridor's end: its door, else an arch, so a wall still parts passage from room."""
        return kind or "arch"

    def touch(a, b) -> bool:
        """Rooms a and b share a wall: they meet along one axis and overlap along the other."""
        d = [abs(cx(a) - cx(b)) * cell, abs(cy(a) - cy(b)) * cell]
        reach = [(size[a][k] + size[b][k]) / 2 for k in (0, 1)]
        return square(a) and square(b) and any(
            abs(d[k] - reach[k]) <= cell / 4 and d[1 - k] < reach[1 - k] - cell for k in (0, 1))

    def lane(a, b):
        """The sides and offsets in cells that run a straight corridor from room a to room b
        where they face one another across a gap, else None."""
        box = lambda c: (at[c][0] - size[c][0] / 2, at[c][1] - size[c][1] / 2,
                         at[c][0] + size[c][0] / 2, at[c][1] + size[c][1] / 2)
        p, q = box(a), box(b)
        for k, (before, after) in enumerate((("e", "w"), ("s", "n"))):
            lo, hi = max(p[1 - k], q[1 - k]), min(p[3 - k], q[3 - k])
            if hi - lo < 2 * cell:
                continue
            if p[k + 2] <= q[k]:
                sides = (before, after)
            elif q[k + 2] <= p[k]:
                sides = (after, before)
            else:
                continue
            along = lambda c: round(min(max((lo + hi) / 2 - box(c)[1 - k], cell / 2), size[c][1 - k] - cell / 2) / cell, 2) \
                if square(c) else round(size[c][1 - k] / 2 / cell, 2)
            return sides[0], along(a), sides[1], along(b)
        return None

    def rough(*ns) -> bool:
        return any(str(n.props.get("type")) in ("Crude", "Broken") for n in ns)

    def span(n) -> int:
        """Cells across a passage: the way's own width, else the block's."""
        return max(1, round(float(n.props.get("width", region.passage(block, "width"))) / cell))
    def toward(n):
        """A placed stair's way, east and south: toward the room it climbs to, else north."""
        if str(n.props.get("climb", "0")).lstrip("-") in ("", "0"):
            return None
        far, here = space.settled().pin(str(n.args[0])), space.centre(dress.get(str(n.args[0])))
        if far is None or here is None:
            return None
        v = (far[0] - here[0], here[1] - far[1])
        return v if math.hypot(*v) >= 1 else (0.0, -1.0)
    seen = {}
    for n in ways:
        a, b = str(n.args[0]), str(n.props["to"])
        if a in at and b in at:
            key = tuple(sorted((a, b), key=number))
            ends = seen.setdefault(key, {})
            ends[a] = (door(n), n)
        elif a in at:                                     # a way out of the block: a mark in its room
            v = step(n) or toward(n)
            if v is None:
                problems.append(f"{a} to {b} states no bearing and distance")
                continue
            climb = int(n.props.get("climb") or 0)
            room = next(r for r in m["rooms"] if r["id"] == rid(a))
            gate = {"locked": ", locked", "secret": ", hidden"}.get(door(n), "")
            room.setdefault("exits", []).append({"kind": "stairs-up" if climb > 0 else "stairs-down" if climb < 0 else "arrow",
                                                 "side": facing(*v),
                                                 "text": f"{'Up to' if climb > 0 else 'Down to' if climb < 0 else 'To'} {b}{gate}"})
    if routed:
        north = lambda x, y: to_cell(x + shift[0], shift[1] - y)      # feet east and north of the block's centre
        if (o := space.outline_value(block.props.get("outline"))) and o[0] == "poly":
            m["bounds"] = [v for x, y in o[1] for v in north(x, y)]
        for r in rocks_of(region, bid):
            xy = space.point_of(r.props.get("xyz")) or [0.0, 0.0]
            if (shape := space.outline_value(r.props.get("outline"))) is not None:
                m.setdefault("areas", []).append({"points": [v for x, y in space.polygon(shape, xy[0], xy[1]) for v in north(x, y)],
                                                  "kind": "rock", "label": str(r.props.get("what", "")), "origin": "tables"})
        named = walls_of(region, members)
        outline = {c: [(at[c][0] + x, at[c][1] + y) for x, y in space.shape_outline(size[c][2][0], size[c][0], size[c][1], size[c][2][1])]
                   for c in at}

        def shared(a, b):
            """The middle of the longest stretch of wall rooms a and b share, in feet, where it is a
            passage wide; else None."""
            best, mid = LATTICE - 1e-6, None
            for p, q in zip(outline[a], outline[a][1:] + outline[a][:1]):
                ex, ey = q[0] - p[0], q[1] - p[1]
                if not (n := math.hypot(ex, ey)):
                    continue
                for r, t in zip(outline[b], outline[b][1:] + outline[b][:1]):
                    if max(abs(ex * (v[1] - p[1]) - ey * (v[0] - p[0])) / n for v in (r, t)) > 1e-6:
                        continue                         # not on the line of a's wall
                    lo, hi = sorted(((v[0] - p[0]) * ex + (v[1] - p[1]) * ey) / n for v in (r, t))
                    lo, hi = max(lo, 0.0), min(hi, n)
                    if hi - lo > best:
                        best, mid = hi - lo, (p[0] + ex * (lo + hi) / 2 / n, p[1] + ey * (lo + hi) / 2 / n)
            return mid

        def end(c, bearing):
            """A passage's end at room c: by the wall its Connection names, else where artgen likes."""
            if bearing is None:
                return {"room": rid(c)}
            if bearing % 90 == 0 and square(c):
                return {"room": rid(c), "side": "nesw"[int(bearing) // 90]}
            ux, uy = math.sin(math.radians(bearing)), -math.cos(math.radians(bearing))
            w, h, (shape, pts) = size[c]
            poly = space.shape_outline(shape, w, h, pts)
            hits = []                                    # where the ray from its centre leaves its outline
            for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
                d = ux * (y1 - y0) - uy * (x1 - x0)
                if abs(d) > 1e-9 and 0 <= (u := (ux * y0 - uy * x0) / d * -1) <= 1:
                    hits.append(((x0 + (x1 - x0) * u) * ux + (y0 + (y1 - y0) * u) * uy, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u))
            _, x, y = max(hits)
            return {"room": rid(c), "port": to_cell(at[c][0] + x, at[c][1] + y)}

        corner = lambda c: (at[c][0] - size[c][0] / 2, at[c][1] - size[c][1] / 2)
        traps = []
        for a, b in sorted(seen, key=lambda k: (round(math.dist(corner(k[0]), corner(k[1]))), number(k[0]), number(k[1]))):
            ends = seen[a, b]                            # shortest first, as `dungeon layout` routes them
            first, second = ends.get(a), ends.get(b)
            rn = [n for _, n in ends.values()]
            hazard = any(c.name == "Hazard" for n in rn for c in n.children)
            if door := shared(a, b):                     # a door through the wall they share
                kind, n = strongest(first, second)
                m["connections"].append({"a": rid(a), "b": rid(b), "at": to_cell(*door), "origin": "tables",
                                         "kind": kind or GAP.get(str(n.props.get("type")), "open")})
                traps += [("connection", len(m["connections"]) - 1)] if hazard else []
                continue
            m["corridors"].append({"from": end(a, named.get((a, b))), "to": end(b, named.get((b, a))), "route": "maze",
                                   "width": round(LATTICE / cell, 2), "origin": "tables",
                                   **({"style": "natural"} if rough(*rn) else {}),
                                   "doors": [opening(first[0] if first else None), opening(second[0] if second else None)]})
            traps += [("corridor", len(m["corridors"]) - 1)] if hazard else []
        added = [(i, k) for i, c in enumerate(m["corridors"]) for k in (0, 1) if c["doors"][k] == "arch"]
        if added:                                        # an added arch that meets another corridor's end is left open
            f = engine("facts", m)
            ends = [(f["corridors"][i]["path"][0:2], f["corridors"][i]["path"][-2:]) for i in range(len(m["corridors"]))]
            for i, k in added:
                here = ends[i][k]
                if any(math.dist(here, ends[j][q]) < 1 for j in range(len(ends)) for q in (0, 1) if (j, q) != (i, k)):
                    m["corridors"][i]["doors"][k] = None
        if traps:                                        # a trap at the middle of its way, as artgen draws it
            f = engine("facts", m)
            for kind, i in traps:
                if kind == "connection":                 # in the opening through the shared wall
                    x, y = m["connections"][i]["at"]
                else:
                    path = f["corridors"][i]["path"]
                    pts = list(zip(path[::2], path[1::2]))
                    run = [math.dist(p, q) for p, q in zip(pts, pts[1:])]
                    half, (x, y) = sum(run) / 2, pts[0]
                    for p, q, d in zip(pts, pts[1:], run):
                        if half <= d:
                            x, y = p[0] + (q[0] - p[0]) * half / (d or 1), p[1] + (q[1] - p[1]) * half / (d or 1)
                            break
                        half -= d
                m["overlay"]["symbols"].append({"kind": "trap", "x": round(x, 2), "y": round(y, 2), "origin": "tables"})
        return m, problems
    for (a, b), ends in seen.items():
        first, second = ends.get(a), ends.get(b)
        if touch(a, b):                                  # through the wall they share
            kind, n = strongest(first, second)
            m["connections"].append({"a": rid(a), "b": rid(b), "origin": "tables",
                                     "kind": kind or GAP.get(str(n.props.get("type")), "open")})
            continue
        run = lane(a, b)
        m["corridors"].append({"from": {"room": rid(a), "side": run[0], "offset": run[1]} if run
                               else {"room": rid(a), "side": facing(cx(b) - cx(a), cy(b) - cy(a))},
                               "to": {"room": rid(b), "side": run[2], "offset": run[3]} if run
                               else {"room": rid(b), "side": facing(cx(a) - cx(b), cy(a) - cy(b))},
                               "width": max(span(n) for _, n in ends.values()), "origin": "tables",
                               **({"style": "natural"} if rough(*(n for _, n in ends.values())) else {}),
                               "doors": [first[0] if first else None, second[0] if second else None]})
        if any(c.name == "Hazard" for _, n in ends.values() for c in n.children):
            m["overlay"]["symbols"].append({"kind": "trap", "x": round((cx(a) + cx(b)) / 2, 2),
                                            "y": round((cy(a) + cy(b)) / 2, 2), "origin": "tables"})
    return m, problems


def route_around(m: dict) -> None:
    """Sends each corridor artgen finds running through a room, or across another corridor,
    round the rooms in its way, and then, if it still does, by whichever walls artgen picks.
    A routed or maze passage is already round them. The answer is kept under .maps-cache."""
    if all("via" in c or c.get("route") == "maze" for c in m["corridors"]):
        return
    key = hashlib.sha256((json.dumps(m) + BUILD).encode()).hexdigest()
    kept = CACHE / f"{key}.around.json"
    if kept.exists():
        m["corridors"] = json.loads(kept.read_text())
        return
    with tempfile.TemporaryDirectory() as tmp:
        file = Path(tmp) / "block.json"
        for fix in (lambda c: c.update(route="around"),
                    lambda c: [c[end].pop(k, None) for end in ("from", "to") for k in ("side", "offset")]):
            file.write_text(json.dumps(m))
            done = artgen("dungeon", "check", "--file", file, "--json")
            report = json.loads(done.stdout) if done.stdout.startswith("{") else {}
            found = (re.match(r"corridors\[(\d+)\]: (runs through|crosses)", f"{w['path']}: {w['message']}")
                     for w in report.get("warnings", []))
            for i in {int(f.group(1)) for f in found if f}:
                if "via" not in m["corridors"][i] and m["corridors"][i].get("route") != "maze":
                    fix(m["corridors"][i])
    CACHE.mkdir(exist_ok=True)
    kept.write_text(json.dumps(m["corridors"]))


FAULTS = ("door-off-wall,through-room,corridors-cross,way-no-passage,reenters-room,port-outside-room,rooms-overlap,"
          "in-keep-out,outside-bounds,maze-no-route,note-off-floor,marks-overlap,end-in-room,offset-moved,junction-at-bend")
SEEN = ("rooms-merge", "doors-stacked", "label-overlap")    # warnings of `check` the validator passes on
REPACK = ("in-keep-out", "outside-bounds")                   # a stale packing: `pack` places the rooms again


def defects(region, block: kdl.Node, m: dict) -> list[tuple[str, str]]:
    """What is wrong with a packed block's map file, as (level, message): `artgen dungeon check`'s
    faults, then its `facts` held to the tables' ways."""
    members = {x.strip() for x in str(block.props["locations"]).split(",")}
    dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    if not all(space.centre(dress.get(c)) for c in members):
        return []                                         # not packed: its corridors are left to artgen
    found = engine("check", m, "--errors", FAULTS)
    out = [("error", f"{x['path']}: {x['message']}" + (f": run `python3 tools/maps.py pack {region.code}` (step 4a)" if x.get("id") in REPACK else ""))
           for x in found.get("errors", [])]
    out += [("warning", f"{x['path']}: {x['message']}") for x in found.get("warnings", []) if x.get("id") in SEEN]
    facts = engine("facts", m)
    wrong = [f"{r} is reached by no way" for r in facts.get("unreached", [])]
    rid = lambda c: c.replace(".", "-")
    ways = {frozenset((rid(str(n.args[0])), rid(str(n.props["to"])))) for n in region.files.get("Connections", [])
            if n.args and str(n.args[0]) in members and str(n.props.get("to")) in members}
    joined = {frozenset((c["from"].get("room"), c["to"].get("room"))) for c in facts.get("corridors", [])}
    joined |= {frozenset((r["id"], c["to"])) for r in facts.get("rooms", []) for c in r.get("connections") or []}
    wrong += [f"the tables join {a} and {b}, but the map draws no way between them" for a, b in sorted(map(sorted, ways - joined))]
    wrong += [f"the map joins {a} and {b}, which the tables do not" for a, b in sorted(map(sorted, joined - ways))]
    leaving = sum(1 for n in region.files.get("Connections", [])
                  if n.args and str(n.args[0]) in members and str(n.props.get("to")) not in members)
    marks = sum(len(r.get("exits") or []) for r in facts.get("rooms", []))
    if marks != leaving:
        wrong.append(f"the tables take {leaving} ways out of the block, the map marks {marks}")
    return out + [("error", w) for w in wrong]


# -- pack: a DANGEROUS level's rooms placed close in a square, and the tables made to say so -----

def with_prop(line: str, key: str, value: str, after: str | None = None) -> str:
    """A KDL entry line with `key` set to `value`, in place or, where it is new, after `after` or last."""
    if re.search(rf"\b{key}=(\"[^\"]*\"|\S+)", line):
        return re.sub(rf"\b{key}=(\"[^\"]*\"|\S+)", f"{key}={value}", line, count=1)
    if after and (m := re.search(rf"\b{after}=(\"[^\"]*\"|\S+)", line)):
        return line[:m.end()] + f" {key}={value}" + line[m.end():]
    return line.rstrip() + f" {key}={value}"


def without(line: str, key: str) -> str:
    """A KDL entry line with `key` taken off."""
    return re.sub(rf"\s+{key}=(\"[^\"]*\"|\S+)", "", line)


SIDE = {"n": "north", "e": "east", "s": "south", "w": "west"}


def passages(region, block: kdl.Node) -> list[tuple[str, str, list, list, float, float]] | None:
    """Each way between two rooms of a packed block as its map draws it: the rooms, each one's door
    in cells, the walk from one room's centre to the other's by the way, and the straight line
    between them, in feet; None where its rooms are not placed. A way no passage fits is left out."""
    members = [m.strip() for m in str(block.props["locations"]).split(",")]
    dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    if not members or not all(space.centre(dress.get(c)) for c in members):
        return None
    file = built(region.code, str(block.args[0]))[0]
    if file is None:
        return None
    m = json.loads(file.read_text())
    f, cell = engine("facts", m), m["scale"]["perCell"]
    label = {r["id"]: r["label"] for r in f.get("rooms", [])}
    centre = {r["id"]: (r["box"]["cells"]["x"] + r["box"]["cells"]["w"] / 2, r["box"]["cells"]["y"] + r["box"]["cells"]["h"] / 2)
              for r in f.get("rooms", [])}
    walk = lambda pts: sum(math.dist(p, q) for p, q in zip(pts, pts[1:])) * cell
    out, seen = [], set()
    for c in f.get("corridors", []):
        a, b, path = c["from"].get("room"), c["to"].get("room"), c.get("path", [])
        if a in centre and b in centre and len(path) >= 4 and not any(x["id"] == "maze-no-route" and x["path"] == f"corridors[{c['index']}]"
                                                                      for x in engine("check", m).get("warnings", [])):
            pts = list(zip(path[::2], path[1::2]))
            out.append((label[a], label[b], list(pts[0]), list(pts[-1]), walk([centre[a], *pts, centre[b]]),
                        math.dist(centre[a], centre[b]) * cell))
    doors = {d["connection"]: d["at"] for d in f.get("doors", []) if d.get("connection") is not None}
    for r in f.get("rooms", []):
        for k in r.get("connections", []):
            if k["connection"] not in seen and k["to"] in centre and (at := k.get("at") or doors.get(k["connection"])):
                seen.add(k["connection"])
                out.append((r["label"], label[k["to"]], at, at, walk([centre[r["id"]], at, centre[k["to"]]]),
                            math.dist(centre[r["id"]], centre[k["to"]]) * cell))
    return out


def faults(region, block: kdl.Node, detour: float | None) -> tuple[list[str], list[tuple[str, str, float]]] | None:
    """A packed block's ways its map draws no passage for, and those that walk more than `detour`
    feet past the straight line between their rooms' centres, with how far; None where its rooms
    are not placed."""
    drawn = passages(region, block)
    if drawn is None:
        return None
    members = {m.strip() for m in str(block.props["locations"]).split(",")}
    pairs = {tuple(sorted((str(n.args[0]), str(n.props["to"])), key=number)) for n in region.files.get("Connections", [])
             if n.args and str(n.args[0]) in members and str(n.props.get("to")) in members}
    have = {frozenset((a, b)) for a, b, *_ in drawn}
    return ([f"{a} to {b}" for a, b in sorted(pairs, key=lambda p: (number(p[0]), number(p[1]))) if frozenset((a, b)) not in have],
            [(a, b, walk - line) for a, b, _, _, walk, line in drawn if detour is not None and walk - line > detour])


@functools.cache
def walks(code: str, setting: Path = tables.SETTING) -> dict[tuple[str, str], tuple[str, int]]:
    """Each way between two rooms of a packed block of the region, both ways round: the wall it
    leaves by - the one its Connection names, else the side its door stands on, else its door's
    compass point - and its walk to the next room's centre, to the nearest 5 feet."""
    region = world_for(setting).regions[code]
    compass, out = space.compass(), {}
    for block in blocks_of(region).values():
        members = [m.strip() for m in str(block.props["locations"]).split(",")]
        named = {k: compass[round(v / 22.5) % 16] for k, v in walls_of(region, members).items()}
        file = built(region.code, str(block.args[0]))[0]
        boxes = {r["label"]: r["box"]["cells"] for r in engine("facts", json.loads(file.read_text())).get("rooms", [])} if file else {}
        for a, b, door_a, door_b, how, _ in passages(region, block) or ():
            for here, there, (x, y) in ((a, b, door_a), (b, a, door_b)):
                r = boxes[here]
                side = next((s for s, hit in (("w", abs(x - r["x"])), ("e", abs(x - r["x"] - r["w"])),
                                              ("n", abs(y - r["y"])), ("s", abs(y - r["y"] - r["h"]))) if hit < 1e-6), None)
                toward = math.degrees(math.atan2(x - r["x"] - r["w"] / 2, r["y"] + r["h"] / 2 - y)) % 360
                out[here, there] = (named.get((here, there)) or SIDE.get(side) or compass[round(toward / 22.5) % 16],
                                    round(how / 5) * 5)
    return out


def glued(region, members: list[str], dress: dict) -> tuple[dict, list[str]]:
    """Each room of a block placed against another, as (that room, feet east, feet south of it)
    for the packer, where the dry fire would place it; and why any cannot be packed so."""
    glue, why = {}, []
    for c in members:
        d = dress[c]
        if "against" not in d.props:
            continue
        a = space.anchor_of(d.props["against"])
        if a is None or a[0] not in members or a[1] in ("above", "below"):
            why.append(f"{c} is placed against {d.props['against']}: a level is packed flat, against another of its rooms")
            continue
        xy = space.touching(space.outline_of(dress[a[0]]), (0.0, 0.0), space.outline_of(d), a[1],
                            space.point_of(d.props.get("xyz")) or [0.0, 0.0, None])
        if xy is None:
            why.append(f"{c} is placed against {a[0]} {a[1]}, and their outlines never meet there")
            continue
        corner = [xy[k] + (float(dress[a[0]].props[n]) - float(d.props[n])) / 2 for k, n in ((0, "width"), (1, "length"))]
        if any(round(v, 6) % LATTICE for v in corner):
            why.append(f"{c}'s place against {a[0]} puts its corners off the {LATTICE}-foot lattice: "
                       f"keep its slide and gap on it")
            continue
        glue[c] = (a[0], xy[0], -xy[1])
    return glue, why


def unbear_stairs(code: str) -> list[str]:
    """Takes the bearing and distance off each stair to or from the region whose two rooms are
    both placed, on both its sides: it stands one room over the other, which their places say."""
    s, out = space.settled(), []
    for region in s.world.regions.values():
        path = region.dir / "Connections.md"
        lines, changed = path.read_text().split("\n") if path.exists() else [], False
        for n in region.files.get("Connections", []):
            a, b = str(n.args[0]), str(n.props.get("to"))
            if code not in (a.split(".")[0], b.split(".")[0]) or not s.stair(region, n) \
                    or "bearing" not in n.props and "distance" not in n.props:
                continue
            if all((t := s.things.get(c)) and t.at[0] is not None for c in (a, b)):
                lines[n.line - 1] = without(without(lines[n.line - 1], "bearing"), "distance")
                changed = True
                out.append(f"{a} to {b}")
        if changed:
            path.write_text("\n".join(lines))
    if out:
        space.refresh()
    return out


CELL = 5                        # feet to a cell in a layout graph
MARGIN = 2                      # cells artgen's layout leaves round the footprint


def held_of(region, members: list[str], dress: dict) -> dict[str, tuple[float, float]]:
    """Each placed room of a block with a way out of it that states a bearing and distance, at its
    place: the place beyond was set from it, so it keeps that place."""
    return {c: at for n in region.files.get("Connections", [])
            if n.args and (c := str(n.args[0])) in members and str(n.props.get("to")) not in members
            and "bearing" in n.props and "distance" in n.props and (at := space.centre(dress.get(c)))}


def framed(poly: list | None, side: float | None):
    """The function that turns a place in feet, east and north of a block's centre, into cells from the
    footprint's top-left: the polygon's own corner, else the centre of a square of `side` feet."""
    ox, oy = (min(x for x, _ in poly), min(-y for _, y in poly)) if poly else (-(side or 0) / 2,) * 2
    return lambda x, y: [round((x - ox) / CELL, 3), round((-y - oy) / CELL, 3)]


def held_over(pin: tuple, frame) -> dict:
    """A room that must stand over a box, (east, north, width, length) of its block's centre in feet, as a graph's `over`."""
    e, n, w, h = pin
    x, y = frame(e - w / 2, n + h / 2)
    return {"x": x, "y": y, "w": w / CELL, "h": h / CELL}


def graph_shell(gid: str, rooms: list, ways: list, rates: dict, seed: int, tries: int, poly: list | None,
                side: float | None, rocks: list, frame) -> dict:
    """A layout graph round its rooms and ways: BRIEF.md's fill, passages and detour, and the ground - the
    polygon or the square - with each Rock's outline kept out. `rocks` are ((x, y), outline) in feet."""
    g = {"id": gid, "rooms": rooms, "ways": ways,
         "width": LATTICE / CELL, "scale": {"perCell": CELL, "unit": "ft"}, "fill": list(rates["fill"]),
         "passages": rates["passages"], "seed": seed, "tries": tries, "margin": MARGIN}
    if rates["detour"] is not None:
        g["detour"] = rates["detour"] / CELL
    if poly:
        g["footprint"] = [v for x, y in poly for v in frame(x, y)]
    elif side:
        g["footprint"] = side / CELL
    if rocks:
        g["keepOut"] = [[v for x, y in space.polygon(s, at[0], at[1]) for v in frame(x, y)] for at, s in rocks]
    return g


def graph_of(region, block: kdl.Node, rates: dict, seed: int, tries: int, far: set) -> dict | str:
    """A block's layout graph for `artgen dungeon layout`, in 5-foot cells: its rooms, each way
    with the bearing it keeps - out past the wall it names, else as its rooms lie unless that
    way detours, else as its Connection says - and its ground; or why it cannot be packed. A room
    held (`held_of`) stands over its own place, and one a stair comes down into over that room."""
    members = sorted((m.strip() for m in str(block.props["locations"]).split(",")), key=number)
    dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    compass = space.compass()
    o = space.outline_value(block.props.get("outline"))
    poly = o[1] if o and o[0] == "poly" else None
    side = None if poly else rates["footprint"]
    held = held_of(region, members, dress)
    pins = {c: over for c in members if (over := space.settled().pin(c))}
    pins |= {c: (x, y, float(dress[c].props["width"]), float(dress[c].props["length"])) for c, (x, y) in held.items()}
    rocks = [(space.point_of(r.props.get("xyz")) or [0.0, 0.0], s) for r in rocks_of(region, str(block.args[0]))
             if (s := space.outline_value(r.props.get("outline"))) is not None]
    if side is None and not poly and (pins or rocks):
        return "BRIEF.md states no pack footprint, and a stair or Rock needs the square's frame"
    glue, why = glued(region, members, dress)
    if why:
        return "\n".join(why)
    frame = framed(poly, side)
    rooms = []
    for c in members:
        d = dress.get(c)
        if d is None or "width" not in d.props or "length" not in d.props:
            return f"{c} states no width and length"
        shape, points = footprint(d)
        r = {"id": c, "w": int(d.props["width"]) / CELL, "h": int(d.props["length"]) / CELL, "shape": shape,
             "hall": str(d.props.get("shape")) == "hall", "turns": turns(region, c, dress)}
        if points:
            r["points"] = [v / CELL for p in points for v in p]
        if c in glue:
            r["against"] = {"room": glue[c][0], "dx": glue[c][1] / CELL, "dy": glue[c][2] / CELL}
        if c in pins:
            r["over"] = held_over(pins[c], frame)
        rooms.append(r)
    placed = {c: at for c in members if (at := space.centre(dress[c]))}
    walls, ways, seen = walls_of(region, members), [], set()
    for n in region.files.get("Connections", []):
        a, b = str(n.args[0]), str(n.props.get("to"))
        if a not in members or b not in members:
            continue
        if frozenset((a, b)) in seen:                    # the second of a pair says only its own wall
            if (a, b) in walls:
                ways.append({"a": a, "b": b, "wall": walls[a, b]})
            continue
        seen.add(frozenset((a, b)))
        if (a, b) in walls or (b, a) in walls:           # the far room lies out past the wall it names
            bearing = walls[a, b] if (a, b) in walls else (walls[b, a] + 180) % 360
        elif a in placed and b in placed and not {(a, b), (b, a)} & far:   # a detour's line is no guide
            bearing = math.degrees(math.atan2(placed[b][0] - placed[a][0], placed[b][1] - placed[a][1])) % 360
        else:
            bearing = compass.index(str(n.props["bearing"])) * 22.5 if "bearing" in n.props else None
        ways.append({"a": a, "b": b, **({"bearing": bearing} if bearing is not None else {}),
                     **({"wall": walls[a, b]} if (a, b) in walls else {})})
    return graph_shell(f"{region.code}-{str(block.args[0]).split('.')[-1]}", rooms, ways, rates, seed, tries, poly, side, rocks, frame)


def pack_region(code: str, seed: int = 1, again: bool = False, tries: int = 12) -> int:
    """Packs each block of a DANGEROUS region with `artgen dungeon layout`: its rooms close in its
    footprint, each way a door through a shared wall or a passage within BRIEF.md's detour,
    keeping each way's direction as its rooms lie, or else as its bearing says. Writes each
    room's `xyz` from the block's centre to Dressing.md and the block's `outline` to Blocks.md, and
    takes `bearing` and `distance` off each way within the block, which the rooms' positions now
    place. A block whose rooms are placed and whose ways all route within BRIEF.md's detour on its
    map is left where it lies, unless `again`. Of `tries` packings, the one
    whose ways walk least is kept. A room that turns (`turns`) is written as it now lies: its
    width and length, and its outline. A room placed against another keeps its line and is
    carried with it. A room with a way out of the block that states a bearing and distance keeps
    its place. A stair whose two rooms are now placed loses its bearing and distance. The
    region is settled before (over the block a stair reaches) and after (where a way with a
    bearing puts it): tools/space.py."""
    for line in space.settle(code):
        print(f"settled {line}")
    world = world_for(tables.SETTING)
    region = world.regions[code]
    if region.rating.upper() != "DANGEROUS":
        print(f"{code} is {region.rating}: only a DANGEROUS region's blocks are packed")
        return 1
    rates = tables.Brief(world.schema).packing(code)
    if rates["fill"] is None or rates["passages"] is None:
        print(f"BRIEF.md states no pack fill and passages for {code}")
        return 1
    files = {k: (region.dir / f"{k}.md") for k in ("Dressing", "Blocks", "Connections")}
    text = {k: f.read_text().split("\n") for k, f in files.items()}
    failed = False
    for bid, block in blocks_of(region).items():
        if bid in maps.designed(region):
            print(f"{bid} has an approved design: its places come from step 3d (`python3 tools/design.py`), not `pack`")
            failed = True
            continue
        members = [m.strip() for m in str(block.props["locations"]).split(",")]
        found = faults(region, block, rates["detour"])
        poly = (o := space.outline_value(block.props.get("outline"))) is not None and o[0] == "poly"   # the design's own ground
        sized = poly or rates["footprint"] is None or side_of(block) == rates["footprint"]
        far = {(a, b) for a, b, _ in found[1]} if found else set()
        side = None
        if found and not found[0] and sized and not far and not again:
            print(f"{bid}: packed, and every way routes within its detour; left where it lies (--again repacks it)")
        else:
            g = graph_of(region, block, rates, seed, tries, far)
            if isinstance(g, str):
                print(g)
                return 1
            with tempfile.TemporaryDirectory() as tmp:
                (Path(tmp) / "graph.json").write_text(json.dumps(g))
                done = artgen("dungeon", "layout", "--file", Path(tmp) / "level.json", "--graph", Path(tmp) / "graph.json",
                              "--seed", seed, "--json", "--force")
            if done.returncode:
                print(f"{bid}: {done.stderr.strip() or done.stdout.strip()}")
                failed = True
                continue
            out = json.loads(done.stdout)
            report, laid = out["report"], {r["label"]: r for r in out["dungeon"]["rooms"]}
            side = report["side"] * CELL
            ox, oy = (min(x for x, _ in o[1]), min(-y for _, y in o[1])) if poly else (-side / 2,) * 2
            at = {c: ((r["x"] + r["w"] / 2 - MARGIN) * CELL + ox, -((r["y"] + r["h"] / 2 - MARGIN) * CELL + oy))
                  for c, r in laid.items()}
            dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
            moved = [c for c, xy in held_of(region, members, dress).items() if math.dist(xy, at[c]) > 0.5]
            if report["left"] or moved:
                print(f"{bid}: " + "; ".join([f"no passage fits the way from {w}" for w in report["left"]] +
                                             [f"{c} left the place its way out of the block holds" for c in moved])
                      + "; try another --seed")
                failed = True
                continue
            print(f"{bid}: {len(members)} rooms in {'its outline' if poly else f'a square {side:g} feet across'}, room "
                  f"{report['fill']:.0%} of it; {report['passages']} passages, {report['walls']} shared walls, "
                  f"{report['corridorCells'] * LATTICE} feet of corridor")
            lies = {}                                     # a turned room, as it now lies
            for c, r in laid.items():
                w, h = round(r["w"] * CELL), round(r["h"] * CELL)
                pts = [((x - r["x"] - r["w"] / 2) * CELL, (r["y"] + r["h"] / 2 - y) * CELL)
                       for x, y in zip(r["points"][::2], r["points"][1::2])] if "points" in r else None
                was = space.outline_value(dress[c].props.get("outline"))
                if (w, h) != (int(dress[c].props["width"]), int(dress[c].props["length"])) or pts and (was is None or \
                        [tuple(round(v, 3) for v in q) for q in was[1]] != [tuple(round(v, 3) for v in q) for q in pts]):
                    lies[c] = (w, h, pts)
            for d in report["detours"]:
                print(f"{bid}: the way from {d['a']} to {d['b']} walks {d['extra'] * CELL:.0f} feet out of its way, past "
                      f"BRIEF.md's pack detour of {rates['detour']:g}; try another --seed")
            if lies:
                print(f"{bid}: turned {', '.join(lies)}")
            for i, line in enumerate(text["Dressing"]):
                if (m := re.match(r"Dressing (\S+) ", line)) and m[1] in lies:
                    w, h, pts = lies[m[1]]
                    line = with_prop(with_prop(line, "width", str(w)), "length", str(h))
                    if pts:
                        line = with_prop(line, "outline", '"poly ' + " ".join(f"{x + 0:g},{y + 0:g}" for x, y in pts) + '"')
                    text["Dressing"][i] = line
                if (m := re.match(r"Dressing (\S+) ", line)) and m[1] in at and "against=" not in line:   # an anchor holds its own
                    text["Dressing"][i] = with_prop(text["Dressing"][i], "xyz", f'"{round(at[m[1]][0])},{round(at[m[1]][1])}"', after="length")
            for i, line in enumerate(text["Connections"]):
                if (m := re.match(r"Connection (\S+) to=\"(\S+)\"", line)) and m[1] in members and m[2] in members:
                    text["Connections"][i] = without(without(line, "bearing"), "distance")
        for i, line in enumerate(text["Blocks"]):
            if line.startswith(f"Block {bid} ") and side and not poly:
                text["Blocks"][i] = with_prop(line, "outline", f'"rect {side:g} {side:g}"')
    if failed:
        return 1
    for k, f in files.items():
        f.write_text("\n".join(text[k]))
    space.refresh()
    for line in space.settle(code):
        print(f"settled {line}")
    if stairs := unbear_stairs(code):
        print(f"stairs now placed, their bearings taken off: {', '.join(stairs)}")
    return 0


# -- problems: what the validator reports of a packed block ------------------------------

def side_of(block: kdl.Node) -> float | None:
    """The side of the square a packed block's rooms lie in: its outline, a "rect S S"."""
    o = space.outline_value(block.props.get("outline"))
    return o[1] if o and o[0] == "rect" and o[1] == o[2] else None


def problems(region, block: kdl.Node) -> list[tuple[str, Path, str]]:
    """What is wrong with a block, as (level, file, message). A room is a hall where it is one
    passage wide and at least twice as long, and only there. An unpacked block is a warning.
    A packed one has BRIEF.md's footprint as its outline, its rooms covering the least of
    BRIEF.md's fill, a passage on its map for every way and within BRIEF.md's detour, its rooms
    within its outline and off its Rock, no bearing or distance on a way within it, and nothing
    wrong with its map (`defects`). Where its rooms
    lie, against its outline and the blocks a stair joins it to, is tools/space.py's.
    """
    bid, path = str(block.args[0]), region.dir / "Blocks.md"
    dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    members = [m.strip() for m in str(block.props.get("locations", "")).split(",") if m.strip()]
    at = {c: xy for c in members if (xy := space.centre(dress.get(c)))}
    out, across = [], region.passage(block, "width")
    for c in members:
        if c in dress and "width" in dress[c].props and "length" in dress[c].props:
            narrow, long = sorted(float(dress[c].props[k]) for k in ("width", "length"))
            fits, said = narrow <= across and long >= 2 * narrow, str(dress[c].props.get("shape")) == "hall"
            if fits != said:
                out.append(("error", region.dir / "Dressing.md",
                            f"{c} is {narrow:g} by {long:g} feet, {'' if fits else 'not '}one passage ({across:g} feet) wide and "
                            f"at least twice as long, so its shape is {'' if fits else 'not '}hall (step 4a)"))
            o = space.outline_value(dress[c].props.get("outline"))
            if o and o[0] == "poly":
                xs, ys = [q[0] for q in o[1]], [q[1] for q in o[1]]
                if max(xs) + min(xs) or max(ys) + min(ys):
                    out.append(("error", region.dir / "Dressing.md",
                                f"{c}'s outline is not centred on its place: its extent runs as far each way (step 4a)"))
    if not at:
        return out + [("warning", path, f"{bid}'s rooms are not packed: run `python3 tools/maps.py pack {region.code}` (step 4a)")]
    side, o = side_of(block), space.outline_value(block.props.get("outline"))
    poly = bool(o and o[0] == "poly")
    if side is None and not poly:
        return out + [("error", path, f'{bid} places its rooms but states no outline, "rect S S" or a poly, that they are packed in')]
    wide = lambda c, k: float(dress[c].props["width" if k == 0 else "length"])
    world = world_for(tables.SETTING)
    rates = tables.Brief(world.schema).packing(region.code)
    if not poly and rates["footprint"] is not None and side != rates["footprint"]:
        out.append(("error", path, f"{bid}'s square is {side:g} feet, where BRIEF.md's pack footprint asks {rates['footprint']:g}: "
                                   f"run `python3 tools/maps.py pack {region.code}` (step 4a)"))
    rock = sum(area(space.polygon(r, xy[0], xy[1])) for n in rocks_of(region, bid)
               if (r := space.outline_value(n.props.get("outline"))) is not None and (xy := space.point_of(n.props.get("xyz")) or [0.0, 0.0]))
    room = (area(o[1]) if poly else side * side) - rock
    covered, least = sum(wide(c, 0) * wide(c, 1) for c in at), (rates["fill"] or (0, 0))[0]
    if covered < least * room:
        out.append(("error", path, f"{bid}'s rooms cover {covered / room:.0%} of its ground, under BRIEF.md's "
                                   f"pack fill of {least:.0%}"))
    left, far = faults(region, block, rates["detour"]) or ([], [])
    for way in left:
        out.append(("error", path, f"{bid}: no passage fits the way from {way}: run `python3 tools/maps.py pack {region.code}` (step 4a)"))
    for a, b, extra in far:
        out.append(("warning", path, f"{bid}: the way from {a} to {b} walks {extra:.0f} feet out of its way, past "
                                     f"BRIEF.md's pack detour of {rates['detour']:g}: run `python3 tools/maps.py pack {region.code}` (step 4a)"))
    if mapfile := built(region.code, bid)[0]:
        for level, d in defects(region, block, json.loads(mapfile.read_text())):
            out.append((level, path, f"{bid}'s map: {d}"))
    for n in region.files.get("Connections", []):
        if str(n.args[0]) in at and str(n.props.get("to")) in at and ("bearing" in n.props or "distance" in n.props):
            out.append(("error", region.dir / "Connections.md",
                        f"line {n.line}: {n.args[0]} to {n.props['to']} states a bearing or distance, which its rooms' "
                        f"places give: take it off"))
    return out
