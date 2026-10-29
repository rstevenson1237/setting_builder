"""Corridors for a packed block: each way a winding passage from one room's wall to another's.

Rooms are rectangles whose corners lie on a LATTICE-foot grid. A passage is a path of lattice
cells from a cell against one room's wall to a cell against the other's, bending where it
likes, never touching another way's passage but where the two leave one room, and never
running through a room. A door stands on the wall between the room and the path's first cell.
"""
from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field

SEED = 1                    # the noise every plan is routed with, so a draw finds the passages a pack did
LATTICE = 10                # feet, a passage's width and the grid rooms and passages lie on
TURN = 0.5                  # what a bend costs, in cells of path
RUN = 4                     # cells a passage runs straight before each further cell costs
RUN_COST = 0.2
SHARE = 0.4                 # taken off a cell another way from the same room already uses
WANDER = 0.45               # the most a cell's noise adds, so equal routes differ
STEPS = {"n": (0, -1), "e": (1, 0), "s": (0, 1), "w": (-1, 0)}
TURNED = {"n": "s", "s": "n", "e": "w", "w": "e"}


@dataclass
class Rect:
    x: float                # feet east and south of the plan's origin, top left
    y: float
    w: float
    h: float
    round: bool = False

    @property
    def cells(self) -> tuple[int, int, int, int]:
        """First and last lattice column and row the room covers."""
        return (math.floor(self.x / LATTICE + 1e-6), math.floor(self.y / LATTICE + 1e-6),
                math.ceil((self.x + self.w) / LATTICE - 1e-6) - 1, math.ceil((self.y + self.h) / LATTICE - 1e-6) - 1)


@dataclass
class Route:
    a: str
    b: str
    side_a: str = ""
    side_b: str = ""
    door_a: tuple[float, float] = (0.0, 0.0)        # on the wall, in feet
    door_b: tuple[float, float] = (0.0, 0.0)
    cells: list[tuple[int, int]] = field(default_factory=list)
    length: float = 0.0                             # feet from one room's centre to the other's, by the way

    def points(self) -> list[tuple[float, float]]:
        """The way's corners from door to door, in feet."""
        pts = [self.door_a] + [((i + 0.5) * LATTICE, (j + 0.5) * LATTICE) for i, j in self.cells] + [self.door_b]
        keep = [pts[0]]
        for p, q, r in zip(pts, pts[1:], pts[2:]):
            if (q[0] - p[0]) * (r[1] - q[1]) != (q[1] - p[1]) * (r[0] - q[0]):
                keep.append(q)
        return keep + [pts[-1]]


