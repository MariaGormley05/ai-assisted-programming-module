---
title: Automated Checking and Evals
topic: cicd
type: lecture
source: authored
marp: true
theme: aiap
paginate: true
transition: fade
---

<!-- Speaker notes: ~0:01. Title while they settle.

Two kinds of check that are really one idea: automated checks for code
that behaves the same every time, and automated checks for code that does
not. Part 1 says what to check and in what order; part 2 says how a run
actually works and how a score is actually made. The evals material is the
part nobody teaches, and the part any app with an AI feature needs. -->

<!-- _class: lead -->

<span class="kicker">// making the machine check the machine</span>

# Automated Checking and Evals

---

<!-- Speaker notes: ~0:02. The hook. It follows directly from the argument
that you cannot read every line of generated code.

Ask it and let it sit. If review moved from your eyes to your tests, then
the tests are now load-bearing — and nobody checked whether they are any
good. Do not resolve yet. -->

## If you are not reading every line

…then something else is checking it.

* What, exactly?

* And who checks **that**?

---

<!-- Speaker notes: ~0:04. The idea. Say it once.

The misconception: students treat CI as an administrative hurdle imposed
by lecturers or employers. It is the opposite — it is the thing that makes
generating code you did not read a defensible engineering practice rather
than negligence. -->

## The one idea

<div class="callout">

Automated checks are what make it **defensible** to ship code you did not
read line by line. Without them you did not move up a level — you stopped
checking.

</div>

* CI is not administration. It is the other half of the trade

---

<!-- Speaker notes: ~0:05. Agenda. Part 1 is what to check and in what
order, ending with evals — the part most people have never met. Part 2 is
mechanism: what a run physically is, and how a score is actually made,
because those are the two things students get wrong the first time they
build either one. -->

## The two hours

**Part 1 — what to check, and in what order**

- A pipeline is a script with a trigger; what goes in it, by value
- AI inside the pipeline, and the one honesty rule
- **Evals** — a set and a rate, for things that answer differently every time
- The assertion ladder, and the judge at the top of it

**Part 2 — how it actually works**

- What a run really is, and why first runs fail
- What each rung of the ladder can and cannot catch
- A second case: output that feeds other code — then **try it now**

---

<!-- Speaker notes: ~0:07. What a pipeline is. Deliberately unglamorous —
it is a script that runs on a trigger, and that is genuinely all it is.

The only real distinction from running it yourself: it runs whether or not
you remembered. Part 2 opens up step 02 — the clean machine — because that
is where most first-run failures come from. -->

## A pipeline is a script with a trigger

<div class="flow">
  <div class="step"><span class="n">01</span>You push</div>
  <div class="step"><span class="n">02</span>A clean machine appears</div>
  <div class="step"><span class="n">03</span>It runs your checks</div>
  <div class="step"><span class="n">04</span>Pass or fail, visibly</div>
</div>

* The only real difference from running them yourself: **it runs whether
  or not you remembered**

---

<!-- Speaker notes: ~0:10. What to put in it, in value order. This is the
practical slide for anything they build.

The ordering is the teaching: linting is cheap and catches least; tests
cost most to write and catch most. Secret scanning is free and catches the
thing that ends careers. -->

## What goes in, roughly in value order

| Check | Cost to add | Catches |
|---|---|---|
| Does it build / import | Minutes | Broken merges |
| Linting and formatting | Minutes | Style drift, some bugs |
| Secret scanning | Minutes | The mistake you cannot undo |
| Dependency scanning | Minutes | Known vulnerabilities |
| Unit tests | Real effort | Actual regressions |

<span class="kicker">// the top four are nearly free; do them first</span>

---

<!-- Speaker notes: ~0:13. PREDICT beat 1; vote before revealing. Tests
whether they can rank checks by value per minute rather than by what CI
is "for".

The wrong answer to expect is "a full test suite". The faulty model is
that CI means tests, so a project without good tests gets nothing from CI.
In fact the highest value per minute is secret scanning: it costs nothing
to enable and catches the one failure that cannot be undone by fixing the
code. -->

## Predict: your project has few tests. What is worth adding first?

* Nothing — CI is pointless without a test suite
* A full test suite, before anything else
* Secret scanning and dependency checks
* A deployment step

---

<!-- Speaker notes: ~0:16. The reveal, with the asymmetry stated plainly.

