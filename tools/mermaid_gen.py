#!/usr/bin/env python3
"""Derive every diagram tier from the ``connections.md`` tables.

Nothing in the diagram layer is hand-authored. Two tables are the whole input:
``setting/connections.md`` holds region-to-region edges, and each region's
``connections.md`` holds location-to-location edges. Everything drawn at any of
the five tiers is a projection of one of those two tables onto a container
membership, so a diagram cannot disagree with the graph it draws unless this
script is stale, and `validate.py` M11 re-derives every file to prove it is not.

Connection type is drawn at tier 4 and nowhere else (SPEC.md section 5.2).
Above tier 4 a connected pair gets one plain edge answering only whether they
connect, because a setting diagram carrying twelve typed edges between two
regions is unreadable. `validate.py` M12 checks that from the other side.

Tier 4 is also the one tier that draws outside its own frame: where an edge
leaves the container, the destination location is drawn outside the frame so a
referee reading one container's diagram can see where its exits go. Tiers 2 and
3 do not, because tier 1 already answers cross-container connectivity and the
tier below always redraws the same edge in full.

Tier 5 is a location. It is the leaf and it has no diagram.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402

RE_NODE_ID = re.compile(r"[^A-Za-z0-9]+")

HEADER = "flowchart TD"

# A container id and a region code cannot collide today, but a container named
# `r03` would, and the collision would silently merge two nodes into one. The
# prefix costs nothing and removes the class of bug.
CONTAINER_PREFIX = "C_"


class MermaidError(Exception):
    """A diagram could not be derived."""


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Node:
    """One box. ``key`` is what edges are written in terms of."""

    key: str
    label: str

    @property
    def ident(self) -> str:
        return RE_NODE_ID.sub("_", self.key).strip("_").upper()


@dataclass(frozen=True)
class Link:
    """One drawn edge. ``kind`` is empty above tier 4, where type is not drawn."""

    source: str
    target: str
    kind: str = ""
    one_way: bool = False

    def sort_key(self) -> tuple[str, str, str]:
        return (self.source, self.target, self.kind)


def _escape(text: str) -> str:
    """Make a name safe inside a quoted mermaid label."""
    return text.replace('"', "'").replace("\n", " ").strip()


def _node_line(node: Node, indent: str = "    ") -> str:
    return f'{indent}{node.ident}["{_escape(node.label)}"]'


def _link_line(link: Link, nodes: dict[str, Node], indent: str = "    ") -> str:
    source = nodes[link.source].ident
    target = nodes[link.target].ident
    arrow = "-->" if link.one_way else "---"
    if link.kind:
        return f"{indent}{source} {arrow}|{_escape(link.kind)}| {target}"
    return f"{indent}{source} {arrow} {target}"


def render(
    note: str,
    nodes: list[Node],
    links: list[Link],
    frame: tuple[str, str] | None = None,
    inside: set[str] | None = None,
) -> str:
    """One diagram file: a comment naming its source, then one mermaid block.

    ``frame`` draws a subgraph around the members named in ``inside``. Only
    tier 4 passes it, because only tier 4 draws nodes that are not its own.
    """
    index = {node.key: node for node in nodes}
    lines = [HEADER, f"%% {note}", "%% Derived by tools/mermaid_gen.py. Do not edit."]

    if not nodes:
        lines.append('    EMPTY["Nothing to draw yet"]')
    elif frame is None:
        lines += [_node_line(node) for node in nodes]
    else:
        frame_id, frame_label = frame
        inside = inside or set()
        lines.append(f'    subgraph {RE_NODE_ID.sub("_", frame_id).upper()}'
                     f'["{_escape(frame_label)}"]')
        members = [node for node in nodes if node.key in inside]
        if members:
            lines += [_node_line(node, indent="        ") for node in members]
        else:
            lines.append('        EMPTY["No members yet"]')
        lines.append("    end")
        lines += [_node_line(node) for node in nodes if node.key not in inside]

    lines += [_link_line(link, index) for link in links]
    return "```mermaid\n" + "\n".join(lines) + "\n```\n"


# --------------------------------------------------------------------------
# Derivation
# --------------------------------------------------------------------------


def _containers(doc: common.Doc | None) -> list[tuple[str, str]]:
    """A holder's declared containers, as ``(id, name)`` in declared order."""
    if doc is None:
        return []
    entries: list[tuple[str, str]] = []
    for entry in doc.fm.get("containers", []) or []:
        if isinstance(entry, dict) and "id" in entry:
            entries.append((str(entry["id"]), str(entry.get("name", entry["id"]))))
    return entries


