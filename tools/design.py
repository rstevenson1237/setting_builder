#!/usr/bin/env python3
"""Block designs: a region's Design.md as an artgen design, laid out by the engine, and held to the tables.

  python3 tools/design.py layouts                  # the layouts a design can use: artgen's, and this repo's layouts/
  python3 tools/design.py expand CODE [BLOCK]      # the design as artgen's, and the graph the engine expands it to
  python3 tools/design.py solve CODE [BLOCK] [--seeds N] [--keep K] [--free]   # N seeds laid out and scored, the best K drawn
  python3 tools/design.py accept CODE [BLOCK] --seed S                # write that seed's places into Design.md
  python3 tools/design.py check [CODE]             # a design and its tables, against one another

A design (`setting/region/[Code]/Design.md`, `patterns/Region_Schema.md`) names the layouts a block uses, binds
each layout's roles to location codes, joins their sockets and fills the rest of its locations. This tool writes it
as artgen's design (`artgen schema design`): its `Use`, `Bind`, `Fill` and `Join` lines as `uses`, `bind`, `rooms`
and `joins`, sizes in 5 ft cells, a stair's room `over` the room it meets, its outline as the footprint and its
voids kept out, its settings over BRIEF.md's `design` and `pack` lines. The engine expands the layouts
(`dungeon design`), lays the level out over seeds and scores each (`dungeon layout --design --seeds`). A layout of
`layouts/` (artgen's layout format) is used in place of the bundled one of its id.

`accept` writes one seed's `Place` and `Link` lines, its seed and score and, for a design that states no outline,
the `hull`; it never writes `approved`, which only the user's word sets, and takes away one the design had.
`check` holds an approved design and the tables to one another. SAFE and WILD blocks are fixed geometry, not solved:
their `Place` lines are written by hand, and `check` holds them too.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dungeon                  # noqa: E402
import kdl                      # noqa: E402
import maps                     # noqa: E402
import space                    # noqa: E402
import tables                   # noqa: E402

LAYOUTS = tables.ROOT / "layouts"
ROOM = 20                       # feet: a fill room's side, where its Fill states none
LATTICE = dungeon.LATTICE       # feet: rooms are sized in whole steps of it, so each lies on the lattice at a whole-foot place
CELL = dungeon.CELL
RING = 24                       # sides of the polygon a circular outline is given as
SHAPES = {"rect": "rect", "cave": "cave", "round": "round", "octagon": "octagon", "hexagon": "hexagon", "hall": "rect"}


def words(v) -> list[str]:
    return [w.strip() for w in str(v or "").split(",") if w.strip()]


def engine(*args) -> tuple[dict | None, str]:
    """One artgen dungeon call with this repo's layouts, `--json`: its output, or why it failed."""
    done = maps.artgen("dungeon", *args, "--layouts", LAYOUTS, "--json")
    if not done.returncode and done.stdout.startswith("{"):
        return json.loads(done.stdout), ""
    return None, (done.stderr or done.stdout).strip()


def layouts() -> tuple[dict | None, str]:
    return engine("layouts")


# -- a design, as artgen's -------------------------------------------------------------

