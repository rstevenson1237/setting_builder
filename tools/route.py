"""Corridors for a packed block: each way a door through a shared wall or a winding passage.

A room is a footprint whose box has its corners on a LATTICE-foot grid; its floor is the
lattice cells whose centres its outline holds. A passage is a path of free cells from a cell
against one room's wall to a cell against the other's, bending where it likes, never touching
another way's passage but where the two leave one room, and never running through a room. Two
passages leaving one room may join and part again, but never run side by side.
Its door stands on the wall between the room and the path's first cell: square across it
where that wall runs along the lattice, else where the line from the room's hub to that cell
crosses the wall. A way that names its wall, as a bearing from the room's centre, leaves by a
door within half a compass point of it, or where the room has none there, the nearest it has.
"""
from __future__ import annotations

import functools
import heapq
import math
from dataclasses import dataclass, field

VERSION = 3                 # raised by any change that routes placed rooms differently; a packed Block records it
SEED = 1                    # the noise every plan is routed with, so a draw finds the passages a pack did
LATTICE = 10                # feet, a passage's width and the grid rooms and passages lie on
TURN = 0.5                  # what a bend costs, in cells of path
RUN = 4                     # cells a passage runs straight before each further cell costs
RUN_COST = 0.2
SHARE = 0.4                 # taken off a cell another way from the same room already uses
WANDER = 0.45               # the most a cell's noise adds, so equal routes differ
HALF = 11.25                # degrees: half a compass point, how far a door may stand from its stated wall
CIRCLE = 64                 # sides of the polygon a round room is drawn as, as artgen draws it
STEPS = {"n": (0, -1), "e": (1, 0), "s": (0, 1), "w": (-1, 0)}
TURNED = {"n": "s", "s": "n", "e": "w", "w": "e"}
SHAPES = ("rect", "cave", "round", "octagon", "hexagon", "poly")   # a cave is routed as its box


def outline_of(shape: str, w: float, h: float, points=None) -> list[tuple[float, float]]:
    """A room's outline in feet east and south of its box's centre. A round room is its box's
    ellipse; an octagon cuts its box's corners so a square one is regular; a hexagon has flat
    north and south walls and points east and west; a poly is its own points. Each runs clockwise
    on the page, as artgen draws a wall."""
    a, b = w / 2, h / 2
    if shape == "round":
        return [(a * math.cos(2 * math.pi * i / CIRCLE), b * math.sin(2 * math.pi * i / CIRCLE)) for i in range(CIRCLE)]
    if shape == "octagon":
        c = min(w, h) / (2 + math.sqrt(2))
        return [(-a + c, -b), (a - c, -b), (a, -b + c), (a, b - c), (a - c, b), (-a + c, b), (-a, b - c), (-a, -b + c)]
    if shape == "hexagon":
        return [(-a / 2, -b), (a / 2, -b), (a, 0.0), (a / 2, b), (-a / 2, b), (-a, 0.0)]
    if shape == "poly" and points:
        p = [(float(x), float(y)) for x, y in points]
        return p if sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(p, p[1:] + p[:1])) > 0 else p[::-1]
    return [(-a, -b), (a, -b), (a, b), (-a, b)]


def holds(poly: list[tuple[float, float]], x: float, y: float) -> bool:
    inside = False
    for (x0, y0), (x1, y1) in zip(poly, poly[-1:] + poly[:-1]):
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            inside = not inside
    return inside


def raster(poly: list[tuple[float, float]], whole: bool = False) -> frozenset[tuple[int, int]]:
    """The lattice cells an outline reaches into, or with `whole`, those it holds entirely."""
    xs, ys, e = [p[0] for p in poly], [p[1] for p in poly], 1e-3 * LATTICE
    out = set()
    for i in range(math.floor(min(xs) / LATTICE), math.ceil(max(xs) / LATTICE)):
        for j in range(math.floor(min(ys) / LATTICE), math.ceil(max(ys) / LATTICE)):
            if whole:
                marks = [(u * LATTICE + (e if u == i else -e), v * LATTICE + (e if v == j else -e)) for u in (i, i + 1) for v in (j, j + 1)]
            else:
                marks = [((i + (k + 0.5) / 4) * LATTICE, (j + (m + 0.5) / 4) * LATTICE) for k in range(4) for m in range(4)]
            if (all if whole else any)(holds(poly, *p) for p in marks):
                out.add((i, j))
    return frozenset(out)


