"""Defects in a dungeon map file, found by rebuilding its floor and testing it.

The floor is a set of unit cells, each owned by one room or one corridor, rebuilt from the
file's rooms, corridors (ports on room walls, bends between them, a width) and connections
(doors through a wall two rooms share). What is then tested is what a reader would see wrong:

  rooms overlapping, or touching where the map draws no shared walls; a corridor running through a room, or on across another corridor it
  does not share a room with, so joining ways nothing authored joins; a door that does not
  stand on the wall between two floors (a door in an open room, in rock, or stacked on
  another); a passage whose end is not on its room's wall; a room no way reaches; ways the
  tables name that the map lacks, and passages it draws that they do not name; and a stair
  or mark outside its room. Labels laid over one another come back as `label: ...`, the one
  kind a reader can still read round; notes are left to artgen, which places them clear.
"""
from __future__ import annotations

import math

SIDES = {"n": (0, -1), "e": (1, 0), "s": (0, 1), "w": (-1, 0)}
OPEN = (None, "open", "arch")          # a way with no door in it, still drawn on a wall
NAME_H = 1.4                           # cells: a room's code, at its centre


def inside(shape: str, r: dict, x: float, y: float) -> bool:
    if shape == "circle":
        return math.hypot(x - r["x"] - r["w"] / 2, y - r["y"] - r["h"] / 2) <= min(r["w"], r["h"]) / 2 + 1e-6
    return r["x"] - 1e-6 <= x <= r["x"] + r["w"] + 1e-6 and r["y"] - 1e-6 <= y <= r["y"] + r["h"] + 1e-6


def port(r: dict, end: dict) -> tuple[float, float] | None:
    side, off = end.get("side"), end.get("offset")
    if side not in SIDES or off is None:
        return None
    return {"n": (r["x"] + off, r["y"]), "s": (r["x"] + off, r["y"] + r["h"]),
            "w": (r["x"], r["y"] + off), "e": (r["x"] + r["w"], r["y"] + off)}[side]


class Floor:
    """Cells owned by rooms and corridors, as the file draws them."""

    def __init__(self, m: dict):
        self.m = m
        self.rooms = {r["id"]: r for r in m.get("rooms", [])}
        self.room_at: dict[tuple[int, int], list[str]] = {}
        self.corr_at: dict[tuple[int, int], list[int]] = {}
        self.errors: list[str] = []
        for rid, r in self.rooms.items():
            for i in range(math.floor(r["x"]), math.ceil(r["x"] + r["w"])):
                for j in range(math.floor(r["y"]), math.ceil(r["y"] + r["h"])):
                    if inside(r.get("shape", "rect"), r, i + 0.5, j + 0.5):
                        self.room_at.setdefault((i, j), []).append(rid)
        self.lines: list[list[tuple[float, float]]] = []
        for k, c in enumerate(m.get("corridors", [])):
            pts = self.line(k, c)
            self.lines.append(pts)
            half = float(c.get("width", 1)) / 2
            boxes = []
            for p, q in zip(pts, pts[1:]):
                if p[0] != q[0] and p[1] != q[1]:
                    self.errors.append(f"corridor {k} bends diagonally between {p} and {q}")
                    continue
                horizontal = p[1] == q[1]
                boxes.append((min(p[0], q[0]) - (0 if horizontal else half), min(p[1], q[1]) - (half if horizontal else 0),
                              max(p[0], q[0]) + (0 if horizontal else half), max(p[1], q[1]) + (half if horizontal else 0)))
            boxes += [(v[0] - half, v[1] - half, v[0] + half, v[1] + half) for v in pts[1:-1]]
            for x0, y0, x1, y1 in boxes:
                for i in range(math.floor(x0), math.ceil(x1)):
                    for j in range(math.floor(y0), math.ceil(y1)):
                        if x0 <= i + 0.5 <= x1 and y0 <= j + 0.5 <= y1 and k not in self.corr_at.get((i, j), []):
                            self.corr_at.setdefault((i, j), []).append(k)

    def line(self, k: int, c: dict) -> list[tuple[float, float]]:
        ends = []
        for name in ("from", "to"):
            e = c[name]
            if "room" in e and e["room"] in self.rooms:
                p = port(self.rooms[e["room"]], e)
                if p is None:
                    self.errors.append(f"corridor {k} {name} {e['room']} states no side and offset")
                    p = (self.rooms[e["room"]]["x"], self.rooms[e["room"]]["y"])
                ends.append(p)
            elif "at" in e:
                ends.append(tuple(e["at"]))
            else:
                self.errors.append(f"corridor {k} {name} is not a room or a point")
                ends.append((0.0, 0.0))
        via = c.get("via", [])
        return [ends[0]] + [(via[i], via[i + 1]) for i in range(0, len(via) - 1, 2)] + [ends[1]]

    def owners(self, x: float, y: float) -> tuple[tuple[str, ...], tuple[int, ...]]:
        c = (math.floor(x), math.floor(y))
        return tuple(self.room_at.get(c, ())), tuple(self.corr_at.get(c, ()))