class Expand:
    """One block's design as artgen's design: `design`, or `problems` (file, message)."""

    def __init__(self, region, brief: tables.Brief, bid: str, seed: int = 1, tries: int = 12, free: bool = False):
        self.region, self.bid, self.free, self.problems = region, bid, free, []
        self.design = None
        lines = [n for n in region.files.get("Design", []) if n.args]
        self.node = next((n for n in lines if n.name == "Design" and str(n.args[0]) == bid), None)
        if self.node is None:
            self.problems.append((region.dir / "Design.md", f"{region.code} holds no Design for {bid}"))
            return
        mine = lambda name: [n for n in lines if n.name == name and str(n.args[0]) == bid]
        self.locations = words(self.node.props.get("locations"))
        self.shape: dict[str, str] = {}
        self.uses = {str(n.props.get("id")): n for n in mine("Use")}
        self.bind = [b for n in mine("Bind") if (b := self.bound(n))]
        self.rooms = [r for n in mine("Fill") for r in self.filled(n)]
        unbound = [c for c in self.locations if c not in self.shape]
        if unbound:
            self.problems.append((region.dir / "Design.md", f"{', '.join(unbound)} of {bid} are in no Bind or Fill"))
        self.exits, self.joins = [], [j for n in mine("Join") if (j := self.join(n))]
        if not self.problems:
            self.design = self.build(brief, mine("Void"), seed, tries)

    def say(self, n: kdl.Node, msg: str):
        self.problems.append((self.region.dir / "Design.md", f"line {n.line}: {msg}"))

    def take(self, n: kdl.Node, c: str, shape: str) -> bool:
        if c in self.shape:
            self.say(n, f"{c} is bound twice")
        elif c not in self.locations:
            self.say(n, f"{c} is not one of the design's locations")
        else:
            self.shape[c] = shape
            return True
        return False

    def own(self, n: kdl.Node) -> dict:
        """A Bind's or Fill's own `pad`, which its rooms take in place of the design's."""
        if "pad" not in n.props:
            return {}
        if m := tables.PAD_RE.fullmatch(str(n.props["pad"])):
            return {"pad": int(m[1]) / CELL}
        self.say(n, 'pad is "N feet"')
        return {}

    def bound(self, n: kdl.Node) -> dict | None:
        uid, codes = str(n.props.get("use")), words(n.props.get("locations"))
        if uid not in self.uses:
            return self.say(n, f"Bind names use {uid!r}, which no Use of this design holds")
        if len(words(n.props.get("type"))) not in (1, len(codes)):
            return self.say(n, f"{len(codes)} locations and {len(words(n.props.get('type')))} types: one type, or one each")
        return {"use": uid, "role": str(n.props.get("role")),
                "rooms": [{"id": c, **self.own(n)} for c in codes if self.take(n, c, "layout")]}

    def filled(self, n: kdl.Node) -> list[dict]:
        if len(words(n.props.get("type"))) not in (1, len(words(n.props.get("locations")))):
            self.say(n, "a Fill states one type for its locations, or one each")
        shape, out = str(n.props.get("shape", "rect")), []
        if shape not in SHAPES:
            self.say(n, f"shape {shape} is not one of {', '.join(SHAPES)}")
            return []
        size = (int(n.props.get("width", ROOM)), int(n.props.get("length", ROOM)))
        poly = None
        if (o := space.outline_value(n.props.get("outline"))) is not None:        # a poly where no shape draws the room
            if o[0] != "poly":
                self.say(n, "a Fill's outline is a poly, or its width and length")
            else:
                poly = o[1]
                xs, ys = [x for x, _ in poly], [y for _, y in poly]
                size = (round(max(xs) - min(xs)), round(max(ys) - min(ys)))
        if any(v % LATTICE for v in size):
            self.say(n, f"{size[0]} by {size[1]} ft: a room is sized in whole {LATTICE} ft steps")
        for c in words(n.props.get("locations")):
            if self.take(n, c, shape):
                r = {"id": c, "w": size[0] / CELL, "h": size[1] / CELL, "shape": "poly" if poly else SHAPES[shape],
                     "hall": shape == "hall", **self.own(n)}
                if poly:
                    r["points"] = [v for x, y in poly for v in (x / CELL, -y / CELL)]
                out.append(r)
        return out

    def join(self, n: kdl.Node) -> dict | None:
        ends = [str(n.props.get("from")), str(n.props.get("to"))]
        socket = [e.split(".", 1)[0] in self.uses for e in ends]
        inside = [s or e in self.locations for e, s in zip(ends, socket)]
        if not any(inside):
            return self.say(n, "a Join has a room of this block at one end")
        if not all(inside):                       # a way out of the block: its room keeps it, the tables write it
            self.exits.append({"room": ends[inside.index(True)], "to": ends[inside.index(False)]})
            return None
        return {"from": ends[0], "to": ends[1]}

    def build(self, brief: tables.Brief, voids: list, seed: int, tries: int) -> dict | None:
        node = self.node
        self.settings = settings(brief, self.region.code, node)
        rates = brief.packing(self.region.code)
        overlay(rates, self.settings)
        if rates["fill"] is None or rates["passages"] is None:
            return self.say(node, "BRIEF.md states no pack fill and passages") or None
        poly, side = self.poly, self.side = ground(space.outline_value(node.props.get("outline")))
        frame = dungeon.framed(poly, side)
        pins = {} if self.free else {c: p for c in self.locations if (p := space.settled().pin(c))}   # free: the levels a stair joins are placed after this one
        rocks = [(space.point_of(v.props.get("xyz")) or [0.0, 0.0], s) for v in voids
                 if (s := space.outline_value(v.props.get("outline"))) is not None]
        if (pins or rocks) and not (poly or side):
            held = f"a stair into {', '.join(pins)}" if pins else "a void"
            return self.say(node, f"{held} is placed in the design's frame, so the design states an outline") or None
        for r in [r for b in self.bind for r in b["rooms"]] + self.rooms:
            if r["id"] in pins:
                r["over"] = dungeon.held_over(pins[r["id"]], frame)
        held = {j[k] for j in self.joins for k in ("from", "to") if "." in j["from"] + j["to"]}
        for r in self.rooms:                      # a room a socket holds keeps the socket's bearing
            r["turns"] = r["id"] not in held
        gid = f"{self.region.code}-{self.bid.split('.')[-1]}"
        d = dungeon.graph_shell(gid, self.rooms, [], rates, seed, tries, poly, side, rocks, frame)
        del d["ways"]
        d.update(uses=[{"id": uid, "layout": str(n.props.get("layout")),
                        "params": {k: int(v) for k, v in re.findall(r"([\w-]+)=(\d+)", str(n.props.get("params", "")))}}
                       for uid, n in self.uses.items()],
                 bind=self.bind, joins=self.joins, spokes=True, style=dungeon.looked({}))
        if m := tables.PAD_RE.fullmatch(self.settings.get("pad", "")):
            d["pad"] = int(m[1]) / CELL
        if m := tables.SPACING_RE.fullmatch(self.settings.get("spacing", "")):
            d["reach"] = int(m[2]) / CELL
        if not (poly or side):
            d["bounds"] = "hull"
        self.design = d
        got, why = self.run("design")
        if got is None:
            self.design = None
            return self.say(node, f"artgen: {why}") or None
        self.graph = got["graph"]
        for r in self.graph["rooms"]:             # a layout's room takes the shape the layout gives it
            if self.shape.get(r["id"]) == "layout":
                self.shape[r["id"]] = "hall" if r.get("hall") else r.get("shape", "rect")
        return d

    def run(self, command: str, *args) -> tuple[dict | None, str]:
        """`artgen dungeon <command>` over this design, written to a file: `layout` writes its dungeon there too."""
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "design.json"
            f.write_text(json.dumps(self.design))
            if command == "design":
                return engine("design", "--design", f)
            return engine("layout", "--file", Path(tmp) / "level.json", "--design", f, *args, "--force")


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


