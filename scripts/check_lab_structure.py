#!/usr/bin/env python3
"""Enforce the lab README formula (see AGENTS.md, "Lab formula").

These labs arrived by migration from nine separate GitHub Classroom repos
written by different hands at different times, so they disagreed about
almost everything: Task vs Part vs Exercise, whether hints existed, whether
a student could self-check at all. A student meeting a new lab each week
should not have to relearn where things are.

The required shape:

    # <title>
    ## What you'll learn
    ## Table of Contents
    ## Getting started
    ... numbered sections, each with `### DIY k: <name>` exercises ...
    ## Summary                                    <- LAST heading

and every `### DIY k` must carry all three of:

    1. numbered steps
    2. `**What you should have**` or `**Expected output**`
    3. a hint in <details><summary>Hint</summary>

CONFORMING is the exemption list, inverted on purpose: a lab is checked
only once it appears there. It now covers EVERY lab, which is the point it
was always aiming at -- so any new lab must be written to the formula, and
any existing one that regresses fails the build.

Run from the repo root:  python scripts/check_lab_structure.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schedule import load  # noqa: E402

# Labs rewritten to the formula and now enforced. ADD TO THIS as each lab is
# reworked -- never remove an entry to make a failure go away.
CONFORMING = {
    "agents", "cicd", "cli-agents", "mcp", "prompting", "rag", "security",
    "setup", "vibe-coding",
}

REQUIRED_SECTIONS = ("What you'll learn", "Table of Contents",
                     "Getting started", "Summary")

H2_RE = re.compile(r"(?m)^##\s+(?:[^\w\s]+\s*)?(.+?)\s*$")
DIY_RE = re.compile(r"(?m)^###\s+DIY\s+(\d+):\s*(.+?)\s*$")
STEP_RE = re.compile(r"(?m)^\s*\d+\.\s+\S")
DELIVERABLE_RE = re.compile(r"\*\*(?:What you should have|Expected output)\*\*")
HINT_RE = re.compile(r"<details>\s*<summary>\s*(?:<[^>]+>\s*)?Hint",
                     re.IGNORECASE)


FENCE_RE = re.compile(r"(?m)^\s*```")


def mask_fences(text: str) -> str:
    """Blank out fenced blocks, preserving offsets and line count.

    Needed because a `**What you should have**` block routinely SHOWS the
    student a markdown template to fill in, and those templates contain
    lines starting with `##`. Read literally, such a line looks like the
    next section heading and truncates the DIY body -- so the hint that
    follows it appears to be missing and the gate reports a lab as broken
    when it is fine. Masking rather than deleting keeps every offset valid
    for the callers.
    """
    out, in_fence = [], False
    for line in text.split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(" " * len(line))
        else:
            out.append(" " * len(line) if in_fence else line)
    return "\n".join(out)


def section_bodies(text: str) -> list[tuple[str, str]]:
    """(diy_label, body) for each DIY block, body running to the next heading."""
    out = []
    scan = mask_fences(text)          # headings only, fences neutralised
    matches = list(DIY_RE.finditer(scan))
    for i, m in enumerate(matches):
        start = m.end()
        # A DIY body ends at the next heading of ANY level -- the next DIY,
        # or the section that follows it.
        nxt = re.compile(r"(?m)^#{2,3}\s+").search(scan, start)
        end = nxt.start() if nxt else len(text)
        if i + 1 < len(matches):
            end = min(end, matches[i + 1].start())
        # Slice the ORIGINAL text: the body's real content is what matters
        # once the boundaries are known.
        out.append((f"DIY {m.group(1)}: {m.group(2)}", text[start:end]))
    return out


def check_lab(lab: Path) -> list[str]:
    readme = lab / "README.md"
    if not readme.is_file():
        return [f"{lab.as_posix()}: no README.md"]

    text = readme.read_text(encoding="utf-8")
    rel = readme.as_posix()
    findings: list[str] = []

    if not re.match(r"^#\s+\S", text):
        findings.append(f"{rel}: must open with a level-1 heading")

    # Same masking reason as section_bodies: a template inside a fenced
    # block can contain `## ...` lines that are not headings.
    headings = [h.strip() for h in H2_RE.findall(mask_fences(text))]
    for required in REQUIRED_SECTIONS:
        if not any(h.lower().startswith(required.lower()) for h in headings):
            findings.append(f"{rel}: missing `## {required}` section")

    if headings and not headings[-1].lower().startswith("summary"):
        findings.append(
            f"{rel}: `## Summary` must be the LAST section (found "
            f"`## {headings[-1]}` after it)")

    diys = section_bodies(text)
    if not diys:
        findings.append(f"{rel}: no `### DIY k: <name>` exercises found")

    numbers = [int(m.group(1)) for m in DIY_RE.finditer(text)]
    if numbers and numbers != list(range(1, len(numbers) + 1)):
        findings.append(
            f"{rel}: DIY numbering must run 1..n with no gaps, got {numbers}")

    for label, body in diys:
        if not STEP_RE.search(body):
            findings.append(f"{rel}: {label} has no numbered steps")
        if not DELIVERABLE_RE.search(body):
            findings.append(
                f"{rel}: {label} has no `**What you should have**` or "
                f"`**Expected output**` block — the student cannot self-check")
        if not HINT_RE.search(body):
            findings.append(f"{rel}: {label} has no <details> Hint block")
    return findings


def main() -> int:
    # (site slug -> source folder) for every scheduled lab: "cicd" ->
    # lectures-and-labs/week10/cicd_lab. CONFORMING is keyed by the slug.
    labs = {r.lab: r.lab_dir for r in load().rows if r.lab}
    if not labs:
        print("check_lab_structure: the schedule names no labs")
        return 0

    all_labs = sorted(labs)
    unknown = CONFORMING - set(all_labs)
    if unknown:
        print(f"check_lab_structure: CONFORMING names a lab that does not "
              f"exist: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 1

    findings: list[str] = []
    for name in all_labs:
        if name in CONFORMING:
            findings.extend(check_lab(labs[name]))

    for line in findings:
        print(line)
    if findings:
        return 1

    pending = [n for n in all_labs if n not in CONFORMING]
    print(f"check_lab_structure: {len(CONFORMING)} lab(s) conform")
    if pending:
        print(f"  not yet rewritten to the formula ({len(pending)}): "
              f"{', '.join(pending)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
