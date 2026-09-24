#!/usr/bin/env python3
"""The module schedule: ONE file, module/schedule.json, that every view derives from.

The README's banner and schedule table, module/module-overview.md's topic
table, the site index and its redirect stubs, the labs page order, the
published schedule.json the Moodle course page reads, and the CI gate
(scripts/check_schedule.py) all import this module and read that file.
Nothing else in the repo may state a week number or a semester date.

Rows are consecutive calendar weeks; the "X" reading-week row is one of them,
so row i covers start + 7*i days. The start is DERIVED unless the file says
otherwise: reading week is always the week of the Irish October bank holiday
(the last Monday of October), so week 1 begins that many weeks earlier as
there are rows before the X row. A `startDate` (a Monday, YYYY-MM-DD) in the
file overrides the rule for a year that breaks it.

    from schedule import load
    sched = load()                       # this year's calendar
    for row in sched.rows: ...
    row = sched.row_for(datetime.date.today())   # None outside the semester
    sched.to_public()                    # builder-format dict, absolute URLs

The file is the same shape as an export from the lecturer's
module-schedule-table-builder app, minus the URLs: a row names its lecture and
lab by site folder (`lecture`, `lab`), and an export's `lectureUrl`/`labUrl` are
accepted in their place. Those names are the site addresses (/<lecture>/ and
/labs/<lab>/) and never change; the SOURCE lives in one folder per row under
lectures-and-labs/, named from the week (Row.dir, Row.lecture, Row.lab_dir).
"""
from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass
from pathlib import Path

SCHEDULE = Path("module/schedule.json")
SITE = "https://danielcregg.is-a.dev/ai-assisted-programming/"
# One folder per schedule row under lectures-and-labs/, named from the week
# number (week01 ... week12; the reading week is week{NN}b-reading-week, right
# after week NN so it sorts in place). A teaching week holds <deck>-lecture.md;
# a lab week also holds <lab>_lab/ (the site slug with hyphens as underscores,
# so the folder is a valid Python package name) with README.md and the starter
# code. MCQ weeks and the reading week hold a README.md explainer.
ROOT = Path("lectures-and-labs")
MCQ = Path("mcq")
MCQ_RE = re.compile(r"^MCQ (\d)\b")
NAME_RE = re.compile(r"^[a-z0-9-]+$")


@dataclass(frozen=True)
class Row:
    index: int          # position in the semester, 0-based, reading week included
    week: str           # "1".."12", or "X" for the reading week
    topic: str          # "Coding Agents"; empty on MCQ and reading-week rows
    deck: str | None    # the lecture's site folder (/<deck>/) and the stem of <deck>-lecture.md
    lab: str | None     # the lab's site folder (/labs/<lab>/); its source folder is <lab>_lab/
    assessment: str     # "PA3 (4%)", "MCQ 1 (32%)", or empty
    notes: str
    dir: str            # its folder under lectures-and-labs/: week05, week06b-reading-week

    @property
    def is_break(self) -> bool:
        return self.week == "X"

    @property
    def mcq(self) -> str | None:
        """'1' for the MCQ 1 row, else None."""
        m = MCQ_RE.match(self.assessment)
        return m.group(1) if m else None

    @property
    def page(self) -> Path | None:
        """The non-teaching page an MCQ row owns: mcq/mcq<n>/README.md."""
        return MCQ / f"mcq{self.mcq}" / "README.md" if self.mcq else None

    @property
    def label(self) -> str:
        return self.topic or self.assessment or self.notes

    @property
    def path(self) -> Path:
        """The week's folder: lectures-and-labs/<dir>/."""
        return ROOT / self.dir

    @property
    def lecture(self) -> Path | None:
        """The week's deck: lectures-and-labs/<dir>/<deck>-lecture.md."""
        return self.path / f"{self.deck}-lecture.md" if self.deck else None

    @property
    def lab_folder(self) -> str | None:
        """The lab folder's name: the site slug with hyphens as underscores plus
        _lab (cli-agents -> cli_agents_lab), so it is a valid Python package
        name and cannot be mistaken for the lecture beside it."""
        return f"{self.lab.replace('-', '_')}_lab" if self.lab else None

    @property
    def lab_dir(self) -> Path | None:
        """The lab: lectures-and-labs/<dir>/<lab_folder>/."""
        return self.path / self.lab_folder if self.lab_folder else None

    @property
    def explainer(self) -> Path:
        """The README.md an MCQ week or the reading week keeps in its folder."""
        return self.path / "README.md"