SETTINGS = ("fill", "spacing", "passages", "detour", "pad")


def settings(brief: tables.Brief, code: str, node: kdl.Node | None) -> dict[str, str]:
    """A block design's settings: BRIEF.md's `design` line for its region, then the Design line's own."""
    line = brief.designs.get(code)
    got = {k: str(v) for k, v in (line.props.items() if line is not None else ()) if k in SETTINGS}
    got.update({k: str(v) for k, v in (node.props.items() if node is not None else ()) if k in SETTINGS})
    return got


def overlay(rates: dict, got: dict[str, str]):
    """Settings over the rates a `pack` line gives. `spacing`, the passage wanted between joined rooms, sets
    `passages` (all, where it asks for 10 ft or more) and `detour` (its most) where `got` does not, and its
    most is the engine's `reach`. `pad` keeps each room that far clear of the next."""
    if m := tables.FILL_RE.fullmatch(got.get("fill", "")):
        rates["fill"] = (int(m[1]) / 100, int(m[2]) / 100)
    if "passages" in got:
        rates["passages"] = int(got["passages"][:-1]) / 100
    if "detour" in got:
        rates["detour"] = maps.feet(got["detour"])
    if m := tables.SPACING_RE.fullmatch(got.get("spacing", "")):
        if "passages" not in got and int(m[1]) >= 10:
            rates["passages"] = 1.0
        if "detour" not in got:
            rates["detour"] = float(m[2])


