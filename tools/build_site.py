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

import kdl
import schema_graph
import site_common as sc
import templates as tp

ROOT = sc.ROOT
ASSETS_SRC = Path(__file__).resolve().parent / "site_assets"
# The dice roller (assets/dice-overlay.js) loads on first use; this is the one place its three.js version is set.
THREE_URL = "https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.module.js"

# Pages that are not one setting file: the index, the checklists and the schema reference.
TAIL_LINKS = [
    ("lookup.html", "Index"),
    ("checklists.html", "Review Checklists"),
    ("patterns.html", "Schema Reference"),
]


def nav_links(setting: sc.Setting) -> list[tuple[str, str]]:
    """Home, then a page for each table of the schema and each prose file, in the order
    Setting_Schema.md gives them: a table added there appears here without an edit."""
    links = [("index.html", "Home")]
    for slug, ts in setting.pages().items():
        links.append((f"{slug}.html", re.sub(r" [IVX]+$", "", ts[0].name)))
    links += [(f"{p.slug}.html", p.title.split(" of ")[0]) for p in setting.prose]
    return links + TAIL_LINKS


# The judgement-check checklists rendered on checklists.html are parsed straight out of
# these templates' own Instructions sections, so the site never carries a second copy of
# wording that could drift from templates/checks/*_Judgement_Check.md.
CHECKLIST_SOURCES = [(f"templates/checks/{p.name}", p.stem.replace("_", " "), p.stem.split("_")[0].lower())
                     for p in sorted((ROOT / "templates" / "checks").glob("*_Judgement_Check.md"))]


# ---------------------------------------------------------------------------
# Schema reference: patterns/*_Schema.md, shared schemas first, drawn as a graph by
# schema_graph.py. It reads the framework rather than setting/, so it builds whatever
# setting/ holds.
# ---------------------------------------------------------------------------

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
        if kind == "entry":
            table, title = args
            return f"{sc.slugify(re.sub(r' [IVX]+$', '', table))}.html", sc.anchor_id(kind, table, title)
        if kind == "table":
            (name,) = args
            return f"{sc.slugify(re.sub(r' [IVX]+$', '', name))}.html", sc.anchor_id(kind, name)
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
    for href, label in nav_links(setting):
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
    <button class="nav-toggle" aria-label="Toggle navigation" aria-controls="site-nav" aria-expanded="true">
      <span></span><span></span><span></span>
    </button>
    <a class="brand" href="{rel_asset(current_page, 'index.html')}">{html.escape(setting.name)}</a>
    <div class="dice-pill" role="group" aria-label="Dice roller"></div>
  </div>
</header>
<nav class="site-nav" id="site-nav" aria-label="Site">
  <div class="nav-search">
    <input type="search" id="site-search" placeholder="Search the setting…" autocomplete="off"
           data-index="{search_rel}">
    <ul id="search-results" class="search-results" hidden></ul>
  </div>
  <ul class="nav-list">
    {''.join(items)}
    <li class="nav-dropdown">
      <button class="dropdown-toggle" aria-expanded="false">Regions ▾</button>
      <ul class="dropdown-menu">{''.join(region_items)}</ul>
    </li>
    <li><a class="pdf-link" href="{pdf_rel}" download>⬇ Download PDF</a></li>
  </ul>
