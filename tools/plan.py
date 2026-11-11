#!/usr/bin/env python3
"""Block plans: a block laid out from what its design states - its layouts, its rooms and the routes between them.

  python3 tools/plan.py solve CODE [BLOCK] [--out DIR] [--seeds N]    # a region's planned blocks, from Design.md
  python3 tools/plan.py solve --file PLAN.md [BLOCK] [--out DIR]     # any file of plan lines, for trying one out
  python3 tools/plan.py accept CODE BLOCK                            # write the solved places and ways into Design.md
  --free: a region's stair rooms are not held over the rooms they meet, for the first level of a chain

A plan is a block's `Design` line with `Layout`, `Room` and `Route` lines in place of a layout engine's `Use` and
`Bind` (`patterns/Region_Schema.md`; how to write one: the `block-plan` skill). Every size and place is in feet,
x east and y north of the parent's centre; the solver works on the map's 10 ft squares. Every place, facing, side
and length is a goal, never a rule: the solver tries `--seeds` orders of placing, routes every way in each, and keeps
the one that routes most and misses fewest goals, then reports each goal it missed. A plan that still leaves a
way unrouted relaxes its goals in turn - sides, facings, then lengths - then lets passages cross, then grows the
block, and says which it did.
"""
from __future__ import annotations

import argparse
import heapq
import json
import math
import random
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kdl                      # noqa: E402

SQ = 10                         # feet to a square: the lattice rooms stand on and passages run along
CELL = 5                        # feet to an artgen cell
K = SQ // CELL                  # cells to a square
EDGE = 1                        # squares of rock round the block on the map
ROOM = 20                       # feet: a room's side where it states none
FACING = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
SIDES = {"north": "we", "south": "we", "east": "ns", "west": "ns"}
ARRANGE = ("cluster", "row", "column", "grid", "spine", "ring")
SHAPES = {"rect": "rect", "hall": "rect", "round": "circle", "octagon": "octagon", "cave": "cave", "diamond": "poly",
          "hexagon": "hexagon"}
CORNERED = ("round", "octagon", "diamond", "hexagon")   # shapes whose box corners are rock: doors only near a side's middle
DIAGONAL = {"north-east": "ne", "south-east": "se", "south-west": "sw", "north-west": "nw"}
DOORS = ("door", "secret", "locked", "portcullis", "arch", "double", "open", "none")
CODE_RE = re.compile(r"[A-Z]{1,2}\.\d+")
BLOCK_RE = re.compile(r"[A-Z]{1,2}\.[a-z]")
FEET_RE = re.compile(r"(-?\d+(?:\.\d+)?)(?: feet)?")
EXAMPLES = Path(__file__).resolve().parent.parent / ".claude" / "skills" / "block-plan" / "examples"


def feet(v, default=None) -> float | None:
    if v is None:
        return default
    m = FEET_RE.fullmatch(str(v).strip())
    return float(m[1]) if m else default


def squares(v: float) -> int:
    return max(1, math.ceil(v / SQ - 1e-9))


def point(v) -> tuple[float, float] | None:
    if v is None:
        return None
    try:
        c = [float(x) for x in str(v).split(",")]
    except ValueError:
        return None
    return (c[0], c[1]) if len(c) >= 2 else None


def words(v) -> list[str]:
    return [w.strip() for w in str(v or "").split(",") if w.strip()]


# -- what a plan states ------------------------------------------------------------------

@dataclass
class Room:
    key: str                    # its code, or a made-up id for a room no location holds
    named: bool
    w: int                      # squares
    h: int
    shape: str = "rect"
    layout: str | None = None
    origin: tuple | None = None # feet from its parent's centre, x east, y north
    facing: str | None = None
    side: str | None = None
    label: str | None = None
    line: int = 0
    at: tuple | None = None     # (i, j): its box's top-left square in the block, once placed


@dataclass
class Layout:
    id: str
    arrange: str = "cluster"
    gap: int = 0                # squares between its rooms
    origin: tuple | None = None
    facing: str | None = None
    side: str | None = None
    entry: str | None = None
    links: str = "auto"
    cols: int | None = None
    align: str = "centre"
    door: str = "door"
    rooms: list = field(default_factory=list)
    line: int = 0
    diagonal: set = field(default_factory=set)   # (hub, room): a straight diagonal passage, not one on the lattice


@dataclass
class End:
    target: str
    facing: str | None = None
    side: str | None = None


@dataclass
class Route:
    ends: list
    length: str = "short"       # short, long, or a count of squares
    kind: str = "passage"       # passage, or door: through a shared wall where the rooms touch
    doors: list = field(default_factory=list)
    width: float = SQ
    stair: str | None = None    # up or down: a way out of the block drawn as a stair in its room
    label: str | None = None
    line: int = 0
    inner: bool = False         # one of a layout's own ways