def expand(region, bid: str, seed: int = 1, tries: int = 12, free: bool = False) -> Expand:
    world = maps.world_for(tables.SETTING)
    return Expand(region, tables.Brief(world.schema), bid, seed, tries, free)


# -- solving and accepting -------------------------------------------------------------

def feet(ex: Expand, out: dict):
    """The function that turns a place in the engine's frame, in cells from the footprint's top-left, into feet east
    and north of the block's centre."""
    side = out["report"]["side"] * CELL
    ox, oy = (min(x for x, _ in ex.poly), min(-y for _, y in ex.poly)) if ex.poly else (-side / 2,) * 2
    return lambda x, y: (round(x * CELL + ox), round(-(y * CELL + oy)))


def notes(ex: Expand, c: dict) -> str:
    """Where a candidate falls short: what `dungeon check` found, and fill outside the design's."""
    lo, hi = ex.design["fill"]
    out = [f"{k} ({n})" for k, n in sorted(c.get("findings", {}).items())]
    if c.get("fill") is not None and not lo <= c["fill"] <= hi:
        out.append(f"fill {c['fill']:.0%} is {'under' if c['fill'] < lo else 'over'} {lo:.0%}-{hi:.0%}")
    return "; ".join(out) or "meets the design"


def problems_out(ex: Expand) -> bool:
    for path, msg in ex.problems:
        print(f"ERROR: {path.relative_to(tables.ROOT)}: {msg}", file=sys.stderr)
    return ex.design is None


def solve(region, bid: str, seeds: int, keep: int, folder: Path | None, free: bool = False) -> int:
    if region.rating.upper() != "DANGEROUS":
        print(f"{bid}: a {region.rating} block is fixed geometry, not solved: write its Place lines in Design.md")
        return 1
    ex = expand(region, bid, 1, free=free)
    if problems_out(ex):
        return 1
    folder = folder or Path(tempfile.gettempdir()) / f"design-{bid}"
    folder.mkdir(parents=True, exist_ok=True)
    out, why = ex.run("layout", "--seeds", seeds, "--keep", keep, "--sheet", folder / "contact.png")
    if out is None:
        print(f"{bid}: {why}")
        return 1
    print("seed  score  fill  ")
    for c in out["candidates"]:
        if c.get("score") is None:
            print(f"{c['seed']:<4}  -      -     {c.get('error', '').split(';')[0]}")
        else:
            print(f"{c['seed']:<4}  {c['score']:<5}  {c['fill']:.0%}   {notes(ex, c)}")
    routed = sum(c.get("score") is not None for c in out["candidates"])
    if not routed:
        print(f"{bid}: no seed of {seeds} routes every way; widen the outline, set a pad, lower the fill, or join fewer rooms")
        return 1
    print(f"\n{routed} of {seeds} seeds route every way. Contact sheet: {folder / 'contact.png'}\n"
          f"Then: python3 tools/design.py accept {region.code} {bid} --seed N")
    return 0


