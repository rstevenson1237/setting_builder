"""Packs a DANGEROUS block's rooms close into a square, with room between them for passages.

A room is a footprint of its Dressing's width and length whose box's corners lie on
route.LATTICE; two rooms overlap where their floors reach into one lattice cell. Rooms joined
by a way sit near one another, touching where a door through the shared wall will do and a
passage apart where it will not; rooms not joined may touch too, their shared
wall drawn by the map's `sharedWalls`. A room placed against another is carried with it, never
moved alone. The packing is annealed, so a seed fixes it, and is kept only where route.Router
fits a passage for every way.
"""
from __future__ import annotations

import math
import random
import zlib
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

import route

GRID = route.LATTICE        # feet a room's corner moves by
DOOR = 10                   # feet of wall facing wall that a straight lane needs
STEPS = 60000
FAR = 120                   # feet between joined rooms past which the packing is penalised
OVER, CORNER, STRAIGHT, ROUND, CLOSE, PULL, REPAIR, LABELS, PIN = 40.0, 1.0, 1.0, 3.0, 1.0, 0.00004, 6.0, 8.0, 2.0
LABEL_H = 15.0              # feet a room's number and code take, stacked at its centre
NAME_H = 7.0                # and a hall's code alone
REPAIRS, REPAIR_STEPS = 8, 20000    # rounds of re-annealing for the ways that found no passage


@dataclass
class Room:
    code: str
    w: int
    h: int
    shape: str = "rect"         # one of route.SHAPES
    points: tuple | None = None  # a poly's outline, feet east and south of its centre
    hall: bool = False          # shows its code alone, so its label is shorter

    @property
    def round(self) -> bool:
        return self.shape == "round"


def compass_vector(bearing: float) -> tuple[float, float]:
    """East and south components of a compass angle in degrees, clockwise from north."""
    a = math.radians(bearing)
    return math.sin(a), -math.cos(a)