@dataclass(frozen=True)
class Schedule:
    start: datetime.date
    derived: bool        # True when start came from the bank-holiday rule
    rows: tuple[Row, ...]
    raw: dict

    @property
    def reading_index(self) -> int:
        return next(r.index for r in self.rows if r.is_break)

    def monday(self, row: Row) -> datetime.date:
        return self.start + datetime.timedelta(weeks=row.index)

    def sunday(self, row: Row) -> datetime.date:
        return self.monday(row) + datetime.timedelta(days=6)

    @property
    def end(self) -> datetime.date:
        """The first Monday after the last row."""
        return self.start + datetime.timedelta(weeks=len(self.rows))

    def row_for(self, day: datetime.date) -> Row | None:
        i = (monday_of(day) - self.start).days // 7
        return self.rows[i] if 0 <= i < len(self.rows) else None

    @property
    def teaching(self) -> tuple[Row, ...]:
        return tuple(r for r in self.rows if r.deck)

    def deck_for_lab(self, lab: str) -> str | None:
        for r in self.rows:
            if r.lab == lab:
                return r.deck
        return None

    def to_public(self) -> dict:
        """The schedule as the site publishes it (build/schedule.json).

        Builder-format rows with absolute URLs, so the Moodle course page and
        the builder app can both read it; plus the resolved start and whether
        it was derived, so a reader can re-derive next year's dates itself.
        """
        weeks = []
        for r in self.rows:
            weeks.append({
                "week": r.week, "topic": r.topic,
                "lectureUrl": f"{SITE}{r.deck}/" if r.deck else "",
                "videoUrl": "", "notebookLmUrl": "",
                "labUrl": f"{SITE}labs/{r.lab}/" if r.lab else "",
                "assessment": r.assessment, "notes": r.notes,
            })
        extra = {k: v for k, v in self.raw.items()
                 if k not in ("weeks", "startDate", "_comment")}
        return {**extra, "startDate": self.start.isoformat(), "startDateDerived": self.derived,
                "readingWeekIndex": self.reading_index, "site": SITE, "weeks": weeks}


def monday_of(day: datetime.date) -> datetime.date:
    return day - datetime.timedelta(days=day.weekday())


def bank_holiday_monday(year: int) -> datetime.date:
    """The Irish October bank holiday: the last Monday of October."""
    return monday_of(datetime.date(year, 10, 31))


def academic_year(day: datetime.date) -> int:
    """The autumn whose semester-1 calendar is in force on `day`.

    From July onward that is this year's; before July it is still last
    year's, so in January the banner says the semester finished (and when
    teaching returns) rather than that a semester nine months away has not
    started. The site index and the Moodle loader apply the same rule.
    """
    return day.year if day.month >= 7 else day.year - 1


def today() -> datetime.date:
    from zoneinfo import ZoneInfo
    return datetime.datetime.now(ZoneInfo("Europe/Dublin")).date()


def _name(w: dict, key: str, url_key: str, prefix: str, week: str) -> str | None:
    """A folder name from `key`, or from a builder-export URL under `prefix`."""
    name = str(w.get(key, "") or "").strip()
    url = str(w.get(url_key, "") or "").strip()
    if not name and url:
        if not (url.startswith(prefix) and url.endswith("/")):
            raise SystemExit(f"schedule: week {week}: {url_key} must be {prefix}<name>/ (got {url!r})")
        name = url[len(prefix):].strip("/")
    if not name:
        return None
    if not NAME_RE.match(name):
        raise SystemExit(f"schedule: week {week}: {key} names {name!r}, which is not a "
                         f"kebab-case folder name")
    return name


def load(path: Path = SCHEDULE, year: int | None = None) -> Schedule:
    """Load the schedule; `year` picks which year's calendar (default: this one)."""
    if not path.is_file():
        raise SystemExit(f"schedule: {path} is missing. It is the module's only schedule.")
    raw = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    previous = 0          # the last numbered week, which names the reading-week folder
    for i, w in enumerate(raw.get("weeks", [])):
        week = str(w.get("week", "")).strip()
        if week == "X":
            folder = f"week{previous:02d}b-reading-week"
        elif week.isdigit():
            previous = int(week)
            folder = f"week{previous:02d}"
        else:
            raise SystemExit(f"schedule: row {i + 1}: week must be a number or X (got {week!r})")
        rows.append(Row(
            index=i, week=week,
            topic=str(w.get("topic", "")).strip(),
            deck=_name(w, "lecture", "lectureUrl", SITE, week),
            lab=_name(w, "lab", "labUrl", SITE + "labs/", week),
            assessment=str(w.get("assessment", "")).strip(),
            notes=str(w.get("notes", "")).strip(),
            dir=folder,
        ))
    if not rows:
        raise SystemExit(f"schedule: {path} has no weeks")
    breaks = [r.index for r in rows if r.is_break]
    if len(breaks) != 1:
        raise SystemExit(f"schedule: {path} needs exactly one reading-week row (week \"X\"); found {len(breaks)}")

    if raw.get("startDate"):
        try:
            start = datetime.date.fromisoformat(str(raw["startDate"]))
        except ValueError:
            raise SystemExit(f"schedule: startDate must be YYYY-MM-DD (got {raw['startDate']!r})")
        derived = False
    else:
        if year is None:
            year = academic_year(today())
        start = bank_holiday_monday(year) - datetime.timedelta(weeks=breaks[0])
        derived = True
    return Schedule(start=start, derived=derived, rows=tuple(rows), raw=raw)
