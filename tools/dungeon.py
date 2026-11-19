"""A DANGEROUS block: its map's passages, and what is wrong with it.

passages     a block's ways as its map draws them, from `artgen dungeon facts`
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
from maps import BUILD, CACHE, artgen, blocks_of, built

DOOR = {"Open": None, "Archway": None, "Broken": None, "Crude": None, "Ladder": None, "Rope": None, "Chute": None, "Lift": None,
        "Iron": "portcullis"}   # any other a door; a Hatch is drawn as one
GAP = {"Archway": "arch"}       # a doorless way through a shared wall, else open
ROUTED_WALL = 2.5               # a routed block's wall stroke, so a wall between two floors reads as one, its rock hatched


def number(code: str) -> int:
    return int(code.split(".")[1])


def rocks_of(region, bid: str) -> list[kdl.Node]:
    return [n for n in region.files.get("Blocks", []) if n.name == "Rock" and n.args and str(n.args[0]) == bid]


def area(poly: list[tuple[float, float]]) -> float:
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))) / 2


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


FAULTS = ("door-off-wall,through-room,corridors-cross,way-no-passage,reenters-room,port-outside-room,rooms-overlap,"
          "in-keep-out,outside-bounds,maze-no-route,note-off-floor,marks-overlap,end-in-room,offset-moved,junction-at-bend")
SEEN = ("rooms-merge", "doors-stacked", "label-overlap", "passages-tangle")    # warnings of `check` the validator passes on


def defects(region, block: kdl.Node, m: dict) -> list[tuple[str, str]]:
    """What is wrong with a block's map file, as (level, message): `artgen dungeon check`'s
    faults, then its `facts` held to the tables' ways."""
    members = {x.strip() for x in str(block.props["locations"]).split(",")}
    dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    if not all(space.centre(dress.get(c)) for c in members):
        return []                                         # its rooms are not placed yet
    found = engine("check", m, "--errors", FAULTS)
    leaving = {f"corridors[{k}]" for k, c in enumerate(m.get("corridors", [])) if "exit" in c["to"] or "exit" in c["from"]}
    out = [("error", f"{x['path']}: {x['message']}") for x in found.get("errors", []) if not (x.get("id") == "outside-bounds" and x["path"] in leaving)]   # a way off the map leaves it
    out += [("warning", f"{x['path']}: {x['message']}") for x in found.get("warnings", []) if x.get("id") in SEEN]
    facts = engine("facts", m)
    wrong = [f"{r} is reached by no way" for r in facts.get("unreached", [])]
    rid = lambda c: c.replace(".", "-")
    ways = {frozenset((rid(str(n.args[0])), rid(str(n.props["to"])))) for n in region.files.get("Connections", [])
            if n.args and str(n.args[0]) in members and str(n.props.get("to")) in members}
    root, nets = {}, {}                                   # passages joined to one another join every room they reach
    for c in m.get("corridors", []):
        cid = c.get("id") or id(c)
        root[cid] = root.get(c["to"].get("corridor"), c["to"].get("corridor")) or cid
        nets.setdefault(root[cid], set()).update(e["room"] for e in (c["from"], c["to"]) if e.get("room"))
    joined = {frozenset((a, b)) for net in nets.values() for a in net for b in net if a < b}
    joined |= {frozenset((r["id"], c["to"])) for r in facts.get("rooms", []) for c in r.get("connections") or []}
    codes = {rid(c) for c in members}                     # a room no location holds is the map's own
    joined = {j for j in joined if j <= codes}
    wrong += [f"the tables join {a} and {b}, but the map draws no way between them" for a, b in sorted(map(sorted, ways - joined))]
    wrong += [f"the map joins {a} and {b}, which the tables do not" for a, b in sorted(map(sorted, joined - ways))]
    leaving = sum(1 for n in region.files.get("Connections", [])
                  if n.args and str(n.args[0]) in members and str(n.props.get("to")) not in members)
    marks = sum(len(r.get("exits") or []) for r in facts.get("rooms", [])) + \
        sum(1 for c in m.get("corridors", []) if ("exit" in c["to"]) != ("exit" in c["from"]))   # a cleft, edge to edge, leads nowhere
    if marks != leaving:
        wrong.append(f"the tables take {leaving} ways out of the block, the map marks {marks}")
    return out + [("error", w) for w in wrong]


