---
title: Prompting and Context Engineering
topic: prompting
type: lecture
source: authored
marp: true
theme: aiap
paginate: true
transition: fade
---

<!-- Speaker notes: ~0:01. Title while they settle.

Two halves, and the join is the point of the two hours: prompting (how
you ask) was the whole skill in 2023; context engineering (what the model
can see) is the larger half now. Part 1 states the rules; part 2 explains
the mechanism behind them and puts the room's hands on it. Do not treat
context engineering as an advanced extra — it is where most real failures
live. -->

<!-- _class: lead -->

<span class="kicker">// how you ask, and what it can see</span>

# Prompting and Context Engineering

---

<!-- Speaker notes: ~0:02. The hook: two prompts for the same task, and the
question is not which is better but WHY. Nearly everyone picks B, and they
are right for the wrong reason — they say "because it is more detailed".
The actual reason is that B makes DECISIONS the model would otherwise have
to guess: day-first or month-first, what happens on bad input, whether a
library is allowed. That distinction is the first idea of the two hours;
it is stated on the next slide and paid off at "The opening pair,
decoded". Have the room commit before revealing. -->

## Two prompts, same task

<p class="prompt bad">write a function to parse a date string</p>

<p class="prompt good">Write a Python function parse_date(s: str) -> date.
Accept "2026-08-12" and "12/08/2026" (day first). Raise ValueError on
anything else. No external libraries.</p>

* Which gets the better answer — and **why**?

---

<!-- Speaker notes: ~0:04. The idea, said once and plainly: a prompt is a
specification, and every gap in it is filled by the model from whatever
was commonest in its training data. Part 2 explains how that filling
actually happens.

The misconception to kill immediately: students think a good prompt is a
LONG prompt, and start padding. Length is not the variable. Decisions
made, and information supplied, are the variables. -->

## The one idea

<div class="callout">

A prompt is not a request. It is a **specification**. Everything you leave
unspecified, the model decides for you — silently, and from whatever was
most common in its training data.

</div>

* "Better prompt" does not mean "longer prompt"

---

<!-- Speaker notes: ~0:05. Agenda, and the shape of the two hours. Part 1
states the rules — what a prompt is mechanically, SPEC, non-goals, the
three techniques, and the turn from wording to context. Part 2 explains
the mechanism behind those rules: how a gap actually gets filled, what is
literally in the window when the model answers, why more context makes
answers worse, and why long threads go stale — then the room does it with
its own hands. Reference slide, brisk. -->

<!-- _class: dense -->

## Two hours, two halves

**Part 1 — how you ask: the rules**

- Tokens and the context window
- SPEC, constraints and non-goals; three techniques and when to use each
- The turn to **context engineering**, and the diagnostic question
- Where prompting cannot help you

**Part 2 — what it can see: the mechanism**

- How a gap gets filled, and what is actually in the window
- A failing test, diagnosed with and without its context
- Why more is not better, and why long threads go stale
- Try it now: make the silent decisions visible

---

<!-- Speaker notes: ~0:07. Tokens: the unit the model actually reads,
priced, limited and remembered. Keep this SHORT and make it earn its place
— this is not a machine-learning lecture. They need tokens only so that
context windows and cost make sense later.

The misconception: students think the model reads words, so a "short"
paste of code feels cheap. Code fragments heavily — identifiers and
punctuation shatter — so a file costs more than its word count suggests.
A tokeniser playground demo (a camelCase name splitting into four tokens)
earns its minute if the clock allows. -->

## Tokens: the unit it actually reads

* A token is a chunk of text — a word, part of a word, or punctuation

- `"Programming"` → `Pro` + `gram` + `ming` — one tokenizer's split; others
  cut differently
- Everything is priced, limited, and remembered **in tokens**

<div class="callout">

Rough rule: **one token ≈ ¾ of a word** in English. Code is denser —
identifiers and punctuation fragment heavily.

</div>

---

<!-- Speaker notes: ~0:09. The context window: short-term memory with a
hard edge. Everything inside can influence the answer; everything outside
may as well not exist. THIS is the slide that makes context engineering
make sense, so spend the time. There is no partial credit for "I told you
earlier" if earlier fell out.

Part 2 returns to this diagram and asks a sharper question: who put each
layer there, and what was left off the list. -->

## The context window

