#!/usr/bin/env python3
"""Every region, block and location at a point in one space, and what does not fit: the dry fire.

  python3 tools/space.py [--only REGION]
  python3 tools/space.py settle [REGION]
  python3 tools/space.py from CODE to CODE
  python3 tools/space.py section [--out FILE.svg] [--along x|y] [--heights N]

x runs east, y north and z up, in feet, from the origin: the centre of the sheet BRIEF.md's `origin`
names - the master map - at the sea, else a point the regions' own places are stated from. Each
thing states its place in its parent's frame - a region in the setting's, a block in its region's,
a location in its block's, or its region's where it is in none - and its absolute place adds its
ancestors'.

A SAFE or DANGEROUS region states x,y,z; a WILD one states x,y, and stands at the origin's level, so
its locations' heights are their own. A region's point is its way in. Every block and location
states x,y,z, but a WILD location on the master map may leave z to its ground there, and a WILD
region's `elevation` bounds its locations' heights. Where a region states fewer axes than it should,
the master sheet gives its plan and a SAFE one's ground, and a way's climb, bearing and distance
from a placed region give the rest; a climbing way between two DANGEROUS blocks sets one block's
centre over the other's. `settle` writes what these give. A thing placed `against`
a sibling starts at its origin, slides across the side by its xyz, moves out along the side
until their outlines last touch, then takes its xyz along the side as a gap; above or below,
its floor meets the other's roof.

A void is ground in a SAFE or WILD block that no location takes: a location whose outline meets one is a problem.

Prints each thing's place in its parent and in the setting, its outline and its floor and roof,
then each problem; exits 1 on an error. `settle` writes into Regions.md the place of each region
that states none but whose sheet or joins give it in full, and never moves one that states one.
`from` prints how far, in what direction and how far up or down one region, block or location lies
from another, by their places in the setting. `section` draws the setting from the side.
"""
from __future__ import annotations

import argparse
from html import escape
import functools
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kdl                      # noqa: E402
import maps                     # noqa: E402
import site_common as sc        # noqa: E402
import tables                   # noqa: E402

TOUCH = 1.0                     # square feet two outlines may share and still only touch
CIRCLE = 128                    # sides of the polygon a circle is measured as
NEAR = 10                       # feet a stated distance may miss by, or a tenth of it where more


@dataclass
class Thing:
    code: str
    kind: str                   # region, block, location or stop
    region: str
    parent: "Thing | None"
    at: list = field(default_factory=lambda: [None, None, None])   # its place in its parent's frame
    by: str = ""
    outline: tuple | None = None    # ("rect", w, l), ("circle", r) or ("poly", points)
    height: float = 0.0
    file: Path | None = None
    line: int = 0
    anchor: tuple | None = None     # (code, side): placed against a sibling
    shift: list | None = None       # with an anchor, its xyz: a slide across the side, then a gap along it
    ground: float | None = None     # a SAFE or WILD location's ground, above its region's way in


# -- outlines, as polygons in plan ------------------------------------------------------

def polygon(outline: tuple | None, x: float, y: float) -> list[tuple[float, float]]:
    """An outline round (x, y), anticlockwise; a point where it has none."""
    if outline is None:
        return [(x, y)]
    if outline[0] == "circle":
        r = outline[1]
        return [(x + r * math.cos(2 * math.pi * i / CIRCLE), y + r * math.sin(2 * math.pi * i / CIRCLE))
                for i in range(CIRCLE)]
    if outline[0] == "poly":
        p = [(x + a, y + b) for a, b in outline[1]]
        return p if signed(p) > 0 else p[::-1]
    w, l = outline[1] / 2, outline[2] / 2
    return [(x - w, y - l), (x + w, y - l), (x + w, y + l), (x - w, y + l)]


def signed(p: list) -> float:
    return sum(p[i - 1][0] * p[i][1] - p[i][0] * p[i - 1][1] for i in range(len(p))) / 2


def area(p: list) -> float:
    return abs(signed(p))


def turn(a, b, c) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def pieces(p: list) -> list[list]:
    """A simple anticlockwise polygon as convex pieces: itself where convex, else triangles cut off it ear by ear."""
    if all(turn(p[i - 2], p[i - 1], p[i]) >= 0 for i in range(len(p))):
        return [p]
    out, left = [], list(p)
    while len(left) > 3:
        for i in range(len(left)):
            a, b, c = left[i - 1], left[i], left[(i + 1) % len(left)]
            if turn(a, b, c) > 0 and not any(turn(a, b, q) >= 0 and turn(b, c, q) >= 0 and turn(c, a, q) >= 0
                                             for q in left if q not in (a, b, c)):
                out.append([a, b, c])
                del left[i]
                break
        else:
            break
    return out + [left]


def clipped(a: list, b: list) -> float:
    """The area two convex anticlockwise polygons share, by clipping one with the other."""
    out = a
    for i in range(len(b)):
        (x1, y1), (x2, y2) = b[i - 1], b[i]
        side = lambda p: (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1)
        kept = []
        for j in range(len(out)):
            p, q = out[j - 1], out[j]
            if side(q) >= 0:
                if side(p) < 0:
                    kept.append(cross(p, q, side))
                kept.append(q)
            elif side(p) >= 0:
                kept.append(cross(p, q, side))
        out = kept
        if not out:
            return 0.0
    return area(out) if len(out) > 2 else 0.0


def cross(p, q, side):
    t = side(p) / (side(p) - side(q))
    return p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])


def common(a: list, b: list) -> float:
    """The area two outlines share."""
    return sum(clipped(x, y) for x in pieces(a) for y in pieces(b))


def edges(p: list):
    return zip([p[-1]] + p[:-1], p)


def gap(q, a, b) -> float:
    """A point's distance from a segment."""
    t = max(0.0, min(1.0, ((q[0] - a[0]) * (b[0] - a[0]) + (q[1] - a[1]) * (b[1] - a[1])) / (math.dist(a, b) ** 2 or 1)))
    return math.dist(q, (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))


