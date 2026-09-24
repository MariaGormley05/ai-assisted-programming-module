#!/usr/bin/env python3
"""Render the lab READMEs, their supporting pages and the MCQ pages for GitHub Pages.

For every scheduled lab (lectures-and-labs/weekNN/<slug>_lab/README.md) this
emits OUTPUT_DIR/labs/<slug>/index.html in the site's visual identity, plus a
labs index at OUTPUT_DIR/labs/index.html. <slug> is the schedule's lab name,
so a lab keeps its web address when the semester is renumbered.
Every other Markdown file under a lab (a TROUBLESHOOTING.md, a part folder's
README, a worksheet template) is rendered beside it at the same relative path
(README.md -> index.html, NAME.md -> NAME.html), so links between them keep
working on the site. Relative links to anything that is not Markdown (starter
code, data files) point at the file on GitHub, since the site does not serve
source files. mcq/<n>/README.md renders the same way under OUTPUT_DIR/mcq/.

Pages are READ-ONLY previews -- each lab README carries a banner telling
students to make their own copy of the repo from the template and work in a
Codespace.

Rendering is CommonMark via markdown-it-py (pip install markdown-it-py), with
tables and strikethrough enabled -- the same dialect GitHub renders, so a
fenced code block indented inside a numbered step comes out as a code block,
not as inline code with a stray "bash" in it, which is what Python-Markdown
made of it. Headings get GitHub's anchor ids so the READMEs' tables of
contents resolve. Mermaid fences render client-side (pinned mermaid), and
```python fences get client-side highlight.js colouring, pinned to the same
version marp-core bundles, with the token palette copied from themes/aiap.css
so lab code looks exactly like deck code. ```text fences (Expected output)
stay flat.

Usage:
    python scripts/build_lab_pages.py [OUTPUT_DIR]     # default: build
"""
import html
import posixpath
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

MCQ = Path("mcq")
REPO_URL = "https://github.com/danielcregg/ai-assisted-programming"

# Both scripts are third-party code executed on the module's public site, so
# each carries a Subresource Integrity hash: the browser refuses to run the
# file unless it hashes to exactly this, which makes a pinned version
# genuinely immutable rather than merely named. `crossorigin="anonymous"` is
# required for SRI to be enforced on a cross-origin request -- without it the
# response is opaque and the integrity attribute is silently ignored.
# Regenerate a hash after any version bump:
#   curl -sL <url> | openssl dgst -sha384 -binary | openssl base64 -A
MERMAID_JS = "https://cdn.jsdelivr.net/npm/mermaid@11.6.0/dist/mermaid.min.js"
MERMAID_SRI = "sha384-zkWMJO4sgpPUzyuOgDx8HB/K55glbAwajEpk1Go2NWRuPkPA/wIhoEJTuSkmOYrV"
# Same major.minor.patch as marp-core's bundled highlight.js — keeps lab
# token classes identical to the rendered decks'.
HLJS_JS = "https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11.11.1/highlight.min.js"
HLJS_SRI = "sha384-RH2xi4eIQ/gjtbs9fUXM68sLSi99C7ZWBRX1vDrVv6GQXRibxXLbwO2NGZB74MbU"

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
           "viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' "
           "fill='%23FBFAF7'/%3E%3Ctext x='16' y='25' font-family='Consolas,monospace' "
           "font-size='26' font-weight='700' fill='%23E76F00' "
           "text-anchor='middle'%3E;%3C/text%3E%3C/svg%3E")