def accept(region, bid: str, seed: int, free: bool = False) -> int:
    if region.rating.upper() != "DANGEROUS":
        print(f"{bid}: a {region.rating} block is fixed geometry: write its Place lines in Design.md")
        return 1
    ex = expand(region, bid, seed, free=free)
    if problems_out(ex):
        return 1
    out, why = ex.run("layout")
    if out is None or out["report"]["left"]:
        print(f"{bid}: seed {seed} does not route every way: {why or ', '.join(map(str, out['report']['left']))}")
        return 1
    scored, _ = ex.run("layout", "--seeds", 2, "--keep", 1)          # the engine scores seeds from the design's own
    score = next((c["score"] for c in (scored or {}).get("candidates", []) if c["seed"] == seed), None)
    at = feet(ex, out)
    d, rep = out["dungeon"], out["report"]
    places = {p["id"]: {"at": at(p["cx"], p["cy"]), "w": round(p["w"] * CELL), "l": round(p["h"] * CELL)} for p in rep["places"]}
    drawn_as = {r["label"]: r for r in d["rooms"]}
    code = {r["id"]: r["label"] for r in d["rooms"]}.get
    ends = [(c["a"], c["b"]) for c in d["connections"]] + [(k["from"]["room"], k["to"]["room"]) for k in d["corridors"]]
    pairs = {tuple(sorted((code(a), code(b)), key=dungeon.number)) for a, b in ends}
    pairs = {k: "door" if touching(places[k[0]], places[k[1]]) else "passage" for k in pairs}      # a padded room's door is a passage across the pad
    lines = []
    for c in ex.locations:
        r, drawn = places[c], drawn_as.get(c, {})
        pts = drawn.get("points")
        box = ("poly " + " ".join(f"{(x - drawn['x'] - drawn['w'] / 2) * CELL:g},{(drawn['y'] + drawn['h'] / 2 - y) * CELL:g}"
                                  for x, y in zip(pts[::2], pts[1::2]))) if pts else f"rect {r['w']} {r['l']}"
        lines.append(f'Place {c} xyz="{r["at"][0]},{r["at"][1]}" outline="{box}" shape={ex.shape[c]}')
    lines += [f'Link {a} to="{b}" kind={kind}' for (a, b), kind in sorted(pairs.items(), key=lambda p: (dungeon.number(p[0][0]), dungeon.number(p[0][1])))]
    path = region.dir / "Design.md"
    text, fence = path.read_text().split("\n"), False
    kept, mine, last, had = [], set(ex.locations), None, False
    for line in text:
        if line.strip() == "```kdl":
            fence = True
        elif line.strip() == "```":
            fence, last = False, len(kept)
        elif fence and (m := re.match(r"(Place|Link) (\S+)", line)) and m[2] in mine:
            continue
        elif fence and line.startswith(f"Design {bid} "):
            had = "approved=" in line
            for k in ("approved", "seed", "score", "hull"):
                line = dungeon.without(line, k)
            line = dungeon.with_prop(line, "seed", str(seed))
            if score is not None:
                line = dungeon.with_prop(line, "score", f'"{score}"')
            if not ex.node.props.get("outline") and rep.get("hull"):
                h = rep["hull"]
                line = dungeon.with_prop(line, "hull", '"poly ' + " ".join("%d,%d" % at(x, y) for x, y in zip(h[::2], h[1::2])) + '"')
        kept.append(line)
    kept[last:last] = lines
    path.write_text("\n".join(kept))
    print(f"{bid}: seed {seed}, score {score}: {len(ex.locations)} places and {len(pairs)} ways written to {path.relative_to(tables.ROOT)}"
          + ("; its approval is cleared, for the user to give again" if had else "") + "\nThe user approves it, then steps 3e and 3f write the tables to agree.")
    return 0


# -- the design and its tables ---------------------------------------------------------

TOL = 0.5                       # feet two places may differ by and agree


def groups(region) -> dict[str, dict]:
    """A region's Design.md by block: its Design line, and every other line stating that block, a Place and a Link by the
    block whose locations they name."""
    out = {str(n.args[0]): {"design": n, "lines": [], "places": {}, "links": []}
           for n in region.files.get("Design", []) if n.name == "Design" and n.args}
    owner = {c: bid for bid, g in out.items() for c in words(g["design"].props.get("locations"))}
    for n in region.files.get("Design", []):
        if not n.args or n.name == "Design":
            continue
        bid = owner.get(str(n.args[0])) if n.name in ("Place", "Link") else str(n.args[0])
        if bid in out:
            out[bid]["lines"].append(n)
            if n.name == "Place":
                out[bid]["places"][str(n.args[0])] = n
            elif n.name == "Link":
                out[bid]["links"].append(n)
    return out


