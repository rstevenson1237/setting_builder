#!/usr/bin/env python3
"""Block designs: the layouts a block is built from, and the graph `artgen dungeon layout` packs.

  python3 tools/design.py layouts                  # the library: id, tags, parameters, sockets
  python3 tools/design.py expand CODE [BLOCK]      # a design as a `dungeon layout` graph, JSON
  python3 tools/design.py solve CODE [BLOCK] [--seeds N] [--keep K] [--free]   # N packings scored, the best K drawn
  python3 tools/design.py accept CODE [BLOCK] --seed S                # write that packing's places into Design.md
  python3 tools/design.py check [CODE]             # a design and its tables, against one another

A design (`setting/region/[Code]/Design.md`, `patterns/Region_Schema.md`) names the layouts a block
uses (`layouts/`, `patterns/Layout_Schema.md`), binds each layout's roles to location codes, joins
their sockets and leaves the rest of its locations to fill. `expand` turns it into rooms and ways:
a role's rooms are its bound locations, sized at the middle of the layout's range, a Tie joins the
rooms of two roles, a Join the rooms at two sockets or a socket and a location, a fill room the
size its Fill states. The ground is the design's `outline`, else left to the least square its `fill`
allows; its voids are kept out. A `pad` grows each room in the solve and `Place` states the room itself, so the
rooms stand a passage apart in the tables. Where the design leaves `fill`, `passages` or `detour` unset BRIEF.md's
`design` line, then its `pack` line, gives them. Prints the graph on stdout and every problem on stderr, and exits 1 on any.

`solve` packs the graph over N seeds, scores each against the design (the rooms are all there, the share of the
ground they cover, the passage between joined rooms against `spacing`, the ways that walk past the detour,
and the symmetry or straightness a layout asks for), and draws the best K in the house look on one contact
sheet with a table of scores. `accept` writes one packing's `Place` and `Link` lines, its seed and score, and,
for a design that states no outline, the `hull`; it never writes `approved`, which only the user's word sets,
and takes away one the design had. `check` holds an approved design and the tables to one another. SAFE and WILD
blocks are fixed geometry, not solved: their `Place` lines are written by hand, and `check` holds them too.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import dataclasses
import json
import math
import re
import statistics
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dungeon                  # noqa: E402
import kdl                      # noqa: E402
import maps                     # noqa: E402
import space                    # noqa: E402
import tables                   # noqa: E402

LAYOUTS = tables.ROOT / "layouts"
GRID = 5                        # feet: a layout states sizes on this grid
ROOM = 20                       # feet: a fill room's side, where its Fill states none
LATTICE = dungeon.LATTICE       # feet: rooms are sized in whole steps of it, so each lies on the lattice at a whole-foot place
RING = 24                       # sides of the polygon a circular outline is given as
SHAPES = {"rect": "rect", "cave": "cave", "round": "round", "octagon": "octagon", "hexagon": "hexagon", "hall": "rect"}
NODES = {"Layout": {"name", "tags", "source"}, "Param": {"name", "range"},
         "Part": {"role", "shape", "width", "length", "count", "at", "focal"}, "Tie": {"a", "b", "kind", "of_a", "of_b"},
         "Socket": {"name", "part", "of", "bearing", "width"}, "Constraint": {"kind", "parts"}}
RANGE_RE = re.compile(r"(\d+)(?:-(\d+))?")


@dataclasses.dataclass
class Layout:
    id: str
    name: str = ""
    tags: list = dataclasses.field(default_factory=list)
    source: str = ""
    params: dict = dataclasses.field(default_factory=dict)     # name -> (least, most)
    parts: dict = dataclasses.field(default_factory=dict)      # role -> its Part's props
    ties: list = dataclasses.field(default_factory=list)
    sockets: dict = dataclasses.field(default_factory=dict)    # name -> its Socket's props
    constraints: list = dataclasses.field(default_factory=list)


def words(v) -> list[str]:
    return [w.strip() for w in str(v or "").split(",") if w.strip()]


def span(v) -> tuple[int, int] | None:
    m = RANGE_RE.fullmatch(str(v or ""))
    return (int(m[1]), int(m[2] or m[1])) if m and int(m[1]) <= int(m[2] or m[1]) else None


def read_layout(path: Path, compass: list[str], shapes) -> tuple[Layout | None, list[tuple[Path, str]]]:
    """One layout file, and what it gets wrong, each with the file."""
    problems = []
    p = lambda n, msg: problems.append((path, f"line {n.line}: {msg}"))
    try:
        nodes = kdl.fenced(path.read_text())
    except SyntaxError as e:
        return None, [(path, str(e))]
    if not nodes or nodes[0].name != "Layout" or [n.name for n in nodes].count("Layout") != 1:
        return None, [(path, "opens with one Layout line")]
    lay = Layout(str(nodes[0].args[0]) if nodes[0].args else "")
    if lay.id != path.stem:
        p(nodes[0], f"Layout {lay.id!r} is not the file's id {path.stem!r}")
    for n in nodes:
        if n.name not in NODES:
            p(n, f"{n.name!r} is not one of {', '.join(NODES)}")
        for k in n.props:
            if n.name in NODES and k not in NODES[n.name]:
                p(n, f"{n.name} takes {', '.join(sorted(NODES[n.name]))}, not {k}")
    roles = {str(n.props.get("role")) for n in nodes if n.name == "Part"}
    params = {str(n.props.get("name")) for n in nodes if n.name == "Param"}
    for n in nodes:
        q = {k: str(v) for k, v in n.props.items()}
        if n.name == "Layout":
            lay.name, lay.tags, lay.source = q.get("name", ""), words(q.get("tags")), q.get("source", "")
            if not (lay.name and lay.tags and lay.source.split(" ")[0] in ("drawn", "written")):
                p(n, "a Layout states name, tags and a source that opens drawn or written")
        elif n.name == "Param":
            if q.get("name") in lay.params or not q.get("name") or span(q.get("range")) is None:
                p(n, "a Param states one name and a range, N or N-M")
            else:
                lay.params[q["name"]] = span(q["range"])
        elif n.name == "Part":
            role = q.get("role")
            if not role or role in lay.parts:
                p(n, "a Part states one role, once")
                continue
            lay.parts[role] = q
            if q.get("shape", "rect") not in shapes:
                p(n, f"shape {q.get('shape')!r} is not one of {', '.join(shapes)}")
            for k in ("width", "length"):
                feet = span(q.get(k))
                if not (q.get(k) in params or feet and all(v % GRID == 0 for v in feet)):
                    p(n, f"{k} is a Param's name or feet on the {GRID} ft grid, N or N-M")
            if "count" in q and not (q["count"].isdigit() or q["count"] in params):
                p(n, "count is a number or a Param's name")
            if "at" in q:
                role_of, _, side = q["at"].partition(" ")
                if role_of not in roles or side not in compass:
                    p(n, 'at is "[role] [Compass]", of a role this layout holds')
        elif n.name == "Tie":
            if q.get("a") not in roles or q.get("b") not in roles or q.get("kind") not in ("door", "passage"):
                p(n, "a Tie joins two roles of the layout, as a door or a passage")
            if any(k in q and q[k] not in ("first", "last") and not q[k].isdigit() for k in ("of_a", "of_b")):
                p(n, "of_a and of_b are first, last or a number")
            lay.ties.append(q)
        elif n.name == "Socket":
            if not q.get("name") or q["name"] in lay.sockets or q.get("part") not in roles \
                    or q.get("bearing") not in compass or not q.get("width", "").isdigit():
                p(n, "a Socket states one name, a role, a Compass bearing and a width in feet")
            else:
                lay.sockets[q["name"]] = q
        elif n.name == "Constraint":
            if q.get("kind") not in ("mirror", "straight") or not set(words(q.get("parts"))) <= roles:
                p(n, "a Constraint is mirror or straight, between roles of the layout")
            lay.constraints.append(q)
    return lay, problems


def read_layouts(root: Path = LAYOUTS) -> tuple[dict[str, Layout], list[tuple[Path, str]]]:
    """Every layout of `layouts/`, by id, and what they get wrong, each with its file."""
    schema = tables.Schema()
    compass, shapes = list(schema.setting_enums["Compass"]), list(schema.setting_enums["Room_Shape"])
    out, problems = {}, []
    for path in sorted(root.glob("*.md")) if root.exists() else []:
        lay, bad = read_layout(path, compass, shapes)
        problems += bad
        if lay is not None:
            out[lay.id] = lay
    return out, problems


# -- a design, as a graph --------------------------------------------------------------

def pick(rooms: list[str], which: str | None) -> list[str]:
    """The rooms of a role a Tie ends at: all of them, or the first, the last or the Nth."""
    if which is None or not rooms:
        return rooms
    i = len(rooms) - 1 if which == "last" else int(which) - 1 if which.isdigit() else 0
    return [rooms[i]] if 0 <= i < len(rooms) else []


def mid(lo: int, hi: int, grid: int = 1) -> int:
    return max(grid, int((lo + hi) / 2 / grid + 0.5) * grid)


class Expand:
    """One block's design as the `dungeon layout` graph: `graph`, or `problems`."""

    def __init__(self, region, brief: tables.Brief, bid: str, seed: int = 1, tries: int = 12, free: bool = False):
        self.region, self.bid, self.free, self.problems = region, bid, free, []        # problems: (file, message)
        self.graph = None
        self.compass = space.compass()
        self.layouts, bad = read_layouts()
        self.problems += bad
        lines = [n for n in region.files.get("Design", []) if n.args]
        self.node = next((n for n in lines if n.name == "Design" and str(n.args[0]) == bid), None)
        if self.node is None:
            self.problems.append((region.dir / "Design.md", f"{region.code} holds no Design for {bid}"))
            return
        mine = lambda name: [n for n in lines if n.name == name and str(n.args[0]) == bid]
        self.locations = words(self.node.props.get("locations"))
        self.uses = {}
        for n in mine("Use"):
            self.use(n)
        self.rooms: dict[tuple[str, str], list[str]] = {}      # (use, role) -> the locations bound to it
        self.size: dict[str, tuple[int, int]] = {}
        self.shape: dict[str, str] = {}
        self.points: dict[str, list] = {}                      # a fill room's poly outline, in feet round its centre
        self.pads: dict[str, int] = {}                         # a room's own pad, where its Bind or Fill states one
        self.fixed: set[str] = set()                           # rooms a layout shapes, which may not turn
        for n in mine("Bind"):
            self.bind(n)
        for n in mine("Fill"):
            self.fill(n)
        unbound = [c for c in self.locations if c not in self.size]
        if unbound:
            self.problems.append((region.dir / "Design.md", f"{', '.join(unbound)} of {bid} are in no Bind or Fill"))
        self.ways: dict[frozenset, dict] = {}
        for uid, (lay, _) in self.uses.items():
            self.ties(uid, lay)
        self.exits = []
        for n in mine("Join"):
            self.join(n)
        if not self.problems:
            self.graph = self.build(brief, mine("Void"), seed, tries)

    def say(self, n: kdl.Node, msg: str):
        self.problems.append((self.region.dir / "Design.md", f"line {n.line}: {msg}"))

    def use(self, n: kdl.Node):
        uid, lay = str(n.props.get("id")), self.layouts.get(str(n.props.get("layout")))
        if lay is None or uid in self.uses or not uid or uid == "None":
            return self.say(n, f"Use states one id, once, and a layout of layouts/ ({', '.join(self.layouts)})")
        given = dict(re.findall(r"([\w-]+)=(\d+)", str(n.props.get("params", ""))))
        values = {}
        for name, (lo, hi) in lay.params.items():
            values[name] = int(given.pop(name)) if name in given else mid(lo, hi, LATTICE if hi >= LATTICE else 1)
            if not lo <= values[name] <= hi:
                self.say(n, f"{name}={values[name]} is outside {lay.id}'s range {lo}-{hi}")
        if given:
            self.say(n, f"{lay.id} has no parameter {', '.join(given)}")
        self.uses[uid] = (lay, values)

    def number(self, lay: Layout, values: dict, spec: str, grid: int) -> int:
        if spec in values:
            return values[spec]
        lo, hi = span(spec)
        return mid(lo, hi, grid)

    def count(self, lay: Layout, values: dict, role: str) -> int:
        c = lay.parts[role].get("count")
        return 1 if c is None else self.number(lay, values, c, 1)

    def bind(self, n: kdl.Node):
        uid, role = str(n.props.get("use")), str(n.props.get("role"))
        if uid not in self.uses or role not in self.uses[uid][0].parts:
            return self.say(n, f"Bind names use {uid!r} and role {role!r}, which no Use of this design holds")
        lay, values = self.uses[uid]
        codes = words(n.props.get("locations"))
        if len(words(n.props.get("type"))) not in (1, len(codes)):
            return self.say(n, f"{uid}'s role {role} has {len(codes)} locations and {len(words(n.props.get('type')))} types: one type, or one each")
        if (uid, role) in self.rooms:
            return self.say(n, f"{uid}'s role {role} is bound twice")
        if len(codes) != self.count(lay, values, role):
            return self.say(n, f"{uid}'s role {role} holds {self.count(lay, values, role)}, and is bound to {len(codes)} locations")
        self.rooms[uid, role] = codes
        part = lay.parts[role]
        for c in codes:
            if c in self.size:
                self.say(n, f"{c} is bound twice")
            elif c not in self.locations:
                self.say(n, f"{c} is not one of the design's locations")
            else:
                self.size[c] = (self.number(lay, values, part["width"], LATTICE), self.number(lay, values, part["length"], LATTICE))
                self.shape[c] = part.get("shape", "rect")
                self.fixed.add(c)
                self.own_pad(n, c)

    def fill(self, n: kdl.Node):
        if len(words(n.props.get("type"))) not in (1, len(words(n.props.get("locations")))):
            self.say(n, "a Fill states one type for its locations, or one each")
        for c in words(n.props.get("locations")):
            if c in self.size:
                self.say(n, f"{c} is bound twice")
            elif c not in self.locations:
                self.say(n, f"{c} is not one of the design's locations")
            else:
                self.size[c] = (int(n.props.get("width", ROOM)), int(n.props.get("length", ROOM)))
                self.shape[c] = str(n.props.get("shape", "rect"))
                self.own_pad(n, c)
                if self.shape[c] not in SHAPES:
                    self.say(n, f"{c} is shape {self.shape[c]}: one of {', '.join(SHAPES)}")
                if (o := space.outline_value(n.props.get("outline"))) is not None:      # a poly where no shape draws the room
                    if o[0] != "poly":
                        self.say(n, f"{c}'s outline is a poly, or its width and length")
                    else:
                        self.points[c] = o[1]
                        xs, ys = [x for x, _ in o[1]], [y for _, y in o[1]]
                        self.size[c] = (round(max(xs) - min(xs)), round(max(ys) - min(ys)))
                if any(v % LATTICE for v in self.size[c]):
                    self.say(n, f"{c} is {self.size[c][0]} by {self.size[c][1]} ft: a room is sized in whole {LATTICE} ft steps")

    def own_pad(self, n: kdl.Node, c: str):
        """A Bind's or Fill's own `pad`, which a room it names takes in place of the design's."""
        if "pad" in n.props:
            if m := tables.PAD_RE.fullmatch(str(n.props["pad"])):
                self.pads[c] = int(m[1])
            else:
                self.say(n, 'pad is "N feet"')

    def tie(self, a: str, b: str, bearing: float | None):
        key = frozenset((a, b))
        if a != b and key not in self.ways:
            self.ways[key] = {"a": a, "b": b, **({"bearing": bearing} if bearing is not None else {})}
        elif a != b and bearing is not None and "bearing" not in self.ways[key]:     # a Join gives a Tie's way its direction
            self.ways[key].update(a=a, b=b, bearing=bearing)

    def ties(self, uid: str, lay: Layout):
        look = lambda role: self.rooms.get((uid, role), [])
        for t in lay.ties:
            a, b = pick(look(t["a"]), t.get("of_a")), pick(look(t["b"]), t.get("of_b"))
            if t["a"] == t["b"]:
                at = lay.parts[t["a"]].get("at", "").partition(" ")
                bearing = self.compass.index(at[2]) * 22.5 if at[0] == t["a"] else None
                for x, y in zip(a, a[1:]):
                    self.tie(x, y, bearing)
                continue
            for x, y in ([(x, y) for x in a for y in b] if len(a) == 1 or len(b) == 1 else list(zip(a, b))):
                at_b, at_a = (lay.parts[t[k]].get("at", "").partition(" ") for k in ("b", "a"))
                bearing = self.compass.index(at_b[2]) * 22.5 if at_b[0] == t["a"] else \
                    (self.compass.index(at_a[2]) * 22.5 + 180) % 360 if at_a[0] == t["b"] else None
                self.tie(x, y, bearing)

    def end(self, n: kdl.Node, name: str) -> tuple[str, float | None, int | None] | None:
        """One end of a Join: the room a socket stands on, with its bearing and width, or a location code."""
        if "." in name and name.split(".")[0] in self.uses:
            uid, sock = name.split(".", 1)
            lay, _ = self.uses[uid]
            s = lay.sockets.get(sock)
            if s is None:
                return self.say(n, f"{uid} has no socket {sock!r}; {lay.id} has {', '.join(lay.sockets)}")
            rooms = self.rooms.get((uid, s["part"]), [])
            of = s.get("of", "first")
            if len(rooms) > 1 and "of" not in s:
                return self.say(n, f"socket {name} stands on {s['part']}, which has {len(rooms)} rooms: it states none of them")
            i = len(rooms) - 1 if of == "last" else int(of) - 1 if of.isdigit() else 0
            if not rooms or not 0 <= i < len(rooms):
                return self.say(n, f"socket {name} has no room: {uid}'s role {s['part']} is unbound")
            return rooms[i], self.compass.index(s["bearing"]) * 22.5, int(s["width"])
        return name, None, None

    def join(self, n: kdl.Node):
        a, b = self.end(n, str(n.props.get("from"))), self.end(n, str(n.props.get("to")))
        if a is None or b is None:
            return
        (x, bx, wx), (y, by, wy) = a, b
        inside = [c in self.locations for c in (x, y)]
        if not any(inside):
            return self.say(n, "a Join has a room of this block at one end")
        if not all(inside):                       # a way out of the block: its room keeps it, the tables write it
            self.exits.append({"room": x if inside[0] else y, "to": y if inside[0] else x})
            return
        if bx is not None and by is not None and (abs((bx - by + 180) % 360 - 180) < 135 or wx != wy):
            return self.say(n, f"{n.props['from']} leaves {self.compass[round(bx / 22.5)]} {wx} ft wide and {n.props['to']} "
                               f"{self.compass[round(by / 22.5)]} {wy} ft: sockets joined face one another and match in width")
        self.tie(x, y, bx)

    def constrained(self) -> list[tuple[str, list[str]]]:
        """Each constraint of a used layout, with the rooms of the roles it holds between."""
        out = []
        for uid, (lay, _) in self.uses.items():
            for c in lay.constraints:
                roles = words(c.get("parts")) or list(lay.parts)
                out.append((c["kind"], [code for r in roles for code in self.rooms.get((uid, r), [])]))
        return out

    def build(self, brief: tables.Brief, voids: list, seed: int, tries: int) -> dict | None:
        node = self.node
        self.settings = settings(brief, self.region.code, node)
        self.pad = int(m[1]) if (m := tables.PAD_RE.fullmatch(self.settings.get("pad", ""))) else 0
        rates = brief.packing(self.region.code)
        overlay(rates, self.settings)
        if rates["fill"] is None or rates["passages"] is None:
            return self.say(node, "BRIEF.md states no pack fill and passages") or None
        poly, side = self.poly, self.side = ground(space.outline_value(node.props.get("outline")))
        frame = dungeon.framed(poly, side)
        pins = {} if self.free else {c: p for c in self.locations if (p := space.settled().pin(c))}   # free: the levels a stair joins are placed after this one
        rocks = [(space.point_of(v.props.get("xyz")) or [0.0, 0.0], s) for v in voids
                 if (s := space.outline_value(v.props.get("outline"))) is not None]
        if (pins or rocks) and not (poly or side):
            held = f"a stair into {', '.join(pins)}" if pins else "a void"
            return self.say(node, f"{held} is placed in the design's frame, so the design states an outline") or None
        rooms = []
        for c in self.locations:
            w, h = self.size[c]
            grown = 0 if c in self.points else 2 * self.pads.get(c, self.pad)       # a poly is not grown; a room is, so rooms that touch in the solve stand twice the pad apart
            r = {"id": c, "w": (w + grown) / GRID, "h": (h + grown) / GRID, "shape": "poly" if c in self.points else SHAPES[self.shape[c]], "hall": self.shape[c] == "hall",
                 "turns": c not in self.fixed and not any("bearing" in way for k, way in self.ways.items() if c in k)}
            if c in self.points:
                r["points"] = [v for x, y in self.points[c] for v in (x / GRID, -y / GRID)]
            if c in pins:
                r["over"] = dungeon.held_over(pins[c], frame)
            rooms.append(r)
        gid = f"{self.region.code}-{self.bid.split('.')[-1]}"
        return dungeon.graph_shell(gid, rooms, list(self.ways.values()), rates, seed, tries, poly, side, rocks, frame)