</nav>
"""


def page_shell(setting: sc.Setting, current_page: str, title: str, body: str, description: str = "",
               extra_scripts: list[str] | None = None, footer_note: str = "", main_class: str = "page") -> str:
    css_rel = rel_asset(current_page, "assets/style.css")
    js_rel = rel_asset(current_page, "assets/app.js")
    shim_rel = rel_asset(current_page, "assets/cannon-shim.js")
    if not shim_rel.startswith("."):
        shim_rel = "./" + shim_rel  # import-map addresses must be ./, ../ or absolute
    full_title = f"{title} — {setting.name}" if title != setting.name else title
    desc = html.escape(description or setting.outline[:200])
    extra_tags = "".join(f'<script src="{rel_asset(current_page, s)}"></script>' for s in (extra_scripts or []))
    footer = footer_note or f"{html.escape(setting.name)} — generated from <code>setting/</code> by <code>tools/build_site.py</code>."
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{css_rel}">
<script type="importmap">{{"imports": {{"three": "{THREE_URL}", "cannon": "{shim_rel}"}}}}</script>
</head>
<body data-cites="{rel_asset(current_page, 'cites.json')}">
<a class="skip-link" href="#content">Skip to content</a>
{nav_html(setting, current_page)}
<div class="site-body">
<main class="{main_class}" id="content" tabindex="-1">
{body}
</main>
<footer class="site-footer">
  <p>{footer}</p>
</footer>
</div>
<script src="{js_rel}"></script>
{extra_tags}
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



def connections_list(lines: list[str]) -> str:
    return f'<ul class="connection-list">{"".join(f"<li>{html.escape(l)}</li>" for l in lines)}</ul>' if lines else ""


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def build_index(setting: sc.Setting, out: Path) -> None:
    page = "index.html"
    body = [f'<h1>{html.escape(setting.name)}</h1>']
    if setting.tagline:
        body.append(f'<p class="tagline">{html.escape(setting.tagline)}</p>')
    body.append(f'<p class="outline">{render_inline(setting.outline, setting, page)}</p>')

    cards = []
    for href, label in nav_links(setting)[1:]:
        cards.append(f'<a class="card" href="{rel_asset(page, href)}">{label}</a>')
    body.append(f'<div class="card-grid">{"".join(cards)}</div>')

    region_rows = []
    for code in setting.region_order:
        r = setting.regions[code]
        href = RESOLVER.href("region", code, page)
        region_rows.append(
            f'<a class="region-row" href="{href}">'
            f'<div class="region-code">{code}</div>'
            f'<div><div class="region-name">{html.escape(r.name)} '
            f'<span class="badge badge-{r.rating.lower()}">{r.rating} {r.die}</span></div>'
            f'<div class="region-blurb">{render_inline(r.gazetteer_blurb, setting, page, no_links=True)}</div></div>'
            f'</a>'
        )
    body.append(section("Regions", f'<div class="region-list">{"".join(region_rows)}</div>'))

    body.append(section("Region Connections", connections_list(sc.join_lines(setting))))
    if sheets := sc.sheets_html(sc.maps_fit_site, (setting, RESOLVER, page)):
        body.append(section("Sheets", sheets))

    write_page(out, page, page_shell(setting, page, setting.name, "\n".join(body)))


def build_tables(setting: sc.Setting, out: Path) -> None:
    """One page per group of schema tables, and one per prose file."""
    for slug, ts in setting.pages().items():
        page = f"{slug}.html"
        title = re.sub(r" [IVX]+$", "", ts[0].name)
        render = lambda text, page=page: render_inline(text, setting, page)
        if len(ts) == 1:
            inner = sc.table_html(ts[0], render, setting=setting)
        else:
            inner = "".join(sc.table_html(t, render, t.heading or t.name, setting=setting) for t in ts)
        write_page(out, page, page_shell(setting, page, title, f"<h1>{html.escape(title)}</h1>{inner}"))
    for p in setting.prose:
        page = f"{p.slug}.html"
        render = lambda text, page=page: render_inline(text, setting, page)
        body = f"<h1>{html.escape(p.title)}</h1>{sc.prose_html(p.text, render)}"
        write_page(out, page, page_shell(setting, page, p.title, body))


def render_static_inline(text: str) -> str:
    """Escape plain reference text and turn `backticked` spans into <code>, without
    touching setting cross-reference syntax - these checklists aren't setting content."""
    escaped = html.escape(text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def parse_checklist_source(rel_path: str) -> dict:
    """Pull the Purpose blurb and the Instructions checklist bullets out of a
    templates/checks/*_Judgement_Check.md file - the bullets are the checklist itself,
    each written as "- **Title** - description"."""
    text = (ROOT / rel_path).read_text(encoding="utf-8")
    purpose = re.search(r"## Purpose\n(.*?)\n##", text, re.S).group(1).strip()
    instructions = re.search(r"## Instructions\n(.*?)\n## Template", text, re.S).group(1).strip()

    intro_lines = []
    items = []
    for line in instructions.splitlines():
        line = line.strip()
        if not line:
            continue
        bullet = re.match(r"-\s+\*\*(.+?)\*\*\s*-\s*(.*)", line)
        if bullet:
            items.append((bullet.group(1), bullet.group(2)))
        elif not items:
            intro_lines.append(line)

    return {"purpose": purpose, "intro": " ".join(intro_lines), "items": items}


def build_lookup(setting: sc.Setting, out: Path) -> None:
    """Where each setting entry turns up: every location whose tables name it."""
    page = "lookup.html"
    body = ["<h1>Index</h1>", '<p class="hint">Every setting entry the region tables name, with each location '
            "that names it and what there names it.</p>", sc.index_html(setting, RESOLVER, page)]
    write_page(out, page, page_shell(setting, page, "Index", "\n".join(body)))


def build_checklists(setting: sc.Setting, out: Path) -> None:
    page = "checklists.html"
    body = [
        "<h1>Review Checklists</h1>",
        '<p class="hint">Non-mechanical judgement checks for reviewing this setting by eye - '
        "<code>tools/validate_setting.py</code> catches structural breakage, these catch everything "
        "that still needs a human or model glance. Checked boxes are saved in this browser only, "
        "so they're a personal reading aid, not a shared record of results.</p>",
    ]
    for rel_path, title, slug in CHECKLIST_SOURCES:
        data = parse_checklist_source(rel_path)
        items_html = []
        for i, (item_title, desc) in enumerate(data["items"]):
            cb_id = f"{slug}-{i}"
            items_html.append(
                f'<li class="checklist-item"><label for="{cb_id}">'
                f'<input type="checkbox" id="{cb_id}" data-checklist-id="{cb_id}">'
                f'<span><strong>{render_static_inline(item_title)}</strong> — '
                f'{render_static_inline(desc)}</span></label></li>'
            )
        section_body = (
            f'<p>{render_static_inline(data["purpose"])}</p>'
            + (f'<p class="hint">{render_static_inline(data["intro"])}</p>' if data["intro"] else "")
            + f'<ul class="checklist">{"".join(items_html)}</ul>'
        )
        body.append(section(title, section_body, anchor=slug))

    write_page(out, page, page_shell(setting, page, "Review Checklists", "\n".join(body)))


def build_patterns(setting: sc.Setting, out: Path) -> None:
    """The schema explorer: a graph of every definition, and an entry for each. The model it
    runs on is embedded in the page, so it works from a `file://` open; without scripts the
    schema files are listed as written."""
    import json

    page = "patterns.html"
    graph = schema_graph.Graph()
    model = json.dumps(graph.model(), separators=(",", ":")).replace("</", "<\\/")
    plain = []
    for path in graph.paths:
        text = path.read_text(encoding="utf-8")
        title = (re.search(r"^#\s+(.+)$", text, re.M) or [None, path.stem])[1]
        prose = text.split("```")[0].split("\n", 1)[-1].strip()
        code = re.search(r"```kdl\n(.*?)```", text, re.S)
        inner = "".join(f"<p>{render_static_inline(par)}</p>" for par in prose.split("\n\n") if par.strip())
        if code:
            inner += f"<pre><code>{html.escape(code.group(1))}</code></pre>"
        plain.append(section(title, f'<div class="schema-block">{inner}</div>', anchor=path.stem.lower()))
    body = ('<div id="schema-explorer" class="sx"></div>'
            f'<script type="application/json" id="schema-data">{model}</script>'
            '<noscript><h1>Schema Reference</h1>' + "".join(plain) + '</noscript>')
    write_page(out, page, page_shell(setting, page, "Schema Reference", body,
                                     extra_scripts=["assets/schema-explorer.js"], main_class="page page-explorer"))


def build_region(setting: sc.Setting, out: Path, code: str) -> None:
    region = setting.regions[code]
    page = f"region/{code}/index.html"

    body = [
        f'<p class="breadcrumb"><a href="{rel_asset(page, "index.html")}">Home</a> / Regions / {code}</p>',
        f'<h1>{code} {html.escape(region.name)} '
        f'<span class="badge badge-{region.rating.lower()}">{region.rating} {region.die}</span></h1>',
        f'<p class="tagline">{render_inline(region.gazetteer_blurb, setting, page, no_links=True)}</p>',
    ]

    for label, text in region.fields:
        body.append(section(label, sc.field_html(text, lambda t: render_inline(t, setting, page))))
    for label, lines in region.drawn:
        body.append(section(label, sc.field_html("\n".join("- " + l for l in lines),
                                                 lambda t: render_inline(t, setting, page))))

    for table_label, table_rows in region.tables:
        rows = "".join(
            f'<tr><td class="num">{n}</td><td>{render_inline(text, setting, page)}</td></tr>'
            for n, text in table_rows
        )
        table = f'<div class="table-scroll"><table class="data-table"><tbody>{rows}</tbody></table></div>'
        body.append(section(table_label, table))

    def loc_row(num: int) -> str:
        loc = region.locations[num]
        href = RESOLVER.href("location", code, num, page)
        weight = f'<span class="badge badge-weight-{loc.weight}">{loc.weight}</span>' if loc.weight else ""
        ltags = " · ".join(t.strip() for t in loc.tags.split(","))
        return (
            f'<a class="location-row" href="{href}">'
            f'<span class="loc-code">{loc.code}</span>'
            f'<span class="loc-name">{html.escape(loc.name)} {weight}</span>'
            f'<span class="loc-tags">{html.escape(ltags)}</span>'
            f'</a>'
        )

    def loc_list(nums) -> str:
        return f'<div class="location-list">{"".join(loc_row(n) for n in nums)}</div>'

    if drawn := sc.drawn_html(code, sc.maps_fit_site, (setting, RESOLVER, page)):
        body.append(section("Map", drawn))
    body.append(section("Locations", loc_list(sorted(region.locations))))
    if lines := sc.connection_lines(code, setting):
        body.append(section("Connections", connections_list(lines)))

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
    body.append(f'<p class="{sc.line_class("summary", "player-summary")}">{render_inline(loc.player_summary, setting, page, skip_location=loc.code)}</p>')
    body.append(f'<p class="referee-notes">{render_inline(loc.referee_notes, setting, page, skip_location=loc.code)}</p>')

    body.append(sc.cut_html(code, num, sc.maps_fit_site))
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
                f'<li>{render_inline(sc.exit_text(loc.code, approach, ecode), setting, page, skip_location=loc.code)} '
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
    for t in setting.tables:
        if t.kind == "roll":
            continue
        for e in t.entries:
            entries.append({"title": e.title, "url": RESOLVER.href("entry", t.name, e.title, "index.html"),
                            "type": t.name})
    for href, label in nav_links(setting):
        entries.append({"title": label, "url": href, "type": "Page"})

    (out / "search-index.json").write_text(json.dumps(entries), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_cite_data(setting: sc.Setting, out: Path) -> None:
    """cites.json: what a citation opens in a box below it, with links relative to the site root."""
    import json

    render = lambda text: render_inline(text, setting, "index.html")
    (out / "cites.json").write_text(json.dumps(sc.cite_data(setting, render)), encoding="utf-8")


def build(out_dir: Path) -> sc.Setting:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    setting = sc.load_setting()

    assets_dest = out_dir / "assets"
    shutil.copytree(ASSETS_SRC, assets_dest)

    build_index(setting, out_dir)
    build_tables(setting, out_dir)
    build_lookup(setting, out_dir)
    build_checklists(setting, out_dir)
    build_patterns(setting, out_dir)
    for code in setting.region_order:
        build_region(setting, out_dir, code)
        for num in setting.regions[code].locations:
            build_location(setting, out_dir, code, num)

    build_search_index(setting, out_dir)
    build_cite_data(setting, out_dir)
    (out_dir / ".nojekyll").write_text("")
    return setting


def build_patterns_only(out_dir: Path) -> None:
    """patterns.html alone, with no setting/ content loaded, so the schema reference
    builds before step 1."""
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    shutil.copytree(ASSETS_SRC, out_dir / "assets")
    build_patterns(sc.Setting(name="Schema Reference"), out_dir)


def check(setting: sc.Setting, out_dir: Path) -> list[str]:
    """What setting/ and the schema hold that the built pages do not show."""
    skip = {"patterns.html", "checklists.html"}
    text = " ".join(p.read_text(encoding="utf-8") for p in out_dir.rglob("*.html") if p.name not in skip)
    problems = sc.coverage(setting, text, lambda slug: (out_dir / f"{slug}.html").exists())
    import json
    graph = schema_graph.Graph()
    problems += [f"patterns.html: {p}" for p in graph.problems]
    held = sum(1 for path in graph.paths for n in kdl.fenced(path.read_text(encoding="utf-8")))
    drawn = [d for d in graph.defs.values() if d["kind"] != "template"]
    if held != len(drawn):
        problems.append(f"patterns.html: {held} schema definitions, {len(drawn)} in the explorer")
    templates = len(tp.load_all())
    if templates != len(graph.defs) - len(drawn):
        problems.append(f"patterns.html: {templates} templates, {len(graph.defs) - len(drawn)} in the explorer")
    cites = json.loads((out_dir / "cites.json").read_text(encoding="utf-8"))
    for t in setting.tables:
        held = cites["roll" if t.kind == "roll" else "entry"].get(t.name, {})
        for e in t.entries:
            if t.kind in ("roll", "entry") and (dict(e.fields).get("#") if t.kind == "roll" else e.title) not in held:
                problems.append(f"{t.name} / {e.title}: not in cites.json")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="_site", help="output directory (default: _site)")
    parser.add_argument("--patterns-only", action="store_true",
                        help="build only patterns.html - needs no setting/ content")
    parser.add_argument("--check", action="store_true",
                        help="fail if a table, field or page setting/ holds is not on the site")
    args = parser.parse_args()
    out_dir = (ROOT / args.out).resolve() if not os.path.isabs(args.out) else Path(args.out)
    if args.patterns_only:
        build_patterns_only(out_dir)
        print(f"Built patterns.html into {out_dir}")
        return 0
    setting = build(out_dir)
    page_count = sum(1 for _ in out_dir.rglob("*.html"))
    print(f"Built {page_count} pages for '{setting.name}' into {out_dir}")
    if args.check:
        problems = check(setting, out_dir)
        for p in problems:
            print(f"site: {p}")
        print(f"{len(problems)} problem(s)")
        return 1 if problems else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