def kinds_of(n: kdl.Node) -> dict[str, str]:
    """The type each location of a Bind or Fill line asks for: its one type for all, or one each in order."""
    codes, types = words(n.props.get("locations")), words(n.props.get("type"))
    return {c: t for c, t in zip(codes, types * len(codes) if len(types) == 1 else types)}


def box(outline: tuple | None) -> tuple[float, float] | None:
    """The width and length of an outline's box."""
    if outline is None:
        return None
    if outline[0] == "circle":
        return 2 * outline[1], 2 * outline[1]
    if outline[0] == "rect":
        return outline[1], outline[2]
    xs, ys = [x for x, _ in outline[1]], [y for _, y in outline[1]]
    return max(xs) - min(xs), max(ys) - min(ys)


def touching(a: dict, b: dict) -> bool:
    """Whether two placed rooms share a wall: their boxes meet along one axis and overlap along the other."""
    d = [abs(a["at"][k] - b["at"][k]) for k in (0, 1)]
    reach = [((a["w"], a["l"])[k] + (b["w"], b["l"])[k]) / 2 for k in (0, 1)]
    return any(abs(d[k] - reach[k]) <= TOL * 5 and d[1 - k] < reach[1 - k] - CELL for k in (0, 1))


def at(p: list | None) -> str:
    return f"{p[0]:g},{p[1]:g}" if p else "no xyz"