A failing test costs you a red build. A leaked key costs you a rotation,
possibly a bill, possibly a breach — and pushing a fix does not un-leak
it. Irreversibility is what makes it top of the list. -->

## The checks you cannot undo by fixing the code

* A failing test → a red build. Push a fix

* A leaked key → rotate it, and hope. **Pushing a fix does not un-leak it**

<div class="callout">

Order your checks by **irreversibility**, not by sophistication.

</div>

---

<!-- Speaker notes: ~0:19. AI inside the pipeline. Short section — the
useful framing is what AI can check that a compiler cannot.

A linter finds style. A compiler finds type errors. Neither can say "this
function's name no longer matches what it does". The next slide shows the
prompt that makes the difference. -->

## AI inside the pipeline

- **Review on pull requests** — asks the questions a linter cannot
- **Issue triage** — classify, label, route
- **Documentation drift** — does the README still describe this code?

<div class="callout">

Ask it what a compiler **cannot** check. Never ask it whether the code
compiles — a compiler answers that exactly, and a model guesses.

</div>

---

<!-- Speaker notes: ~0:22. The worked example for AI in the pipeline: the
prompt is the whole design. The review job earns its place only by asking
questions nothing else can answer exactly — naming, drift, edge cases —
and by fixing the answer for "nothing", so that an empty review and a
broken review can never look the same.

The characteristic mistake is asking the model whether the code is
correct. That is the compiler's question and the tests' question, and the
model guesses at it in confident prose; the job then reports a guess as a
finding. The NONE convention is what the next slide depends on: a reply of
NONE is a result, a missing reply is a failure. -->

## What you ask it, and what you do not

<p class="prompt bad">Review this pull request and tell me whether the code is correct.</p>

* "Correct" is the compiler's question and the tests' question. A model
  **guesses** at it, in confident prose

<p class="prompt good">Here is a diff. List only: a function or variable whose name no longer matches what it does; a docstring or README line this change made false; an edge case the change does not handle. If there are none, reply NONE.</p>

- A closed list of things no compiler can check, and a fixed word for
  "nothing" — so an empty review and a broken review can never look the same

---

<!-- Speaker notes: ~0:25. The honesty rule for AI in CI, and it is
worth a slide because it is a real failure mode.

If a model call fails, that is a FAILURE. It must not be written into the
report as though it were a finding, and a run that reviewed nothing must
go red rather than filing a cheerful empty report. Otherwise green stops
meaning anything. Part 2 shows the exact mechanism by which this happens
— an exit code of zero — and how one shell operator can cause it. -->

## A failed call is a failure, not a finding

* If the model call errors, the run **failed**. It did not "find nothing"

* A job that reviewed nothing must go **red**

<div class="callout">

Otherwise you get the worst outcome available: a green tick over a check
that never ran.

</div>

---

<!-- Speaker notes: ~0:28. The turn into evals. This is where part 1
changes gear.

Set it up with the concrete problem: an app with an AI feature in it.
Every testing instinct they have assumes determinism. Same input, same
output, assertEqual. That assumption is now false. -->

## The turn: an app with an AI feature

* Same input. **Different output.** Every time

* Every testing instinct you have assumes determinism

```python
assert summarise(article) == "Revenue grew 12%."
```

* This test fails on a perfectly good answer

---

<!-- Speaker notes: ~0:31. The idea of evals. One sentence.

The shift from a test to a test SET, and from pass/fail to a rate, is the
whole concept. Everything else is technique. -->

## Evals: measure a rate, not a result

<div class="callout">

Stop asking "did this one call work?" Start asking **"across a set of
cases, how often is it acceptable — and is that number moving?"**

</div>

* One case tells you almost nothing

* Twenty cases tell you whether your change helped

---

<!-- Speaker notes: ~0:34. The assertion ladder. THE practical slide of
the evals half; it stays up while the next two slides run.

Work down it: use the strongest assertion the task allows. Most teams jump
straight to LLM-as-judge when a structural check would have been exact,
cheap and deterministic. Part 2 returns to this table and says what each
rung physically compares, and therefore what it is blind to. -->

## The assertion ladder