class Plan:
    """One block's plan: its outline on the lattice, its rooms and layouts, its routes, and what is wrong with it."""

    def __init__(self, bid: str, lines: list[kdl.Node], others: dict[str, tuple] | None = None, pins: dict | None = None):
        self.bid, self.problems, self.others = bid, [], others or {}
        self.pins = pins or {}                  # a stair's room: (east, north) of the block's centre it stands over
        heads = [n for n in lines if n.name == "Design" and n.args]
        head = next((n for n in heads if str(n.args[0]) == bid), None)
        if head is None:
            raise ValueError(f"no Design line for {bid}")
        ids = {str(n.props.get("id")) for n in lines if n.name == "Layout" and n.args and str(n.args[0]) == bid}
        held = set(words(head.props.get("locations")))
        elsewhere = {c for n in heads if n is not head for c in words(n.props.get("locations"))}
        mine = [n for n in lines if n.args and (str(n.args[0]) == bid or n.name == "Room" and (
            str(n.args[0]) in held or str(n.props.get("layout")) in ids or
            len(heads) == 1 and CODE_RE.fullmatch(str(n.args[0])) and str(n.args[0]) not in elsewhere) or
            n.name == "Route" and any(e.split(":")[0].strip() in held | ids | {bid} for e in words(n.props.get("ends"))))]
        self.head = head
        p = head.props
        self.locations = words(p.get("locations"))
        self.fill = self.fill_of(p.get("fill"))
        self.facing, self.side = p.get("facing"), p.get("side")
        self.width = feet(p.get("width"), SQ)
        self.pad = int(feet(p.get("pad"), 0) // SQ) if p.get("pad") is not None else (1 if self.fill[1] >= .4 else 2)
        self.xyz = [float(c) for c in str(p.get("xyz", "0,0,0")).split(",")] + [0.0] * 3
        self.layouts: dict[str, Layout] = {}
        self.rooms: dict[str, Room] = {}
        self.routes: list[Route] = []
        made = 0
        for n in mine:
            q = n.props
            if n.name == "Layout":
                lay = Layout(str(q.get("id")), str(q.get("arrange", "cluster")), int(feet(q.get("gap"), 0) // SQ),
                             point(q.get("xyz")), q.get("facing"), q.get("side"), q.get("entry"),
                             str(q.get("links", "auto")), int(q["cols"]) if q.get("cols") else None,
                             str(q.get("align", "centre")), str(q.get("door", "door")), line=n.line)
                if lay.arrange not in ARRANGE:
                    self.say(n, f"arrange {lay.arrange} is not one of {', '.join(ARRANGE)}")
                    lay.arrange = "cluster"
                if lay.id in self.layouts or CODE_RE.fullmatch(lay.id) or BLOCK_RE.fullmatch(lay.id):
                    self.say(n, f"layout id {lay.id!r} is taken or reads as a location or block")
                self.layouts[lay.id] = lay
        for n in mine:
            q = n.props
            if n.name != "Room":
                continue
            code = str(n.args[0])
            shape = str(q.get("shape", "rect"))
            if shape not in SHAPES:
                self.say(n, f"shape {shape} is not one of {', '.join(SHAPES)}")
                shape = "rect"
            w, h = feet(q.get("width"), ROOM), feet(q.get("length"), ROOM)
            if (w % SQ or h % SQ) and code != bid:
                self.say(n, f"{w:g} by {h:g} ft is drawn {squares(w) * SQ} by {squares(h) * SQ}: rooms stand on {SQ} ft squares")
            layout = q.get("layout")
            if layout is not None and layout not in self.layouts:
                self.say(n, f"layout {layout!r} is no Layout of {bid}")
                layout = None
            count = int(q.get("count", 1)) if code == bid else 1
            for _ in range(count):
                if code == bid:
                    made += 1
                    key, named = f"{bid}-{made}", False
                else:
                    key, named = code, True
                    if key in self.rooms:
                        self.say(n, f"{key} has two Room lines")
                        continue
                r = Room(key, named, squares(w), squares(h), shape, layout, point(q.get("xyz")),
                         DIAGONAL.get(str(q.get("facing")), q.get("facing")),
                         q.get("side"), q.get("label"), n.line)
                self.rooms[key] = r
                if layout:
                    self.layouts[layout].rooms.append(r)
        for c in self.locations:
            if c not in self.rooms:
                self.problems.append(f"{c} has no Room line: drawn {ROOM} ft square, placed where it routes best")
                self.rooms[c] = Room(c, True, squares(ROOM), squares(ROOM))
        for c, r in self.rooms.items():
            if r.named and self.locations and c not in self.locations:
                self.problems.append(f"{c} has a Room line but is not one of the Design's locations")
        for n in mine:
            if n.name == "Route":
                self.routes.append(self.route(n))
        for lay in self.layouts.values():
            if not lay.rooms:
                self.problems.append(f"layout {lay.id} holds no rooms")
        self.layouts = {k: v for k, v in self.layouts.items() if v.rooms}
        self.voids = [n for n in mine if n.name == "Void"]
        self.outline = self.outline_of(p.get("outline"))

    def say(self, n: kdl.Node, msg: str):
        self.problems.append(f"line {n.line}: {msg}")

    @staticmethod
    def fill_of(v) -> tuple[float, float]:
        m = re.fullmatch(r"(\d+)(?:-(\d+))?%", str(v or "45-60%"))
        if not m:
            return .45, .6
        lo = int(m[1]) / 100
        return lo, int(m[2] or m[1]) / 100

    def route(self, n: kdl.Node) -> Route:
        q = n.props
        ends = []
        for raw in words(q.get("ends")):
            bits = [b.strip() for b in raw.split(":")]
            e = End(bits[0], bits[1] if len(bits) > 1 and bits[1] else None, bits[2] if len(bits) > 2 else None)
            if e.facing and e.facing not in FACING:
                self.say(n, f"{raw}: facing is north, south, east or west")
                e.facing = None
            if e.side and (not e.facing or e.side not in SIDES[e.facing]):
                self.say(n, f"{raw}: side is {' or '.join(SIDES.get(e.facing, 'nswe'))} for facing {e.facing}")
                e.side = None
            ends.append(e)
        if len(ends) < 2:
            self.say(n, "a Route has two or more ends")
        length = str(q.get("length", "short"))
        if length not in ("short", "long"):
            f = feet(length)
            if f is None:
                self.say(n, f"length {length!r} is short, long, a count of {SQ} ft squares or \"N feet\"")
                length = "short"
            else:
                length = str(max(1, round(f / SQ)) if "feet" in length else int(f))
        doors = words(q.get("door", "door"))
        for d in doors:
            if d not in DOORS:
                self.say(n, f"door {d} is not one of {', '.join(DOORS)}")
        width = feet(q.get("width"), self.width)
        if width > SQ:
            self.say(n, f"a route is at most {SQ} ft wide; a wider way is a room (shape hall)")
            width = SQ
        kind = str(q.get("kind", "passage"))
        if kind not in ("passage", "door"):
            self.say(n, "kind is passage or door")
            kind = "passage"
        return Route(ends, length, kind, [None if d == "none" else d for d in doors], width,
                     q.get("stair"), q.get("label"), n.line)

    def outline_of(self, v) -> list[tuple[float, float]]:
        """The block's outline in feet from its centre, x east, y north; grown round its rooms where it states none."""
        bits = str(v or "").split()
        if bits and bits[0] == "rect" and len(bits) == 3:
            w, h = float(bits[1]), float(bits[2])
            return [(-w / 2, h / 2), (w / 2, h / 2), (w / 2, -h / 2), (-w / 2, -h / 2)]
        if bits and bits[0] == "circle" and len(bits) == 2:
            r = float(bits[1])
            return [(r * math.cos(math.pi * i / 12), r * math.sin(math.pi * i / 12)) for i in range(24)]
        if bits and bits[0] == "poly":
            return [tuple(float(c) for c in b.split(",")) for b in bits[1:]]
        if v is not None:
            self.problems.append(f"outline {v!r} is \"rect W H\", \"circle R\" or \"poly x,y …\"")
        area = sum(r.w * r.h for r in self.rooms.values()) * SQ * SQ
        side = math.ceil(math.sqrt(area / max(.1, sum(self.fill) / 2)) / (2 * SQ)) * 2 * SQ
        side = max(side, max((max(r.w, r.h) for r in self.rooms.values()), default=2) * SQ + 2 * SQ)
        self.problems.append(f"no outline: grown to rect {side:g} {side:g} for a fill of {self.fill[0]:.0%}-{self.fill[1]:.0%}")
        return [(-side / 2, side / 2), (side / 2, side / 2), (side / 2, -side / 2), (-side / 2, -side / 2)]


# -- a layout's rooms against one another --------------------------------------------------

def arrange(lay: Layout) -> tuple[dict[str, tuple[int, int]], list[tuple[str, str]], list[str]]:
    """Each room's top-left in the layout's own frame (squares, y south), the ways between its rooms, and what
    the arrangement could not do."""
    rs, g, notes = lay.rooms, lay.gap, []
    at: dict[str, tuple[int, int]] = {}
    links: list[tuple[str, str]] = []
    if lay.arrange in ("row", "column"):
        across = max((r.h if lay.arrange == "row" else r.w) for r in rs)
        run = 0
        for k, r in enumerate(rs):
            size = r.h if lay.arrange == "row" else r.w
            off = {"centre": (across - size) // 2, "n": 0, "w": 0, "s": across - size, "e": across - size}.get(lay.align, 0)
            at[r.key] = (run, off) if lay.arrange == "row" else (off, run)
            nxt = rs[k + 1] if k + 1 < len(rs) else None   # a round room shares no wall: a passage's room is left
            run += (r.w if lay.arrange == "row" else r.h) + (max(g, 1) if nxt and "round" in (r.shape, nxt.shape) else g)
        links = [(a.key, b.key) for a, b in zip(rs, rs[1:])]
    elif lay.arrange == "grid":
        cols = lay.cols or math.ceil(math.sqrt(len(rs)))
        cw, ch = max(r.w for r in rs), max(r.h for r in rs)
        for k, r in enumerate(rs):
            c, w = k % cols, k // cols
            at[r.key] = (c * (cw + g) + (cw - r.w) // 2, w * (ch + g) + (ch - r.h) // 2)
            if c:
                links.append((rs[k - 1].key, r.key))
            elif w:
                links.append((rs[k - cols].key, r.key))
    elif lay.arrange == "spine":
        hall = next((r for r in rs if r.key == lay.entry), rs[0])
        long_x = hall.w >= hall.h
        a_side, b_side = ("north", "south") if long_x else ("west", "east")
        sides = {a_side: [], b_side: []}
        flip = 0
        for r in rs:
            if r is hall:
                continue
            if r.facing in sides:
                sides[r.facing].append(r)
            else:
                sides[(a_side, b_side)[flip]].append(r)
                flip ^= 1
        runs = {s: sum((r.w if long_x else r.h) for r in v) + g * max(0, len(v) - 1) for s, v in sides.items()}
        span = hall.w if long_x else hall.h
        if max(runs.values()) > span:
            notes.append(f"layout {lay.id}: hall {hall.key} grown from {span * SQ} to {max(runs.values()) * SQ} ft to hold its rooms")
            span = max(runs.values())
            if long_x:
                hall.w = span
            else:
                hall.h = span
        deep = {s: max(((r.h if long_x else r.w) for r in v), default=0) for s, v in sides.items()}
        base = deep[a_side] + g          # the hall's near edge, squares from the layout's top or left
        at[hall.key] = (0, base) if long_x else (base, 0)
        for s, v in sides.items():
            run = (span - runs[s]) // 2
            for r in v:
                d = r.h if long_x else r.w
                near = base - g - d if s == a_side else base + (hall.h if long_x else hall.w) + g
                at[r.key] = (run, near) if long_x else (near, run)
                run += (r.w if long_x else r.h) + g
                links.append((hall.key, r.key))
    elif lay.arrange == "ring":
        hub = next((r for r in rs if r.key == lay.entry), rs[0])
        order = ["north", "south", "east", "west", "ne", "sw", "se", "nw"]
        taken: dict[str, int] = {}
        at[hub.key] = (0, 0)
        free = [o for o in order]
        for r in rs:
            if r is hub:
                continue
            want = r.facing if r.facing in order else None
            way = want or (free.pop(0) if free else order[len(taken) % 8])
            if want in free:
                free.remove(want)
            push = taken.get(way, 0)
            gap = max(g, 1) if lay.links != "wall" else 0
            vx = 1 if "e" in way[-1:] or way == "east" else -1 if way == "west" or way[-1:] == "w" else 0
            vy = -1 if way.startswith("n") else 1 if way.startswith("s") else 0
            if way in ("east", "west"):
                vy = 0
            x = {1: hub.w + gap + push, -1: -gap - r.w - push, 0: (hub.w - r.w) // 2}[vx]
            y = {1: hub.h + gap + push, -1: -gap - r.h - push, 0: (hub.h - r.h) // 2}[vy]
            if vx and vy and hub.shape in CORNERED and r.shape in CORNERED:
                x = hub.w + gap + push if vx > 0 else -gap - r.w - push      # corner to corner on the diagonal
                y = hub.h + gap + push if vy > 0 else -gap - r.h - push
                lay.diagonal.add((hub.key, r.key))
            taken[way] = push + (r.w if vx else r.h) + gap
            at[r.key] = (x, y)
            links.append((hub.key, r.key))
    else:                                               # cluster: each room set against one already placed
        first = rs[0]
        at[first.key] = (0, 0)
        for r in rs[1:]:
            best = None
            for o in rs:
                if o.key not in at or o is r:
                    continue
                ox, oy = at[o.key]
                spots = [(ox + o.w + g, oy + (o.h - r.h) // 2, "east"), (ox - g - r.w, oy + (o.h - r.h) // 2, "west"),
                         (ox + (o.w - r.w) // 2, oy - g - r.h, "north"), (ox + (o.w - r.w) // 2, oy + o.h + g, "south")]
                for x, y, way in spots:
                    if any(x < at[k][0] + rr.w and at[k][0] < x + r.w and y < at[k][1] + rr.h and at[k][1] < y + r.h
                           for k, rr in ((k, lay_room(rs, k)) for k in at)):
                        continue
                    xs = [at[k][0] for k in at] + [x]
                    ys = [at[k][1] for k in at] + [y]
                    xe = [at[k][0] + lay_room(rs, k).w for k in at] + [x + r.w]
                    ye = [at[k][1] + lay_room(rs, k).h for k in at] + [y + r.h]
                    cost = (max(xe) - min(xs)) * (max(ye) - min(ys)) + (0 if r.facing in (None, way) else 1000)
                    if best is None or cost < best[0]:
                        best = (cost, x, y, o.key)
            if best is None:
                notes.append(f"layout {lay.id}: {r.key} found no place against its rooms")
                continue
            at[r.key] = best[1:3]
            links.append((best[3], r.key))
    for r in rs:                                        # a room's own place in the layout overrides the arrangement
        if r.origin is not None and r.key in at:
            xs = [at[k][0] for k in at]
            ys = [at[k][1] for k in at]
            xe = [at[k][0] + lay_room(rs, k).w for k in at]
            ye = [at[k][1] + lay_room(rs, k).h for k in at]
            cx, cy = (min(xs) + max(xe)) / 2, (min(ys) + max(ye)) / 2
            at[r.key] = (round(cx + r.origin[0] / SQ - r.w / 2), round(cy - r.origin[1] / SQ - r.h / 2))
    if lay.links == "none":
        named = {r.key for r in rs if r.named}
        links = [(a, b) for a, b in links if not (a in named and b in named)]
    lo = (min(v[0] for v in at.values()), min(v[1] for v in at.values()))
    return {k: (v[0] - lo[0], v[1] - lo[1]) for k, v in at.items()}, links, notes


def lay_room(rs, key):
    return next(r for r in rs if r.key == key)


# -- the block on the lattice ---------------------------------------------------------------

def inside(poly, x, y) -> bool:
    hit = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


@dataclass
class Item:
    key: str
    w: int
    h: int
    rooms: dict                 # room key -> (dx, dy) in the item
    origin: tuple | None = None
    facing: str | None = None
    side: str | None = None
    at: tuple | None = None


class Solver:
    """One attempt at a plan: its items placed by one seed's order, then every route run on the lattice."""

    def __init__(self, plan: Plan, seed: int, relax: set[str]):
        self.plan, self.seed, self.relax = plan, seed, relax
        self.rng = random.Random(seed)
        self.notes: list[str] = []
        self.missed: list[str] = []
        xs, ys = [x for x, _ in plan.outline], [y for _, y in plan.outline]
        need = sum((r.w + plan.pad) * (r.h + plan.pad) for r in plan.rooms.values()) * SQ * SQ / max(.1, plan.fill[1])
        have = (max(xs) - min(xs)) * (max(ys) - min(ys))
        grow = max(1.25, math.sqrt(need / have)) if "grow" in relax else 1.0   # a quarter, or what the rooms need
        self.gw = math.ceil((max(xs) - min(xs)) * grow / SQ)
        self.gh = math.ceil((max(ys) - min(ys)) * grow / SQ)
        self.ox, self.oy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2   # the outline's centre, feet
        cx, cy = self.gw / 2, self.gh / 2
        self.poly = [(x * grow, y * grow) for x, y in plan.outline]
        self.cell_in = [[inside(self.poly,
                                (i + .5 - cx) * SQ + self.ox, (cy - j - .5) * SQ + self.oy)
                         for j in range(self.gh)] for i in range(self.gw)]
        for v in plan.voids:
            o = point(v.props.get("xyz")) or (0.0, 0.0)
            bits = str(v.props.get("outline", "")).split()
            if len(bits) == 3 and bits[0] == "rect":
                w, h = float(bits[1]), float(bits[2])
                for i in range(self.gw):
                    for j in range(self.gh):
                        x, y = (i + .5 - cx) * SQ, (cy - j - .5) * SQ
                        if abs(x - o[0]) < w / 2 and abs(y - o[1]) < h / 2:
                            self.cell_in[i][j] = False
        self.owner: dict[tuple[int, int], tuple[str, str]] = {}
        self.links: list[tuple[str, str, str]] = []      # (a, b, door) through a shared wall
        self.corridors: list[dict] = []
        self.failed: list[str] = []
        self.length_error = 0
        self.crossed = 0

    # -- placing ------------------------------------------------------------------

    def ok(self, i, j) -> bool:
        return 0 <= i < self.gw and 0 <= j < self.gh and self.cell_in[i][j]

    def items(self) -> list[Item]:
        p, out, self.inner = self.plan, [], []
        for lay in p.layouts.values():
            at, links, notes = arrange(lay)
            self.notes += notes
            w = max(at[r.key][0] + r.w for r in lay.rooms)
            h = max(at[r.key][1] + r.h for r in lay.rooms)
            origin = lay.origin
            held = next((r for r in lay.rooms if r.key in p.pins), None)
            if origin is None and held:                 # a stair's room over the room it meets: the layout moves with it
                e, n = p.pins[held.key]
                origin = (e - (at[held.key][0] + held.w / 2 - w / 2) * SQ, n + (at[held.key][1] + held.h / 2 - h / 2) * SQ)
            out.append(Item(lay.id, w, h, at, origin, lay.facing, lay.side))
            for a, b in links:
                kind = "diagonal" if (a, b) in lay.diagonal else "door" if lay.gap == 0 else "passage"
                self.inner.append(Route([End(a), End(b)], "short", kind, [lay.door], p.width, inner=True, line=lay.line))
        for r in p.rooms.values():
            if r.layout is None:
                out.append(Item(r.key, r.w, r.h, {r.key: (0, 0)}, r.origin or p.pins.get(r.key), r.facing, r.side))
        return out

    def place(self, items: list[Item], first: set = frozenset()) -> None:
        p = self.plan
        owner_of = {k: it.key for it in items for k in it.rooms}
        for lay in p.layouts.values():
            owner_of[lay.id] = lay.id
        self.owner_of = owner_of
        self.door_pairs = {frozenset(e.target for e in r.ends[:2]) for r in p.routes + self.inner
                           if r.kind == "door" and all(e.target in p.rooms for e in r.ends[:2])}
        ties: dict[str, list[tuple[str, Route]]] = {it.key: [] for it in items}
        for r in p.routes + self.inner:
            keys = [owner_of.get(e.target) for e in r.ends]
            for a in keys:
                for b in keys:
                    if a and b and a != b:
                        ties[a].append((b, r))
        fixed = [it for it in items if it.origin is not None]
        rest = [it for it in items if it.origin is None]
        self.rng.shuffle(rest)
        rest.sort(key=lambda it: (it.key not in first, it.facing is None and "facing" not in self.relax,
                                  -len(ties[it.key]) - it.w * it.h / 50))
        anchors = fixed + [x for x in rest if x.key in first] + \
            [x for x in rest if x.key not in first and x.facing and "facing" not in self.relax]
        order, seen = [], set()
        for it in anchors + rest:                       # anchors first, then outward along the ways from them
            if it.key in seen:
                continue
            queue = [it] if it not in anchors else [a for a in anchors if a.key not in seen]
            while queue:
                x = queue.pop(0)
                if x.key in seen:
                    continue
                seen.add(x.key)
                order.append(x)
                queue += [y for y in rest if y.key not in seen and any(b == y.key for b, _ in ties[x.key])]
        placed: list[Item] = []
        cx, cy = self.gw / 2, self.gh / 2
        f = sum(p.fill) / 2
        for it in order:
            best = None
            if it.origin is not None:
                i = round(cx + (it.origin[0] - self.ox) / SQ - it.w / 2)
                j = round(cy - (it.origin[1] - self.oy) / SQ - it.h / 2)
                cands = [(i, j)] + [(i + di, j + dj) for d in range(1, 6) for di in range(-d, d + 1)
                                    for dj in range(-d, d + 1) if max(abs(di), abs(dj)) == d]
            else:
                cands = [(i, j) for i in range(self.gw - it.w + 1) for j in range(self.gh - it.h + 1)]
            for i, j in cands:
                if not self.fits(it, i, j, placed, ties):
                    continue
                s = self.score(it, i, j, placed, ties, f)
                if it.origin is not None:
                    s += 50 * (abs(i - cands[0][0]) + abs(j - cands[0][1]))
                if best is None or s < best[0]:
                    best = (s, i, j)
                if it.origin is not None and best and best[0] < 1e8 and (i, j) == cands[0]:
                    break
            if best is None:
                self.unplaced.append(it.key)
                continue
            it.at = (best[1], best[2])
            if it.origin is not None and it.at != cands[0]:
                self.missed.append(f"{it.key} moved {SQ * (abs(it.at[0] - cands[0][0]) + abs(it.at[1] - cands[0][1]))} ft from its xyz")
            placed.append(it)
            for k, (dx, dy) in it.rooms.items():
                r = p.rooms[k]
                r.at = (it.at[0] + dx, it.at[1] + dy)
                for a in range(r.w):
                    for b in range(r.h):
                        self.owner[(r.at[0] + a, r.at[1] + b)] = ("room", k)
        self.placed = placed

    def fits(self, it: Item, i, j, placed, ties) -> bool:
        for k, (dx, dy) in it.rooms.items():
            r = self.plan.rooms[k]
            for a in range(r.w):
                for b in range(r.h):
                    if not self.ok(i + dx + a, j + dy + b):
                        return False
        for o in placed:
            joined = any(b == o.key and r.kind == "door" for b, r in ties[it.key])
            pad = 0 if joined else self.plan.pad
            if i < o.at[0] + o.w + pad and o.at[0] < i + it.w + pad and j < o.at[1] + o.h + pad and o.at[1] < j + it.h + pad:
                if not joined or self.overlaps(it, i, j, o, self.plan.pad):
                    return False
        return True

    def overlaps(self, it, i, j, o, pad=0) -> bool:
        """Any room of it at (i, j) on, or within pad of, a room of o it shares no door with."""
        for k, (dx, dy) in it.rooms.items():
            r = self.plan.rooms[k]
            for kk, (ex, ey) in o.rooms.items():
                q = self.plan.rooms[kk]
                g = 0 if frozenset((k, kk)) in self.door_pairs else pad
                if i + dx < o.at[0] + ex + q.w + g and o.at[0] + ex < i + dx + r.w + g and \
                        j + dy < o.at[1] + ey + q.h + g and o.at[1] + ey < j + dy + r.h + g:
                    if g or (i + dx < o.at[0] + ex + q.w and o.at[0] + ex < i + dx + r.w and
                             j + dy < o.at[1] + ey + q.h and o.at[1] + ey < j + dy + r.h):
                        return True
        return False

    def score(self, it: Item, i, j, placed, ties, f) -> float:
        s = 0.0
        byk = {o.key: o for o in placed}

        def box(item, at, ends):
            """The box of the room a route names in this item - or the whole item, where it names the layout."""
            k = next((e.target for e in ends if e.target in item.rooms), None)
            if k is None:
                return at[0], at[1], item.w, item.h, None
            dx, dy = item.rooms[k]
            r = self.plan.rooms[k]
            return at[0] + dx, at[1] + dy, r.w, r.h, k
        for b, r in ties[it.key]:
            o = byk.get(b)
            if o is None:
                continue
            ax, ay, aw, ah, ka = box(it, (i, j), r.ends)
            bx, by, bw, bh, kb = box(o, o.at, r.ends)
            dx = max(0, bx - (ax + aw), ax - (bx + bw))
            dy = max(0, by - (ay + ah), ay - (by + bh))
            d = dx + dy
            if r.kind == "door" and not d:              # touching where no door fits: a corner, a curve, a cut
                ox = min(ax + aw, bx + bw) - max(ax, bx)
                oy = min(ay + ah, by + bh) - max(ay, by)
                if ox < 1 and oy < 1:
                    d = 1
                elif ka and kb:
                    ra, rb = self.plan.rooms[ka], self.plan.rooms[kb]
                    keep = ra.at, rb.at
                    ra.at, rb.at = (ax, ay), (bx, by)
                    d = 0 if self.touching(ra, rb) else 1
                    ra.at, rb.at = keep
            for e in r.ends:                            # an end's facing: the far end lies that way from it
                if e.facing not in FACING or "facing" in self.relax:
                    continue
                me = self.owner_of.get(e.target)
                if me not in (it.key, o.key):
                    continue
                vx, vy = FACING[e.facing]
                ux = (ax + aw / 2) - (bx + bw / 2)
                uy = (ay + ah / 2) - (by + bh / 2)
                if me == it.key:
                    ux, uy = -ux, -uy
                along = ux * vx + uy * vy
                s += (10 if r.kind == "door" else 3) * max(0.0, (aw + bw) / 2 * abs(vx) + (ah + bh) / 2 * abs(vy) - along) \
                    + 0.5 * abs(ux * vy - uy * vx)
            if r.kind == "door":
                s += 6 * d
            elif r.length == "short" or "length" in self.relax:
                s += d
            elif r.length == "long":
                s -= 0.6 * d
            else:
                s += 1.5 * abs(d + 1 - int(r.length))
        fx = (i + it.w / 2) / self.gw
        fy = (j + it.h / 2) / self.gh
        hint = 4 * max(self.gw, self.gh)
        if it.facing in FACING and "facing" not in self.relax:
            s += hint * {"north": fy, "south": 1 - fy, "west": fx, "east": 1 - fx}[it.facing]
            if it.side and "side" not in self.relax:
                t = fx if it.facing in ("north", "south") else fy
                s += hint * max(0, {"w": t - .5, "e": .5 - t, "n": t - .5, "s": .5 - t}.get(it.side, 0))
        if self.tight:                                  # a block too full for its rooms: pack them to its walls
            s += 0.4 * min(i, j, self.gw - i - it.w, self.gh - j - it.h)
        else:
            s += (1 - f) * 0.4 * math.hypot(i + it.w / 2 - self.gw / 2, j + it.h / 2 - self.gh / 2)
        return s + self.rng.random() * 0.01

    # -- routing ------------------------------------------------------------------

    def resolve(self, e: End, other: tuple | None) -> tuple[str, list]:
        """An end's kind - room, layout, exit or stair - and the squares a passage may leave it from, each
        (door square, (wall point in cells), the wall's outward step)."""
        p = self.plan
        facing = e.facing if "facing" not in self.relax else None
        side = e.side if "side" not in self.relax else None
        if e.target in p.rooms:
            return "room", self.walls([p.rooms[e.target]], facing, side, e.target in p.rooms and not p.rooms[e.target].named)
        if e.target in p.layouts:
            lay = p.layouts[e.target]
            rs = [r for r in lay.rooms if r.key == lay.entry] if lay.entry and not facing else lay.rooms
            return "layout", self.walls(rs, facing, side, False, outer=facing is not None)
        out = []                                        # a way out of the block, at its edge: an end naming this block
        way = facing if e.target == p.bid else self.toward(e.target)   # faces its side; one naming another, that block's
        for i in range(self.gw):
            for j in range(self.gh):
                if not self.ok(i, j):
                    continue
                for f, (vx, vy) in FACING.items():
                    if way and f != way:
                        continue
                    if not self.ok(i + vx, j + vy):
                        out.append(((i, j), self.wall_point(i, j, vx, vy), (vx, vy), f))
        if way and out:
            if way in ("north", "south"):
                edge = min(o[0][1] for o in out) if way == "north" else max(o[0][1] for o in out)
                out = [o for o in out if o[0][1] == edge] or out
                xs = sorted(o[0][0] for o in out)
                if side:
                    mid = (xs[0] + xs[-1]) / 2
                    out = [o for o in out if (o[0][0] <= mid) == (side == "w")] or out
            else:
                edge = max(o[0][0] for o in out) if way == "east" else min(o[0][0] for o in out)
                out = [o for o in out if o[0][0] == edge] or out
                ys = sorted(o[0][1] for o in out)
                if side:
                    mid = (ys[0] + ys[-1]) / 2
                    out = [o for o in out if (o[0][1] <= mid) == (side == "n")] or out
        return "exit", [(o[0], o[1], o[2]) for o in out]

    def toward(self, target: str) -> str | None:
        """The side of the block facing another block of the plan or region, where its xyz is known."""
        far = self.plan.others.get(target)
        if far is None:
            return None
        dx, dy = far[0] - self.plan.xyz[0], far[1] - self.plan.xyz[1]
        if abs(dx) < 1 and abs(dy) < 1:
            return None
        return ("east" if dx > 0 else "west") if abs(dx) > abs(dy) else ("north" if dy > 0 else "south")

    def wall_point(self, i, j, vx, vy) -> tuple[float, float]:
        """The middle of square (i, j)'s wall on the side (vx, vy), in artgen cells."""
        x, y = (i + EDGE) * K + K / 2, (j + EDGE) * K + K / 2
        return x + vx * K / 2, y + vy * K / 2

    def walls(self, rooms: list[Room], facing, side, plain: bool, outer: bool = False) -> list:
        """Door squares round these rooms: outside a wall, on the facing wall where one is asked, and on the
        half of it the side asks; where none is free, the nearest the ask allows."""
        keys = {r.key for r in rooms}
        cand = []
        for r in rooms:
            i0, j0 = r.at
            for f, (vx, vy) in FACING.items():
                if f in ("north", "south"):
                    span = [(i0 + a, j0 - 1 if f == "north" else j0 + r.h) for a in range(r.w)]
                else:
                    span = [(i0 - 1 if f == "west" else i0 + r.w, j0 + b) for b in range(r.h)]
                if r.shape in CORNERED and len(span) > 2:   # off the cut corners, or the curve's ends
                    n = len(span)
                    cut = min(r.w, r.h) / (2 + math.sqrt(2)) if r.shape == "octagon" else n * (.3 if r.shape == "round" else .4)
                    span = [s for k, s in enumerate(span) if cut <= k + .5 <= n - cut] or span[(n - 1) // 2:n // 2 + 1]
                for k, (a, b) in enumerate(span):
                    own = self.owner.get((a, b))
                    if own and own[0] == "room" or not self.ok(a, b):
                        continue                         # a wall against another room, or the block's edge
                    cand.append(((a, b), self.wall_point(a - vx, b - vy, vx, vy), (vx, vy), f, k / max(1, len(span) - 1)))
        if facing:
            mine = [c for c in cand if c[3] == facing]
            if mine and outer:                          # the most northern (or southern...) of a layout's walls
                key = {"north": lambda c: c[0][1], "south": lambda c: -c[0][1],
                       "west": lambda c: c[0][0], "east": lambda c: -c[0][0]}[facing]
                lead = min(key(c) for c in mine)
                mine = [c for c in mine if key(c) == lead]
            if side and mine:
                along = (lambda c: c[0][0]) if facing in ("north", "south") else (lambda c: c[0][1])
                lo, hi = min(along(c) for c in mine), max(along(c) for c in mine)
                mid = (lo + hi) / 2
                half = [c for c in mine if (along(c) <= mid if side in "wn" else along(c) >= mid)]
                mine = half or mine
            cand = mine or cand
        return [(c[0], c[1], c[2]) for c in cand]

    def walls_out(self, e: End, way) -> list:
        """An end's walls that stand on the block's edge, facing out: the way asked first."""
        p = self.plan
        rooms = [p.rooms[e.target]] if e.target in p.rooms else p.layouts[e.target].rooms if e.target in p.layouts else []
        out = []
        for r in rooms:
            i0, j0 = r.at
            for f, (vx, vy) in FACING.items():
                if way and f != way:
                    continue
                span = [(i0 + a, j0 - 1 if f == "north" else j0 + r.h) for a in range(r.w)] if f in ("north", "south") \
                    else [(i0 - 1 if f == "west" else i0 + r.w, j0 + b) for b in range(r.h)]
                n = len(span)
                for k, (a, b) in enumerate(span):
                    if abs(k + .5 - n / 2) < max(1, n / 4) and not self.ok(a, b):
                        out.append(((a, b), self.wall_point(a - vx, b - vy, vx, vy), (vx, vy)))
        return sorted(out, key=lambda w: abs(w[1][0] + w[1][1]))[:1] if out else []

    def diagonal(self, rid, hub: Room, r: Room, rt: Route, door):
        """A straight passage from the hub's corner face to the room's, on the diagonal between them."""
        def face(x: Room, sx, sy):
            x0, y0, w, h = (x.at[0] + EDGE) * K, (x.at[1] + EDGE) * K, x.w * K, x.h * K
            cxx, cyy = x0 + w / 2, y0 + h / 2
            if x.shape == "octagon":
                c = min(w, h) / (2 + math.sqrt(2))
                return cxx + sx * (w / 2 - c / 2), cyy + sy * (h / 2 - c / 2)
            if x.shape == "diamond":
                return cxx + sx * w / 4, cyy + sy * h / 4
            return cxx + sx * w / 2 * math.sqrt(.5), cyy + sy * h / 2 * math.sqrt(.5)
        sx = 1 if r.at[0] > hub.at[0] else -1
        sy = 1 if r.at[1] > hub.at[1] else -1
        a, b = face(hub, sx, sy), face(r, -sx, -sy)
        for t in range(0, 21):                          # the squares it crosses are taken
            x = a[0] + (b[0] - a[0]) * t / 20
            y = a[1] + (b[1] - a[1]) * t / 20
            sq = (int(x // K) - EDGE, int(y // K) - EDGE)
            if sq not in self.owner:
                self.owner[sq] = ("corr", rid)
        pa, pb = [round(v, 2) for v in a], [round(v, 2) for v in b]
        self.corridors.append({"id": rid, "from": {"room": rid_of(hub.key), "port": pa}, "to": {"room": rid_of(r.key), "port": pb},
                               "via": pa + pb, "width": round(rt.width / CELL, 2), "origin": "plan", "doors": [door, door]})

    def free(self, c, rid, join=frozenset()) -> bool:
        if not self.ok(*c):
            return False
        own = self.owner.get(c)
        return own is None or own[0] == "corr" and (own[1] in join or "cross" in self.relax and own[1] != rid)

    def crowded(self, c, rid, join=frozenset()) -> bool:
        """A square beside another passage's, where a passage would run into it."""
        if "cross" in self.relax:
            return False
        for vx, vy in FACING.values():
            own = self.owner.get((c[0] + vx, c[1] + vy))
            if own and own[0] == "corr" and own[1] != rid and own[1] not in join:
                return True
        return False

    def search(self, starts, goals, rid, banned=frozenset(), join=frozenset(), field_only=False):
        """Least-cost path on the lattice from any start (square, step out of its wall) to any goal square:
        a step costs 1, a turn 2 more, a square beside a room's wall 1.5 more, a crossing 20."""
        goals = set(goals)
        dist, prev, heap = {}, {}, []
        for sq, step in starts:
            if sq in banned or not self.free(sq, rid, join) or self.crowded(sq, rid, join):
                continue
            st = (sq, step)
            dist[st] = 0
            heapq.heappush(heap, (0, sq, step))
        while heap:
            d, sq, step = heapq.heappop(heap)
            if d > dist.get((sq, step), 1e18):
                continue
            if sq in goals and not field_only:
                path, st = [sq], (sq, step)
                while st in prev:
                    st = prev[st]
                    path.append(st[0])
                return path[::-1], d
            for vx, vy in FACING.values():
                nxt = (sq[0] + vx, sq[1] + vy)
                if nxt in banned or not self.free(nxt, rid, join):
                    continue
                if nxt not in goals and self.crowded(nxt, rid, join):
                    continue
                cost = 1 + (2 if (vx, vy) != step else 0) + (1.5 if self.hugs(nxt) else 0)
                own = self.owner.get(nxt)
                if own and own[0] == "corr" and own[1] not in join:
                    cost += 20
                nd = d + cost
                if nd < dist.get((nxt, (vx, vy)), 1e18):
                    dist[(nxt, (vx, vy))] = nd
                    prev[(nxt, (vx, vy))] = (sq, step)
                    heapq.heappush(heap, (nd, nxt, (vx, vy)))
        if field_only:
            out = {}
            for (sq, _), d in dist.items():
                out[sq] = min(out.get(sq, 1e18), d)
            return out
        return None, None

    def hugs(self, c) -> bool:
        return any((o := self.owner.get((c[0] + vx, c[1] + vy))) and o[0] == "room" for vx, vy in FACING.values())

    def run(self, rid, a_ends, b_ends, length) -> list | None:
        """The squares of a passage from a door square of a to one of b, near the length asked."""
        starts = [(sq, step) for sq, _, step in a_ends]
        goals = {sq for sq, _, _ in b_ends}
        path, _ = self.search(starts, goals, rid)
        if path is None:
            return None
        if length == "short" or "length" in self.relax:
            return path
        want = None if length == "long" else int(length)
        if want is not None and len(path) >= want:
            if len(path) > want + 1:
                self.missed.append(f"route {rid}: {len(path) * SQ} ft where {want * SQ} ft was asked, the least it can run")
                self.length_error += len(path) - want
            return path
        fa = self.search(starts, (), rid, field_only=True)
        fb = self.search([(sq, step) for sq, _, step in b_ends], (), rid, field_only=True)
        pool = [w for w in fa if w in fb and w not in goals]
        if want is None:
            pool.sort(key=lambda w: -(fa[w] + fb[w]))
        else:
            pool.sort(key=lambda w: abs(fa[w] + fb[w] - want * 1.4))
        best = path
        for w in pool[:40]:
            leg1, _ = self.search(starts, {w}, rid)
            if leg1 is None:
                continue
            ban = set(leg1[:-1])
            for c in leg1[:-1]:
                ban |= {(c[0] + vx, c[1] + vy) for vx, vy in FACING.values()}
            ban.discard(w)
            ban -= {leg1[-1]}
            step = (leg1[-1][0] - leg1[-2][0], leg1[-1][1] - leg1[-2][1]) if len(leg1) > 1 else (0, 0)
            leg2, _ = self.search([(w, step)], goals, rid, banned=frozenset(ban - {w}))
            if leg2 is None:
                continue
            whole = leg1 + leg2[1:]
            if len(set(whole)) != len(whole):
                continue
            if want is None:
                if len(whole) > len(best):
                    best = whole
            elif abs(len(whole) - want) < abs(len(best) - want):
                best = whole
                if len(whole) == want:
                    break
        if want is not None and abs(len(best) - want) > 1:
            self.missed.append(f"route {rid}: {len(best) * SQ} ft where {want * SQ} ft was asked")
            self.length_error += abs(len(best) - want)
        return best

    def take(self, path, rid):
        for c in path:
            if self.owner.get(c, ("", ""))[0] == "corr" and self.owner[c][1] != rid:
                self.crossed += 1
            self.owner[c] = ("corr", rid)

    def touching(self, a: Room, b: Room):
        """The middle of the wall rooms a and b share, in cells, where it is a square long; else None."""
        ai, aj, bi, bj = a.at[0], a.at[1], b.at[0], b.at[1]

        def flat(r: Room, lo, hi, start, size) -> bool:  # the stretch is on the room's straight wall
            if r.shape not in CORNERED:
                return True
            if r.shape == "round":
                return False
            cut = size / (2 + math.sqrt(2)) if r.shape == "octagon" else size * (.3 if r.shape == "round" else .5)
            return lo + .5 >= start + cut - 1e-9 and hi - .5 <= start + size - cut + 1e-9 or \
                (lo + hi) / 2 >= start + cut and (lo + hi) / 2 <= start + size - cut and r.shape != "diamond"
        if ai + a.w == bi or bi + b.w == ai:            # side by side, east and west
            lo, hi = max(aj, bj), min(aj + a.h, bj + b.h)
            if hi - lo >= 1 and flat(a, lo, hi, aj, a.h) and flat(b, lo, hi, bj, b.h):
                x = max(ai, bi)
                return ((x + EDGE) * K, (lo + hi) / 2 * K + EDGE * K)
        if aj + a.h == bj or bj + b.h == aj:
            lo, hi = max(ai, bi), min(ai + a.w, bi + b.w)
            if hi - lo >= 1 and flat(a, lo, hi, ai, a.w) and flat(b, lo, hi, bi, b.w):
                y = max(aj, bj)
                return ((lo + hi) / 2 * K + EDGE * K, (y + EDGE) * K)
        return None

    def route_all(self):
        p = self.plan
        todo = list(self.inner) + sorted(p.routes, key=lambda r: (r.length == "long", r.length not in ("short",), r.kind != "door"))
        for n, r in enumerate(todo):
            rid = f"r{n + 1}"
            self.route(r, rid)

    def route(self, r: Route, rid: str):
        p = self.plan
        label = f"route on line {r.line}" if r.line and not r.inner else f"{r.ends[0].target} to {r.ends[1].target}"
        here = lambda e: e.target in p.rooms or e.target in p.layouts
        order = {id(e): k for k, e in enumerate(r.ends)}
        door = lambda e: (r.doors[min(order[id(e)], len(r.doors) - 1)]) if r.doors else "door"
        inside = [e for e in r.ends if here(e)]
        if not inside:
            return
        ends = []
        for e in r.ends:                                # an end in a block over or under this one is a stair
            far = p.others.get(e.target)
            climb = r.stair if r.stair and not here(e) and e.target != p.bid else \
                ("up" if far[2] > p.xyz[2] else "down") if far and not here(e) and abs(far[2] - p.xyz[2]) > 1e-6 else None
            if climb:
                room = p.rooms.get(inside[0].target) or next(iter(p.layouts[inside[0].target].rooms), None)
                if room and room.at:
                    self.stairs.append((room.key, climb, (inside[0].facing or "north")[0], e.target))
            else:
                ends.append(e)
        ends = [e for e in ends if here(e)] + [e for e in ends if not here(e)]
        if len(ends) < 2:
            return
        a, b = ends[0], ends[1]
        ra, rb = p.rooms.get(a.target), p.rooms.get(b.target)
        if r.kind == "diagonal" and ra and rb and ra.at and rb.at:
            self.diagonal(rid, ra, rb, r, door(a))
            return
        if ra and rb and ra.at and rb.at and (mid := self.touching(ra, rb)) and (r.kind == "door" or r.inner) and len(ends) == 2:
            self.links.append((a.target, b.target, door(a) or "open", mid))
            return
        if ra and rb and r.kind == "door" and not r.inner:
            self.missed.append(f"{label}: {a.target} and {b.target} do not touch, so the door is a passage")
        kinds = []
        for e in (a, b):
            if e.target in p.rooms and p.rooms[e.target].at is None or \
                    e.target in p.layouts and any(q.at is None for q in p.layouts[e.target].rooms):
                self.failed.append(f"{label}: {e.target} was not placed")
                return
            kinds.append(self.resolve(e, None))
        (ka, wa), (kb, wb) = kinds
        for (kx, wx, ex), (ky, wy, ey), flip in (((ka, wa, a), (kb, wb, b), False), ((kb, wb, b), (ka, wa, a), True)):
            if kx != "exit" and ky == "exit" and len(ends) == 2:   # a room on the block's edge: out through its wall
                way = (ey.facing if ey.target == p.bid else ex.facing or self.toward(ey.target)) \
                    if "facing" not in self.relax else None
                edge = [w for w in self.walls_out(ex, way)]
                if edge:
                    sq, pt, step = edge[0]
                    out = [pt[0] + step[0] * K / 2, pt[1] + step[1] * K / 2]
                    room = ex.target if ex.target in p.rooms else self.owner_room(sq, step)
                    self.corridors.append({"id": rid, "from": {"room": rid_of(room), "port": [round(v, 2) for v in pt]},
                                           "to": {"at": out, "exit": {"text": f"To {ey.target}" if ey.target != p.bid else "Out"}},
                                           "via": [round(v, 2) for v in list(pt) + out], "width": round(r.width / CELL, 2),
                                           "origin": "plan", "doors": [door(ex), None]})
                    return
        if not wa or not wb:
            self.failed.append(f"{label}: no free wall at {a.target if not wa else b.target}")
            return
        path = self.run(rid, wa, wb, r.length)
        if path is None and ka != "exit" and kb != "exit" and len(ends) == 2:
            if self.branch(rid, a, b, ka, wa, kb, wb, r, door, label):
                return
        if path is None:
            self.failed.append(f"{label}: no way from {a.target} to {b.target}")
            return
        self.take(path, rid)
        self.corridors.append(self.corridor(rid, path, (ka, wa, door(a), a), (kb, wb, door(b) if kb != "exit" else None, b), r))
        for k, e in enumerate(ends[2:], start=2):       # each further end: a branch to the nearest of the passage
            ke, we = self.resolve(e, None)
            trunk = {c for c, o in self.owner.items() if o == ("corr", rid)}
            goals = {(c[0] + vx, c[1] + vy) for c in trunk for vx, vy in FACING.values()} - trunk
            goals = {g for g in goals if self.free(g, rid + "b")}
            bid = f"{rid}b{k}"
            starts = [(sq, step) for sq, _, step in we]
            if ke == "exit":
                path, _ = self.search([(c, (0, 0)) for c in goals], {sq for sq, _, _ in we}, bid, join=frozenset({rid}))
                path = path[::-1] if path else None
            else:
                path, _ = self.search(starts, goals, bid, join=frozenset({rid}))
            if path is None:
                self.failed.append(f"{label}: no way from {e.target} to the passage")
                continue
            self.take(path, bid)
            joint = next(c for c in trunk if abs(c[0] - path[-1][0]) + abs(c[1] - path[-1][1]) == 1)
            self.corridors.append(self.corridor(bid, path, (ke, we, door(e) if ke != "exit" else None, e), ("join", joint, None, rid), r))

    def branch(self, rid, a, b, ka, wa, kb, wb, r, door, label) -> bool:
        """Where no passage of its own fits, one end's way off a passage that already leaves the other end."""
        for (x, kx, wx, dx), (y, ky, wy) in (((b, kb, wb, 1), (a, ka, wa)), ((a, ka, wa, 0), (b, kb, wb))):
            rooms = {rid_of(y.target)} if y.target in self.plan.rooms else \
                {rid_of(q.key) for q in self.plan.layouts[y.target].rooms} if y.target in self.plan.layouts else set()
            for c in list(self.corridors):
                if "corridor" in c["to"] or not ({c["from"].get("room"), c["to"].get("room")} & rooms):
                    continue
                trunk = {q for q, o in self.owner.items() if o == ("corr", c["id"])}
                goals = {(q[0] + vx, q[1] + vy) for q in trunk for vx, vy in FACING.values()} - trunk
                goals = {g for g in goals if self.free(g, rid)}
                path, _ = self.search([(sq, step) for sq, _, step in wx], goals, rid, join=frozenset({c["id"]}))
                if path is None:
                    continue
                self.take(path, rid)
                joint = next(q for q in trunk if abs(q[0] - path[-1][0]) + abs(q[1] - path[-1][1]) == 1)
                self.corridors.append(self.corridor(rid, path, (kx, wx, door(x), x), ("join", joint, None, c["id"]), r))
                self.missed.append(f"{label}: no wall of its own left free, so {x.target} joins the passage at {y.target}")
                return True
        return False

    def corridor(self, rid, path, a, b, r: Route) -> dict:
        """An artgen corridor along these squares: from a's wall to b's, a passage's end, or the block's edge."""
        centre = lambda c: [(c[0] + EDGE) * K + K / 2, (c[1] + EDGE) * K + K / 2]

        def end(spec, sq):
            kind, ws, door, e = spec
            if kind == "join":
                return {"corridor": e, "near": centre(ws)}, None
            pt, step = next((w[1], w[2]) for w in ws if w[0] == sq)
            if kind == "exit":
                x, y = centre(sq)
                return {"at": [x + step[0] * K / 2, y + step[1] * K / 2],
                        "exit": {"text": f"To {e.target}" if e.target != self.plan.bid else "Out"}}, None
            room = e.target if e.target in self.plan.rooms else self.owner_room(sq, step)
            return {"room": rid_of(room), "port": [round(pt[0], 2), round(pt[1], 2)]}, door
        f, df = end(a, path[0])
        t, dt = end(b, path[-1]) if b[0] != "join" else end(b, None)
        pts = [centre(c) for c in path]
        if b[0] == "join":
            pts.append(centre(b[1]))
        bends = [pts[0]]
        for p0, p1, p2 in zip(pts, pts[1:], pts[2:]):
            if (p1[0] - p0[0]) * (p2[1] - p1[1]) != (p1[1] - p0[1]) * (p2[0] - p1[0]):
                bends.append(p1)
        bends.append(pts[-1])
        bends = [b for k, b in enumerate(bends) if not k or b != bends[k - 1]]
        via = [v for p in bends for v in p]
        c = {"id": rid, "from": f, "to": t, "via": via, "width": round(r.width / CELL, 2), "origin": "plan",
             "doors": [df, dt]}
        if r.label:
            c["label"] = r.label
        return c

    def owner_room(self, sq, step) -> str:
        own = self.owner.get((sq[0] - step[0], sq[1] - step[1]))
        return own[1] if own else ""

    def solve(self):
        self.stairs = []
        items, first, self.tight = self.items(), set(), False
        for k in range(4):                              # an item that found no room is placed earlier, and all again
            self.unplaced, self.owner, self.missed = [], {}, []
            for r in self.plan.rooms.values():
                r.at = None
            for it in items:
                it.at = None
            self.place(items, first)
            if not self.unplaced:
                break
            first |= set(self.unplaced)
            self.tight = k >= 1
        self.notes += [f"{k} finds no room in the block" for k in self.unplaced]
        unplaced = [k for k, r in self.plan.rooms.items() if r.at is None]
        self.failed += [f"{k} was not placed" for k in unplaced]
        self.route_all()
        self.check_hints()
        return self

    def check_hints(self):
        for k, (e, n) in self.plan.pins.items():
            r = self.plan.rooms.get(k)
            if r and r.at:
                x = (r.at[0] + r.w / 2 - self.gw / 2) * SQ + self.ox
                y = (self.gh / 2 - r.at[1] - r.h / 2) * SQ + self.oy
                if abs(x - e) >= r.w * SQ / 2 or abs(y - n) >= r.h * SQ / 2:
                    self.missed.append(f"{k} stands at {x:g},{y:g}, not over the room its stair meets at {e:g},{n:g}: "
                                       f"solve this level --free, then place the next")
        cells = sum(1 for col in self.cell_in for c in col if c)
        cover = sum(r.w * r.h for r in self.plan.rooms.values() if r.at) / max(1, cells)
        lo, hi = self.plan.fill
        if not lo - .02 <= cover <= hi + .02:
            self.notes.append(f"rooms cover {cover:.0%} of the block, outside the fill of {lo:.0%}-{hi:.0%}: "
                              f"{'grow the rooms or shrink the outline' if cover < lo else 'shrink the rooms or grow the outline'}")
        for it in self.placed:
            if it.facing in FACING:
                fx = (it.at[0] + it.w / 2) / self.gw
                fy = (it.at[1] + it.h / 2) / self.gh
                v = {"north": fy, "south": 1 - fy, "west": fx, "east": 1 - fx}[it.facing]
                if v > .5:
                    self.missed.append(f"{it.key} is not in the {it.facing} of the block")
                elif it.side:
                    t = fx if it.facing in ("north", "south") else fy
                    if (t > .5) == (it.side in "wn"):
                        self.missed.append(f"{it.key} is not on the {it.side} side")

    def score_of(self) -> tuple:
        return (len(self.failed), self.crossed, len(self.missed), self.length_error,
                sum(len(c["via"]) for c in self.corridors))


def rid_of(code: str) -> str:
    return code.replace(".", "-")


# -- the map ----------------------------------------------------------------------------------

def dungeon_file(s: Solver, title: str | None = None, look: bool = True) -> dict:
    p = s.plan
    rooms = []
    for k, r in p.rooms.items():
        if r.at is None:
            continue
        shape = SHAPES[r.shape]
        room = {"id": rid_of(k), "shape": shape, "x": (r.at[0] + EDGE) * K, "y": (r.at[1] + EDGE) * K,
                "w": r.w * K, "h": r.h * K, "number": False, "origin": "plan"}
        if r.named:
            room["label"] = r.label or k
        elif r.label:
            room["label"] = r.label
        else:
            room["label"] = ""
        if shape == "octagon":
            room["cut"] = round(1 / (2 + math.sqrt(2)), 4)
        if r.shape == "diamond":
            x, y, w, h = room["x"], room["y"], room["w"], room["h"]
            room["points"] = [x + w / 2, y, x + w, y + h / 2, x + w / 2, y + h, x, y + h / 2]
        rooms.append(room)
    for key, way, side, far in s.stairs:
        room = next(x for x in rooms if x["id"] == rid_of(key))
        sides = [x["side"] for x in room.get("exits", [])]
        side = next((d for d in [side] + list("nesw") if d not in sides), side)   # each stair by a wall of its own
        room.setdefault("exits", []).append({"kind": "stairs-up" if way == "up" else "stairs-down", "side": side,
                                             "text": f"{'Up' if way == 'up' else 'Down'} to {far}"})
    cx, cy = s.gw / 2, s.gh / 2
    bounds = [v for x, y in s.poly for v in (round((cx + (x - s.ox) / SQ + EDGE) * K, 2), round((cy - (y - s.oy) / SQ + EDGE) * K, 2))]
    m = {"id": rid_of(p.bid), "version": 2, "seed": s.seed, "cols": (s.gw + 2 * EDGE) * K, "rows": (s.gh + 2 * EDGE) * K,
         "grid": {"show": True, "size": K, "sub": True, "clip": "floor"},
         "style": {"hatch": "full", "wall": 1.5}, "scale": {"perCell": CELL, "unit": "ft"},
         "numbers": False, "scaleBar": True, "compass": False, "furniture": {"place": "outside"},
         "rooms": rooms, "corridors": s.corridors,
         "connections": [{"a": rid_of(a), "b": rid_of(b), "at": [round(mid[0], 2), round(mid[1], 2)],
                          "kind": d if d in DOORS and d != "none" else "open", "origin": "plan"} for a, b, d, mid in s.links],
         "overlay": {"labels": [], "symbols": []}, "bounds": bounds}
    if title:
        m["title"] = title
    if look:
        try:
            import dungeon
            m["style"] = dungeon.looked(m["style"])
        except Exception:                               # a plan tried outside the setting keeps the plain look
            pass
    return m


# -- solving ------------------------------------------------------------------------------------

LADDER = [set(), {"side"}, {"side", "facing"}, {"side", "facing", "length"},
          {"side", "facing", "length", "grow"}, {"side", "facing", "length", "grow", "cross"}]
SAID = {"side": "sides set aside", "facing": "facings set aside", "length": "lengths set aside", "grow": "the block grown",
        "cross": "passages let cross"}


def solve(lines: list[kdl.Node], bid: str, seeds: int = 16, others: dict | None = None,
          pins: dict | None = None) -> tuple[Solver | None, list[str]]:
    """The best attempt at a block's plan: over seeds, then down the ladder of goals set aside until every
    way routes; with the plan's own problems."""
    best = None
    for relax in LADDER:
        for seed in range(1, seeds + 1):
            try:
                plan = Plan(bid, lines, others, pins)
            except ValueError as e:
                return None, [str(e)]
            s = Solver(plan, seed, relax).solve()
            if best is None or (len(s.failed), len(relax), s.score_of()) < (len(best.failed), len(best.relax), best.score_of()):
                best = s
            if not s.failed and not s.missed and not s.crossed:
                break
        if not best.failed:
            break
    if best.relax:
        best.notes.append("to route every way: " + ", ".join(SAID[k] for k in SAID if k in best.relax))
    return best, best.plan.problems


def report(s: Solver) -> list[str]:
    p = s.plan
    out = []
    area = sum(r.w * r.h for r in p.rooms.values() if r.at)
    cells = sum(1 for col in s.cell_in for c in col if c)
    out.append(f"{p.bid}: {len(p.rooms)} rooms ({sum(r.named for r in p.rooms.values())} locations), "
               f"{len(s.corridors)} passages, {len(s.links)} doors through shared walls; seed {s.seed}; "
               f"rooms cover {area / max(1, cells):.0%} of the block (asked {p.fill[0]:.0%}-{p.fill[1]:.0%})")
    for c in s.corridors:
        out.append(f"  {c['id']}: {describe(c)}")
    for x in s.failed:
        out.append(f"  UNROUTED: {x}")
    for x in s.missed:
        out.append(f"  goal missed: {x}")
    for x in s.notes:
        out.append(f"  note: {x}")
    if s.crossed:
        out.append(f"  note: {s.crossed} square(s) where passages cross")
    return out


def describe(c: dict) -> str:
    def end(e):
        return e.get("room") or (f"passage {e['corridor']}" if "corridor" in e else e.get("exit", {}).get("text", "edge"))
    pts = list(zip(c["via"][::2], c["via"][1::2]))
    run = sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(pts, pts[1:])) * CELL + SQ
    return f"{end(c['from'])} to {end(c['to'])}, about {run:.0f} ft"


def engine(*args) -> tuple[int, str]:
    import subprocess
    js = Path(__file__).resolve().parent / "artgen" / "artgen-maps.js"
    done = subprocess.run(["node", str(js), *map(str, args)], capture_output=True, text=True)
    return done.returncode, done.stdout + done.stderr


def write(s: Solver, out: Path, render: bool = True) -> list[str]:
    out.mkdir(parents=True, exist_ok=True)
    f = out / f"{s.plan.bid}.json"
    f.write_text(json.dumps(dungeon_file(s), indent=1))
    said = []
    code, text = engine("dungeon", "check", "--file", f, "--json")
    try:
        got = json.loads(text[text.index("{"):])
        leaving = {f"corridors[{k}]" for k, c in enumerate(s.corridors) if "exit" in c["to"] or "exit" in c["from"]}
        said += [f"  map {w.get('id', 'error')}: {w['path']}: {w['message']}" for w in got.get("errors", []) + got.get("warnings", [])
                 if not (w.get("id") == "outside-bounds" and w["path"] in leaving)]
    except (ValueError, KeyError):
        said.append(f"  map check: {text.strip()[:300]}")
    if render:
        engine("dungeon", "render", "--file", f, "--format", "png", "--out", out, "--ppu", 24)
        said.append(f"  drawn: {out / (s.plan.bid + '.png')}")
    return said


def lines_of(path: Path) -> list[kdl.Node]:
    text = path.read_text()
    return kdl.fenced(text) if "```kdl" in text else kdl.parse(text)


def planned(lines: list[kdl.Node]) -> list[str]:
    """The blocks these lines plan: a Design with a Layout, Room or Route line."""
    has = {str(n.args[0]) for n in lines if n.name in ("Layout", "Route") and n.args} | \
          {str(n.args[0]) for n in lines if n.name == "Room" and n.args and BLOCK_RE.fullmatch(str(n.args[0]))}
    room_blocks = {str(n.args[0]) for n in lines if n.name == "Design" and n.args and
                   any(r.name == "Room" and r.args and str(r.args[0]) in words(n.props.get("locations")) for r in lines)}
    return [str(n.args[0]) for n in lines if n.name == "Design" and n.args and str(n.args[0]) in has | room_blocks]


def others_of(lines) -> dict:
    """Each block's xyz, under its id, its layouts' ids and its locations' codes: where a way out of another block leads."""
    out = {}
    for n in lines:
        if n.name == "Design" and n.args and n.props.get("xyz"):
            c = ([float(x) for x in str(n.props["xyz"]).split(",")] + [0.0, 0.0])[:3]
            bid = str(n.args[0])
            for k in [bid] + words(n.props.get("locations")) + [str(m.props.get("id")) for m in lines
                                                               if m.name == "Layout" and m.args and str(m.args[0]) == bid]:
                out[k] = tuple(c)
    return out


def accept_lines(s: Solver) -> list[str]:
    """The `Place` and `Link` lines one solve writes: each location's centre from the block's, and each way between
    two locations of the block - every pair a route's passage joins."""
    p, out = s.plan, []
    cx, cy = s.gw / 2, s.gh / 2
    for k, r in p.rooms.items():
        if not r.named or r.at is None:
            continue
        x = (r.at[0] + r.w / 2 - cx) * SQ + s.ox
        y = (cy - r.at[1] - r.h / 2) * SQ + s.oy
        out.append(f'Place {k} xyz="{x:g},{y:g}" outline="rect {r.w * SQ} {r.h * SQ}" shape={r.shape}')
    seen = set()
    named = lambda e: e if e in p.rooms and p.rooms[e].named else None
    pairs = [(a, b, "door") for a, b, _, _ in s.links]
    groups: dict[str, set] = {}
    for c in s.corridors:
        root = c["to"].get("corridor") or c["id"]
        g = groups.setdefault(root, set())
        for e in (c["from"], c["to"]):
            if "room" in e:
                g.add(e["room"].replace("-", "."))
    for g in groups.values():
        for a in g:
            for b in g:
                if a < b:
                    pairs.append((a, b, "passage"))
    num = lambda c: int(c.split(".")[1])
    for a, b, kind in sorted((min(x, y, key=num), max(x, y, key=num), k) for x, y, k in pairs if named(x) and named(y)):
        if (a, b) not in seen:
            seen.add((a, b))
            out.append(f'Link {a} to="{b}" kind={kind}')
    return out


# -- the framework's side: a region's planned blocks ------------------------------------------

def plans_of(region) -> list[str]:
    """A region's planned blocks: Design lines with Layout, Room or Route lines."""
    return planned(region.files.get("Design", []))


def pins_of(lines, bid: str) -> dict:
    """Each room of the block a stair joins to a placed room of another level: the centre of the box it stands over."""
    import space
    head = next((n for n in lines if n.name == "Design" and n.args and str(n.args[0]) == bid), None)
    out = {}
    for c in words(head.props.get("locations")) if head else []:
        if pin := space.settled().pin(c):
            out[c] = (pin[0], pin[1])
    return out


def problems_of(region, bid: str) -> tuple[list[str], list[str]]:
    """A planned block's faults - what the plan states wrongly - and the ways no solve routes."""
    lines = region.files.get("Design", [])
    s, said = solve(lines, bid, others=others_of(lines), pins=pins_of(lines, bid))
    return said, (s.failed if s else ["no solve"])


def block_map(region, block: kdl.Node) -> tuple[dict | None, list[str]]:
    """An approved plan's map: its solve, with each door the kind the tables' Connections give it."""
    import dungeon
    lines = region.files.get("Design", [])
    bid = str(block.args[0])
    s, said = solve(lines, bid, others=others_of(lines), pins=pins_of(lines, bid))
    if s is None:
        return None, said
    m = dungeon_file(s, look=False)
    m["style"] = dungeon.looked({"hatch": "full", "wall": dungeon.ROUTED_WALL})
    ways = {}
    for n in region.files.get("Connections", []):
        if n.args and "to" in n.props:
            kids = {k.name for k in n.children}
            kind = "locked" if "Lock" in kids else "secret" if "Secret" in kids else dungeon.DOOR.get(str(n.props.get("type")), "door")
            ways[(str(n.args[0]), str(n.props["to"]))] = kind
    code = lambda rid: rid.replace("-", ".")
    groups: dict[str, set] = {}                         # rooms each network of passages joins
    root = {}
    for c in m["corridors"]:
        root[c["id"]] = root.get(c["to"].get("corridor"), c["to"].get("corridor")) or c["id"]
        groups.setdefault(root[c["id"]], set()).update(e["room"] for e in (c["from"], c["to"]) if "room" in e)
    for c in m["corridors"]:
        for k, e in enumerate((c["from"], c["to"])):
            if "room" not in e or c["doors"][k] is None:
                continue
            here = code(e["room"])
            got = [ways[(here, code(o))] for o in groups[root[c["id"]]] if (here, code(o)) in ways]
            if got:
                c["doors"][k] = next((g for g in got if g in ("locked", "secret")), got[0]) or "arch"
    for x in m["connections"]:
        got = ways.get((code(x["a"]), code(x["b"]))) or ways.get((code(x["b"]), code(x["a"])))
        if (code(x["a"]), code(x["b"])) in ways or (code(x["b"]), code(x["a"])) in ways:
            x["kind"] = got or dungeon.GAP.get("Archway", "open")
    return m, said + s.failed


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["solve", "accept"])
    ap.add_argument("code", nargs="?")
    ap.add_argument("block", nargs="?")
    ap.add_argument("--file", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--seeds", type=int, default=16)
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--free", action="store_true", help="ignore where the levels a stair joins put its rooms")
    a = ap.parse_args(argv)
    if a.file:
        lines, where, block = lines_of(a.file), a.file, a.code
    else:
        if not a.code:
            ap.error("name a region, or --file")
        where = Path(__file__).resolve().parent.parent / "setting" / "region" / a.code / "Design.md"
        if not where.exists():
            print(f"{where} does not exist", file=sys.stderr)
            return 1
        lines, block = lines_of(where), a.block
    blocks = [b for b in planned(lines) if block in (None, b)]
    if not blocks:
        print(f"{where} plans no block{' ' + block if block else ''}: a plan is a Design line with Layout, Room and Route lines",
              file=sys.stderr)
        return 1
    out = a.out or Path(tempfile.gettempdir()) / "plans"
    bad = 0
    for b in blocks:
        s, problems = solve(lines, b, a.seeds, others_of(lines), None if a.file or a.free else pins_of(lines, b))
        for x in problems:
            print(f"  plan: {x}")
        if s is None:
            bad += 1
            continue
        if a.command == "accept":
            if s.failed:
                print("\n".join(report(s)))
                print(f"{b} leaves ways unrouted: nothing written", file=sys.stderr)
                bad += 1
                continue
            text = where.read_text()
            fresh = [l for l in text.splitlines() if not re.match(rf"\s*(Place|Link) ({re.escape(b.split('.')[0])}\.\d+)\b", l)
                     or not any(l.strip().split()[1] == c for c in s.plan.rooms)]
            close = max(i for i, l in enumerate(fresh) if l.strip() == "```")
            fresh[close:close] = accept_lines(s)
            fresh = [re.sub(r' seed=\S+', "", re.sub(r' approved="[^"]*"', "", l)) + f" seed={s.seed}"
                     if l.startswith(f"Design {b} ") else l for l in fresh]
            where.write_text("\n".join(fresh) + "\n")
            print(f"{b}: wrote {len(accept_lines(s))} Place and Link lines to {where}")
            continue
        print("\n".join(report(s)))
        print("\n".join(write(s, out, not a.no_render)))
        bad += bool(s.failed)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