def agree(region, bid: str, g: dict) -> list[tuple[str, str]]:
    """What an approved design and the region's tables disagree on, as (level, message), each naming the step that fixes
    it: a missing entry is a warning, a different one an error."""
    out = []
    node, path = g["design"], f"{bid}"
    members = set(words(node.props.get("locations")))
    danger = region.rating.upper() == "DANGEROUS"
    locs, dress = region.locations(), {str(n.args[0]): n for n in region.files.get("Dressing", []) if n.args}
    ways = [n for n in region.files.get("Connections", []) if n.args and "to" in n.props]
    block = tables_blocks(region).get(bid)
    if block is None:
        out.append(("warning", f"{bid} is no block in Blocks.md yet, and the design places {len(members)} locations in it - owed to step 3f"))
    elif set(words(block.props.get("locations"))) != members:
        out.append(("error", f"{bid} holds {', '.join(sorted(words(block.props.get('locations')), key=dungeon.number))} in Blocks.md and "
                             f"{', '.join(sorted(members, key=dungeon.number))} in its design - owed to step 3f, or 3d if the design is wrong"))
    mine = {}
    for c in sorted(members, key=dungeon.number):
        p = g["places"].get(c)
        if p is None:
            out.append(("error", f"the design approves {bid} and places no {c}: solve and accept it - owed to step 3d"))
            continue
        want = space.point_of(p.props.get("xyz"))
        size = box(space.outline_value(p.props.get("outline")))
        mine[c] = {"at": want[:2], "w": size[0], "l": size[1]}
        have, owes = (dress.get(c), "4a") if danger else (locs.get(c), "3e")        # a DANGEROUS room's place is its Dressing's
        if c not in locs or have is None:
            out.append(("warning", f"{c} is not in {'Locations.md' if c not in locs else 'Dressing.md'} yet, and the design places it - "
                                   f"owed to step {'3e' if c not in locs else '4a'}"))
            continue
        got = space.point_of(have.props.get("xyz"))
        if got is None or math.dist(got[:2], want[:2]) > TOL:
            out.append(("error", f"{c} lies at {at(got)} in the tables and at {at(want)} in the design - owed to step {owes}, or 3d if the design is wrong"))
        d = dress.get(c)
        if d is not None and "width" in d.props and "length" in d.props:
            if abs(float(d.props["width"]) - size[0]) > TOL or abs(float(d.props["length"]) - size[1]) > TOL:
                out.append(("error", f"{c} is {d.props['width']} by {d.props['length']} in Dressing.md and {size[0]:g} by {size[1]:g} in the design - owed to step 4a, or 3d if the design is wrong"))
        if str(d.props.get("shape", "rect") if d is not None else "rect") != str(p.props.get("shape", "rect")):
            out.append(("error", f"{c} is shape {d.props.get('shape', 'rect') if d is not None else 'rect'} in Dressing.md and {p.props.get('shape', 'rect')} in the design - owed to step 4a, or 3d if the design is wrong"))
    wanted = {}
    for n in g["lines"]:
        if n.name in ("Bind", "Fill"):
            for c, t in kinds_of(n).items():
                if c in locs and str(locs[c].props.get("type")) != t:
                    out.append(("error", f"{c} is type {locs[c].props.get('type')} in Locations.md and {t} in the design - owed to step 3e, or 3d if the design is wrong"))
    for n in g["links"]:
        a, b = str(n.args[0]), str(n.props.get("to"))
        wanted[frozenset((a, b))] = (a, b, str(n.props.get("kind")))
        if str(n.props.get("kind")) == "door" and a in mine and b in mine and not touching(mine[a], mine[b]):
            out.append(("error", f"the design joins {a} and {b} by a door, and they share no wall - owed to step 3d"))
    stated = {(str(n.args[0]), str(n.props["to"])) for n in ways if str(n.args[0]) in members and str(n.props["to"]) in members}
    for k, (a, b, _) in wanted.items():
        for x, y in ((a, b), (b, a)):
            if (x, y) not in stated:
                unwritten = not any(c in q for q in stated for c in (x, y))     # neither end has a way yet: owed, not wrong
                out.append(("warning" if unwritten else "error",
                            f"the design joins {a} and {b}, and Connections.md lacks {x} to {y} - owed to step 3f"))
    for x, y in sorted(stated):
        if frozenset((x, y)) not in wanted:
            out.append(("error", f"Connections.md joins {x} and {y}, which the design does not - owed to step 3f, or 3d if the design lacks it"))
    voids = {(space.outline_value(n.props.get("outline")), tuple(space.point_of(n.props.get("xyz")) or [0.0, 0.0])[:2]) for n in g["lines"] if n.name == "Void"}
    held = {(space.outline_value(n.props.get("outline")), tuple(space.point_of(n.props.get("xyz")) or [0.0, 0.0])[:2])
            for n in region.files.get("Blocks", []) if n.args and str(n.args[0]) == bid and n.name == ("Rock" if danger else "Void")}
    atp = lambda p: f"{p[0]:g},{p[1]:g}"
    for kind, a, b in (("Void", voids, held), (("Rock" if danger else "Void"), held, voids)):
        for o, xy in sorted(a - b, key=str):
            out.append(("error", f"{bid} has a {kind} {space.said(o)} at {atp(list(xy))} in {'its design' if a is voids else 'Blocks.md'} and none in {'Blocks.md' if a is voids else 'its design'} - owed to step 3f"))
    return out


def tables_blocks(region) -> dict[str, kdl.Node]:
    return maps.blocks_of(region)


