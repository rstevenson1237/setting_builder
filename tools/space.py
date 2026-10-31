#!/usr/bin/env python3
"""Every region, block and location at a point in one space, and what does not fit: the dry fire.

  python3 tools/space.py [--only REGION]

x runs east, y north and z up, in feet, from the origin region's way in at its ground: BRIEF.md's
`origin`, else the first region in the gazetteer. Each thing stands at a place in its parent's
frame - a region in the setting's, a block in its region's, a location in its block's, or its
region's where it is in none - and its absolute place adds its ancestors'. Plan (x and y) and
height (z) are known apart: a room not yet packed stands on its block's floor at no known point.

A region's origin is its way in, a DANGEROUS region's its first block's centre; a block's is its
centre, and a SAFE or WILD block lies at its region's origin; a location's is its centre. A
region is placed from the origin through a sheet it shares with a placed region, or a join to
one: a way's climb places it in height, its bearing and distance in plan, and a climbing way
between two DANGEROUS blocks sets one block's centre over the other's.

Prints each thing's place in its parent and in the setting, its outline and its floor and roof,
then each problem; exits 1 on an error.
"""
from __future__ import annotations

import argparse
import functools
import math
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
PLAN, HEIGHT = (0, 1), (2,)


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


def outline_of(dress: kdl.Node | None) -> tuple | None:
    """A location's outline: its own, else its width and length, a circle where it is round."""
    p = dress.props if dress is not None else {}
    if "outline" in p:
        return outline_value(p["outline"])
    if "width" not in p or "length" not in p:
        return None
    w, l = float(p["width"]), float(p["length"])
    return ("circle", w / 2) if str(p.get("shape")) == "round" else ("rect", w, l)


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


FORMS = (("way in", ("at",)), ("bearing and distance", ("bearing", "distance")), ("xyz", ("xyz",)))


def forms(node: kdl.Node) -> list[str]:
    """The ways a SAFE or WILD location or stop states its place."""
    p = node.props
    return [f for f, keys in FORMS if any(k in p for k in keys) and (f != "way in" or str(p["at"]) == "way in")]


def own(node: kdl.Node) -> list | None:
    """A SAFE or WILD location's or stop's place from its block's origin, z None where it stands
    on its ground; None where it states no one place."""
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


def offset(region, node: kdl.Node) -> tuple[float, float] | None:
    """A SAFE or WILD location's or stop's (east, north) in feet from its region's way in, or None
    where it states no place."""
    if (o := own(node)) is None:
        return None
    if node.name == "Location":
        code = str(node.args[0])
        for block in maps.blocks_of(region).values():
            if code in [m.strip() for m in str(block.props.get("locations", "")).split(",")]:
                if (b := point_of(block.props.get("xyz"))):
                    return o[0] + b[0], o[1] + b[1]
    return o[0], o[1]


