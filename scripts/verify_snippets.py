#!/usr/bin/env python3
"""Parse every fenced snippet in the decks and lab READMEs.

The sibling OOC repo compiles every ```java fence with javac, and that gate
is the single most valuable guarantee in a programming module: a lecture
cannot ship code that claims to work but doesn't.

This module has no equivalent, because its decks do not carry one language.
They carry Python, JSON, YAML and bash. But all four PARSE, even where they
cannot meaningfully run, and the errors that parsing catches are exactly the
ones that waste a room's hour:

    ```python   ast.parse            a syntax error in a worked example
    ```json     json.loads           an MCP server config that does not load
    ```yaml     yaml.safe_load       the CI/CD deck is largely workflow files
    ```bash     bash -n (no exec)    unbalanced quoting in a paste-me command

This is a WEAKER guarantee than javac and is described as such: it catches
malformed configuration and broken syntax; it cannot catch a prompt that
returns nonsense or a retrieval pipeline that ranks badly.

The contract is the same as OOC's, and the marker is the point -- a fence is
either verified, or explicitly declared unverifiable:

    <!-- no-parse -->
    ```python
    def broken(:          # deliberately wrong, shown as a counter-example
    ```

Put the marker on the line directly above the opening fence. Anything else
is checked, so nothing is silently unchecked.

Deliberately-illustrative fragments are common in this module's material, so
two shapes are tolerated without a marker rather than forcing one everywhere:

  - REPL transcripts (`>>> ...`), where the input lines are extracted and
    parsed and the output lines ignored.
  - Shell blocks whose lines start with a `$ ` prompt, which is stripped.

Ellipsis placeholders (`...`) need no special handling: `...` is a real
expression in Python and valid YAML, so a snippet eliding a body still
parses.

Run from the repo root:  python scripts/verify_snippets.py
Prints one line per failure and exits 1; a summary + exit 0 when clean.
"""
import ast
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

FENCE_RE = re.compile(r"^(\s*)```([A-Za-z0-9_+-]*)\s*$")
CLOSE_RE = re.compile(r"^\s*```\s*$")
NO_PARSE_RE = re.compile(r"<!--\s*no-parse\s*-->")

# Fence tags we check, normalised to a checker name.
LANGS = {
    "python": "python", "py": "python", "python3": "python",
    "json": "json",
    "yaml": "yaml", "yml": "yaml",
    "bash": "bash", "sh": "bash", "shell": "bash", "zsh": "bash",
}

# Scanned trees. Anything tracked outside these is prose, not teaching code.
ROOTS = ("lectures-and-labs", "mcq", "module", "practice")


def tracked_markdown() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "*.md"],
                         capture_output=True, text=True, encoding="utf-8", check=True)
    paths = []
    for rel in out.stdout.splitlines():
        if not rel:
            continue
        p = Path(rel)
        if p.parts and p.parts[0] in ROOTS and p.is_file():
            paths.append(p)
    return paths


def scan(text: str):
    """Yield (lineno, tag, code, marked) for each fenced block.

    lineno is 1-based and points at the OPENING fence, so an editor jumps to
    the fence rather than to the first line of its body.

    A `<!-- no-parse -->` marker sits on the line directly above the fence.
    Blank lines between the two are tolerated, because Markdown often needs
    one there.
    """
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = FENCE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        open_line = i + 1
        tag = m.group(2).lower()
        j = i - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        marked = j >= 0 and bool(NO_PARSE_RE.search(lines[j]))

        body = []
        i += 1
        while i < len(lines) and not CLOSE_RE.match(lines[i]):
            body.append(lines[i])
            i += 1
        i += 1
        yield open_line, tag, "\n".join(body), marked


def dedent(code: str) -> str:
    """Strip the common leading indentation a nested fence carries."""
    real = [ln for ln in code.split("\n") if ln.strip()]
    if not real:
        return code
    pad = min(len(ln) - len(ln.lstrip()) for ln in real)
    if pad == 0:
        return code
    return "\n".join(ln[pad:] if ln.strip() else ln for ln in code.split("\n"))


def strip_repl(code: str) -> str | None:
    """Extract the input lines of a `>>>` transcript, or None if not one."""
    lines = code.split("\n")
    if not any(ln.lstrip().startswith(">>>") for ln in lines):
        return None
    out = []
    for ln in lines:
        s = ln.lstrip()
        if s.startswith(">>> ") or s == ">>>":
            out.append(s[4:])
        elif s.startswith("... ") or s == "...":
            out.append(s[4:])
        # everything else is output; ignore it
    return "\n".join(out)


def strip_prompts(code: str) -> str:
    """Drop a leading `$ ` shell prompt and any `#` comment-only preamble."""
    out = []
    for ln in code.split("\n"):
        s = ln.lstrip()
        if s.startswith("$ "):
            out.append(s[2:])
        elif s == "$":
            continue
        else:
            out.append(ln)
    return "\n".join(out)