class Packer:
    def __init__(self, rooms: list[Room], ways: list[tuple[str, str, float | None]], side: int, seed: int,
                 passages: float, pins: dict[str, tuple[float, float, float, float]],
                 glue: dict[str, tuple[str, float, float]] | None = None):
        """`ways` are (room, room, compass bearing to keep or None); `passages` the share of ways run
        as passages; `pins` each room to stand over another, as its (east, north, width, length)
        from the square's centre; `glue` each room placed against another, as (that room, feet
        east, feet south of it)."""
        self.rooms, self.side = rooms, side
        self.ix = {r.code: i for i, r in enumerate(rooms)}
        self.w = [r.w for r in rooms]
        self.h = [r.h for r in rooms]
        self.round = [r.round for r in rooms]
        fps = [route.Footprint(0, 0, r.w, r.h, r.shape, r.points) for r in rooms]
        self.floor = [f.touched for f in fps]           # the cells its floor reaches, from its box's corner
        self.boxed = [f.square for f in fps]
        self.edges: dict[tuple[int, int], tuple[float, float] | None] = {}  # i < j: unit vector from i to j to keep, if any
        for a, b, bearing in ways:
            i, j = self.ix[a], self.ix[b]
            v = compass_vector(bearing) if bearing is not None else None
            if i > j and v:
                v = (-v[0], -v[1])
            if i > j:
                i, j = j, i
            self.edges[(i, j)] = v
        self.passage = {k for k in self.edges if zlib.crc32(f"{rooms[k[0]].code}-{rooms[k[1]].code}".encode()) % 100 < passages * 100}
        self.pins = {self.ix[c]: (side / 2 + e, side / 2 - n, w, h) for c, (e, n, w, h) in pins.items() if c in self.ix}
        self.near = [[j for j in range(len(rooms)) if (min(i, j), max(i, j)) in self.edges] for i in range(len(rooms))]
        self.trouble: dict[tuple[int, int], str] = {}   # ways no passage fitted, and how to give them room
        self.rng = random.Random(seed)
        self.x = [0.0] * len(rooms)
        self.y = [0.0] * len(rooms)
        self.glue = {self.ix[c]: (self.ix[a], dx, dy) for c, (a, dx, dy) in (glue or {}).items()}
        self.free = [i for i in range(len(rooms)) if i not in self.glue]
        self.carrying = {j for j, _, _ in self.glue.values()}

    def follow(self):
        """Each room placed against another, carried to its place by it; a chain settles in as many rounds as it is long."""
        for _ in range(len(self.glue)):
            for i, (j, dx, dy) in self.glue.items():
                self.x[i], self.y[i] = self.x[j] + dx, self.y[j] + dy

    # -- geometry ------------------------------------------------------------------------

    def snap(self, i: int, x: float, y: float) -> tuple[float, float]:
        """The centre nearest (x, y) at which room i's corners lie on the lattice."""
        return (round((x - self.w[i] / 2) / GRID) * GRID + self.w[i] / 2,
                round((y - self.h[i] / 2) / GRID) * GRID + self.h[i] / 2)

    def box(self, i, x=None, y=None):
        x = self.x[i] if x is None else x
        y = self.y[i] if y is None else y
        return x - self.w[i] / 2, y - self.h[i] / 2, x + self.w[i] / 2, y + self.h[i] / 2

    def gaps(self, i, j, xi=None, yi=None):
        a, b = self.box(i, xi, yi), self.box(j)
        return max(b[0] - a[2], a[0] - b[2]), max(b[1] - a[3], a[1] - b[3])

    def face(self, i, j, xi=None, yi=None):
        """How i and j face: (axis, gap) where they see one another straight across `gap` feet
        along `axis` and share a door's width of wall, else None."""
        a, b = self.box(i, xi, yi), self.box(j)
        sx, sy = max(b[0] - a[2], a[0] - b[2]), max(b[1] - a[3], a[1] - b[3])
        best = None
        if sx >= 0 and min(a[3], b[3]) - max(a[1], b[1]) >= DOOR:
            best = ("x", sx)
        if sy >= 0 and min(a[2], b[2]) - max(a[0], b[0]) >= DOOR and (best is None or sy < best[1]):
            best = ("y", sy)
        return best

    # -- energy --------------------------------------------------------------------------

    def shared(self, i, j, xi=None, yi=None) -> int:
        """How many lattice cells both rooms' floors reach into."""
        a, b = self.box(i, xi, yi), self.box(j)
        di, dj = round((b[0] - a[0]) / GRID), round((b[1] - a[1]) / GRID)
        theirs = self.floor[j]
        return sum((u - di, v - dj) in theirs for u, v in self.floor[i])

    def pair(self, i, j, xi=None, yi=None) -> float:
        a, b = self.box(i, xi, yi), self.box(j)
        sx, sy = max(b[0] - a[2], a[0] - b[2]), max(b[1] - a[3], a[1] - b[3])
        if sx < 0 and sy < 0:
            if self.boxed[i] and self.boxed[j]:
                return OVER * (1 + min(-sx, -sy) / GRID)
            if n := self.shared(i, j, xi, yi):
                return OVER * (1 + math.sqrt(n))
        lw = 5 * (0.8 * (len(self.rooms[i].code) + len(self.rooms[j].code)) / 2 + 1)          # their labels, side by side
        lh = sum(NAME_H if self.rooms[k].hall else LABEL_H for k in (i, j)) / 2
        if abs((self.x[j]) - (self.x[i] if xi is None else xi)) < lw and abs(self.y[j] - (self.y[i] if yi is None else yi)) < lh:
            return LABELS + self.pair_cost(i, j, sx, sy, xi, yi)
        return self.pair_cost(i, j, sx, sy, xi, yi)

    def pair_cost(self, i, j, sx, sy, xi=None, yi=None) -> float:
        joined = (min(i, j), max(i, j)) in self.edges
        if not joined:
            return 0.0
        gap = max(sx, sy, 0)
        f = self.face(i, j, xi, yi)
        if (min(i, j), max(i, j)) in self.passage:       # a passage: apart, and bending where it can
            e = CLOSE if gap < 2 * GRID else 0.0
            e += STRAIGHT if f and gap > 0 else 0.0
            e += math.hypot(max(sx, 0), max(sy, 0)) / 60
        else:                                            # a door through the shared wall
            e = gap / 80 if f else CORNER + gap / 80 + math.hypot(max(sx, 0), max(sy, 0)) / 60
        if (self.round[i] or self.round[j]) and gap < GRID:
            e += ROUND
        if gap > FAR:
            e += 3 * (gap - FAR) / GRID
        if want := self.edges[(min(i, j), max(i, j))]:
            dx = (self.x[j] - (self.x[i] if xi is None else xi)) * (1 if i < j else -1)
            dy = (self.y[j] - (self.y[i] if yi is None else yi)) * (1 if i < j else -1)
            e += 1.2 * (1 - (dx * want[0] + dy * want[1]) / (math.hypot(dx, dy) or 1))
        mode = self.trouble.get((min(i, j), max(i, j)))
        if mode == "door" and not (f and gap == 0) or mode == "lane" and not (f and 2 * GRID <= gap <= 4 * GRID):
            e += REPAIR
        return e

    def inside(self, i, x=None, y=None) -> float:
        a = self.box(i, x, y)
        e = 0.0
        for lo, hi in ((a[0], a[2]), (a[1], a[3])):
            if lo < 0:
                e += OVER * (-lo / GRID + 1)
            if hi > self.side:
                e += OVER * ((hi - self.side) / GRID + 1)
        return e

    def pin(self, i, x=None, y=None) -> float:
        """How far room i stands from the room it is pinned over, if any."""
        if i not in self.pins:
            return 0.0
        tx, ty, _, _ = self.pins[i]
        return PIN * math.hypot((self.x[i] if x is None else x) - tx, (self.y[i] if y is None else y) - ty) / GRID

    def over(self) -> bool:
        """Whether every pinned room overlaps, in plan, the room it is pinned over."""
        return all(abs(self.x[i] - tx) < (self.w[i] + w) / 2 and abs(self.y[i] - ty) < (self.h[i] + h) / 2
                   for i, (tx, ty, w, h) in self.pins.items())

    def local(self, i, x=None, y=None) -> float:
        cx, cy = (self.x[i] if x is None else x) - self.side / 2, (self.y[i] if y is None else y) - self.side / 2
        return self.inside(i, x, y) + self.pin(i, x, y) + PULL * (cx * cx + cy * cy) / GRID ** 2 * 100 \
            + sum(self.pair(i, j, x, y) for j in range(len(self.w)) if j != i)

    def total(self) -> float:
        n = len(self.w)
        return sum(self.inside(i) + self.pin(i) + PULL * 100 * ((self.x[i] - self.side / 2) ** 2 + (self.y[i] - self.side / 2) ** 2) / GRID ** 2
                   for i in range(n)) + sum(self.pair(i, j) for i in range(n) for j in range(i + 1, n))

    # -- search --------------------------------------------------------------------------

    def place(self):
        """Rooms in order of the ways, each against the one before it."""
        n, rng = len(self.w), self.rng
        order = [0]
        for i in order:
            order += [j for j in self.near[i] if j not in order]
        order += [i for i in range(n) if i not in order]
        self.x[order[0]], self.y[order[0]] = self.snap(order[0], self.side / 2, self.side / 2)
        for k, i in enumerate(order[1:], 1):
            anchors = [j for j in self.near[i] if j in order[:k]] or order[:k]
            self.x[i], self.y[i] = self.against(i, rng.choice(anchors))
        self.follow()

    def against(self, i, j):
        """A spot for room i against room j, on a side and at an offset chosen at random."""
        rng = self.rng
        side = rng.choice("nesw")
        gap = rng.choice((0, 0, GRID, 2 * GRID))
        sign = -1 if side in "nw" else 1
        slide = lambda a, b: max(0, (a + b) // 2 - DOOR)  # how far it may slide along j and still share a door's width
        if side in "ns":
            y = self.y[j] + sign * ((self.h[j] + self.h[i]) / 2 + gap)
            x = self.x[j] + rng.randint(-slide(self.w[j], self.w[i]), slide(self.w[j], self.w[i]))
        else:
            x = self.x[j] + sign * ((self.w[j] + self.w[i]) / 2 + gap)
            y = self.y[j] + rng.randint(-slide(self.h[j], self.h[i]), slide(self.h[j], self.h[i]))
        return self.snap(i, x, y)

    def anneal(self, steps: int = STEPS, t0: float = 3.0, again: bool = False):
        rng, n = self.rng, len(self.w)
        if not again:
            self.place()
        cur = self.total()
        best, best_at = cur, (self.x[:], self.y[:])
        t1 = 0.04
        for s in range(steps):
            t = t0 * (t1 / t0) ** (s / steps)
            i = rng.choice(self.free) if self.glue else rng.randrange(n)
            r = rng.random()
            if r < 0.55:
                reach = max(GRID, int(50 * (1 - s / steps)))
                nx, ny = self.snap(i, self.x[i] + rng.randint(-reach, reach), self.y[i] + rng.randint(-reach, reach))
            elif r < 0.9 and self.near[i]:
                nx, ny = self.against(i, rng.choice(self.near[i]))
            else:
                j = rng.randrange(n)
                if j == i or self.glue and {i, j} & (set(self.glue) | self.carrying):
                    continue
                before = self.local(i) + self.local(j) - self.pair(i, j)
                old = (self.x[i], self.y[i], self.x[j], self.y[j])
                self.x[i], self.y[i] = self.snap(i, old[2], old[3])
                self.x[j], self.y[j] = self.snap(j, old[0], old[1])
                after = self.local(i) + self.local(j) - self.pair(i, j)
                if after - before <= 0 or rng.random() < math.exp(-(after - before) / t):
                    cur += after - before
                else:
                    self.x[i], self.y[i], self.x[j], self.y[j] = old
                continue
            if i in self.carrying:                       # it moves the rooms placed against it
                old = (self.x[:], self.y[:])
                before = self.total()
                self.x[i], self.y[i] = nx, ny
                self.follow()
                after = self.total()
                if after - before <= 0 or rng.random() < math.exp(-(after - before) / t):
                    cur += after - before
                else:
                    self.x, self.y = old
            else:
                before, after = self.local(i), self.local(i, nx, ny)
                if after - before <= 0 or rng.random() < math.exp(-(after - before) / t):
                    self.x[i], self.y[i] = nx, ny
                    cur += after - before
            if cur < best - 1e-9:
                best, best_at = cur, (self.x[:], self.y[:])
        self.x, self.y = best_at[0][:], best_at[1][:]
        return self.total()

    def clear(self) -> bool:
        """Whether no two rooms overlap and every room lies in the square."""
        n = len(self.w)
        return all(self.inside(i) == 0 for i in range(n)) and \
            all(max(self.gaps(i, j)) >= 0 or not (self.boxed[i] and self.boxed[j]) and not self.shared(i, j)
                for i in range(n) for j in range(i + 1, n))

    def rects(self) -> dict[str, route.Footprint]:
        return {r.code: route.Footprint(self.x[i] - self.w[i] / 2, self.y[i] - self.h[i] / 2, self.w[i], self.h[i],
                                        r.shape, r.points) for i, r in enumerate(self.rooms)}


def squares(rooms: list[Room], fill: tuple[float, float]) -> list[int]:
    """Sides to try, in feet, from where the rooms cover the most of the square `fill` allows to
    where they cover the least."""
    area = sum(r.w * r.h for r in rooms)
    base = max(math.ceil(math.sqrt(area / fill[1]) / GRID) * GRID, max(max(r.w, r.h) for r in rooms) + 2 * GRID)
    return list(range(base, max(base, math.floor(math.sqrt(area / fill[0]) / GRID) * GRID) + 1, GRID))


def attempt(args):
    """One packing from one seed, re-annealed round the ways that found no passage until every way has one."""
    rooms, ways, side, seed, passages, pins, glue, walls = args
    p = Packer(rooms, ways, side, seed, passages, pins, glue)
    p.anneal()
    pairs = [(a, b) for a, b, _ in ways]
    for _ in range(REPAIRS):
        found, left = route.plan(p.rects(), pairs, walls)
        if not left and p.clear() and p.over():
            return True, p.total(), p.x, p.y
        for name in left:
            a, b = (p.ix[c] for c in name.split(" to "))
            key = (min(a, b), max(a, b))
            hard = p.round[a] or p.round[b] or p.trouble.get(key) == "door"
            p.trouble[key] = "lane" if hard else "door"
        p.anneal(REPAIR_STEPS, 1.0, again=True)
    return False, p.total(), p.x, p.y


def pack(rooms, ways, seed: int, fill: tuple[float, float], passages: float, footprint: int | None = None,
         pins: dict | None = None, tries: int = 12, glue: dict | None = None, walls: dict | None = None):
    """The lowest-energy packing, over a few seeds at each side in turn - `footprint` alone where
    it is given - stopping at the first side where some seed leaves every way a passage, each by
    the wall `walls` names, and every pinned room over its pin: (side, packer, routes, energy),
    routes None where no side did."""
    pairs, pins = [(a, b) for a, b, _ in ways], pins or {}
    side = footprint
    with ProcessPoolExecutor() as pool:
        for side in [footprint] if footprint else squares(rooms, fill):
            runs = [r for r in pool.map(attempt, [(rooms, ways, side, seed * 1000 + k, passages, pins, glue, walls)
                                                  for k in range(tries)]) if r[0]]
            if runs:
                ok, e, x, y = min(runs, key=lambda r: r[1])
                p = Packer(rooms, ways, side, seed, passages, pins, glue)
                p.x, p.y = x, y
                return side, p, route.plan(p.rects(), pairs, walls)[0], e
    return side, None, None, 0.0
