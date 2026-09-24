#!/usr/bin/env python3
"""Speaker notes exist for an AI first. Check they are written that way.

The convention (see AGENTS.md, "Speaker notes are primarily FOR AN AI"):
notes are read mainly by an assistant helping a student who is stuck on a
slide, and only incidentally by a presenter. The presenter's half -- pacing
and tempo -- is a by-product.

The asymmetry that makes this worth a gate: a slide states the RIGHT
answer. It never states the wrong one, and the wrong one is the entire
reason a `Predict:` slide exists. An assistant can infer what the code
does; it cannot infer which mistaken model a learner characteristically
reaches for. If that is not written down, the assistant explains the
correct answer to someone who needed their error diagnosed.

Checks, per deck:

  1. Every slide has a note. A slide with none is invisible to an
     assistant beyond its own bullets.
  2. Every `Predict:` slide's note names the MISCONCEPTION -- the wrong
     answer to expect, and ideally the faulty reasoning behind it. This is
     the mandatory one.
  3. Timing markers use `~H:MM` cumulative elapsed, matching the sibling
     module. `~47:00` is a common slip meaning 47 minutes; in this format
     that reads as 47 hours.
  4. A note is not MOSTLY stage direction. Choreography is worth a clause;
     a note made of it carries nothing an assistant can use.

Run from the repo root:  python scripts/check_speaker_notes.py
"""
import re
import sys
from pathlib import Path

ROOT = Path("lectures-and-labs")

NOTE_RE = re.compile(r"<!--\s*Speaker notes:(.*?)-->", re.S)
HEADING_RE = re.compile(r"(?m)^#{1,2}\s+(.+?)\s*$")
PREDICT_RE = re.compile(r"(?i)^#{1,2}\s*Predict\b")

# Language that names the wrong answer rather than the right one.
MISCONCEPTION_RE = re.compile(
    r"(?i)wrong answer|misconception|expect the room|faulty|"
    r"students? (?:assume|think|believe|expect)|"
    r"the room (?:assumes|thinks|guesses|expects)|commonly assume")

# `~H:MM` — lectures are two-hour slots, so hours is 0 or 1 and minutes is
# 0-59. Anything from 2:00 up is the M:SS slip (`~47:00` meaning 47 minutes).
GOOD_TIMING_RE = re.compile(r"~(\d+):([0-5]\d)\b")

STAGE_RE = re.compile(
    r"(?i)ask for hands|take a vote|show of hands|expect photograph|"
    r"read it out|pause here|put it (?:up|on the board)|deadpan|"
    r"walk (?:the|to)|take answers|take hands")


def slides_of(text: str) -> list[str]:
    """Split a deck into slides on `---` at line start, dropping frontmatter."""
    parts = re.split(r"(?m)^---\s*$", text)
    return parts[2:] if len(parts) > 2 else parts


def check(deck: Path) -> list[str]:
    text = deck.read_text(encoding="utf-8")
    rel = deck.as_posix()
    findings = []

    for i, slide in enumerate(slides_of(text), start=1):
        heading_m = HEADING_RE.search(slide)
        heading = heading_m.group(1).strip() if heading_m else f"(slide {i})"
        notes = NOTE_RE.findall(slide)

        if not notes:
            if not slide.strip():
                continue
            findings.append(f"{rel}: slide {i} ({heading[:44]}) has no speaker note")
            continue

        note = " ".join(notes)
        is_predict = bool(heading_m and PREDICT_RE.match(heading_m.group(0)))

        if is_predict and not MISCONCEPTION_RE.search(note):
            findings.append(
                f"{rel}: slide {i} ({heading[:44]}) is a Predict slide but its "
                f"note never names the WRONG answer to expect — which is the "
                f"only thing an assistant cannot infer from the slide")

        # A two-hour lecture, so hours is 0 or 1 and minutes 0-59. Without
        # the hours<=1 rule, `~47:00` passes as "47 hours" -- which is
        # exactly the M:SS slip this check exists to catch.
        for hrs, mins in re.findall(r"~(\d+):(\d\d)\b", note):
            if int(hrs) > 1 or int(mins) > 59:
                findings.append(
                    f"{rel}: slide {i}: timing ~{hrs}:{mins} is not ~H:MM "
                    f"cumulative elapsed — twenty minutes in is ~0:20 and an "
                    f"hour and ten is ~1:10, not ~70:00")
        if re.search(r"~\d+:\d", note) and not GOOD_TIMING_RE.search(note):
            findings.append(
                f"{rel}: slide {i}: timing marker is malformed — expected "
                f"~H:MM cumulative elapsed")

        # CONCEPT-FIRST. The note's opening sentence is what a reader --
        # human or machine -- weights most, and an assistant helping a stuck
        # student can use none of "ask for hands". Choreography is welcome
        # later in the note; it must not be the first thing said.
        body = re.sub(r"^\s*~\d+:\d\d\.?\s*", "", note.strip())
        first = re.split(r"(?<=[.!?])\s", body, maxsplit=1)[0] if body else ""
        if first and STAGE_RE.search(first):
            findings.append(
                f"{rel}: slide {i} ({heading[:40]}): note OPENS with stage "
                f"direction — lead with what the slide teaches, then the "
                f"misconception. Choreography goes last, if at all")

        # And a note that is nothing but choreography carries nothing.
        words = len(body.split())
        if words < 30 and len(STAGE_RE.findall(note)) >= 2:
            findings.append(
                f"{rel}: slide {i} ({heading[:40]}): note is mostly stage "
                f"direction ({words} words) — say what the slide TEACHES")
    return findings


def main() -> int:
    if not ROOT.is_dir():
        return 0
    decks = sorted(ROOT.glob("*/*-lecture.md"))
    findings, n_notes, n_predict = [], 0, 0
    for deck in decks:
        text = deck.read_text(encoding="utf-8")
        n_notes += len(NOTE_RE.findall(text))
        n_predict += len(PREDICT_RE.findall(text))
        findings.extend(check(deck))

    for line in findings:
        print(line)
    if findings:
        print(f"\n{len(findings)} speaker-note problem(s). Notes are read "
              f"mainly by an assistant helping a student — see AGENTS.md.",
              file=sys.stderr)
        return 1

    print(f"check_speaker_notes: {n_notes} notes across {len(decks)} decks; "
          f"every Predict slide names its misconception")
    return 0


if __name__ == "__main__":
    sys.exit(main())
