#!/usr/bin/env python3
"""Render every lecture for the site: lectures-and-labs/<weekNN>/<topic>-lecture.md ->
OUTPUT_DIR/<topic>/index.html and OUTPUT_DIR/<topic>/slides.pdf.

<topic> is the schedule's `lecture` name, not the week folder, so a lecture keeps
its web address when the semester is renumbered. A week's img/ folder is copied
beside the output. The Marp CLI is `marp` (CI installs it globally); set MARP to
run it another way, e.g. MARP="npx --no-install marp".

A PowerPoint lecture (<topic>-lecture.pptx) is not rendered: the deck is the only
source, published as it is as slides.pptx, with an index.html that shows it in
Microsoft's web viewer above every slide's text. The text is read from the deck
itself (scripts/deck_text.py), so the page can never disagree with it.

stdin is closed for every marp call: marp-cli treats piped stdin as an extra
markdown input, which once turned a loop over the decks into "Converting 2
markdowns" and an output-path error.

Usage:
    python scripts/render_decks.py [OUTPUT_DIR]      # default: build
"""
from __future__ import annotations

import html
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schedule import SITE, Row, load  # noqa: E402

THEME = "themes/aiap.css"
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# Microsoft's free Office viewer renders a public .pptx in the browser, builds
# included; it needs no account or download. Microsoft does not support it for
# production use, so the page offers the deck itself as the fallback.
OFFICE_VIEWER = "https://view.officeapps.live.com/op/view.aspx?src="
OFFICE_EMBED = "https://view.officeapps.live.com/op/embed.aspx?src="

DECK_CSS = """<style>
  .wrap { max-width: 1120px; }
  .standfirst { color: var(--slate); max-width: 66ch; margin: 4px 0 0; }
  .deck-actions { display: flex; flex-wrap: wrap; gap: 12px; margin: 18px 0 22px; }
  iframe.viewer { display: block; width: 100%; aspect-ratio: 16 / 10; background: #FFFFFF;
                  border: 1px solid var(--rule); border-radius: 10px; }
  .viewer-note { color: var(--muted); font-size: 14px; margin: 8px 0 0; }
  .slides { max-width: 780px; }
  .slide { border-top: 1px solid var(--rule); padding-bottom: 10px; }
  .slide-no { font-family: var(--mono); font-size: 13px; margin: 14px 0 0; }
  .slide-no a { color: var(--muted); }
  .slide h3 { color: var(--ink); margin-top: 8px; }
  .slide h4 { font-family: var(--mono); font-size: 16px; color: var(--slate); margin: 16px 0 4px; }
  @media (max-width: 700px) { iframe.viewer { aspect-ratio: 4 / 3; } }
</style>
"""


def demote(body_html: str) -> str:
    """Slide headings sit under the page's own: h1 and h2 become h3, h3 becomes h4."""
    return re.sub(r"<(/?)h([1-3])\b",
                  lambda m: f"<{m.group(1)}h{4 if m.group(2) == '3' else 3}", body_html)


def deck_page(row: Row) -> str:
    """The page for a PowerPoint lecture: the deck in Microsoft's web viewer, then
    every slide's text, read from the deck."""
    from build_lab_pages import RENDERER, page   # markdown-it-py, as the lab pages use
    from deck_text import slides_of
    deck_title, slides = slides_of(row.lecture.read_bytes(), [])
    title = html.escape(deck_title or row.topic)
    sections = []
    for md in slides:
        md = COMMENT_RE.sub("", md).strip()
        if not md:
            continue
        n = len(sections) + 1
        sections.append(
            f'<section class="slide" id="slide-{n}">\n'
            f'<p class="slide-no"><a href="#slide-{n}">slide {n}</a></p>\n'
            f"{demote(RENDERER.render(md))}"
            "</section>\n")
    deck = quote(f"{SITE}{row.deck}/slides.pptx", safe="")
    view = html.escape(OFFICE_VIEWER + deck)
    body_html = (
        f"<h1>{title}</h1>\n"
        f'<p class="standfirst">The slides in Microsoft\'s web viewer, with every slide\'s text '
        f"below. Download the PowerPoint to present it with its animations.</p>\n"
        f'<p class="deck-actions">'
        f'<a class="open" href="{view}" rel="noopener">View slides</a>'
        f'<a class="open" href="slides.pptx" download>Download PowerPoint</a></p>\n'
        f'<iframe class="viewer" src="{html.escape(OFFICE_EMBED + deck)}" '
        f'title="{title}: the slides" allowfullscreen></iframe>\n'
        f'<p class="viewer-note">No slides above? Use <a href="{view}" rel="noopener">View '
        f'slides</a>, or <a href="slides.pptx" download>Download PowerPoint</a>.</p>\n'
        f'<h2 id="every-slide">Every slide, as text</h2>\n'
        f"<p>All {len(sections)} slides.</p>\n"
        f'<div class="slides">\n{"".join(sections)}</div>\n')
    return page(title, '<a href="../">ai-assisted programming</a> · lecture', body_html, False,
                needs_hljs="language-python" in body_html, extra_css=DECK_CSS)


def publish_pptx(row: Row, out: Path) -> None:
    """Publish a PowerPoint lecture: the deck itself, and its page."""
    shutil.copyfile(row.lecture, out / "slides.pptx")
    (out / "index.html").write_text(deck_page(row), encoding="utf-8", newline="\n")


def main() -> None:
    out_root = Path(sys.argv[1] if len(sys.argv) > 1 else "build")
    marp = shlex.split(os.environ.get("MARP", "marp"))
    if os.name == "nt" and marp[0] in ("marp", "npx"):
        marp[0] += ".cmd"           # Windows resolves the npm shims by their .cmd name
    rows = load().teaching
    for row in rows:
        src = row.lecture
        if not src.is_file():
            raise SystemExit(f"render_decks: week {row.week} ({row.topic}) has no {src.as_posix()}")
        out = out_root / row.deck
        out.mkdir(parents=True, exist_ok=True)
        if row.is_pptx:
            publish_pptx(row, out)
            print(f"published {src.as_posix()} -> {out.as_posix()}/")
            continue
        if (row.path / "img").is_dir():
            shutil.copytree(row.path / "img", out / "img", dirs_exist_ok=True)
        for target in ("index.html", "slides.pdf"):
            subprocess.run([*marp, str(src), "--html", "--allow-local-files",
                            "--theme-set", THEME, "-o", str(out / target)],
                           check=True, stdin=subprocess.DEVNULL)
        print(f"rendered {src.as_posix()} -> {out.as_posix()}/")
    print(f"render_decks: {len(rows)} lectures")


if __name__ == "__main__":
    main()
