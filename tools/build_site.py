#!/usr/bin/env python3
"""Builds the static, hyperlinked web view of setting/ into an output directory.

Usage: python3 tools/build_site.py [--out _site]

Pure standard library - no external dependencies. Every page is a plain
static .html file with relative links, so the output works unmodified from
any subpath (a GitHub Pages project site included) and from a local
`file://` open. Run tools/build_pdf.py afterwards (or before - order does
not matter) to add the downloadable PDF into the same output directory.
"""
from __future__ import annotations

import argparse
import html
import os
import re
import shutil
from pathlib import Path

import site_common as sc

ROOT = sc.ROOT
ASSETS_SRC = Path(__file__).resolve().parent / "site_assets"

REGISTRY_FILE_NAMES = {
    "lore": "lore.html",
    "keys": "keys.html",
    "named_creatures": "named-creatures.html",
    "unique_treasures": "unique-treasures.html",
}
REGISTRY_PAGE_TITLES = {
    "lore": "Lore",
    "keys": "Keys",
    "named_creatures": "Named Creatures",
    "unique_treasures": "Unique Treasures",
}

NAV_LINKS = [
    ("index.html", "Home"),
    ("history.html", "History"),
    ("truths.html", "Truths"),
    ("rumours.html", "Rumours"),
    ("bestiary.html", "Bestiary"),
    ("factions.html", "Factions"),
    ("treasure.html", "Treasure"),
    ("lore.html", "Lore"),
    ("keys.html", "Keys"),
    ("named-creatures.html", "Named Creatures"),
    ("unique-treasures.html", "Unique Treasures"),
]


def pdf_filename(setting: sc.Setting) -> str:
    return f"{sc.slugify(setting.name)}.pdf"


# ---------------------------------------------------------------------------
# Link resolver
# ---------------------------------------------------------------------------

class SiteLinkResolver(sc.LinkResolver):
    def target(self, kind: str, *args) -> tuple[str, str | None]:
        """Return (site-root-relative file path, anchor-or-None) for a target."""
        if kind == "location":
            region, num = args
            return f"region/{region}/{num}.html", None
        if kind == "region":
            (code,) = args
            return f"region/{code}/index.html", None
        if kind in REGISTRY_FILE_NAMES:
            (title,) = args
            return REGISTRY_FILE_NAMES[kind], f"{kind}-{sc.slugify(title)}"
        if kind == "treasure":
            (roman,) = args
            return "treasure.html", f"treasure-{roman}"
        if kind == "bestiary":
            (name,) = args
            return "bestiary.html", f"bestiary-{sc.slugify(name)}"
        raise ValueError(f"unknown link kind {kind!r}")

    def href(self, kind: str, *args) -> str | None:
        *target_args, current_page = args
        file_path, anchor = self.target(kind, *target_args)
        current_dir = os.path.dirname(current_page)
        rel = os.path.relpath(file_path, current_dir) if current_dir else file_path
        rel = rel.replace(os.sep, "/")
        return f"{rel}#{anchor}" if anchor else rel


RESOLVER = SiteLinkResolver()


def rel_asset(current_page: str, asset_path: str) -> str:
    current_dir = os.path.dirname(current_page)
    rel = os.path.relpath(asset_path, current_dir) if current_dir else asset_path
    return rel.replace(os.sep, "/")


# ---------------------------------------------------------------------------
# HTML page shell
# ---------------------------------------------------------------------------

def render_inline(text: str, setting: sc.Setting, current_page: str, skip_location: str | None = None,
                   no_links: bool = False) -> str:
    return sc.render_inline(text, setting, RESOLVER, current_page, skip_location=skip_location, no_links=no_links)


