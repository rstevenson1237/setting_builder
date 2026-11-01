"""Packs a DANGEROUS block's rooms close into a square, with room between them for passages.

A room is a footprint of its Dressing's width and length whose box's corners lie on
route.LATTICE; two rooms overlap where their floors reach into one lattice cell. Rooms joined
by a way sit near one another, touching where a door through the shared wall will do and a
passage apart where it will not; rooms not joined may touch too, their shared
wall drawn by the map's `sharedWalls`. A room placed against another is carried with it, never
moved alone. A room that turns may lie in any quarter turn or mirror of itself, and a room may
be set into the corners another's floor leaves empty, where touching floors earn their contact.
Where the block gives its ground - an outline of its own, or rock no room may take - every
room's floor lies on it.
The packing is annealed, so a seed fixes it, and is kept only where route.Router fits a passage
for every way.
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
CONTACT = 0.25              # taken off for each lattice cell's edge two floors share, where either is no box
TURN, NEST = 0.06, 0.06     # the share of moves that turn a room, and that set one into another's empty corners
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
    turns: bool = False         # may lie in any quarter turn or mirror of itself

    @property
    def round(self) -> bool:
        return self.shape == "round"

    def forms(self) -> list[tuple[int, int, tuple | None]]:
        """Each way the room may lie, as (width, length, points), as drawn first; each differs."""
        out, seen = [], set()
        for k in range(4 if self.turns else 1):
            for mirror in (False, True) if self.turns else (False,):
                pts = self.points
                if pts:
                    pts = tuple((-x, y) for x, y in pts) if mirror else pts
                    for _ in range(k):
                        pts = tuple((-y, x) for x, y in pts)
                w, h = (self.w, self.h) if k % 2 == 0 else (self.h, self.w)
                key = (w, h, frozenset((round(x, 6), round(y, 6)) for x, y in pts) if pts else None)
                if key not in seen:
                    seen.add(key)
                    out.append((w, h, pts))
        return out


def compass_vector(bearing: float) -> tuple[float, float]:
    """East and south components of a compass angle in degrees, clockwise from north."""
    a = math.radians(bearing)
    return math.sin(a), -math.cos(a)


class Packer:
    def __init__(self, rooms: list[Room], ways: list[tuple[str, str, float | None]], side: int, seed: int,
                 passages: float, pins: dict[str, tuple[float, float, float, float]],
                 glue: dict[str, tuple[str, float, float]] | None = None, ground: frozenset | None = None):
        """`ways` are (room, room, compass bearing to keep or None); `passages` the share of ways run
        as passages; `pins` each room to stand over another, as its (east, north, width, length)
        from the square's centre; `glue` each room placed against another, as (that room, feet
        east, feet south of it); `ground` the lattice cells of the square its rooms may take, where
        not all of them."""
        self.rooms, self.side, self.ground = rooms, side, ground
        self.ix = {r.code: i for i, r in enumerate(rooms)}
        self.round = [r.round for r in rooms]
        self.lies = []                                  # each room's forms, as (width, length, points, floor, holes)
        for r in rooms:
            forms = []
            for w, h, pts in r.forms():
                f = route.Footprint(0, 0, w, h, r.shape, pts)
                i0, j0, i1, j1 = f.span
                holes = [(i, j) for i in range(i0, i1 + 1) for j in range(j0, j1 + 1) if (i, j) not in f.touched]
                forms.append((w, h, pts, f.touched, holes))
            self.lies.append(forms)
        self.boxed = [route.Footprint(0, 0, r.w, r.h, r.shape, r.points).square for r in rooms]
        n = len(rooms)
        self.o, self.w, self.h, self.pts, self.floor = [0] * n, [0] * n, [0] * n, [None] * n, [None] * n
        for i in range(len(rooms)):
            self.lie(i, 0)
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
        self.turners = [i for i in self.free if len(self.lies[i]) > 1 and i not in self.carrying]
        self.notched = [j for j in range(len(rooms)) if any(f[4] for f in self.lies[j])]

    def lie(self, i: int, k: int):
        """Room i laid in its k-th form."""
        self.o[i] = k
        self.w[i], self.h[i], self.pts[i], self.floor[i], _ = self.lies[i][k]

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

    def contact(self, i, j, xi=None, yi=None) -> int:
        """How many lattice cells' edges the two rooms' floors share."""
        a, b = self.box(i, xi, yi), self.box(j)
        di, dj = round((b[0] - a[0]) / GRID), round((b[1] - a[1]) / GRID)
        theirs = self.floor[j]
        return sum((u + dx - di, v + dy - dj) in theirs for u, v in self.floor[i] for dx, dy in route.STEPS.values())

    def pair(self, i, j, xi=None, yi=None) -> float:
        a, b = self.box(i, xi, yi), self.box(j)
        sx, sy = max(b[0] - a[2], a[0] - b[2]), max(b[1] - a[3], a[1] - b[3])
        if sx < 0 and sy < 0:
            if self.boxed[i] and self.boxed[j]:
                return OVER * (1 + min(-sx, -sy) / GRID)
            if n := self.shared(i, j, xi, yi):
                return OVER * (1 + math.sqrt(n))
        touching = self.contact(i, j, xi, yi) if sx <= 0 and sy <= 0 and not (self.boxed[i] and self.boxed[j]) else 0
        lw = 5 * (0.8 * (len(self.rooms[i].code) + len(self.rooms[j].code)) / 2 + 1)          # their labels, side by side
        lh = sum(NAME_H if self.rooms[k].hall else LABEL_H for k in (i, j)) / 2
        e = -CONTACT * touching + self.pair_cost(i, j, sx, sy, xi, yi, touching)
        if abs((self.x[j]) - (self.x[i] if xi is None else xi)) < lw and abs(self.y[j] - (self.y[i] if yi is None else yi)) < lh:
            return LABELS + e
        return e

    def pair_cost(self, i, j, sx, sy, xi=None, yi=None, touching=0) -> float:
        joined = (min(i, j), max(i, j)) in self.edges
        if not joined:
            return 0.0
        gap = max(sx, sy, 0)
        f = self.face(i, j, xi, yi) or touching and ("set in", 0)
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
        if self.ground is not None:                     # its floor on the block's ground
            di, dj = round(a[0] / GRID), round(a[1] / GRID)
            e += OVER * sum((u + di, v + dj) not in self.ground for u, v in self.floor[i])
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
        best, best_at = cur, (self.x[:], self.y[:], self.o[:])
        t1 = 0.04
        for s in range(steps):
            t = t0 * (t1 / t0) ** (s / steps)
            if self.turners and rng.random() < TURN:     # a room turned or mirrored where it stands
                i = rng.choice(self.turners)
                old = (self.o[i], self.x[i], self.y[i])
                before = self.local(i)
                self.lie(i, rng.choice([k for k in range(len(self.lies[i])) if k != old[0]]))
                self.x[i], self.y[i] = self.snap(i, old[1], old[2])
                after = self.local(i)
                if after - before <= 0 or rng.random() < math.exp(-(after - before) / t):
                    cur += after - before
                    if cur < best - 1e-9:
                        best, best_at = cur, (self.x[:], self.y[:], self.o[:])
                else:
                    self.lie(i, old[0])
                    self.x[i], self.y[i] = old[1], old[2]
                continue
            i = rng.choice(self.free) if self.glue else rng.randrange(n)
            if self.notched and rng.random() < NEST:      # set into a corner another room's floor leaves empty
                j = rng.choice(self.notched)
                holes = self.lies[j][self.o[j]][4]
                if j == i or i in self.carrying or not holes:
                    continue
                hi, hj = rng.choice(holes)
                ci, cj = rng.randrange(max(1, round(self.w[i] / GRID))), rng.randrange(max(1, round(self.h[i] / GRID)))
                nx, ny = self.snap(i, self.x[j] - self.w[j] / 2 + (hi - ci) * GRID + self.w[i] / 2,
                                   self.y[j] - self.h[j] / 2 + (hj - cj) * GRID + self.h[i] / 2)
                r = 1.0
            else:
                r = rng.random()
            if r < 0.55:
                reach = max(GRID, int(50 * (1 - s / steps)))
                nx, ny = self.snap(i, self.x[i] + rng.randint(-reach, reach), self.y[i] + rng.randint(-reach, reach))
            elif r < 0.9 and self.near[i]:
                nx, ny = self.against(i, rng.choice(self.near[i]))
            elif r < 1.0:
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
                best, best_at = cur, (self.x[:], self.y[:], self.o[:])
        self.x, self.y = best_at[0][:], best_at[1][:]
        for i, k in enumerate(best_at[2]):
            self.lie(i, k)
        return self.total()

    def clear(self) -> bool:
        """Whether no two rooms overlap and every room lies in the square."""
        n = len(self.w)
        return all(self.inside(i) == 0 for i in range(n)) and \
            all(max(self.gaps(i, j)) >= 0 or not (self.boxed[i] and self.boxed[j]) and not self.shared(i, j)
                for i in range(n) for j in range(i + 1, n))

    def rects(self) -> dict[str, route.Footprint]:
        return {r.code: route.Footprint(self.x[i] - self.w[i] / 2, self.y[i] - self.h[i] / 2, self.w[i], self.h[i],
                                        r.shape, self.pts[i]) for i, r in enumerate(self.rooms)}


def squares(rooms: list[Room], fill: tuple[float, float]) -> list[int]:
    """Sides to try, in feet, from where the rooms cover the most of the square `fill` allows to
    where they cover the least."""
    area = sum(r.w * r.h for r in rooms)
    base = max(math.ceil(math.sqrt(area / fill[1]) / GRID) * GRID, max(max(r.w, r.h) for r in rooms) + 2 * GRID)
    return list(range(base, max(base, math.floor(math.sqrt(area / fill[0]) / GRID) * GRID) + 1, GRID))


def attempt(args):
    """One packing from one seed, re-annealed round the ways that found no passage or walk more than
    `detour` out of their way, until none do: whether every way found one, how the best that did
    reads - its ways over `detour`, then the feet they all walk - and its energy and rooms' places."""
    rooms, ways, side, seed, passages, pins, glue, walls, detour, ground = args
    p = Packer(rooms, ways, side, seed, passages, pins, glue, ground)
    p.anneal()
    pairs, best = [(a, b) for a, b, _ in ways], None
    for _ in range(REPAIRS):
        rects = p.rects()
        found, left = route.plan(rects, pairs, walls, ground)
        far = [] if left else route.detours(found, rects, detour)
        if not left and p.clear() and p.over():
            score = (len(far), sum(r.length for r in found))
            if best is None or score < best[1]:
                best = (True, score, p.total(), p.x[:], p.y[:], p.o[:])
            if not far:
                break
        for name in left + [f"{r.a} to {r.b}" for r, _ in far]:
            a, b = (p.ix[c] for c in name.split(" to "))
            key = (min(a, b), max(a, b))
            hard = p.round[a] or p.round[b] or p.trouble.get(key) == "door"
            p.trouble[key] = "lane" if hard else "door"
        p.anneal(REPAIR_STEPS, 1.0, again=True)
    return best or (False, None, p.total(), p.x, p.y, p.o)


