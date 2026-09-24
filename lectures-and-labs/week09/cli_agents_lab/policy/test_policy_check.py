"""Tests for the policy checker's matching rules.

These use their own small policy on purpose, not team-policy.json: the lab
asks you to work out what that policy decides for yourself.
"""
import pytest

from policy_check import decide, parse_rule, split_commands

POLICY = {
    "allow": ["read", "shell(ls)", "shell(make)"],
    "deny": ["shell(make clean)"],
}


def test_rules_parse_into_kind_and_words():
    assert parse_rule("shell(make clean)") == ("shell", ["make", "clean"])
    assert parse_rule("read") == ("read", None)


def test_wildcards_and_empty_rules_are_refused():
    with pytest.raises(ValueError):
        parse_rule("shell(make:*)")
    with pytest.raises(ValueError):
        parse_rule("shell()")


def test_a_rule_covers_the_command_and_anything_after_it():
    assert decide("ls", POLICY) == "ALLOW"
    assert decide("ls -la", POLICY) == "ALLOW"


def test_a_rule_matches_whole_words_not_letters():
    # `lsof` starts with the letters "ls", but not with the word `ls`.
    assert decide("lsof -i", POLICY) == "ASK"


def test_deny_beats_allow_and_covers_what_follows():
    assert decide("make clean", POLICY) == "DENY"
    assert decide("make clean all", POLICY) == "DENY"


def test_a_different_word_in_front_escapes_a_deny():
    # The deny names `make clean`. `make -k clean` starts `make -k`, so the
    # deny misses it -- and the broad allow on `make` lets it through.
    assert decide("make -k clean", POLICY) == "ALLOW"


def test_every_part_of_a_chain_is_judged():
    assert decide("make build && make clean", POLICY) == "DENY"
    assert decide("make build | tee build.log", POLICY) == "ASK"


def test_a_separator_inside_quotes_does_not_split():
    assert split_commands('echo "a; b"') == [["echo", "a; b"]]


def test_non_shell_rules_never_decide_a_shell_command():
    # `read` is the agent's own file-reading tool. It says nothing about
    # running `cat` in a shell.
    assert decide("cat notes.txt", POLICY) == "ASK"


def test_unbalanced_quotes_are_asked_rather_than_guessed():
    assert decide('echo "oops', POLICY) == "ASK"
