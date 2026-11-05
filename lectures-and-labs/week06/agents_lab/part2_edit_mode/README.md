# Part 2: Edit with inline chat (DIY 2, step by step)

The walkthrough for **DIY 2** on the [lab page](../README.md), with the
same steps in the same order.

Edit is **inline chat**: select some code, press `Ctrl+I` (`Cmd+I` on a
Mac), describe the change, and it rewrites the selection in place. You see
the change as a diff, red lines out and green lines in, and choose
**Keep** or **Undo**. The diff is the whole safety mechanism.

From the lab folder:

```bash
cd part2_edit_mode
```

## The steps

1. Run the checker. It calls `calc()` from `messy_code.py` on four lists
   and compares each answer with what the original file returned:

   ```bash
   python check_refactor.py
   ```

2. Open `messy_code.py`, select the whole file (`Ctrl+A`), press `Ctrl+I`
   and ask:

   > Refactor this for readability: better variable names, smaller
   > functions, no behaviour change. Keep the function names calc,
   > proc_data and get_stuff, because other code calls them.

3. **Read the diff before you choose Keep.** Find at least one change you
   did not ask for: a docstring, a type hint, a guard for an empty list,
   `max()` in place of a loop. Then choose **Keep** and run the checker
   again:

   ```bash
   python check_refactor.py
   ```

4. If any line says `CHANGED`, put the file back and ask again, this time
   naming what must not change:

   ```bash
   git restore messy_code.py
   ```

   > Refactor this for readability. Every result must stay exactly the
   > same for every input, including negative numbers, a list containing
   > 0 and an empty list. Keep the function names calc, proc_data and
   > get_stuff.

   Choose **Keep** and run the checker a third time.
5. Run the calculator and pick one wrong line, `5! = 24` or
   `Is 1 prime? True`:

   ```bash
   python broken_calculator.py
   ```

   Select only that function (`factorial` or `is_prime`), press `Ctrl+I`
   and ask:

   > Fix the bug in this function. Change nothing else.

   Read the diff, choose **Keep**, then run it again and count what
   changed:

   ```bash
   python broken_calculator.py
   git diff --stat broken_calculator.py
   ```

6. **The hunt.** Put the calculator back (`git restore
   broken_calculator.py`) and give the step 5 prompt twice more. Does it
   change the same lines each time?

## Expected output

Step 1:

```text
calc() on four lists, before the refactor and now:

  [10, 20, 30, 40, 50]   same
  [-5, -3]               same
  [5, 0, 3]              same
  []                     same

No behaviour change.
```

After step 3, if the refactor swapped in `max()` and `min()`:

```text
  [-5, -3]               CHANGED  before: {'avg': -4.0, 'max': 0, 'min': -5, 'sum': -8}
                                  now:    {'avg': -4.0, 'max': -3, 'min': -5, 'sum': -8}
  [5, 0, 3]              CHANGED  before: {'avg': 2.6666666666666665, 'max': 5, 'min': 3, 'sum': 8}
                                  now:    {'avg': 2.6666666666666665, 'max': 5, 'min': 0, 'sum': 8}
```

The original `calc` starts its maximum at 0 and treats 0 as "no minimum
yet", so it was wrong on negative numbers and on a list containing 0. A
tidy refactor fixes that: a bug fix, and also a behaviour change you asked
it not to make. Whether to keep the fix is your decision, not one to find
hidden in a refactor. If the checker says it cannot find `calc`, the
refactor renamed it although you asked it not to.

Step 5: your line now reads `5! = 120` or `Is 1 prime? False`, and
`git diff --stat` reports one file and a few lines, not dozens.

## If you finish early

- **Generate from nothing.** Open `validators.py`, put the cursor in it,
  press `Ctrl+I` and ask for an `EmailValidator` class with a
  `validate_email` method that checks the format with a regular
  expression. Then select the class and ask for a method that returns the
  domain of an address. Which addresses would you test it on?
- **More planted bugs.** The calculator has others that its own test
  never prints: `multiply(3, -2)` gives 0 and `power(2, -1)` gives 1. Fix
  them one at a time, one function selected each time.