| Rung | Check | Use when |
|---|---|---|
| **Exact match** | `output == expected` | Classification, extraction |
| **Contains / regex** | Key fact present | The answer must mention something |
| **Structural** | Valid JSON, required fields | The output feeds other code |
| **Property** | Length, no leaked prompt, cites a source | Always worth adding |
| **LLM-as-judge** | Another model scores it | Nothing above can express it |

* Use the **strongest rung the task allows**, not the fanciest

---

<!-- Speaker notes: ~0:37. PREDICT beat 2; vote before revealing. Tests
whether they reach for the cheapest exact check or the most impressive
one.

The wrong answer to expect is "LLM-as-judge, because summaries are
subjective". The faulty model is that subjective output requires
subjective checking. Several exact, deterministic properties are available
here — mentions the figure, does not exceed a length, is not empty, does
not echo the prompt — and each is cheap and reliable. Judge is a last
resort, not a first. -->

## Predict: how do you test a summariser?

Your feature summarises articles. Which do you build first?

* LLM-as-judge — summaries are subjective
* Exact match against a reference summary
* Property checks: mentions the key figure, under 50 words, non-empty
* You cannot test it; ship and see

---

<!-- Speaker notes: ~0:40. The reveal. Property checks first — cheap,
deterministic, and they catch the failures that actually happen (empty
output, prompt echo, runaway length).

Then the honest note: judge is for the residue, the part properties cannot
express. -->

## Properties first, judge last

* Property checks are **cheap, deterministic and repeatable**

* They catch the failures that actually happen: empty output, prompt echo,
  runaway length, missing the key fact

- Keep the judge for the residue that no property can express

---

<!-- Speaker notes: ~0:43. LLM-as-judge and its failure modes. Be honest
— it is genuinely useful and genuinely biased.

Self-preference is the one to name: a model scoring output from the same
family tends to rate it higher. Position bias too: in an A/B comparison,
order affects the verdict. Both are measurable, both are real. -->

## LLM-as-judge, honestly

* Give a model the output and a rubric; ask for a score and a reason

* It works. It is also **biased in known ways**:

| Bias | What happens |
|---|---|
| Self-preference | Rates output from its own family higher |
| Position | In an A/B comparison, order changes the verdict |
| Verbosity | Longer answers score better than they deserve |

- Always ask for the **reason**, not just the score — an unjustifiable
  score is usually visibly unjustifiable

---

<!-- Speaker notes: ~0:46. PREDICT beat 3, and the one that most changes
how they work on anything with an AI feature.

The wrong answer to expect is "it got better — I improved the prompt and
the examples I checked all improved". The faulty model is that improvement
on the cases you looked at is improvement on the feature. That is exactly
the trap: people tune against the two or three cases they happen to look
at, and regress the ones they do not. Without a set measured before and
after, "better" is a feeling. -->

## Predict: you tweak the prompt and your three test cases improve

Is the feature better?

* Yes — the evidence is right there
* Unknown, until you measure the whole set
* Only if the model version stayed the same
* Yes, if the three cases were representative

---

<!-- Speaker notes: ~0:49. The reveal, and the regression point that
makes evals worth the effort at all.

This is the entire argument: without a measured set, prompt tuning is
folklore. With one, it is engineering. Say that. -->

## Unknown — and this is the whole point

* You improved the cases you were looking at

* You have no idea what happened to the ones you were not

<div class="callout">

Without a measured set, prompt tuning is **folklore**. With one, it is
engineering.

</div>

- Run the set on every change. Track the number over time

---

<!-- Speaker notes: ~0:52. Practical shape for a real app. Keep it
small and achievable — 20 cases in a JSON file is a real eval suite and
takes an afternoon.

Discourage the instinct to build a framework. Part 2 shows what each of
these four boxes physically contains. -->

## What this looks like for a project

<div class="flow">
  <div class="step"><span class="n">01</span>20 real inputs in a file</div>
  <div class="step"><span class="n">02</span>Expected properties per case</div>
  <div class="step"><span class="n">03</span>A script that scores the set</div>
  <div class="step"><span class="n">04</span>Run it in CI, record the rate</div>
</div>

* Twenty cases in a JSON file is a **real** eval suite

* Do not build a framework. Build the file

---

<!-- Speaker notes: ~0:55. Break. Part 1 named the things: a pipeline, a
set, a rate, a ladder. Part 2 opens each one up — what a run physically is
and why that explains the first red X, and how a check actually scores an
answer that is never the same twice. The try-it-now in part 2 needs
laptops open and whatever assistant they already use; no key is needed. -->