def ground(o: tuple | None) -> tuple[list | None, float | None]:
    """A design's outline as the ground of its graph: the side of a square, or a polygon in feet round its centre,
    or neither where it states none and the solver takes the least square its fill allows."""
    if o is None:
        return None, None
    if o[0] == "rect" and o[1] == o[2]:
        return None, float(o[1])
    if o[0] == "circle":
        return [(o[1] * math.cos(2 * math.pi * i / RING), o[1] * math.sin(2 * math.pi * i / RING)) for i in range(RING)], None
    return (o[1] if o[0] == "poly" else space.polygon(o, 0, 0)), None


SETTINGS = ("fill", "spacing", "passages", "detour", "pad")


def settings(brief: tables.Brief, code: str, node: kdl.Node | None) -> dict[str, str]:
    """A block design's settings: BRIEF.md's `design` line for its region, then the Design line's own."""
    line = brief.designs.get(code)
    got = {k: str(v) for k, v in (line.props.items() if line is not None else ()) if k in SETTINGS}
    got.update({k: str(v) for k, v in (node.props.items() if node is not None else ()) if k in SETTINGS})
    return got


def overlay(rates: dict, got: dict[str, str]):
    """Settings over the rates a `pack` line gives. `spacing`, the passage wanted between joined rooms, sets
    `passages` (all, where it asks for 10 ft or more) and `detour` (its most) where `got` does not. `pad` is
    read by `Expand`: it grows each room in the solve, so rooms that touch there stand apart."""
    if m := tables.FILL_RE.fullmatch(got.get("fill", "")):
        rates["fill"] = (int(m[1]) / 100, int(m[2]) / 100)
    if "passages" in got:
        rates["passages"] = int(got["passages"][:-1]) / 100
    if "detour" in got:
        rates["detour"] = maps.feet(got["detour"])
    if m := tables.SPACING_RE.fullmatch(got.get("spacing", "")):
        if "passages" not in got and int(m[1]) >= 10:
            rates["passages"] = 1.0
        if "detour" not in got:
            rates["detour"] = float(m[2])


