#!/usr/bin/env python3
"""Decide what an agent permission policy actually allows, before an agent runs.

    python policy_check.py team-policy.json "git push --force origin main"
    python policy_check.py team-policy.json --file commands.txt

A policy is a JSON file with two lists of rules, "allow" and "deny". Rules
are written the way terminal coding agents write them:

    shell                   every shell command
    shell(git)              every command that starts with the word `git`
    shell(git push)         every command that starts with the words
                            `git push` -- `git push --force origin main` too

A rule names the WORDS A COMMAND STARTS WITH, and nothing else. There are
no wildcards, because none are needed: shell(git) already covers every git
command. Any other kind of rule ("read", "write", an MCP server's tools...)
is about a different tool, not the shell, so it never decides a shell
command.

How one command line is decided:

  1. It is split into separate commands at  |  ||  &&  ;  &
     (quoted text is respected, so a ; inside quotes does not split).
  2. Each separate command is judged on its own:
         a DENY rule matches   -> DENY    (deny always wins)
         else an ALLOW rule    -> ALLOW
         else                  -> ASK     (a person is asked first)
  3. The whole line is DENY if any part is denied, otherwise ASK if any
     part would be asked, otherwise ALLOW.

Real agents share this shape -- deny beats allow, and anything not allowed
is asked -- but they differ from each other, and between versions, in the
details of matching: a command name and subcommand in one, a text prefix
in another, the exact command unless the rule ends in a wildcard in a
third. That is the reason to test a policy before you trust one. This
checker does NOT look inside command substitution ($(...) or backticks),
and it treats every & as a separator, so a redirection such as 2>&1 is
split into two commands; a real policy has to reckon with both.
"""
import json
import re
import shlex
import sys

RULE_RE = re.compile(r"^\s*([A-Za-z_][\w-]*)\s*(?:\((.*)\))?\s*$")
SEPARATOR_CHARS = "|&;"


def parse_rule(rule):
    """'shell(git push)' -> ('shell', ['git', 'push']);  'read' -> ('read', None)."""
    if not isinstance(rule, str):
        raise ValueError("a rule is a string, not %r" % (rule,))
    match = RULE_RE.match(rule)
    if not match:
        raise ValueError("not a rule: %r" % rule)
    kind, argument = match.group(1), match.group(2)
    if argument is None:
        return kind, None
    if "*" in argument:
        raise ValueError("%r: this checker has no wildcards -- shell(git) "
                         "already covers every git command" % rule)
    words = shlex.split(argument)
    if not words:
        raise ValueError("%r is empty -- write shell for every command" % rule)
    return kind, words


def split_commands(line):
    """Split one shell line into its separate commands, each a list of words."""
    parts, current, quote = [], [], None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            current.append(ch)
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
            current.append(ch)
        elif ch in SEPARATOR_CHARS:
            # A run such as && or || is one separator, not two.
            while i + 1 < len(line) and line[i + 1] in SEPARATOR_CHARS:
                i += 1
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
        i += 1
    parts.append("".join(current))
    return [shlex.split(part) for part in parts if part.strip()]


def rule_matches(rule, words):
    """Does this rule cover this one command (given as a list of words)?"""
    kind, prefix = parse_rule(rule)
    if kind != "shell":
        return False
    if prefix is None:
        return True
    return words[:len(prefix)] == prefix


def decide_one(words, policy):
    """ALLOW, ASK or DENY for one command that has already been split out."""
    if any(rule_matches(rule, words) for rule in policy.get("deny", [])):
        return "DENY"
    if any(rule_matches(rule, words) for rule in policy.get("allow", [])):
        return "ALLOW"
    return "ASK"


def decide(line, policy):
    """ALLOW, ASK or DENY for a whole shell line."""
    try:
        commands = split_commands(line)
    except ValueError:  # unbalanced quotes: never guess, ask a person
        return "ASK"
    if not commands:
        return "ASK"
    verdicts = [decide_one(words, policy) for words in commands]
    if "DENY" in verdicts:
        return "DENY"
    if "ASK" in verdicts:
        return "ASK"
    return "ALLOW"


def check_policy(policy):
    """Raise ValueError for anything in the policy this checker cannot read."""
    if not isinstance(policy, dict):
        raise ValueError("a policy is a JSON object with allow and deny lists")
    for key in ("allow", "deny"):
        rules = policy.get(key, [])
        if not isinstance(rules, list):
            raise ValueError('"%s" must be a list of rules' % key)
        for rule in rules:
            parse_rule(rule)


def main(argv):
    if len(argv) < 3 or (argv[2] == "--file" and len(argv) < 4):
        print("usage: python policy_check.py POLICY.json \"COMMAND\"")
        print("       python policy_check.py POLICY.json --file COMMANDS.txt")
        return 2
    with open(argv[1], encoding="utf-8") as fh:
        policy = json.load(fh)
    try:
        check_policy(policy)
    except ValueError as err:
        print("policy error: %s" % err)
        return 2
    if argv[2] == "--file":
        with open(argv[3], encoding="utf-8") as fh:
            lines = [ln.rstrip("\n") for ln in fh
                     if ln.strip() and not ln.lstrip().startswith("#")]
    else:
        lines = [" ".join(argv[2:])]
    for line in lines:
        print("%-5s  %s" % (decide(line, policy), line))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