def _binary(pairs: set[tuple[str, str]]) -> list[Link]:
    """Untyped edges, deduplicated and orientation-free. Tiers 1 to 3."""
    unique = {tuple(sorted(pair)) for pair in pairs if pair[0] != pair[1]}
    return [Link(source, target) for source, target in sorted(unique)]


def _lift(edges: list[common.Edge], group: dict[str, str]) -> set[tuple[str, str]]:
    """Project node-to-node edges onto the containers holding them.

    An edge whose ends share a container disappears at the tier above, which is
    the point: that tier draws the containers, and the edge is drawn in full one
    tier down.
    """
    lifted: set[tuple[str, str]] = set()
    for edge in edges:
        source = group.get(edge.source)
        target = group.get(edge.target)
        if source and target and source != target:
            lifted.add((source, target))
    return lifted


def derive(corpus: common.Corpus) -> dict[str, str]:
    """Every diagram the corpus implies, as filename to file contents.

    This is the whole contract with `validate.py` M11: the files on disk are
    correct exactly when they are what this function returns.
    """
    diagrams: dict[str, str] = {}
    setting = corpus.setting

    setting_containers = _containers(setting)
    region_container = {
        code: str(doc.fm.get("container", ""))
        for code, doc in corpus.regions.items()
    }
    region_edges = common.edges_from(corpus.setting_connections)

    # -- tier 1, the setting -------------------------------------------
    nodes = [Node(ident, name) for ident, name in setting_containers]
    diagrams[common.diagram_name(1, "SETTING")] = render(
        f"Tier 1. The setting: {len(nodes)} setting-level containers, binary edges.",
        [Node(CONTAINER_PREFIX + n.key, n.label) for n in nodes],
        [
            Link(CONTAINER_PREFIX + link.source, CONTAINER_PREFIX + link.target)
            for link in _binary(_lift(region_edges, region_container))
        ],
    )

    # -- tier 2, one per setting-level container ------------------------
    for ident, name in setting_containers:
        members = sorted(
            code for code, holder in region_container.items() if holder == ident
        )
        nodes = [
            Node(code, f"{code} {corpus.regions[code].fm.get('name', '')}".strip())
            for code in members
        ]
        held = set(members)
        links = _binary(
            {
                (edge.source, edge.target)
                for edge in region_edges
                if edge.source in held and edge.target in held
            }
        )
        diagrams[common.diagram_name(2, ident)] = render(
            f"Tier 2. Container {ident}: the regions inside it, binary edges.",
            nodes,
            links,
        )

    # -- tiers 3 and 4, one region at a time ----------------------------
    for region_code, region in sorted(corpus.regions.items()):
        locations = {doc.code: doc for doc in corpus.locations_in(region_code)}
        location_container = {
            code: str(doc.fm.get("container", "")) for code, doc in locations.items()
        }
        location_edges = common.edges_from(corpus.region_connections.get(region_code))
        region_containers = _containers(region)

        # Tier 3: the region's own containers, binary.
        nodes = [Node(CONTAINER_PREFIX + ident, name) for ident, name in region_containers]
        links = [
            Link(CONTAINER_PREFIX + link.source, CONTAINER_PREFIX + link.target)
            for link in _binary(_lift(location_edges, location_container))
        ]
        known = {node.key for node in nodes}
        diagrams[common.diagram_name(3, region_code)] = render(
            f"Tier 3. Region {region_code}: the region-level containers inside it, "
            f"binary edges.",
            nodes,
            [link for link in links if link.source in known and link.target in known],
        )

        # Tier 4: one per region-level container, typed, and drawing the
        # destinations its edges reach outside the frame.
        for ident, name in region_containers:
            inside = sorted(
                code for code, holder in location_container.items() if holder == ident
            )
            held = set(inside)
            touching = [
                edge
                for edge in location_edges
                if edge.source in held or edge.target in held
            ]
            outside = sorted(
                {
                    code
                    for edge in touching
                    for code in (edge.source, edge.target)
                    if code not in held and code in locations
                }
            )
            nodes = [
                Node(code, f"{code} {locations[code].fm.get('name', '')}".strip())
                for code in inside + outside
            ]
            drawn = {node.key for node in nodes}
            links = sorted(
                {
                    Link(edge.source, edge.target, edge.kind, edge.one_way)
                    for edge in touching
                    if edge.source in drawn and edge.target in drawn
                    and edge.source != edge.target
                },
                key=Link.sort_key,
            )
            diagrams[common.diagram_name(4, region_code, ident)] = render(
                f"Tier 4. Container {ident} of {region_code}: its locations, "
                f"typed edges, and the destinations they reach outside it.",
                nodes,
                links,
                frame=(ident, name),
                inside=held,
            )

    return diagrams


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def write(root: Path, diagrams: dict[str, str]) -> tuple[list[str], list[str], list[str]]:
    """Write every derived diagram and delete anything else in the directory.

    The directory is derived output in full. A file left behind after its
    container was renamed draws a grouping that no longer exists, and M11
    reports it, so the regeneration removes it rather than reporting it twice.
    """
    directory = root / common.DIAGRAMS_DIR
    directory.mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    unchanged: list[str] = []
    for name, text in sorted(diagrams.items()):
        path = directory / name
        if path.exists() and path.read_text(encoding="utf-8") == text:
            unchanged.append(name)
            continue
        path.write_text(text, encoding="utf-8")
        written.append(name)

    removed: list[str] = []
    for path in sorted(directory.glob("*.md")):
        if path.name not in diagrams:
            path.unlink()
            removed.append(path.name)

    return written, unchanged, removed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", type=Path, default=common.REPO_ROOT)
    parser.add_argument("--check", action="store_true",
                        help="fail if any file on disk is not what the tables imply")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    try:
        diagrams = derive(common.load_corpus(root))
    except (MermaidError, common.DocError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    directory = root / common.DIAGRAMS_DIR
    if args.check:
        stale: list[str] = []
        for name, text in sorted(diagrams.items()):
            path = directory / name
            if not path.exists():
                stale.append(f"{name} has not been derived")
            elif path.read_text(encoding="utf-8") != text:
                stale.append(f"{name} differs from what the tables imply")
        if directory.is_dir():
            for path in sorted(directory.glob("*.md")):
                if path.name not in diagrams:
                    stale.append(f"{path.name} is derived from no table")
        if stale:
            for problem in stale:
                print(f"error: {problem}", file=sys.stderr)
            print("error: run python tools/mermaid_gen.py.", file=sys.stderr)
            return 1
        print(f"{common.DIAGRAMS_DIR} is current: {len(diagrams)} diagrams.")
        return 0

    written, unchanged, removed = write(root, diagrams)
    for name in removed:
        print(f"removed {common.DIAGRAMS_DIR}/{name}")
    for name in written:
        print(f"wrote {common.DIAGRAMS_DIR}/{name}")
    print(f"{len(diagrams)} diagrams: {len(written)} written, {len(unchanged)} unchanged, "
          f"{len(removed)} removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