def expand(region, bid: str, seed: int = 1, tries: int = 12, free: bool = False) -> Expand:
    world = maps.world_for(tables.SETTING)
    return Expand(region, tables.Brief(world.schema), bid, seed, tries, free)



# -- solving: packings, scored ---------------------------------------------------------

CELL, MARGIN = dungeon.CELL, dungeon.MARGIN
# What a miss costs, in points off a hundred: a point per share of a percent of fill, per 2 feet of spacing,
# per way past its detour, per finding of artgen's own `dungeon check` (two doors on one spot, a passage through a
# room), per lattice cell two passages leaving one room share, a crossing or a run side by side, and per 5 feet of symmetry or straightness.
COST = {"fill": 100.0, "spacing": 0.5, "detour": 5.0, "symmetry": 0.2, "straight": 0.2, "check": 6.0, "shared": 10.0}


def layout(graph: dict, seed: int) -> dict | str:
    """`artgen dungeon layout` over the graph at a seed: its report and dungeon, or why it failed."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "graph.json").write_text(json.dumps(dict(graph, seed=seed)))
        done = maps.artgen("dungeon", "layout", "--file", Path(tmp) / "level.json", "--graph", Path(tmp) / "graph.json",
                           "--seed", seed, "--json", "--force")
    return json.loads(done.stdout) if not done.returncode and done.stdout.startswith("{") else (done.stderr or done.stdout).strip()


def laid(ex: Expand, out: dict) -> dict[str, dict]:
    """Each room of a packing, as feet east and north of the block's centre: `at`, `w`, `l`, and a poly's `points`."""
    side = out["report"]["side"] * CELL
    ox, oy = (min(x for x, _ in ex.poly), min(-y for _, y in ex.poly)) if ex.poly else (-side / 2,) * 2
    rooms = {}
    for r in out["dungeon"]["rooms"]:
        code = r["label"]
        rooms[code] = {"at": (round((r["x"] + r["w"] / 2 - MARGIN) * CELL + ox), round(-((r["y"] + r["h"] / 2 - MARGIN) * CELL + oy))),
                       "w": round(r["w"] * CELL) - (0 if "points" in r else 2 * ex.pads.get(code, ex.pad)), "l": round(r["h"] * CELL) - (0 if "points" in r else 2 * ex.pads.get(code, ex.pad)),
                       **({"points": [((x - r["x"] - r["w"] / 2) * CELL, (r["y"] + r["h"] / 2 - y) * CELL)
                                      for x, y in zip(r["points"][::2], r["points"][1::2])]} if "points" in r else {})}
    return rooms


def gap(a: dict, b: dict) -> float:
    """The feet between two rooms' boxes: nothing where they touch or overlap."""
    return math.hypot(*(max(0.0, abs(a["at"][k] - b["at"][k]) - ((a["w"], a["l"])[k] + (b["w"], b["l"])[k]) / 2) for k in (0, 1)))


