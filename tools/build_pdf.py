#!/usr/bin/env python3
"""Builds a single, internally hyperlinked PDF of the whole setting.

Usage: python3 tools/build_pdf.py [--out _site/<slug>.pdf]

Renders one combined HTML document (same content and cross-reference links
as tools/build_site.py's web view) and converts it to PDF with WeasyPrint.
WeasyPrint is not part of the standard library - install it with
`pip install weasyprint` (see requirements-pdf.txt) before running this.

Connections are listed as plain "X — Y" lines: the gazetteer's Joins between
regions, and each region's Connections.md between locations.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

import site_common as sc

ROOT = sc.ROOT

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


def connections_block(lines: list[str]) -> str:
    if not lines:
        return ""
    items = "".join(f"<li>{html.escape(l)}</li>" for l in lines)
    return f'<div class="connections"><h3>Connections</h3><ul>{items}</ul></div>'


def build_document(setting: sc.Setting) -> str:
    parts: list[str] = []
    toc: list[str] = []

    # ---- cover ----
    parts.append(f"""
<section class="cover">
  <h1 class="cover-title">{html.escape(setting.name)}</h1>
  <p class="cover-tags">{html.escape(setting.tagline)}</p>
  <p class="cover-outline">{ri(setting.outline, setting)}</p>
</section>
""")

    # ---- table of contents ----
    toc_placeholder_index = len(parts)
    parts.append("")  # filled in after we know every section

    # ---- setting-level documents: a section per page of the site, from the same schema ----
    render = lambda text: ri(text, setting)
    for slug, ts in setting.pages().items():
        title = re.sub(r" [IVX]+$", "", ts[0].name)
        if len(ts) == 1:
            inner = sc.table_html(ts[0], render)
        else:
            inner = "".join(sc.table_html(t, render, t.heading or t.name) for t in ts)
        parts.append(f'<section class="doc" id="{slug}"><h1>{html.escape(title)}</h1>{inner}</section>')
        toc.append(toc_entry(title, slug))
    for p in setting.prose:
        parts.append(f'<section class="doc" id="{p.slug}"><h1>{html.escape(p.title)}</h1>'
                     f'{sc.prose_html(p.text, render)}</section>')
        toc.append(toc_entry(p.title, p.slug))

    # ---- regions + locations ----
    top_conn = connections_block(sc.join_lines(setting)) + sc.sheets_html("170x230mm")
    region_toc: list[str] = []
    for code in setting.region_order:
        region = setting.regions[code]
        r_anchor = sc.anchor_id("region", code)
        field_html = "".join(
            f'<h3>{html.escape(label)}</h3>' + sc.field_html(text, lambda t: ri(t, setting))
            for label, text in region.fields
        )
        field_html += "".join(
            f'<h3>{html.escape(label)}</h3>' + sc.field_html("\n".join("- " + l for l in lines), lambda t: ri(t, setting))
            for label, lines in region.drawn
        )
        table_html = ""
        for table_label, table_rows in region.tables:
            trows = "".join(f'<tr><td class="num">{n}</td><td>{ri(t, setting)}</td></tr>' for n, t in table_rows)
            table_html += f'<h3>{html.escape(table_label)}</h3><table class="data-table"><tbody>{trows}</tbody></table>'

        rconn = connections_block(sc.connection_lines(code, setting))

        parts.append(
            f'<section class="doc region-doc" id="{r_anchor}">'
            f'<h1>{code} {html.escape(region.name)} '
            f'<span class="badge badge-{region.rating.lower()}">{region.rating} {region.die}</span></h1>'
            f'{field_html}{table_html}{sc.drawn_html(code, sc.maps_fit_pdf)}{rconn}'
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
                f'{sc.cut_html(code, num, sc.maps_fit_pdf)}<ul class="feature-list">{feats}</ul>{exits_html}'
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
.badge-weight-landmark { background: #2f6f4f; }
.badge-weight-hidden { background: #8a6d1e; }
.badge-weight-secret { background: #8a2e2e; }

.data-table { width: 100%; border-collapse: collapse; margin: 0.4em 0 0.8em; font-size: 9.5pt; }
.data-table th, .data-table td { text-align: left; padding: 0.25em 0.5em; border-bottom: 0.5pt solid #cbbb98; vertical-align: top; }
.data-table .num { color: #766a5a; width: 2em; }

.stat-grid { display: block; }
.stat-card, .faction-card, .registry-card { border: 0.5pt solid #cbbb98; border-radius: 4px; padding: 0.5em 0.7em; margin-bottom: 0.6em; break-inside: avoid; }
.stat-card .kind, .faction-card .ad, .registry-card .typetag { color: #5a4f42; font-weight: 400; font-size: 9pt; }
.stat-card .ad { color: #7a2e1d; font-weight: 700; }
.faction-note { color: #5a4f42; font-style: italic; margin-top: 0.6em; }

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
.plan-figure { margin: 0.8em 0; page-break-inside: avoid; }
.plan-figure svg { width: 11cm; display: block; }
.plan-figure figcaption, .plan-figure details { font-size: 9pt; color: #5a4f42; }
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


def check(setting: sc.Setting, doc_html: str) -> list[str]:
    """What setting/ and the schema hold that the PDF does not show."""
    def has_page(slug: str) -> bool:
        if m := re.fullmatch(r"region/([A-Z]+)/(\d+)", slug):
            slug = sc.anchor_id("location", m.group(1), m.group(2))
        return f'id="{slug}"' in doc_html
    return sc.coverage(setting, doc_html, has_page)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=None, help="output PDF path (default: _site/<setting-slug>.pdf)")
    parser.add_argument("--html-out", default=None, help="also write the intermediate combined HTML to this path")
    parser.add_argument("--check", action="store_true",
                        help="fail if a table, field or page setting/ holds is not in the PDF; "
                             "needs no WeasyPrint")
    args = parser.parse_args()

    setting = sc.load_setting()
    doc_html = build_html(setting)
    if args.check:
        problems = check(setting, doc_html)
        for p in problems:
            print(f"pdf: {p}")
        print(f"{len(problems)} problem(s)")
        return 1 if problems else 0

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