def kernel(poly: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """The part of an outline from which every point of it can be seen: empty where none can."""
    turn = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))
    out = list(poly)
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        side = lambda p: ((bx - ax) * (p[1] - ay) - (by - ay) * (p[0] - ax)) * (1 if turn > 0 else -1)
        kept = []
        for p, q in zip(out, out[1:] + out[:1]):
            sp, sq = side(p), side(q)
            if sp >= -1e-9:
                kept.append(p)
            if (sp >= -1e-9) != (sq >= -1e-9):
                t = sp / (sp - sq)
                kept.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
        out = kept
        if len(out) < 3:
            return []
    return out


def edge(p, a, b) -> float:
    """Feet from point p to the segment from a to b."""
    L2 = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    t = max(0.0, min(1.0, ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / L2)) if L2 else 0.0
    return math.dist(p, (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))


def bearing(dx: float, dy: float) -> float:
    """Degrees clockwise from north of a displacement east and south."""
    return math.degrees(math.atan2(dx, -dy)) % 360


def off(a: float, b: float) -> float:
    """Degrees between two bearings."""
    return abs((a - b + 180) % 360 - 180)


@dataclass(frozen=True)
class Slot:
    """Where a door of a room can stand: the free cell it opens on, the room's cell behind it, the
    side of the room it is on (none where the wall there is not square to the lattice), the
    door's point on the wall, and its bearing from the room's centre."""
    cell: tuple[int, int]
    inner: tuple[int, int]
    side: str
    point: tuple[float, float]
    bearing: float


