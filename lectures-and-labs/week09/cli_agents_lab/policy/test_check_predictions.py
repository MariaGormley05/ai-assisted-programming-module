"""Tests for the prediction scorer (DIY 5).

Like test_policy_check.py, these use a small policy of their own, not
team-policy.json: the lab asks you to predict that one yourself.
"""
import json

from check_predictions import main, read_predictions

POLICY = {"allow": ["shell(ls)", "shell(make)"], "deny": ["shell(make clean)"]}


def test_a_line_is_a_verdict_then_the_command(tmp_path):
    predictions = tmp_path / "p.txt"
    predictions.write_text("# a comment\n\nallow ls -la\nDENY\tmake clean\nmake\n",
                           encoding="utf-8")
    assert list(read_predictions(predictions)) == [
        (3, "ALLOW", "ls -la"), (4, "DENY", "make clean"), (5, None, "make")]


def test_each_prediction_is_scored_against_the_checker(tmp_path, capsys):
    policy = tmp_path / "policy.json"
    policy.write_text(json.dumps(POLICY), encoding="utf-8")
    predictions = tmp_path / "p.txt"
    predictions.write_text("ALLOW ls\nALLOW make clean\nASK rm -rf build\n",
                           encoding="utf-8")
    assert main(["check_predictions.py", str(policy), str(predictions)]) == 0
    out = capsys.readouterr().out
    assert "  ALLOW  ls\n" in out
    assert "x DENY   make clean    <- you said ALLOW" in out
    assert "  ASK    rm -rf build\n" in out
    assert "2 of 3 predictions right." in out