def inside(q: tuple, p: list, margin: float = -0.5) -> bool:
    """A point lies inside a polygon at least `margin` feet from its edge, or, where margin is
    negative, inside it or within -margin of its edge."""
    if len(p) < 3:
        return False
    within = sum((a[1] > q[1]) != (b[1] > q[1]) and q[0] < a[0] + (q[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                 for a, b in edges(p)) % 2 == 1
    near = min(gap(q, a, b) for a, b in edges(p))
    return within and near >= margin if margin >= 0 else within or near <= -margin


def simple(p: list) -> bool:
    """A polygon has area and no two of its edges cross."""
    sides = list(edges(p))
    for i, (a, b) in enumerate(sides):
        for c, d in sides[i + 1:]:
            if len({a, b, c, d}) == 4 and turn(a, b, c) * turn(a, b, d) < 0 and turn(c, d, a) * turn(c, d, b) < 0:
                return False
    return area(p) > 0


def meets(a: list, b: list) -> bool:
    """Two outlines overlap in plan, beyond touching."""
    if len(a) == 1 and len(b) == 1:
        return False
    if len(a) == 1 or len(b) == 1:
        point, poly = (a, b) if len(a) == 1 else (b, a)
        return inside(point[0], poly, 0.5)
    return common(a, b) > TOUCH


SIDES = {"north": (0, 1), "east": (1, 0), "south": (0, -1), "west": (-1, 0), "above": None, "below": None}


def contact(p: list, q: list, u: tuple) -> float | None:
    """How far outline q moves along u until it last touches outline p: the farthest a vertex
    of either, run along u, meets an edge of the other. None where they never meet."""
    hits = []
    for points, sides, sign in ((q, p, 1), (p, q, -1)):
        for v in points:
            for a, b in (edges(sides) if len(sides) > 1 else ()):
                e = (b[0] - a[0], b[1] - a[1])
                d = (sign * u[0], sign * u[1])
                den = d[0] * e[1] - d[1] * e[0]
                w = (a[0] - v[0], a[1] - v[1])
                if abs(den) < 1e-9:
                    if abs(w[0] * e[1] - w[1] * e[0]) < 1e-9:           # along the edge: its two ends
                        hits += [sign * (w[0] * d[0] + w[1] * d[1]), sign * ((b[0] - v[0]) * d[0] + (b[1] - v[1]) * d[1])]
                    continue
                t, k = (w[0] * e[1] - w[1] * e[0]) / den, (w[0] * d[1] - w[1] * d[0]) / den
                if -1e-9 <= k <= 1 + 1e-9:
                    hits.append(sign * t)
    return max(hits) if hits else None


def touching(a: tuple | None, at: tuple, t: tuple | None, side: str, shift: list) -> tuple[float, float] | None:
    """Where a thing of outline t lands placed against one of outline a at `at` on a plan side:
    slid across the side by its shift, out along it until the outlines last touch, rounded
    outward to whole feet, then out by its shift along the side. None where they never meet."""
    u = SIDES[side]
    sx, sy = shift[0] or 0.0, shift[1] or 0.0
    start = (at[0] + (sx if u[0] == 0 else 0), at[1] + (sy if u[1] == 0 else 0))
    d = contact(polygon(a, *at), polygon(t, *start), u)
    if d is None:
        return None
    d = math.ceil(d - 1e-6) + (sx * u[0] + sy * u[1]) * (u[0] + u[1])
    return start[0] + d * u[0], start[1] + d * u[1]


def stacked(a: tuple, b: tuple) -> bool:
    """Two (floor, roof) spans share height, beyond touching; a flat thing shares a solid's
    inside or another flat thing's level."""
    (a0, a1), (b0, b1) = a, b
    if a0 == a1 and b0 == b1:
        return abs(a0 - b0) < 0.5
    return min(a1, b1) - max(a0, b0) > 0.5 or a0 == a1 and b0 < a0 < b1 or b0 == b1 and a0 < b0 < a1


# -- reading places from the tables ------------------------------------------------------

def num(v) -> float:
    s = str(v)
    return -maps.feet(s[1:]) if s.startswith("-") else maps.feet(s)


def point_of(v) -> list | None:
    """A `point` value as [x, y, z], z None where unstated; None where it is no point."""
    if v is None or not tables.POINT_RE.fullmatch(str(v)):
        return None
    c = [float(x) for x in str(v).split(",")]
    return c + [None] * (3 - len(c))


def outline_value(v) -> tuple | None:
    """An `outline` value as ("rect", w, l), ("circle", r) or ("poly", points); None where it is none."""
    if v is None or not tables.OUTLINE_RE.fullmatch(str(v)):
        return None
    kind, *rest = str(v).split()
    if kind == "poly":
        return "poly", [tuple(float(c) for c in q.split(",")) for q in rest]
    return (kind, *(float(x) for x in rest))



def shape_outline(shape: str, w: float, h: float, points=None) -> list[tuple[float, float]]:
    """A room's outline in feet east and south of its box's centre, clockwise on the page as
    artgen draws a wall. A round room is its box's ellipse in 64 sides; an octagon cuts its box's
    corners so a square one is regular; a hexagon has flat north and south walls and points east
    and west; a poly is its own points."""
    a, b = w / 2, h / 2
    if shape == "round":
        return [(a * math.cos(math.pi * i / 32), b * math.sin(math.pi * i / 32)) for i in range(64)]
    if shape == "octagon":
        c = min(w, h) / (2 + math.sqrt(2))
        return [(-a + c, -b), (a - c, -b), (a, -b + c), (a, b - c), (a - c, b), (-a + c, b), (-a, b - c), (-a, -b + c)]
    if shape == "hexagon":
        return [(-a / 2, -b), (a / 2, -b), (a, 0.0), (a / 2, b), (-a / 2, b), (-a, 0.0)]
    if shape == "diamond":
        return [(0.0, -b), (a, 0.0), (0.0, b), (-a, 0.0)]
    if shape == "poly" and points:
        p = [(float(x), float(y)) for x, y in points]
        return p if sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(p, p[1:] + p[:1])) > 0 else p[::-1]
    return [(-a, -b), (a, -b), (a, b), (-a, b)]

def outline_of(dress: kdl.Node | None) -> tuple | None:
    """A location's outline: its own, else its shape's in its width and length."""
    p = dress.props if dress is not None else {}
    if "outline" in p:
        return outline_value(p["outline"])
    if "width" not in p or "length" not in p:
        return None
    w, l = float(p["width"]), float(p["length"])
    shape = str(p.get("shape"))
    if shape in ("octagon", "hexagon"):
        return "poly", [(x, -y) for x, y in shape_outline(shape, w, l)]
    return ("circle", w / 2) if shape == "round" else ("rect", w, l)


def said(outline: tuple | None) -> str:
    if outline is None:
        return "-"
    if outline[0] == "poly":
        return f"poly of {len(outline[1])} points"
    return " ".join([outline[0]] + [fmt(v) for v in outline[1:]])


def fmt(v) -> str:
    if v is None:
        return "?"
    v = round(v, 1) + 0.0
    return f"{v:g}" if v == int(v) else f"{v:.1f}"


def point(v: list) -> str:
    return ",".join(fmt(c) for c in v)


@functools.cache
def compass() -> list[str]:
    return list(tables.Schema().setting_enums["Compass"])


def vector(bearing: str, d: float) -> tuple[float, float]:
    a = math.radians(compass().index(bearing) * 22.5)
    return d * math.sin(a), d * math.cos(a)


FORMS = (("way in", ("at",)), ("bearing and distance", ("bearing", "distance")), ("xyz", ("xyz",)),
         ("against", ("against",)))


def forms(node: kdl.Node) -> list[str]:
    """The ways a SAFE or WILD location or stop states its place."""
    p = node.props
    return [f for f, keys in FORMS if any(k in p for k in keys) and (f != "way in" or str(p["at"]) == "way in")]


def twice(got: list[str]) -> bool:
    """A place stated more than one way; xyz with an anchor is its slide and gap, not a second place."""
    return len(set(got) - ({"xyz"} if "against" in got else set())) > 1


def anchor_of(v) -> tuple | None:
    """An `anchor` value as (code, side); None where it is none."""
    if v is None or not tables.ANCHOR_RE.fullmatch(str(v)):
        return None
    code, side = str(v).split()
    return code, side


def own(node: kdl.Node) -> list | None:
    """A SAFE or WILD location's or stop's place from its block's origin, z None where it stands
    on its ground; None where it states no one place, or is placed against another."""
    p, got = node.props, forms(node)
    if len(got) != 1:
        return None
    if got == ["way in"]:
        return [0.0, 0.0, None]
    if got == ["xyz"]:
        return point_of(p["xyz"])
    if "bearing" not in p or "distance" not in p:
        return None
    try:
        return [*vector(str(p["bearing"]), num(p["distance"])), None]
    except (ValueError, KeyError):
        return None


def design_places(region) -> dict[str, list]:
    """The place, in its block's frame, of each location an approved design places."""
    held = {c.strip() for n in region.files.get("Design", []) if n.name == "Design" and n.props.get("approved")
            for c in str(n.props.get("locations", "")).split(",")}
    return {str(n.args[0]): p for n in region.files.get("Design", [])
            if n.name == "Place" and n.args and str(n.args[0]) in held and (p := point_of(n.props.get("xyz")))}


@functools.cache
def settled() -> "Space":
    """The setting's places, resolved once a run."""
    world = maps.world_for(tables.SETTING)
    return Space(world, tables.Brief(world.schema))


def refresh():
    """Forget the tables read so far, after a tool has written them."""
    maps.world_for.cache_clear()
    maps.built.cache_clear()
    settled.cache_clear()


def settle(only: str | None = None) -> list[str]:
    """Writes `xyz` for each region, block and location that states fewer axes than it should but whose
    sheet, joins, design or parent give them all, rounded to whole feet: a region's into Regions.md, a
    block's into Blocks.md, a DANGEROUS room's into Dressing.md, any other location's into Locations.md
    in place of a bearing and distance. Never moves an axis a thing states. Returns what it wrote."""
    import dungeon
    s, wrote = settled(), {}
    for t, axes, _ in s.missing:
        got = t.at[:len(axes.split(","))]
        if None not in got and (only is None or t.region == only):
            name = {"region": "Region", "block": "Block"}.get(t.kind, "Dressing" if t.file.name == "Dressing.md" else "Location")
            wrote.setdefault(t.file, {})[(name, t.code)] = (",".join(str(round(v)) for v in got), t.by)
    said = []
    for path, things in wrote.items():
        lines = path.read_text().split("\n")
        for i, line in enumerate(lines):
            if (m := re.match(r"(\w+) (\S+) ", line)) and (m[1], m[2]) in things:
                for k in ("bearing", "distance"):
                    line = dungeon.without(line, k)
                lines[i] = dungeon.with_prop(line, "xyz", f'"{things[(m[1], m[2])][0]}"')
                said.append(f"{m[2]} at {things[(m[1], m[2])][0]}, by {things[(m[1], m[2])][1] or 'its place'}")
        path.write_text("\n".join(lines))
    if said:
        refresh()
    return said


def offset(region, node: kdl.Node) -> tuple[float, float] | None:
    """A SAFE or WILD location's or stop's (east, north) in feet from its region's way in, or None
    where it has no place."""
    if node.name == "Location" and (t := settled().things.get(str(node.args[0]))):
        w = settled().within(t)
        return None if w[0] is None else (w[0], w[1])
    return None if (o := own(node)) is None else (o[0], o[1])


def centre(d: kdl.Node | None) -> tuple[float, float] | None:
    """A DANGEROUS room's centre (east, north) from its block's, where its Dressing places it."""
    if d is not None and "against" in d.props:
        t = settled().things.get(str(d.args[0]))
        return (t.at[0], t.at[1]) if t and t.at[0] is not None else None
    c = point_of(d.props.get("xyz")) if d is not None else None
    return (c[0], c[1]) if c else None


class Space:
    def __init__(self, world: tables.Setting, brief: tables.Brief):
        self.world, self.brief = world, brief
        self.things: dict[str, Thing] = {}
        self.problems: list[tuple[str, Path | None, str, set]] = []
        self.joins = [(r, n) for r in world.regions.values() for n in r.files.get("Connections", [])
                      if n.args and "to" in n.props]
        self._build()
        while self._anchors() | self._place_blocks() | self._place_regions():
            pass
        self._unanchored()
        self._check()

    def say(self, level: str, file: Path | None, msg: str, *codes: str):
        self.problems.append((level, file, msg, {c.split(".")[0] for c in codes}))

    # -- the tree, and each thing's place in its parent ---------------------------------

    def _build(self):
        self.master = self.brief.origin if self.brief.origin in self.brief.sheets else None
        self.missing: list[tuple[Thing, str, str]] = []     # (thing, the axes it should state, the step that writes them)
        rows = sc.read_tables(tables.SETTING / "Sheets.md")[0].dicts() if (tables.SETTING / "Sheets.md").exists() else []
        self.squares = {n: maps.Sheet(n, node).square for n, node in self.brief.sheets.items()}
        self.on = {}                                    # region -> {sheet: (column, row)}
        self.sea = {}                                   # region -> the ground at its way in, above the sea
        for d in rows:
            self.on.setdefault(d["Region"], {})[d["Sheet"]] = tuple(float(v) for v in d["Way in"].split(","))
        self.centre = {}                                # sheet -> its centre, in squares
        for n, node in self.brief.sheets.items():
            sh = maps.Sheet(n, node)
            self.centre[n] = (sh.cols / 2, sh.rows / 2)
        gazetteer = {str(n.args[0]): n for n in tables.gazetteer() if n.args}
        for code, region in self.world.regions.items():
            g = gazetteer.get(code)
            r = self.things[code] = Thing(code, "region", code, None, file=tables.GAZETTEER, line=g.line if g else 0)
            self._shape(r, g)
            wild = region.rating.upper() == "WILD"
            danger = region.rating.upper() == "DANGEROUS"
            ground = {str(n.args[0]): n for n in region.files.get("Ground", []) if n.name == "At" and n.args}
            g0 = next((n for n in region.files.get("Ground", []) if n.name == "Ground"), None)
            if g0 is not None and "height" in g0.props:
                self.sea[code] = float(g0.props["height"])
            mapped = g0 is not None and self.master is not None and str(g0.props.get("sheet")) == self.master
            c = point_of(g.props.get("xyz")) if g is not None else None
            if c and wild and c[2] is not None:
                self.say("error", r.file, f"line {r.line}: {code} is WILD and states a z: its locations take their "
                                          f"heights from its ground, or state them", code)
            if c:
                r.at, r.by = [c[0], c[1], 0.0 if wild else c[2]], "xyz"
            elif wild:
                r.at[2] = 0.0                           # a WILD region's heights are its locations', above the origin
            if not c or (c[2] is None and not wild):
                self.missing.append((r, "x,y" if wild else "x,y,z", "3b" if code in self.on else "4a"))
            dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
            home = {}
            for i, (bid, block) in enumerate(maps.blocks_of(region).items()):
                b = self.things[bid] = Thing(bid, "block", code, r, file=region.dir / "Blocks.md", line=block.line)
                self._shape(b, block)
                c = point_of(block.props.get("xyz"))
                if self._anchored(b, block):
                    pass
                elif c:
                    b.at, b.by = [c[0], c[1], c[2] if c[2] is not None else 0.0], "xyz"
                elif not danger or i == 0:
                    b.at, b.by = [0.0, 0.0, 0.0], "the region's origin"
                if not b.anchor and (c is None or c[2] is None):
                    self.missing.append((b, "x,y,z", "4a" if danger else "3f"))
                for m in str(block.props.get("locations", "")).split(","):
                    home[m.strip()] = b
            conditions = region.seed("Conditions")
            designed = design_places(region)                 # an approved design places a location its tables have not yet
            for loc, node in region.locations().items():
                d = dress.get(loc)
                t = self.things[loc] = Thing(loc, "location", code, home.get(loc, r))
                if danger:
                    t.file, t.line = region.dir / "Dressing.md", d.line if d is not None else 0
                    p = d.props if d is not None else {}
                    t.height = float(p.get("height", conditions.props.get("height", 0) if conditions else 0))
                    c, by = point_of(p.get("xyz")), "xyz"
                    if c is None and loc in designed:
                        c, by = designed[loc], "design"
                    elif c and loc in designed and math.dist(c[:2], designed[loc][:2]) > 0.5:
                        self.say("error", t.file, f"{loc} lies at {fmt(c[0])},{fmt(c[1])} in the tables and at "
                                                  f"{fmt(designed[loc][0])},{fmt(designed[loc][1])} in its design", loc)
                    if not self._anchored(t, d):
                        t.at = [c[0], c[1], c[2] or 0.0] if c else [None, None, 0.0]
                        t.by = by if c else ""
                        if c is None or c[2] is None:
                            self.missing.append((t, "x,y,z", "4a"))
                else:
                    t.file, t.line = region.dir / "Locations.md", node.line
                    floor = t.parent.at[2] if t.parent.kind == "block" and t.parent.at[2] is not None else 0.0
                    if wild and mapped and loc in ground:   # its ground on the master map, from its parent's floor
                        t.ground = float(ground[loc].props["height"]) - floor
                    if loc in designed and not forms(node):   # its tables state no place: the design's is
                        t.at, t.by = [designed[loc][0], designed[loc][1], None], "design"
                    else:
                        self._own(t, node)
                    if t.at[2] is None and not t.anchor:
                        t.at[2] = t.ground if t.ground is not None else None if wild else 0.0
                        if t.ground is None and forms(node) != ["way in"]:   # a way in is the region's point
                            self.missing.append((t, "x,y,z", "3e" if loc in designed else "3d"))
                self._shape(t, d, of_location=True)
            for i, n in enumerate(region.files.get("Stops", [])):
                if n.args:
                    s = self.things[f"{n.args[0]}/{i + 1}"] = Thing(f"{n.args[0]}/{i + 1}", "stop", code, r,
                                                                    file=region.dir / "Stops.md", line=n.line)
                    self._own(s, n)
            for i, n in enumerate(n for n in region.files.get("Blocks", []) if n.name == "Void" and n.args):
                if (up := self.things.get(str(n.args[0]))) is None or up.kind != "block":
                    continue
                c = point_of(n.props.get("xyz")) or [0.0, 0.0, 0.0]
                v = self.things[f"{n.args[0]}/void{i + 1}"] = Thing(f"{n.args[0]}/void{i + 1}", "void", code, up, [c[0], c[1], c[2] or 0.0],
                                                                    "xyz" if "xyz" in n.props else "block's centre",
                                                                    file=region.dir / "Blocks.md", line=n.line)
                self._shape(v, n)

    def _shape(self, t: Thing, node: kdl.Node | None, of_location: bool = False):
        """A thing's outline, and what is wrong with it: a poly with no area or crossing itself,
        or one whose extent is not the width and length stated beside it."""
        t.outline = outline_of(node) if of_location else outline_value(node.props.get("outline")) if node else None
        if t.outline is None or t.outline[0] != "poly":
            return
        pts, where = t.outline[1], f"{'line ' + str(node.line) + ': ' if node is not None else ''}{t.code}'s outline"
        if not simple(pts):
            self.say("error", t.file, f"{where} has no area or crosses itself", t.code)
        p = node.props if node is not None else {}
        if "width" in p and "length" in p:
            w = max(x for x, _ in pts) - min(x for x, _ in pts)
            l = max(y for _, y in pts) - min(y for _, y in pts)
            if abs(w - float(p["width"])) > 0.5 or abs(l - float(p["length"])) > 0.5:
                self.say("error", t.file, f"{where} is {fmt(w)} by {fmt(l)} feet, where its width and length are "
                                          f"{p['width']} by {p['length']}", t.code)

    def _own(self, t: Thing, node: kdl.Node) -> bool:
        """A SAFE or WILD location's or stop's place in its parent, by the one form it states, or
        True where it is placed against another, to be resolved once that one is."""
        got = forms(node)
        if twice(got):
            self.say("error", t.file, f"line {t.line}: {t.code} is placed by {' and by '.join(got)}: state one", t.code)
        elif "against" in got:
            return self._anchored(t, node)
        elif got and (o := own(node)) is not None:
            t.at, t.by = o, got[0]
        elif got:
            self.say("error", t.file, f"line {t.line}: {t.code} states a bearing or a distance without the other", t.code)
        else:
            self.say("error", t.file, f'line {t.line}: {t.code} states no place: bearing and distance, xyz, against, '
                                      f'or at="way in" (step 3d)', t.code)
        return False

    def _anchored(self, t: Thing, node: kdl.Node | None) -> bool:
        """Notes a thing placed against a sibling, its place left to resolve once the sibling's is."""
        if node is None or "against" not in node.props:
            return False
        t.anchor, t.shift = anchor_of(node.props["against"]), point_of(node.props.get("xyz")) or [0.0, 0.0, None]
        t.at, t.by = [None, None, None], ""
        return t.anchor is not None

    # -- anchors ------------------------------------------------------------------------

    def reach(self, t: Thing) -> tuple[float, float]:
        """A thing's floor and roof above its own origin: a block's lowest floor and highest roof."""
        if t.kind != "block":
            return 0.0, t.height
        spans = [(m.at[2], m.at[2] + m.height) for m in self.things.values() if m.parent is t and m.at[2] is not None]
        return (min(s[0] for s in spans), max(s[1] for s in spans)) if spans else (0.0, 0.0)

    def _anchors(self) -> bool:
        """Places each thing whose anchor is placed: across the side by its slide, then out along it
        until the two outlines touch, then by its gap; above or below, floor on roof."""
        changed = False
        for t in self.things.values():
            if t.anchor is None or t.at[0] is not None or t.by == "unplaceable":
                continue
            code, side = t.anchor
            a = self.things.get(code)
            if a is None or a is t or a.parent is not t.parent or a.kind != t.kind:
                self.say("error", t.file, f"{'line ' + str(t.line) + ': ' if t.line else ''}{t.code} is placed against "
                                          f"{code}, which is no {t.kind} beside it", t.code)
                t.by = "unplaceable"
                continue
            if None in a.at[:2] or a.at[2] is None and side in ("above", "below"):
                continue
            sx, sy, sz = (v or 0.0 for v in t.shift)
            if SIDES[side] is None:
                x, y = a.at[0] + sx, a.at[1] + sy
                if not meets(polygon(a.outline, a.at[0], a.at[1]), polygon(t.outline, x, y)):
                    self.never(t, code, side)
                    continue
                (a0, a1), (t0, t1) = self.reach(a), self.reach(t)
                z = a.at[2] + a1 - t0 + sz if side == "above" else a.at[2] + a0 - t1 + sz
                t.at, t.by, changed = [x, y, z], f"against {code} {side}", True
                continue
            if (xy := touching(a.outline, (a.at[0], a.at[1]), t.outline, side, t.shift)) is None:
                self.never(t, code, side)
                continue
            if t.shift[2] is None and t.ground is not None:
                z = t.ground
            else:
                z = None if a.at[2] is None else a.at[2] + sz
            t.at, t.by, changed = [xy[0], xy[1], z], f"against {code} {side}", True
        return changed

    def never(self, t: Thing, code: str, side: str):
        self.say("error", t.file, f"{'line ' + str(t.line) + ': ' if t.line else ''}{t.code} is placed against {code} "
                                  f"{side}, and their outlines never meet there", t.code, code)
        t.by = "unplaceable"

    def _unanchored(self):
        """An anchor that never resolved: a loop of anchors, or one whose anchor has no place."""
        for t in self.things.values():
            if t.anchor is None or t.at[0] is not None or t.by == "unplaceable":
                continue
            seen, a = [t.code], self.things.get(t.anchor[0])
            while a is not None and a.anchor and a.at[0] is None and a.code not in seen:
                seen.append(a.code)
                a = self.things.get(a.anchor[0])
            loop = a is not None and a.code in seen
            self.say("error" if loop else "warning", t.file,
                     f"{'line ' + str(t.line) + ': ' if t.line else ''}{t.code} is placed against "
                     + (f"a loop of anchors: {' against '.join(seen + [a.code])}" if loop
                        else f"{t.anchor[0]}, which has no place"), t.code)

    # -- resolving places ---------------------------------------------------------------

    def within(self, t: Thing) -> list:
        """A thing's place in its region's frame, axis by axis."""
        if t.kind == "region":
            return [0.0, 0.0, 0.0]
        up = self.within(t.parent) if t.parent.kind != "region" else [0.0, 0.0, 0.0]
        return [None if a is None or b is None else a + b for a, b in zip(up, t.at)]

    def absolute(self, t: Thing) -> list:
        r = self.things[t.region]
        return [None if a is None or b is None else a + b for a, b in zip(r.at, self.within(t))]

    def frame(self, a: Thing, b: Thing) -> tuple[list, list]:
        """Two things' places in the closest frame both are known in: their region's, or the setting's."""
        return (self.within(a), self.within(b)) if a.region == b.region else (self.absolute(a), self.absolute(b))

    def climbs(self, n: kdl.Node) -> float | None:
        """A way's rise to its far end, where it can state one: a Way states none."""
        return float(n.props.get("climb", 0)) if n.name == "Connection" else None

    def stair(self, region, n: kdl.Node) -> bool:
        far = self.world.regions.get(str(n.props["to"]).split(".")[0])
        return (n.name == "Connection" and self.climbs(n) and region.rating.upper() == "DANGEROUS"
                and far is not None and far.rating.upper() == "DANGEROUS")

    def ends(self, region, n: kdl.Node) -> tuple[Thing, Thing] | None:
        a, b = self.things.get(str(n.args[0])), self.things.get(str(n.props["to"]))
        return (a, b) if a and b else None

    def _place_blocks(self) -> bool:
        """A DANGEROUS region's later blocks, each over or under the block a climbing way joins it to."""
        moved = False
        for region, n in self.joins:
            if not self.stair(region, n) or not (e := self.ends(region, n)) or e[0].region != e[1].region:
                continue
            for near, far, rise in ((e[0], e[1], self.climbs(n)), (e[1], e[0], -self.climbs(n))):
                nb, fb = near.parent, far.parent
                if nb is not fb and nb.anchor is None and nb.at[0] is None and fb.at[0] is not None \
                        and None not in (near.at[2], far.at[2]):
                    nb.at = [fb.at[0], fb.at[1], fb.at[2] + far.at[2] + rise - near.at[2]]
                    nb.by, moved = f"over or under {fb.code}, from {n.args[0]} to {n.props['to']}", True
        return moved

    def _place_regions(self) -> bool:
        """Each region's place from the origin, in plan and in height apart, by the first sheet or
        join reaching a placed region, in gazetteer and file order."""
        regions = [self.things[c] for c in self.world.regions if self.things[c].anchor is None]
        moved = False
        for r in regions:
            moved |= self._from_master(r)
        for r in regions:
            for q in regions:
                if q is not r and (sheet := self.shared(r, q)):
                    moved |= self._from_sheet(r, q, sheet)
        for region, n in self.joins:
            if (e := self.ends(region, n)) and e[0].region != e[1].region:
                moved |= self._from_join(region, n, *e) | self._from_join(region, n, *e, back=True)
        return moved

    def shared(self, r: Thing, q: Thing) -> str | None:
        both = set(self.on.get(r.code, {})) & set(self.on.get(q.code, {}))
        return min(both, key=lambda s: self.squares[s]) if both else None

    def _from_master(self, r: Thing) -> bool:
        """A region on the master sheet: its way in's square from the sheet's centre, and a SAFE one's ground there."""
        if self.master is None or self.master not in self.on.get(r.code, {}):
            return False
        done = False
        if r.at[0] is None:
            r.at[:2] = self.on_master(r.code)
            r.by, done = f"sheet {self.master}", True
        if r.at[2] is None and self.world.regions[r.code].rating.upper() == "SAFE" and r.code in self.sea:
            r.at[2] = self.sea[r.code]
            r.by, done = (r.by + "; " if r.by else "") + f"its ground on sheet {self.master}", True
        return done

    def on_master(self, code: str) -> list[float]:
        (x, y), (cx, cy), sq = self.on[code][self.master], self.centre[self.master], self.squares[self.master]
        return [(x - cx) * sq, (cy - y) * sq]

    def _from_sheet(self, r: Thing, q: Thing, sheet: str) -> bool:
        """r's plan from q's, on a sheet they share; only the master map gives a height."""
        if r.at[0] is not None or q.at[0] is None:
            return False
        (xr, yr), (xq, yq), sq = self.on[r.code][sheet], self.on[q.code][sheet], self.squares[sheet]
        r.at[:2] = [q.at[0] + (xr - xq) * sq, q.at[1] - (yr - yq) * sq]
        r.by = f"sheet {sheet} from {q.code}"
        return True

    def _from_join(self, region, n: kdl.Node, a: Thing, b: Thing, back: bool = False) -> bool:
        """Places a's region from b's across the way a to b, or b's from a's where `back`."""
        sign = -1 if back else 1
        near, far = (b, a) if back else (a, b)
        r, q = self.things[near.region], self.things[far.region]
        if r.anchor is not None:
            return False
        wn, wf, done = self.within(near), self.within(far), False
        how = f"from {n.args[0]} to {n.props['to']}"
        rise = self.climbs(n)
        if r.at[2] is None and q.at[2] is not None and rise is not None and wn[2] is not None and wf[2] is not None:
            r.at[2] = q.at[2] + wf[2] - sign * rise - wn[2]
            r.by, done = (r.by + "; " if r.by else "") + f"height {how}", True
        if r.at[0] is None and q.at[0] is not None:
            if self.stair(region, n) and near.parent.at[0] is not None and far.parent.at[0] is not None:
                fb, nb = self.within(far.parent), self.within(near.parent)
                r.at[:2] = [q.at[0] + fb[0] - nb[0], q.at[1] + fb[1] - nb[1]]
            elif "bearing" in n.props and "distance" in n.props and None not in wn[:2] + wf[:2]:
                dx, dy = vector(str(n.props["bearing"]), num(n.props["distance"]))
                r.at[:2] = [q.at[0] + wf[0] - sign * dx - wn[0], q.at[1] + wf[1] - sign * dy - wn[1]]
            else:
                return done
            r.by, done = (r.by + "; " if r.by else "") + f"plan {how}", True
        return done

    def stairs_from(self, code: str) -> list[str]:
        """The DANGEROUS rooms a stair from room `code` reaches: by a climbing Connection either way, or by a
        design's Route with a stair, which is all there is before the Connections are written."""
        far = []
        for r in self.world.regions.values():
            for n in r.files.get("Connections", []):
                if n.args and self.stair(r, n) and code in (str(n.args[0]), str(n.props["to"])):
                    far.append(str(n.props["to"]) if str(n.args[0]) == code else str(n.args[0]))
            for n in r.files.get("Design", []):
                ends = [e.split(":")[0].strip() for e in str(n.props.get("ends", "")).split(",")]
                if n.name == "Route" and n.props.get("stair") and code in ends and len(ends) == 2:
                    far.append(ends[1 - ends.index(code)])
        rated = lambda c: (g := self.world.regions.get(c.split(".")[0])) is not None and g.rating.upper() == "DANGEROUS"
        return [f for f in dict.fromkeys(far) if rated(f)]

    def pin(self, code: str) -> tuple[float, float, float, float] | None:
        """The room a way that climbs from room `code` reaches, as (east, north, width, length) from
        the centre of `code`'s block: from where both lie, else from the far room's own block,
        whose centre a stair's two blocks share until placed."""
        t = self.things.get(code)
        for far in self.stairs_from(code):
            f = self.things.get(far)
            if f is None or f.at[0] is None or f.outline is None:
                continue
            if t is None:                       # a room not yet written: its block is its region's first, centred on the region's origin
                near, far = self.absolute(self.things[code.split(".")[0]]), self.absolute(f)
            else:
                near, far = self.frame(t.parent, f)
            x, y = (far[0] - near[0], far[1] - near[1]) if None not in near[:2] + far[:2] else (f.at[0], f.at[1])
            if f.outline[0] == "poly":          # a polygon room: the box it fits in
                w, l = (max(v) - min(v) for v in zip(*f.outline[1]))
            else:
                w, l = (2 * f.outline[1],) * 2 if f.outline[0] == "circle" else f.outline[1:3]
            return x, y, w, l
        return None

    # -- what does not fit --------------------------------------------------------------

    def span(self, t: Thing, at: list) -> tuple[float, float] | None:
        """A thing's floor and roof, at its place `at`."""
        return None if at[2] is None else tuple(at[2] + r for r in self.reach(t))

    def _check(self):
        things = list(self.things.values())
        for t, axes, step in self.missing:
            where = f"{'line ' + str(t.line) + ': ' if t.line else ''}{t.code}"
            got = t.at[:len(axes.split(","))]
            if None in got:
                self.say("warning", t.file, f"{where} states no xyz {axes}, and nothing gives it one (step {step})", t.code)
            else:
                self.say("warning", t.file, f"{where} states no xyz {axes}: {point(got)}, by {t.by or 'its place'} "
                                            f"(step {step})", t.code)
        self._elevations([t for t in things if t.kind == "location"])
        self._overlaps([t for t in things if t.kind == "location"])
        self._overlaps([t for t in things if t.kind == "block" and t.outline is not None])
        self._outside(things)
        self._voids([t for t in things if t.kind == "void"], [t for t in things if t.kind == "location"])
        self._ways()
        self._sheets()

    def _elevations(self, locations: list[Thing]):
        """Each WILD location's height within its region's `elevation`."""
        gazetteer = {str(n.args[0]): n for n in tables.gazetteer() if n.args}
        for t in locations:
            g = gazetteer.get(t.region)
            m = tables.SPAN_RE.fullmatch(str(g.props.get("elevation", ""))) if g is not None else None
            if not m or (z := self.absolute(t)[2]) is None:
                continue
            low, high = (maps.feet(f"{v} {m.group(3)}") for v in (m.group(1), m.group(2) or m.group(1)))
            if not low - 0.5 <= z <= high + 0.5:
                self.say("error", t.file, f"{t.code} stands {fmt(z)} feet up, outside {t.region}'s elevation of "
                                          f"{g.props['elevation']}", t.code)

    def _overlaps(self, group: list[Thing]):
        """No two blocks anywhere overlap, nor two locations of one region. Regions may: a
        DANGEROUS region can lie within a SAFE one within a WILD one, its rooms under their ground."""
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                if a.kind == "location" and a.region != b.region:
                    continue
                pa, pb = self.frame(a, b)
                if None in pa[:2] + pb[:2] or not meets(polygon(a.outline, *pa[:2]), polygon(b.outline, *pb[:2])):
                    continue
                sa, sb = self.span(a, pa), self.span(b, pb)
                if sa is None or sb is None or stacked(sa, sb):
                    self.say("error", a.file, f"{a.code} and {b.code} overlap", a.code, b.code)

    def _outside(self, things: list[Thing]):
        for t in things:
            up = t.parent
            while up is not None and up.outline is None:
                up = up.parent
            if up is None or t.kind == "region":
                continue
            mine, theirs = self.within(t), self.within(up) if up.kind != "region" else [0.0, 0.0, 0.0]
            if None in mine[:2] + theirs[:2]:
                continue
            p, q = polygon(t.outline, *mine[:2]), polygon(up.outline, *theirs[:2])
            if (len(p) == 1 and not inside(p[0], q)) or (len(p) > 1 and area(p) - common(p, q) > TOUCH):
                self.say("error", t.file, f"{'line ' + str(t.line) + ': ' if t.line else ''}{t.code} lies outside "
                                          f"{up.code}'s {said(up.outline)}", t.code)

    def _voids(self, voids: list[Thing], locations: list[Thing]):
        """No location of a block stands in one of its voids."""
        for v in voids:
            for t in locations:
                if t.parent is v.parent and None not in t.at[:2] and meets(polygon(t.outline, *t.at[:2]), polygon(v.outline, *v.at[:2])):
                    self.say("error", t.file, f"{t.code} stands in {v.parent.code}'s void (Blocks.md line {v.line})", t.code)

    def _ways(self):
        for region, n in self.joins:
            if not (e := self.ends(region, n)):
                continue
            a, b = e
            file, where = region.dir / "Connections.md", f"line {n.line}: {n.args[0]} to {n.props['to']}"
            pa, pb = self.frame(a, b)
            rise = self.climbs(n)
            if rise is not None and pa[2] is not None and pb[2] is not None and abs(pb[2] - pa[2] - rise) > 0.5:
                self.say("error", file, f"{where} climbs {fmt(rise)} feet, where their floors differ by {fmt(pb[2] - pa[2])}",
                         a.code, b.code)
            plan = None not in pa[:2] + pb[:2]
            if "bearing" in n.props and "distance" in n.props and plan:
                dx, dy = pb[0] - pa[0], pb[1] - pa[1]
                d, want = math.hypot(dx, dy), num(n.props["distance"])
                off = abs((math.degrees(math.atan2(dx, dy)) - compass().index(str(n.props["bearing"])) * 22.5 + 180) % 360 - 180)
                if off > maps.BEARING_SLACK or abs(d - want) > max(NEAR, want / 10):
                    toward = maps.compass(dx, -dy)
                    self.say("error", file, f"{where} runs {n.props['bearing']} {n.props['distance']}, where {b.code} lies "
                                            f"{toward} {fmt(round(d))} feet from {a.code}", a.code, b.code)
            if self.stair(region, n) and a.parent is not b.parent and plan and \
                    not meets(polygon(a.outline, *pa[:2]), polygon(b.outline, *pb[:2])):
                self.say("error", file, f"{where} climbs, and {a.code} does not stand over or under {b.code}", a.code, b.code)
            if a.parent is not b.parent and not rise and "bearing" not in n.props:
                self.say("error", file, f"{where} joins two blocks or regions, and states no bearing and distance or climb",
                         a.code, b.code)

    def _sheets(self):
        regions = [self.things[c] for c in self.world.regions]
        for r in regions:
            if self.master in self.on.get(r.code, {}) and r.by == "xyz":
                want, sq = self.on_master(r.code), self.squares[self.master]
                if math.dist(want, r.at[:2]) > sq:
                    self.say("error", r.file, f"line {r.line}: {r.code} lies at {point(r.at[:2])}, where its way in on sheet "
                                              f"{self.master} is {point(want)}", r.code)
                if self.world.regions[r.code].rating.upper() == "SAFE" and r.code in self.sea and r.at[2] is not None \
                        and abs(r.at[2] - self.sea[r.code]) > NEAR:
                    self.say("error", r.file, f"line {r.line}: {r.code} stands at {fmt(r.at[2])} feet, where its ground "
                                              f"on sheet {self.master} is {fmt(self.sea[r.code])}", r.code)
        for i, r in enumerate(regions):
            for q in regions[i + 1:]:
                if (sheet := self.shared(r, q)) and sheet != self.master and None not in r.at[:2] + q.at[:2]:
                    (xr, yr), (xq, yq), sq = self.on[r.code][sheet], self.on[q.code][sheet], self.squares[sheet]
                    want = ((xr - xq) * sq, -(yr - yq) * sq)
                    if math.dist(want, (r.at[0] - q.at[0], r.at[1] - q.at[1])) > sq:
                        self.say("error", r.file, f"{r.code} lies {fmt(r.at[0] - q.at[0])},{fmt(r.at[1] - q.at[1])} from "
                                                  f"{q.code}, where sheet {sheet} puts it {fmt(want[0])},{fmt(want[1])}", r.code, q.code)

    # -- the report ---------------------------------------------------------------------

    def rows(self, only: str | None = None) -> list[list[str]]:
        out = [["code", "kind", "parent", "place", "in the setting", "outline", "floor..roof", "by"]]
        for t in self.things.values():
            if only and t.region != only:
                continue
            ab = self.absolute(t)
            sp = self.span(t, ab)
            out.append([t.code, t.kind, t.parent.code if t.parent else "setting", point(t.at), point(ab), said(t.outline),
                        "?" if sp is None else f"{fmt(sp[0])}..{fmt(sp[1])}", t.by or "-"])
        return out


def between(space: "Space", a: str, b: str) -> str:
    """How far, which way and how far up or down `b` lies from `a`; an error where either has no place."""
    ends = []
    for code in (a, b):
        t = space.things.get(code)
        if t is None:
            raise ValueError(f"{code} is no region, block or location of this setting")
        ends.append(space.absolute(t))
        if None in ends[-1]:
            raise ValueError(f"{code} has no place in the setting yet: run `python3 tools/space.py --only {t.region}` for why")
    (x0, y0, z0), (x1, y1, z1) = ends
    dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
    d = math.hypot(dx, dy)
    deg = math.degrees(math.atan2(dx, dy)) % 360
    way = "no bearing: the same plan place" if d < 0.5 else f"{compass()[round(deg / 22.5) % 16]} ({deg:.0f} degrees)"
    climb = "level" if abs(dz) < 0.5 else f"{fmt(abs(dz))} feet {'up' if dz > 0 else 'down'}"
    return f"{a} to {b}: {fmt(round(d))} feet {way}, {climb}; {fmt(round(math.sqrt(d * d + dz * dz)))} feet in a straight line"


# -- the section: every placed thing seen from the side --------------------------------

SECTION_WIDTH = 1400            # pixels across
SECTION_EDGE = (150, 40, 40, 70)   # pixels left of, above, right of and below the drawing
DEPTH_STEP = 50                 # feet between the depth marks


def section(space: "Space", along: str | None = None, heights: float = 3.0) -> str:
    """A side elevation of the setting as an SVG: every placed block a band from its floor to its roof, every placed
    location within it, a SAFE or WILD region its floor, and every way between two blocks or regions a line between
    its ends. `along` is the plan axis drawn across, `x` (east to the right) or `y` (north to the right), the one the
    setting spreads farther on where unstated; heights are drawn `heights` times the plan's scale, and say so."""
    names = {str(n.args[0]): str(n.props.get("name", "")) for n in tables.gazetteer() if n.args}
    placed = [(t, ab) for t in space.things.values() if None not in (ab := space.absolute(t))]

    def run(t: Thing, ab: list, k: int) -> tuple[float, float]:
        vs = [q[k] for q in polygon(t.outline, ab[0], ab[1])]
        return min(vs), max(vs)

    if not placed:
        return ""
    k = "xy".index(along) if along else max((0, 1), key=lambda k: max(run(t, ab, k)[1] for t, ab in placed) - min(run(t, ab, k)[0] for t, ab in placed))
    lo, hi = min(run(t, ab, k)[0] for t, ab in placed), max(run(t, ab, k)[1] for t, ab in placed)
    spans = {t.code: sp for t, ab in placed if (sp := space.span(t, ab))}
    top, bottom = max([0.0] + [sp[1] for sp in spans.values()]), min([0.0] + [sp[0] for sp in spans.values()])
    left, above, right, below = SECTION_EDGE
    px = (SECTION_WIDTH - left - right) / ((hi - lo) or 1)
    X = lambda v: left + (v - lo) * px
    Y = lambda z: above + (top - z) * px * heights
    height = Y(bottom) + below
    want = maps.look("dungeon")
    ink, floor, rock = want.get("ink", "#222222"), want.get("floor", "#ffffff"), want.get("rock-color", "#dddddd")
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SECTION_WIDTH} {height:.0f}" width="{SECTION_WIDTH}" height="{height:.0f}" '
           f'role="img" aria-label="Section" font-family="sans-serif" font-size="11" fill="{ink}">',
           f'<style>text {{ paint-order: stroke; stroke: {floor}; stroke-width: 3px; stroke-linejoin: round; }}</style>',
           f'<rect width="{SECTION_WIDTH}" height="{height:.0f}" fill="{floor}"/>',
           f'<rect x="{left}" y="{Y(0):.1f}" width="{SECTION_WIDTH - left - right}" height="{Y(bottom) - Y(0) + 20:.1f}" fill="{rock}"/>']
    for z in range(0, int(bottom) - 1, -DEPTH_STEP):
        out.append(f'<line x1="{left - 6}" y1="{Y(z):.1f}" x2="{left}" y2="{Y(z):.1f}" stroke="{ink}"/>'
                   f'<text x="{left - 10}" y="{Y(z) + 4:.1f}" text-anchor="end">{"ground" if z == 0 else f"{z} ft"}</text>')
    regions = [(t, ab) for t, ab in placed if t.kind == "region"]
    for t, ab in regions:                               # a region with no block that stands: its floor, across its area
        if space.world.regions[t.code].rating.upper() == "DANGEROUS" or t.outline is None:
            continue
        a, b = run(t, ab, k)
        out.append(f'<line x1="{X(a):.1f}" y1="{Y(ab[2]):.1f}" x2="{X(b):.1f}" y2="{Y(ab[2]):.1f}" stroke="{ink}" stroke-width="1.5" stroke-dasharray="6 3"/>'
                   f'<text x="{X(b):.1f}" y="{Y(ab[2]) - 6:.1f}" text-anchor="end">{t.code} {escape(names.get(t.code, ""))}</text>')
    for t, ab in placed:
        if t.kind == "block" and t.code in spans and space.world.regions[t.region].rating.upper() == "DANGEROUS":
            (a, b), (z0, z1) = run(t, ab, k), spans[t.code]
            out.append(f'<rect x="{X(a):.1f}" y="{Y(z1):.1f}" width="{(b - a) * px:.1f}" height="{Y(z0) - Y(z1):.1f}" fill="{floor}" fill-opacity="0.35" stroke="{ink}" stroke-width="0.6"/>'
                       f'<text x="{X(a) - 6:.1f}" y="{(Y(z0) + Y(z1)) / 2 + 4:.1f}" text-anchor="end">{t.region} {escape(names.get(t.region, "").split(" - ")[0])}</text>')
    for t, ab in placed:
        if t.kind != "location":
            continue
        (a, b), sp = run(t, ab, k), spans.get(t.code) or (ab[2], ab[2])
        tall = max(Y(sp[0]) - Y(sp[1]), 3)              # a place with no height is a mark on its ground
        out.append(f'<rect x="{X(a):.1f}" y="{Y(sp[0]) - tall:.1f}" width="{max((b - a) * px, 1.5):.1f}" height="{tall:.1f}" fill="{floor}" stroke="{ink}" stroke-width="0.8"><title>{t.code}</title></rect>')
    seen = set()
    for region, n in space.joins:
        if not (e := space.ends(region, n)) or frozenset(c.code for c in e) in seen:
            continue
        pa, pb = space.absolute(e[0]), space.absolute(e[1])
        if None in pa + pb or e[0].parent is e[1].parent and abs(pa[2] - pb[2]) < 0.5:     # a level way within a block is its map's
            continue
        seen.add(frozenset(c.code for c in e))
        out.append(f'<line x1="{X(pa[k]):.1f}" y1="{Y(pa[2]):.1f}" x2="{X(pb[k]):.1f}" y2="{Y(pb[2]):.1f}" stroke="{ink}" stroke-width="1.6"><title>{e[0].code} to {e[1].code}</title></line>')
        if e[0].region != e[1].region and abs(pa[k] - pb[k]) * px > 40:      # a long way between regions names its ends
            for c, q, far in ((e[0], pa, pb), (e[1], pb, pa)):
                out.append(f'<text x="{X(q[k]):.1f}" y="{Y(q[2]) - 5:.1f}" text-anchor="{"end" if q[k] > far[k] else "start"}" font-size="10">{c.code}</text>')
    bar = 10 ** math.floor(math.log10((hi - lo) / 4 or 1))
    out.append(f'<line x1="{left}" y1="{height - 30:.0f}" x2="{left + bar * px:.1f}" y2="{height - 30:.0f}" stroke="{ink}" stroke-width="2"/>'
               f'<text x="{left}" y="{height - 12:.0f}">{bar:g} feet across; heights drawn {heights:g} times as tall; '
               f'{("west", "south")[k]} at the left, {("east", "north")[k]} at the right</text>')
    return "\n".join(out + ["</svg>"])


