#!/usr/bin/env python3
"""Block designs: a region's Design.md laid out, accepted, and held to the tables.

  python3 tools/design.py solve CODE [BLOCK] [--seeds N] [--keep K] [--free]   # a plan's drawing; a settlement's seeds, scored
  python3 tools/design.py accept CODE [BLOCK] [--seed S]              # write the places into Design.md
  python3 tools/design.py apply CODE               # an approved design's places into the tables
  python3 tools/design.py check [CODE]             # a design and its tables, against one another

A design (`setting/region/[Code]/Design.md`, `patterns/Region_Schema.md`) states a block before its tables are
written. A DANGEROUS block's is a plan (`Layout`, `Room` and `Route` lines), solved by `tools/plan.py`, which `solve`,
`accept` and `apply` hand it to. A SAFE or WILD block is a settlement: its `Fill`, `Tie` and `Street` lines are
artgen's settlement graph, each building the kind its location's type gives, laid out by `settlement layout` seed by
seed and scored on the faults it reports and how far each tie strays.

`accept` writes the `Place` lines (a plan's `Link` and `Part` lines too), the seed and the score; it never writes
`approved`, which only the user's word sets, and takes away one the design had. `apply` writes an approved design's
places where its tables hold them: a DANGEROUS room's in Dressing.md, a SAFE or WILD location's in Locations.md.
`check` holds an approved design and the tables to one another.
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
import plan                     # noqa: E402
import space                    # noqa: E402
import tables                   # noqa: E402

ROOM = 20                       # feet: a building's side, where its Fill states none


def words(v) -> list[str]:
    return [w.strip() for w in str(v or "").split(",") if w.strip()]


SETTINGS = ("fill", "pad")


# -- accepting -------------------------------------------------------------------------

def write_places(region, bid: str, locations: list[str], lines: list[str], seed: int, score, hull: str | None, what: str):
    """A design's Place and Link lines for its block replaced by `lines`, its seed and score set, and its approval cleared."""
    path = region.dir / "Design.md"
    text, fence = path.read_text().split("\n"), False
    kept, mine, last, had = [], set(locations), None, False
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
            if hull:
                line = dungeon.with_prop(line, "hull", hull)
        kept.append(line)
    kept[last:last] = lines
    path.write_text("\n".join(kept))
    print(f"{bid}: seed {seed}, score {score}: {what} written to {path.relative_to(tables.ROOT)}"
          + ("; its approval is cleared, for the user to give again" if had else "") + f"\nThe user approves it; then `python3 tools/design.py apply {region.code}` writes its places.")


# -- a SAFE or WILD block: a settlement laid out to a graph -----------------------------

SETTLE_CELLS = (5, 10, 20)      # feet to a cell, the finest that keeps the settlement within the engine's sheet
SETTLE_MOST = 200               # cells across the engine draws a settlement in, with room for its margin


