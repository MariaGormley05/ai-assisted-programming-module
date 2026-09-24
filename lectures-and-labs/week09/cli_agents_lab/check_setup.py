"""Confirm this lab can run before you start it.

    python check_setup.py

Checks Python, Node (the agents are npm packages and need Node 22 or
newer), git, whether a terminal agent is installed yet, and the files the
exercises use. Prints one line per check and exits non-zero if anything
essential is missing. It never reads or prints a token.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
NEEDED = ["policy/policy_check.py", "policy/team-policy.json",
          "policy/commands.txt", "sample-app/stats.py",
          "sample-app/test_stats.py"]
AGENTS = ("copilot", "gemini")


def line(ok: bool, label: str, detail: str = "") -> bool:
    print(f"  [{'ok' if ok else '  '}] {label}{'  — ' + detail if detail else ''}")
    return ok


def node_major() -> int | None:
    """Node's major version, or None if Node is missing or will not run."""
    node = shutil.which("node")
    if not node:
        return None
    try:
        out = subprocess.run([node, "--version"], capture_output=True,
                             text=True, encoding="utf-8", errors="replace", timeout=10).stdout
    except (OSError, subprocess.TimeoutExpired):
        return None
    m = re.match(r"v(\d+)", out.strip())
    return int(m.group(1)) if m else None


def main() -> int:
    print("CLI agents lab setup check\n")
    good = True

    v = sys.version_info
    good &= line(v >= (3, 10), f"Python {v.major}.{v.minor}",
                 "" if v >= (3, 10) else "3.10 or newer required")

    major = node_major()
    if major is None:
        good &= line(False, "Node", "not found — the agents need Node 22+")
    else:
        good &= line(major >= 22, f"Node {major}",
                     "" if major >= 22 else "22 or newer required")

    has_git = shutil.which("git") is not None
    good &= line(has_git, "git", "" if has_git else "not found")

    # Not essential: DIY 1 is where you install one.
    found = [name for name in AGENTS if shutil.which(name)]
    line(bool(found), "terminal agent",
         ", ".join(found) if found else "none yet — DIY 1 installs one")

    for rel in NEEDED:
        present = (HERE / rel).is_file()
        good &= line(present, rel, "" if present else "missing")

    print()
    print("Ready." if good else "Something above needs fixing before you start.")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