STYLE = """<style>
  :root {
    --paper:#FBFAF7; --ink:#1E2833; --blue:#33698C; --orange:#6741D9;
    --slate:#46536B; --rule:#DED8C9; --muted:#8B8471; --codebg:#16222E;
    --mono:'Cascadia Code','SF Mono',Menlo,Consolas,'Courier New',monospace;
    --sans:'Segoe UI','Helvetica Neue',Arial,sans-serif;
    color-scheme: light;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; font-family: var(--sans); color: var(--ink); line-height: 1.6;
    background: linear-gradient(to right,
      var(--paper) 0, var(--paper) 56px, var(--rule) 56px, var(--rule) 58px,
      var(--paper) 58px, var(--paper) 100%);
  }
  .wrap { max-width: 880px; padding: 40px 32px 80px 88px; }
  .kicker { font-family: var(--mono); font-size: 14px; color: var(--muted); }
  .kicker::before { content: '// '; color: var(--orange); }
  .kicker a { color: var(--muted); }
  h1, h2, h3 { font-family: var(--mono); letter-spacing: -0.01em; line-height: 1.25; }
  h1 { font-size: clamp(26px, 4.5vw, 38px); margin: 10px 0 6px; }
  h1::after, h2::after { content: ';'; color: var(--orange); }
  h2 { font-size: 25px; margin: 40px 0 12px; border-top: 1px solid var(--rule); padding-top: 26px; }
  h3 { font-size: 20px; margin: 28px 0 10px; color: var(--slate); }
  a { color: var(--blue); text-decoration-color: var(--orange); }
  .copy-banner {
    border-left: 4px solid var(--orange); background: #FDEFD9;
    padding: 12px 18px; margin: 20px 0 8px; font-size: 15.5px; color: #7A4A12;
    border-radius: 0 8px 8px 0;
  }
  .copy-banner a { color: #B94E00; font-weight: 600; }
  code {
    font-family: var(--mono); background: #EFECE3; color: #B94E00;
    padding: 0.08em 0.35em; border-radius: 5px; font-size: 0.9em;
  }
  pre {
    background: var(--codebg); border-radius: 10px; padding: 16px 20px;
    overflow-x: auto; line-height: 1.5;
  }
  pre code { background: transparent; color: #E8ECF1; padding: 0; font-size: 14.5px; }
  /* code token colours — same palette as section pre code in themes/aiap.css */
  pre code .hljs-string { color: #F0B26B; }
  pre code .hljs-keyword { color: #7FB4D8; }
  pre code .hljs-title, pre code .hljs-built_in { color: #A8D3EE; }
  pre code .hljs-comment { color: #7C8B99; }
  pre.mermaid { background: #FFFFFF; border: 1px solid var(--rule); text-align: center; }
  table { border-collapse: collapse; margin: 14px 0; font-size: 15.5px; }
  th { font-family: var(--mono); text-align: left; color: var(--slate);
       border-bottom: 2px solid var(--ink); padding: 7px 22px 7px 6px; }
  td { border-bottom: 1px solid var(--rule); padding: 8px 22px 8px 6px; vertical-align: top; }
  blockquote { border-left: 4px solid var(--orange); background: #F4F0E6;
               margin: 14px 0; padding: 10px 18px; color: var(--slate); }
  blockquote p { margin: 4px 0; }
  details { border: 1.5px solid var(--blue); border-radius: 9px;
            padding: 10px 16px; margin: 12px 0; background: #FFFFFF; }
  details summary { font-family: var(--mono); font-weight: 600; color: var(--blue); cursor: pointer; }
  img { max-width: 100%; }
  li > pre { margin: 8px 0; }
  .row-list { list-style: none; padding: 0; }
  .row-list li { border-bottom: 1px solid var(--rule); padding: 14px 4px; display: flex;
                 justify-content: space-between; align-items: baseline; gap: 16px; }
  .row-list li:first-child { border-top: 1px solid var(--rule); }
  .row-list .wk { font-family: var(--mono); font-size: 13.5px; color: var(--muted);
                  flex: none; width: 64px; }
  .row-list .t { font-family: var(--mono); font-weight: 600; font-size: 19px; flex: 1; }
  .row-list .t a { color: var(--ink); text-decoration: none; }
  .row-list .t a:hover { color: var(--blue); }
  .open { font-family: var(--mono); font-size: 14px; color: var(--blue);
          border: 1.5px solid var(--blue); border-radius: 7px; padding: 5px 14px;
          text-decoration: none; white-space: nowrap; }
  .open:hover { background: var(--blue); color: var(--paper); }
  @media (max-width: 700px) {
    body { background: var(--paper); }
    .wrap { padding: 28px 18px 60px; }
    .open { padding: 10px 20px; font-size: 15px; }
  }
</style>"""

RENDERER = MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"])
TAG_RE = re.compile(r"<[^>]+>")
HEADING_RE = re.compile(r"<h([1-4])>(.*?)</h\1>", re.S)
HREF_RE = re.compile(r'href="([^"]+)"')