class Settle:
    """A SAFE or WILD block's design as artgen's settlement graph (`artgen schema settlement-graph`): each Fill a
    building or open area, each Tie one place a bearing and distance from another, each Street the buildings it runs
    past in order. The design's first location stands at the block's centre; every place the ties reach from it stands
    where they put it, and the solve lays out the rest and the streets."""

    def __init__(self, region, bid: str):
        self.region, self.bid, self.problems, self.graph = region, bid, [], None
        lines = [n for n in region.files.get("Design", []) if n.args]
        self.node = next((n for n in lines if n.name == "Design" and str(n.args[0]) == bid), None)
        if self.node is None:
            self.problems.append((region.dir / "Design.md", f"{region.code} holds no Design for {bid}"))
            return
        mine = lambda name: [n for n in lines if n.name == name and str(n.args[0]) == bid]
        say = lambda n, msg: self.problems.append((region.dir / "Design.md", f"line {n.line}: {msg}"))
        self.locations = words(self.node.props.get("locations"))
        compass = space.compass()
        size = {}
        kinds = {c: str(n.props.get("type")) for c, n in region.locations().items()}
        for n in mine("Fill"):
            for c in words(n.props.get("locations")):
                if c not in self.locations or c in size or c not in kinds:
                    say(n, f"{c} is not one of the design's locations in Locations.md, or is filled twice")
                    continue
                size[c] = (int(n.props.get("width", ROOM)), int(n.props.get("length", ROOM)))
        if unfilled := [c for c in self.locations if c not in size]:
            self.problems.append((region.dir / "Design.md", f"{', '.join(unfilled)} of {bid} are in no Fill"))
        ties = []
        for n in mine("Tie"):
            a, b = str(n.props.get("from")), str(n.props.get("to"))
            if a not in size or b not in size or str(n.props.get("bearing")) not in compass or "distance" not in n.props:
                say(n, "a Tie joins two of the design's locations, with a Compass bearing and a distance")
                continue
            ties.append((a, b, compass.index(str(n.props["bearing"])) * 22.5, maps.feet(str(n.props["distance"]))))
        if self.problems:
            return
        self.size = size
        span = max([d for *_, d in ties] + [max(max(v) for v in size.values())]) * 2
        self.cell = next((c for c in SETTLE_CELLS if span / c <= SETTLE_MOST), SETTLE_CELLS[-1])
        wild = region.rating.upper() == "WILD"
        kind = lambda t: "market" if t == "Market" else "ruin" if wild and t == "Ruin" else maps.BUILDING.get(t, "house")
        self.fixed = {self.locations[0]: (0.0, 0.0)}    # each place the ties reach from the first, east and south in feet
        first = space.point_of(region.locations()[self.locations[0]].props.get("xyz")) or [0.0, 0.0]
        for c in self.locations[1:]:                    # and each the tables place by xyz and no tie names
            xyz = space.point_of(region.locations()[c].props.get("xyz"))
            if xyz and not any(c in t[:2] for t in ties):
                self.fixed[c] = (xyz[0] - first[0], first[1] - xyz[1])
        for _ in ties:
            for a, b, br, d in ties:
                if a in self.fixed and b not in self.fixed:
                    r = math.radians(br)
                    self.fixed[b] = (self.fixed[a][0] + d * math.sin(r), self.fixed[a][1] - d * math.cos(r))
        way = space.offset(region, region.locations()[self.locations[0]]) or (0.0, 0.0)
        stands = {c: (v, size[c]) for c, v in self.fixed.items()}   # and each block of another region through its ground
        for b, poly in maps.breaking(region.code):
            xs, ys = [x for x, _ in poly], [y for _, y in poly]
            stands[b] = (((min(xs) + max(xs)) / 2 - way[0], way[1] - (min(ys) + max(ys)) / 2), (max(xs) - min(xs), max(ys) - min(ys)))
        lo = [min(v[k] - z[k] / 2 for v, z in stands.values()) for k in (0, 1)]
        at = lambda c: {"x": round((stands[c][0][0] - stands[c][1][0] / 2 - lo[0]) / self.cell, 1),
                        "y": round((stands[c][0][1] - stands[c][1][1] / 2 - lo[1]) / self.cell, 1)}
        self.graph = {"id": f"{region.code}-{bid.split('.')[-1]}", "kind": "village", "ground": "sand" if wild else "grass",
                      "scale": {"perCell": self.cell, "unit": "ft"}, "wall": False if wild and "wall" not in self.node.props else {"kind": "stone"},
                      "buildings": [{"id": c, "w": max(1, round(w / self.cell, 1)), "h": max(1, round(h / self.cell, 1)), "kind": kind(kinds[c]),
                                     **({"at": at(c)} if c in self.fixed else {"turns": not any(c in t[:2] for t in ties)})}
                                    for c, (w, h) in size.items()]
                                   + [{"id": b, "w": round(z[0] / self.cell, 1), "h": round(z[1] / self.cell, 1), "kind": "square", "at": at(b)}
                                      for b, (_, z) in stands.items() if b not in size],
                      "ties": [{"a": a, "b": b, "bearing": br, "distance": round(d / self.cell, 1), "hold": True} for a, b, br, d in ties
                               if not {a, b} <= set(self.fixed)],
                      "streets": [{"past": words(n.props.get("past")), **({"kind": str(n.props["kind"])} if "kind" in n.props else {})}
                                  for n in mine("Street")]}
        for k in ("streets", "ties"):
            if not self.graph[k]:
                del self.graph[k]

    def run(self, seed: int, folder: Path) -> dict | str:
        """`artgen settlement layout` at a seed, its file kept in `folder`: its output, or why it failed."""
        f = folder / f"seed-{seed}.json"
        (folder / "graph.json").write_text(json.dumps(dict(self.graph, seed=seed)))
        done = maps.artgen("settlement", "layout", "--file", f, "--graph", folder / "graph.json", "--seed", seed, "--json", "--force")
        return json.loads(done.stdout) if not done.returncode and done.stdout.startswith("{") else (done.stderr or done.stdout).strip()

    def places(self, out: dict) -> dict[str, tuple[int, int, int, int]]:
        """Each building's centre, east and north in feet of the first location's, and its width and length."""
        got = {p["id"]: p for p in out["report"]["places"]}
        o, k = got[self.locations[0]], self.cell
        return {c: (round(self.fixed[c][0]), round(-self.fixed[c][1]), *self.size[c]) if c in self.fixed else
                (round((p["cx"] - o["cx"]) * k), round(-(p["cy"] - o["cy"]) * k),
                 round(2 * (p["cx"] - p["x"]) * k), round(2 * (p["cy"] - p["y"]) * k)) for c, p in got.items() if c in self.size}


