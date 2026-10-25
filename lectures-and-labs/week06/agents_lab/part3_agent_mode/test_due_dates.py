from datetime import date
from pathlib import Path

import pytest

from cli import main


@pytest.fixture
def data_file(tmp_path: Path) -> Path:
    return tmp_path / "tasks.json"


def run(data_file: Path, *args: str, capsys: pytest.CaptureFixture[str]) -> str:
    main(["--file", str(data_file), *args])
    return capsys.readouterr().out


def test_due_date_is_persisted_and_shown(data_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert "due 2099-01-02" in run(
        data_file, "add", "Plan trip", "--due-date", "2099-01-02", capsys=capsys
    )
    assert "due 2099-01-02" in run(data_file, "list", capsys=capsys)


def test_overdue_lists_only_incomplete_overdue_tasks(
    data_file: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    run(data_file, "add", "Old task", "--due", "2000-01-01", capsys=capsys)
    run(data_file, "add", "Future task", "--due", "2099-01-01", capsys=capsys)
    run(data_file, "add", "Finished old task", "--due", "2000-01-01", capsys=capsys)
    run(data_file, "done", "3", capsys=capsys)

    output = run(data_file, "list", "--overdue", capsys=capsys)

    assert "Old task" in output
    assert "Future task" not in output
    assert "Finished old task" not in output


def test_today_lists_tasks_due_today(
    data_file: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    class FixedDate(date):
        @classmethod
        def today(cls) -> date:
            return date(2026, 10, 25)

    monkeypatch.setattr("cli.date", FixedDate)
    run(data_file, "add", "Today task", "--due", "2026-10-25", capsys=capsys)
    run(data_file, "add", "Tomorrow task", "--due", "2026-10-26", capsys=capsys)

    output = run(data_file, "list", "--today", capsys=capsys)

    assert "Today task" in output
    assert "Tomorrow task" not in output


def test_invalid_due_date_is_rejected(data_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(["--file", str(data_file), "add", "Invalid", "--due", "tomorrow"])
    assert "due date must be in YYYY-MM-DD format" in capsys.readouterr().err


def test_version_prints_1_0(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["--version"])

    assert error.value.code == 0
    assert capsys.readouterr().out == "1.0\n"
