#!/usr/bin/env python3
"""Show where you are in the prompting lab. Runs locally, reports nowhere.

    python scripts/check_progress.py

Two things happen. The lab's tests run — they FAIL until DIY 8 replaces the
placeholder test, and that is expected. Then each task file is compared
with the blank template you started from (git still has it), so a task
counts as having work in it once you have actually written something there.
Nothing is installed and nothing is scored: the Practical Assessment for
this lab is on Moodle and asks about the work itself, not this checklist.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GREEN, YELLOW, DIM, BOLD, RESET = "\x1b[32m", "\x1b[33m", "\x1b[2m", "\x1b[1m", "\x1b[0m"
TOTAL_TASKS = 11
MIN_NEW_CHARS = 60      # this much text beyond the template counts as work

# Fallback only, for a copy without git: the sections each task's file must
# contain, each with something written under it (substring matches against
# the template headings).
REQUIRED: dict[int, list[str]] = {
    1: ["bad prompt", "good prompt", "ai output", "why better"],
    2: ["good prompt", "ai output"],
    3: ["constraints", "non-goals", "ai output"],
    4: ["clarifying questions", "follow-up prompt", "ai output"],
    5: ["persona prompt", "raw ai review", "top 3"],
    6: ["(a) buggy", "(b) trimmed reasoning", "(c) micro tests", "(d) minimal fix", "(e) root cause"],
    7: ["few-shot", "strict constraints", "ai output"],
    9: ["prompt (unified diff request)", "ai diff output", "how you applied"],
    10: ["answer 1", "with the file", "what changed"],
}
PLACEHOLDERS = ["# paste", "paste the", "paste your", "todo", "fill in", "placeholder", "replace this"]


def git(*args: str) -> str | None:
    try:
        proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    except OSError:
        return None
    return proc.stdout if proc.returncode == 0 else None


def template_of(path: Path) -> str | None:
    """The file as it was when the lab was handed out, from git.

    In a copy made from the template that is the first commit; in the module
    repo itself HEAD holds the untouched file. None if git cannot say.
    """
    top = git("rev-parse", "--show-toplevel")
    if not top:
        return None
    rel = path.resolve().relative_to(Path(top.strip()).resolve()).as_posix()
    roots = git("rev-list", "--max-parents=0", "HEAD") or ""
    for ref in [r for r in roots.split() if r] + ["HEAD"]:
        text = git("show", f"{ref}:{rel}")
        if text is not None:
            return text
    return None


def read(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def has_work(path: Path, fallback_keys: list[str] | None = None) -> bool:
    """True once the file holds real text beyond the template it started as."""
    current = read(path)
    if current is None:
        return False
    template = template_of(path)
    if template is not None:
        old_lines = {ln.strip() for ln in template.splitlines()}
        new_text = "".join(ln.strip() for ln in current.splitlines()
                           if ln.strip() and ln.strip() not in old_lines)
        return len(new_text) >= MIN_NEW_CHARS
    return _heuristic(current.lower(), fallback_keys or [])


def _heuristic(text: str, keys: list[str]) -> bool:
    if len(text.strip()) < 30 or not keys:
        return False
    lines = text.splitlines()

    def substance_after(key: str) -> bool:
        for idx, line in enumerate(lines):
            if key not in line:
                continue
            for nxt in lines[idx + 1: idx + 9]:
                nxt = nxt.strip()
                if not nxt or nxt.startswith("#"):
                    continue
                if any(p in nxt for p in PLACEHOLDERS):
                    return False
                if len(nxt) >= 6:
                    return True
            return False
        return False

    return all(key in text and substance_after(key) for key in keys)


def run_tests() -> tuple[bool, str]:
    """Run the lab's tests. Returns (all passed, one-line summary)."""
    cmd = [sys.executable, "-m", "pytest", "lab/tests", "-q", "--no-header", "-p", "no:cacheprovider"]
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    except OSError as e:
        return False, f"could not start pytest: {e}"
    if "No module named pytest" in proc.stderr:
        return False, "pytest is not installed — run: pip install -r requirements.txt"
    lines = [ln.strip("= ").strip() for ln in proc.stdout.splitlines() if ln.strip()]
    return proc.returncode == 0, (lines[-1] if lines else "no output from pytest")


def main() -> int:
    print(f"\n{BOLD}Prompting lab — progress{RESET} {DIM}(local only; nothing is sent or scored){RESET}\n")

    tests_ok, summary = run_tests()
    if tests_ok:
        print(f"  {GREEN}Tests (DIY 8): pass{RESET} — {summary}")
    else:
        print(f"  {YELLOW}Tests (DIY 8): not passing{RESET} — {summary}")
        print(f"  {DIM}Expected until DIY 8 replaces the placeholder test with real ones.{RESET}")

    prompts = ROOT / "lab" / "prompts"
    done: list[int] = []
    for task in list(range(1, 8)) + [10]:
        if has_work(prompts / f"task{task}.md", REQUIRED[task]):
            done.append(task)
    if tests_ok:
        done.append(8)
    if has_work(prompts / "task9.md", REQUIRED[9]) and has_work(ROOT / "lab" / "diffs" / "task9.diff"):
        done.append(9)
    if has_work(ROOT / "lab" / "REFLECTION.md"):
        done.append(11)
    todo = [t for t in range(1, TOTAL_TASKS + 1) if t not in done]

    print()
    print(f"  {GREEN}Tasks with work in them:{RESET} {' '.join(map(str, sorted(done))) or '—'}")
    print(f"  {YELLOW}Tasks still to do:{RESET}       {' '.join(map(str, todo)) or '—'}")
    print(f"\n  {len(done)}/{TOTAL_TASKS} tasks show work. {DIM}Run this again any time.{RESET}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