def settle_score(out: dict) -> tuple[int, str]:
    """Out of 100: ten off for each fault the engine reports, and one for each foot or degree a tie is off."""
    rep = out["report"]
    faults = rep.get("faults", [])
    off = sum(abs(t.get("distance", 0) - t.get("want", 0)) + abs((t.get("bearing", 0) - t.get("wantBearing", 0) + 180) % 360 - 180)
              for t in rep.get("ties", []))
    return max(0, round(100 - 10 * len(faults) - off)), "; ".join(faults) or "every tie held"


def settle_solve(region, bid: str, seeds: int, keep: int, folder: Path | None) -> int:
    st = Settle(region, bid)
    for path, msg in st.problems:
        print(f"ERROR: {path.relative_to(tables.ROOT)}: {msg}", file=sys.stderr)
    if st.graph is None:
        return 1
    folder = folder or Path(tempfile.gettempdir()) / f"design-{bid}"
    folder.mkdir(parents=True, exist_ok=True)
    found = []
    print("seed  score")
    for seed in range(1, seeds + 1):
        out = st.run(seed, folder)
        if isinstance(out, str):
            print(f"{seed:<4}  -      {out.splitlines()[0]}")
            continue
        score, note = settle_score(out)
        found.append((score, seed))
        print(f"{seed:<4}  {score:<5}  {note}")
    if not found:
        return 1
    kept = [s for _, s in sorted(found, key=lambda f: (-f[0], f[1]))[:keep]]
    panels = []
    for s in kept:
        maps.artgen("settlement", "render", "--file", folder / f"seed-{s}.json", "--format", "svg", "--fit", "800x800px", "--out", folder)
        panels.append((s, maps.own_ids((folder / f"seed-{s}.color.svg").read_text(), f"s{s}")))
    body = ""
    for i, (s, svg) in enumerate(panels):
        svg = re.sub(r'(<svg\b[^>]*?)\s(width|height)="[^"]*"', r"\1", re.sub(r'(<svg\b[^>]*?)\s(width|height)="[^"]*"', r"\1", svg, count=1), count=1)
        body += svg.replace("<svg ", f'<svg x="{i * 820 + 10}" y="40" width="800" height="800" ', 1)
        body += f'<text x="{i * 820 + 10}" y="26" font-family="sans-serif" font-size="20">seed {s} - score {dict((b, a) for a, b in found)[s]}</text>'
    sheet = folder / "contact.svg"
    sheet.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{len(panels) * 820 + 10}" height="860" style="background:#fff">{body}</svg>')
    print(f"\n{len(found)} of {seeds} seeds laid out. Contact sheet: {sheet}\nThen: python3 tools/design.py accept {region.code} {bid} --seed N")
    return 0


