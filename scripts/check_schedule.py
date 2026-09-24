#!/usr/bin/env python3
"""CI gate: module/schedule.json is the module's only schedule, and every view agrees.

Fails (exit 1, every finding listed) when:
  - the schedule itself is malformed: a startDate that is not a Monday, week
    numbers not 1..N in order, no lecture on a row that is neither an MCQ nor
    the reading week, a lecture row with no topic;
  - a row's folder under lectures-and-labs/ (named from its week number) is
    missing, or does not hold what the row promises: a teaching week holds
    exactly one lecture, <deck>-lecture.md for that deck (its frontmatter
    `topic` is the deck); a lab week also holds <lab>_lab/ with README.md,
    no other folder, and no README.md at week level; an MCQ week and the
    reading week hold README.md, titled without a week number;
  - a tracked file under lectures-and-labs/ belongs to no schedule row, or
    anything is tracked under the retired lectures/ or labs/ layout, or an
    mcq/ folder is claimed by no row;
  - a deck declares `week:` in its frontmatter or a week number in its title
    kicker, or an MCQ page titles itself with a week -- the schedule is
    stated ONCE;
  - README.md or lectures-and-labs/README.md holds a stale week table (run
    update_current_week.py);
  - module/module-overview.md's topic table is missing a lecture topic or
    lists them out of schedule order.

Usage:
    python scripts/check_schedule.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schedule import MCQ, ROOT, load  # noqa: E402
import update_current_week  # noqa: E402

OVERVIEW = Path("module/module-overview.md")
VSCODE = Path(".vscode/settings.json")
README = Path("README.md")
TABLE_RE = re.compile(r"<!-- schedule-table:start -->\n(.*?)<!-- schedule-table:end -->", re.S)
TOPIC_RE = re.compile(r'(?m)^topic:\s*"?([^"\n]+?)"?\s*$')


def tracked(*paths: str) -> list[str]:
    out = subprocess.run(["git", "ls-files", "--", *paths], capture_output=True,
                         text=True, encoding="utf-8", check=True)
    return [p for p in out.stdout.splitlines() if p]


def frontmatter_topic(text: str) -> str | None:
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    t = TOPIC_RE.search(m.group(1))
    return t.group(1).strip() if t else None


def first_line(path: Path) -> str:
    return path.read_text(encoding="utf-8").splitlines()[0]


def table_findings(path: Path, want: str) -> list[str]:
    """The committed week table in `path` must be what the schedule renders now
    (the ➡️ current-week marker aside, which moves on its own every Monday)."""
    text = path.read_text(encoding="utf-8")
    m = TABLE_RE.search(text)
    if not m:
        return [f"{path.as_posix()}: schedule-table markers are missing"]
    committed = re.sub(r"\*\*➡️ (.*?)\*\*", r"\1", m.group(1)).strip()
    if committed != want.strip():
        return [f"{path.as_posix()}: the week table is stale; run scripts/update_current_week.py"]
    return []


def main() -> None:
    findings: list[str] = []
    sched = load()

    if sched.start.weekday() != 0:
        findings.append(f"start {sched.start} is a {sched.start:%A}, not a Monday")
    numbered = [r.week for r in sched.rows if not r.is_break]
    if numbered != [str(n) for n in range(1, len(numbered) + 1)]:
        findings.append(f"week numbers must run 1..N in order; got {numbered}")

    folders = {r.dir for r in sched.rows}
    for r in sched.rows:
        d = r.path
        if not r.deck and not r.mcq and not r.is_break:
            findings.append(f"week {r.week}: has no lecture, is not an MCQ and is not the reading week")
        if not d.is_dir():
            findings.append(f"week {r.week}: {d.as_posix()}/ does not exist")
            continue
        lectures = sorted(p.name for p in d.iterdir()
                          if p.is_file() and p.name.endswith("-lecture.md"))
        # Local caches (__pycache__, .pytest_cache) are not part of the shape.
        subdirs = sorted(p.name for p in d.iterdir()
                         if p.is_dir() and p.name != "img"
                         and not p.name.startswith((".", "__")))

        if r.deck:
            if not r.topic:
                findings.append(f"week {r.week}: a lecture row needs a topic")
            if not r.lecture.is_file():
                findings.append(f"week {r.week}: {r.lecture.as_posix()} does not exist")
            else:
                topic = frontmatter_topic(r.lecture.read_text(encoding="utf-8"))
                if topic != r.deck:
                    findings.append(f"week {r.week}: {r.lecture.as_posix()} is the {topic!r} "
                                    f"lecture, but the schedule names {r.deck!r}")
            extra = [n for n in lectures if n != r.lecture.name]
            if extra:
                findings.append(f"week {r.week}: {d.as_posix()}/ also holds {extra}; "
                                f"the lecture is {r.lecture.name}")
        elif lectures:
            findings.append(f"week {r.week}: {d.as_posix()}/ holds {lectures}, but the "
                            f"schedule has no lecture this week")

        if r.lab:
            if not r.deck:
                findings.append(f"week {r.week}: a lab row needs a lecture")
            ld = r.lab_dir
            if not ld.is_dir():
                findings.append(f"week {r.week}: {ld.as_posix()}/ (the lab folder) does not exist")
            elif not (ld / "README.md").is_file():
                findings.append(f"week {r.week}: {(ld / 'README.md').as_posix()} "
                                f"(the lab instructions) does not exist")
            extra = [n for n in subdirs if n != r.lab_folder]
            if extra:
                findings.append(f"week {r.week}: {d.as_posix()}/ holds folders {extra}; "
                                f"the lab folder is {r.lab_folder}/")
            if (d / "README.md").is_file():
                findings.append(f"week {r.week}: {d.as_posix()}/README.md exists, but a lab "
                                f"week keeps its README inside {r.lab_folder}/")
        elif subdirs:
            findings.append(f"week {r.week}: {d.as_posix()}/ holds folders {subdirs}, but "
                            f"the schedule has no lab this week")

        if r.mcq or r.is_break:
            readme = r.explainer
            if not readme.is_file():
                findings.append(f"week {r.week}: {readme.as_posix()} does not exist")
            elif re.search(r"[Ww]eek \d", first_line(readme)):
                findings.append(f"{readme.as_posix()}: the title must not state a week number")
        if r.mcq and not r.page.is_file():
            findings.append(f"week {r.week}: {r.page.as_posix()} does not exist")

    for f in tracked(ROOT.as_posix()):
        parts = f.split("/")
        if len(parts) == 2 and parts[1] == "README.md":
            continue
        if len(parts) < 3 or parts[1] not in folders:
            findings.append(f"{f}: {ROOT.as_posix()}/{parts[1]}/ is not the folder of any "
                            f"schedule row")
    for f in tracked("lectures", "labs"):
        findings.append(f"{f}: the lectures/ and labs/ layout is retired; everything lives "
                        f"under {ROOT.as_posix()}/")
    if MCQ.is_dir():
        claimed = {f"mcq{r.mcq}" for r in sched.rows if r.mcq}
        for d in sorted(p.name for p in MCQ.iterdir() if p.is_dir()):
            if d not in claimed:
                findings.append(f"mcq/{d}/ is not in module/schedule.json")

    for deck in sorted(ROOT.glob("*/*-lecture.md")):
        text = deck.read_text(encoding="utf-8")
        if re.search(r"(?m)^week:", text):
            findings.append(f"{deck.as_posix()}: frontmatter must not declare week: "
                            f"(the folder name does)")
        if re.search(r'class="kicker">// week \d', text):
            findings.append(f"{deck.as_posix()}: the title kicker must not state a week number")
    for r in sched.rows:
        if r.page and r.page.is_file() and re.search(r"[Ww]eek \d", first_line(r.page)):
            findings.append(f"{r.page.as_posix()}: the title must not state a week number")

    findings += table_findings(
        README, update_current_week.render_table(sched, None, update_current_week.FROM_ROOT))
    findings += table_findings(
        ROOT / "README.md", update_current_week.render_table(sched, None, update_current_week.FROM_INDEX))

    topics = [r.topic for r in sched.rows if r.deck]
    cells = []
    for line in OVERVIEW.read_text(encoding="utf-8").splitlines():
        m2 = re.match(r"^\|\s*([^|]+?)\s*\|", line)
        if m2 and m2.group(1) not in ("Topic", "---"):
            cells.append(re.sub(r"&amp;", "&", m2.group(1)).strip("* "))
    last = -1
    for t in topics:
        idx = next((i for i, c in enumerate(cells) if c == t), None)
        if idx is None:
            findings.append(f"{OVERVIEW.as_posix()}: no row for '{t}' in the topic table")
        elif idx < last:
            findings.append(f"{OVERVIEW.as_posix()}: '{t}' is out of schedule order")
        else:
            last = idx

    # The editor's import search path lists every lab folder, so Pylance can
    # resolve a lab's own packages (`from lab.code...`, `from hello_app...`)
    # without the student opening that folder as a workspace of its own.
    want_paths = [r.lab_dir.as_posix() for r in sched.rows if r.lab]
    try:
        have_paths = json.loads(VSCODE.read_text(encoding="utf-8")).get(
            "python.analysis.extraPaths", [])
    except (OSError, ValueError) as e:
        findings.append(f"{VSCODE.as_posix()}: unreadable ({e})")
        have_paths = want_paths
    if have_paths != want_paths:
        findings.append(f"{VSCODE.as_posix()}: python.analysis.extraPaths must list the "
                        f"lab folders in schedule order: {want_paths}")

    if findings:
        print("\n".join("check_schedule: " + f for f in findings))
        sys.exit(1)
    how = "derived from the October bank holiday" if sched.derived else "from startDate"
    print(f"check_schedule: {len(sched.rows)} rows; week 1 begins {sched.start} ({how}); "
          f"every view agrees")


if __name__ == "__main__":
    main()
