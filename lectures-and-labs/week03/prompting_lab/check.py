"""One checker for every comparison in this lab. It marks nothing and sends
nothing anywhere: it runs the code you and the assistant wrote, and prints
what happened.

    python check.py                           where you are: one line per task
    python check.py slug slug_a slug_b ...    DIY 1: each slugify on awkward titles
    python check.py receipt                   DIY 2: does calculate_total count every item?
    python check.py rates                     DIY 3: is get_rate cached, and does today's rate refresh?
    python check.py uploads                   DIY 4: can a file land outside uploads/?
    python check.py batches                   DIY 5: does batches keep the last, short batch?
    python check.py csv FILE [FILE ...]       DIY 6: does each CSV file hold the right rows?

Run it from this lab's folder.
"""
from __future__ import annotations

import csv
import datetime as dt
import importlib
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import time
import types
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")


def fresh(module_name: str) -> types.ModuleType:
    """Import a lab module from scratch, so each check sees the file as it is now."""
    for name in [n for n in sys.modules if n == module_name or n.startswith(module_name + ".")]:
        del sys.modules[name]
    return importlib.import_module(module_name)


def git_numstat(rel: str) -> str:
    """'+a -d' lines changed in one file since your last commit, or '' if git cannot say."""
    try:
        proc = subprocess.run(["git", "diff", "--numstat", "--", rel], cwd=HERE, capture_output=True,
                              text=True, check=False)
    except OSError:
        return ""
    if proc.returncode != 0:
        return ""
    out = proc.stdout.split()
    return f"+{out[0]} -{out[1]}" if len(out) >= 2 else "+0 -0"


# ------------------------------------------------------------------ DIY 1: slugify
TITLES = (
    ("Ireland's Best", "an apostrophe: dropped, or a word break?"),
    ("Ireland’s Best", "the curly apostrophe a phone types"),
    ("Tom & Jerry", "is & dropped, or spelt 'and'?"),
    ("Café au lait", "an accent: stripped, or the letter lost?"),
    ("Über Straße", "ß: 'ss', or dropped?"),
    ("C++ & C#", "symbols that carry the meaning"),
    ("2026: A Year in Review", "digits and a colon"),
    ("Hello  World", "two spaces"),
    ("  Leading and trailing  ", "spaces at the ends"),
    ("日本語のタイトル", "no Latin letters at all"),
    ("!!!", "nothing survives"),
    ("How to Write a Very Long Title That Keeps Going Well Past Sixty Characters",
     "cut short, or kept whole?"),
)


