"""A small persistent command-line to-do list."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Sequence


DATA_FILE = Path(__file__).with_name("tasks.json")


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    due_date: str | None = None


class TodoStore:
    def __init__(self, path: Path = DATA_FILE) -> None:
        self.path = path

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise RuntimeError(f"could not read {self.path}: {error}") from error
        if not isinstance(data, list):
            raise RuntimeError(f"{self.path} must contain a JSON list")
        try:
            return [
                Task(
                    int(item["id"]),
                    str(item["title"]),
                    bool(item["done"]),
                    item.get("due_date"),
                )
                for item in data
            ]
        except (AttributeError, KeyError, TypeError, ValueError) as error:
            raise RuntimeError(f"{self.path} contains an invalid task: {error}") from error

    def save(self, tasks: list[Task]) -> None:
        try:
            self.path.write_text(
                json.dumps([asdict(task) for task in tasks], indent=2) + "\n",
                encoding="utf-8",
            )
        except OSError as error:
            raise RuntimeError(f"could not save {self.path}: {error}") from error


def _task(tasks: list[Task], task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task
    raise ValueError(f"task {task_id} does not exist")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a persistent to-do list.")
    parser.add_argument("--version", action="version", version="1.0")
    parser.add_argument(
        "--file",
        type=Path,
        default=DATA_FILE,
        help="JSON file used to store tasks (default: tasks.json)",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="add a task")
    add.add_argument("title", help="task title")
    add.add_argument(
        "--due-date",
        "--due",
        dest="due_date",
        type=_parse_due_date,
        help="due date in YYYY-MM-DD format",
    )
    list_parser = commands.add_parser("list", help="list tasks")
    filters = list_parser.add_mutually_exclusive_group()
    filters.add_argument("--overdue", action="store_true", help="list incomplete overdue tasks")
    filters.add_argument("--today", action="store_true", help="list incomplete tasks due today")

    done = commands.add_parser("done", help="mark a task complete")
    done.add_argument("id", type=int, help="task ID")

    delete = commands.add_parser("delete", help="delete a task")
    delete.add_argument("id", type=int, help="task ID")
    return parser


def _parse_due_date(value: str) -> str:
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("due date must be in YYYY-MM-DD format") from error
    return value


def _format_task(task: Task) -> str:
    marker = "x" if task.done else " "
    due = f" (due {task.due_date})" if task.due_date else ""
    return f"[{marker}] {task.id}: {task.title}{due}"


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = TodoStore(args.file)

    try:
        tasks = store.load()
        if args.command == "add":
            next_id = max((task.id for task in tasks), default=0) + 1
            task = Task(next_id, args.title, due_date=args.due_date)
            tasks.append(task)
            store.save(tasks)
            due = f" (due {task.due_date})" if task.due_date else ""
            print(f"Added {task.id}: {task.title}{due}")
        elif args.command == "list":
            today = date.today()
            if args.overdue:
                tasks = [
                    task
                    for task in tasks
                    if not task.done and task.due_date and date.fromisoformat(task.due_date) < today
                ]
            elif args.today:
                tasks = [
                    task
                    for task in tasks
                    if not task.done and task.due_date == today.isoformat()
                ]

            if not tasks:
                print("No tasks.")
            else:
                for task in tasks:
                    print(_format_task(task))
        elif args.command == "done":
            task = _task(tasks, args.id)
            task.done = True
            store.save(tasks)
            print(f"Completed {task.id}: {task.title}")
        elif args.command == "delete":
            task = _task(tasks, args.id)
            tasks.remove(task)
            store.save(tasks)
            print(f"Deleted {task.id}: {task.title}")
    except (RuntimeError, ValueError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