def nav_html(setting: sc.Setting, current_page: str) -> str:
    items = []
    for href, label in NAV_LINKS:
        rel = rel_asset(current_page, href)
        active = " class=\"active\"" if href == current_page else ""
        items.append(f'<li><a href="{rel}"{active}>{label}</a></li>')

    region_items = []
    for code in setting.region_order:
        region = setting.regions[code]
        rel = RESOLVER.href("region", code, current_page)
        region_items.append(f'<li><a href="{rel}">{code} {html.escape(region.name)}</a></li>')

    pdf_rel = rel_asset(current_page, pdf_filename(setting))
    search_rel = rel_asset(current_page, "search-index.json")

    return f"""
<header class="site-header">
  <div class="header-bar">
    <a class="brand" href="{rel_asset(current_page, 'index.html')}">{html.escape(setting.name)}</a>
    <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
  <nav class="site-nav">
    <ul class="nav-list">
      {''.join(items)}
      <li class="nav-dropdown">
        <button class="dropdown-toggle" aria-expanded="false">Regions ▾</button>
        <ul class="dropdown-menu">{''.join(region_items)}</ul>
      </li>
      <li><a class="pdf-link" href="{pdf_rel}" download>⬇ Download PDF</a></li>
    </ul>
    <div class="nav-search">
      <input type="search" id="site-search" placeholder="Search the setting…" autocomplete="off"
             data-index="{search_rel}">
      <ul id="search-results" class="search-results" hidden></ul>
    </div>
  </nav>
</header>
"""


def page_shell(setting: sc.Setting, current_page: str, title: str, body: str, description: str = "") -> str:
    css_rel = rel_asset(current_page, "assets/style.css")
    js_rel = rel_asset(current_page, "assets/app.js")
    full_title = f"{title} — {setting.name}" if title != setting.name else title
    desc = html.escape(description or setting.outline[:200])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{css_rel}">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body>
{nav_html(setting, current_page)}
<main class="page">
{body}
</main>
<footer class="site-footer">
  <p>{html.escape(setting.name)} — generated from <code>setting/</code> by <code>tools/build_site.py</code>.</p>