def settle_accept(region, bid: str, seed: int) -> int:
    st = Settle(region, bid)
    for path, msg in st.problems:
        print(f"ERROR: {path.relative_to(tables.ROOT)}: {msg}", file=sys.stderr)
    if st.graph is None:
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        out = st.run(seed, Path(tmp))
    if isinstance(out, str):
        print(f"{bid}: seed {seed}: {out}")
        return 1
    score, _ = settle_score(out)
    lines = [f'Place {c} xyz="{x},{y}" outline="rect {w} {l}" shape=rect' for c, (x, y, w, l) in st.places(out).items()]
    write_places(region, bid, st.locations, lines, seed, score, None, f"{len(lines)} places")
    return 0


def settle_apply(region) -> list[str]:
    """An approved SAFE or WILD design's places into Locations.md: each location's `xyz`, its Place's, in place of
    any bearing and distance."""
    done, path = [], region.dir / "Locations.md"
    places = {c: p for g in groups(region).values() if g["design"].props.get("approved") for c, p in g["places"].items()}
    text = []
    for line in path.read_text().splitlines():
        m = re.match(r"Location (\S+) ", line)
        if m and (p := places.get(m[1])) and 'at="way in"' not in line:   # the way in is its place already
            had = space.point_of(re.search(r'xyz="([^"]*)"', line)[1]) if 'xyz="' in line else None
            up = f",{had[2]:g}" if had and len(had) > 2 and had[2] else ""     # its height stays the tables'
            for k in ("bearing", "distance", "against"):
                line = dungeon.without(line, k)
            line = dungeon.with_prop(line, "xyz", f'"{p.props["xyz"]}{up}"')
            done.append(f"{m[1]}: placed")
        text.append(line)
    path.write_text("\n".join(text) + "\n")
    return done


# -- the design and its tables ---------------------------------------------------------

TOL = 0.5                       # feet two places may differ by and agree
SHARED = 5                      # feet of wall two rooms must share to hold a door