# A teaching snippet is often a FRAGMENT, not a module: the `elif` arm being
# added to an existing chain, the `except` clause under discussion, a method
# body shown on its own. OOC's javac gate retries a bare Java declaration
# wrapped in a class; this is the same idea. Each prefix is tried in turn and
# the snippet passes if any of them parses.
FRAGMENT_WRAPS = (
    ("", ""),                              # a complete module
    ("if True:\n    pass\n", ""),          # a leading elif / else arm
    ("try:\n    pass\n", ""),              # a leading except / finally clause
    ("while True:\n    pass\n", ""),       # a leading else on a loop
    ("def _fragment():\n", "    "),        # a method body: return / yield / await
    ("class _Fragment:\n", "    "),        # bare methods or attributes
)


def check_python(code: str) -> str | None:
    repl = strip_repl(code)
    if repl is not None:
        code = repl

    first_error: SyntaxError | None = None
    for prefix, indent in FRAGMENT_WRAPS:
        body = code
        if indent:
            body = "\n".join(indent + ln if ln.strip() else ln
                             for ln in code.split("\n"))
        try:
            ast.parse(prefix + body)
            return None
        except SyntaxError as e:
            if first_error is None:
                first_error = e  # report against the snippet as written

    e = first_error
    return f"python syntax: {e.msg} (snippet line {e.lineno})"


def check_json(code: str) -> str | None:
    try:
        json.loads(code)
        return None
    except json.JSONDecodeError as e:
        return f"json: {e.msg} (snippet line {e.lineno}, col {e.colno})"


def check_yaml(code: str) -> str | None:
    if yaml is None:
        return "yaml: PyYAML is not installed (pip install pyyaml)"
    try:
        list(yaml.safe_load_all(code))
        return None
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        where = f" (snippet line {mark.line + 1})" if mark else ""
        return f"yaml: {getattr(e, 'problem', e)}{where}"


BASH = shutil.which("bash")


def check_bash(code: str) -> str | None:
    """Syntax-only check. `bash -n` reads and parses but NEVER executes.

    The script goes in on stdin rather than via a temp file: under Git Bash
    on Windows a native temp path (C:\\Users\\...) reaches bash with its
    backslashes eaten and every check fails with "No such file or
    directory" -- a broken checker that looks exactly like broken content.
    """
    if not BASH:
        return None  # degrade quietly off-Linux; CI runs on ubuntu and gates
    # BYTES, not text=True. On Windows text mode translates every \n on the
    # stdin pipe into \r\n, so bash receives `then\r` and `else\r` and every
    # multi-line if/for/case block fails with "unexpected token `fi'". That
    # reads exactly like broken content and is entirely this checker's fault.
    # Encoding is explicit for the same reason: these snippets carry arrows,
    # box-drawing and smart quotes that the Windows ANSI codepage cannot map.
    r = subprocess.run([BASH, "-n"], input=strip_prompts(code).encode("utf-8"),
                       capture_output=True)
    if r.returncode != 0:
        err = r.stderr.decode("utf-8", errors="replace").strip()
        # bash names stdin "line N" already; keep its own wording.
        return f"bash syntax: {err.split(chr(10))[-1]}"
    return None


CHECKERS = {"python": check_python, "json": check_json,
            "yaml": check_yaml, "bash": check_bash}


def main() -> int:
    if yaml is None:
        print("warning: PyYAML missing — yaml fences will be reported as "
              "failures. pip install pyyaml", file=sys.stderr)
    if not BASH:
        print("warning: bash not found — bash fences are not checked on this "
              "machine; CI checks them", file=sys.stderr)
    findings, checked, skipped = [], 0, 0
    by_lang: dict[str, int] = {}

    for path in tracked_markdown():
        text = path.read_text(encoding="utf-8")
        for lineno, tag, code, marked in scan(text):
            lang = LANGS.get(tag)
            if lang is None:
                continue  # untagged, or a language we make no claim about
            if marked:
                skipped += 1
                continue
            if not code.strip():
                continue
            err = CHECKERS[lang](dedent(code))
            checked += 1
            by_lang[lang] = by_lang.get(lang, 0) + 1
            if err:
                findings.append(f"{path.as_posix()}:{lineno}: {err}")

    for line in findings:
        print(line)
    if findings:
        print(f"\n{len(findings)} snippet(s) failed to parse. Fix them, or "
              f"mark a deliberately-broken one with <!-- no-parse --> on the "
              f"line above its fence.", file=sys.stderr)
        return 1

    tally = ", ".join(f"{n} {lang}" for lang, n in sorted(by_lang.items()))
    print(f"verify_snippets: {checked} snippet(s) parsed ({tally}); "
          f"{skipped} marked no-parse")
    if not BASH:
        print("note: bash not found — bash fences were not checked locally "
              "(CI checks them)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
