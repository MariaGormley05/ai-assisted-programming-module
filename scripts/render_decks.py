#!/usr/bin/env python3
"""Render every lecture for the site: lectures-and-labs/<weekNN>/<topic>-lecture.md ->
OUTPUT_DIR/<topic>/index.html and OUTPUT_DIR/<topic>/slides.pdf.

<topic> is the schedule's `lecture` name, not the week folder, so a lecture keeps
its web address when the semester is renumbered. A week's img/ folder is copied
beside the output. The Marp CLI is `marp` (CI installs it globally); set MARP to
run it another way, e.g. MARP="npx --no-install marp".

stdin is closed for every marp call: marp-cli treats piped stdin as an extra
markdown input, which once turned a loop over the decks into "Converting 2
markdowns" and an output-path error.

Usage:
    python scripts/render_decks.py [OUTPUT_DIR]      # default: build
"""
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schedule import load  # noqa: E402

THEME = "themes/aiap.css"


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
