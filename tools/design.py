#!/usr/bin/env python3
"""Block designs: the layouts a block is built from, and the graph `artgen dungeon layout` packs.

  python3 tools/design.py layouts                  # the library: id, tags, parameters, sockets
  python3 tools/design.py expand CODE [BLOCK]      # a design as a `dungeon layout` graph, JSON

A design (`setting/region/[Code]/Design.md`, `patterns/Region_Schema.md`) names the layouts a block
uses (`layouts/`, `patterns/Layout_Schema.md`), binds each layout's roles to location codes, joins
their sockets and leaves the rest of its locations to fill. `expand` turns it into rooms and ways:
a role's rooms are its bound locations, sized at the middle of the layout's range, a Tie joins the
rooms of two roles, a Join the rooms at two sockets or a socket and a location, a fill room the
size its Fill states. The ground is the design's `outline`, else left to the least square its `fill`
allows; its voids are kept out. Where the design leaves `fill`, `passages` or `detour` unset BRIEF.md's
`pack` line gives them. Prints the graph on stdout and every problem on stderr, and exits 1 on any.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import math
import re
import sys
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
RING = 24                       # sides of the polygon a circular outline is given as
SHAPES = {"rect": "rect", "cave": "cave", "round": "round", "octagon": "octagon", "hexagon": "hexagon", "hall": "rect"}
NODES = {"Layout": {"name", "tags", "source"}, "Param": {"name", "range"},
         "Part": {"role", "shape", "width", "length", "count", "at", "focal"}, "Tie": {"a", "b", "kind"},
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

def mid(lo: int, hi: int, grid: int = 1) -> int:
    return max(grid, int((lo + hi) / 2 / grid + 0.5) * grid)


class Expand:
    """One block's design as the `dungeon layout` graph: `graph`, or `problems`."""

    def __init__(self, region, brief: tables.Brief, bid: str, seed: int = 1, tries: int = 12):
        self.region, self.bid, self.problems = region, bid, []
        self.graph = None
        self.compass = space.compass()
        self.layouts, bad = read_layouts()
        self.problems += [f"{path.relative_to(tables.ROOT)}: {msg}" for path, msg in bad]
        lines = [n for n in region.files.get("Design", []) if n.args]
        self.node = next((n for n in lines if n.name == "Design" and str(n.args[0]) == bid), None)
        if self.node is None:
            self.problems.append(f"{region.code} holds no Design for {bid}")
            return
        mine = lambda name: [n for n in lines if n.name == name and str(n.args[0]) == bid]
        self.locations = words(self.node.props.get("locations"))
        self.uses = {}
        for n in mine("Use"):
            self.use(n)
        self.rooms: dict[tuple[str, str], list[str]] = {}      # (use, role) -> the locations bound to it
        self.size: dict[str, tuple[int, int]] = {}
        self.shape: dict[str, str] = {}
        self.fixed: set[str] = set()                           # rooms a layout shapes, which may not turn
        for n in mine("Bind"):
            self.bind(n)
        for n in mine("Fill"):
            self.fill(n)
        unbound = [c for c in self.locations if c not in self.size]
        if unbound:
            self.problems.append(f"{', '.join(unbound)} of {bid} are in no Bind or Fill")
        self.ways: dict[frozenset, dict] = {}
        for uid, (lay, _) in self.uses.items():
            self.ties(uid, lay)
        self.exits = []
        for n in mine("Join"):
            self.join(n)
        if not self.problems:
            self.graph = self.build(brief, mine("Void"), seed, tries)

    def say(self, n: kdl.Node, msg: str):
        self.problems.append(f"{self.region.dir.relative_to(tables.ROOT)}/Design.md: line {n.line}: {msg}")

    def use(self, n: kdl.Node):
        uid, lay = str(n.props.get("id")), self.layouts.get(str(n.props.get("layout")))
        if lay is None or uid in self.uses or not uid or uid == "None":
            return self.say(n, f"Use states one id, once, and a layout of layouts/ ({', '.join(self.layouts)})")
        given = dict(re.findall(r"([\w-]+)=(\d+)", str(n.props.get("params", ""))))
        values = {}
        for name, (lo, hi) in lay.params.items():
            values[name] = int(given.pop(name)) if name in given else mid(lo, hi, GRID if hi >= 10 else 1)
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
                self.size[c] = (self.number(lay, values, part["width"], GRID), self.number(lay, values, part["length"], GRID))
                self.shape[c] = part.get("shape", "rect")
                self.fixed.add(c)

    def fill(self, n: kdl.Node):
        for c in words(n.props.get("locations")):
            if c in self.size:
                self.say(n, f"{c} is bound twice")
            elif c not in self.locations:
                self.say(n, f"{c} is not one of the design's locations")
            else:
                self.size[c] = (int(n.props.get("width", ROOM)), int(n.props.get("length", ROOM)))
                self.shape[c] = "rect"

    def tie(self, a: str, b: str, bearing: float | None):
        key = frozenset((a, b))
        if a != b and key not in self.ways:
            self.ways[key] = {"a": a, "b": b, **({"bearing": bearing} if bearing is not None else {})}

    def ties(self, uid: str, lay: Layout):
        look = lambda role: self.rooms.get((uid, role), [])
        for t in lay.ties:
            a, b = look(t["a"]), look(t["b"])
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

    def build(self, brief: tables.Brief, voids: list, seed: int, tries: int) -> dict | None:
        node = self.node
        rates = brief.packing(self.region.code)
        if (m := re.fullmatch(r"(\d+)-(\d+)%", str(node.props.get("fill", "")))):
            rates["fill"] = (int(m[1]) / 100, int(m[2]) / 100)
        if "passages" in node.props:
            rates["passages"] = int(str(node.props["passages"])[:-1]) / 100
        if "detour" in node.props:
            rates["detour"] = maps.feet(str(node.props["detour"]))
        if (m := re.fullmatch(r"(\d+)-(\d+) feet", str(node.props.get("spacing", "")))):   # the passage wanted between rooms
            if "passages" not in node.props and int(m[1]) >= 10:
                rates["passages"] = 1.0
            if "detour" not in node.props:
                rates["detour"] = float(m[2])
        if rates["fill"] is None or rates["passages"] is None:
            return self.say(node, "BRIEF.md states no pack fill and passages") or None
        poly, side = ground(space.outline_value(node.props.get("outline")))
        frame = dungeon.framed(poly, side)
        pins = {c: p for c in self.locations if (p := space.settled().pin(c))}
        rocks = [(space.point_of(v.props.get("xyz")) or [0.0, 0.0], s) for v in voids
                 if (s := space.outline_value(v.props.get("outline"))) is not None]
        if (pins or rocks) and not (poly or side):
            held = f"a stair into {', '.join(pins)}" if pins else "a void"
            return self.say(node, f"{held} is placed in the design's frame, so the design states an outline") or None
        rooms = []
        for c in self.locations:
            w, h = self.size[c]
            r = {"id": c, "w": w / GRID, "h": h / GRID, "shape": SHAPES[self.shape[c]], "hall": self.shape[c] == "hall",
                 "turns": c not in self.fixed and not any("bearing" in way for k, way in self.ways.items() if c in k)}
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


def expand(region, bid: str, seed: int = 1, tries: int = 12) -> Expand:
    world = maps.world_for(tables.SETTING)
    return Expand(region, tables.Brief(world.schema), bid, seed, tries)


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
    args = ap.parse_args()
    if args.command == "layouts":
        return show_layouts()
    world = maps.world_for(tables.SETTING)
    region = world.regions.get(args.code)
    if region is None:
        print(f"ERROR: {args.code} is no region of this setting", file=sys.stderr)
        return 1
    blocks = [str(n.args[0]) for n in region.files.get("Design", []) if n.name == "Design" and n.args]
    bid = args.block or (blocks[0] if len(blocks) == 1 else None)
    if bid is None:
        print(f"ERROR: {args.code} holds {'no design' if not blocks else 'designs for ' + ', '.join(blocks) + ': name one'}", file=sys.stderr)
        return 1
    done = expand(region, bid, args.seed, args.tries)
    for p in done.problems:
        print(f"ERROR: {p}", file=sys.stderr)
    if done.graph is not None:
        print(json.dumps(done.graph, indent=1))
    return 1 if done.problems else 0


if __name__ == "__main__":
    sys.exit(main())
