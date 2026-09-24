# Scripts

Two helpers for this lab. Both run locally and report nowhere.

## `check_progress.py`

```bash
python scripts/check_progress.py
```

Runs the lab's tests — they fail until DIY 8 replaces the placeholder test,
and that is expected — then checks each `lab/prompts/taskN.md` for the
sections its task asks for, `lab/diffs/task9.diff` for a real diff, and
`lab/REFLECTION.md` for a real reflection. It does not grade anything: the
Practical Assessment for this lab is on Moodle and asks about the work
itself.

## `setup_check.py`

```bash
python scripts/setup_check.py
```

Checks Python and pip, installs this lab's requirements if pytest is
missing, and confirms the lab folders exist. Run it if the tests will not
start.
