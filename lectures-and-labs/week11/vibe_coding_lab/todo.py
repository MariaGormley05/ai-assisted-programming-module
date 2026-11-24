"""Exam Season To-Do: the program the coding agent writes in this lab.

SPEC.md says what the program must do, and tests/test_todo.py checks it.
Every method below is a stub: it is here so that the tests can run, but it
does nothing yet. That is why all 9 tests fail before anyone works on it.
"""


class TodoList:
    """A to-do list. SPEC.md, under Technical notes, says what each method does."""

    def add(self, title, priority="medium", due=None):
        return None

    def complete(self, task_id):
        return None

    def pending(self):
        return []

    def overdue(self, today=None):
        return []

    def save(self, path):
        return None

    @classmethod
    def load(cls, path):
        return cls()


if __name__ == "__main__":
    print("The command line is not written yet. SPEC.md says what it must do.")
