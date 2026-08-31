#!/usr/bin/env python3
"""Builds a single, internally hyperlinked PDF of the whole setting.

Usage: python3 tools/build_pdf.py [--out _site/<slug>.pdf]

Renders one combined HTML document (same content and cross-reference links
as tools/build_site.py's web view) and converts it to PDF with WeasyPrint.
WeasyPrint is not part of the standard library - install it with
`pip install weasyprint` (see requirements-pdf.txt) before running this.

Mermaid diagrams can't be executed by WeasyPrint (no JavaScript), so each
Connections.mmd is rendered instead as a plain "X — Y" connection list
carrying the same information.
"""
from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

import site_common as sc

ROOT = sc.ROOT

REGISTRY_TITLES = {
    "lore": "Lore",
    "keys": "Keys",
    "named_creatures": "Named Creatures",
    "unique_treasures": "Unique Treasures",
}
REGISTRY_MARKER = {
    "lore": "Found at",
    "keys": "Found at",
    "named_creatures": "Appears at",
    "unique_treasures": "Found at",
}


class PdfLinkResolver(sc.LinkResolver):
    """Everything lives in one document, so every link is just '#anchor-id'."""

    def href(self, kind: str, *args) -> str | None:
        *target_args, _current_page = args
        return f"#{sc.anchor_id(kind, *target_args)}"


RESOLVER = PdfLinkResolver()


def ri(text: str, setting: sc.Setting, skip_location: str | None = None) -> str:
    return sc.render_inline(text, setting, RESOLVER, "pdf", skip_location=skip_location)


def toc_entry(title: str, anchor: str, level: int = 0) -> str:
    cls = "toc-entry" + (f" toc-level-{level}" if level else "")
    return f'<li class="{cls}"><a href="#{anchor}">{html.escape(title)}</a></li>'


def connections_block(mmd_text: str, setting: sc.Setting) -> str:
    lines = sc.describe_edges(mmd_text, setting)
    if not lines:
        return ""
    items = "".join(f"<li>{html.escape(l)}</li>" for l in lines)
    return f'<div class="connections"><h3>Connections</h3><ul>{items}</ul></div>'