def groups(region) -> dict[str, dict]:
    """A region's Design.md by block: its Design line, and every other line stating that block, a Place and a Link by the
    block whose locations they name."""
    out = {str(n.args[0]): {"design": n, "lines": [], "places": {}, "links": []}
           for n in region.files.get("Design", []) if n.name == "Design" and n.args}
    owner = {c: bid for bid, g in out.items() for c in words(g["design"].props.get("locations"))}
    for n in region.files.get("Design", []):
        if not n.args or n.name == "Design":
            continue
        bid = owner.get(str(n.args[0])) if n.name in ("Place", "Link", "Part") else str(n.args[0])
        if bid in out:
            out[bid]["lines"].append(n)
            if n.name == "Place":
                out[bid]["places"][str(n.args[0])] = n
            elif n.name == "Link":
                out[bid]["links"].append(n)
    return out


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
    return any(abs(d[k] - reach[k]) <= TOL * 5 and d[1 - k] < reach[1 - k] - SHARED for k in (0, 1))


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
                             f"{', '.join(sorted(members, key=dungeon.number))} in its design - owed to step 3f, or 3e if the design is wrong"))
    mine = {}
    for c in sorted(members, key=dungeon.number):
        p = g["places"].get(c)
        if p is None:
            out.append(("error", f"the design approves {bid} and places no {c}: solve and accept it - owed to step 3e"))
            continue
        want = space.point_of(p.props.get("xyz"))
        size = box(space.outline_value(p.props.get("outline")))
        mine[c] = {"at": want[:2], "w": size[0], "l": size[1]}
        have, owes = (dress.get(c), "4a") if danger else (locs.get(c), "3e")        # a DANGEROUS room's place is its Dressing's
        if c not in locs or have is None:
            out.append(("warning", f"{c} is not in {'Locations.md' if c not in locs else 'Dressing.md'} yet, and the design places it - "
                                   f"owed to step {'3d' if c not in locs else '4a'}"))
            continue
        got = space.point_of(have.props.get("xyz")) if danger else list(space.offset(region, have) or []) or None
        if got is None or math.dist(got[:2], want[:2]) > TOL:
            out.append(("error", f"{c} lies at {at(got)} in the tables and at {at(want)} in the design: run `python3 tools/design.py apply {region.code}` (step {owes}), or 3e if the design is wrong"))
        d = dress.get(c)
        if d is not None and "width" in d.props and "length" in d.props:
            if abs(float(d.props["width"]) - size[0]) > TOL or abs(float(d.props["length"]) - size[1]) > TOL:
                out.append(("error", f"{c} is {d.props['width']} by {d.props['length']} in Dressing.md and {size[0]:g} by {size[1]:g} in the design - owed to step 4a, or 3e if the design is wrong"))
        if str(d.props.get("shape", "rect") if d is not None else "rect") != str(p.props.get("shape", "rect")):
            out.append(("error", f"{c} is shape {d.props.get('shape', 'rect') if d is not None else 'rect'} in Dressing.md and {p.props.get('shape', 'rect')} in the design - owed to step 4a, or 3e if the design is wrong"))
    wanted = {}
    for n in g["links"]:
        a, b = str(n.args[0]), str(n.props.get("to"))
        wanted[frozenset((a, b))] = (a, b, str(n.props.get("kind")))
        if str(n.props.get("kind")) == "door" and a in mine and b in mine and not touching(mine[a], mine[b]):
            out.append(("error", f"the design joins {a} and {b} by a door, and they share no wall - owed to step 3e"))
    stated = {(str(n.args[0]), str(n.props["to"])) for n in ways if str(n.args[0]) in members and str(n.props["to"]) in members}
    for k, (a, b, _) in wanted.items():
        for x, y in ((a, b), (b, a)):
            if (x, y) not in stated:
                unwritten = not any(c in q for q in stated for c in (x, y))     # neither end has a way yet: owed, not wrong
                out.append(("warning" if unwritten else "error",
                            f"the design joins {a} and {b}, and Connections.md lacks {x} to {y} - owed to step 3f"))
    for x, y in sorted(stated) if danger else []:          # only a plan states its ways, as Links
        if frozenset((x, y)) not in wanted:
            out.append(("error", f"Connections.md joins {x} and {y}, which the design does not - owed to step 3f, or 3e if the design lacks it"))
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
    """Every region's designs and tables against one another: (level, file, message). A DANGEROUS region, or one whose
    BRIEF.md node asks for a design, that has its locations and no approved design is owed to step 3e; each approved
    design is held to the tables."""
    out = []
    for code, region in world.regions.items():
        path = region.dir / "Design.md"
        made = groups(region)
        danger = region.rating.upper() == "DANGEROUS"
        if (danger or code in brief.designs) and (region.dir / "Locations.md").exists() \
                and not any(g["design"].props.get("approved") for g in made.values()):
            why = "a DANGEROUS region's blocks are planned" if danger else f"BRIEF.md asks region {code} for a design"
            out.append(("warning", path if path.exists() else region.dir, f"{why}, and none is approved - owed to step 3e"))
        for bid, g in made.items():
            node, approved = g["design"], bool(g["design"].props.get("approved"))
            for k in SETTINGS:
                if k in node.props and (bad := tables.design_setting(k, str(node.props[k]))):
                    out.append(("error", path, f"line {node.line}: Design {bid} {bad}"))
            for n in (n for n in g["lines"] if n.name == "Fabric"):
                if str(n.props.get("kind")) not in maps.BUILDING_KINDS:
                    out.append(("error", path, f"line {n.line}: Fabric {bid} kind is a building kind: {' | '.join(maps.BUILDING_KINDS)} - step 3e"))
                if not any(m.name == "Street" for m in g["lines"]):
                    out.append(("warning", path, f"line {n.line}: Fabric {bid} lines the design's streets, and it has none - step 3e"))
            if region.rating.upper() == "DANGEROUS" and bid in plan.plans_of(region):   # a plan: its faults, and ways it leaves unrouted
                said, unrouted = plan.problems_of(region, bid)
                out += [("error" if approved else "warning", path, f"Design {bid}: {m} - owed to step 3e") for m in said + unrouted]
            elif region.rating.upper() == "DANGEROUS":
                out.append(("error", path, f"line {node.line}: Design {bid} holds no Room: a DANGEROUS block is designed as a plan - owed to step 3e"))
            if approved:
                out += [(level, path, msg) for level, msg in agree(region, bid, g)]
            if approved and region.rating.upper() == "DANGEROUS" and bid in plan.plans_of(region):
                out += [("warning", path, f"Design {bid}: {m}, the nearest a coherent layout allows - step 3e") for m in plan.goals_missed(region, bid)]
                out += sized(region, brief, bid, g["design"])
    return out


