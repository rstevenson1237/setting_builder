"""Packs a DANGEROUS block's rooms close into a square, and says where each stands.

A room is a rectangle of its Dressing's width and length, centred on a multiple of GRID feet.
Rooms joined by a way are cast face to face: touching, so the way is a door through the
shared wall, or a short straight lane apart. Rooms not joined may touch but leave no slit
narrower than a passage. A way out of the block leaves from the side of the square its
bearing faces. The packing is annealed, so a seed fixes it.
"""
from __future__ import annotations

import math
import random
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

GRID = 5                    # feet a room's centre moves by
DOOR = 10                   # feet of shared wall a way needs
LANE = 10                   # feet, the narrowest slit or passage between rooms
LONGEST = 50                # feet, the longest lane before it is a corridor of its own
FILL = 0.58                 # the share of the square its rooms cover, before the passages
STEPS = 90000
OVER, SLIT, DIAGONAL, BLOCKED, SIDE = 40.0, 4.0, 8.0, 3.0, 6.0


@dataclass
class Room:
    code: str
    w: int
    h: int
    round: bool = False


def compass_vector(bearing: float) -> tuple[float, float]:
    """East and south components of a compass angle in degrees, clockwise from north."""
    a = math.radians(bearing)
    return math.sin(a), -math.cos(a)


