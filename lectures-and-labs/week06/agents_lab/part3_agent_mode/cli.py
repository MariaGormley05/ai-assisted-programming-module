"""A small persistent command-line to-do list."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


DATA_FILE = Path(__file__).with_name("tasks.json")


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


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
        return [Task(int(item["id"]), str(item["title"]), bool(item["done"])) for item in data]

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
    parser.add_argument(
        "--file",
        type=Path,
        default=DATA_FILE,
        help="JSON file used to store tasks (default: tasks.json)",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="add a task")
    add.add_argument("title", help="task title")
    commands.add_parser("list", help="list tasks")

    done = commands.add_parser("done", help="mark a task complete")
    done.add_argument("id", type=int, help="task ID")

    delete = commands.add_parser("delete", help="delete a task")
    delete.add_argument("id", type=int, help="task ID")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = TodoStore(args.file)

    try:
        tasks = store.load()
        if args.command == "add":
            next_id = max((task.id for task in tasks), default=0) + 1
            task = Task(next_id, args.title)
            tasks.append(task)
            store.save(tasks)
            print(f"Added {task.id}: {task.title}")
        elif args.command == "list":
            if not tasks:
                print("No tasks.")
            else:
                for task in tasks:
                    marker = "x" if task.done else " "
                    print(f"[{marker}] {task.id}: {task.title}")
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