@dataclass(eq=False)
class Footprint:
    x: float                # feet east and south of the plan's origin, its box's top left
    y: float
    w: float
    h: float
    shape: str = "rect"
    points: tuple | None = None     # a poly's outline, feet east and south of its box's centre

    @property
    def square(self) -> bool:
        """Every wall runs along the lattice and the box is the floor."""
        return self.shape in ("rect", "cave")

    @property
    def round(self) -> bool:
        return self.shape == "round"

    @property
    def centre(self) -> tuple[float, float]:
        return self.x + self.w / 2, self.y + self.h / 2

    @functools.cached_property
    def outline(self) -> list[tuple[float, float]]:
        cx, cy = self.centre
        return [(cx + a, cy + b) for a, b in outline_of(self.shape, self.w, self.h, self.points)]

    def holds(self, x: float, y: float) -> bool:
        if self.square:
            return self.x < x < self.x + self.w and self.y < y < self.y + self.h
        return holds(self.outline, x, y)

    @property
    def span(self) -> tuple[int, int, int, int]:
        """First and last lattice column and row the room's box covers."""
        return (math.floor(self.x / LATTICE + 1e-6), math.floor(self.y / LATTICE + 1e-6),
                math.ceil((self.x + self.w) / LATTICE - 1e-6) - 1, math.ceil((self.y + self.h) / LATTICE - 1e-6) - 1)

    @functools.cached_property
    def cells(self) -> frozenset[tuple[int, int]]:
        """The lattice cells of its floor: those whose centres it holds."""
        i0, j0, i1, j1 = self.span
        return frozenset((i, j) for i in range(i0, i1 + 1) for j in range(j0, j1 + 1)
                         if self.square or self.holds((i + 0.5) * LATTICE, (j + 0.5) * LATTICE))

    @functools.cached_property
    def touched(self) -> frozenset[tuple[int, int]]:
        """The lattice cells any of its floor reaches into, which no other room may."""
        if self.square:
            return self.cells
        i0, j0, i1, j1 = self.span
        marks = [(k + 0.5) / 4 for k in range(4)]
        return self.cells | frozenset((i, j) for i in range(i0, i1 + 1) for j in range(j0, j1 + 1)
                                      if any(self.holds((i + u) * LATTICE, (j + v) * LATTICE) for u in marks for v in marks))

    def full(self, c: tuple[int, int]) -> bool:
        """Whether a cell lies wholly on its floor."""
        if self.square:
            return c in self.cells
        e = 1e-3 * LATTICE
        return c in self.cells and all(self.holds((c[0] + u) * LATTICE + (e if u == 0 else -e), (c[1] + v) * LATTICE + (e if v == 0 else -e))
                                       for u in (0, 1) for v in (0, 1))

    @functools.cached_property
    def hub(self) -> tuple[float, float] | None:
        """The point a way is drawn from to a door: of the points that see every wall, the one
        clearest of the walls, up to half a passage, and nearest the centre; None where no point
        sees every wall."""
        if self.shape != "poly":
            return self.centre
        k = kernel(self.outline)
        if not k:
            return None
        step, c = LATTICE / 4, self.centre
        xs, ys = [p[0] for p in k], [p[1] for p in k]
        seen = [c] + [(x0 + i * step, y0 + j * step) for x0, y0 in [(min(xs), min(ys))]
                      for i in range(int((max(xs) - x0) / step) + 1) for j in range(int((max(ys) - y0) / step) + 1)]
        seen = [p for p in seen if holds(k, *p) and self.holds(*p)]
        clear = lambda p: min(LATTICE / 2, min(edge(p, a, b) for a, b in zip(self.outline, self.outline[1:] + self.outline[:1])))
        return max(seen, key=lambda p: (round(clear(p), 6), -math.dist(p, c))) if seen else None

    def cross(self, inner: tuple[float, float], outer: tuple[float, float]) -> tuple[float, float]:
        """Where the line from a point it holds to one it does not crosses its wall."""
        lo, hi = 0.0, 1.0
        for _ in range(30):
            t = (lo + hi) / 2
            if self.holds(inner[0] + (outer[0] - inner[0]) * t, inner[1] + (outer[1] - inner[1]) * t):
                lo = t
            else:
                hi = t
        return inner[0] + (outer[0] - inner[0]) * lo, inner[1] + (outer[1] - inner[1]) * lo

    @functools.cached_property
    def slots(self) -> list[Slot]:
        """Every place a door of the room can stand, in a fixed order."""
        out, seen = [], set()
        cx, cy = self.centre
        for i, j in self.cells:
            for s, (dx, dy) in STEPS.items():
                f = (i + dx, j + dy)
                if f in self.cells:
                    continue
                mid = ((i + 0.5 + dx / 2) * LATTICE, (j + 0.5 + dy / 2) * LATTICE)
                if self.full((i, j)) and not self.holds(mid[0] + dx * LATTICE / 4, mid[1] + dy * LATTICE / 4):
                    p = self.cross(((i + 0.5) * LATTICE, (j + 0.5) * LATTICE), ((f[0] + 0.5) * LATTICE, (f[1] + 0.5) * LATTICE)) \
                        if not self.square else {"n": (mid[0], self.y), "s": (mid[0], self.y + self.h),
                                                 "w": (self.x, mid[1]), "e": (self.x + self.w, mid[1])}[s]
                    out.append(Slot(f, (i, j), s, p, bearing(p[0] - cx, p[1] - cy)))
                elif f not in seen and self.hub:
                    seen.add(f)
                    p = self.cross(self.hub, ((f[0] + 0.5) * LATTICE, (f[1] + 0.5) * LATTICE))
                    out.append(Slot(f, (i, j), "", p, bearing(p[0] - cx, p[1] - cy)))
        rank = "nswe"
        return sorted(out, key=lambda s: (0, s.cell[0], rank.index(s.side), s.cell[1]) if s.side in ("n", "s")
                      else (1, s.cell[1], rank.index(s.side), s.cell[0]) if s.side else (2, s.bearing))

    def allowed(self, want: float | None) -> list[Slot]:
        """The slots a way may leave by: all, or those within half a compass point of the wall it
        names, or where none are, the nearest."""
        if want is None or not self.slots:
            return self.slots
        near = [s for s in self.slots if off(s.bearing, want) <= HALF + 1e-6]
        if near:
            return near
        least = min(off(s.bearing, want) for s in self.slots)
        return [s for s in self.slots if off(s.bearing, want) <= least + 1e-6]

    def lead(self, side: str, door: tuple[float, float]) -> list[tuple[float, float]]:
        """The points inside the room a way is drawn through to reach its door from the hub: none
        where it leaves a square room by a side, which draws it straight."""
        if self.square and side:
            return []
        if not side:
            return [self.hub]
        dx, dy = STEPS[side]
        return [self.hub, (door[0] - dx * LATTICE / 2, door[1] - dy * LATTICE / 2)]


