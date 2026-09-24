#!/usr/bin/env python3
"""Rewrite the current-week banner and the week tables from module/schedule.json.

All generated, so none can drift from the schedule:

    README.md
      <!-- current-week:start --> ... <!-- current-week:end -->    the banner
      <!-- schedule-table:start --> ... <!-- schedule-table:end -->  the week table
    lectures-and-labs/README.md
      <!-- schedule-table:start --> ... <!-- schedule-table:end -->  the same table,
                                        linked from inside that folder

The tables get a **➡️** marker on the current row (none outside term). Weeks
run Mon-Sun, Europe/Dublin. A GitHub Action runs this every Monday; the CI gate
scripts/check_schedule.py fails if a committed table is stale, so run it after
any change to module/schedule.json.

Usage:
    python scripts/update_current_week.py [--date YYYY-MM-DD]

--date overrides "today" for testing. Exit 0 always; the caller decides
whether anything changed (git diff).
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schedule import ROOT, Row, Schedule, academic_year, load  # noqa: E402

README = Path("README.md")
INDEX = ROOT / "README.md"
BANNER_RE = re.compile(r"<!-- current-week:start -->.*?<!-- current-week:end -->", re.DOTALL)
TABLE_RE = re.compile(r"<!-- schedule-table:start -->.*?<!-- schedule-table:end -->", re.DOTALL)

# Where each table's links start from: README.md sits at the repo root,
# lectures-and-labs/README.md inside the week folders' parent. (week folder
# prefix, mcq folder prefix)
FROM_ROOT = (f"{ROOT.as_posix()}/", "mcq/")
FROM_INDEX = ("", "../mcq/")


def banner(sched: Schedule, today: datetime.date) -> tuple[str, Row | None]:
    """Return (banner line, the current row or None)."""
    row = sched.row_for(today)
    if row is None:
        if today < sched.start:
            return (f"> 🗓️ **Semester has not started yet** — teaching begins the "
                    f"week of {sched.start:%d %b %Y}."), None
        if sched.derived:
            nxt = load(year=academic_year(today) + 1).start
            return (f"> 🗓️ **Semester finished** — teaching returns the week of "
                    f"{nxt:%d %b %Y}."), None
        return "> 🗓️ **Semester finished** — no more lectures or labs this semester.", None
    monday = sched.monday(row)
    if row.is_break:
        return (f"> 🗓️ **Reading week** (no lectures or labs) — week beginning "
                f"{monday:%d %b %Y}."), row
    if row.mcq:
        when = (row.notes[0].lower() + row.notes[1:]) if row.notes else "held during the lab slot"
        return (f"> 🗓️ **This week: {row.assessment}** — {when} (week beginning "
                f"{monday:%d %b %Y}). Read [what it covers]({row.page.as_posix()}) first."), row
    return (f"> 🗓️ **Current teaching week: {row.week} — {row.topic}** "
            f"(week beginning {monday:%d %b %Y})."), row


def table_row(row: Row, current: Row | None, links: tuple[str, str] = FROM_ROOT) -> str:
    folder, mcq = links
    week = "—" if row.is_break else row.week
    if current is not None and row.index == current.index:
        week = f"**➡️ {week}**"
    if row.deck:
        lecture = f"[slides]({folder}{row.dir}/{row.lecture.name})"
        if row.lab:
            lab = f"[lab]({folder}{row.dir}/{row.lab_folder}/README.md)"
        else:
            lab = f"_{row.notes}_" if row.notes else "—"
        return f"| {week} | {row.topic} | {lecture} | {lab} |"
    if row.mcq:
        name, _, rest = row.assessment.partition(" (")
        weight = f" ({rest}" if rest else ""
        note = f" · {row.notes[0].lower() + row.notes[1:]}" if row.notes else ""
        return (f"| {week} | **{name}**{weight}{note} | [details]({folder}{row.dir}/README.md) · "
                f"[what it covers]({mcq}mcq{row.mcq}/README.md) | — |")
    return f"| {week} | {row.notes or 'Reading week'} | [details]({folder}{row.dir}/README.md) | — |"


def render_table(sched: Schedule, current: Row | None, links: tuple[str, str] = FROM_ROOT) -> str:
    lines = ["| Week | Topic | Lecture | Lab |", "|---|---|---|---|"]
    lines += [table_row(r, current, links) for r in sched.rows]
    return "\n".join(lines) + "\n"


def replace_table(text: str, table: str, where: Path) -> str:
    if not TABLE_RE.search(text):
        raise SystemExit(f"{where} is missing the schedule-table markers")
    return TABLE_RE.sub(lambda _: "<!-- schedule-table:start -->\n" + table
                        + "<!-- schedule-table:end -->", text)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    args = ap.parse_args()
    if args.date:
        today = datetime.date.fromisoformat(args.date)
    else:
        from zoneinfo import ZoneInfo
        today = datetime.datetime.now(ZoneInfo("Europe/Dublin")).date()

    sched = load(year=academic_year(today))
    line, current = banner(sched, today)

    text = README.read_text(encoding="utf-8")
    if not BANNER_RE.search(text):
        raise SystemExit("README is missing the current-week markers")
    text = BANNER_RE.sub(lambda _: f"<!-- current-week:start -->\n{line}\n<!-- current-week:end -->", text)
    text = replace_table(text, render_table(sched, current, FROM_ROOT), README)
    README.write_text(text, encoding="utf-8", newline="\n")

    index = INDEX.read_text(encoding="utf-8")
    INDEX.write_text(replace_table(index, render_table(sched, current, FROM_INDEX), INDEX),
                     encoding="utf-8", newline="\n")
    print(line.encode("ascii", errors="ignore").decode().strip())


if __name__ == "__main__":
    main()