def mirror(rooms: list[dict]) -> float:
    """How far, on average, a room's reflection across the best vertical or horizontal line through the group's
    centre lies from a room of its own size, in feet."""
    best = None
    for k in (0, 1):
        axis = statistics.mean(r["at"][k] for r in rooms)
        miss = []
        for r in rooms:
            want = [r["at"][0], r["at"][1]]
            want[k] = 2 * axis - want[k]
            miss.append(min(math.dist(want, o["at"]) for o in rooms if (o["w"], o["l"]) in ((r["w"], r["l"]), (r["l"], r["w"]))))
        best = min(best, statistics.mean(miss)) if best is not None else statistics.mean(miss)
    return best


def straight(rooms: list[dict]) -> float:
    """The spread, in feet, of a group's centres across the line they run along best."""
    return min(statistics.pstdev(r["at"][1 - k] for r in rooms) for k in (0, 1))


def runs(d: dict) -> list[tuple[str, str, set]]:
    """Each passage of a packing as the lattice cells its centre line crosses, with its two rooms."""
    out = []
    for k in d["corridors"]:
        via = k.get("via") or []
        pts = [tuple(k["from"]["port"]), *(list(zip(via[::2], via[1::2])) if via and not isinstance(via[0], (list, tuple)) else map(tuple, via)),
               tuple(k["to"]["port"])]
        cells = set()
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(1, round(max(abs(x1 - x0), abs(y1 - y0))))
            cells |= {(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)}
        out.append((k["from"]["room"], k["to"]["room"], cells))
    return out


