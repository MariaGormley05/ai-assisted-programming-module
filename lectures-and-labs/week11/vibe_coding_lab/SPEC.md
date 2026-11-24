# Spec: Exam Season To-Do (version 1)

## Goal
A small command-line to-do list that helps a student keep track of tasks during exams.

## Users
One student, on their own computer.

## Must have (with acceptance criteria)
1. **Add a task** with a title, a priority (low, medium or high; default medium) and an optional due date (YYYY-MM-DD).
   - Each new task gets the next id, starting at 1.
   - Ids are never reused, even after the list is saved and loaded again.
2. **Reject bad input.** A blank title, or a priority that isn't low, medium or high, gives a clear error and adds nothing.
3. **Mark a task done** by its id. An id that doesn't exist gives a clear error.
4. **List pending tasks** (not done): high first, then medium, then low. Within a priority, the earliest due date comes first and tasks with no due date come last.
5. **List overdue tasks:** pending tasks whose due date is before today.
6. **Save and load:** tasks are saved to tasks.json and loaded again when the program starts.

## Technical notes
(In GitHub Spec Kit these would go in the plan, not the spec.)
- Python 3.10 or newer, standard library only. pytest is used for the tests.
- All code goes in `todo.py`, which has a class `TodoList` with these methods:
  - `add(title, priority="medium", due=None)` returns the new task's id (an int). `due` is a `datetime.date` or None.
  - `complete(task_id)`
  - `pending()` returns a list of tasks, sorted as in point 4.
  - `overdue(today=None)` returns a list of pending tasks due before `today` (default: the real today).
  - `save(path)` and a class method `load(path)` that returns a TodoList.
- A task has the fields `id`, `title`, `priority`, `due` (a `datetime.date` or None) and `done`.
- Bad input raises `ValueError`. An unknown id raises `KeyError`.
- Command line:
  - `python todo.py add "Revise Java" --priority high --due 2026-12-01`
  - `python todo.py list`
  - `python todo.py done 3`
  - `python todo.py overdue`

## Out of scope
Accounts, a web page or GUI, reminders, editing a task's title.
