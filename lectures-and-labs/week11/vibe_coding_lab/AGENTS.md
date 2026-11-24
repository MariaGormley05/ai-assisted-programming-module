# AGENTS.md

## Project
Exam Season To-Do: a command-line to-do list. The spec is in SPEC.md. Read it before you write any code.

## Setup and tests
- Python 3.10 or newer, standard library only. Do not install any package.
- pytest is the test runner. If it is missing, install it: `python -m pip install pytest`
- Run the tests from this folder: `python -m pytest -q`

## Rules
- Never edit or delete anything in tests/. The tests are the referee.
- Put all the code in todo.py.
- Work in small steps: change a little, run the tests, repeat.
- Don't special-case the tests. The code must work for any input the spec allows.
- When every test passes, try each command in the spec's Command line section by hand.
- Finish with a short list of what you built and anything in SPEC.md you were unsure about.
