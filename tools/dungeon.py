"""A DANGEROUS block: its map, its passages, its packing, and what is wrong with it.

block_map    the artgen dungeon file for a block, from its Dressing, Connections and Blocks
plan_of      a packed block's routes, from the positions its Dressing states
pack_region  `python3 tools/maps.py pack`: a region's blocks packed and routed (tools/pack.py,
             tools/route.py), and the positions written to its tables
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
import mapcheck
import pack as packing
import route
import space
import tables
from maps import ARTGEN, CACHE, UNSIZED, artgen, blocks_of, built, feet, world_for

DOOR = {"Open": None, "Archway": None, "Broken": None, "Crude": None, "Lift": None, "Chute": None, "Iron": "portcullis"}
GAP = {"Archway": "arch"}       # a doorless way through a shared wall, else open
DRAWN = {"rect": "rect", "cave": "cave", "round": "circle"}    # artgen's shape for a footprint's, else a poly of its outline
APART = 10                      # feet two routes to one room may disagree by
EDGE = 6                        # cells of map beyond the rooms, for the ways out of it
EXIT = 4                        # cells a way out of the block runs past its room's wall
MAX_CELLS = 150
CELLS = (5, 10, 20)             # feet to a cell, the finest that fits the block
STAIR_INSET = 1.2               # cells between a stair mark's centre and the wall it stands by
STAIR_HALF = 0.8                # half a stair mark, in cells
STAIR_TIGHT = 0.5               # cells from the wall, in a room too small for anything better
NAME_HALF = 0.7                 # half the height of a room's code, in cells
ROUTED_CELLS = (5, 10)          # and where its passages are routed on route.LATTICE
ROUTED_WALL = 2.5               # a routed block's wall stroke, so a wall between two floors reads as one, its rock hatched
                                # and a wall drawn between every two rooms that touch


def footprint(d: kdl.Node | None, x: float = 0.0, y: float = 0.0) -> route.Footprint:
    """A room's footprint from its Dressing, its box's top left at (x, y) feet east and south: its
    own poly outline, else its shape in its width and length."""
    p = d.props if d is not None else {}
    w, h = float(p.get("width", UNSIZED)), float(p.get("length", UNSIZED))
    o = space.outline_value(p.get("outline"))
    if o and o[0] == "poly":
        return route.Footprint(x, y, w, h, "poly", tuple((a, -b) for a, b in o[1]))
    shape = str(p.get("shape", "rect"))
    return route.Footprint(x, y, w, h, "rect" if shape == "hall" else shape)


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


def walls_of(region, members) -> dict[tuple[str, str], float]:
    """The wall each way within a block names at the room it leaves, as a bearing in degrees."""
    compass = space.compass()
    return {(str(n.args[0]), str(n.props["to"])): compass.index(str(n.props["wall"])) * 22.5
            for n in region.files.get("Connections", [])
            if n.args and str(n.args[0]) in members and str(n.props.get("to")) in members and str(n.props.get("wall")) in compass}


def facing(dx: float, dy: float) -> str:
    """The wall, n, e, s or w, facing a displacement in cells, y running south."""
    return ("e" if dx > 0 else "w") if abs(dx) > abs(dy) else ("s" if dy > 0 else "n")

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
        first = next(iter(at))
        shift = [(-(at[first][k] - size[first][k] / 2)) % route.LATTICE for k in (0, 1)]
        at = {c: (at[c][0] + shift[0], at[c][1] + shift[1]) for c in at}
        for c in at:
            if any(abs((at[c][k] - size[c][k] / 2) / route.LATTICE - round((at[c][k] - size[c][k] / 2) / route.LATTICE)) > 1e-6
                   for k in (0, 1)):
                problems.append(f"{c} does not lie on the {route.LATTICE}-foot lattice")
    rects = {c: route.Footprint(at[c][0] - size[c][0] / 2, at[c][1] - size[c][1] / 2, size[c][0], size[c][1],
                                size[c][2].shape, size[c][2].points) for c in at}
    for i, a in enumerate(list(at)):
        for b in list(at)[i + 1:]:
            if all(abs(at[a][k] - at[b][k]) < (size[a][k] + size[b][k]) / 2 - APART / 5 for k in (0, 1)) \
                    and (not routed or rects[a].square and rects[b].square or rects[a].touched & rects[b].touched):
                problems.append(f"{a} and {b} overlap")
    lo = [min(at[c][i] - size[c][i] / 2 for c in at) for i in (0, 1)]
    hi = [max(at[c][i] + size[c][i] / 2 for c in at) for i in (0, 1)]
    fits = ROUTED_CELLS if routed else CELLS
    cell = next((f for f in fits if max(hi[i] - lo[i] for i in (0, 1)) / f + 2 * EDGE <= MAX_CELLS), fits[-1])
    cols, rows = (max(4, math.ceil((hi[i] - lo[i]) / cell) + 2 * EDGE) for i in (0, 1))
    cx = lambda c: (at[c][0] - lo[0]) / cell + EDGE
    cy = lambda c: (at[c][1] - lo[1]) / cell + EDGE
    rid = lambda c: c.replace(".", "-")
    m = {"id": f"{code}-{bid.split('.')[-1]}", "version": 1, "seed": 1, "cols": cols, "rows": rows,
         "gen": {"rooms": 1, "minSize": 3, "maxSize": 8, "caves": 0, "round": 0, "loops": 0, "doors": 0,
                 "corridorWidth": 1, "spacing": 2, "entrance": False},
         "grid": {"show": True, "size": 2, "sub": True, "clip": "floor"},
         "style": {"hatch": "band", "band": 0.9, "wall": 1}, "scale": {"perCell": cell, "unit": "ft"},
         "numbers": False, "scaleBar": True, "compass": False, "furniture": {"place": "outside"},
         "rooms": [], "corridors": [], "connections": [], "overlay": {"labels": [], "symbols": []}}
    if routed:
        m["style"].update(wall=ROUTED_WALL, hatch="full", sharedWalls=True)
    for c in at:
        w, h, fp = size[c]
        shape = DRAWN.get(fp.shape, "poly")
        m["rooms"].append({"id": rid(c), "shape": shape, "x": round(cx(c) - w / 2 / cell, 2),
                           "y": round(cy(c) - h / 2 / cell, 2), "w": max(1, round(w / cell, 2)),
                           "h": max(1, round(h / cell, 2)), "label": c, "number": False, "origin": "tables"})
        if shape == "poly":
            m["rooms"][-1]["points"] = [round(v, 2) for x, y in rects[c].outline
                                        for v in ((x - lo[0]) / cell + EDGE, (y - lo[1]) / cell + EDGE)]

    def door(n):
        kids = {k.name for k in n.children}
        if "Lock" in kids:
            return "locked"
        if "Secret" in kids:
            return "secret"
        return DOOR.get(str(n.props.get("type")), "door")

    def touch(a, b) -> bool:
        """Rooms a and b share a wall: they meet along one axis and overlap along the other."""
        d = [abs(cx(a) - cx(b)) * cell, abs(cy(a) - cy(b)) * cell]
        reach = [(size[a][k] + size[b][k]) / 2 for k in (0, 1)]
        return size[a][2].square and size[b][2].square and any(
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
                if size[c][2].square else round(size[c][1 - k] / 2 / cell, 2)
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
    seen, marked = {}, {}
    for n in ways:
        a, b = str(n.args[0]), str(n.props["to"])
        if a in at and b in at:
            key = tuple(sorted((a, b)))
            ends = seen.setdefault(key, {})
            ends[a] = (door(n), n)
        elif a in at:                                     # a way out of the block: a mark in its room
            v = step(n) or toward(n)
            if v is None:
                problems.append(f"{a} to {b} states no bearing and distance")
                continue
            ux, uy = v[0] / math.hypot(*v), v[1] / math.hypot(*v)
            hw, hh = size[a][0] / 2 / cell, size[a][1] / 2 / cell
            inset = lambda h: max(0.0, h - STAIR_INSET)
            spots = [(sx_ * inset(hw), sy_ * inset(hh)) for sx_ in (-1, 0, 1) for sy_ in (-1, 0, 1) if sx_ or sy_]
            spots.sort(key=lambda p: -(p[0] * ux + p[1] * uy) / (math.hypot(*p) or 1))     # nearest the wall it faces first
            lw = (0.8 * len(a) + 1) / 2 + STAIR_HALF                    # clear of the room's own code
            fits = [p for p in spots if abs(p[0]) >= lw or abs(p[1]) >= NAME_HALF + STAIR_HALF]
            if not fits:                                        # no room beside the code: stand it nearer the wall
                tight = [(sx_ * max(0.0, hw - STAIR_TIGHT), sy_ * max(0.0, hh - STAIR_TIGHT)) for sx_ in (-1, 0, 1)
                         for sy_ in (-1, 0, 1) if sx_ or sy_]
                tight.sort(key=lambda p: -(p[0] * ux + p[1] * uy) / (math.hypot(*p) or 1))
                spots = tight
                fits = [p for p in spots if abs(p[0]) >= lw or abs(p[1]) >= NAME_HALF + STAIR_HALF]
            clear = lambda ps: [p for p in ps if all(math.dist(p, q) >= 2 * STAIR_HALF for q in marked.get(a, []))]
            spot = (clear(fits) or clear(spots) or fits or spots)[0]   # clear of a mark already in the room
            marked.setdefault(a, []).append(spot)
            sx, sy = cx(a) + spot[0], cy(a) + spot[1]
            climb = n.props.get("climb")
            up = bool(climb) and int(climb) > 0
            down = bool(climb) and int(climb) < 0
            m["overlay"]["symbols"].append({"kind": "stairs-up" if up else "stairs-down" if down else "arrow",
                                            "x": round(sx, 2), "y": round(sy, 2), "scale": 1.0, "origin": "tables",
                                            "angle": round(math.degrees(math.atan2(uy, ux)) % 360)})
            m["overlay"]["labels"].append({"text": f"{'Up to' if up else 'Down to' if down else 'To'} {b}",
                                           "x": round(sx, 2), "y": round(sy + 2.2, 2), "kind": "note", "origin": "tables"})
    if routed:
        found, left = route.plan(rects, list(seen), walls_of(region, members))
        problems += [f"no passage fits the way from {x}" for x in left]
        to_cell = lambda p: (round((p[0] - lo[0]) / cell + EDGE, 2), round((p[1] - lo[1]) / cell + EDGE, 2))
        along = lambda c, side, p: round(((p[0] - rects[c].x) if side in "ns" else (p[1] - rects[c].y)) / cell, 2)
        for rt in found:
            ends = seen[tuple(sorted((rt.a, rt.b)))]
            first, second = ends.get(rt.a), ends.get(rt.b)
            rn = [n for _, n in ends.values()]
            if rt.kind == "wall":                         # a door through the wall the rooms share
                kind, n = first or second
                m["connections"].append({"a": rid(rt.a), "b": rid(rt.b), "at": list(to_cell(rt.door_a)), "origin": "tables",
                                         "kind": kind or GAP.get(str(n.props.get("type")), "open")})
                mid = rt.door_a
            else:
                pts = rt.points()
                lead_a, lead_b = rects[rt.a].lead(rt.side_a, rt.door_a), rects[rt.b].lead(rt.side_b, rt.door_b)
                end = lambda c, side, door: {"room": rid(c), "side": side, "offset": along(c, side, door)} \
                    if rects[c].square and side else {"room": rid(c)}     # else drawn from its hub, through the door
                m["corridors"].append({"from": end(rt.a, rt.side_a, rt.door_a), "to": end(rt.b, rt.side_b, rt.door_b),
                                       "via": [v for p in lead_a + pts[1:-1] + lead_b[::-1] for v in to_cell(p)],
                                       "width": round(route.LATTICE / cell, 2), "origin": "tables",
                                       **({"style": "natural"} if rough(*rn) else {}),
                                       "doors": [first[0] if first else None, second[0] if second else None]})
                run = [math.dist(p, q) for p, q in zip(pts, pts[1:])]
                half, mid = sum(run) / 2, pts[0]
                for p, q, d in zip(pts, pts[1:], run):
                    if half <= d:
                        mid = (p[0] + (q[0] - p[0]) * half / (d or 1), p[1] + (q[1] - p[1]) * half / (d or 1))
                        break
                    half -= d
            if any(c.name == "Hazard" for n in rn for c in n.children):
                m["overlay"]["symbols"].append({"kind": "trap", "x": to_cell(mid)[0], "y": to_cell(mid)[1], "origin": "tables"})
        return m, problems
    for (a, b), ends in seen.items():
        first, second = ends.get(a), ends.get(b)
        if touch(a, b):                                  # through the wall they share
            kind, n = first or second
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
    A routed passage is already round them. The answer is kept under .maps-cache."""
    if all("via" in c for c in m["corridors"]):
        return
    key = hashlib.sha256((json.dumps(m) + ARTGEN.parent.joinpath("VERSION").read_text()).encode()).hexdigest()
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
                if "via" not in m["corridors"][i]:                # a routed passage is already round them
                    fix(m["corridors"][i])
    CACHE.mkdir(exist_ok=True)
    kept.write_text(json.dumps(m["corridors"]))