</footer>
<script src="{js_rel}"></script>
</body>
</html>
"""


def write_page(out_dir: Path, page_path: str, html_text: str) -> None:
    dest = out_dir / page_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_text, encoding="utf-8")


def section(title: str, body: str, anchor: str | None = None) -> str:
    id_attr = f' id="{anchor}"' if anchor else ""
    return f'<section class="doc-section"{id_attr}><h2>{html.escape(title)}</h2>{body}</section>'


def mermaid_block(mmd_text: str, extra_lines: list[str] | None = None) -> str:
    text = mmd_text
    if extra_lines:
        text = text.rstrip() + "\n" + "\n".join(extra_lines) + "\n"
    return f'<div class="diagram"><pre class="mermaid">{html.escape(text)}</pre></div>'


def region_graph_clicks(mmd_text: str, region_code: str, current_page: str) -> list[str]:
    lines = []
    id_to_code: dict[str, str] = {}
    for m in sc.NODE_RE.finditer(mmd_text):
        id_to_code[m.group(1)] = m.group(2)
    for node_id, code in id_to_code.items():
        if "." not in code:
            continue
        rcode, num = code.split(".", 1)
        href = RESOLVER.href("location", rcode, int(num), current_page)
        lines.append(f'    click {node_id} "{href}" "{code}"')
    return lines


def top_graph_clicks(mmd_text: str, current_page: str) -> list[str]:
    lines = []
    id_to_code: dict[str, str] = {}
    for m in sc.NODE_RE.finditer(mmd_text):
        id_to_code[m.group(1)] = m.group(2)
    for node_id, code in id_to_code.items():
        href = RESOLVER.href("region", code, current_page)
        lines.append(f'    click {node_id} "{href}" "{code}"')
    return lines


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def build_index(setting: sc.Setting, out: Path) -> None:
    page = "index.html"
    tags = " · ".join(t.strip() for t in setting.tags.split(","))
    body = [f'<h1>{html.escape(setting.name)}</h1>']
    body.append(f'<p class="tags">{html.escape(tags)}</p>')
    body.append(f'<p class="outline">{render_inline(setting.outline, setting, page)}</p>')

    cards = []
    for href, label in NAV_LINKS[1:]:
        cards.append(f'<a class="card" href="{rel_asset(page, href)}">{label}</a>')
    body.append(f'<div class="card-grid">{"".join(cards)}</div>')

    region_rows = []
    for code in setting.region_order:
        r = setting.regions[code]
        rtags = " · ".join(t.strip() for t in r.tags.split(","))
        href = RESOLVER.href("region", code, page)
        region_rows.append(
            f'<a class="region-row" href="{href}">'
            f'<div class="region-code">{code}</div>'
            f'<div><div class="region-name">{html.escape(r.name)} '
            f'<span class="badge badge-{r.rating.lower()}">{r.rating} {r.die}</span></div>'
            f'<div class="region-tags">{html.escape(rtags)}</div>'
            f'<div class="region-blurb">{render_inline(r.gazetteer_blurb, setting, page, no_links=True)}</div></div>'
            f'</a>'
        )
    body.append(section("Regions", f'<div class="region-list">{"".join(region_rows)}</div>'))

    clicks = top_graph_clicks(setting.top_connections, page)
    body.append(section("Region Connections", mermaid_block(setting.top_connections, clicks)))

    write_page(out, page, page_shell(setting, page, setting.name, "\n".join(body)))


def build_history(setting: sc.Setting, out: Path) -> None:
    page = "history.html"
    rows = []
    for when, text in setting.history:
        rows.append(
            f'<li><span class="when">{html.escape(when)}</span>'
            f'<span class="event">{render_inline(text, setting, page)}</span></li>'
        )
    body = f'<h1>History</h1><ol class="timeline">{"".join(rows)}</ol>'
    write_page(out, page, page_shell(setting, page, "History", body))


def build_truths(setting: sc.Setting, out: Path) -> None:
    page = "truths.html"
    items = "".join(f'<li>{render_inline(t, setting, page)}</li>' for t in setting.truths)
    body = f'<h1>Truths</h1><ul class="truths-list">{items}</ul>'
    write_page(out, page, page_shell(setting, page, "Truths", body))


def build_rumours(setting: sc.Setting, out: Path) -> None:
    page = "rumours.html"
    rows = []
    label = {"T": "True", "P": "Partly true", "F": "False"}
    for n, text, tpf in setting.rumours:
        cls = {"T": "tpf-true", "P": "tpf-partial", "F": "tpf-false"}.get(tpf, "")
        rows.append(
            f'<tr><td class="num">{n}</td><td>{render_inline(text, setting, page)}</td>'
            f'<td class="tpf {cls}" title="{label.get(tpf, tpf)}">{tpf}</td></tr>'
        )
    body = (
        '<h1>Rumours</h1>'
        '<p class="hint">Referee reference — hover a mark for what it means. Players hear the rumour, not the mark.</p>'
        '<table class="data-table"><thead><tr><th>#</th><th>Rumour</th><th>T/P/F</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
    )
    write_page(out, page, page_shell(setting, page, "Rumours", body))


def build_bestiary(setting: sc.Setting, out: Path) -> None:
    page = "bestiary.html"
    cards = []
    for creature in setting.bestiary:
        anchor = f"bestiary-{sc.slugify(creature['name'])}"
        cards.append(
            f'<article class="stat-card" id="{anchor}">'
            f'<h3>{html.escape(creature["name"])} <span class="kind">({html.escape(creature["kind"])})</span></h3>'
            f'<p class="ad">AD: {html.escape(creature["ad"])}</p>'
            f'<p>{render_inline(creature["description"], setting, page)}</p>'
            f'</article>'
        )
    body = f'<h1>Bestiary</h1><div class="stat-grid">{"".join(cards)}</div>'
    write_page(out, page, page_shell(setting, page, "Bestiary", body))


def build_factions(setting: sc.Setting, out: Path) -> None:
    page = "factions.html"
    cards = []
    for faction in setting.factions:
        rows = "".join(
            f'<tr><th>{html.escape(k)}</th><td>{render_inline(v, setting, page)}</td></tr>'
            for k, v in faction["fields"]
        )
        cards.append(
            f'<article class="faction-card">'
            f'<h3>{html.escape(faction["name"])} <span class="ad">AD: {html.escape(faction["ad"])}</span></h3>'
            f'<table class="kv-table">{rows}</table>'
            f'</article>'
        )
    body = f'<h1>Factions</h1><div class="faction-list">{"".join(cards)}</div>'
    write_page(out, page, page_shell(setting, page, "Factions", body))


def build_treasure(setting: sc.Setting, out: Path) -> None:
    page = "treasure.html"
    sections = []
    for roman in ("I", "II", "III", "IV", "V"):
        rows = "".join(
            f'<tr><td class="num">{n}</td><td>{render_inline(item, setting, page)}</td>'
            f'<td>{html.escape(value)}</td><td>{html.escape(wt)}</td></tr>'
            for n, item, value, wt in setting.treasure[roman]
        )
        table = (
            f'<table class="data-table"><thead><tr><th>#</th><th>Item</th>'
            f'<th>Value (cn)</th><th>Wt</th></tr></thead><tbody>{rows}</tbody></table>'
        )
        sections.append(section(sc.TREASURE_TITLES[roman], table, anchor=f"treasure-{roman}"))
    body = f'<h1>Treasure Tables</h1>{"".join(sections)}'
    write_page(out, page, page_shell(setting, page, "Treasure", body))


def build_registry(setting: sc.Setting, out: Path, kind: str) -> None:
    page = REGISTRY_FILE_NAMES[kind]
    entries = getattr(setting, kind)
    cards = []
    for e in entries:
        anchor = f"{kind}-{sc.slugify(e.title)}"
        loc_links = ", ".join(
            f'<a href="{RESOLVER.href("location", c.split(".")[0], int(c.split(".")[1]), page)}">'
            f'{c} {html.escape(setting.all_locations[c].name)}</a>'
            for c in e.locations if c in setting.all_locations
        )
        marker = "Appears at" if kind == "named_creatures" else "Found at"
        typetag = render_inline(e.typetag, setting, page) if e.typetag else ""
        typetag_html = f'<span class="typetag">({typetag})</span>' if typetag else ""
        cards.append(
            f'<article class="registry-card" id="{anchor}">'
            f'<h3>{html.escape(e.title)} {typetag_html}</h3>'
            f'<p class="registry-location">{marker} {loc_links}</p>'
            f'<div class="registry-body">{render_inline(e.body, setting, page)}</div>'
            f'</article>'
        )
    title = REGISTRY_PAGE_TITLES[kind]
    empty = '<p class="hint">Nothing recorded yet.</p>' if not cards else ""
    body = f'<h1>{title}</h1>{empty}<div class="registry-list">{"".join(cards)}</div>'
    write_page(out, page, page_shell(setting, page, title, body))


def build_region(setting: sc.Setting, out: Path, code: str) -> None:
    region = setting.regions[code]
    page = f"region/{code}/index.html"
    tags = " · ".join(t.strip() for t in region.tags.split(","))

    body = [
        f'<p class="breadcrumb"><a href="{rel_asset(page, "index.html")}">Home</a> / Regions / {code}</p>',
        f'<h1>{code} {html.escape(region.name)} '
        f'<span class="badge badge-{region.rating.lower()}">{region.rating} {region.die}</span></h1>',
        f'<p class="tags">{html.escape(tags)}</p>',
    ]

    for label, text in region.fields:
        body.append(section(label, f'<p>{render_inline(text, setting, page)}</p>'))

    if region.table_rows:
        rows = "".join(
            f'<tr><td class="num">{n}</td><td>{render_inline(text, setting, page)}</td></tr>'
            for n, text in region.table_rows
        )
        table = f'<table class="data-table"><tbody>{rows}</tbody></table>'
        body.append(section(region.table_label, table))

    loc_rows = []
    for num in sorted(region.locations):
        loc = region.locations[num]
        href = RESOLVER.href("location", code, num, page)
        weight = f'<span class="badge badge-weight-{loc.weight}">{loc.weight}</span>' if loc.weight else ""
        ltags = " · ".join(t.strip() for t in loc.tags.split(","))
        loc_rows.append(
            f'<a class="location-row" href="{href}">'
            f'<span class="loc-code">{loc.code}</span>'
            f'<span class="loc-name">{html.escape(loc.name)} {weight}</span>'
            f'<span class="loc-tags">{html.escape(ltags)}</span>'
            f'</a>'
        )
    body.append(section("Locations", f'<div class="location-list">{"".join(loc_rows)}</div>'))

    cpath = sc.SETTING / "region" / code / "Connections.mmd"
    mmd_text = sc.load_mmd(cpath)
    if mmd_text.strip():
        clicks = region_graph_clicks(mmd_text, code, page)
        body.append(section("Connections", mermaid_block(mmd_text, clicks)))

    write_page(out, page, page_shell(setting, page, f"{code} {region.name}", "\n".join(body)))


def build_location(setting: sc.Setting, out: Path, code: str, num: int) -> None:
    region = setting.regions[code]
    loc = region.locations[num]
    page = f"region/{code}/{num}.html"

    region_href = RESOLVER.href("region", code, page)
    body = [
        f'<p class="breadcrumb"><a href="{rel_asset(page, "index.html")}">Home</a> / '
        f'<a href="{region_href}">{code} {html.escape(region.name)}</a> / {loc.code}</p>',
    ]
    weight = f' <span class="badge badge-weight-{loc.weight}">{loc.weight}</span>' if loc.weight else ""
    tags = " · ".join(t.strip() for t in loc.tags.split(","))
    body.append(f'<h1>{loc.code} {html.escape(loc.name)}{weight}</h1>')
    body.append(f'<p class="tags">{html.escape(tags)}</p>')
    body.append(f'<p class="player-summary">{render_inline(loc.player_summary, setting, page, skip_location=loc.code)}</p>')
    body.append(f'<p class="referee-notes">{render_inline(loc.referee_notes, setting, page, skip_location=loc.code)}</p>')

    feature_items = "".join(
        f'<li><span class="feature-label">{html.escape(label)}:</span> '
        f'{render_inline(text, setting, page, skip_location=loc.code)}</li>'
        for label, text in loc.features
    )
    body.append(f'<ul class="feature-list">{feature_items}</ul>')

    if loc.exits:
        exit_items = []
        for approach, ecode, ename in loc.exits:
            eregion = ecode.split(".")[0]
            enum = int(ecode.split(".")[1])
            href = RESOLVER.href("location", eregion, enum, page)
            exit_items.append(
                f'<li>{render_inline(approach, setting, page, skip_location=loc.code)} '
                f'&rarr; <a href="{href}">{ecode} {html.escape(ename)}</a></li>'
            )
        body.append(section("Exits", f'<ul class="exit-list">{"".join(exit_items)}</ul>'))
    else:
        body.append(section("Exits", '<p class="hint">None.</p>'))

    write_page(out, page, page_shell(setting, page, loc.code + " " + loc.name, "\n".join(body)))


# ---------------------------------------------------------------------------
# Search index
# ---------------------------------------------------------------------------

def build_search_index(setting: sc.Setting, out: Path) -> None:
    import json

    entries = []
    for code in setting.region_order:
        region = setting.regions[code]
        entries.append({"title": f"{code} {region.name}", "url": RESOLVER.href("region", code, "index.html"),
                         "type": "Region"})
        for num, loc in sorted(region.locations.items()):
            entries.append({"title": f"{loc.code} {loc.name}", "url": RESOLVER.href("location", code, num, "index.html"),
                             "type": "Location"})
    for kind in ("lore", "keys", "named_creatures", "unique_treasures"):
        label = REGISTRY_PAGE_TITLES[kind]
        for e in getattr(setting, kind):
            entries.append({"title": e.title, "url": RESOLVER.href(kind, e.title, "index.html"), "type": label})
    for creature in setting.bestiary:
        entries.append({"title": creature["name"], "url": RESOLVER.href("bestiary", creature["name"], "index.html"),
                         "type": "Bestiary"})
    for faction in setting.factions:
        entries.append({"title": faction["name"], "url": "factions.html", "type": "Faction"})
    for href, label in NAV_LINKS:
        entries.append({"title": label, "url": href, "type": "Page"})

    (out / "search-index.json").write_text(json.dumps(entries), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build(out_dir: Path) -> sc.Setting:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    setting = sc.load_setting()

    assets_dest = out_dir / "assets"
    shutil.copytree(ASSETS_SRC, assets_dest)

    build_index(setting, out_dir)
    build_history(setting, out_dir)
    build_truths(setting, out_dir)
    build_rumours(setting, out_dir)
    build_bestiary(setting, out_dir)
    build_factions(setting, out_dir)
    build_treasure(setting, out_dir)
    for kind in ("lore", "keys", "named_creatures", "unique_treasures"):
        build_registry(setting, out_dir, kind)
    for code in setting.region_order:
        build_region(setting, out_dir, code)
        for num in setting.regions[code].locations:
            build_location(setting, out_dir, code, num)

    build_search_index(setting, out_dir)
    (out_dir / ".nojekyll").write_text("")
    return setting


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="_site", help="output directory (default: _site)")
    args = parser.parse_args()
    out_dir = (ROOT / args.out).resolve() if not os.path.isabs(args.out) else Path(args.out)
    setting = build(out_dir)
    page_count = sum(1 for _ in out_dir.rglob("*.html"))
    print(f"Built {page_count} pages for '{setting.name}' into {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
