import datetime as dt

import pytest

from todo import TodoList


def test_ids_start_at_1_and_go_up():
    todos = TodoList()
    assert todos.add("Revise Java") == 1
    assert todos.add("Lab report") == 2


def test_default_priority_is_medium():
    todos = TodoList()
    todos.add("Buy milk")
    assert todos.pending()[0].priority == "medium"


def test_blank_title_is_rejected():
    todos = TodoList()
    with pytest.raises(ValueError):
        todos.add("   ")
    assert todos.pending() == []


def test_unknown_priority_is_rejected():
    with pytest.raises(ValueError):
        TodoList().add("Gym", priority="urgent")


def test_done_tasks_leave_the_pending_list():
    todos = TodoList()
    first = todos.add("Revise Java")
    todos.add("Lab report")
    todos.complete(first)
    assert [t.title for t in todos.pending()] == ["Lab report"]


def test_completing_an_unknown_id_raises():
    with pytest.raises(KeyError):
        TodoList().complete(99)


def test_pending_sorted_by_priority_then_due_date():
    todos = TodoList()
    todos.add("Low job", priority="low")
    todos.add("High later", priority="high", due=dt.date(2026, 12, 10))
    todos.add("High sooner", priority="high", due=dt.date(2026, 12, 1))
    todos.add("High no date", priority="high")
    todos.add("Medium job")
    assert [t.title for t in todos.pending()] == [
        "High sooner",
        "High later",
        "High no date",
        "Medium job",
        "Low job",
    ]


def test_overdue_lists_only_late_pending_tasks():
    todos = TodoList()
    todos.add("Late", due=dt.date(2026, 11, 1))
    finished = todos.add("Late but done", due=dt.date(2026, 11, 2))
    todos.add("Not yet", due=dt.date(2026, 12, 1))
    todos.add("No date")
    todos.complete(finished)
    today = dt.date(2026, 11, 24)
    assert [t.title for t in todos.overdue(today=today)] == ["Late"]


def test_save_and_load_keep_tasks_and_ids(tmp_path):
    path = tmp_path / "tasks.json"
    todos = TodoList()
    todos.add("Revise Java", priority="high", due=dt.date(2026, 12, 1))
    done = todos.add("Lab report")
    todos.complete(done)
    todos.save(path)

    loaded = TodoList.load(path)
    assert [t.title for t in loaded.pending()] == ["Revise Java"]
    assert loaded.pending()[0].due == dt.date(2026, 12, 1)
    assert loaded.add("Next task") == 3