def build_document(setting: sc.Setting) -> str:
    parts: list[str] = []
    toc: list[str] = []

    # ---- cover ----
    tags = " · ".join(t.strip() for t in setting.tags.split(","))
    parts.append(f"""
<section class="cover">
  <h1 class="cover-title">{html.escape(setting.name)}</h1>
  <p class="cover-tags">{html.escape(tags)}</p>
  <p class="cover-outline">{ri(setting.outline, setting)}</p>
</section>
""")

    # ---- table of contents ----
    toc_placeholder_index = len(parts)
    parts.append("")  # filled in after we know every section

    # ---- setting-level documents ----
    parts.append('<section class="doc" id="history"><h1>History</h1><ol class="timeline">' + "".join(
        f'<li><strong>{html.escape(when)}</strong> — {ri(text, setting)}</li>' for when, text in setting.history
    ) + "</ol></section>")
    toc.append(toc_entry("History", "history"))

    parts.append('<section class="doc" id="truths"><h1>Truths</h1><ul>' + "".join(
        f"<li>{ri(t, setting)}</li>" for t in setting.truths
    ) + "</ul></section>")
    toc.append(toc_entry("Truths", "truths"))

    rrows = "".join(
        f'<tr><td class="num">{n}</td><td>{ri(text, setting)}</td><td class="tpf">{tpf}</td></tr>'
        for n, text, tpf in setting.rumours
    )
    parts.append(
        '<section class="doc" id="rumours"><h1>Rumours</h1>'
        '<table class="data-table"><thead><tr><th>#</th><th>Rumour</th><th>T/P/F</th></tr></thead>'
        f'<tbody>{rrows}</tbody></table></section>'
    )
    toc.append(toc_entry("Rumours", "rumours"))

    bcards = "".join(
        f'<div class="stat-card" id="{sc.anchor_id("bestiary", c["name"])}">'
        f'<h3>{html.escape(c["name"])} <span class="kind">({html.escape(c["kind"])})</span></h3>'
        f'<p class="ad">AD: {html.escape(c["ad"])}</p><p>{ri(c["description"], setting)}</p></div>'
        for c in setting.bestiary
    )
    parts.append(f'<section class="doc" id="bestiary"><h1>Bestiary</h1><div class="stat-grid">{bcards}</div></section>')
    toc.append(toc_entry("Bestiary", "bestiary"))

    fcards = []
    for fac in setting.factions:
        rows = "".join(f'<tr><th>{html.escape(k)}</th><td>{ri(v, setting)}</td></tr>' for k, v in fac["fields"])
        fcards.append(
            f'<div class="faction-card"><h3>{html.escape(fac["name"])} '
            f'<span class="ad">AD: {html.escape(fac["ad"])}</span></h3>'
            f'<table class="kv-table">{rows}</table></div>'
        )
    parts.append(f'<section class="doc" id="factions"><h1>Factions</h1>{"".join(fcards)}</section>')
    toc.append(toc_entry("Factions", "factions"))

    toc.append(toc_entry("Treasure Tables", "treasure"))
    tsections = []
    for roman in ("I", "II", "III", "IV", "V"):
        rows = "".join(
            f'<tr><td class="num">{n}</td><td>{ri(item, setting)}</td><td>{html.escape(v)}</td><td>{html.escape(w)}</td></tr>'
            for n, item, v, w in setting.treasure[roman]
        )
        tsections.append(
            f'<div id="{sc.anchor_id("treasure", roman)}"><h2>{html.escape(sc.TREASURE_TITLES[roman])}</h2>'
            f'<table class="data-table"><thead><tr><th>#</th><th>Item</th><th>Value (cn)</th><th>Wt</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
        )
        toc.append(toc_entry(sc.TREASURE_TITLES[roman], sc.anchor_id("treasure", roman), level=1))
    parts.append(f'<section class="doc" id="treasure"><h1>Treasure Tables</h1>{"".join(tsections)}</section>')

    for kind in ("lore", "keys", "named_creatures", "unique_treasures"):
        entries = getattr(setting, kind)
        cards = []
        for e in entries:
            anchor = sc.anchor_id(kind, e.title)
            loc_links = ", ".join(
                f'<a href="#{sc.anchor_id("location", c.split(".")[0], int(c.split(".")[1]))}">'
                f'{c} {html.escape(setting.all_locations[c].name)}</a>'
                for c in e.locations if c in setting.all_locations
            )
            typetag = f' <span class="typetag">({ri(e.typetag, setting)})</span>' if e.typetag else ""
            cards.append(
                f'<div class="registry-card" id="{anchor}"><h3>{html.escape(e.title)}{typetag}</h3>'
                f'<p class="registry-location">{REGISTRY_MARKER[kind]} {loc_links}</p>'
                f'<div>{ri(e.body, setting)}</div></div>'
            )
        title = REGISTRY_TITLES[kind]
        parts.append(f'<section class="doc" id="{kind}"><h1>{title}</h1>{"".join(cards)}</section>')
        toc.append(toc_entry(title, kind))

    # ---- regions + locations ----
    top_conn = connections_block(setting.top_connections, setting)
    region_toc: list[str] = []
    for code in setting.region_order:
        region = setting.regions[code]
        r_anchor = sc.anchor_id("region", code)
        field_html = "".join(
            f'<h3>{html.escape(label)}</h3><p>{ri(text, setting)}</p>' for label, text in region.fields
        )
        table_html = ""
        if region.table_rows:
            trows = "".join(f'<tr><td class="num">{n}</td><td>{ri(t, setting)}</td></tr>' for n, t in region.table_rows)
            table_html = f'<h3>{html.escape(region.table_label)}</h3><table class="data-table"><tbody>{trows}</tbody></table>'

        rconn_path = sc.SETTING / "region" / code / "Connections.mmd"
        rconn = connections_block(sc.load_mmd(rconn_path), setting)

        parts.append(
            f'<section class="doc region-doc" id="{r_anchor}">'
            f'<h1>{code} {html.escape(region.name)} '
            f'<span class="badge badge-{region.rating.lower()}">{region.rating} {region.die}</span></h1>'
            f'{field_html}{table_html}{rconn}'
            f'</section>'
        )
        region_toc.append(toc_entry(f"{code} {region.name}", r_anchor, level=1))

        for num in sorted(region.locations):
            loc = region.locations[num]
            l_anchor = sc.anchor_id("location", code, num)
            weight = f' <span class="badge badge-weight-{loc.weight}">{loc.weight}</span>' if loc.weight else ""
            feats = "".join(
                f'<li><span class="feature-label">{html.escape(lbl)}:</span> {ri(txt, setting, skip_location=loc.code)}</li>'
                for lbl, txt in loc.features
            )
            if loc.exits:
                exit_items = "".join(
                    f'<li>{ri(approach, setting, skip_location=loc.code)} &rarr; '
                    f'<a href="#{sc.anchor_id("location", ecode.split(".")[0], int(ecode.split(".")[1]))}">{ecode} {html.escape(ename)}</a></li>'
                    for approach, ecode, ename in loc.exits
                )
                exits_html = f'<h3>Exits</h3><ul class="exit-list">{exit_items}</ul>'
            else:
                exits_html = '<h3>Exits</h3><p>None.</p>'
            parts.append(
                f'<section class="doc location-doc" id="{l_anchor}">'
                f'<h2>{loc.code} {html.escape(loc.name)}{weight}</h2>'
                f'<p class="player-summary">{ri(loc.player_summary, setting, skip_location=loc.code)}</p>'
                f'<p class="referee-notes">{ri(loc.referee_notes, setting, skip_location=loc.code)}</p>'
                f'<ul class="feature-list">{feats}</ul>{exits_html}'
                f'</section>'
            )
            region_toc.append(toc_entry(f"{loc.code} {loc.name}", l_anchor, level=2))

    toc.append(toc_entry("Regions", "regions-toc"))
    toc.extend(region_toc)

    toc_html = f"""
<section class="cover toc-page">
  <h1 id="regions-toc">Contents</h1>
  {top_conn}
  <ul class="toc">{"".join(toc)}</ul>
</section>
"""
    parts[toc_placeholder_index] = toc_html

    return "\n".join(parts)