<!-- _class: lead -->

<span class="kicker">// part 1 named the things. part 2 opens them up</span>

## Ten minutes

Part 2 answers two questions: what actually happens when a run starts, and
how you score an answer that is never the same twice.

---

<!-- Speaker notes: ~1:05. The mechanism part 1 only named. A workflow run
is a fresh machine that does exactly the steps listed, in order, and
decides pass or fail by the exit code of each step. Those four facts —
trigger, empty machine, listed steps, exit code — explain nearly every
first-run failure students meet.

The misconception is that the runner is a copy of their laptop: it has
their packages, their files, their environment, their working folder. It
has none of them, and it does not even have their code until a step
fetches it. That emptiness is why a green run means something: the machine
can only pass on what is actually committed and actually listed. -->

## What actually happens when you push

<div class="flow">
  <div class="step"><span class="n">01</span>The trigger matches: a push, a pull request, a schedule</div>
  <div class="step"><span class="n">02</span>A fresh machine starts — empty</div>
  <div class="step"><span class="n">03</span>Your steps run in order, each one a shell command</div>
  <div class="step"><span class="n">04</span>Each step's exit code: 0 is green, anything else is red</div>
</div>

* The machine is **not your laptop**. No packages, no files, no keys — not
  even your code until a step fetches it

* A step that exits non-zero fails the job, and the steps after it do not run

* That emptiness is the point: the run can only pass on what is actually
  **committed**

---

<!-- Speaker notes: ~1:07. The four facts as a file. Every line maps onto
the previous slide: the trigger, the machine, a checkout step that is a
step like any other, an install step because the machine has nothing, and
a test command whose exit code is the verdict.

The concept: there is no magic in here. `uses` runs a step somebody else
published; `run` is one shell line. The mistake to expect is treating the
checkout line as ceremony that can be trimmed — it is the only reason the
code is on the machine at all. And the run starts in the repository root,
not in the folder the tests live in, which is the commonest reason a
correct test command finds nothing. -->

## The smallest real workflow

```yaml
name: ci
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4        # 01: fetch the code
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt   # 02: it has nothing
      - run: python -m pytest            # 03: the exit code decides
```

<span class="kicker">// it starts in the repository root, not in your folder</span>

---

<!-- Speaker notes: ~1:09. Each symptom is one of the four facts being
unknown, which is the point of teaching the mechanism: a student who knows
the machine is empty can read the log instead of re-running it and hoping.

The misconception is reading the first red X as "my code is broken".
Almost always the code is fine and the workflow described a machine that
does not exist — a package that was on the laptop, a folder the run did
not start in, a key that was in a local .env file. Fixing the workflow
rather than the code is not a failure; finding that difference is what the
first run is for. The last row is the dangerous one and gets the next two
slides. -->

## Why first runs fail

| The log says | What actually happened |
|---|---|
| `No module named …` | Fresh machine. Installed on your laptop is not installed here |
| `No such file or directory` | No checkout step — or the run started in the repository root, not your folder |
| The model call fails: no key | Nothing from your `.env` is there. A secret reaches the run only if the workflow hands it in |
| Red on the first push, green on the second | You fixed the **workflow**, not the code. That is what the first run is for |
| Green, but it ran nothing | The step exited 0 anyway. Next slide |

---

<!-- Speaker notes: ~1:11. PREDICT beat 4; commit before revealing. Tests
the exit-code mechanism: a step's verdict is the exit status of the last
command it ran, `||` runs its right-hand side exactly when the left side
fails, and `echo` always succeeds. So this step is green on every possible
outcome.

The wrong answer to expect is "the review ran and found nothing".
The faulty model is that green means the check passed — that a tick is
a verdict about the code. Green means only that the last command exited 0,
and this line was written, probably by someone tidying a noisy log, to
make that happen no matter what. It is the part-1 rule — a failed call is
a failure, not a finding — reduced to one shell operator. -->

## Predict: this step is green. What did it prove?

```yaml
- name: AI review
  run: python review.py || echo "review step finished"
```

* The review ran and found nothing
* The review ran; we do not know what it found
* Nothing — it is green whether the review ran, failed, or was never installed
* That `review.py` exists