# -- a table line, edited in place ------------------------------------------------------

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
    """Each way between two rooms of a block as its map draws it: the rooms, each one's door
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
    out += junctions(m, f, label, centre, walk, cell)
    doors = {d["connection"]: d["at"] for d in f.get("doors", []) if d.get("connection") is not None}
    for r in f.get("rooms", []):
        for k in r.get("connections", []):
            if k["connection"] not in seen and k["to"] in centre and (at := k.get("at") or doors.get(k["connection"])):
                seen.add(k["connection"])
                out.append((r["label"], label[k["to"]], at, at, walk([centre[r["id"]], at, centre[k["to"]]]),
                            math.dist(centre[r["id"]], centre[k["to"]]) * cell))
    return out


def arc_at(poly: list, p) -> float:
    """How far along a polyline its nearest point to p lies."""
    best, run = (math.inf, 0.0), 0.0
    for a, b in zip(poly, poly[1:]):
        seg = math.dist(a, b)
        t = 0.0 if not seg else max(0.0, min(1.0, ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / seg ** 2))
        q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        if math.dist(p, q) < best[0]:
            best = (math.dist(p, q), run + seg * t)
        run += seg
    return best[1]


def between(poly: list, s0: float, s1: float) -> list:
    """The stretch of a polyline from s0 along it to s1, either way round."""
    if s1 < s0:
        return between(poly, s1, s0)[::-1]
    marks, run = [0.0], 0.0
    for a, b in zip(poly, poly[1:]):
        run += math.dist(a, b)
        marks.append(run)

    def at(s):
        for (a, b), lo, hi in zip(zip(poly, poly[1:]), marks, marks[1:]):
            if s <= hi or hi == marks[-1]:
                t = 0.0 if hi == lo else min(1.0, max(0.0, (s - lo) / (hi - lo)))
                return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        return poly[-1]
    return [at(s0)] + [q for q, d in zip(poly, marks) if s0 < d < s1] + [at(s1)]


def junctions(m: dict, f: dict, label: dict, centre: dict, walk, cell: float) -> list:
    """Each way a junction makes, as passages() gives a way: a branch passage joins its trunk, so the room it leaves
    reaches each room at the trunk's ends, and each room another branch of that trunk leaves, along the trunk."""
    paths = {c["index"]: list(zip(c["path"][::2], c["path"][1::2])) for c in f.get("corridors", []) if len(c.get("path", [])) >= 4}
    ids = [c.get("id") for c in m.get("corridors", [])]
    branches: dict[int, list] = {}
    for k, c in enumerate(m.get("corridors", [])):
        t = c["to"].get("corridor")
        if t in ids and k in paths and c["from"].get("room") in centre and ids.index(t) in paths:
            branches.setdefault(ids.index(t), []).append(k)
    out = []
    for t, ks in branches.items():
        tp, trunk = paths[t], m["corridors"][t]
        stops = [(arc_at(tp, paths[k][-1]), m["corridors"][k]["from"]["room"], paths[k]) for k in ks]
        stops += [(0.0, trunk["from"].get("room"), [tp[0]]), (arc_at(tp, tp[-1]), trunk["to"].get("room"), [tp[-1]])]
        stops = [x for x in stops if x[1] in centre]
        for i, (sa, a, pa) in enumerate(stops[:len(ks)]):            # each branch to every other stop on the trunk
            for sb, b, pb in stops[:i] + stops[i + 1:]:
                if a == b:
                    continue
                pts = pa + between(tp, sa, sb) + pb[::-1]
                out.append((label[a], label[b], list(pa[0]), list(pb[0]), walk([centre[a], *pts, centre[b]]),
                            math.dist(centre[a], centre[b]) * cell))
    return out


@functools.cache
def walks(code: str, setting: Path = tables.SETTING) -> dict[tuple[str, str], tuple[str, int, str]]:
    """Each way between two rooms of a block of the region, both ways round: the wall it leaves by - the side its
    door stands on, else its door's compass point - its walk to the next room's centre, to the nearest 5 feet, and
    where its door stands, as `maps.wall_said` reads it out."""
    region = maps.world_for(setting).regions[code]
    compass, out = space.compass(), {}
    for block in blocks_of(region).values():
        file = built(region.code, str(block.args[0]))[0]
        rooms = {r["label"]: r for r in engine("facts", json.loads(file.read_text())).get("rooms", [])} if file else {}
        for a, b, door_a, door_b, how, _ in passages(region, block) or ():
            for here, there, (x, y) in ((a, b, door_a), (b, a, door_b)):
                r = rooms[here]["box"]["cells"]
                side = next((s for s, hit in (("w", abs(x - r["x"])), ("e", abs(x - r["x"] - r["w"])),
                                              ("n", abs(y - r["y"])), ("s", abs(y - r["y"] - r["h"]))) if hit < 1e-6), None)
                toward = math.degrees(math.atan2(x - r["x"] - r["w"] / 2, r["y"] + r["h"] / 2 - y)) % 360
                out[here, there] = (SIDE.get(side) or compass[round(toward / 22.5) % 16], round(how / 5) * 5,
                                    maps.wall_said(rooms[here]["shape"], r, (x, y)))
    return out