def centre(d: kdl.Node | None) -> tuple[float, float] | None:
    """A DANGEROUS room's centre (east, north) from its block's, where its Dressing places it."""
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
        self._place_blocks()
        self._place_regions()
        self._check()

    def say(self, level: str, file: Path | None, msg: str, *codes: str):
        self.problems.append((level, file, msg, {c.split(".")[0] for c in codes}))

    # -- the tree, and each thing's place in its parent ---------------------------------

    def _build(self):
        self.origin = self.brief.origin or next(iter(self.world.regions), None)
        rows = sc.read_tables(tables.SETTING / "Sheets.md")[0].dicts() if (tables.SETTING / "Sheets.md").exists() else []
        self.squares = {n: maps.Sheet(n, node).square for n, node in self.brief.sheets.items()}
        self.on = {}                                    # region -> {sheet: (column, row)}
        for d in rows:
            self.on.setdefault(d["Region"], {})[d["Sheet"]] = tuple(float(v) for v in d["Way in"].split(","))
        gazetteer = {str(n.args[0]): n for n in tables.gazetteer() if n.args}
        for code, region in self.world.regions.items():
            g = gazetteer.get(code)
            r = self.things[code] = Thing(code, "region", code, None, file=tables.GAZETTEER, line=g.line if g else 0)
            self._shape(r, g)
            if code == self.origin:
                if g is not None and "xyz" in g.props and point_of(g.props["xyz"])[:2] != [0, 0]:
                    self.say("error", r.file, f"line {r.line}: {code} is BRIEF.md's origin, so its place is 0,0,0", code)
                r.at, r.by = [0.0, 0.0, 0.0], "origin"
            elif g is not None and (c := point_of(g.props.get("xyz"))):
                r.at, r.by = [c[0], c[1], c[2] or 0.0], "xyz"
            danger = region.rating.upper() == "DANGEROUS"
            dress = {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
            ground = {str(n.args[0]): n for n in region.files.get("Ground", []) if n.name == "At" and n.args}
            way_in = next((c for c, n in region.locations().items() if str(n.props.get("at")) == "way in"), None)
            home = {}
            for i, (bid, block) in enumerate(maps.blocks_of(region).items()):
                b = self.things[bid] = Thing(bid, "block", code, r, file=region.dir / "Blocks.md", line=block.line)
                self._shape(b, block)
                c = point_of(block.props.get("xyz"))
                if danger and i == 0:
                    if c:
                        self.say("error", b.file, f"line {b.line}: {bid} is its region's first block, whose centre "
                                                  f"is the region's origin: it states no xyz", bid)
                    b.at, b.by = [0.0, 0.0, 0.0], "first block"
                elif c:
                    b.at, b.by = [c[0], c[1], c[2] or 0.0], "xyz"
                elif not danger:
                    b.at, b.by = [0.0, 0.0, 0.0], "region's way in"
                for m in str(block.props.get("locations", "")).split(","):
                    home[m.strip()] = b
            conditions = region.seed("Conditions")
            for loc, node in region.locations().items():
                d = dress.get(loc)
                t = self.things[loc] = Thing(loc, "location", code, home.get(loc, r))
                if danger:
                    t.file, t.line = region.dir / "Dressing.md", d.line if d is not None else 0
                    p = d.props if d is not None else {}
                    t.height = float(p.get("height", conditions.props.get("height", 0) if conditions else 0))
                    c = point_of(p.get("xyz"))
                    t.at = [c[0], c[1], c[2] or 0.0] if c else [None, None, 0.0]
                    t.by = "xyz" if c else ""
                else:
                    t.file, t.line = region.dir / "Locations.md", node.line
                    self._own(t, node)
                    if t.at[2] is None and loc in ground and way_in in ground:
                        t.at[2] = float(ground[loc].props["height"]) - float(ground[way_in].props["height"])
                self._shape(t, d, of_location=True)
            for b in (self.things[bid] for bid in maps.blocks_of(region)) if danger else ():
                b.height = max((t.at[2] + t.height for t in self.things.values() if t.parent is b), default=0.0)
            for i, n in enumerate(region.files.get("Stops", [])):
                if n.args:
                    s = self.things[f"{n.args[0]}/{i + 1}"] = Thing(f"{n.args[0]}/{i + 1}", "stop", code, r,
                                                                    file=region.dir / "Stops.md", line=n.line)
                    self._own(s, n)

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

    def _own(self, t: Thing, node: kdl.Node):
        """A SAFE or WILD location's or stop's place in its parent, by the one form it states."""
        got = forms(node)
        if len(got) > 1:
            self.say("error", t.file, f"line {t.line}: {t.code} is placed by {' and by '.join(got)}: state one", t.code)
        elif got and (o := own(node)) is not None:
            t.at, t.by = o, got[0]
        elif got:
            self.say("error", t.file, f"line {t.line}: {t.code} states a bearing or a distance without the other", t.code)
        else:
            self.say("error", t.file, f'line {t.line}: {t.code} states no place: bearing and distance, xyz, or at="way in" '
                                      f"(step 3d)", t.code)

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

    def _place_blocks(self):
        """A DANGEROUS region's later blocks, each over or under the block a climbing way joins it to."""
        changed = True
        while changed:
            changed = False
            for region, n in self.joins:
                if not self.stair(region, n) or not (e := self.ends(region, n)) or e[0].region != e[1].region:
                    continue
                for near, far, rise in ((e[0], e[1], self.climbs(n)), (e[1], e[0], -self.climbs(n))):
                    nb, fb = near.parent, far.parent
                    if nb is not fb and nb.at[0] is None and fb.at[0] is not None:
                        nb.at = [fb.at[0], fb.at[1], fb.at[2] + far.at[2] + rise - near.at[2]]
                        nb.by, changed = f"over or under {fb.code}, from {n.args[0]} to {n.props['to']}", True

    def _place_regions(self):
        """Each region's place from the origin, in plan and in height apart, by the first sheet or
        join reaching a placed region, in gazetteer and file order."""
        regions = [self.things[c] for c in self.world.regions]
        changed = True
        while changed:
            changed = False
            for r in regions:
                for q in regions:
                    if q is not r and (sheet := self.shared(r, q)):
                        changed |= self._from_sheet(r, q, sheet)
            for region, n in self.joins:
                if (e := self.ends(region, n)) and e[0].region != e[1].region:
                    changed |= self._from_join(region, n, *e) | self._from_join(region, n, *e, back=True)

    def shared(self, r: Thing, q: Thing) -> str | None:
        both = set(self.on.get(r.code, {})) & set(self.on.get(q.code, {}))
        return min(both, key=lambda s: self.squares[s]) if both else None

    def _from_sheet(self, r: Thing, q: Thing, sheet: str) -> bool:
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

    # -- what does not fit --------------------------------------------------------------

    def span(self, t: Thing, at: list) -> tuple[float, float] | None:
        return None if at[2] is None else (at[2], at[2] + t.height)

    def _check(self):
        things = list(self.things.values())
        for region in self.world.regions.values():
            r = self.things[region.code]
            for axes, name in ((PLAN, "plan"), (HEIGHT, "height")):
                if r.at[axes[0]] is None:
                    self.say("warning", r.file, f"{r.code} has no place in {name}: no sheet or join reaches it from a "
                                                f"placed region (step 4a)", r.code)
            for bid in maps.blocks_of(region):
                if self.things[bid].at[0] is None:
                    self.say("warning", self.things[bid].file, f"{bid} has no place: it states no xyz, and no climbing "
                                                               f"way joins it to a placed block (step 4a)", bid)
        self._overlaps([t for t in things if t.kind == "location"])
        self._overlaps([t for t in things if t.kind == "block"])
        self._overlaps([t for t in things if t.kind == "region"])
        self._outside(things)
        self._ways()
        self._sheets()

    def _overlaps(self, group: list[Thing]):
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                if a.kind == "block" and a.region != b.region:
                    continue
                pa, pb = self.frame(a, b) if a.kind != "region" else (a.at, b.at)
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
        for i, r in enumerate(regions):
            for q in regions[i + 1:]:
                if (sheet := self.shared(r, q)) and None not in r.at[:2] + q.at[:2]:
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
            out.append([t.code, t.kind, t.parent.code if t.parent else "setting", point(t.at), point(ab), said(t.outline),
                        "?" if ab[2] is None else f"{fmt(ab[2])}..{fmt(ab[2] + t.height)}", t.by or "-"])
        return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", metavar="REGION", help="one region's rows, and the problems touching it")
    args = ap.parse_args()
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