def shared(d: dict) -> int:
    """The lattice cells that passages leaving one room share, where they cross or run together: artgen lets passages
    that leave one room join, and a hub's passages read as spokes only where they do not."""
    got = runs(d)
    return sum(len(a[2] & b[2]) for i, a in enumerate(got) for b in got[i + 1:] if {a[0], a[1]} & {b[0], b[1]})


def judge(ex: Expand, out: dict, rooms: dict[str, dict]) -> tuple[float, dict, list[str]]:
    """A packing's score out of a hundred, what was measured, and where it falls short."""
    rep = out["report"]
    lo, hi = ex.graph["fill"]
    seen = {"fill": rep["fill"], "corridor": rep["corridorCells"] * dungeon.LATTICE, "passages": rep["passages"],
            "walls": rep["walls"], "detours": len(rep["detours"])}
    gaps = [gap(rooms[w["a"]], rooms[w["b"]]) for w in ex.ways.values() if w["a"] in rooms and w["b"] in rooms]
    seen["spacing"] = statistics.median(gaps) if gaps else 0.0
    degree = {c: sum(c in k for k in ex.ways) for c in ex.locations}
    seen["dead ends"] = sum(d == 1 for d in degree.values()) / max(1, len(degree))
    cost, notes = 0.0, []
    found = dungeon.engine("check", out["dungeon"])
    if findings := found.get("errors", []) + found.get("warnings", []):
        seen["check"] = len(findings)
        cost += COST["check"] * len(findings)
        notes += sorted({f"{f['id']} ({sum(g['id'] == f['id'] for g in findings)})" for f in findings})
    if n := shared(out["dungeon"]):
        seen["shared"] = n
        cost += COST["shared"] * n
        notes.append(f"passages from one room cross or run together over {n} lattice cell(s)")
    if (miss := max(0.0, lo - rep["fill"], rep["fill"] - hi)) > 0:
        cost += COST["fill"] * miss
        notes.append(f"fill {rep['fill']:.0%} is {'under' if rep['fill'] < lo else 'over'} {lo:.0%}-{hi:.0%}")
    if m := tables.SPACING_RE.fullmatch(ex.settings.get("spacing", "")):
        if (miss := max(0.0, int(m[1]) - seen["spacing"], seen["spacing"] - int(m[2]))) > 0:
            cost += COST["spacing"] * miss
            notes.append(f"median gap {seen['spacing']:.0f} ft, wanted {m[1]}-{m[2]}")
    if rep["detours"]:
        cost += COST["detour"] * len(rep["detours"])
        notes.append(f"{len(rep['detours'])} way(s) walk past the detour")
    for kind, codes in ex.constrained():
        group = [rooms[c] for c in codes if c in rooms]
        if len(group) > 1:
            off = (mirror if kind == "mirror" else straight)(group)
            seen["symmetry" if kind == "mirror" else "straight"] = off
            cost += COST["symmetry" if kind == "mirror" else "straight"] * off
            if off >= 5:
                notes.append(f"{kind} off by {off:.0f} ft")
    return max(0.0, 100.0 - cost), seen, notes


def candidate(ex: Expand, seed: int) -> dict | None:
    out = layout(ex.graph, seed)
    if isinstance(out, str):
        return {"seed": seed, "error": out}
    if out["report"]["left"]:
        return {"seed": seed, "error": f"no passage fits the way from {', '.join(out['report']['left'])}"}
    rooms = laid(ex, out)
    score, seen, notes = judge(ex, out, rooms)
    return {"seed": seed, "out": out, "rooms": rooms, "score": score, "seen": seen, "notes": notes}


def hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """The convex hull of points, anticlockwise (Andrew's monotone chain)."""
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts
    turn = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for seq, out in ((pts, lower), (pts[::-1], upper)):
        for p in seq:
            while len(out) >= 2 and turn(out[-2], out[-1], p) <= 0:
                out.pop()
            out.append(p)
    return lower[:-1] + upper[:-1]


def ground_of(ex: Expand, cand: dict) -> list[tuple[int, int]]:
    """The hull of the floor a packing holds, in feet round the block's centre: its rooms' corners, and each passage's
    run with half its width either side."""
    d, out = cand["out"]["dungeon"], []
    for c, r in cand["rooms"].items():
        pts = r.get("points") or [(-r["w"] / 2, -r["l"] / 2), (r["w"] / 2, -r["l"] / 2), (r["w"] / 2, r["l"] / 2), (-r["w"] / 2, r["l"] / 2)]
        out += [(r["at"][0] + x, r["at"][1] + y) for x, y in pts]
    side = cand["out"]["report"]["side"] * CELL
    ox, oy = (min(x for x, _ in ex.poly), min(-y for _, y in ex.poly)) if ex.poly else (-side / 2,) * 2
    for k in d["corridors"]:
        via = k.get("via") or []
        pts = [k["from"]["port"], *(list(zip(via[::2], via[1::2])) if via and not isinstance(via[0], (list, tuple)) else via), k["to"]["port"]]
        half = k.get("width", 2) * CELL / 2
        for x, y in pts:
            ex_, ey = (x - MARGIN) * CELL + ox, -((y - MARGIN) * CELL + oy)
            out += [(ex_ + dx, ey + dy) for dx in (-half, half) for dy in (-half, half)]
    return [(round(x), round(y)) for x, y in hull(out)]


def solved(region, bid: str, seeds: int, tries: int = 12, free: bool = False) -> tuple[Expand, list[dict]]:
    ex = expand(region, bid, 1, tries, free)
    if ex.graph is None:
        return ex, []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(seeds, 8)) as pool:   # each packing is its own artgen process
        found = list(pool.map(lambda s: candidate(ex, s), range(1, seeds + 1)))
    return ex, found