def pack(rooms, ways, seed: int, fill: tuple[float, float], passages: float, footprint: int | None = None,
         pins: dict | None = None, tries: int = 12, glue: dict | None = None, walls: dict | None = None,
         detour: float | None = None, ground=None):
    """The best packing over `tries` seeds at each side in turn - `footprint` alone where it is
    given - stopping at the first side where some seed leaves every way a passage, each by the
    wall `walls` names, and every pinned room over its pin. Best is fewest ways walking more than
    `detour` feet out of their way, then fewest feet walked, then lowest energy. `ground`, given a
    side, names the cells of that square its rooms and passages may take, or None for all:
    (side, packer, routes, energy), routes None where no side did."""
    pairs, pins = [(a, b) for a, b, _ in ways], pins or {}
    side = footprint
    with ProcessPoolExecutor() as pool:
        for side in [footprint] if footprint else squares(rooms, fill):
            g = ground(side) if ground else None
            runs = [r for r in pool.map(attempt, [(rooms, ways, side, seed * 1000 + k, passages, pins, glue, walls, detour, g)
                                                  for k in range(tries)]) if r[0]]
            if runs:
                ok, _, e, x, y, o = min(runs, key=lambda r: (r[1], r[2]))
                p = Packer(rooms, ways, side, seed, passages, pins, glue, g)
                p.x, p.y = x, y
                for i, k in enumerate(o):
                    p.lie(i, k)
                return side, p, route.plan(p.rects(), pairs, walls, g)[0], e
    return side, None, None, 0.0
