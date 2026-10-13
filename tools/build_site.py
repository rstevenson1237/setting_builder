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
    "quests": "quests.html",
}
REGISTRY_PAGE_TITLES = {
    "lore": "Lore",
    "keys": "Keys",
    "named_creatures": "Named Creatures",
    "unique_treasures": "Unique Treasures",
    "quests": "Quests",
}
REGISTRY_MARKER_LABELS = {
    "lore": "Found at",
    "keys": "Found at",
    "named_creatures": "Appears at",
    "unique_treasures": "Found at",
    "quests": "Points to",
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
    ("quests.html", "Quests"),
    ("checklists.html", "Review Checklists"),
    ("patterns.html", "Schema Reference"),
]

# The judgement-check checklists rendered on checklists.html are parsed straight out of
# these templates' own Instructions sections, so the site never carries a second copy of
# wording that could drift from templates/checks/*_Judgement_Check.md.
CHECKLIST_SOURCES = [
    ("templates/checks/Template_Judgement_Check.md", "Template Judgement Check", "template"),
    ("templates/checks/Schema_Judgement_Check.md", "Schema Judgement Check", "schema"),
    ("templates/checks/Setting_Judgement_Check.md", "Setting Judgement Check", "setting"),
]


# ---------------------------------------------------------------------------
# Schema reference: patterns/*_Schema.md as written, shared schemas first. It reads
# the framework rather than setting/, so it builds whatever setting/ holds.
# ---------------------------------------------------------------------------

import tables
import validate_setting as vs  # read_block_files


def schema_files() -> list[Path]:
    shared = [tables.PATTERNS / f"{n}_Schema.md" for n in tables.SHARED]
    return shared + sorted(set(tables.PATTERNS.glob("*_Schema.md")) - set(shared))


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


def page_shell(setting: sc.Setting, current_page: str, title: str, body: str, description: str = "",
               extra_scripts: list[str] | None = None, footer_note: str = "", main_class: str = "page") -> str:
    css_rel = rel_asset(current_page, "assets/style.css")
    js_rel = rel_asset(current_page, "assets/app.js")
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
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body>
{nav_html(setting, current_page)}
<main class="{main_class}">
{body}
</main>
<footer class="site-footer">
  <p>{footer}</p>
</footer>
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



MERMAID_FENCE_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)


def mermaid_block(mmd_text: str, extra_lines: list[str] | None = None) -> str:
    m = MERMAID_FENCE_RE.search(mmd_text)
    text = m.group(1) if m else mmd_text
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
    body = [f'<h1>{html.escape(setting.name)}</h1>']
    if setting.tagline:
        body.append(f'<p class="tagline">{html.escape(setting.tagline)}</p>')
    body.append(f'<p class="outline">{render_inline(setting.outline, setting, page)}</p>')

    cards = []
    for href, label in NAV_LINKS[1:]:
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

    clicks = top_graph_clicks(setting.top_connections, page)
    body.append(section("Region Connections", mermaid_block(setting.top_connections, clicks)))

    write_page(out, page, page_shell(setting, page, setting.name, "\n".join(body)))