def gh_slugify(text: str) -> str:
    text = re.sub(r"[`*_]", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def preprocess(md_text: str) -> str:
    """Turn mermaid fences into pass-through <pre class="mermaid"> blocks."""
    def mermaid_repl(m):
        return '<pre class="mermaid">\n' + html.escape(m.group(1)) + "\n</pre>"
    return re.sub(r"```mermaid\n(.*?)\n```", mermaid_repl, md_text, flags=re.DOTALL)


def add_heading_ids(body: str) -> str:
    """GitHub's anchor rule, including -1, -2 suffixes for repeated headings."""
    seen: dict[str, int] = {}

    def repl(m):
        level, inner = m.group(1), m.group(2)
        slug = gh_slugify(html.unescape(TAG_RE.sub("", inner)))
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        if n:
            slug = f"{slug}-{n}"
        return f'<h{level} id="{slug}">{inner}</h{level}>'
    return HEADING_RE.sub(repl, body)


def rewrite_links(body: str, source: Path) -> str:
    """Relative links: Markdown targets become their rendered pages; anything
    else (starter code, folders) becomes a link to the file on GitHub."""
    src_dir = source.parent.as_posix()

    def repl(m):
        href = m.group(1)
        if re.match(r"^(?:[a-z]+:|#|/|//)", href):
            return m.group(0)
        path, sep, frag = href.partition("#")
        if not path:
            return m.group(0)
        if path.endswith("README.md"):
            new = path[: -len("README.md")] or "./"
        elif path.endswith(".md"):
            new = path[:-3] + ".html"
        else:
            target = posixpath.normpath(posixpath.join(src_dir, path))
            kind = "tree" if path.endswith("/") else "blob"   # a Makefile is a file too
            new = f"{REPO_URL}/{kind}/main/{target}"
        return f'href="{new}{sep}{frag}"'
    return HREF_RE.sub(repl, body)


def render(md_text: str, source: Path) -> str:
    body = RENDERER.render(preprocess(md_text))
    return rewrite_links(add_heading_ids(body), source)


def page(title: str, kicker_html: str, body_html: str, needs_mermaid: bool,
         banner_html: str = "", needs_hljs: bool = False) -> str:
    mermaid = (f'<script src="{MERMAID_JS}" integrity="{MERMAID_SRI}"'
               ' crossorigin="anonymous"></script>'
               '<script>mermaid.initialize({startOnLoad:true,theme:"neutral"});</script>'
               if needs_mermaid else "")
    # `typeof hljs` guard: if SRI rejects the file the script never defines
    # hljs, and an unguarded call would throw and abort the rest of the page.
    # Uncoloured code is a fine degradation; a broken page is not.
    hljs = (f'<script src="{HLJS_JS}" integrity="{HLJS_SRI}"'
            ' crossorigin="anonymous"></script>'
            "<script>if(typeof hljs!=='undefined'){"
            "document.querySelectorAll('pre code.language-python')"
            ".forEach(function(el){hljs.highlightElement(el);});}</script>"
            if needs_hljs else "")
    return (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title}</title>\n<link rel="icon" href="{FAVICON}">\n{STYLE}\n'
            f"</head>\n<body>\n<div class=\"wrap\">\n"
            f'<p class="kicker">{kicker_html}</p>\n{banner_html}{body_html}\n'
            f"</div>\n{hljs}{mermaid}</body>\n</html>\n")


def title_of(text: str, fallback: str) -> str:
    m = re.match(r"#\s+(.+)", text)
    return m.group(1).strip() if m else fallback


def write_page(source: Path, dest: Path, kicker: str, banner: str = "") -> str:
    text = source.read_text(encoding="utf-8")
    body = render(text, source)
    title = title_of(text, source.stem.replace("_", " ").title())
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        page(html.escape(title), kicker, body, "```mermaid" in text or 'class="mermaid"' in body,
             banner, needs_hljs="language-python" in body),
        encoding="utf-8", newline="\n")
    return title


def dest_for(source: Path, root: Path, out: Path) -> Path:
    rel = source.relative_to(root)
    if rel.name == "README.md":
        return out / rel.parent / "index.html"
    return out / rel.with_suffix(".html")