def main() -> int:
    if sys.argv[1:2] == ["from"]:
        if len(sys.argv) != 5 or sys.argv[3] != "to":
            print("usage: space.py from CODE to CODE")
            return 2
        world = maps.world_for(tables.SETTING)
        try:
            print(between(Space(world, tables.Brief(world.schema)), sys.argv[2], sys.argv[4]))
        except ValueError as e:
            print(f"ERROR: {e}")
            return 1
        return 0
    if sys.argv[1:2] == ["section"]:
        ap = argparse.ArgumentParser(prog="space.py section", description="the setting seen from the side, as an SVG")
        ap.add_argument("--out", type=Path, help="the file to write; printed where unstated")
        ap.add_argument("--along", choices=["x", "y"], help="the plan axis drawn across; the wider where unstated")
        ap.add_argument("--heights", type=float, default=3.0, help="how many times as tall heights are drawn")
        a = ap.parse_args(sys.argv[2:])
        world = maps.world_for(tables.SETTING)
        svg = section(Space(world, tables.Brief(world.schema)), a.along, a.heights)
        if a.out:
            a.out.write_text(svg)
        else:
            print(svg)
        return 0
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("settle", nargs="?", choices=["settle"], help="write each place a thing states too few axes of, where it is derived")
    ap.add_argument("region", nargs="?", help="with settle, that region alone")
    ap.add_argument("--only", metavar="REGION", help="one region's rows, and the problems touching it")
    args = ap.parse_args()
    if args.settle:
        wrote = settle(args.region)
        print("\n".join(wrote) if wrote else "every region is placed already, or cannot be yet")
        return 0
    world = maps.world_for(tables.SETTING)
    space = Space(world, tables.Brief(world.schema))
    rows = space.rows(args.only)
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]) - 1)]
    for r in rows:
        print("  ".join(c.ljust(w) for c, w in zip(r, widths)) + "  " + r[-1])
    problems = [p for p in space.problems if not args.only or args.only in p[3]]
    print()
    for level, file, msg, _ in problems:
        print(f"{level.upper()}: {file.relative_to(tables.SETTING.parent) if file else ''}: {msg}")
    things = [t for t in space.things.values() if not args.only or t.region == args.only]
    full = sum(None not in space.absolute(t) for t in things)
    errors = sum(p[0] == "error" for p in problems)
    print(f"\n{len(things)} things, {full} placed in full in the setting; "
          f"{errors} error(s), {len(problems) - errors} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
