# Scripts

## `setup_check.py`

```bash
python scripts/setup_check.py
```

Checks Python and pip, installs this lab's requirements if pytest is
missing, and confirms the lab's files are where the tasks expect them. Run
it if `python check.py` or the tests will not start.

The lab's own checker is `check.py`, in the lab folder itself: the tasks
tell you when to run it. It runs locally, changes nothing, and reports
nowhere.