class Packer:
    def __init__(self, rooms: list[Room], ways: list[tuple[str, str, float]], exits: dict[str, float],
                 side: int, seed: int = 1):
        self.rooms, self.side = rooms, side
        self.ix = {r.code: i for i, r in enumerate(rooms)}
        self.w = [r.w for r in rooms]
        self.h = [r.h for r in rooms]
        self.round = [r.round for r in rooms]
        self.edges: dict[tuple[int, int], tuple[float, float]] = {}     # i < j: unit vector from i to j as authored
        for a, b, bearing in ways:
            i, j = self.ix[a], self.ix[b]
            v = compass_vector(bearing)
            self.edges[(i, j)] = v if i < j else (-v[0], -v[1])
            if i > j:
                self.edges[(j, i)] = self.edges.pop((i, j))
        self.exits = {self.ix[c]: compass_vector(b) for c, b in exits.items()}
        self.near = [[j for j in range(len(rooms)) if (min(i, j), max(i, j)) in self.edges] for i in range(len(rooms))]
        self.rng = random.Random(seed)
        self.x = [0] * len(rooms)
        self.y = [0] * len(rooms)

    # -- geometry ------------------------------------------------------------------------

    def box(self, i, x=None, y=None):
        x = self.x[i] if x is None else x
        y = self.y[i] if y is None else y
        return x - self.w[i] / 2, y - self.h[i] / 2, x + self.w[i] / 2, y + self.h[i] / 2

    def gaps(self, i, j, xi=None, yi=None):
        a, b = self.box(i, xi, yi), self.box(j)
        return max(b[0] - a[2], a[0] - b[2]), max(b[1] - a[3], a[1] - b[3])

    def face(self, i, j, xi=None, yi=None):
        """How i and j face: (axis, gap, band) where the rooms see one another straight across
        `gap` feet along `axis` and share `band` = (low, high) on the other, else None."""
        a, b = self.box(i, xi, yi), self.box(j)
        sx, sy = max(b[0] - a[2], a[0] - b[2]), max(b[1] - a[3], a[1] - b[3])
        best = None
        if sx >= 0 and min(a[3], b[3]) - max(a[1], b[1]) >= DOOR:
            best = ("x", sx, (max(a[1], b[1]), min(a[3], b[3])))
        if sy >= 0 and min(a[2], b[2]) - max(a[0], b[0]) >= DOOR and (best is None or sy < best[1]):
            best = ("y", sy, (max(a[0], b[0]), min(a[2], b[2])))
        return best

    def lane(self, i, j, face, xi=None, yi=None):
        """The rectangle a lane between facing rooms i and j runs through."""
        a, b = self.box(i, xi, yi), self.box(j)
        axis, gap, (lo, hi) = face
        mid = (lo + hi) / 2
        if axis == "x":
            left, right = (a, b) if a[0] < b[0] else (b, a)
            return (left[2], mid - LANE / 2, right[0], mid + LANE / 2)
        top, bottom = (a, b) if a[1] < b[1] else (b, a)
        return (mid - LANE / 2, top[3], mid + LANE / 2, bottom[1])

    # -- energy --------------------------------------------------------------------------

    def pair(self, i, j, xi=None, yi=None) -> float:
        a, b = self.box(i, xi, yi), self.box(j)
        sx, sy = max(b[0] - a[2], a[0] - b[2]), max(b[1] - a[3], a[1] - b[3])
        if sx < 0 and sy < 0:
            return OVER * (1 + min(-sx, -sy) / GRID)
        joined = (min(i, j), max(i, j)) in self.edges
        e = 0.0
        if not joined:
            if (0 < sx < LANE and sy < 0) or (0 < sy < LANE and sx < 0):
                e += SLIT
            return e
        f = self.face(i, j, xi, yi)
        if f is None:
            d = math.hypot(max(sx, 0), max(sy, 0))
            e += DIAGONAL + d / 20
        else:
            gap = f[1]
            if self.round[i] or self.round[j]:       # a round room is met by a lane, on its centre line
                if gap < LANE:
                    e += 2 + (LANE - gap) / 5
                for r in (i, j):
                    if self.round[r]:
                        at = (xi if r == i and xi is not None else self.x[r], yi if r == i and yi is not None else self.y[r])
                        if not f[2][0] <= at[1 if f[0] == "x" else 0] <= f[2][1]:
                            e += 2
            if gap > 0:
                e += 0.15 + gap / 160
            if gap > LONGEST:
                e += 3 * (gap - LONGEST) / 10
        want = self.edges[(min(i, j), max(i, j))]
        dx = (self.x[j] - (self.x[i] if xi is None else xi)) * (1 if i < j else -1)
        dy = (self.y[j] - (self.y[i] if yi is None else yi)) * (1 if i < j else -1)
        n = math.hypot(dx, dy) or 1
        e += 1.2 * (1 - (dx * want[0] + dy * want[1]) / n)
        return e

    def blocked(self, i, x=None, y=None) -> float:
        """What the lanes of the ways cost where room i, at x, y, lies across them."""
        e = 0.0
        mine = self.box(i, x, y)
        for (a, b) in self.edges:
            if i in (a, b):
                other = b if i == a else a
                f = self.face(i, other, x, y)
                if f and f[1] > 0:
                    r = self.lane(i, other, f, x, y)
                    for k in range(len(self.w)):
                        if k not in (a, b) and self.hit(self.box(k), r):
                            e += BLOCKED
                continue
            f = self.face(a, b)
            if f and f[1] > 0 and self.hit(mine, self.lane(a, b, f)):
                e += BLOCKED
        return e

    @staticmethod
    def hit(a, b) -> bool:
        return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]

    def edge_of_square(self, i, x=None, y=None) -> float:
        x = self.x[i] if x is None else x
        y = self.y[i] if y is None else y
        a = self.box(i, x, y)
        e = 0.0
        for lo, hi in ((a[0], a[2]), (a[1], a[3])):
            if lo < 0:
                e += OVER * (-lo / GRID + 1)
            if hi > self.side:
                e += OVER * ((hi - self.side) / GRID + 1)
        if i in self.exits:
            v = self.exits[i]
            if abs(v[0]) >= abs(v[1]):
                d = self.side - a[2] if v[0] > 0 else a[0]
            else:
                d = self.side - a[3] if v[1] > 0 else a[1]
            e += SIDE * max(0, d) / 10
        return e

    def local(self, i, x=None, y=None) -> float:
        e = self.edge_of_square(i, x, y) + self.blocked(i, x, y)
        for j in range(len(self.w)):
            if j != i:
                e += self.pair(i, j, x, y)
        return e

    def total(self) -> float:
        n = len(self.w)
        e = sum(self.edge_of_square(i) for i in range(n))
        e += sum(self.pair(i, j) for i in range(n) for j in range(i + 1, n))
        e += sum(self.blocked(i) for i in range(n)) / 2
        return e

    def unmet(self) -> list[str]:
        """The ways whose rooms do not face one another within LONGEST, the rooms overlapping and the
        ways out that do not leave from the square's edge."""
        out = []
        for (i, j) in self.edges:
            f = self.face(i, j)
            if f is None or f[1] > LONGEST:
                out.append(f"{self.rooms[i].code} to {self.rooms[j].code}")
        for i in self.exits:
            a = self.box(i)
            v = self.exits[i]
            d = (self.side - a[2] if v[0] > 0 else a[0]) if abs(v[0]) >= abs(v[1]) else (self.side - a[3] if v[1] > 0 else a[1])
            if d > 10:
                out.append(f"{self.rooms[i].code} is {d:g} feet from the side its way out faces")
        for i in range(len(self.w)):
            for j in range(i + 1, len(self.w)):
                sx, sy = self.gaps(i, j)
                if sx < 0 and sy < 0:
                    out.append(f"{self.rooms[i].code} overlaps {self.rooms[j].code}")
        return out

    # -- search --------------------------------------------------------------------------

    def snap(self, v):
        return int(round(v / GRID)) * GRID

    def place(self):
        """Rooms in order of the ways, each against the one before it."""
        n, rng = len(self.w), self.rng
        order = [0]
        for i in order:
            order += [j for j in self.near[i] if j not in order]
        order += [i for i in range(n) if i not in order]
        self.x[order[0]] = self.snap(self.side / 2)
        self.y[order[0]] = self.snap(self.side / 2)
        for k, i in enumerate(order[1:], 1):
            placed = order[:k]
            anchors = [j for j in self.near[i] if j in placed] or placed
            j = rng.choice(anchors)
            self.x[i], self.y[i] = self.against(i, j)

    def against(self, i, j):
        """A spot for room i touching room j, on a side and at an offset chosen at random."""
        rng = self.rng
        side = rng.choice("nesw")
        gap = rng.choice((0, 0, 0, LANE, 2 * LANE))
        if side in "ns":
            y = self.y[j] + (self.h[j] + self.h[i]) / 2 * (-1 if side == "n" else 1) + gap * (-1 if side == "n" else 1)
            x = self.x[j] + rng.randint(-(self.w[j] + self.w[i]) // 2 + DOOR, (self.w[j] + self.w[i]) // 2 - DOOR)
        else:
            x = self.x[j] + (self.w[j] + self.w[i]) / 2 * (-1 if side == "w" else 1) + gap * (-1 if side == "w" else 1)
            y = self.y[j] + rng.randint(-(self.h[j] + self.h[i]) // 2 + DOOR, (self.h[j] + self.h[i]) // 2 - DOOR)
        return self.snap(x), self.snap(y)

    def anneal(self, steps: int = STEPS):
        rng, n = self.rng, len(self.w)
        self.place()
        cur = self.total()
        best, best_at = cur, (self.x[:], self.y[:])
        t0, t1 = 3.0, 0.04
        for s in range(steps):
            t = t0 * (t1 / t0) ** (s / steps)
            i = rng.randrange(n)
            r = rng.random()
            if r < 0.55:
                reach = max(GRID, int(40 * (1 - s / steps)))
                nx = self.snap(self.x[i] + rng.randint(-reach, reach))
                ny = self.snap(self.y[i] + rng.randint(-reach, reach))
            elif r < 0.9 and self.near[i]:
                nx, ny = self.against(i, rng.choice(self.near[i]))
            else:
                j = rng.randrange(n)
                if j == i:
                    continue
                before = self.local(i) + self.local(j) - self.pair(i, j)
                self.x[i], self.x[j] = self.x[j], self.x[i]
                self.y[i], self.y[j] = self.y[j], self.y[i]
                after = self.local(i) + self.local(j) - self.pair(i, j)
                if after - before <= 0 or rng.random() < math.exp(-(after - before) / t):
                    cur += after - before
                else:
                    self.x[i], self.x[j] = self.x[j], self.x[i]
                    self.y[i], self.y[j] = self.y[j], self.y[i]
                continue
            before = self.local(i)
            after = self.local(i, nx, ny)
            if after - before <= 0 or rng.random() < math.exp(-(after - before) / t):
                self.x[i], self.y[i] = nx, ny
                cur += after - before
            if cur < best - 1e-9:
                best, best_at = cur, (self.x[:], self.y[:])
        self.x, self.y = best_at[0][:], best_at[1][:]
        return self.total()


def squares(rooms: list[Room]) -> list[int]:
    """Sides to try, in feet, from where the rooms fill FILL of the square upward."""
    area = sum(r.w * r.h for r in rooms)
    base = math.ceil(math.sqrt(area / FILL) / 10) * 10
    longest = max(max(r.w, r.h) for r in rooms)
    base = max(base, longest + 20)
    return [base + 10 * k for k in range(0, 8)]


def attempt(args):
    rooms, ways, exits, side, seed = args
    p = Packer(rooms, ways, exits, side, seed)
    e = p.anneal()
    return e, p.x, p.y, seed


def pack(rooms, ways, exits, seed=1, tries=8):
    """The best packing over a few seeds at each side in turn, stopping at the first that
    leaves every way face to face and every room clear: (side, packer, energy)."""
    with ProcessPoolExecutor() as pool:
        for side in squares(rooms):
            runs = list(pool.map(attempt, [(rooms, ways, exits, side, seed * 1000 + k) for k in range(tries)]))
            e, x, y, _ = min(runs, key=lambda r: r[0])
            p = Packer(rooms, ways, exits, side)
            p.x, p.y = x, y
            if not p.unmet() and e < 12 + len(rooms):
                return side, p, e
    return side, p, e
