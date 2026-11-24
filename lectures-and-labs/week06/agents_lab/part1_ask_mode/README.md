# Part 1: Ask (DIY 1, step by step)

The walkthrough for **DIY 1** on the [lab page](../README.md), with the
same steps in the same order.

**Ask** reads your files and answers in the chat. It cannot edit a file or
run a command that changes anything, so every change in this part is one
you make yourself. Open the chat with `Ctrl+Alt+I` (`Ctrl+Cmd+I` on a
Mac), press the `+` at the top of the panel for a fresh conversation, and
pick **Ask** in the agent picker under the chat input (the control that
first says **Agent**).

From the lab folder:

```bash
cd part1_ask_mode
```

## The steps

1. Open `mystery_code.py`. **Do not run it yet.** Its docstring suggests
   some questions; leave them for now.
2. Fresh conversation, **Ask**, with the file open:

   > Walk me through mystery_code.py line by line and tell me exactly what
   > it prints.

   Then make your own guess at the last line it prints and ask:

   > I think the total comes out at $____. Am I right?

3. Run it and see who was right:

   ```bash
   python mystery_code.py
   ```

   Then ask about a call the file never makes:

   > What would add_discount(150) do to the total?

   and check its answer by running it:

   ```bash
   python -c "from mystery_code import ShoppingCart as C; c = C(); c.add_item('Laptop', 100); c.add_discount(150); print(c.calculate_total())"
   ```

4. Open `buggy_code.py`. It reads `grades.csv` and gets the right answer
   on that file. Fresh conversation, **Ask**:

   > What input could make buggy_code.py crash, or print the wrong
   > average? List the inputs. Don't fix anything.

5. Prove two of them: a grade with a decimal point, and a negative grade.

   ```bash
   printf 'name,grade,subject\nAoife,72.5,Maths\n' > decimal.csv
   python -c "from buggy_code import load_grades; print(load_grades('decimal.csv'))"
   printf 'name,grade,subject\nAoife,72,Maths\nBen,-100,Maths\n' > negative.csv
   python -c "from buggy_code import load_grades, generate_report; print(generate_report(load_grades('negative.csv')))"
   ```

   Now fix one of the two in `buggy_code.py` **yourself**, using what the
   assistant told you (Ask cannot edit, and that is the point), and run
   the same command again.
6. **The hunt.** Ask the step 4 question in two more fresh conversations.
   Does it name the same inputs each time? Does every answer catch the
   decimal grade?

## Expected output

Step 3:

```text
=== Shopping Cart ===
Laptop: $999.99 x 1
Mouse: $29.99 x 2
Keyboard: $79.99 x 1

Subtotal: $1139.96
Discount: -$114.00
Total: $1025.96
```

and the 150% discount prints `-50.0`: nothing stops a discount over 100%,
so the shop pays you.

Step 5, before your fix, the decimal grade stops the program:

```text
ValueError: invalid literal for int() with base 10: '72.5'
```

and the negative grade goes into the average without a word:

```text
    Average Grade: -14.00
    Highest Grade: Aoife - 72
    Lowest Grade: Ben - -100
```

After your fix, the same command does what you decided it should: skip
the row, round it, or refuse it with a clear message. Which one is right
is your call, not the assistant's.

## If you finish early

- **Review, not chat.** Select all of `buggy_code.py`, right-click and
  choose **Review** (it may sit inside a **Generate Code** submenu). Its
  findings appear in the **Comments** panel and inline in the editor, not
  in the chat. Did it find the decimal grade?
- **Learn something new.** Fresh conversation, **Ask**: pick a Python idea
  you have not met, such as `async`/`await`, decorators, or `deepcopy`
  against a shallow copy, and ask for an explanation with a five-line
  example. Run the example.