def check(m: dict, ways: set[frozenset] | None = None, exits: int | None = None) -> list[str]:
    """Every defect in map file `m`. `ways` are the pairs of room ids the tables join inside
    the block and `exits` the ways they take out of it, to hold the map to them."""
    f = Floor(m)
    out = list(f.errors)
    rooms = f.rooms
    # rooms overlapping
    for cell, ids in f.room_at.items():
        if len(ids) > 1:
            out.append(f"{' and '.join(ids)} overlap at {cell}")
    walls = m.get("style", {}).get("sharedWalls", bool(m.get("connections")))
    for (i, j), ids in f.room_at.items():
        for dx, dy in ((1, 0), (0, 1)):
            for other in f.room_at.get((i + dx, j + dy), ()):
                if other not in ids and not walls:
                    out.append(f"{ids[0]} and {other} touch at {(i, j)}, but the map does not draw shared walls")
    out = sorted(set(out))
    # corridors: through rooms, and across or beside ones they share no room with
    ends = [{c["from"].get("room"), c["to"].get("room")} - {None} for c in m.get("corridors", [])]
    for cell, ks in f.corr_at.items():
        for k in ks:
            for rid in f.room_at.get(cell, ()):
                if rid not in ends[k]:
                    out.append(f"corridor {k} runs through {rid} at {cell}")
                else:
                    out.append(f"corridor {k} runs into {rid} at {cell}, past its wall")
    seen = set()
    for (i, j), ks in f.corr_at.items():
        near = set(ks)
        for dx, dy in SIDES.values():
            near |= set(f.corr_at.get((i + dx, j + dy), ()))
        for a in near:
            for b in near:
                if a < b and not (ends[a] & ends[b]) and (a, b) not in seen:
                    seen.add((a, b))
                    out.append(f"corridors {a} and {b} touch near {(i, j)}, joining rooms the tables do not")
    # doors stand on a wall between two floors
    stands: list[tuple[float, float, str]] = []

    def door(at, kind, a_ids, b_ids, label):
        for x, y, other in stands:
            if abs(x - at[0]) < 0.9 and abs(y - at[1]) < 0.9:
                out.append(f"{label} stands on {other}")
        stands.append((at[0], at[1], label))
        for dx, dy in SIDES.values():
            one = f.owners(at[0] - dx * 0.5, at[1] - dy * 0.5)
            two = f.owners(at[0] + dx * 0.5, at[1] + dy * 0.5)
            if (set(one[0]) & a_ids and (set(two[0]) & b_ids or (set(two[1]) & b_ids))) and not (set(one[0]) & set(two[0])):
                return
        out.append(f"{label} at {tuple(round(v, 1) for v in at)} does not stand on a wall between its two sides")

    for k, c in enumerate(m.get("corridors", [])):
        pts = f.lines[k]
        for end, kind, p in ((c["from"], (c.get("doors") or [None, None])[0], pts[0]),
                             (c["to"], (c.get("doors") or [None, None])[1], pts[-1])):
            if "room" in end and end["room"] in rooms:
                r = rooms[end["room"]]
                on = (abs(p[0] - r["x"]) < 1e-6 or abs(p[0] - r["x"] - r["w"]) < 1e-6 or abs(p[1] - r["y"]) < 1e-6 or abs(p[1] - r["y"] - r["h"]) < 1e-6)
                if not on or not (r["x"] - 1e-6 <= p[0] <= r["x"] + r["w"] + 1e-6 and r["y"] - 1e-6 <= p[1] <= r["y"] + r["h"] + 1e-6):
                    out.append(f"corridor {k} leaves {end['room']} from {p}, not on its wall")
                    continue
                # the door is the wall between the room and the corridor's first cell
                label = f"door of corridor {k} at {end['room']}"
                ok = False
                for dx, dy in SIDES.values():
                    a = f.owners(p[0] - dx * 0.5, p[1] - dy * 0.5)
                    b = f.owners(p[0] + dx * 0.5, p[1] + dy * 0.5)
                    if end["room"] in a[0] and k in b[1] and not b[0]:
                        ok = True
                if not ok:
                    out.append(f"{label} at {tuple(round(v, 1) for v in p)} does not stand on a wall between the room and the corridor")
                for x, y, o in stands:
                    if abs(x - p[0]) < 0.9 and abs(y - p[1]) < 0.9:
                        out.append(f"{label} stands on {o}")
                stands.append((p[0], p[1], label))
    for n, c in enumerate(m.get("connections", [])):
        a, b = c["a"], c["b"]
        label = f"connection {n} ({a} to {b})"
        if "at" not in c:
            out.append(f"{label} has no position")
            continue
        door(c["at"], c.get("kind"), {a}, {b}, label)
    # reach
    graph: dict[str, set[str]] = {rid: set() for rid in rooms}
    joined = set()
    for c in m.get("corridors", []):
        a, b = c["from"].get("room"), c["to"].get("room")
        if a in rooms and b in rooms:
            graph[a].add(b)
            graph[b].add(a)
            joined.add(frozenset((a, b)))
    for c in m.get("connections", []):
        if c["a"] in rooms and c["b"] in rooms:
            graph[c["a"]].add(c["b"])
            graph[c["b"]].add(c["a"])
            joined.add(frozenset((c["a"], c["b"])))
    if rooms:
        first = next(iter(rooms))
        reach, todo = {first}, [first]
        while todo:
            for n in graph[todo.pop()] - reach:
                reach.add(n)
                todo.append(n)
        for rid in sorted(set(rooms) - reach):
            out.append(f"{rid} is reached by no way from {first}")
    if ways is not None:
        for w in sorted(map(sorted, ways - joined)):
            out.append(f"the tables join {w[0]} and {w[1]}, but the map draws no way between them")
        for w in sorted(map(sorted, joined - ways)):
            out.append(f"the map joins {w[0]} and {w[1]}, which the tables do not")
    # marks
    notes = []
    for s in m.get("overlay", {}).get("symbols", []):
        if s.get("kind", "").startswith("stairs") or s.get("kind") == "arrow":
            rid = [r for r, rm in rooms.items() if inside(rm.get("shape", "rect"), rm, s["x"], s["y"])]
            if not rid:
                out.append(f"{s['kind']} at {(s['x'], s['y'])} is outside every room")
            notes.append((s["x"], s["y"], 1.6, 1.6, s["kind"]))
    if exits is not None:
        got = sum(1 for s in m.get("overlay", {}).get("symbols", []) if s.get("kind", "").startswith("stairs") or s.get("kind") == "arrow")
        if got != exits:
            out.append(f"the tables take {exits} ways out of the block, the map marks {got}")
    boxes = []
    for rid, r in rooms.items():
        text = r.get("label") or ""
        w = max(2.2, 0.8 * len(text) + 1)
        boxes.append((r["x"] + r["w"] / 2, r["y"] + r["h"] / 2, w, NAME_H, f"label of {rid}"))
    boxes += notes
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if abs(a[0] - b[0]) < (a[2] + b[2]) / 2 and abs(a[1] - b[1]) < (a[3] + b[3]) / 2:
                out.append(f"label: {a[4]} and {b[4]} overlap")
    return sorted(set(out))