def defects(region, block: kdl.Node, m: dict) -> list[str]:
    """What tools/mapcheck.py finds wrong in a block's map file, held to the tables' ways."""
    members = {x.strip() for x in str(block.props["locations"]).split(",")}
    dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    if not all(space.centre(dress.get(c)) for c in members):
        return []                                         # not packed: its corridors are left to artgen
    rid = lambda c: c.replace(".", "-")
    ways = {frozenset((rid(str(n.args[0])), rid(str(n.props["to"])))) for n in region.files.get("Connections", [])
            if n.args and str(n.args[0]) in members and str(n.props.get("to")) in members}
    leaving = sum(1 for n in region.files.get("Connections", [])
                  if n.args and str(n.args[0]) in members and str(n.props.get("to")) not in members)
    return mapcheck.check(m, ways, leaving)


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


def plan_of(region, block: kdl.Node):
    """A packed block's routes, from the positions its Dressing states: (routes, rects, what no
    passage fitted), or None where its rooms state no xyz."""
    members = [m.strip() for m in str(block.props["locations"]).split(",")]
    dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    if not members or not all(space.centre(dress.get(c)) and "width" in dress[c].props and "length" in dress[c].props
                              for c in members):
        return None
    corner = lambda c: (space.centre(dress[c])[0] - float(dress[c].props["width"]) / 2,
                        -space.centre(dress[c])[1] - float(dress[c].props["length"]) / 2)
    first = corner(members[0])
    shift = ((-first[0]) % route.LATTICE, (-first[1]) % route.LATTICE)     # corners onto the lattice, as block_map does
    rects = {c: footprint(dress[c], corner(c)[0] + shift[0], corner(c)[1] + shift[1]) for c in members}
    ways = [(str(n.args[0]), str(n.props["to"])) for n in region.files.get("Connections", [])
            if n.args and str(n.args[0]) in rects and str(n.props.get("to")) in rects]
    routes, left = route.plan(rects, ways, walls_of(region, members))
    return routes, rects, left