SIZE_SLACK = (10.0, 0.10)       # feet, and a share of the target: how far a level may span from BRIEF.md's footprint unremarked


def sized(region, brief, bid: str, node) -> list[tuple[str, Path, str]]:
    """A planned level's drawn span against BRIEF.md's `footprint` for its region: a target the design meets as nearly
    as a readable layout allows, so a miss is a warning."""
    want = brief.footprint(region.code)
    m = plan.block_map(region, node)[0] if want else None
    if m is None:
        return []
    w, h = plan.span(m)
    if abs(max(w, h) - want) <= max(SIZE_SLACK[0], SIZE_SLACK[1] * want):
        return []
    return [("warning", region.dir / "Design.md", f"Design {bid} spans {w:g} by {h:g} feet, where BRIEF.md's footprint asks "
             f"about {want:g}: shape the plan nearer it where the layout stays readable - step 3e")]


# -- the commands ----------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="command", required=True)
    free = dict(action="store_true", help="a plan: ignore the places of the levels a stair joins, which are placed after this one")
    v = sub.add_parser("solve", help="a plan drawn; a settlement's N seeds laid out and scored, the best K on a contact sheet")
    v.add_argument("code")
    v.add_argument("block", nargs="?", help="a block id, where the region has designs for several")
    v.add_argument("--seeds", type=int, default=12)
    v.add_argument("--keep", type=int, default=3)
    v.add_argument("--out", type=Path, help="where the drawings go; default a folder of the system's temporary directory")
    v.add_argument("--free", **free)
    a = sub.add_parser("accept", help="write the places into Design.md")
    a.add_argument("code")
    a.add_argument("block", nargs="?")
    a.add_argument("--seed", type=int, help="a settlement's seed to accept; a plan takes none")
    a.add_argument("--free", **free)
    y = sub.add_parser("apply", help="an approved design's places into the tables")
    y.add_argument("code")
    c = sub.add_parser("check", help="every approved design against its tables")
    c.add_argument("code", nargs="?")
    args = ap.parse_args()
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
    danger = region.rating.upper() == "DANGEROUS"
    if args.command == "apply":
        done = plan.apply(args.code) if danger else settle_apply(region)
        print("\n".join(done) or f"{args.code} holds no approved design")
        return 0
    blocks = [str(n.args[0]) for n in region.files.get("Design", []) if n.name == "Design" and n.args]
    bid = args.block or (blocks[0] if len(blocks) == 1 else None)
    if bid is None:
        print(f"ERROR: {args.code} holds {'no design' if not blocks else 'designs for ' + ', '.join(blocks) + ': name one'}", file=sys.stderr)
        return 1
    if danger:                                           # a plan is solved by tools/plan.py
        if bid not in plan.plans_of(region):
            print(f"ERROR: Design {bid} holds no Room: a DANGEROUS block is designed as a plan (the block-plan skill)", file=sys.stderr)
            return 1
        return plan.main([args.command, args.code, bid] + (["--out", str(args.out)] if getattr(args, "out", None) else [])
                         + (["--free"] if args.free else []))
    if args.command == "solve":
        return settle_solve(region, bid, args.seeds, args.keep, args.out)
    if args.seed is None:
        print("ERROR: accept takes --seed N", file=sys.stderr)
        return 1
    return settle_accept(region, bid, args.seed)


if __name__ == "__main__":
    sys.exit(main())