<div class="stack">
  <div class="layer top"><span>System instruction + your prompt</span><span class="rank">in</span></div>
  <div class="layer"><span>Files, errors, docs you pasted</span><span class="rank">in</span></div>
  <div class="layer"><span>The conversation so far</span><span class="rank">in</span></div>
  <div class="layer untrusted"><span>Everything else you know and it does not</span><span class="rank">invisible</span></div>
</div>

* It is short-term memory with a **hard edge**

* Inside, it can influence the answer. Outside, it does not exist

---

<!-- Speaker notes: ~0:12. SPEC: the recipe, and the thing they will
actually use every day. Four letters, one slide.

Say that any framework works and the discipline matters more than the
acronym — but pick one and stay with it, because switching frameworks is a
way of avoiding the work. The E is the letter students skip, and it is the
one part 2 shows to be the strongest steering there is: an example is a
pattern the model continues, where a description is something it
interprets. -->

## SPEC — a recipe for every prompt

| | | Example |
|---|---|---|
| **S** | Specific goal | "Parse a date string into a `date`" |
| **P** | Programming language / file | "Python 3.12, in `utils/dates.py`" |
| **E** | Example, input → output | `"2026-08-12"` → `date(2026, 8, 12)` |
| **C** | Constraints | "No external libraries. Raise on bad input" |

<span class="kicker">// other frameworks exist; the discipline matters more than the acronym</span>

---

<!-- Speaker notes: ~0:15. Back to the opening pair, now analysable: take
B through SPEC letter by letter and all four are present.

Then the payoff line: the difference is not detail, it is DECISIONS. Day
first or month first? That is a product decision, and the vague prompt
hands it to a text predictor. Part 2 shows what the predictor does with
it — fills it from a frequency. -->

## The opening pair, decoded

<p class="prompt good">Write a Python function parse_date(s: str) -> date.
Accept "2026-08-12" and "12/08/2026" (day first). Raise ValueError on
anything else. No external libraries.</p>

- **S** parse a date · **P** Python, typed signature
- **E** two formats shown · **C** raises, no dependencies

<div class="callout">

`12/08/2026` — is that August or December? The vague prompt hands that
decision to a text predictor. **That** is the difference, not the length.

</div>

---

<!-- Speaker notes: ~0:18. Constraints and non-goals. Non-goals are the
under-used half and the one that saves them most pain.

The misconception: students think an assistant that adds extra things is
being helpful, so they tolerate it. In a review, unrequested changes are
where real defects hide — they are the changes nobody was looking at. -->

## Constraints and non-goals

**Constraints** — the boundaries the answer must respect:

- `Python 3.12` · `no new dependencies` · `under 200ms` · `no eval()`

**Non-goals** — what it must *not* touch:

- ❌ no database schema changes
- ❌ no error handling yet
- ❌ do not reformat the rest of the file

<div class="callout">

Assistants **over-deliver**. Unrequested changes are where defects hide,
because they are the changes nobody was reviewing.

</div>

---

<!-- Speaker notes: ~0:21. PREDICT beat 1: what an assistant does with a
whole file and a vague instruction. Vote before revealing.

The wrong answer to expect is "it just fixes the bug". The faulty model is
that a narrow ask produces a narrow change — that the size of the request
bounds the size of the diff. In practice, given a whole file and a vague
instruction, assistants commonly reformat, rename, add type hints and add
try/except, and the one-line fix is buried in a 40-line diff nobody reads
carefully. That is the argument for non-goals, made by experience rather
than assertion. -->

## Predict: what comes back?

<p class="prompt bad">here's my file, fix the bug in calculate_total</p>

* Just the fixed function
* The fixed function, plus type hints it added
* The whole file, reformatted, with error handling added
* All of the above, in one 40-line diff

---

<!-- Speaker notes: ~0:24. The reveal — usually the last option. Then the
fix, which is one sentence of non-goal.

Land the review point: a 3-line diff gets read. A 40-line diff gets
skimmed. The size of your diff determines whether review actually
happened. -->

## Usually the biggest one

* Ask narrowly, and say what **not** to touch

<p class="prompt good">Fix only the off-by-one in calculate_total.
Change nothing else — no formatting, no type hints, no error handling.
Show me a diff, not the file.</p>

<div class="callout">