class Router:
    def __init__(self, rooms: dict[str, Rect], seed: int = 1, margin: int = 2):
        self.rooms, self.seed = rooms, seed
        spans = [r.cells for r in rooms.values()]
        self.lo = (min(s[0] for s in spans) - margin, min(s[1] for s in spans) - margin)
        self.hi = (max(s[2] for s in spans) + margin, max(s[3] for s in spans) + margin)
        self.solid: dict[tuple[int, int], str] = {}
        for code, r in rooms.items():
            i0, j0, i1, j1 = r.cells
            for i in range(i0, i1 + 1):
                for j in range(j0, j1 + 1):
                    self.solid[i, j] = code
        self.against: dict[tuple[int, int], set[str]] = {}      # the rooms whose wall a free cell lies against
        for (i, j), code in self.solid.items():
            for dx, dy in STEPS.values():
                if (i + dx, j + dy) not in self.solid:
                    self.against.setdefault((i + dx, j + dy), set()).add(code)
        self.used: dict[tuple[int, int], set[int]] = {}         # cell -> the routes through it
        self.doors: set[tuple[str, tuple[int, int]]] = set()    # (room, cell) taken by a door
        self.routes: list[Route] = []
        self.ends: list[tuple[str, str]] = []

    # -- cells ---------------------------------------------------------------------------

    def noise(self, c) -> float:
        i, j = c[0] - self.lo[0], c[1] - self.lo[1]      # from the plan's own corner, so a shifted plan routes alike
        return ((i * 73856093 ^ j * 19349663 ^ self.seed * 83492791) % 1000) / 1000 * WANDER

    def doorway(self, room: str) -> list[tuple[tuple[int, int], str]]:
        """The cells a door of `room` can open on, each with the side of the room it is on."""
        r = self.rooms[room]
        i0, j0, i1, j1 = r.cells
        cx, cy = r.x + r.w / 2, r.y + r.h / 2
        out = []
        for i in range(i0, i1 + 1):
            if not r.round or abs((i + 0.5) * LATTICE - cx) <= LATTICE / 2 + 1e-6:
                out += [((i, j0 - 1), "n"), ((i, j1 + 1), "s")]
        for j in range(j0, j1 + 1):
            if not r.round or abs((j + 0.5) * LATTICE - cy) <= LATTICE / 2 + 1e-6:
                out += [((i0 - 1, j), "w"), ((i1 + 1, j), "e")]
        return [(c, s) for c, s in out if self.inside(c) and c not in self.solid]

    def inside(self, c) -> bool:
        return self.lo[0] <= c[0] <= self.hi[0] and self.lo[1] <= c[1] <= self.hi[1]

    def related(self, i: int, j: int) -> bool:
        """Whether routes i and j leave a room in common, so may run together."""
        return bool(set(self.ends[i]) & set(self.ends[j]))

    def free(self, c, me: int) -> bool:
        if c in self.solid or not self.inside(c):
            return False
        for d in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            for u in self.used.get((c[0] + d[0], c[1] + d[1]), ()):
                if not self.related(u, me):
                    return False
        return True

    # -- one way -------------------------------------------------------------------------

    def add(self, a: str, b: str) -> Route | None:
        """Routes a to b, or returns None where no passage fits."""
        me = len(self.routes)
        self.ends.append((a, b))
        path = self.search(a, b, me)
        if path is None:
            self.ends.pop()
            return None
        cells, sa, sb = path
        route = Route(a, b, sa, sb, self.door(a, cells[0], sa), self.door(b, cells[-1], sb), cells)
        route.length = self.measure(route)
        for c in cells:
            self.used.setdefault(c, set()).add(me)
        self.doors |= {(a, cells[0]), (b, cells[-1])}
        self.routes.append(route)
        return route

    def door(self, room: str, cell, side: str) -> tuple[float, float]:
        r = self.rooms[room]
        x, y = (cell[0] + 0.5) * LATTICE, (cell[1] + 0.5) * LATTICE
        return {"n": (x, r.y), "s": (x, r.y + r.h), "w": (r.x, y), "e": (r.x + r.w, y)}[side]

    def measure(self, route: Route) -> float:
        a, b = self.rooms[route.a], self.rooms[route.b]
        pts = [(a.x + a.w / 2, a.y + a.h / 2)] + route.points() + [(b.x + b.w / 2, b.y + b.h / 2)]
        return sum(math.dist(p, q) for p, q in zip(pts, pts[1:]))

    def search(self, a: str, b: str, me: int):
        goals = {c: s for c, s in self.doorway(b) if (b, c) not in self.doors}
        starts = [(c, s) for c, s in self.doorway(a) if (a, c) not in self.doors]
        if not goals or not starts:
            return None
        rb = self.rooms[b]
        tx, ty = rb.x / LATTICE + rb.w / LATTICE / 2, rb.y / LATTICE + rb.h / LATTICE / 2
        h = lambda c: abs(c[0] + 0.5 - tx) + abs(c[1] + 0.5 - ty) - (rb.w + rb.h) / LATTICE / 2
        tie = 0
        heap, best, back = [], {}, {}
        for c, side in starts:
            if self.free(c, me) and self.against.get(c, set()) <= {a} | ({b} if c in goals else set()):
                state = (c, None, 0)
                cost = 1 + self.noise(c)
                best[state] = cost
                back[state] = (None, side)
                tie += 1
                heapq.heappush(heap, (cost + max(h(c), 0), tie, cost, state))
        while heap:
            _, _, cost, state = heapq.heappop(heap)
            if cost > best.get(state, 1e9) + 1e-9:
                continue
            c, d, run = state
            if c in goals:
                cells, st, side = [], state, goals[c]
                while st:
                    cells.append(st[0])
                    prev, first = back[st]
                    if prev is None:
                        entry = first
                    st = prev
                return cells[::-1], entry, side
            for nd, (dx, dy) in STEPS.items():
                n = (c[0] + dx, c[1] + dy)
                if d and nd == TURNED[d] or not self.free(n, me):
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


def plan(rooms: dict[str, Rect], ways) -> tuple[list[Route], list[str]]:
    """Each way, as a pair of room codes in either order, routed shortest first: the routes,
    and the ways no passage fitted."""
    pairs = sorted({tuple(sorted(w, key=number)) for w in ways},
                   key=lambda w: (round(math.dist((rooms[w[0]].x, rooms[w[0]].y), (rooms[w[1]].x, rooms[w[1]].y))), w))
    router = Router(rooms, SEED)
    left = [f"{a} to {b}" for a, b in pairs if router.add(a, b) is None]
    return router.routes, left