PDF_CSS = """
@page {
  size: letter;
  margin: 2.2cm 1.8cm 2.4cm;
  @bottom-center { content: counter(page) " / " counter(pages); font-size: 9pt; color: #766a5a; }
}
* { box-sizing: border-box; }
body { font-family: Georgia, "Times New Roman", serif; color: #221c15; font-size: 10.5pt; line-height: 1.45; }
h1 { font-size: 20pt; bookmark-level: 1; margin: 0 0 0.3em; }
h2 { font-size: 15pt; bookmark-level: 2; margin: 1.1em 0 0.3em; border-bottom: 1pt solid #cbbb98; padding-bottom: 0.15em; }
h3 { font-size: 12pt; bookmark-level: 3; margin: 0.9em 0 0.25em; color: #7a2e1d; }
a { color: #7a2e1d; text-decoration: none; }
code { background: #f1e9da; padding: 0 3px; }

.cover { page-break-after: always; padding-top: 30%; text-align: center; }
.cover-title { font-size: 34pt; margin-bottom: 0.2em; }
.cover-tags { font-style: italic; color: #5a4f42; }
.cover-outline { max-width: 32em; margin: 1.5em auto 0; font-size: 12pt; }

.toc-page { page-break-after: always; padding-top: 5%; text-align: left; }
.toc { list-style: none; padding: 0; column-count: 1; }
.toc-entry { display: flex; justify-content: space-between; border-bottom: 1pt dotted #cbbb98; padding: 0.15em 0; }
.toc-entry a { color: #221c15; flex: 1; }
.toc-entry a::after { content: leader(dotted) target-counter(attr(href), page); float: right; color: #766a5a; }
.toc-level-1 { padding-left: 1.2em; font-size: 9.5pt; }
.toc-level-2 { padding-left: 2.4em; font-size: 9pt; color: #5a4f42; }

.doc { page-break-before: always; }
.location-doc { page-break-before: always; }
.region-doc { page-break-before: always; }

.badge { display: inline-block; font-size: 8pt; font-weight: 700; padding: 0.1em 0.6em; border-radius: 999px; color: #fff; }
.badge-safe { background: #2f6f4f; }
.badge-wild { background: #8a6d1e; }
.badge-dangerous { background: #8a2e2e; }
.badge-weight-low { background: #6b7a8f; }
.badge-weight-medium { background: #8a6d1e; }
.badge-weight-high { background: #8a2e2e; }

.data-table { width: 100%; border-collapse: collapse; margin: 0.4em 0 0.8em; font-size: 9.5pt; }
.data-table th, .data-table td { text-align: left; padding: 0.25em 0.5em; border-bottom: 0.5pt solid #cbbb98; vertical-align: top; }
.data-table .num { color: #766a5a; width: 2em; }

.stat-grid { display: block; }
.stat-card, .faction-card, .registry-card { border: 0.5pt solid #cbbb98; border-radius: 4px; padding: 0.5em 0.7em; margin-bottom: 0.6em; break-inside: avoid; }
.stat-card .kind, .faction-card .ad, .registry-card .typetag { color: #5a4f42; font-weight: 400; font-size: 9pt; }
.stat-card .ad { color: #7a2e1d; font-weight: 700; }

.kv-table { width: 100%; }
.kv-table th { text-align: left; vertical-align: top; width: 8em; color: #7a2e1d; font-size: 9pt; padding: 0.15em 0.4em 0.15em 0; }
.kv-table td { padding: 0.15em 0; }

.registry-location { color: #5a4f42; font-size: 9pt; }

.player-summary { font-size: 11pt; }
.referee-notes { font-style: italic; color: #5a4f42; }
.feature-list { list-style: none; padding: 0; }
.feature-list li { margin-bottom: 0.4em; }
.feature-label { color: #7a2e1d; font-weight: 700; }
.exit-list { list-style: none; padding: 0; }
.exit-list li { padding: 0.2em 0; }

.connections { margin-top: 0.8em; }
.connections ul { margin: 0.2em 0 0; padding-left: 1.2em; font-size: 9.5pt; }

.timeline { list-style: none; padding: 0; }
.timeline li { margin-bottom: 0.5em; }
"""


def build_html(setting: sc.Setting) -> str:
    body = build_document(setting)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(setting.name)}</title>
<style>{PDF_CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=None, help="output PDF path (default: _site/<setting-slug>.pdf)")
    parser.add_argument("--html-out", default=None, help="also write the intermediate combined HTML to this path")
    args = parser.parse_args()

    setting = sc.load_setting()
    doc_html = build_html(setting)

    if args.html_out:
        Path(args.html_out).write_text(doc_html, encoding="utf-8")

    out_path = Path(args.out) if args.out else ROOT / "_site" / f"{sc.slugify(setting.name)}.pdf"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from weasyprint import HTML
    except ImportError:
        print(
            "WeasyPrint is not installed. Run `pip install -r tools/requirements-pdf.txt` "
            "(or `pip install weasyprint`) and try again.",
            file=sys.stderr,
        )
        return 1

    HTML(string=doc_html, base_url=str(ROOT)).write_pdf(str(out_path))
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