def sheet(ex: Expand, kept: list[dict], folder: Path) -> Path:
    """Each kept packing drawn in the house look, as PNG and SVG, and one contact sheet of them."""
    folder.mkdir(parents=True, exist_ok=True)
    panels = []
    for c in kept:
        m = c["out"]["dungeon"]
        m["style"] = dungeon.looked(m.get("style") or {})
        f = folder / f"seed-{c['seed']}.json"
        f.write_text(json.dumps(m))
        maps.artgen("dungeon", "render", "--file", f, "--format", "both", "--fit", "800x800px", "--out", folder)
        panels.append(maps.own_ids((folder / f"seed-{c['seed']}.svg").read_text(), f"s{c['seed']}"))
    box = [float(v) for v in re.search(r'viewBox="([^"]+)"', panels[0]).group(1).split()]
    w, h = 800, 800 * box[3] / box[2]
    body = ""
    for i, (c, svg) in enumerate(zip(kept, panels)):
        svg = re.sub(r'(<svg\b[^>]*?)\swidth="[^"]*"', r"\1", svg, count=1)
        svg = re.sub(r'(<svg\b[^>]*?)\sheight="[^"]*"', r"\1", svg, count=1)
        body += svg.replace("<svg ", f'<svg x="{i * (w + 20) + 10}" y="40" width="{w}" height="{h:.0f}" ', 1)
        body += (f'<text x="{i * (w + 20) + 10}" y="26" font-family="sans-serif" font-size="20">'
                 f'seed {c["seed"]} - score {c["score"]:.0f}</text>')
    out = folder / "contact.svg"
    out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{len(kept) * (w + 20) + 10:.0f}" height="{h + 60:.0f}" '
                   f'style="background:#fff">{body}</svg>')
    return out


def solve(region, bid: str, seeds: int, keep: int, folder: Path | None, free: bool = False) -> int:
    if region.rating.upper() != "DANGEROUS":
        print(f"{bid}: a {region.rating} block is fixed geometry, not solved: write its Place lines in Design.md")
        return 1
    ex, found = solved(region, bid, seeds, free=free)
    for path, msg in ex.problems:
        print(f"ERROR: {path.relative_to(tables.ROOT)}: {msg}", file=sys.stderr)
    if ex.graph is None:
        return 1
    good, seen = [], set()
    for c in sorted((c for c in found if "out" in c), key=lambda c: -c["score"]):   # a packing another seed also found is listed once
        if (key := json.dumps({k: (v["at"], v["w"], v["l"]) for k, v in c["rooms"].items()}, sort_keys=True)) not in seen:
            seen.add(key)
            good.append(c)
    for c in found:
        if "error" in c:
            print(f"seed {c['seed']}: {c['error']}")
    if not good:
        print(f"{bid}: no seed of {seeds} routes every way; widen the outline, lower the fill, or join fewer rooms")
        return 1
    kept = good[:keep]
    folder = folder or Path(tempfile.gettempdir()) / f"design-{bid}"
    contact = sheet(ex, kept, folder)
    cols = ("seed", "score", "fill", "gap ft", "corridor ft", "detours", "dead ends", "")
    print("  ".join(c.ljust(w) for c, w in zip(cols, (4, 5, 5, 6, 11, 7, 9, 0))))
    for c in good:
        s = c["seen"]
        row = (str(c["seed"]), f"{c['score']:.0f}", f"{s['fill']:.0%}", f"{s['spacing']:.0f}", f"{s['corridor']:.0f}", str(s["detours"]),
               f"{s['dead ends']:.0%}", "; ".join(c["notes"]) or "meets the design")
        print("  ".join(v.ljust(w) for v, w in zip(row, (4, 5, 5, 6, 11, 7, 9, 0))) + ("   <- drawn" if c in kept else ""))
    routed = sum("out" in c for c in found)
    print(f"\n{routed} of {seeds} seeds route every way, as {len(good)} different packings. Contact sheet: {contact}\n"
          f"Then: python3 tools/design.py accept {region.code} {bid} --seed N")
    return 0


# -- accepting one -------------------------------------------------------------------

def accept(region, bid: str, seed: int, free: bool = False) -> int:
    if region.rating.upper() != "DANGEROUS":
        print(f"{bid}: a {region.rating} block is fixed geometry: write its Place lines in Design.md")
        return 1
    ex = expand(region, bid, seed, free=free)
    for path, msg in ex.problems:
        print(f"ERROR: {path.relative_to(tables.ROOT)}: {msg}", file=sys.stderr)
    if ex.graph is None:
        return 1
    cand = candidate(ex, seed)
    if "error" in cand:
        print(f"{bid}: seed {seed} does not route every way: {cand['error']}")
        return 1
    d = cand["out"]["dungeon"]
    code = lambda rid: rid.replace("-", ".")
    pairs = {tuple(sorted((code(c["a"]), code(c["b"])), key=dungeon.number)): "door" for c in d["connections"]}
    pairs |= {tuple(sorted((code(k["from"]["room"]), code(k["to"]["room"])), key=dungeon.number)): "passage" for k in d["corridors"]}
    mine = {c: {"at": r["at"], "w": r["w"], "l": r["l"]} for c, r in cand["rooms"].items()}
    pairs = {k: "door" if touching(mine[k[0]], mine[k[1]]) else "passage" for k in pairs}      # a padded room's door is a passage across the pad
    lines = []
    for c in ex.locations:
        r = cand["rooms"][c]
        box = "poly " + " ".join(f"{x:g},{y:g}" for x, y in r["points"]) if "points" in r else f"rect {r['w']} {r['l']}"
        lines.append(f'Place {c} xyz="{r["at"][0]},{r["at"][1]}" outline="{box}" shape={ex.shape[c]}')
    lines += [f'Link {a} to="{b}" kind={kind}' for (a, b), kind in sorted(pairs.items(), key=lambda p: (dungeon.number(p[0][0]), dungeon.number(p[0][1])))]
    path = region.dir / "Design.md"
    text, fence = path.read_text().split("\n"), False
    kept, mine, last, had = [], set(ex.locations), None, False
    for i, line in enumerate(text):
        if line.strip() == "```kdl":
            fence = True
        elif line.strip() == "```":
            fence, last = False, len(kept)
        elif fence and (m := re.match(r"(Place|Link) (\S+)", line)) and m[2] in mine:
            continue
        elif fence and line.startswith(f"Design {bid} "):
            had = "approved=" in line
            line = dungeon.without(dungeon.without(dungeon.without(dungeon.without(line, "approved"), "seed"), "score"), "hull")
            line = dungeon.with_prop(dungeon.with_prop(line, "seed", str(seed)), "score", f'"{cand["score"]:.0f}"')
            if not ex.node.props.get("outline"):
                line = dungeon.with_prop(line, "hull", '"poly ' + " ".join(f"{x},{y}" for x, y in ground_of(ex, cand)) + '"')
        kept.append(line)
    kept[last:last] = lines
    path.write_text("\n".join(kept))
    print(f"{bid}: seed {seed}, score {cand['score']:.0f}: {len(ex.locations)} places and {len(pairs)} ways written to {path.relative_to(tables.ROOT)}"
          + ("; its approval is cleared, for the user to give again" if had else "") + "\nThe user approves it, then steps 3e and 3f write the tables to agree.")
    return 0