---

<!-- Speaker notes: ~1:13. The reveal. Green means every step exited 0 and
nothing more. The `||` swallows the failure in shell; the same swallow in
Python is a bare except that turns the error into text and exits 0; and a
job skipped by a condition is not red either. All three leave a tick over
a check that never ran.

The teaching point is the discipline that follows from the mechanism: make
it fail on purpose once. A pipeline that has never been seen red is one
nobody has evidence works — the lab's first exercise ends on exactly that
step, and its review exercise ends on breaking the key to watch the job go
red. -->

<!-- _class: code-sm -->

## Green means "every step exited 0". Nothing more

* `||` runs its right-hand side only when the left fails — and `echo`
  always succeeds. The same swallow in Python:

```python
try:
    findings = review(diff)
except Exception:
    findings = "no findings"   # the error just became a verdict
print(findings)                # ...and the step exits 0
```

* A job **skipped** by a condition is not red either. Skipped and passed
  look the same from a distance

<div class="callout">

Make it go **red on purpose** once. A pipeline you have never seen fail is
one you have no evidence works.

</div>

---

<!-- Speaker notes: ~1:15. The second mechanism: what "scoring the set"
physically is. For each case, call the feature once, apply every check to
that one output, record pass or fail with a reason, and divide at the end.

Two things students miss. First, one output is a sample of the feature's
behaviour, not its answer: the same case can pass now and fail on the next
run, and that variability is the thing being measured, not noise to
eliminate. Second, with twenty cases one case is five points of the rate,
so a small move on a single run is not yet a regression — the same case
failing on every run is. The reason string is what makes the number
readable; a bare count cannot say which check failed or why. -->

## How an eval run scores one answer

<div class="flow">
  <div class="step"><span class="n">01</span>Take a case: an input, and what must be true of the output</div>
  <div class="step"><span class="n">02</span>Call the feature once. That is one sample of its behaviour</div>
  <div class="step"><span class="n">03</span>Apply every check. Record pass or fail — and the reason</div>
  <div class="step"><span class="n">04</span>Repeat over the set. Rate = passes ÷ cases</div>
</div>

* One output is a **sample**, not the answer. The same case can pass now
  and fail next run — that variability is what you are measuring

* Twenty cases: one case is **five points**. A small move on one run is not
  yet a regression; the same case failing every run is

* The reason string is what you read when the number moves

---

<!-- Speaker notes: ~1:17. The ladder from part 1, opened up: what each
rung physically compares, and therefore what it is blind to. Everything
below the judge compares shape — the presence of a token, whether a parser
accepts the text, a length — and is exact about shape and silent about
meaning. Only the judge reads meaning, and it pays for that by being a
biased, non-deterministic instrument whose verdict is itself a sample.

The misconception this slide exists to break: that a passing property
check is evidence the answer is right. It is evidence the answer has the
right shape. The next predict makes the room feel the gap. -->

<!-- _class: dense -->

## What each rung can and cannot catch

| Rung | Catches | Blind to |
|---|---|---|
| **Exact match** | Any deviation at all | Nothing — but rejects every good paraphrase too |
| **Contains / regex** | The key fact missing | The key fact present with its meaning reversed |
| **Structural** | Output that will not parse, missing fields | Wrong values in the right shape |
| **Property** | Empty, too long, echoed prompt | Whether any of it is true |
| **Model-as-judge** | Meaning, faithfulness, tone | Its own bias — its verdict is a sample too |

<span class="kicker">// below the judge, every rung is exact about shape and silent about meaning</span>

---

<!-- Speaker notes: ~1:19. PREDICT beat 5; commit before revealing. Tests
whether they have absorbed that the lower rungs check shape. The article
says revenue rose; the summary says it fell; every property on the list
passes.

The wrong answer to expect is "the mentions-12% check catches it".
The faulty model is that checking for the presence of the key fact is
checking the fact — presence is not meaning, and a regex that finds "12%" is fully
satisfied by a sentence that reverses it. A second wrong answer is "exact
match is the only fix": true that it would have caught this, and useless,
because exact match also fails every correct paraphrase, so it cannot tell
a good answer from this one. The right answer is that nothing on the list
catches it; this is the residue the judge exists for, or a targeted
property if the domain allows one. -->

## Predict: which check catches this?