@functools.cache
def stairs(code: str, setting: Path = tables.SETTING) -> dict[tuple[str, str], str]:
    """Each stair out of a block of the region, from its room to the location it reaches: the wall it stands
    against, as `maps.wall_said` reads it out."""
    region = maps.world_for(setting).regions[code]
    out = {}
    for block in blocks_of(region).values():
        if not (file := built(region.code, str(block.args[0]))[0]):
            continue
        m = json.loads(file.read_text())
        seen = {r["label"]: r for r in engine("facts", m).get("rooms", [])}
        for room in m.get("rooms", []):
            r = seen.get(room.get("label"))
            drawn = {f.get("text"): f["at"] for f in (r or {}).get("exits") or []}
            for e in room.get("exits", []):
                if (far := re.search(r"to (\S+)", e.get("text", ""))) and e.get("text") in drawn:
                    out[room["label"], far[1]] = maps.wall_said(r["shape"], r["box"]["cells"], drawn[e["text"]], e["side"],
                                                                       "against")
    return out


# -- problems: what the validator reports of a block --------------------------------------

def problems(region, block: kdl.Node) -> list[tuple[str, Path, str]]:
    """What is wrong with a block, as (level, file, message). A room is a hall where it is one passage wide and at
    least twice as long, and only there. A block whose plan is approved and applied states its outline, its rooms
    cover the least of its design's fill, each Connection's `wall` is the one its map draws, no way within it states
    a bearing or distance, and nothing is wrong with its map (`defects`). A block with no approved plan is
    tools/design.py's to report; where its rooms lie, against its outline and the blocks a stair joins it to, is
    tools/space.py's."""
    import plan
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
    if not at or bid not in maps.designed(region) & set(plan.plans_of(region)):
        return out
    o = space.outline_value(block.props.get("outline"))
    if o is None:
        return out + [("error", path, f"{bid} places its rooms but states no outline: its plan's, or the hull `accept` wrote")]
    head = next(n for n in plan.with_brief(region.files.get("Design", []), region.code) if n.name == "Design" and n.args and str(n.args[0]) == bid)
    rock = sum(area(space.polygon(r, xy[0], xy[1])) for n in rocks_of(region, bid)
               if (r := space.outline_value(n.props.get("outline"))) is not None and (xy := space.point_of(n.props.get("xyz")) or [0.0, 0.0]))
    room = area(space.polygon(o, 0, 0)) - rock
    covered = sum(float(dress[c].props["width"]) * float(dress[c].props["length"]) for c in at)
    least = (plan.Plan.fill_of(head.props.get("fill")) or (0, 0))[0]
    if covered < least * room:
        out.append(("error", path, f"{bid}'s rooms cover {covered / room:.0%} of its ground, under its design's fill of {least:.0%}"))
    points, drawn = space.compass(), walks(region.code)
    for n in region.files.get("Connections", []):
        a, b = str(n.args[0]), str(n.props.get("to"))
        if a in at and b in at and "wall" in n.props and (w := drawn.get((a, b))):
            gap = abs((points.index(str(n.props["wall"])) - points.index(w[0])) * 22.5 + 180) % 360 - 180
            if abs(gap) > 45:
                out.append(("error", region.dir / "Connections.md", f"line {n.line}: {a} to {b} leaves by the "
                            f"{n.props['wall']} wall, where the plan's map draws it leaving {w[0]} - owed to step 4a"))
        if a in at and b in at and ("bearing" in n.props or "distance" in n.props):
            out.append(("error", region.dir / "Connections.md",
                        f"line {n.line}: {a} to {b} states a bearing or distance, which its rooms' places give: take it off"))
    if mapfile := built(region.code, bid)[0]:
        for level, d in defects(region, block, json.loads(mapfile.read_text())):
            out.append((level, path, f"{bid}'s map: {d}"))
    return out
