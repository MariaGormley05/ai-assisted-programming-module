#!/usr/bin/env python3
"""Check that the lab code students are handed is not broken.

Two levels, because this module's labs cannot all be verified to the same
depth and pretending otherwise would be the real failure:

  1. SYNTAX -- every .py in every scheduled lab folder is byte-compiled. No dependencies, no
     network, no keys. Runs for every lab, always.

  2. TESTS -- where a lab ships tests, pytest runs them. One lab needs
     live API access (see NEEDS_KEY) and cannot pass in CI without secrets,
     so its tests are reported as SKIPPED rather than quietly dropped.

Point 2 is the honest limit of this gate and it is printed on every run: a
lab in NEEDS_KEY has had its syntax checked and nothing more. The rule is
the same one the safety audit follows -- state what was not verified rather
than let a green tick imply it was.

Run from the repo root:
    python scripts/verify_labs.py            # syntax + runnable tests
    python scripts/verify_labs.py --syntax   # syntax only (no pytest)

Exits 1 if anything fails to compile or a runnable test fails.
"""
import argparse
import py_compile
import re
import subprocess
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schedule import load  # noqa: E402

# Labs whose tests need live API access or a cloud project, so CI cannot run
# them without secrets. Their syntax is still checked. Keep this list SHORT
# and justified -- it is a list of things this gate does not guarantee.
NEEDS_KEY = {
    "rag": "an LLM API key for the generation half",
}

# Test files whose expected state is RED. Two kinds: SCAFFOLDING the student
# replaces (prompting), and a real test that fails because the lab hands the
# student a planted bug to fix (cli-agents, where an agent is pointed at it).
# Either way a normal pytest run would report the lab broken forever.
#
# The check is inverted instead, which turns a nuisance into a useful gate:
# if a placeholder starts PASSING, someone has committed a worked solution
# into the public repo. Given that solutions live in a separate private repo
# and this module's tutor brief puts no restriction on the assistant, that
# boundary is worth watching automatically.
PLACEHOLDER_TESTS = {
    "prompting": ["lab/tests/test_extract_domain.py"],
    "cli-agents": ["sample-app/test_stats.py"],
}

TEST_GLOBS = ("test_*.py", "*_test.py")

# A collection error naming one of these is "the lab's dependencies are not
# installed", not "the lab is broken". Reported differently so a developer
# without every lab's requirements installed does not see nine red lines.
THIRD_PARTY_HINTS = ("flask", "fastapi", "chromadb", "sentence_transformers",
                     "google", "firebase", "mcp", "openai", "anthropic",
                     "uvicorn", "pydantic", "httpx", "requests", "numpy")


def lab_dirs() -> list[tuple[str, Path]]:
    """(site slug, source folder) for every scheduled lab, in teaching order:
    ("cicd", lectures-and-labs/week10/cicd_lab). NEEDS_KEY, PLACEHOLDER_TESTS
    and the report are keyed by the slug, which never changes; the folder
    moves when the schedule is renumbered."""
    return [(r.lab, r.lab_dir) for r in load().rows if r.lab]


def slug_of(lab: Path) -> str:
    """cli_agents_lab -> cli-agents (the inverse of schedule.Row.lab_folder)."""
    return lab.name[:-len("_lab")].replace("_", "-")


def python_files(lab: Path) -> list[Path]:
    return sorted(p for p in lab.rglob("*.py")
                  if "__pycache__" not in p.parts and "node_modules" not in p.parts)


def test_files(lab: Path) -> list[Path]:
    found: set[Path] = set()
    for pattern in TEST_GLOBS:
        found.update(p for p in lab.rglob(pattern)
                     if "__pycache__" not in p.parts
                     and "node_modules" not in p.parts)
    placeholders = {(lab / rel).resolve()
                    for rel in PLACEHOLDER_TESTS.get(slug_of(lab), [])}
    return sorted(p for p in found if p.resolve() not in placeholders)


def compile_lab(lab: Path) -> list[str]:
    errors = []
    for path in python_files(lab):
        try:
            py_compile.compile(str(path), cfile=None, doraise=True)
        except py_compile.PyCompileError as e:
            first = str(e).strip().split("\n")[0]
            errors.append(f"{path.as_posix()}: {first}")
    return errors


