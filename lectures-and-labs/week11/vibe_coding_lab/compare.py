"""Give every version of the to-do app the same exam, and print the results.

Run it from this lab's folder:

    python compare.py

It looks for up to four versions of todo.py:

    vibe/todo.py    the version you vibe-coded (DIY 1)
    spec/todo.py    the version you built from the spec (DIY 4)
    todo.py         the version the agent built (DIY 6)
    ralph/todo.py   the version the Ralph loop built (DIY 10, if you did it)

Each version is copied into a new temporary folder before its exam, so
nothing here changes your files or the tasks you have saved. The exam has
two parts:

1. The 9 tests in tests/test_todo.py.
2. The command line from SPEC.md, run as three separate commands, the way
   you would type them: add a task, add a task with the priority "urgent",
   then list the tasks. If the third command lists the first task, the
   program saved it and loaded it again.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LAB = Path(__file__).resolve().parent
TESTS = LAB / "tests" / "test_todo.py"
STUB_MARK = "Every method below is a stub"

# (the name shown in the table, the folder that holds that version's todo.py)
VERSIONS = [
    ("vibe", LAB / "vibe"),
    ("spec", LAB / "spec"),
    ("agent", LAB),
    ("ralph", LAB / "ralph"),
]


def copy_program(folder, scratch):
    """Copy a version's own .py files into the scratch folder: not its tests, not this script."""
    for path in folder.glob("*.py"):
        if path.name != "compare.py" and not path.name.startswith("test_"):
            shutil.copy(path, scratch / path.name)


def run(command, scratch, seconds):
    """Run a command in the scratch folder with no keyboard attached.

    Returns (exit code, everything the command printed). The exit code is None
    if the command was still running after the given number of seconds, which
    usually means the program was waiting for someone to type.
    """
    # A program that keeps its tasks in your home folder keeps them in the
    # scratch folder instead, so the exam never touches your real tasks.
    env = dict(os.environ, HOME=str(scratch), USERPROFILE=str(scratch))
    try:
        finished = subprocess.run(command, cwd=scratch, env=env,
                                  stdin=subprocess.DEVNULL, capture_output=True,
                                  text=True, timeout=seconds)
    except subprocess.TimeoutExpired:
        return None, ""
    return finished.returncode, finished.stdout + finished.stderr


def sit_the_tests(folder):
    """Run the 9 tests against one version. Returns (tests passed, why none passed)."""
    with tempfile.TemporaryDirectory() as name:
        scratch = Path(name)
        copy_program(folder, scratch)
        shutil.copy(TESTS, scratch / TESTS.name)
        command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TESTS.name]
        code, output = run(command, scratch, 120)
    if code is None:
        return 0, ("the tests were still running after two minutes: "
                   "the program may be waiting for someone to type")
    passed = re.search(r"(\d+) passed", output)
    if passed:
        return int(passed.group(1)), None
    if STUB_MARK in (folder / "todo.py").read_text(encoding="utf-8", errors="replace"):
        return 0, "todo.py is still the stub that does nothing"
    if "reading from stdin while output is captured" in output:
        return 0, ("the program waits for someone to type as soon as it is loaded, "
                   "so the tests could not start")
    # pytest starts each line that explains a failure or an error with "E".
    # Prefer the line that names the error, such as "ImportError: ...".
    reasons = [line[1:].strip() for line in output.splitlines() if line.startswith("E ")]
    named = [line for line in reasons if re.match(r"\w*(Error|Exception)\b", line)]
    reason = (named or reasons or output.strip().splitlines() or ["no output"])[0]
    return 0, re.sub(r" \((?:/|[A-Za-z]:\\)[^)]*\)", "", reason)  # drop the temporary path


def sit_the_command_line(folder):
    """Run the spec's commands as three separate runs: add, add "urgent", list.

    Returns two answers: does the list show the task the first run added, and
    was the priority "urgent" refused. The second is None when it could not
    be checked.
    """
    with tempfile.TemporaryDirectory() as name:
        scratch = Path(name)
        copy_program(folder, scratch)
        todo = [sys.executable, "todo.py"]
        run(todo + ["add", "Revise Java", "--priority", "high", "--due", "2026-12-01"],
            scratch, 5)
        run(todo + ["add", "Panic", "--priority", "urgent"], scratch, 5)
        _, listing = run(todo + ["list"], scratch, 5)
    keeps = "Revise Java" in listing
    # Only a program that lists its tasks can show whether "Panic" got in.
    refuses = ("Panic" not in listing) if keeps else None
    return keeps, refuses


def word(answer):
    """yes, no, or - for a check that could not be made."""
    if answer is None:
        return "-"
    return "yes" if answer else "no"


def main():
    if not TESTS.is_file():
        sys.exit("compare.py: tests/test_todo.py is missing. Run this script from the lab folder.")

    print("Giving each version the same exam...\n")
    names, why, missing = [], [], []
    rows = {
        "Tests passed (out of 9)": [],
        "Lists a task added by an earlier run": [],
        'Refuses the priority "urgent"': [],
    }
    for name, folder in VERSIONS:
        if not (folder / "todo.py").is_file():
            if name in ("vibe", "spec"):
                missing.append(f"No {name}/todo.py yet, so the {name} version was skipped.")
            continue
        passed, reason = sit_the_tests(folder)
        keeps, refuses = sit_the_command_line(folder)
        names.append(name)
        for row, value in zip(rows, (str(passed), word(keeps), word(refuses))):
            rows[row].append(value)
        if reason:
            why.append(f"  {name}: {reason}")

    print("The same exam for every version of the to-do app\n")
    width = max(len(row) for row in rows) + 4
    print((" " * width + "".join(f"{name:<9}" for name in names)).rstrip())
    for row, values in rows.items():
        print((f"{row:<{width}}" + "".join(f"{value:<9}" for value in values)).rstrip())
    if "-" in rows['Refuses the priority "urgent"']:
        print("\n- means it could not be checked, because the list did not show the first task.")
    if why:
        print("\nWhy a version passed none of the tests:")
        print("\n".join(why))
    if missing:
        print()
        print("\n".join(missing))


if __name__ == "__main__":
    main()