The article says revenue **rose** 12%. The feature returns:

<p class="reply">Revenue fell 12% this quarter, driven by renewals.</p>

Your checks: non-empty · under 50 words · mentions "12%" · does not echo
the prompt.

* The length check
* The "mentions 12%" check
* None of them — all four pass
* Exact match is the only fix

---

<!-- Speaker notes: ~1:21. The reveal: presence is not meaning. A reversed
claim has perfect shape, so every rung below the judge passes it. The two
honest responses are a targeted property where the domain allows one — a
direction word that contradicts the source — or a judge that is given the
source and asked one narrow question: is every claim in the summary
supported by the article?

The detail that matters most in practice: give the judge the source. A
judge shown only the summary cannot check faithfulness; it can only rate
how the sentence reads, and a wrong summary reads perfectly well. -->

## Presence is not meaning

* Every rung below the judge checks **shape**: is the token there, does it
  parse, how long is it

* A reversed claim has perfect shape. This is the residue the judge exists for

* Two honest options: a **targeted property** if the domain allows one — a
  direction word that contradicts the source — or a **judge** given the
  article and one question: *is every claim in the summary supported by it?*

<div class="callout">

Give the judge the **source**. Shown only the summary, it cannot check
faithfulness — it can only rate how the sentence reads, and a wrong summary
reads perfectly well.

</div>

---

<!-- Speaker notes: ~1:23. TRY IT NOW, five to eight minutes, on their own
laptops with whatever assistant they already use; no key, no repository.
The concept is felt rather than told: the same prompt yields different
sentences, an equality assertion would have failed on a correct answer,
and the properties the three outputs share are the first entries in a case
file.

What to expect and how to read it. Most students get three different
sentences. Some get one that dropped the 40% or turned "a third" into a
number — that is the case that goes first in their file, and it is the
reversed-figure failure from the previous predict arriving unprompted. A
student who gets three identical sentences has not found a counter-example:
nothing promised that, the fourth run may differ, and the test still
asserts something that was never guaranteed. The weak property to expect
is "contains the word bookings" — true of a wrong summary too; push them
towards the figure and the direction. -->

## Try it now: three runs, one figure

Type this at whatever assistant you have. Then open a **new conversation**
and type it again. Three runs in total.

<p class="prompt">Summarise this in one sentence: "The library moved study-room bookings online in March. Bookings rose 40% in the first month, mostly for evening slots, and no-shows fell by a third once reminders were added."</p>

- **Notice:** the three sentences differ. A test of `==` would have failed
  a correct answer on at least one run
- Write down **three properties** all three share that a wrong summary
  would fail. Did any run drop a figure — or change one?

---

<!-- Speaker notes: ~1:30. The second worked case, different in kind from
the summariser. A support inbox: the feature reads a message and returns
fields that a ticketing system will consume. The output feeds other code,
so the first thing that matters is whether it parses at all — and because
some fields are labels, exact match is genuinely available here.

The concept: "strongest rung the task allows" is a property of the task,
not of the model. The summariser topped out at properties; this feature
reaches exact match on one field and structural checks on the whole, and
the eval is stronger for it. Students tend to carry one pattern between
tasks — either "everything needs a judge" or "everything is properties" —
and this case shows the ladder has to be re-climbed per feature. -->

## A second case: output that feeds other code

A support inbox. The feature reads a customer message and returns fields
for the ticketing system:

```json
{"product": "kettle", "issue": "stopped heating", "priority": "high"}
```

* Different in kind from the summariser: some fields have **one right answer**

* `priority` is a label from a fixed list → **exact match**. `product` must
  come from the message → a **property**. The whole thing must parse →
  **structural**

* Strongest rung the task allows — and this task allows higher rungs than a
  summary ever could

---

<!-- Speaker notes: ~1:32. What a case physically is: an input and the
things that must be true of the output. Not the output itself — a case
that stores the expected output is an exact-match test in disguise and
fails on every acceptable variant. `keys` and `priority` are checked
exactly; `product_in_input` is a property, because the right product can
be phrased several ways but must not be invented.

The misconception: that writing cases needs tooling. It needs a text file
and a decision about what "acceptable" means, and that decision is the
whole skill. -->

<!-- _class: code-sm -->

## One case in the file