@dataclass
class Route:
    a: str
    b: str
    kind: str                                       # "wall": a door through the wall the rooms share; "path"
    side_a: str = ""                                # n, e, s or w; none where the door is off the lattice
    side_b: str = ""
    door_a: tuple[float, float] = (0.0, 0.0)        # on the wall, in feet
    door_b: tuple[float, float] = (0.0, 0.0)
    cells: list[tuple[int, int]] = field(default_factory=list)
    length: float = 0.0                             # feet from one room's centre to the other's, by the way
    bearing_a: float = 0.0                          # each door's bearing from its room's centre
    bearing_b: float = 0.0

    def points(self) -> list[tuple[float, float]]:
        """The way's corners from door to door, in feet."""
        if self.kind == "wall":
            return [self.door_a, self.door_b]
        pts = [self.door_a] + [((i + 0.5) * LATTICE, (j + 0.5) * LATTICE) for i, j in self.cells] + [self.door_b]
        keep = [pts[0]]
        for p, q, r in zip(pts, pts[1:], pts[2:]):
            if abs((q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])) > 1e-6:
                keep.append(q)
        return keep + [pts[-1]]


def box_wall(p: Footprint, q: Footprint):
    """Where two rect rooms touch along a wall a door fits: (side of p, side of q, door point
    mid-way along it, the stretch's ends along it), else None."""
    for (ap, aq, sp, sq) in ((p.x + p.w, q.x, "e", "w"), (q.x + q.w, p.x, "w", "e")):
        lo, hi = max(p.y, q.y), min(p.y + p.h, q.y + q.h)
        if abs(ap - aq) < 1e-6 and hi - lo >= LATTICE:
            return sp, sq, (ap, (lo + hi) / 2), lo, hi
    for (ap, aq, sp, sq) in ((p.y + p.h, q.y, "s", "n"), (q.y + q.h, p.y, "n", "s")):
        lo, hi = max(p.x, q.x), min(p.x + p.w, q.x + q.w)
        if abs(ap - aq) < 1e-6 and hi - lo >= LATTICE:
            return sp, sq, ((lo + hi) / 2, ap), lo, hi
    return None


def shared_wall(p: Footprint, q: Footprint, want_p: float | None = None, want_q: float | None = None):
    """Where two rooms meet along a square wall a door fits: (side of p, side of q, door point),
    else None. With no wall named, the door stands mid-way along the longest stretch."""
    boxed = box_wall(p, q) if p.square and q.square else None
    if p.square and q.square and (boxed is None or want_p is None and want_q is None):
        return boxed and boxed[:3]
    theirs = {(s.inner, s.side, round(s.point[0], 6), round(s.point[1], 6)) for s in q.allowed(want_q) if s.side}
    meet = [s for s in p.allowed(want_p) if s.side and (s.cell, TURNED[s.side], round(s.point[0], 6), round(s.point[1], 6)) in theirs
            and (boxed is None or s.side == boxed[0]
                 and boxed[3] + LATTICE / 2 - 1e-6 <= s.point[1 if s.side in "ew" else 0] <= boxed[4] - LATTICE / 2 + 1e-6)]
    if not meet:
        return None
    if want_p is None and want_q is None:
        runs: list[list[Slot]] = []
        for s in sorted(meet, key=lambda s: (s.side, s.point[1] if s.side in "ns" else s.point[0],
                                              s.point[0] if s.side in "ns" else s.point[1])):
            last = runs[-1][-1] if runs else None
            if last and last.side == s.side and math.dist(last.point, s.point) <= LATTICE + 1e-6 \
                    and (last.point[1] == s.point[1] if s.side in "ns" else last.point[0] == s.point[0]):
                runs[-1].append(s)
            else:
                runs.append([s])
        run = max(runs, key=len)
        door = ((run[0].point[0] + run[-1].point[0]) / 2, (run[0].point[1] + run[-1].point[1]) / 2)
        return run[0].side, TURNED[run[0].side], door
    qc = q.centre
    best = min(meet, key=lambda s: (off(s.bearing, want_p) if want_p is not None else 0)
               + (off(bearing(s.point[0] - qc[0], s.point[1] - qc[1]), want_q) if want_q is not None else 0))
    return best.side, TURNED[best.side], best.point