def check(world, brief) -> list[tuple[str, Path, str]]:
    """Every region's designs and tables against one another: (level, file, message). A region whose BRIEF.md node asks
    for a design and has none approved is owed to step 3d; each approved design is held to the tables."""
    out = []
    for code, region in world.regions.items():
        path = region.dir / "Design.md"
        made = groups(region)
        if code in brief.designs and not any(g["design"].props.get("approved") for g in made.values()):
            out.append(("warning", path if path.exists() else region.dir, f"BRIEF.md asks region {code} for a design, and none is approved - owed to step 3d"))
        for bid, g in made.items():
            node, approved = g["design"], bool(g["design"].props.get("approved"))
            for k in SETTINGS:
                if k in node.props and (bad := tables.design_setting(k, str(node.props[k]))):
                    out.append(("error", path, f"line {node.line}: Design {bid} {bad}"))
            if region.rating.upper() == "DANGEROUS" and any(n.name in ("Use", "Bind", "Fill") for n in g["lines"]):
                ex = expand(region, bid)
                out += [("error" if approved else "warning", f, f"{m} - owed to step 3d") for f, m in ex.problems]
            if approved:
                out += [(level, path, msg) for level, msg in agree(region, bid, g)]
    return out


# -- the commands ----------------------------------------------------------------------

def show_layouts() -> int:
    """The engine's list: its bundled layouts, and each of layouts/ in place of the one of its id."""
    done = maps.artgen("dungeon", "layouts", "--layouts", LAYOUTS)
    print(done.stdout.rstrip() or done.stderr.strip())
    return done.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("layouts", help="the library: id, tags, parameters, sockets")
    e = sub.add_parser("expand", help="the design as artgen's, and the graph the engine expands it to")
    e.add_argument("code")
    e.add_argument("block", nargs="?", help="a block id, where the region has designs for several")
    e.add_argument("--seed", type=int, default=1)
    e.add_argument("--tries", type=int, default=12)
    free = dict(action="store_true", help="ignore the places of the levels a stair joins: they are placed after this one")
    e.add_argument("--free", **free)
    v = sub.add_parser("solve", help="N seeds laid out and scored, the best K drawn on a contact sheet")
    v.add_argument("code")
    v.add_argument("block", nargs="?")
    v.add_argument("--seeds", type=int, default=12)
    v.add_argument("--keep", type=int, default=3)
    v.add_argument("--out", type=Path, help="where the drawings go; default a folder of the system's temporary directory")
    v.add_argument("--free", **free)
    a = sub.add_parser("accept", help="write one seed's places into Design.md")
    a.add_argument("code")
    a.add_argument("block", nargs="?")
    a.add_argument("--seed", type=int, required=True)
    a.add_argument("--free", **free)
    c = sub.add_parser("check", help="every approved design against its tables")
    c.add_argument("code", nargs="?")
    args = ap.parse_args()
    if args.command == "layouts":
        return show_layouts()
    world = maps.world_for(tables.SETTING)
    if args.command == "check":
        found = [f for f in check(world, tables.Brief(world.schema)) if not args.code or f"/region/{args.code}/" in str(f[1])]
        for level, path, msg in found:
            print(f"{level.upper()}: {Path(path).relative_to(tables.ROOT)}: {msg}")
        print(f"{sum(f[0] == 'error' for f in found)} error(s), {sum(f[0] == 'warning' for f in found)} warning(s)")
        return 1 if any(f[0] == "error" for f in found) else 0
    region = world.regions.get(args.code)
    if region is None:
        print(f"ERROR: {args.code} is no region of this setting", file=sys.stderr)
        return 1
    blocks = [str(n.args[0]) for n in region.files.get("Design", []) if n.name == "Design" and n.args]
    bid = args.block or (blocks[0] if len(blocks) == 1 else None)
    if bid is None:
        print(f"ERROR: {args.code} holds {'no design' if not blocks else 'designs for ' + ', '.join(blocks) + ': name one'}", file=sys.stderr)
        return 1
    if args.command == "solve":
        return solve(region, bid, args.seeds, args.keep, args.out, args.free)
    if args.command == "accept":
        return accept(region, bid, args.seed, args.free)
    done = expand(region, bid, args.seed, args.tries, args.free)
    for path, msg in done.problems:
        print(f"ERROR: {path.relative_to(tables.ROOT)}: {msg}", file=sys.stderr)
    if done.design is not None:
        print(json.dumps({"design": done.design, "graph": done.graph}, indent=1))
    return 1 if done.problems else 0


if __name__ == "__main__":
    sys.exit(main())
