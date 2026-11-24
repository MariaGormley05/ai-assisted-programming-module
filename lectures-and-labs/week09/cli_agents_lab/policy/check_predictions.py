#!/usr/bin/env python3
"""Score your predictions against the policy checker. DIY 5.

    python policy/check_predictions.py policy/team-policy.json policy/my-predictions.txt

Each line of the predictions file is the verdict you expect, ALLOW, ASK
or DENY, followed by the command:

    ALLOW git status
    DENY  git push

The script asks policy_check.py's own decide() about every command, prints
the checker's verdict, and puts an x beside each prediction it disagrees
with. Lines starting with # and blank lines are skipped, as in
commands.txt.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from policy_check import check_policy, decide  # noqa: E402

VERDICTS = ("ALLOW", "ASK", "DENY")


def read_predictions(path):
    """Yield (line number, predicted verdict or None, command) for each line."""
    with open(path, encoding="utf-8") as fh:
        for number, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) == 2 and parts[0].upper() in VERDICTS:
                yield number, parts[0].upper(), parts[1].strip()
            else:
                yield number, None, line


def main(argv):
    if len(argv) != 3:
        print("usage: python check_predictions.py POLICY.json PREDICTIONS.txt")
        return 2
    try:
        with open(argv[1], encoding="utf-8") as fh:
            policy = json.load(fh)
    except json.JSONDecodeError as err:
        print("policy error: %s is not valid JSON (line %d, column %d) -- "
              "often a comma after the last rule in a list"
              % (argv[1], err.lineno, err.colno))
        return 2
    try:
        check_policy(policy)
    except ValueError as err:
        print("policy error: %s" % err)
        return 2
    right = total = 0
    for number, predicted, command in read_predictions(argv[2]):
        actual = decide(command, policy)
        total += 1
        if predicted == actual:
            right += 1
            print("  %-5s  %s" % (actual, command))
        elif predicted is None:
            print("x %-5s  %s    <- no ALLOW, ASK or DENY at the start of line %d"
                  % (actual, command, number))
        else:
            print("x %-5s  %s    <- you said %s" % (actual, command, predicted))
    print()
    print("%d of %d predictions right." % (right, total))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
