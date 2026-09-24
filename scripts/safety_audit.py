#!/usr/bin/env python3
"""Safety audit for this repo. Run before every push.

A DETECTION tool: false negatives (a real leak that stays silent) are the
failure mode that matters, not false positives. Every check below is a
"must come up empty" check -- exit 0 with no output when the repo is clean;
otherwise print every finding and exit non-zero.

If it flags something, FIX THE CONTENT. Never widen a detector to make a
warning go away.

Checks:
  1. tracked-file extensions -- no spreadsheet/archive/compiled-binary
     extensions, and no .pptx at all: lecture decks are Marp markdown here,
     so a tracked PowerPoint means a conversion was skipped.
  2. env files -- `.env.example` is the ONLY env file that may be tracked.
     One lab (rag) needs a live API key that students supply themselves,
     so a real .env reaching a public repo is this module's single most
     likely credential leak.
  3. credential shapes -- API keys and tokens by provider prefix, private
     key headers, and service-account JSON. This check does not exist in
     the OOC repo; it exists here because these labs genuinely handle
     secrets.
  4. text scan -- tracked text files, line by line, for leaked Moodle
     submission-path text, ATU student ID numbers, or 32-char hex tokens.
     A match is suppressed ONLY when its entire span lies within one
     known-safe span on the SAME (unmodified) line, so a real token glued
     onto a safe shape still surfaces. This file's own source contains the
     safe shapes verbatim and clears itself through that mechanism -- it is
     not exempted by name.
  5. top-level allowlist -- every tracked path lives under a documented
     top-level entry.

Usage (from repo root): python scripts/safety_audit.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Check 1: tracked-file extensions that must never be committed.
#   pptx: decks are markdown in this repo. A tracked PowerPoint is a deck
#   that never got converted, and it is opaque to every other gate.
#   mbz/zip: Moodle course backups carry student data.
BAD_EXTENSION_RE = re.compile(
    r"\.(xlsx|xls|mbz|zip|class|jar|pptx|ppt|docx|doc|pem|key|p12|pfx)$",
    re.IGNORECASE)

# ---------------------------------------------------------------------------
# Check 2: env files. .env.example ships (it documents which variables a lab
# needs); anything else matching .env* is a real environment file.
ENV_FILE_RE = re.compile(r"(^|/)\.env(\..*)?$")
ENV_ALLOWED = re.compile(r"(^|/)\.env\.example$")

# ---------------------------------------------------------------------------
# Check 3: credential shapes, by provider.
#
# Each pattern is written with a character class immediately after its
# literal prefix, which is what lets this file clear ITSELF: the regex
# source text `sk-[A-Za-z0-9...` has a `[` where the class expects an
# alphanumeric, so no pattern below matches its own definition. Do not
# "simplify" these to bare \S+ -- that breaks the property and the audit
# starts reporting its own source.
CREDENTIAL_PATTERNS = {
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    "Anthropic key": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    "Google API key": re.compile(r"\bAIza[A-Za-z0-9_-]{30,}"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}"),
    "GitHub fine-grained PAT": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitLab PAT": re.compile(r"\bglpat-[A-Za-z0-9_-]{15,}"),
    "HuggingFace token": re.compile(r"\bhf_[A-Za-z0-9]{30,}"),
    "private key header": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "service-account JSON": re.compile(r'"private_key"\s*:\s*"'),
    # An assignment with a long literal on the right-hand side. Deliberately
    # narrow: it requires a quoted value of real length, so KEY = os.environ
    # and KEY = "" (both correct) do not trip it.
    "hardcoded key assignment": re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*"
        r"[\"'][A-Za-z0-9_\-./+]{16,}[\"']"),
}

# ---------------------------------------------------------------------------
# Check 4: sensitive text patterns and the known-safe shapes checked for
# span-containment before a match is flagged.
TEXT_SCAN_GLOBS = ("*.md", "*.yml", "*.yaml", "*.py", "*.html", "*.xml",
                   "*.json", "*.txt", "*.js", "*.ts", "*.tsx", "*.jsx",
                   "*.sh", "*.toml", "*.cfg", "*.ini", "*.env.example")
SENSITIVE_RE = re.compile(r"assignsubmission|G00[0-9]{6}|\b[0-9a-f]{32}\b",
                          re.IGNORECASE)

# GitHub Classroom is RETIRED for this module: labs are distributed by
# template now. There is deliberately NO whitelist for Classroom URLs -- a
# leftover invite link in a migrated lab is exactly what this should surface,
# because it would send students to a dead assignment.
PATTERN_QUOTE = "assignsubmission|G00"
BACKTICK_QUOTE = "`assignsubmission`"
SAFE_SPAN_PATTERNS = (
    re.compile(re.escape(PATTERN_QUOTE)),
    re.compile(re.escape(BACKTICK_QUOTE)),
)
CONTEXT_RADIUS = 40  # chars of context kept either side of a match in output

# ---------------------------------------------------------------------------
# Check 5: only these top-level paths may be tracked.
TOP_LEVEL_ALLOW_RE = re.compile(
    r"^(\.github/|\.gitignore$|\.gitattributes$|README\.md$|CLAUDE\.md$"
    r"|AGENTS\.md$|docs/"
    r"|module/|scripts/|lectures-and-labs/|mcq/|themes/|\.vscode/|\.devcontainer/"
    r"|practice/|package\.json$|package-lock\.json$)")


def git_ls_files(*pathspecs: str) -> list[str]:
    """Tracked paths (repo-relative, forward slashes) matching pathspecs."""
    result = subprocess.run(["git", "ls-files", *pathspecs],
                            capture_output=True, text=True,
                            encoding="utf-8", check=True)
    return [line for line in result.stdout.splitlines() if line]


def safe_spans(line: str) -> list[tuple[int, int]]:
    """Start/end offsets of every known-safe shape occurring in line."""
    return [(m.start(), m.end())
            for pattern in SAFE_SPAN_PATTERNS
            for m in pattern.finditer(line)]


def _snippet(line: str, match: re.Match) -> str:
    start = max(0, match.start() - CONTEXT_RADIUS)
    end = min(len(line), match.end() + CONTEXT_RADIUS)
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(line) else ""
    return prefix + line[start:end].strip() + suffix


def _redact(line: str, match: re.Match) -> str:
    """Context with the matched span masked.

    A credential finding must never print the credential: CI logs are
    readable by anyone who can see the run, so echoing a live key there
    would leak it a second time and in a more durable place.
    """
    head = line[max(0, match.start() - CONTEXT_RADIUS):match.start()]
    tail = line[match.end():match.end() + CONTEXT_RADIUS]
    return f"{head.strip()}<REDACTED {len(match.group(0))} chars>{tail.strip()}"


def scan_text_for_leaks(text: str) -> list[tuple[int, str]]:
    """(line_number, context) for every real leak in text."""
    hits: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        spans = safe_spans(line)
        for match in SENSITIVE_RE.finditer(line):
            if any(s <= match.start() and match.end() <= e for s, e in spans):
                continue
            hits.append((lineno, _snippet(line, match)))
    return hits


def read_text_relaxed(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def check_bad_extensions() -> list[str]:
    return [f"{p}: disallowed tracked extension"
            for p in git_ls_files() if BAD_EXTENSION_RE.search(p)]


def check_env_files() -> list[str]:
    return [f"{p}: only .env.example may be tracked — this looks like a real "
            f"environment file"
            for p in git_ls_files()
            if ENV_FILE_RE.search(p) and not ENV_ALLOWED.search(p)]


def check_credentials() -> list[str]:
    findings = []
    for rel_path in git_ls_files():
        path = Path(rel_path)
        if not path.is_file():
            continue
        try:
            text = read_text_relaxed(path)
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for label, pattern in CREDENTIAL_PATTERNS.items():
                for match in pattern.finditer(line):
                    findings.append(
                        f"{rel_path}:{lineno}: possible {label} — "
                        f"{_redact(line, match)}")
    return findings


def check_text_scan() -> list[str]:
    findings = []
    for rel_path in git_ls_files(*TEXT_SCAN_GLOBS):
        path = Path(rel_path)
        if not path.is_file():
            continue  # tracked-but-deleted in the working tree
        for lineno, snippet in scan_text_for_leaks(read_text_relaxed(path)):
            findings.append(f"{rel_path}:{lineno}: {snippet}")
    return findings


def check_top_level_allowlist() -> list[str]:
    return [f"{p}: not under an allowed top-level path"
            for p in git_ls_files() if not TOP_LEVEL_ALLOW_RE.match(p)]


def main() -> int:
    # Windows consoles default to a legacy codepage that cannot encode every
    # character in this repo; never let a print crash the audit itself.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    findings: list[str] = []
    findings += check_bad_extensions()
    findings += check_env_files()
    findings += check_credentials()
    findings += check_text_scan()
    findings += check_top_level_allowlist()

    for line in findings:
        print(line)
    if not findings:
        print(f"safety_audit: clean ({len(git_ls_files())} tracked files)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