class Router:
    def __init__(self, rooms: dict[str, Footprint], seed: int = 1, margin: int = 2, ground: frozenset | None = None):
        """`ground`: the cells a passage may take, where the block bounds them."""
        self.rooms, self.seed, self.ground = rooms, seed, ground
        spans = [r.span for r in rooms.values()]
        self.lo = (min(s[0] for s in spans) - margin, min(s[1] for s in spans) - margin)
        self.hi = (max(s[2] for s in spans) + margin, max(s[3] for s in spans) + margin)
        self.solid: dict[tuple[int, int], str] = {}
        for code, r in rooms.items():
            for c in r.cells:
                self.solid[c] = code
        self.against: dict[tuple[int, int], set[str]] = {}      # the rooms whose wall a free cell lies against
        for (i, j), code in self.solid.items():
            for dx, dy in STEPS.values():
                if (i + dx, j + dy) not in self.solid:
                    self.against.setdefault((i + dx, j + dy), set()).add(code)
        for code, r in rooms.items():                           # and the cells a floor off the lattice reaches into
            for c in r.touched - r.cells:
                if c not in self.solid:
                    self.against.setdefault(c, set()).add(code)
        self.used: dict[tuple[int, int], set[int]] = {}         # cell -> the routes through it
        self.doors: set[tuple[str, tuple[int, int]]] = set()    # (room, cell) taken by a door
        self.routes: list[Route] = []
        self.ends: list[tuple[str, str]] = []

    # -- cells ---------------------------------------------------------------------------

    def noise(self, c) -> float:
        i, j = c[0] - self.lo[0], c[1] - self.lo[1]      # from the plan's own corner, so a shifted plan routes alike
        return ((i * 73856093 ^ j * 19349663 ^ self.seed * 83492791) % 1000) / 1000 * WANDER

    def doorway(self, room: str, want: float | None = None) -> list[Slot]:
        """The slots a door of `room` can open on: free, on the plan, and within its named wall."""
        return [s for s in self.rooms[room].allowed(want)
                if self.inside(s.cell) and s.cell not in self.solid and (room, s.cell) not in self.doors]

    def inside(self, c) -> bool:
        return self.lo[0] <= c[0] <= self.hi[0] and self.lo[1] <= c[1] <= self.hi[1]

    def related(self, i: int, j: int) -> bool:
        """Whether routes i and j leave a room in common, so may run together."""
        return bool(set(self.ends[i]) & set(self.ends[j]))

    def free(self, c, me: int) -> bool:
        if c in self.solid or not self.inside(c) or self.ground is not None and c not in self.ground:
            return False
        for d in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            for u in self.used.get((c[0] + d[0], c[1] + d[1]), ()):
                if not self.related(u, me):
                    return False
        return True

    def beside(self, c, n, me: int) -> bool:
        """Whether a step from cell c (None at a door) to cell n runs beside the passage of another
        way from the same room, rather than joining it or leaving it."""
        def touches(cell, u, but):
            return any(u in self.used.get((cell[0] + dx, cell[1] + dy), ()) for dx, dy in STEPS.values()
                       if (cell[0] + dx, cell[1] + dy) != but)
        near = {u for dx, dy in STEPS.values() for u in self.used.get((n[0] + dx, n[1] + dy), ())}
        return any(u not in self.used.get(n, ()) and touches(n, u, c)
                   and (c is None or u in self.used.get(c, ()) or touches(c, u, n)) for u in near if u != me)

    # -- one way -------------------------------------------------------------------------

    def add(self, a: str, b: str, want_a: float | None = None, want_b: float | None = None) -> Route | None:
        """Routes a to b, leaving each by its named wall where it names one, or returns None where
        no passage fits."""
        me = len(self.routes)
        self.ends.append((a, b))
        ra, rb = self.rooms[a], self.rooms[b]
        wall = shared_wall(ra, rb, want_a, want_b)
        if wall:
            p = wall[2]
            route = Route(a, b, "wall", wall[0], wall[1], p, p,
                          bearing_a=bearing(p[0] - ra.centre[0], p[1] - ra.centre[1]),
                          bearing_b=bearing(p[0] - rb.centre[0], p[1] - rb.centre[1]))
            route.length = self.measure(route)
            self.routes.append(route)
            return route
        path = self.search(a, b, me, want_a, want_b)
        if path is None:
            self.ends.pop()
            return None
        cells, sa, sb = path
        route = Route(a, b, "path", sa.side, sb.side, sa.point, sb.point, cells, bearing_a=sa.bearing, bearing_b=sb.bearing)
        route.length = self.measure(route)
        for c in cells:
            self.used.setdefault(c, set()).add(me)
        self.doors |= {(a, cells[0]), (b, cells[-1])}
        self.routes.append(route)
        return route

    def measure(self, route: Route) -> float:
        a, b = self.rooms[route.a], self.rooms[route.b]
        pts = [a.centre] + route.points() + [b.centre]
        return sum(math.dist(p, q) for p, q in zip(pts, pts[1:]))

    def search(self, a: str, b: str, me: int, want_a: float | None = None, want_b: float | None = None):
        goals: dict[tuple[int, int], Slot] = {}
        for s in self.doorway(b, want_b):
            goals.setdefault(s.cell, s)
        starts = self.doorway(a, want_a)
        if not goals or not starts:
            return None
        rb = self.rooms[b]
        tx, ty = rb.x / LATTICE + rb.w / LATTICE / 2, rb.y / LATTICE + rb.h / LATTICE / 2
        h = lambda c: abs(c[0] + 0.5 - tx) + abs(c[1] + 0.5 - ty) - (rb.w + rb.h) / LATTICE / 2
        tie = 0
        heap, best, back = [], {}, {}
        for slot in starts:
            c = slot.cell
            if self.free(c, me) and not self.beside(None, c, me) \
                    and self.against.get(c, set()) <= {a} | ({b} if c in goals else set()):
                state = (c, None, 0)
                cost = 1 + self.noise(c)
                if state in best and best[state] <= cost:
                    continue
                best[state] = cost
                back[state] = (None, slot)
                tie += 1
                heapq.heappush(heap, (cost + max(h(c), 0), tie, cost, state))
        while heap:
            _, _, cost, state = heapq.heappop(heap)
            if cost > best.get(state, 1e9) + 1e-9:
                continue
            c, d, run = state
            if c in goals:
                cells, st = [], state
                while st:
                    cells.append(st[0])
                    prev, first = back[st]
                    if prev is None:
                        entry = first
                    st = prev
                return cells[::-1], entry, goals[c]
            for nd, (dx, dy) in STEPS.items():
                n = (c[0] + dx, c[1] + dy)
                if d and nd == TURNED[d] or not self.free(n, me) or self.beside(c, n, me):
                    continue
                if self.against.get(n, set()) > ({b} if n in goals else set()):
                    continue                          # a floor laid against a wall but at a door would read as part of the room
                step = 1 + self.noise(n)
                if self.used.get(n):
                    step -= SHARE
                if d and nd != d:
                    step += TURN
                r = run + 1 if nd == d else 1
                if r > RUN:
                    step += RUN_COST
                ns = (n, nd, min(r, RUN + 1))
                nc = cost + step
                if nc < best.get(ns, 1e9) - 1e-9:
                    best[ns] = nc
                    back[ns] = (state, None)
                    tie += 1
                    heapq.heappush(heap, (nc + max(h(n), 0), tie, nc, ns))
        return None