```json
{
  "id": "ticket-07",
  "input": "My kettle stopped heating after two days. I need a replacement before Friday.",
  "expect": {
    "keys": ["product", "issue", "priority"],
    "priority": "high",
    "product_in_input": true
  }
}
```

* Each case says what must be **true** of the output, not what the output
  must **be**

* Twenty of these is an afternoon. It is also a real eval suite

---

<!-- Speaker notes: ~1:34. The scoring function, and the ladder is the
order of the code: parse first, then required fields, then the exact label,
then the property. Cheap exact checks run first so that the reason string
names the earliest thing that went wrong — "not JSON" is a different
problem from "wrong priority" and needs a different fix.

Worth noticing what is not here: no framework, no judge. Every line is
deterministic, so the only source of variation in the rate is the feature
itself, which is what you want to measure. -->

<!-- _class: code-sm -->

## Scoring it: three rungs in a dozen lines

```python
def score(case, output):
    try:
        data = json.loads(output)                         # structural
    except json.JSONDecodeError:
        return False, "not JSON"
    for key in case["expect"]["keys"]:                    # structural
        if key not in data:
            return False, f"missing field: {key}"
    if data["priority"] != case["expect"]["priority"]:    # exact
        return False, f"priority was {data['priority']}"
    if data["product"].lower() not in case["input"].lower():   # property
        return False, "product not in the message"
    return True, ""
```

* Checks run in **ladder order**, so the reason names the earliest thing
  that went wrong. Every line is deterministic: the only thing that varies
  is the feature

---

<!-- Speaker notes: ~1:36. The run, and the finding that surprises the
room: the commonest failure was not a wrong answer but a right answer
wrapped in prose. The model prefaced the JSON with a sentence, the parser
rejected the whole thing, and downstream code would have crashed on it.
Nothing about the content was wrong; the shape was.

This is what structural checks are for and why they sit low on the ladder:
cheap, exact, and they catch the failure that actually happens. The
priority failure on ticket-07 is a different problem — a judgement the
model made differently from the case author — and the reason strings are
what let you tell the two apart without reading twenty outputs. -->

## What the run found

```text
Running 20 cases

  ticket-01  PASS
  ticket-02  FAIL  not JSON: begins "Here is the JSON you asked for:"
  ticket-03  PASS
  ticket-07  FAIL  priority was medium
  ...

Pass rate: 16/20 (80%)
```

* The commonest failure was not a wrong answer. It was a right answer
  wrapped in **prose** — and the parser downstream would have crashed on it

* Two reasons, two different problems. The strings tell them apart without
  reading twenty outputs

---

<!-- Speaker notes: ~1:37. The fix for the prose-wrapped JSON lives in the
prompt, and the discipline from part 1 applies immediately: change the
prompt, re-run the whole set, read the reasons. The better prompt asks for
exactly the shape the parser needs and pins the label to the fixed list.

The mistake to expect is re-running only ticket-02, seeing it pass, and
declaring the fix good. That is the three-cases trap from part 1 in
miniature: a prompt change can move a different case — a stricter format
instruction can make the model drop a field it used to include — and only
the whole set shows it. -->

## The fix is a prompt change — so prove it

<p class="prompt bad">Extract the product, the issue and the priority from this message.</p>

<p class="prompt good">Extract the product, the issue and the priority from this message. Reply with one JSON object and nothing else: no sentence before it, no code fence around it. priority must be one of: low, medium, high.</p>

* Then re-run **the whole set**, not ticket-02. Did a case that passed
  before start failing?

* A stricter format instruction can cost you a field the model used to
  include. Only the set shows that

---

<!-- Speaker notes: ~1:39. Where the two mechanisms of part 2 join. The
pipeline does not know what an eval is; it sees one step and one exit
code. So the eval script is what turns a rate into a verdict: it prints
the rate and every reason into the log, and exits non-zero when the rate
is below the floor the team chose.

Two things follow. The definition of red is a decision the student makes
in the script, not something the pipeline supplies — below a fixed floor,
or below the last recorded run. And the part-1 rule applies to the eval
job as much as to the review job: if the feature could not be called at
all, the script must exit non-zero, because zero passes of zero cases is
not a hundred percent. -->

## The two halves meet at the exit code