A 3-line diff gets **read**. A 40-line diff gets **skimmed**. You choose
which one you are reviewing when you write the prompt.

</div>

---

<!-- Speaker notes: ~0:27. The three advanced techniques, kept together
so the lab can drill them one at a time.

Say what each is FOR, because students collect techniques without knowing
when to reach for them. Persona = shifts attention. CoT = multi-step
correctness. Few-shot = exact output format. The predict that follows
tests exactly that: given a problem, which one? -->

## Three techniques worth knowing

| Technique | What it does | Reach for it when |
|---|---|---|
| **Persona** | Shifts what it pays attention to | You want a specific lens — security, performance |
| **Chain-of-thought** | Asks for the steps, not just the answer | Correctness depends on intermediate results |
| **Few-shot** | Shows examples instead of describing | Output **format** must be exact |

<span class="kicker">// collect techniques, but know which problem each one solves</span>

---

<!-- Speaker notes: ~0:30. PREDICT beat 2: each technique solves one kind
of failure, and a format failure is a few-shot problem. Commit before the
reveal.

The wrong answer to expect is persona ("tell it it is a data engineer")
or, more often, a longer and firmer description of the format ("no
commentary, I mean it"). The faulty model is that the techniques are
general-purpose "make it better" knobs, so any of them helps with any
problem — and that emphasis is a kind of specification. It is not: persona
changes what the model attends to, not the shape of its output;
chain-of-thought asks for reasoning, which is more text rather than a
tighter format; and a description is interpretable where an example is
exact. -->

## Predict: which technique?

You need a report as CSV — fixed header, fixed column order, no
commentary. It keeps adding a sentence of explanation above the data.

* Persona: "you are a data engineer"
* Chain-of-thought: "think step by step about the format"
* Few-shot: two complete examples of the exact output
* A longer, firmer description: "no commentary, I mean it"

---

<!-- Speaker notes: ~0:33. The reveal: few-shot, because showing is exact
and describing is interpretable. The mechanism, which part 2 returns to:
the model continues patterns in its window, and two examples ARE the
pattern — there is nothing left to interpret.

The detail that matters is that the two examples vary along the edge that
counts — here, a comma inside a value, which the second example shows
being quoted. Two near-identical examples teach nothing about edge cases.
Persona would have changed what it noticed; chain-of-thought would have
changed what it explained. Neither pins a format. -->

## Few-shot, shown

<p class="prompt good">One CSV line per bug report. Header: severity,component,summary.
"Login 500 when the password has an emoji" → high,auth,500 on emoji password
"Typo on the about page, and in the footer" → low,web,"typo on about page, footer"
Now: "Checkout total wrong when a coupon is applied twice"</p>

<p class="reply">high,checkout,coupon applied twice miscounts total</p>

* Two examples, varied along the edge that matters — here, a comma inside a value

* Persona would change what it *notices*; chain-of-thought what it
  *explains*. Neither pins a **format**

---

<!-- Speaker notes: ~0:36. The turn. Everything so far has been about
WORDING. This is where the two hours pivot, and it is the newest material.

Set it up with the honest history: models got much better at inferring
intent from sloppy requests, so the marginal value of rewording fell. What
they still cannot do is invent information they were never given. -->

## The turn: it is not mostly about wording

* Models got **much better** at inferring intent from a sloppy request

* So the value of polishing wording fell

<div class="callout">

What they still cannot do is **invent information they were never given.**

</div>

- The bottleneck moved from *how you ask* to *what it can see*

---

<!-- Speaker notes: ~0:39. The definition, and the comparison table that
makes it concrete.

Emphasise the last row — prompt engineering optimises a human talking to a
model; context engineering optimises an agent working with one. As agents
do more, the second matters more. Part 2 opens the "what does it need to
see" question up: what is literally on the list the model is handed. -->

## Context engineering

| | Prompt engineering | Context engineering |
|---|---|---|
| Question | How do I phrase this? | What does it need to see? |
| You tune | Wording, structure, examples | Files, schemas, errors, prior code |
| Fails when | The request is ambiguous | It is missing something it cannot guess |
| Optimises | Human → model | Agent → model |

---

<!-- Speaker notes: ~0:42. PREDICT beat 3 — the diagnostic, and the most
practically useful thirty seconds of the two hours.

The wrong answer to expect is "reword it again" — it is what everyone
does, and it is why people spend twenty minutes going nowhere. The faulty
model is that every failure is a phrasing failure, so the fix is always on
the keyboard. Consistent failure across rewordings is EVIDENCE, not
proof: the likeliest explanation is missing information, because no
amount of rewording adds any. Name the other explanations when a student
raises them — the request is genuinely ambiguous, or the task is beyond
the model — and the diagnostic on the next slide separates them: if you
can name the fact it lacks, supply it; if you cannot, the problem is not
context. The "bigger model" option shares the mistake — it treats a
missing input as a capacity problem. -->

## Predict: you reworded it three times and it is still wrong

What is that most likely telling you?

* The model is not good enough — try a bigger one
* Keep rewording, you will find the magic phrasing
* **It is missing something it cannot guess**
* Raise the temperature for more variety

---

<!-- Speaker notes: ~0:45. The answer and the rule. This is the sentence
to leave on the board.

Then the counter-intuitive half: MORE context is not better. A huge
irrelevant paste makes answers worse — attention gets diluted, and models
attend less reliably to the middle of very long inputs. Context
engineering is as much about exclusion as inclusion. Part 2 explains the
mechanism; here it is enough to state it. -->

## Ask the diagnostic question

<div class="callout">

*Is this wrong because I **asked** badly, or because it does not **know**
something?*

</div>

* Wording problem → rewrite the prompt

* Knowledge problem → paste the schema, the error, the failing test

- And **more is not better**: a huge irrelevant paste dilutes the relevant
  part and makes answers worse

---

<!-- Speaker notes: ~0:48. Professional practice. These four are what
separates someone using an assistant well from someone typing at it.

Tests-first is the one worth dwelling on: it converts "looks right" into
"passes", which is the same move that lets anyone stop reading generated
code line by line. If the room has met that argument already, call back to
it here. The fourth habit is part 2's whole subject — what "the real
context" is, and what it is not. -->

## Four habits worth building

- **Ask for clarifying questions first** — surfaces the assumptions it
  would otherwise make silently
- **Tests first** — specify behaviour as tests, then ask for code that
  passes them
- **Diffs, not files** — you review a change, not a rewrite
- **Give it the real context** — the file, the error, the schema, not your
  summary of them

---

<!-- Speaker notes: ~0:52. Limits, and the honest close to part 1. Be
blunt: no amount of prompting fixes these, and pretending otherwise wastes
their time.

The last bullet is the honest one — a well-prompted answer to the wrong
question is still wrong, and the assistant will never tell you that you
asked the wrong question. The first bullet is the bridge to the break
question: if wording cannot fix a missing input, what exactly does the
model have in front of it? -->

## What prompting cannot fix

- It has **no access** to anything you did not give it
- It has a **training cutoff** — recent library changes are invisible
- It cannot count reliably, and it cannot do arithmetic reliably
- It will confidently answer a question you **should not have asked**

<span class="kicker">// prompting is a steering wheel, not an engine</span>

---

<!-- Speaker notes: ~0:55. Break. Part 1 stated the rules: specify or it
decides, keep the diff small, and ask whether a failure is wording or
knowledge. Part 2 explains the mechanism behind those rules — how a gap
actually gets filled, what is literally in front of the model when it
answers, and why adding more makes it worse — and then the room does it
with its own hands. Restart ten minutes later. -->

<!-- _class: lead -->

<span class="kicker">// break</span>

## Ten minutes

Part 2 answers: when you leave a gap, *how* does it get filled — and what,
exactly, is in front of the model when it answers?

---

<!-- Speaker notes: ~1:05. Part 2 opens with the mechanism behind part 1's
first rule. A model produces text by predicting the next token given
everything in its window; where your specification is silent, the most
likely continuation wins, and "most likely" means "most common in the
training data for prompts like yours" — not "right for your users". So an
unspecified choice is not a decision at all: it is a frequency wearing the
clothes of a decision.

This is why a vague prompt's choices are always PLAUSIBLE — plausibility
is precisely what the model optimises for — and why plausible is not the
same as correct. The misconception underneath: students read a confident,
specific answer as a considered one. -->

## How a gap gets filled

<div class="flow">
  <div class="step"><span class="n">01</span>Your prompt leaves day-first or month-first unsaid</div>
  <div class="step"><span class="n">02</span>Both continuations are possible from here</div>
  <div class="step"><span class="n">03</span>The commoner pattern in the training data wins</div>
  <div class="step danger"><span class="n">04</span>It looks like a decision. It was a frequency</div>
</div>

* The model predicts the next token from **everything in the window** — and nothing else

* Where the specification is silent, "most likely" wins — and most likely means **most common**, not most correct

<div class="callout">

That is why a vague prompt's choices are always *plausible*. Plausible is
exactly what it optimises for.

</div>

---

<!-- Speaker notes: ~1:07. The mechanism behind part 1's context window:
who put each layer there. An assistant — chat, editor plug-in or agent —
is a PROGRAM that assembles a list of text and calls the model with it.
The list is the window; the model sees the list and nothing else. Some
layers are written by whoever built the assistant (the system prompt),
some by you once (standing instructions, where the assistant reads a
file), some accumulate (the conversation, every turn of it), and some are
chosen per request (what you pasted, what it went and read). Your
repository, your ticket and your intent are not on the list unless one of
those layers carried them in.

The misconception: students picture the model "looking at" their project.
There is no looking; there is a list. -->

## What is actually in the window

<div class="stack">
  <div class="layer top"><span>System prompt — written by whoever built the assistant</span><span class="rank">theirs</span></div>
  <div class="layer"><span>Standing instructions — a file it reads on every request, if you gave it one</span><span class="rank">yours, once</span></div>
  <div class="layer"><span>The conversation so far — every turn, including the dead ends</span><span class="rank">accumulates</span></div>
  <div class="layer"><span>What you pasted, and what it went and read: files, errors, test output</span><span class="rank">per request</span></div>
  <div class="layer untrusted"><span>Your repository, your ticket, your intent</span><span class="rank">not there</span></div>
</div>

* An assistant is a **program** that assembles this list and calls the
  model with it. The model sees the list — nothing else exists

---

<!-- Speaker notes: ~1:10. PREDICT beat 4: what the model can see when you
ask an editor assistant about a file you have not opened. Commit before
the reveal.

The wrong answer to expect is "the whole project — it is open in the
editor". The faulty model is that the assistant IS the editor, so anything
on disk is visible to it; in fact the assistant is a program that picks a
handful of things to put in the window, and the model sees only those —
an open project is a folder on disk, not context. "Everything you have
opened since starting" is the same mistake with memory added. "Nothing
but your question" is closer but misses that editor assistants typically
include the file you are in and may search or read others first. The
teachable answer is "whatever it put in the window — and I should find
out what that was". -->

## Predict: what does it see?

Your editor's assistant. A project of forty files. You ask about a
function in a file you have **not** opened.

* The whole project — it is open in the editor
* Everything you have opened since you started the editor
* The file you are in, plus whatever it decided to read first
* Nothing but your question

---

<!-- Speaker notes: ~1:12. The reveal, and the practical habit that comes
out of it: there is no project, only the window, so when an answer is
wrong the first question is what went in. Some assistants search or read
files before answering; that is context engineering done FOR you, and it
is still worth checking what they chose, because a plausible answer about
the wrong file looks identical to a right one.

Connects back to the diagnostic question: "does not know" now has a
concrete meaning — it was not on the list. -->

## Only what was put in the window

* The file you are in, your selection, and whatever the assistant chose to read

* "The project" is not something it can see. There is only the list

- Some assistants search or read files before answering — that is context
  engineering done **for** you
- It is still worth knowing what went in: when the answer is wrong, that is
  the first place to look

<span class="kicker">// "does not know" means: it was not on the list</span>

---

<!-- Speaker notes: ~1:14. The second worked case, different in kind from
the opening pair: that was GENERATION (write me a function), this is
DIAGNOSIS (why is this broken?). The set-up is the commonest real-world
prompt there is — an error message and the word "fix". Nothing about it
is badly worded, which is the point: the diagnostic question from part 1
should already tell the room this is a knowledge problem, because the
model has been shown a symptom and none of the code. -->

## A second case: the failing test

- The opening pair was **generation**: write me a function. This is
  **diagnosis**: why is this broken?

```text
FAILED tests/test_orders.py::test_total - KeyError: 'unit_price'
```

<p class="prompt bad">my test fails with KeyError: 'unit_price', fix it</p>

- Before the next slide: is this a wording problem, or a knowledge problem?

---

<!-- Speaker notes: ~1:16. PREDICT beat 5: what comes back when the model
has the symptom and none of the code. Commit before the reveal.

The wrong answer to expect is "it asks to see the function", or "it says
it cannot tell without the code". The faulty model is that the model knows
what it does not know — that a missing input registers as a gap. It does
not: a question with a plausible answer gets a plausible answer, because
the most likely continuation of "fix this KeyError" is a fix, not a
question. Silence in the prompt is not a signal it receives. And the fix
it reaches for — a default value — is the commonest answer to a KeyError
in general, which is the first slide of part 2 again: a frequency, not a
diagnosis. -->

## Predict: error only — what comes back?

* It asks to see the function
* A `.get()` with a default value, so the missing key stops raising
* It rewrites the test to match
* "I cannot tell without the code"

---

<!-- Speaker notes: ~1:18. The reveal: a confident, plausible fix, and
the tell that it was a guess — the failure changes shape rather than going
away. A default of 0 stops the KeyError, and the test now fails on the
arithmetic, because every item quietly contributes nothing.

Students often read "different error" as progress. It is the opposite:
the original symptom was honest, and the fix has hidden it. This is the
knowledge problem made visible — nothing in the reply is unreasonable
given what the model could see. -->

## What came back

<p class="reply">A KeyError means some items have no unit_price. Use item.get("unit_price", 0) so a missing price does not raise.</p>

* Plausible, confident, and the commonest answer to a `KeyError` in general

* Apply it, and the test still fails — **differently**:

```text
assert 0 == 10.0
```

* The failure changed shape instead of going away. That is what a guess looks like when it lands

---

<!-- Speaker notes: ~1:20. With the function, the test and the fixture
all in the window, the bug is visible at a glance: the fixture says
`price` and the function says `unit_price`, and neither is wrong on its
own. Two things to land. First, no rewording of "fix it" could have got
here — the information was not in the window, which is the whole of
context engineering in one example. Second, the real fix is a DECISION:
which name is canonical? That is a product question, and it is yours, not
the model's — so the case ends where part 1 began, at specification. The
two halves are one discipline seen from two sides. -->

<!-- _class: code-sm -->

## What it could not see

```python
def order_total(order: dict) -> float:
    return sum(item["unit_price"] * item["qty"] for item in order["items"])
```

```python
def test_total():
    order = {"items": [{"price": 2.50, "qty": 4}]}
    assert order_total(order) == 10.0
```

* The fixture says `price`; the function says `unit_price`. Neither is wrong alone

* No rewording of "fix it" could reach this: the information was not in the window

* The real fix is a **decision** — which name is canonical? That one is yours

---

<!-- Speaker notes: ~1:22. The fourth habit from part 1, made concrete:
what goes in the window for a diagnosis, and what stays out. The verbatim
rule matters mechanically — the model matches patterns, and a paraphrase
drops exactly the tokens that carried the information: the key name, the
line number, the type.

The "leave out" column is the half students skip. The rest of the file and
unrelated files are noise, which the next slide explains; and a stated
theory tends to get agreed with, so give evidence and let it form its
own. -->

## What to put in front of it

| Put in | Leave out |
|---|---|
| The error, **verbatim** — never your paraphrase of it | The rest of the file |
| The function that raised | Files that are not on the path to the error |
| The input that triggered it — the fixture, the request | Your theory of the bug: give evidence, let it form its own |
| The test, the schema, the config it depends on | The forty-minute conversation you had about it |

<span class="kicker">// showing beats summarising; the smallest complete picture beats the biggest</span>

---

<!-- Speaker notes: ~1:24. The mechanism behind part 1's "more is not
better". Everything in the window competes for the model's attention: the
four lines that decide the answer have to be found among whatever else you
pasted, and a model attends less reliably to the middle of a very long
input — so a "just in case" paste can bury the one thing that mattered.
Two consequences: context engineering is as much exclusion as inclusion,
and the cheapest improvement to a bad answer is often to take things OUT.

The misconception: students experience a big paste as diligence. It is
the opposite — it hands the model a search problem it did not need to
have. And everything in the window is priced, every turn. -->

## More is not better — why

<div class="stack">
  <div class="layer"><span>Three files pasted "just in case"</span><span class="rank">noise</span></div>
  <div class="layer"><span>Two attempts already abandoned in this conversation</span><span class="rank">noise</span></div>
  <div class="layer top"><span>The four lines that actually decide the answer</span><span class="rank">signal</span></div>
  <div class="layer"><span>A 300-line log, of which one line matters</span><span class="rank">noise</span></div>
</div>

* Everything in the window competes for attention — and the middle of a
  long input is where the signal is found least reliably

* Context engineering is as much **exclusion** as inclusion — and
  everything in there is priced, every turn

---

<!-- Speaker notes: ~1:26. The conversation is a layer of the window, and
it only grows. Every turn stays: your questions, its answers, and every
attempt you rejected. The model cannot tell which parts you have mentally
discarded — a dead end stays in view as if it were still live, and a
correction sits right beside the wrong version it corrects. That is the
mechanism behind a thread "going in circles": the window has filled with
things you no longer want it to read. When the window is full, something
has to go, and what goes is rarely your choice. Sets up the predict that
follows. -->

## The thread is context too

* Every turn stays in the window — your questions, its answers, and every
  attempt you rejected

* It cannot tell which parts you have mentally discarded. A dead end stays
  in view as if it were still live

* Correct it, and the wrong version is still there, beside the correction

- When the window is full, something has to go — and what goes is rarely
  your choice

<span class="kicker">// a long thread is a window slowly filling with things you no longer want read</span>

---

<!-- Speaker notes: ~1:28. PREDICT beat 6: what to do when a long thread
has stopped converging. Commit before the reveal.

The wrong answer to expect is "push on — it is nearly there", with
"switch to a bigger model" close behind. The faulty model is that the
thread is a workspace accumulating understanding, so leaving it throws
work away. It is the reverse: the thread is the window, and what it has
accumulated is mostly dead ends, all still steering every answer. The
understanding worth keeping — the files, the failing test, what was ruled
out — is small and cheap to restate. "Bigger model" repeats part 1's error
of treating polluted or missing information as a capacity problem; "raise
the temperature" adds randomness to a problem that is about information. -->

## Predict: the thread is going in circles

Forty minutes in, and each answer is a variation on the last one.

* Push on — it is nearly there
* Switch to a bigger model
* New conversation, carrying only the context that turned out to matter
* Raise the temperature for a fresh angle

---

<!-- Speaker notes: ~1:30. The reveal, and the prompt that does it. A
fresh window with three lines of carried context beats forty minutes of
accumulated thread, because the three lines are the whole of what the
thread actually established.

Note what the good prompt carries: the code, the test, and what was RULED
OUT — telling it the default was tried and why it failed is context too,
and it stops the fresh conversation walking straight back into the same
plausible guess. The last line asks it to name its assumption, which turns
a silent decision into a visible one. -->

## Start again, carry the good context

<p class="prompt good">New conversation. Here are order_total, its test, and the fixture it uses.
A default value was already tried and is wrong: the test then fails as 0 == 10.0.
Propose the minimal fix, and state which key name you treat as canonical.</p>

* What you carry: the code, the failing test, and what was **ruled out** —
  three lines

* What you leave behind: forty minutes of dead ends, each still steering
  every answer

- The last line makes the silent decision **visible** — it has to name the
  assumption

---

<!-- Speaker notes: ~1:32. Tests as context — where the two halves meet.
A test is three of part 1's letters at once: an example (E), a constraint
(C), and, because it is real code from your project, information the
model did not have. And it cannot be read two ways, which prose always
can. Written first, it turns "looks right" into "passes", which is the
same move that lets anyone stop reading generated code line by line.

The misconception to name: students write the test AFTER the code, so the
test encodes whatever the code already does, bugs included. The lab's
tests-first exercise exists because of this slide. -->

## The best context is executable

```python
def test_parse_date_day_first():
    assert parse_date("12/08/2026") == date(2026, 8, 12)
```

* An **example**, a **constraint**, and a piece of **information** it did
  not have — in two lines

* Prose can be read two ways. A test can only pass or fail

- Write it first, then ask for code that passes it: "looks right" becomes
  "passes"

<span class="kicker">// a test written after the code encodes whatever the code already does</span>

---

<!-- Speaker notes: ~1:34. TRY IT NOW, seven minutes, on their own laptops
with whatever assistant they have. The activity makes part 2's first
mechanism visible: a deliberately thin request, then a demand for the list
of every decision the model made unasked. The list is always long —
currency symbol, thousands separator, decimal mark, negatives, whitespace,
the return type — and every item on it was filled from a frequency until
the follow-up forced it into the open.

The misconception this dislodges: students believe a working function
means the gaps were small. Debrief on the next slide with the three kinds
of gap. -->

## Try it now: the silent decisions

<span class="kicker">// seven minutes, your own laptop, whatever assistant you have</span>

<p class="prompt">Write a Python function parse_price(s) that turns a price string such as "€1,299.50" into a number. Then list every decision you made that I did not specify.</p>

- **Notice:** the list is long — the symbol, the thousands separator, the
  decimal mark, negatives, whitespace, the return type — and every item
  was decided **silently** until you asked

- If there is time: pick one, add a single line to the prompt, and run it
  again. The code changes

---

<!-- Speaker notes: ~1:41. Debrief, and the synthesis of both halves:
three kinds of gap, three different fixes, and the diagnostic question
separates the first two. Under-specified is the try-it-now list — the fix
is a line of SPEC. Under-informed is the failing test — the fix is putting
the file in the window, and no rewording reaches it. Over-loaded is the
one nobody suspects, because it feels like diligence — the fix is taking
things out.

An assistant helping a student with a bad answer should ask which of the
three it is before suggesting anything. -->

## Three ways an answer goes wrong

| The gap | What it looks like | The fix |
|---|---|---|
| **Under-specified** | Plausible code, full of decisions you never made | Make the decision — one line of SPEC |
| **Under-informed** | Plausible answer, wrong for *your* code; rewording does not move it | Put the file, the error, the test in the window |
| **Over-loaded** | Generic, vague, or fixated on the wrong part | Take things **out** |

<div class="callout">

The diagnostic question separates the first two. The third is the one
nobody suspects, because it feels like diligence.

</div>

---

<!-- Speaker notes: ~1:43. Common mistakes on the asking side, in the
order they will hit them. The first is the commonest and the easiest to
fix: padding a prompt with adjectives instead of decisions — "write a
really good, robust, professional function" specifies nothing. The second
is the technique-collecting habit the part 1 predict tested: a technique
without a problem it solves is noise in the prompt. -->

## Common mistakes: asking

* Padding with adjectives instead of **decisions** — "robust",
  "professional" and "clean" specify nothing

* Reaching for a technique without a problem it solves — a persona for a
  format problem

- Accepting a large diff because the change you asked for is somewhere in it
- Collecting frameworks instead of picking one and using it

---

<!-- Speaker notes: ~1:44. Common mistakes on the context side. The first
two are part 1's; the last three are part 2's, and each is a mechanism
misread: paraphrasing drops the tokens that carried the information, "it
can see my project" mistakes a folder for a window, and staying in a stale
thread mistakes accumulated dead ends for accumulated understanding. -->

## Common mistakes: context

* Rewording when the real problem is missing information

* Pasting far more context than the question needs

- Paraphrasing the error instead of pasting it verbatim
- Assuming it can see the project because the project is open
- Staying in a thread full of dead ends when a fresh window with the good
  context is three lines away

---

<!-- Speaker notes: ~1:45. Summary and close. Return to the opening pair
and ask the room to explain the difference now — they should say
"decisions", not "detail", and after part 2 they should be able to say
where an unmade decision goes: it is filled from a frequency. Then the
sentence to leave on the board: is it wrong because I asked badly, or
because it does not know something? Both halves of the two hours are
answers to that one question. Leave the callout up through questions. -->

<!-- _class: dense -->

## Summary

- A prompt is a **specification**. What you leave out, it fills from a frequency, not a judgement
- **SPEC** every time; **non-goals** keep the diff small enough to review
- Persona shifts attention, chain-of-thought helps multi-step, few-shot fixes format
- **Context engineering**: it sees the window and nothing else — so check what went in
- **More is not better** — exclusion is half the job, and a stale thread is context too
- The best context is executable — a test is example, constraint and information at once

<div class="callout">

*Is it wrong because I asked badly, or because it doesn't know something?*
No amount of rewording adds information.

</div>