# -- the design and its tables ---------------------------------------------------------

TOL = 0.5                       # feet two places may differ by and agree


def groups(region) -> dict[str, dict]:
    """A region's Design.md by block: its Design line, and every other line stating that block, a Place and a Link by the
    block whose locations they name."""
    out = {str(n.args[0]): {"design": n, "lines": [], "places": {}, "links": []}
           for n in region.files.get("Design", []) if n.name == "Design" and n.args}
    owner = {c: bid for bid, g in out.items() for c in words(g["design"].props.get("locations"))}
    for n in region.files.get("Design", []):
        if not n.args or n.name == "Design":
            continue
        bid = owner.get(str(n.args[0])) if n.name in ("Place", "Link") else str(n.args[0])
        if bid in out:
            out[bid]["lines"].append(n)
            if n.name == "Place":
                out[bid]["places"][str(n.args[0])] = n
            elif n.name == "Link":
                out[bid]["links"].append(n)
    return out


def kinds_of(n: kdl.Node) -> dict[str, str]:
    """The type each location of a Bind or Fill line asks for: its one type for all, or one each in order."""
    codes, types = words(n.props.get("locations")), words(n.props.get("type"))
    return {c: t for c, t in zip(codes, types * len(codes) if len(types) == 1 else types)}


def box(outline: tuple | None) -> tuple[float, float] | None:
    """The width and length of an outline's box."""
    if outline is None:
        return None
    if outline[0] == "circle":
        return 2 * outline[1], 2 * outline[1]
    if outline[0] == "rect":
        return outline[1], outline[2]
    xs, ys = [x for x, _ in outline[1]], [y for _, y in outline[1]]
    return max(xs) - min(xs), max(ys) - min(ys)


def touching(a: dict, b: dict) -> bool:
    """Whether two placed rooms share a wall: their boxes meet along one axis and overlap along the other."""
    d = [abs(a["at"][k] - b["at"][k]) for k in (0, 1)]
    reach = [((a["w"], a["l"])[k] + (b["w"], b["l"])[k]) / 2 for k in (0, 1)]
    return any(abs(d[k] - reach[k]) <= TOL * 5 and d[1 - k] < reach[1 - k] - CELL for k in (0, 1))


def at(p: list | None) -> str:
    return f"{p[0]:g},{p[1]:g}" if p else "no xyz"