def number(code: str) -> int:
    return int(code.split(".")[1])


def detours(routes: list[Route], rooms: dict[str, Footprint], limit: float | None) -> list[tuple[Route, float]]:
    """Each way that walks more than `limit` feet beyond the straight line between its rooms'
    centres, with how far beyond."""
    out = [(r, r.length - math.dist(rooms[r.a].centre, rooms[r.b].centre)) for r in routes]
    return [(r, extra) for r, extra in out if limit is not None and extra > limit]


def plan(rooms: dict[str, Footprint], ways, walls: dict | None = None,
         ground: frozenset | None = None) -> tuple[list[Route], list[str]]:
    """Each way, as a pair of room codes in either order, routed shortest first, each end by the
    wall `walls` names for it as (room, far room) -> bearing, and through `ground` where the
    block bounds its passages: the routes, and the ways no passage fitted."""
    walls = walls or {}
    pairs = sorted({tuple(sorted(w, key=number)) for w in ways},
                   key=lambda w: (round(math.dist((rooms[w[0]].x, rooms[w[0]].y), (rooms[w[1]].x, rooms[w[1]].y))), w))
    router = Router(rooms, SEED, ground=ground)
    left = [f"{a} to {b}" for a, b in pairs if router.add(a, b, walls.get((a, b)), walls.get((b, a))) is None]
    return router.routes, left