def load_file(name: str) -> types.ModuleType:
    """Import <name>.py from the folder you are in, or from this lab's folder."""
    stem = name[:-3] if name.endswith(".py") else name
    for folder in (Path.cwd(), HERE):
        path = folder / f"{stem}.py"
        if path.is_file():
            spec = importlib.util.spec_from_file_location(f"student_{stem}", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    sys.exit(f"No {stem}.py in {Path.cwd()} or in {HERE}. If the assistant saved it "
             f"somewhere else, move it into the prompting_lab folder.")


def slug_function(module: types.ModuleType):
    functions = [v for v in vars(module).values()
                 if isinstance(v, types.FunctionType) and v.__module__ == module.__name__]
    if not functions:
        sys.exit(f"{module.__name__[8:]}.py defines no function")
    for fn in functions:
        if fn.__name__ == "slugify":
            return fn
    for fn in functions:
        if "slug" in fn.__name__:
            return fn
    return functions[0]


def cells(text: str) -> int:
    """Terminal columns a string takes: CJK characters are two wide."""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def shown(value: str, width: int) -> str:
    """value cut to fit width columns, then padded to exactly width columns."""
    text = value if value else "(empty)"
    if cells(text) > width:
        while cells(text) > width - 3:
            text = text[:-1]
        text += "..."
    return text + " " * (width - cells(text))


def check_slug(names: list[str]) -> int:
    if not names:
        print("Name the files to compare:  python check.py slug slug_a slug_b")
        return 2
    fns = [slug_function(load_file(n)) for n in names]
    labels = [n[:-3] if n.endswith(".py") else n for n in names]
    width = 22
    print(shown("title", 24) + "  " + "".join(shown(label, width) + "  " for label in labels))
    splits = 0
    for title, note in TITLES:
        results = []
        for fn in fns:
            try:
                results.append(str(fn(title)))
            except Exception as exc:  # raising is a decision too
                results.append(f"ERROR:{type(exc).__name__}")
        if len(set(results)) > 1:
            splits += 1
        print(shown(title, 24) + "  " + "".join(shown(r, width) + "  " for r in results) + note)
    print()
    if len(fns) > 1:
        print(f"{splits} of {len(TITLES)} titles split them. Each split is a decision one prompt made "
              "and another left open.")
    print("Where they all agree, ask: is that what I would have chosen?")
    return 0


# ------------------------------------------------------------------ DIY 2: receipt
RECEIPT_CASES = (
    ([{"price": 10.0, "qty": 1}, {"price": 5.0, "qty": 2}], 24.6, "two items"),
    ([{"price": 2.5, "qty": 4}], 12.3, "one item"),
    ([], 0.0, "no items"),
)


def receipt_state() -> tuple[bool, list[str]]:
    receipt = fresh("lab.code.receipt")
    ok, lines = True, []
    for items, want, label in RECEIPT_CASES:
        try:
            got = receipt.calculate_total(items)
            right = abs(float(got) - want) < 0.005
        except Exception as exc:
            got, right = f"ERROR:{type(exc).__name__}", False
        ok = ok and right
        lines.append(f"  {label:<10} {'ok' if right else f'got {got}, want {want}'}")
    return ok, lines


def check_receipt() -> int:
    ok, lines = receipt_state()
    print("calculate_total, with 23% tax:")
    print("\n".join(lines))
    changed = git_numstat("lab/code/receipt.py")
    if changed:
        print(f"\nlines changed in receipt.py since your last commit: {changed}")
    print("\n" + ("Every item counted." if ok else "Still wrong: it does not count every item."))
    return 0


# ------------------------------------------------------------------ DIY 3: rates
def rates_state() -> tuple[str, list[str]]:
    """Returns (status, lines): status is 'none', 'stale', 'fresh' or 'broken'.

    Each request to the stand-in service sleeps once, so counting sleeps
    counts requests while the clock is moved on.
    """
    rates = fresh("lab.code.rates")
    real_sleep, calls = time.sleep, [0]

    def counting_sleep(seconds):
        calls[0] += 1

    time.sleep = counting_sleep
    try:
        past, today = dt.date(2026, 9, 28), dt.date(2026, 9, 30)
        lines = []

        def at(hour, minute=0):
            rates._CLOCK[0] = dt.datetime(2026, 9, 30, hour, minute)

        def asked(base, quote, day):
            before = calls[0]
            value = rates.get_rate(base, quote, day)
            return value, calls[0] - before

        def row(label, result, verdict):
            lines.append(f"  {label:<42} {result:<20} {verdict}")

        def counted(n):
            return f"{n} service call{'' if n == 1 else 's'}"

        at(9)
        answers = [asked("EUR", "USD", past) for _ in range(3)]
        n = sum(c for _, c in answers)
        cached = n == 1 and len({v for v, _ in answers}) == 1
        row("EUR/USD for a past day, asked 3 times", counted(n), "cached" if cached else "NOT cached")
        gbp, _ = asked("EUR", "GBP", past)
        apart = gbp != answers[0][0] and gbp == rates._service("EUR", "GBP", past)
        row("EUR/GBP for that day", "a different rate" if apart else "the SAME rate",
            "kept apart" if apart else "mixed up with EUR/USD")
        at(14)
        again, n = asked("EUR", "USD", past)
        row("that past day, 5 hours later", counted(n), "still cached" if n == 0 else "asked the service again")
        at(15)
        asked("EUR", "USD", today)
        at(16, 30)
        _, n = asked("EUR", "USD", today)
        row("today's rate, asked again 90 min later", counted(n),
            "asked the service again" if n else "answered from the cache")
        correct = again == answers[0][0] and apart
        if not cached:
            status = "none"
        elif not correct:
            status = "broken"
        else:
            status = "fresh" if n else "stale"
        return status, lines
    finally:
        time.sleep = real_sleep


def check_rates() -> int:
    print("rates check (a call to the stand-in service takes a second; this counts the calls)\n")
    status, lines = rates_state()
    print("\n".join(lines))
    print()
    print({"none": "No cache yet: every request goes to the service.",
           "stale": "Cached, but today's rate came from the cache 90 minutes after it was fetched.\n"
                    "If today's rate can change during the day, that answer may be out of date.\n"
                    "(If your cache does expire, check that it takes the time from now() in rates.py:\n"
                    "this lab's clock is not the real one.)",
           "fresh": "Cached, and today's rate is fetched again once it is over an hour old.",
           "broken": "Cached, but some answers are wrong."}[status])
    return 0


# ------------------------------------------------------------------ DIY 4: uploads
def uploads_state() -> tuple[bool, list[str], str]:
    """Returns (ok, lines, verdict)."""
    old_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        site = root / "site"
        site.mkdir()
        os.chdir(site)
        try:
            uploads = fresh("lab.code.uploads")
            trials = (("report.pdf", True), ("../escaped.txt", False),
                      (str(root / "absolute.txt"), False))
            ok, lines, escaped, refused_ordinary = True, [], False, False
            for name, ordinary in trials:
                before = {p for p in root.rglob("*") if p.is_file()}
                try:
                    uploads.save_upload(name, b"test")
                    error = None
                except Exception as exc:
                    error = type(exc).__name__
                new = {p for p in root.rglob("*") if p.is_file()} - before
                inside = site.resolve() / "uploads"
                outside = [p for p in new if inside not in p.resolve().parents]
                if outside:
                    result, good = "saved OUTSIDE uploads/", False
                elif new:
                    result, good = "saved inside uploads/", True
                elif error:
                    result, good = f"refused ({error})", not ordinary
                else:
                    result, good = "nothing saved", not ordinary
                ok = ok and good
                escaped = escaped or bool(outside)
                refused_ordinary = refused_ordinary or (ordinary and not good)
                note = "ok" if good else ("the flaw" if outside else "an ordinary name should be saved")
                lines.append(f"  {shown(repr(name), 36):<38}{result:<26}{note}")
            if escaped:
                verdict = "A file name chosen by a user decides where the file lands."
            elif refused_ordinary:
                verdict = "Nothing escapes, but an ordinary upload is refused too: that is not a fix."
            else:
                verdict = "Every file stays inside uploads/."
            return ok, lines, verdict
        finally:
            os.chdir(old_cwd)


def check_uploads() -> int:
    print("uploads check (each name is tried in a fresh, empty folder)\n")
    ok, lines, verdict = uploads_state()
    print("\n".join(lines))
    print("\n" + verdict)
    return 0


# ------------------------------------------------------------------ DIY 5: batches
BATCH_CASES = (
    (([1, 2, 3, 4, 5, 6], 3), [[1, 2, 3], [4, 5, 6]]),
    (([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]),
    (([1, 2], 3), [[1, 2]]),
    (([], 2), []),
)


def batches_state() -> tuple[bool, list[str]]:
    batches = fresh("lab.code.batches")
    ok, lines = True, []
    for args, want in BATCH_CASES:
        try:
            got = batches.batches(*args)
        except Exception as exc:
            got = f"ERROR:{type(exc).__name__}"
        right = got == want
        ok = ok and right
        call = f"batches({args[0]}, {args[1]})"
        lines.append(f"  {call:<30} {got!s:<28} {'ok' if right else f'want {want}'}")
    return ok, lines


def check_batches() -> int:
    ok, lines = batches_state()
    print("\n".join(lines))
    print("\n" + ("Every item kept." if ok else "Still losing items."))
    return 0


# ------------------------------------------------------------------ DIY 6: csv
def expected_rows() -> list[list[str]]:
    rows = [["name", "email", "city"]]
    for line in (HERE / "lab" / "data" / "people.txt").read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append([part.strip() for part in line.split("|")])
    return rows


def csv_state(path: Path) -> tuple[bool, list[str]]:
    want = expected_rows()
    text = path.read_text(encoding="utf-8-sig")
    problems = []
    if "```" in text:
        problems.append("it contains a ``` fence line, which a CSV reader takes as data")
    rows = [r for r in csv.reader(io.StringIO(text)) if r and not r[0].startswith("```")]
    if rows and rows[0] != want[0]:
        problems.append(f"the header is {rows[0]}, want {want[0]}")
    for i, expected in enumerate(want[1:], start=1):
        if i >= len(rows):
            problems.append(f"{expected[0]}: missing")
            continue
        got = rows[i]
        if got == expected:
            continue
        if len(got) != len(expected):
            problems.append(f"{expected[0]}: {len(got)} fields, want 3"
                            + (" (a comma in a value needs quotes around the value)" if len(got) > 3 else ""))
        else:
            problems.append(f"{expected[0]}: read as {got}")
    if len(rows) > len(want):
        problems.append(f"{len(rows) - len(want)} extra line(s): commentary, or a blank row")
    right = sum(1 for i, r in enumerate(rows[:len(want)]) if r == want[i])
    head = f"{right} of {len(want)} rows right"
    return not problems, [head] + [f"    {p}" for p in problems]


def check_csv(files: list[str]) -> int:
    if not files:
        print("Name the files to check:  python check.py csv lab/data/people_prose.csv ...")
        return 2
    for name in files:
        path = Path(name)
        if not path.is_file():
            path = HERE / name
        if not path.is_file():
            print(f"{name:<34} not found")
            continue
        ok, lines = csv_state(path)
        print(f"{name:<34} {lines[0]}")
        for line in lines[1:]:
            print(line)
    return 0


# ------------------------------------------------------------------ where you are
def pytest_line(rel: str) -> str:
    try:
        proc = subprocess.run([sys.executable, "-m", "pytest", rel, "-q", "--no-header", "-p", "no:cacheprovider"],
                              cwd=HERE, capture_output=True, text=True, check=False)
    except OSError as exc:
        return f"could not run pytest: {exc}"
    if "No module named pytest" in proc.stderr:
        return "pytest is not installed: pip install -r requirements.txt"
    lines = [ln.strip("= ").strip() for ln in proc.stdout.splitlines() if ln.strip()]
    return lines[-1] if lines else "no output from pytest"


def summary() -> int:
    print("Prompting lab: where you are (nothing is marked or sent)\n")
    slugs = sorted(p.stem for p in HERE.glob("slug_*.py"))
    print(f"  DIY 1  slugify files: {', '.join(slugs) if slugs else 'none yet'}")
    rows = [
        ("DIY 2", lambda: "calculate_total counts every item" if receipt_state()[0]
         else "calculate_total still misses an item"),
        ("DIY 3", lambda: {"none": "get_rate is not cached yet", "stale": "get_rate is cached, but today's rate goes stale",
                           "fresh": "get_rate is cached, and today's rate refreshes",
                           "broken": "get_rate is cached, but gives some wrong answers"}[rates_state()[0]]),
        ("DIY 4", lambda: {"Every": "every upload stays inside uploads/",
                           "A file": "a file name can put a file outside uploads/",
                           "Nothing": "nothing escapes, but ordinary uploads are refused too"}[
                               next(k for k in ("Every", "A file", "Nothing")
                                    if uploads_state()[2].startswith(k))]),
        ("DIY 5", lambda: "batches keeps every item" if batches_state()[0] else "batches still loses items"),
    ]
    for label, fn in rows:
        try:
            text = fn()
        except Exception as exc:
            text = f"could not run it: {type(exc).__name__}: {exc}"
        print(f"  {label}  {text}")
    csvs = sorted(str(p.relative_to(HERE)).replace(os.sep, "/") for p in (HERE / "lab" / "data").glob("*.csv"))
    print(f"  DIY 6  CSV files: {', '.join(csvs) if csvs else 'none yet'}")
    print(f"  DIY 7  test_extract_domain: {pytest_line('lab/tests/test_extract_domain.py')}")
    print(f"  DIY 8  test_orders: {pytest_line('lab/tests/test_orders.py')}")
    print("  DIY 9  happens in the chat")
    print("\nFor detail:  python check.py receipt | rates | uploads | batches | slug NAMES | csv FILES")
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        return summary()
    command, rest = argv[0], argv[1:]
    commands = {"slug": lambda: check_slug(rest), "receipt": check_receipt, "rates": check_rates,
                "uploads": check_uploads, "batches": check_batches, "csv": lambda: check_csv(rest)}
    if command not in commands:
        print(__doc__)
        return 2
    return commands[command]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