def agree(region, bid: str, g: dict) -> list[tuple[str, str]]:
    """What an approved design and the region's tables disagree on, as (level, message), each naming the step that fixes
    it: a missing entry is a warning, a different one an error."""
    out = []
    node, path = g["design"], f"{bid}"
    members = set(words(node.props.get("locations")))
    danger = region.rating.upper() == "DANGEROUS"
    locs, dress = region.locations(), {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    ways = [n for n in region.files.get("Connections", []) if n.args and "to" in n.props]
    block = tables_blocks(region).get(bid)
    if block is None:
        out.append(("warning", f"{bid} is no block in Blocks.md yet, and the design places {len(members)} locations in it - owed to step 3f"))
    elif set(words(block.props.get("locations"))) != members:
        out.append(("error", f"{bid} holds {', '.join(sorted(words(block.props.get('locations')), key=dungeon.number))} in Blocks.md and "
                             f"{', '.join(sorted(members, key=dungeon.number))} in its design - owed to step 3f, or 3d if the design is wrong"))
    mine = {}
    for c in sorted(members, key=dungeon.number):
        p = g["places"].get(c)
        if p is None:
            out.append(("error", f"the design approves {bid} and places no {c}: solve and accept it - owed to step 3d"))
            continue
        want = space.point_of(p.props.get("xyz"))
        size = box(space.outline_value(p.props.get("outline")))
        mine[c] = {"at": want[:2], "w": size[0], "l": size[1]}
        have, owes = (dress.get(c), "4a") if danger else (locs.get(c), "3e")        # a DANGEROUS room's place is its Dressing's
        if c not in locs or have is None:
            out.append(("warning", f"{c} is not in {'Locations.md' if c not in locs else 'Dressing.md'} yet, and the design places it - "
                                   f"owed to step {'3e' if c not in locs else '4a'}"))
            continue
        got = space.point_of(have.props.get("xyz"))
        if got is None or math.dist(got[:2], want[:2]) > TOL:
            out.append(("error", f"{c} lies at {at(got)} in the tables and at {at(want)} in the design - owed to step {owes}, or 3d if the design is wrong"))
        d = dress.get(c)
        if d is not None and "width" in d.props and "length" in d.props:
            if abs(float(d.props["width"]) - size[0]) > TOL or abs(float(d.props["length"]) - size[1]) > TOL:
                out.append(("error", f"{c} is {d.props['width']} by {d.props['length']} in Dressing.md and {size[0]:g} by {size[1]:g} in the design - owed to step 4a, or 3d if the design is wrong"))
        if str(d.props.get("shape", "rect") if d is not None else "rect") != str(p.props.get("shape", "rect")):
            out.append(("error", f"{c} is shape {d.props.get('shape', 'rect') if d is not None else 'rect'} in Dressing.md and {p.props.get('shape', 'rect')} in the design - owed to step 4a, or 3d if the design is wrong"))
    wanted = {}
    for n in g["lines"]:
        if n.name in ("Bind", "Fill"):
            for c, t in kinds_of(n).items():
                if c in locs and str(locs[c].props.get("type")) != t:
                    out.append(("error", f"{c} is type {locs[c].props.get('type')} in Locations.md and {t} in the design - owed to step 3e, or 3d if the design is wrong"))
    for n in g["links"]:
        a, b = str(n.args[0]), str(n.props.get("to"))
        wanted[frozenset((a, b))] = (a, b, str(n.props.get("kind")))
        if str(n.props.get("kind")) == "door" and a in mine and b in mine and not touching(mine[a], mine[b]):
            out.append(("error", f"the design joins {a} and {b} by a door, and they share no wall - owed to step 3d"))
    stated = {(str(n.args[0]), str(n.props["to"])) for n in ways if str(n.args[0]) in members and str(n.props["to"]) in members}
    for k, (a, b, _) in wanted.items():
        for x, y in ((a, b), (b, a)):
            if (x, y) not in stated:
                unwritten = not any(c in q for q in stated for c in (x, y))     # neither end has a way yet: owed, not wrong
                out.append(("warning" if unwritten else "error",
                            f"the design joins {a} and {b}, and Connections.md lacks {x} to {y} - owed to step 3f"))
    for x, y in sorted(stated):
        if frozenset((x, y)) not in wanted:
            out.append(("error", f"Connections.md joins {x} and {y}, which the design does not - owed to step 3f, or 3d if the design lacks it"))
    voids = {(space.outline_value(n.props.get("outline")), tuple(space.point_of(n.props.get("xyz")) or [0.0, 0.0])[:2]) for n in g["lines"] if n.name == "Void"}
    held = {(space.outline_value(n.props.get("outline")), tuple(space.point_of(n.props.get("xyz")) or [0.0, 0.0])[:2])
            for n in region.files.get("Blocks", []) if n.args and str(n.args[0]) == bid and n.name == ("Rock" if danger else "Void")}
    atp = lambda p: f"{p[0]:g},{p[1]:g}"
    for kind, a, b in (("Void", voids, held), (("Rock" if danger else "Void"), held, voids)):
        for o, xy in sorted(a - b, key=str):
            out.append(("error", f"{bid} has a {kind} {space.said(o)} at {atp(list(xy))} in {'its design' if a is voids else 'Blocks.md'} and none in {'Blocks.md' if a is voids else 'its design'} - owed to step 3f"))
    return out


def tables_blocks(region) -> dict[str, kdl.Node]:
    return maps.blocks_of(region)


def check(world, brief) -> list[tuple[str, Path, str]]:
    """Every region's designs and tables against one another: (level, file, message). A region whose BRIEF.md node asks
    for a design and has none approved is owed to step 3d; each approved design is held to the tables."""
    out = []
    for code, region in world.regions.items():
        path = region.dir / "Design.md"
        made = groups(region)
        if code in brief.designs and not any(g["design"].props.get("approved") for g in made.values()):
            out.append(("warning", path if path.exists() else region.dir, f"BRIEF.md asks region {code} for a design, and none is approved - owed to step 3d"))
        for bid, g in made.items():
            node, approved = g["design"], bool(g["design"].props.get("approved"))
            for k in SETTINGS:
                if k in node.props and (bad := tables.design_setting(k, str(node.props[k]))):
                    out.append(("error", path, f"line {node.line}: Design {bid} {bad}"))
            if region.rating.upper() == "DANGEROUS" and any(n.name in ("Use", "Bind", "Fill") for n in g["lines"]):
                ex = expand(region, bid)
                out += [("error" if approved else "warning", f, f"{m} - owed to step 3d") for f, m in ex.problems]
            if approved:
                out += [(level, path, msg) for level, msg in agree(region, bid, g)]
    return out


# -- the commands ----------------------------------------------------------------------

def show_layouts() -> int:
    layouts, problems = read_layouts()
    for lay in layouts.values():
        print(f"{lay.id}  [{', '.join(lay.tags)}]  {lay.name}")
        print(f"    parameters: {', '.join(f'{k} {lo}-{hi}' for k, (lo, hi) in lay.params.items()) or '-'}")
        print(f"    roles:      {', '.join(f'{r}' + (f' x{p['count']}' if 'count' in p else '') for r, p in lay.parts.items())}")
        print(f"    sockets:    {', '.join(f'{s['name']} ({s['bearing']}, {s['width']} ft)' for s in lay.sockets.values()) or '-'}")
    for path, msg in problems:
        print(f"ERROR: {path.relative_to(tables.ROOT)}: {msg}", file=sys.stderr)
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("layouts", help="the library: id, tags, parameters, sockets")
    e = sub.add_parser("expand", help="a design as a `dungeon layout` graph")
    e.add_argument("code")
    e.add_argument("block", nargs="?", help="a block id, where the region has designs for several")
    e.add_argument("--seed", type=int, default=1)
    e.add_argument("--tries", type=int, default=12)
    free = dict(action="store_true", help="ignore the places of the levels a stair joins: they are placed after this one")
    e.add_argument("--free", **free)
    v = sub.add_parser("solve", help="N packings scored, the best K drawn on a contact sheet")
    v.add_argument("code")
    v.add_argument("block", nargs="?")
    v.add_argument("--seeds", type=int, default=12)
    v.add_argument("--keep", type=int, default=3)
    v.add_argument("--out", type=Path, help="where the drawings go; default a folder of the system's temporary directory")
    v.add_argument("--free", **free)
    a = sub.add_parser("accept", help="write one packing's places into Design.md")
    a.add_argument("code")
    a.add_argument("block", nargs="?")
    a.add_argument("--seed", type=int, required=True)
    a.add_argument("--free", **free)
    c = sub.add_parser("check", help="every approved design against its tables")
    c.add_argument("code", nargs="?")
    args = ap.parse_args()
    if args.command == "layouts":
        return show_layouts()
    world = maps.world_for(tables.SETTING)
    if args.command == "check":
        found = [f for f in check(world, tables.Brief(world.schema)) if not args.code or f"/region/{args.code}/" in str(f[1])]
        for level, path, msg in found:
            print(f"{level.upper()}: {Path(path).relative_to(tables.ROOT)}: {msg}")
        print(f"{sum(f[0] == 'error' for f in found)} error(s), {sum(f[0] == 'warning' for f in found)} warning(s)")
        return 1 if any(f[0] == "error" for f in found) else 0
    region = world.regions.get(args.code)
    if region is None:
        print(f"ERROR: {args.code} is no region of this setting", file=sys.stderr)
        return 1
    blocks = [str(n.args[0]) for n in region.files.get("Design", []) if n.name == "Design" and n.args]
    bid = args.block or (blocks[0] if len(blocks) == 1 else None)
    if bid is None:
        print(f"ERROR: {args.code} holds {'no design' if not blocks else 'designs for ' + ', '.join(blocks) + ': name one'}", file=sys.stderr)
        return 1
    if args.command == "solve":
        return solve(region, bid, args.seeds, args.keep, args.out, args.free)
    if args.command == "accept":
        return accept(region, bid, args.seed, args.free)
    done = expand(region, bid, args.seed, args.tries, args.free)
    for path, msg in done.problems:
        print(f"ERROR: {path.relative_to(tables.ROOT)}: {msg}", file=sys.stderr)
    if done.graph is not None:
        print(json.dumps(done.graph, indent=1))
    return 1 if done.problems else 0


if __name__ == "__main__":
    sys.exit(main())