def _pytest(lab: Path, targets: list[str]) -> subprocess.CompletedProcess:
    """Run pytest from INSIDE the lab directory.

    cwd matters: labs are self-contained projects, and their tests import
    their code as a top-level package (the cicd lab's tests/test_app.py does
    `from hello_app.webapp import app`). Run from the repo root, that import
    fails and the lab looks broken when it is merely being run from the
    wrong place. Students run it from the lab folder; so does this.
    """
    return subprocess.run(
        [sys.executable, "-m", "pytest", *targets, "-q", "--no-header",
         "-p", "no:cacheprovider"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(lab))


def _missing_dependency(output: str) -> str | None:
    """Name the third-party module a collection error is really about."""
    m = re.search(r"No module named '([^']+)'", output or "")
    if not m:
        return None
    root = m.group(1).split(".")[0].lower()
    return m.group(1) if root in THIRD_PARTY_HINTS else None


def run_tests(lab: Path) -> tuple[str, str]:
    """Run a lab's real tests. Returns (status, summary) where status is
    'pass', 'fail' or 'deps'."""
    # Placeholders are judged on their own by check_placeholders, and they
    # are meant to be red -- so they stay out of this run, or a lab holding
    # both kinds of test would always look broken.
    ignore = ["--ignore=" + rel for rel in PLACEHOLDER_TESTS.get(slug_of(lab), [])]
    r = _pytest(lab, [".", *ignore])
    out = (r.stdout or "") + (r.stderr or "")
    tail = [ln for ln in out.strip().split("\n") if ln.strip()]
    summary = tail[-1] if tail else "(no output)"

    missing = _missing_dependency(out)
    if missing:
        return "deps", f"needs {missing} — pip install -r requirements.txt"
    # exit 5 == "no tests collected", which is not a failure: every test file
    # this lab has may be a student placeholder.
    return ("pass" if r.returncode in (0, 5) else "fail"), summary


def check_placeholders(lab: Path) -> list[str]:
    """Confirm each student-placeholder test is still RED.

    A placeholder that passes means a worked solution reached the public
    repo. See PLACEHOLDER_TESTS.
    """
    findings = []
    for rel in PLACEHOLDER_TESTS.get(slug_of(lab), []):
        if not (lab / rel).is_file():
            findings.append(f"{lab.as_posix()}/{rel}: placeholder test is "
                            f"listed in PLACEHOLDER_TESTS but does not exist")
            continue
        r = _pytest(lab, [rel])
        out = (r.stdout or "") + (r.stderr or "")
        if _missing_dependency(out):
            continue  # cannot judge without the lab's dependencies
        if r.returncode == 0:
            findings.append(
                f"{lab.as_posix()}/{rel}: placeholder test PASSES — it is "
                f"meant to fail until the student writes it. A solution may "
                f"have been committed to the public repo.")
        elif r.returncode != 1 or "failed" not in out:
            # Exit 1 is "tests failed". Anything else (2 interrupted, 3
            # internal, 4 usage, 5 nothing collected) is broken scaffolding
            # that would look red for the wrong reason.
            findings.append(
                f"{lab.as_posix()}/{rel}: placeholder test could not be "
                f"judged — pytest exited {r.returncode} rather than failing "
                f"the assertion the student is meant to satisfy.")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--syntax", action="store_true",
                    help="compile only; do not run pytest")
    args = ap.parse_args()

    labs = lab_dirs()
    if not labs:
        print("verify_labs: the schedule names no labs — nothing to check")
        return 0

    failures: list[str] = []
    rows: list[tuple[str, int, str]] = []

    for name, lab in labs:
        errors = compile_lab(lab)
        failures.extend(errors)
        n_py = len(python_files(lab))

        if errors:
            rows.append((name, n_py, "COMPILE FAILED"))
            continue
        if args.syntax:
            rows.append((name, n_py, "syntax only (--syntax)"))
            continue
        if name in NEEDS_KEY:
            rows.append((name, n_py, f"tests SKIPPED — needs {NEEDS_KEY[name]}"))
            continue

        failures.extend(check_placeholders(lab))
        n_placeholder = len(PLACEHOLDER_TESTS.get(name, []))
        note = f" (+{n_placeholder} student placeholder)" if n_placeholder else ""

        tests = test_files(lab)
        if not tests:
            rows.append((name, n_py, f"no tests in this lab{note}"))
            continue
        status, summary = run_tests(lab)
        if status == "pass":
            rows.append((name, n_py, f"tests passed — {summary}{note}"))
        elif status == "deps":
            rows.append((name, n_py, f"tests not run — {summary}"))
            if os.environ.get("CI"):
                # Locally a missing package is a note; in CI every lab's
                # requirements were just installed, so it is a broken lab.
                failures.append(f"{lab.as_posix()}: {summary}")
        else:
            rows.append((name, n_py, f"TESTS FAILED — {summary}"))
            failures.append(f"{lab.as_posix()}: pytest failed — {summary}")

    width = max(len(r[0]) for r in rows)
    print("verify_labs:")
    for name, n_py, status in rows:
        print(f"  {name:<{width}}  {n_py:>3} .py  {status}")

    if NEEDS_KEY and not args.syntax:
        unverified = ", ".join(sorted(NEEDS_KEY))
        print(f"\n  NOT verified beyond syntax: {unverified} — these need "
              f"live credentials.\n  A green run does not mean their exercises "
              f"work end to end.")

    for line in failures:
        print(f"\n{line}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
