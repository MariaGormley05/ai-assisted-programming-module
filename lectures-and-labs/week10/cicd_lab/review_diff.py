#!/usr/bin/env python3
"""Ask a model to review a diff for what a compiler cannot check — and fail
loudly when it could not.

    git diff origin/main...HEAD | python review_diff.py
    python review_diff.py changes.diff

The starter for DIY 3. It reads LLM_API_KEY, LLM_BASE_URL and LLM_MODEL
from the environment — the same three the RAG lab uses, with the same free
defaults — and in GitHub Actions they arrive from repository secrets. It
prints the findings to stdout, and it exits non-zero on ANY failure: no key,
no diff, an HTTP error, an empty answer. A review that could not run must go
red, not green; that is the whole point of the exercise.

Standard library only, so the job has nothing to install.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEFAULT_MODEL = "gemini-3.5-flash-lite"
MAX_DIFF_CHARS = 60_000   # past this, the diff is cut and the review says so

REVIEW_PROMPT = """You are reviewing a pull request diff. Report ONLY what a compiler or a
linter cannot check: a name that no longer matches what the code does,
a comment or docstring that has drifted from the behaviour, an edge case
the change forgot, a test whose name no longer says what it tests. Do not
comment on formatting or style, and never say whether it compiles.
Quote the line you mean. If there is nothing to report, say exactly:
No findings.

Diff:
"""


def fail(message: str) -> None:
    print(f"review_diff: {message}", file=sys.stderr)
    sys.exit(1)


def read_diff(argv: list[str]) -> str:
    if len(argv) > 1:
        path = Path(argv[1])
        if not path.is_file():
            fail(f"no such diff file: {path}")
        text = path.read_text(encoding="utf-8", errors="replace")
    else:
        text = sys.stdin.read()
    if not text.strip():
        fail("the diff is empty — nothing to review is a failure, not a pass")
    if len(text) > MAX_DIFF_CHARS:
        text = text[:MAX_DIFF_CHARS] + "\n[diff cut here: too long for one review]\n"
    return text


def review(diff: str) -> str:
    key = os.getenv("LLM_API_KEY")
    if not key:
        fail("LLM_API_KEY is not set (in Actions it comes from a repository secret, passed in as env)")
    base = os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL).rstrip("/") + "/"
    model = os.getenv("LLM_MODEL", DEFAULT_MODEL)

    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": REVIEW_PROMPT + diff}],
        "temperature": 0.2,
    }).encode("utf-8")
    request = urllib.request.Request(
        base + "chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.load(response)
    except urllib.error.HTTPError as e:
        fail(f"the model call failed: HTTP {e.code} {e.reason}")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        fail(f"the model call failed: {e}")
    except json.JSONDecodeError:
        fail("the model call returned something that is not JSON")

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        fail(f"unexpected response shape: {str(data)[:200]}")
    if not content or not content.strip():
        fail("the model returned an empty answer")
    return content.strip()


def main() -> int:
    diff = read_diff(sys.argv)
    findings = review(diff)
    print("## AI review (what a compiler cannot check)\n")
    print(findings)
    return 0


if __name__ == "__main__":
    sys.exit(main())
