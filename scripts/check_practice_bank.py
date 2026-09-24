#!/usr/bin/env python3
"""Validate the MCQ practice bank (practice/bank/*.json).

Fails (exit 1, one line per finding) if any topic file is malformed:
missing fields, wrong option counts, out-of-range answers, duplicate
ids, schedule references (banned — questions are self-contained), a
topic listed in the manifest with no question file / too few questions,
or a file whose correct answers cluster on one option index (a bank that
"always pick B" would pass is not a practice bank).

Run from the repo root:  python scripts/check_practice_bank.py
Prints nothing on success.
"""
import json
import re
import sys
from pathlib import Path

BANK = Path("practice/bank")
MIN_QUESTIONS = 25
MAX_INDEX_SHARE = 0.45   # no option index may hold more than this share of a file's answers
DIFFICULTIES = {"easy", "medium", "hard"}
TYPES = {"concept", "code"}
SCHEDULE_RE = re.compile(r"\bweek\s*\d|\blecture\b|\bthis module\b|\bMCQ\s*[123]\b", re.I)

findings: list[str] = []


def check_topic(slug: str) -> None:
    path = BANK / f"{slug}.json"
    if not path.is_file():
        findings.append(f"{slug}: bank file missing")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        findings.append(f"{slug}: invalid JSON — {e}")
        return
    qs = data.get("questions")
    if not isinstance(qs, list) or len(qs) < MIN_QUESTIONS:
        findings.append(f"{slug}: fewer than {MIN_QUESTIONS} questions")
        return
    seen = set()
    for q in qs:
        qid = q.get("id", "<no id>")
        if qid in seen:
            findings.append(f"{slug}: duplicate id {qid}")
        seen.add(qid)
        if q.get("difficulty") not in DIFFICULTIES:
            findings.append(f"{qid}: bad difficulty {q.get('difficulty')!r}")
        if q.get("type") not in TYPES:
            findings.append(f"{qid}: bad type {q.get('type')!r}")
        opts = q.get("options")
        if not isinstance(opts, list) or len(opts) != 4:
            findings.append(f"{qid}: needs exactly 4 options")
            continue
        if not isinstance(q.get("answer"), int) or not 0 <= q["answer"] <= 3:
            findings.append(f"{qid}: answer index out of range")
        if q.get("type") == "code" and not q.get("code"):
            findings.append(f"{qid}: type=code but no code")
        for field in ("question", "explanation"):
            if not q.get(field):
                findings.append(f"{qid}: missing {field}")
        blob = " ".join([q.get("question", ""), q.get("explanation", ""), *map(str, opts)])
        if SCHEDULE_RE.search(blob):
            findings.append(f"{qid}: schedule/module reference (questions must be self-contained)")
    answers = [q.get("answer") for q in qs if isinstance(q.get("answer"), int)]
    if answers:
        top = max(answers.count(i) for i in range(4))
        if top / len(answers) > MAX_INDEX_SHARE:
            findings.append(f"{slug}: {top} of {len(answers)} correct answers sit on one option "
                            f"index — rotate the options so guessing a position does not pay")


def main() -> None:
    manifest = json.loads((BANK / "manifest.json").read_text(encoding="utf-8"))
    for topic in manifest["topics"]:
        check_topic(topic["slug"])
    if findings:
        print("\n".join(findings))
        sys.exit(1)
    print(f"check_practice_bank: {len(manifest['topics'])} topics well-formed, answers spread")


if __name__ == "__main__":
    main()
