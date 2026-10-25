from pathlib import Path

import pytest

from cli import main


@pytest.fixture
def data_file(tmp_path: Path) -> Path:
    return tmp_path / "tasks.json"


def run(data_file: Path, *args: str, capsys: pytest.CaptureFixture[str]) -> str:
    main(["--file", str(data_file), *args])
    return capsys.readouterr().out


def test_add_and_list_persist_between_runs(data_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert "Added 1: Buy milk" in run(data_file, "add", "Buy milk", capsys=capsys)
    assert "[ ] 1: Buy milk" in run(data_file, "list", capsys=capsys)


def test_done_is_persisted(data_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    run(data_file, "add", "Read book", capsys=capsys)
    assert "Completed 1: Read book" in run(data_file, "done", "1", capsys=capsys)
    assert "[x] 1: Read book" in run(data_file, "list", capsys=capsys)


def test_delete_is_persisted(data_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    run(data_file, "add", "Temporary task", capsys=capsys)
    assert "Deleted 1: Temporary task" in run(data_file, "delete", "1", capsys=capsys)
    assert run(data_file, "list", capsys=capsys) == "No tasks.\n"


def test_new_tasks_can_be_added_after_deletion(
    data_file: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    run(data_file, "add", "First", capsys=capsys)
    run(data_file, "delete", "1", capsys=capsys)
    assert "Added 1: Second" in run(data_file, "add", "Second", capsys=capsys)


def test_missing_task_is_reported(data_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(["--file", str(data_file), "done", "99"])
    assert "task 99 does not exist" in capsys.readouterr().err