@functools.cache
def walks(code: str, setting: Path = tables.SETTING) -> dict[tuple[str, str], tuple[str, int]]:
    """Each way between two rooms of a packed block of the region, both ways round: the wall it
    leaves by - the one its Connection names, else its side, else its door's compass point - and
    its walk to the next room's centre, to the nearest 5 feet."""
    region = world_for(setting).regions[code]
    compass, out = space.compass(), {}
    for block in blocks_of(region).values():
        named = {k: compass[round(v / 22.5) % 16] for k, v in
                 walls_of(region, [m.strip() for m in str(block.props["locations"]).split(",")]).items()}
        for rt in (found := plan_of(region, block)) and found[0] or ():
            how = round(rt.length / 5) * 5
            for a, b, side, toward in ((rt.a, rt.b, rt.side_a, rt.bearing_a), (rt.b, rt.a, rt.side_b, rt.bearing_b)):
                out[a, b] = (named.get((a, b)) or SIDE.get(side) or compass[round(toward / 22.5) % 16], how)
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
        if any(round(v, 6) % route.LATTICE for v in corner):
            why.append(f"{c}'s place against {a[0]} puts its corners off the {route.LATTICE}-foot lattice: "
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


def pack_region(code: str, seed: int = 1, again: bool = False, tries: int = 12) -> int:
    """Packs each block of a DANGEROUS region into a square and routes its passages (tools/pack.py,
    tools/route.py), keeping each way's direction as its rooms lie, or else as its bearing says.
    Writes each room's `xyz` from the block's centre to Dressing.md and the block's
    `outline` and `router` to Blocks.md, and takes `bearing` and `distance` off each way within
    the block, which the rooms' positions now place. A block whose rooms are placed and whose
    ways all route within BRIEF.md's detour is left where it lies, its router stamped, unless
    `again`. Of `tries` packings, the one whose ways walk least is kept. A room that turns
    (`turns`) is written as it now lies: its width and length, and its outline. A room placed
    against another keeps its line and is carried with it. A stair whose two rooms are now
    placed loses its bearing and distance. The region is settled before (over
    the block a stair reaches) and after (where a way with a bearing puts it): tools/space.py."""
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
    dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    compass = list(world.schema.setting_enums["Compass"])
    files = {k: (region.dir / f"{k}.md") for k in ("Dressing", "Blocks", "Connections")}
    text = {k: f.read_text().split("\n") for k, f in files.items()}
    failed = False
    for bid, block in blocks_of(region).items():
        members = sorted((m.strip() for m in str(block.props["locations"]).split(",")), key=route.number)
        rooms = []
        for c in members:
            d = dress.get(c)
            if d is None or "width" not in d.props or "length" not in d.props:
                print(f"{c} states no width and length")
                return 1
            fp = footprint(d)
            rooms.append(packing.Room(c, int(d.props["width"]), int(d.props["length"]), fp.shape, fp.points,
                                      str(d.props.get("shape")) == "hall", turns(region, c, dress)))
        placed = {c: at for c in members if (at := space.centre(dress[c]))}
        found = plan_of(region, block)
        sized = rates["footprint"] is None or side_of(block) == rates["footprint"]
        far = {(r.a, r.b) for r, _ in route.detours(found[0], found[1], rates["detour"])} if found else set()
        if found and not found[2] and sized and not far and not again:
            print(f"{bid}: packed, and every way routes within its detour; left where it lies (--again repacks it)")
            side = None
        else:
            ways, walls = [], walls_of(region, members)
            for n in region.files.get("Connections", []):
                a, b = str(n.args[0]), str(n.props["to"])
                if a not in members or b not in members or (b, a) in [w[:2] for w in ways]:
                    continue
                if (a, b) in walls or (b, a) in walls:      # the far room lies out past the wall it names
                    bearing = walls[a, b] if (a, b) in walls else (walls[b, a] + 180) % 360
                elif a in placed and b in placed and (a, b) not in far and (b, a) not in far:   # a detour's line is no guide
                    bearing = math.degrees(math.atan2(placed[b][0] - placed[a][0], placed[b][1] - placed[a][1])) % 360
                else:
                    bearing = compass.index(str(n.props["bearing"])) * 22.5 if "bearing" in n.props else None
                ways.append((a, b, bearing))
            pins = {c: over for c in members if (over := space.settled().pin(c))}
            glue, why = glued(region, members, dress)
            if why:
                print("\n".join(why))
                return 1
            side, p, routes, energy = packing.pack(rooms, ways, seed, rates["fill"], rates["passages"],
                                                   int(rates["footprint"]) if rates["footprint"] else None, pins,
                                                   tries=tries, glue=glue, walls=walls, detour=rates["detour"])
            if routes is None:
                print(f"{bid}: no packing of {len(members)} rooms left room for every passage; try another --seed")
                failed = True
                continue
            print(f"{bid}: {len(members)} rooms in a square {side} feet across, room "
                  f"{sum(r.w * r.h for r in rooms) / side ** 2:.0%} of it; {sum(r.kind == 'path' for r in routes)} passages, "
                  f"{sum(r.kind == 'wall' for r in routes)} shared walls, {sum(len(r.cells) for r in routes) * route.LATTICE} feet of corridor")
            at = {c: (p.x[i] - side / 2, side / 2 - p.y[i]) for i, c in enumerate(members)}
            lies = {c: p.lies[i][p.o[i]][:3] for i, c in enumerate(members) if p.o[i]}
            if lies:
                print(f"{bid}: turned {', '.join(lies)}")
            for i, line in enumerate(text["Dressing"]):
                if (m := re.match(r"Dressing (\S+) ", line)) and m[1] in lies:   # as it now lies
                    w, h, pts = lies[m[1]]
                    line = with_prop(with_prop(line, "width", str(w)), "length", str(h))
                    if pts:
                        line = with_prop(line, "outline", '"poly ' + " ".join(f"{x + 0:g},{0 - y:g}" for x, y in pts) + '"')
                    text["Dressing"][i] = line
                if (m := re.match(r"Dressing (\S+) ", line)) and m[1] in at and "against=" not in line:   # an anchor holds its own
                    text["Dressing"][i] = with_prop(text["Dressing"][i], "xyz", f'"{round(at[m[1]][0])},{round(at[m[1]][1])}"', after="length")
            for i, line in enumerate(text["Connections"]):
                if (m := re.match(r"Connection (\S+) to=\"(\S+)\"", line)) and m[1] in members and m[2] in members:
                    text["Connections"][i] = without(without(line, "bearing"), "distance")
        for i, line in enumerate(text["Blocks"]):
            if line.startswith(f"Block {bid} "):
                line = with_prop(line, "outline", f'"rect {side} {side}"') if side else line
                text["Blocks"][i] = with_prop(line, "router", str(route.VERSION), after="outline")
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
    BRIEF.md's fill, passages routed by this tools/route.py and fitting every way, no bearing
    or distance on a way within it, and nothing tools/mapcheck.py finds wrong. Where its rooms
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
                elif footprint(dress[c]).hub is None:
                    out.append(("error", region.dir / "Dressing.md",
                                f"{c}'s outline has no point that sees all of it, so a way cannot be drawn to every wall (step 4a)"))
    if not at:
        return out + [("warning", path, f"{bid}'s rooms are not packed: run `python3 tools/maps.py pack {region.code}` (step 4a)")]
    side = side_of(block)
    if side is None:
        return out + [("error", path, f'{bid} places its rooms but states no outline "rect S S", the square they are packed in')]
    wide = lambda c, k: float(dress[c].props["width" if k == 0 else "length"])
    world = world_for(tables.SETTING)
    rates = tables.Brief(world.schema).packing(region.code)
    if rates["footprint"] is not None and side != rates["footprint"]:
        out.append(("error", path, f"{bid}'s square is {side:g} feet, where BRIEF.md's pack footprint asks {rates['footprint']:g}: "
                                   f"run `python3 tools/maps.py pack {region.code}` (step 4a)"))
    if str(block.props.get("router")) != str(route.VERSION):
        out.append(("error", path, f"{bid} was routed by tools/route.py version {block.props.get('router', 'unstated')}, "
                                   f"not {route.VERSION}: run `python3 tools/maps.py pack {region.code}` (step 4a)"))
    area, least = sum(wide(c, 0) * wide(c, 1) for c in at), (rates["fill"] or (0, 0))[0]
    if area < least * side * side:
        out.append(("error", path, f"{bid}'s rooms cover {area / side / side:.0%} of its footprint, under BRIEF.md's "
                                   f"pack fill of {least:.0%}"))
    routes, rects, left = plan_of(region, block)
    for way in left:
        out.append(("error", path, f"{bid}: no passage fits the way from {way}"))
    for rt, extra in route.detours(routes, rects, rates["detour"]):
        out.append(("warning", path, f"{bid}: the way from {rt.a} to {rt.b} walks {extra:.0f} feet out of its way, past "
                                     f"BRIEF.md's pack detour of {rates['detour']:g}: run `python3 tools/maps.py pack {region.code}` (step 4a)"))
    if mapfile := built(region.code, bid)[0]:
        for d in defects(region, block, json.loads(mapfile.read_text())):
            out.append(("warning" if d.startswith("label:") else "error", path, f"{bid}'s map: {d}"))
    for n in region.files.get("Connections", []):
        if str(n.args[0]) in at and str(n.props.get("to")) in at and ("bearing" in n.props or "distance" in n.props):
            out.append(("error", region.dir / "Connections.md",
                        f"line {n.line}: {n.args[0]} to {n.props['to']} states a bearing or distance, which its rooms' "
                        f"places give: take it off"))
    return out
