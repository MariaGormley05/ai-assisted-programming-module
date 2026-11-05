"""Confirm this lab can run before you start it.

    python check_setup.py

Checks Python, the files the exercises use, and outbound access to PyPI
(DIY 3 needs it). Prints one line per check and exits non-zero if
anything essential is missing.
"""
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
NEEDED = ["vulnerable_app.py", "verify_deps.py", "summariser.py",
          "documents/clean.txt", "documents/poisoned.txt"]


def line(ok: bool, label: str, detail: str = "") -> bool:
    print(f"  [{'ok' if ok else '  '}] {label}{'  — ' + detail if detail else ''}")
    return ok


def main() -> int:
    print("Security lab setup check\n")
    good = True

    v = sys.version_info
    good &= line(v >= (3, 10), f"Python {v.major}.{v.minor}",
                 "" if v >= (3, 10) else "3.10 or newer required")

    for rel in NEEDED:
        good &= line((HERE / rel).is_file(), rel,
                     "" if (HERE / rel).is_file() else "missing")

    # DIY 3 asks PyPI whether a package exists, so the check is only
    # meaningful if PyPI is reachable from here.
    try:
        with urllib.request.urlopen("https://pypi.org/pypi/requests/json",
                                    timeout=10) as r:
            reachable = r.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        reachable = False
    good &= line(reachable, "PyPI reachable",
                 "" if reachable else "DIY 3 needs outbound HTTPS")

    print()
    print("Ready." if good else "Something above needs fixing before you start.")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