<div class="flow">
  <div class="step"><span class="n">01</span>The eval script scores the set</div>
  <div class="step"><span class="n">02</span>Prints the rate and every reason into the log</div>
  <div class="step"><span class="n">03</span>Exits non-zero below the floor you chose</div>
  <div class="step"><span class="n">04</span>The pipeline sees an exit code. Nothing else</div>
</div>

* The pipeline does not know what an eval is. It knows that one step
  returned 1

* So "what does red mean?" is **your** decision, in the script: below a
  floor, or below the last run

* And the rule from part 1 still applies: if the feature could not be
  called at all, exit non-zero. **Zero passes of zero cases is not 100%**

---

<!-- Speaker notes: ~1:41. PREDICT beat 6; commit before revealing. Tests
what a rate is for: it is information only if it can move. Ten changes,
ten perfect scores, and the set cannot distinguish the change that helped
from the change that did nothing — so it is not measuring.

The wrong answer to expect is "yes, the feature is solid".
The faulty model is that a passing suite is evidence of quality, which is how
deterministic tests behave and is exactly wrong for an eval set: a
deterministic test that always passes is guarding an invariant, but an
eval case that always passes is one the feature never found hard, and a
whole set of them has stopped telling you anything NEW. It still guards
against regression — which is why those cases stay — but it cannot tell a
good change from a neutral one. The repair is to add the case that fails
today — the reversed figure, the prose-wrapped JSON — and the try-it-now
probably produced one. -->

## Predict: 20 of 20, ten changes in a row. Good news?

Your eval set has passed every case on each of the last ten prompt changes.

* Yes — the feature is solid
* Yes, as long as the cases were realistic
* No — the set has stopped measuring anything new
* You cannot know without a judge

---

<!-- Speaker notes: ~1:43. The reveal. A rate is information only if it
can move; when it stops moving, the set is too easy for the feature. Keep
the passing cases — a case that once failed and now passes is a regression
guard, and dropping it is how a fixed bug comes back — and add cases from
real failures, the ones this part produced. The goal was never a hundred
percent: it is a number that goes up when you improve something and down
when you break something, because that is the only kind of number that
can catch a regression. -->

## A set everything passes has stopped telling you anything new

* Ten changes, ten perfect scores: you cannot tell the change that helped
  from the one that did nothing

* A rate is information only if it can **move**. When it stops moving,
  keep the passing cases as the regression guard and add the case that
  fails today

* The best new cases are real failures: the reversed figure, the JSON
  wrapped in prose, the run that dropped the number

<div class="callout">

The goal is not 100%. The goal is a number that goes **up when you improve
things and down when you break them**.

</div>

---

<!-- Speaker notes: ~1:44. Common mistakes, drawn from both parts. The
pipeline ones all come from the runner not being the laptop and green
meaning only "exited 0"; the eval ones all come from the ladder — shape
below, meaning at the top — and from tuning against what you happened to
look at. -->

## Common mistakes

* Treating CI as administration rather than as the other half of the trade

* Trusting green without ever having watched the pipeline go **red**

- Assuming the runner has what your laptop has: packages, files, keys, your
  folder
- Letting a failed model call be reported as "no findings" — in a `try` or
  in a `||`
- Testing a non-deterministic feature with `assertEqual`
- Reaching for a judge when a property would be exact — or checking a fact
  is *present* and believing you checked it is *true*
- Tuning a prompt against the two examples you looked at; keeping a set at
  100% instead of adding the case that fails

---

<!-- Speaker notes: ~1:45. Summary and close. Return to the opening
question — "what is checking it, and who checks that?" — and let them
answer both halves: a run that is a fresh machine and an exit code, and a
set with a rate that can move. Leave the callout up for questions. -->

<!-- _class: dense -->

## Summary

- Automated checks are what make **not reading every line** defensible
- Order checks by **irreversibility** — secret scanning before test suites
- A run is a **fresh machine** doing only the steps you listed; green means
  every step exited 0, nothing more
- Ask AI what a compiler **cannot** check; a failed call is a failure, not
  a finding
- Non-deterministic features need a **set** and a **rate**; climb the
  ladder, **properties first, judge last** — shape below, meaning only at
  the top
- Measure before and after, or "better" is a feeling — and a rate that
  cannot move is not measuring

<div class="callout">

Twenty cases in a file, scored on every change, red when the number drops.
That is the difference between engineering and folklore.

</div>