def scheduled_labs():
    """Every scheduled lab, in teaching order (module/schedule.json via
    scripts/schedule.py): the rows with a lab, each naming its site slug
    (row.lab), its week folder (row.dir) and its source (row.lab_dir)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from schedule import load
    return [r for r in load().rows if r.lab]


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "build")
    out_labs = out / "labs"
    out_labs.mkdir(parents=True, exist_ok=True)

    labs, pages = [], 0
    scheduled = scheduled_labs()
    for row in scheduled:
        slug, lab_dir = row.lab, row.lab_dir
        readme = lab_dir / "README.md"
        if not readme.is_file():
            continue
        text = readme.read_text(encoding="utf-8")
        if not re.match(r"#\s+(.+)", text):
            # A lab README's first `# ` line is the page title and the
            # labs-index entry. Without this guard it was an AttributeError on
            # None, which says nothing about which file is wrong or why.
            raise SystemExit(
                f"build_lab_pages: {readme} does not start with a `# ` "
                f"heading, so it has no title. Every lab README must open "
                f"with a level-1 heading on its first line.")
        banner = (f'<div class="copy-banner">Read-only preview. To <strong>do</strong> '
                  f'this lab: <a href="{REPO_URL}/generate">make your own copy of the '
                  f'repo</a> ("Use this template"), open a Codespace on it, and work '
                  f'in <code>{lab_dir.as_posix()}/</code>.</div>')
        for source in sorted(lab_dir.rglob("*.md")):
            if any(part.startswith(".") for part in source.relative_to(lab_dir).parts):
                continue   # .pytest_cache and friends ship a README of their own
            dest = dest_for(source, lab_dir, out_labs / slug)
            depth = len(source.relative_to(lab_dir).parts) - 1
            up = "../" * depth
            if source == readme:
                title = write_page(source, dest, '<a href="./..">labs</a> · ai-assisted programming', banner)
                labs.append((slug, title))
            else:
                write_page(source, dest, f'<a href="{up}./">{html.escape(slug)}</a> · '
                                         f'<a href="{up}../">labs</a> · ai-assisted programming')
            pages += 1

    mcq_pages = 0
    if MCQ.is_dir():
        for source in sorted(MCQ.glob("*/README.md")):
            write_page(source, dest_for(source, MCQ, out / "mcq"),
                       '<a href="../../">ai-assisted programming</a> · assessment')
            mcq_pages += 1

    # Teaching order, like the lecture index; anything not in the schedule
    # (optional extra material, should there ever be any) goes under its own
    # heading rather than being listed as if it were taught.
    titles = dict(labs)

    def row(slug: str, label: str) -> str:
        return (f'<li><span class="wk">{label}</span>'
                f'<span class="t"><a href="{slug}/">{html.escape(titles[slug])}</a></span>'
                f'<a class="open" href="{slug}/">open</a></li>\n')

    rows = "".join(row(r.lab, f"week {r.week}") for r in scheduled)
    optional = ""   # every lab is a schedule row now; the shape gate forbids strays

    index_body = (f"<h1>Labs</h1>\n"
                  f"<p>The module's lab exercises in teaching order, one page per "
                  f"lab — read-only previews of the instructions, always the "
                  f"current version. To complete a lab you work in your own copy "
                  f'of the repo: <a href="{REPO_URL}/generate">Use this template</a>, '
                  f"then open a Codespace on it.</p>\n"
                  f"<p><strong>Before your first lab</strong>, sign up for the "
                  f'<a href="https://education.github.com/pack">GitHub Student '
                  f"Developer Pack</a>. It is free for verified students and gives "
                  f"you the Copilot Student plan — the editor assistant and the "
                  f"terminal agent these labs use — and Pro-level Codespaces. "
                  f"Verification can take a few days, so do it early.</p>\n"
                  f"<ul class=\"row-list\">\n{rows}</ul>\n{optional}"
                  f'<p class="kicker"><a href="../">back to the lecture decks</a></p>')
    (out_labs / "index.html").write_text(
        page("AIAP Labs", "ai-assisted programming", index_body, False),
        encoding="utf-8", newline="\n")
    print(f"wrote {len(labs)} lab pages ({pages} pages in all) + labs index under {out_labs}, "
          f"{mcq_pages} MCQ pages under {out / 'mcq'}")


if __name__ == "__main__":
    main()