def build_history(setting: sc.Setting, out: Path) -> None:
    page = "history.html"
    rows = []
    for when, text, left in setting.history:
        marker = f'<span class="when">{html.escape(when)}</span>' if when else ""
        trace = (
            f'<span class="left-mark"><em>Left:</em> {render_inline(left, setting, page)}</span>'
            if left else ""
        )
        rows.append(
            f'<li>{marker}'
            f'<span class="event">{render_inline(text, setting, page)}</span>'
            f'{trace}</li>'
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
    label = {"T": "True", "P": "Partly true", "F": "False", "U": "Unverified"}
    any_settled = any(settled for _, _, _, settled in setting.rumours)
    for n, text, tpf, settled in setting.rumours:
        cls = {"T": "tpf-true", "P": "tpf-partial", "F": "tpf-false", "U": "tpf-unverified"}.get(tpf, "")
        settled_cell = (
            f'<td class="settled">{render_inline(settled, setting, page)}</td>'
            if any_settled else ""
        )
        rows.append(
            f'<tr><td class="num">{n}</td><td>{render_inline(text, setting, page)}</td>'
            f'<td class="tpf {cls}" title="{label.get(tpf, tpf)}">{tpf}</td>'
            f'{settled_cell}</tr>'
        )
    settled_head = "<th>Settled at</th>" if any_settled else ""
    body = (
        '<h1>Rumours</h1>'
        '<p class="hint">Referee reference — hover a mark for what it means. Players hear the rumour, not the mark.</p>'
        '<div class="table-scroll">'
        f'<table class="data-table"><thead><tr><th>#</th><th>Rumour</th><th>Truth</th>{settled_head}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )
    write_page(out, page, page_shell(setting, page, "Rumours", body))


def build_bestiary(setting: sc.Setting, out: Path) -> None:
    page = "bestiary.html"
    cards = []
    for creature in setting.bestiary:
        anchor = f"bestiary-{sc.slugify(creature['name'])}"
        field_paras = "".join(
            f'<p><strong>{html.escape(label)}:</strong> {render_inline(value, setting, page)}</p>'
            for label, value in creature["fields"]
        )
        cards.append(
            f'<article class="stat-card" id="{anchor}">'
            f'<h3>{html.escape(creature["name"])} <span class="kind">({html.escape(creature["kind"])})</span></h3>'
            f'<p class="ad">AD: {html.escape(creature["ad"])}</p>'
            f'{field_paras}'
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
    notes = "".join(
        f'<p class="faction-note">{render_inline(n, setting, page)}</p>'
        for n in setting.faction_notes
    )
    body = f'<h1>Factions</h1><div class="faction-list">{"".join(cards)}</div>{notes}'
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
            f'<div class="table-scroll"><table class="data-table">'
            f'<thead><tr><th>#</th><th>Item</th>'
            f'<th>Value</th><th>Wt</th></tr></thead><tbody>{rows}</tbody></table></div>'
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
        marker = REGISTRY_MARKER_LABELS[kind]
        typetag = render_inline(e.typetag, setting, page) if e.typetag else ""
        typetag_html = f'<span class="typetag">({typetag})</span>' if typetag else ""
        if sc.parse_field_lines(e.body):
            rows = "".join(
                f'<tr><th>{html.escape(label)}</th><td>{render_inline(text, setting, page)}</td></tr>'
                for label, text in sc.parse_field_lines(e.body)
            )
            body_html = f'<table class="kv-table">{rows}</table>'
        else:
            body_html = f'<div class="registry-body">{render_inline(e.body, setting, page)}</div>'
        cards.append(
            f'<article class="registry-card" id="{anchor}">'
            f'<h3>{html.escape(e.title)} {typetag_html}</h3>'
            f'<p class="registry-location">{marker} {loc_links}</p>'
            f'{body_html}'
            f'</article>'
        )
    title = REGISTRY_PAGE_TITLES[kind]
    empty = '<p class="hint">Nothing recorded yet.</p>' if not cards else ""
    body = f'<h1>{title}</h1>{empty}<div class="registry-list">{"".join(cards)}</div>'
    write_page(out, page, page_shell(setting, page, title, body))


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
    """Every schema file: its prose, then its KDL as written."""
    page = "patterns.html"
    body = ['<h1>Schema Reference</h1>',
            '<p class="hint">Every field, enum and range the setting files and location '
            'tables are checked against, read from <code>patterns/*_Schema.md</code> at '
            'build time.</p>']
    for path in schema_files():
        text = path.read_text(encoding="utf-8")
        title = (re.search(r"^#\s+(.+)$", text, re.M) or [None, path.stem])[1]
        prose = text.split("```")[0].split("\n", 1)[-1].strip()
        code = re.search(r"```kdl\n(.*?)```", text, re.S)
        inner = "".join(f"<p>{render_static_inline(par)}</p>" for par in prose.split("\n\n") if par.strip())
        if code:
            inner += f"<pre><code>{html.escape(code.group(1))}</code></pre>"
        body.append(section(title, f'<div class="schema-block">{inner}</div>', anchor=path.stem.lower()))
    write_page(out, page, page_shell(setting, page, "Schema Reference", "\n".join(body),
                                     main_class="page page-wide"))

def read_block_files(code: str) -> list[dict]:
    """Every `[Block Name].mmd` in a region folder, header and diagram.

    A DANGEROUS region's `Connections.mmd` is the block-existence tier, not its
    location graph - the typed location edges live one file per block, per
    STEPS.md 4b. Reading only `Connections.mmd` therefore draws a region of
    one box per block and no rooms at all. The header regex is the validator's,
    so the two readers cannot drift apart.
    """
    rdir = sc.SETTING / "region" / code
    if not rdir.is_dir():
        return []
    blocks = []
    for path in sorted(rdir.glob("*.mmd")):
        if path.name == "Connections.mmd":
            continue
        text = path.read_text()
        head = {k: v for k, v in vs.BLOCK_HEADER_RE.findall(text)}
        blocks.append({
            "name": head.get("Block") or path.stem,
            "purpose": head.get("Purpose", "").strip(),
            "rooms": head.get("Rooms", "").strip(),
            "members": re.findall(r"[A-Z]+\.\d+", head.get("Locations", "")),
            "mmd": text,
        })
    return blocks


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

    summary_mmd = sc.load_mmd(sc.SETTING / "region" / code / "Connections.mmd")
    blocks = read_block_files(code)

    if blocks:
        # A region generated in blocks reads as a summary of its quarters and
        # then one quarter at a time, which is the order it was written in.
        if summary_mmd.strip():
            body.append(section(
                "Region Summary",
                mermaid_block(summary_mmd, region_graph_clicks(summary_mmd, code, page)),
            ))
        claimed: set[int] = set()
        for b in blocks:
            nums = []
            for m in b["members"]:
                rc, num_s = m.split(".", 1)
                if rc == code and int(num_s) in region.locations:
                    nums.append(int(num_s))
            nums.sort()
            claimed.update(nums)
            meta = " · ".join(x for x in (
                f'{html.escape(b["purpose"])}' if b["purpose"] else "",
                f'{len(nums)} locations' if nums else "",
            ) if x)
            inner = f'<p class="block-meta">{meta}</p>' if meta else ""
            inner += mermaid_block(b["mmd"], region_graph_clicks(b["mmd"], code, page))
            if nums:
                inner += loc_list(nums)
            body.append(section(f'Block: {html.escape(b["name"])}', inner))
        rest = [n for n in sorted(region.locations) if n not in claimed]
        if rest:
            body.append(section("Locations outside any block", loc_list(rest)))
    else:
        body.append(section("Locations", loc_list(sorted(region.locations))))
        if summary_mmd.strip():
            body.append(section(
                "Connections",
                mermaid_block(summary_mmd, region_graph_clicks(summary_mmd, code, page)),
            ))

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
    for kind in ("lore", "keys", "named_creatures", "unique_treasures", "quests"):
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
    for kind in ("lore", "keys", "named_creatures", "unique_treasures", "quests"):
        build_registry(setting, out_dir, kind)
    build_checklists(setting, out_dir)
    build_patterns(setting, out_dir)
    for code in setting.region_order:
        build_region(setting, out_dir, code)
        for num in setting.regions[code].locations:
            build_location(setting, out_dir, code, num)

    build_search_index(setting, out_dir)
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="_site", help="output directory (default: _site)")
    parser.add_argument("--patterns-only", action="store_true",
                        help="build only patterns.html - needs no setting/ content")
    args = parser.parse_args()
    out_dir = (ROOT / args.out).resolve() if not os.path.isabs(args.out) else Path(args.out)
    if args.patterns_only:
        build_patterns_only(out_dir)
        print(f"Built patterns.html into {out_dir}")
        return 0
    setting = build(out_dir)
    page_count = sum(1 for _ in out_dir.rglob("*.html"))
    print(f"Built {page_count} pages for '{setting.name}' into {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
