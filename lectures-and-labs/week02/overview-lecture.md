---
title: What AI-Assisted Programming Actually Is
topic: overview
type: lecture
source: authored
marp: true
theme: aiap
paginate: true
transition: fade
---

<!-- Speaker notes: ~0:01. Title slide. This lecture has one job: give the
room a MODEL of what the tool is, accurate enough to predict its behaviour.
Everything else depends on that model. A student who thinks the assistant
"looks things up" will be confused by hallucination for months; one who
knows it predicts text will find hallucination obvious.

Part 1 gives the model at the level of WHAT: prediction, not retrieval, and
what follows from it. Part 2 opens it up to HOW: tokens, the context
window, the ranked list of next tokens, and what each of those lets you do
about it. -->

<style>
/* bespoke to this deck: a token strip and a "rare" stack layer */
section .tokens { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 6px 0; }
section .tokens .tok {
  font-family: 'Cascadia Code', Consolas, monospace; font-size: 21px;
  background: #FFFFFF; border: 2px solid #33698C; border-radius: 6px;
  padding: 5px 12px; color: #1E2833; white-space: pre;
}
section .tokens .tok.next {
  border-style: dashed; border-color: #6741D9; background: #F4F0E6; color: #4C2FB0;
}
section .stack .layer.rare { border-style: dashed; border-color: #AFA893; color: #8B8471; }
section .stack .layer.rare .rank { color: #AFA893; }
</style>

<!-- _class: lead -->

<span class="kicker">// what is actually happening when it writes code</span>

# What AI-Assisted Programming Actually Is

---

<!-- Speaker notes: ~0:02. The hook: the completion everyone has seen and
nobody has asked about. Two questions sit under it, and the two hours
answer them in order. "How did it know?" is answered by prediction over
context — the signature is context, and a body is what usually follows a
signature. "Why is it confidently wrong?" is answered by the same
mechanism: plausible is the target, and nothing checks.

Leave both unanswered here. They are answered on the "prediction, not
retrieval" slide and closed properly on "The question, answered" near the
end. The gap between the two is the lecture. -->

## A question you already know the answer to

You type a function name. The AI llm writes the body.

<!-- no-parse -->
```python
def calculate_median(numbers):
```

* How did it know?

* And why is it sometimes **confidently, fluently wrong**?

---

<!-- Speaker notes: ~0:04. THE idea of the two hours, and the single most
useful sentence in them.

The misconception this kills: students assume the tool SEARCHES — that it
has a database of code and finds the matching snippet. That model predicts
"it can only give me code that exists", which is wrong, and makes
hallucination inexplicable. Prediction explains both the magic and the
failures with one mechanism, which is why it is taught first and why part
2 comes back to open it up. -->

## The one idea

<div class="callout">

It is not looking anything up. It is **predicting the next token**, over
and over, based on everything it has seen so far.

</div>

* Astonishing output and confident nonsense come from the **same**
  mechanism

* Nothing in it checks whether the answer is true

---

<!-- Speaker notes: ~0:06. Agenda, and the shape of the two hours. Part 1
is the model at the level of WHAT it does; part 2 is HOW it does it, which
is where the useful habits come from — what to show it, how to frame the
ask, and when to open a fresh conversation. Reference slide, immediate
bullets. -->

## The two hours

- **Part 1 — what it is**
  - Prediction, not retrieval, and what follows from it
  - The shapes these tools come in, and what each may touch
  - What they are genuinely good at; where they fail, predictably
  - What the job becomes
- **Part 2 — how it works**
  - Tokens, the context window, and why it does not remember
  - Why it wrote the fictional function, and when it will admit it
  - A second case: explaining code it cannot see
  - An activity on your own laptop, then the mistakes to avoid

---

<!-- Speaker notes: ~0:08. The mechanism at the level of behaviour, one
slide, no more. Architecture is not needed to predict what the tool will
do, and part 2 goes one level deeper anyway.

The three consequences are the payload, and each will be visible in their
own work within a fortnight: plausible is the target; it cannot report the
edge of its own knowledge; and the context is the only input, so changing
the context is the only steering. -->

## What follows from prediction

<div class="flow">
  <div class="step"><span class="n">01</span>Reads everything in its context</div>
  <div class="step"><span class="n">02</span>Predicts the most plausible next piece</div>
  <div class="step"><span class="n">03</span>Appends it, and repeats</div>
</div>

* **Plausible is the target** — not correct, not safe, not current

* It cannot tell you what it does not know, because it does not know that
  it does not know

* Change the context and you change the output. That is your entire
  steering wheel

---

<!-- Speaker notes: ~0:11. PREDICT beat 1: what a next-token predictor does
when asked to use something that does not exist. The concept under test is
that "I don't know" is a continuation like any other, and a rare one.

The wrong answer to expect is (b), "it tells you the function does not
exist". The faulty model is projected honesty: a human expert who did not
know would say so, so the tool will too. But a confident continuation is
far more common in training text than an admission of ignorance, so the
plausible next token is a plausible-looking function — which is exactly
what it produces. This lands hallucination by prediction rather than by
assertion, and the lab reproduces it deliberately. -->

## Predict: what does it do?

You ask for a function using `pandas.read_excel_fast()`.

**That function does not exist.**

* It writes a function that calls it, confidently
* It tells you the function does not exist
* It refuses to answer
* It searches the internet to check

---

<!-- Speaker notes: ~0:15. The reveal and the name. It usually writes the
code, because a confident continuation is more plausible than an
admission of ignorance; the mechanism worked exactly as designed.

"Usually" is deliberate. An assistant that says the function does not
exist is not the raw mechanism being honest: it is a product layer — a
search, a refusal tuned in — doing what prediction alone does not, and a
student whose tool said so has met that layer, not a more honest model.
The point survives either way: nothing in the mechanism checks, so where
no check has been added, this is what you get.

Name it — hallucination — and plant one forward reference without
elaborating: attackers can register the names it invents, so this
behaviour is also an attack surface. Part 2's ranked-list slide explains
why the same prompt tends to land on the same invention. -->

## Usually: it writes the code

<p class="prompt">Write a function that loads a spreadsheet using
pandas.read_excel_fast()</p>

<p class="reply">def load_sheet(path):
    return pd.read_excel_fast(path, engine="openpyxl")</p>

* Fluent. Well-named. Correctly styled. **Completely fictional.**

<div class="callout">

This is a **hallucination**, and it is not a bug being fixed — it is the
mechanism working exactly as designed.

</div>

---

<!-- Speaker notes: ~0:18. Recognising the shape of one, because the lab
asks them to produce a hallucination on purpose and then recognise it
later when it costs something. The concept: fluency is evidence of
plausibility and of nothing else, so there is no tell inside the text —
the check is always outside it.

The characteristic error is looking harder at the text for a sign it is
wrong. Students expect a hallucination to look slightly off — odd naming,
a hedge, a wobble — because that is how a human bluff looks. It does not:
the invented name follows the library's own naming pattern, and a real
argument (engine="openpyxl" is a genuine read_excel argument) sits on the
fictional function. The habit to build is "verify outside", not "read
more carefully". -->

## What a hallucination looks like

* Fluent, specific, well-formed — and not hedged at all

* Names that follow the library's own pattern: `read_excel_fast` sits
  beside `read_excel` as if it belonged

* Often a **real** argument on a **fictional** function: `engine="openpyxl"`
  is genuine; the function it is passed to is not

* There is **no tell in the text**. The check is outside it: the
  documentation, or running it

<div class="callout">

Fluency is evidence of plausibility. It is not evidence of anything else.

</div>

---

<!-- Speaker notes: ~0:21. The shapes. This is the slide that ages fastest,
so it teaches the CATEGORIES and treats named products as examples that
will change; saying so out loud is honest and keeps the slide useful in
two years.

The concept: the four shapes differ in how the prediction is wrapped, not
in the predictor. The same mechanism sits under all of them, so everything
said so far applies to all four. Reference slide, immediate bullets. -->

## The shapes these tools come in

| Shape | What it does | Where it lives |
|---|---|---|
| **Completion** | Finishes the line or block you are typing | Inline, as you type |
| **Chat** | Answers questions about code you show it | A side panel |
| **Edit** | Rewrites a selection you describe | In the file, as a diff |
| **Agent** | Works out the steps and does them | Editor or terminal |

<span class="kicker">// the products change yearly; the shapes have been stable</span>

---

<!-- Speaker notes: ~0:24. The four shapes told apart by what each may
change before you see anything — the distinction the lab's four-row table
asks for. The concept: as the shape moves down the list, the tool acts
earlier and you review later, so the thing you review changes from a
suggestion, to a diff, to a finished outcome.

The misconception: students see the four as the same tool with more or
less typing saved. The faulty model is "same output, different
convenience". In fact the review point moves, and an agent has already
changed files and run commands by the time there is anything to look at.
"What did I review?" is the question that separates the rows. -->

## What each shape may touch

<div class="stack">
  <div class="layer"><span><strong>Completion</strong> — the line under your cursor</span><span class="rank">you review: a suggestion</span></div>
  <div class="layer"><span><strong>Chat</strong> — nothing, unless you paste it</span><span class="rank">you review: advice</span></div>
  <div class="layer"><span><strong>Edit</strong> — the selection you described</span><span class="rank">you review: a diff</span></div>
  <div class="layer untrusted"><span><strong>Agent</strong> — files, commands, whatever it decides it needs</span><span class="rank">you review: the outcome</span></div>
</div>

* The further down, the more has changed **before you see anything**

* So the review moves too: a suggestion, then a diff, then an outcome

---

<!-- Speaker notes: ~0:27. Genuinely good at, and meant sincerely — a
lecture that only warns gets discounted, and the room already knows these
tools are useful.

The unifying property is the concept: every item is a task where the right
answer is CONVENTIONAL, and conventional is exactly what a predictor of
plausible text is best at. Part 2 gives the reason — it learned the
statistics of what usually follows what — so this slide is the WHAT and
the tokens slide is the WHY. -->

## What they are genuinely good at

- Boilerplate you have written a hundred times
- Translating between languages or formats
- Explaining unfamiliar code, at speed
- First-draft tests, docstrings, regexes
- Naming things, and the mechanical half of refactoring

<div class="callout">

The pattern: tasks where the right answer is **conventional**. A predictor
of plausible text is excellent at what is, by definition, typical.

</div>

---

<!-- Speaker notes: ~0:30. The mirror image, and the symmetry is
deliberate: the same mechanism explains both lists, which is the whole
point of teaching prediction first. Novel is not typical; recent is not in
the training text; your conventions are not in the context; counting and
arithmetic are done on tokens rather than letters or digits, and part 2
says why.

The one that costs students most is the third: it does not know their
codebase unless they show it. Half of "the AI is useless here" complaints
are context problems, and part 2's context-window slide is where the
reason lives. -->

## Where they fail, predictably

- Anything **novel** — if it is not typical, it is not plausible
- Anything **recent** — training has a cutoff, and libraries move
- **Your** conventions, unless you show them
- Arithmetic and counting, still
- Knowing when to stop: it will confidently answer a question you should
  not have asked

<span class="kicker">// every one of these follows from "plausible, not correct"</span>

---

<!-- Speaker notes: ~0:33. PREDICT beat 2: does the quality of the answer
depend on the tool, or on what you put in front of it? The concept is that
the second prompt supplies a DECISION the tool would otherwise have to
guess.

The wrong answer to expect is "they are equivalent — it knows Python, so it
knows what a valid email is". The faulty model is that the tool has one
fixed level of competence, like a compiler. It does not: quality is a
function of the context, and B removes a guess. This sets up context
engineering directly, and the lab has them run both prompts. -->

## Predict: which gets the better answer?

<p class="prompt bad">Write a function to validate an email address</p>

<p class="prompt good">Write a function to validate an email address.
We accept anything with an @ and a dot after it — we deliberately do NOT
want RFC 5322 compliance. Reject anything over 254 characters.</p>

- Same tool. Same model. **Same day.**

---

<!-- Speaker notes: ~0:37. The reveal and the lesson. B wins, and not
because it is longer — because it makes a decision the tool would
otherwise make for you, silently and probably wrong for your case.

The concept to land: validation strictness is a product decision, and a
text predictor hands an unspecified decision to whatever was most common
in its training text. The gap between those two answers is skill, and it
is learnable — that is the optimistic note of the two hours, and it is
true. -->

## The second one, every time

* Not because it is longer — because it **decides** something

* Left unspecified, the tool picks for you, silently

<div class="callout">

Validation strictness is a **product decision**. Hand it to a text
predictor and you get whatever was most common in its training data.

</div>

- The gap between those two answers is **skill**, and skill is learnable

---

<!-- Speaker notes: ~0:40. What the job becomes. This answers the anxious
question in the room, which is usually "does this replace me", and it is
answered directly: generating code got cheap; deciding what should exist,
supplying the context, and judging what arrived did not. That is a more
senior job than the one it replaced, not a lesser one.

The layers map onto the rest of the lecture: the middle two are what part
2 teaches how to do. -->

## So what is the job now?

<div class="stack">
  <div class="layer top"><span>Deciding what should exist, and what "correct" means</span><span class="rank">yours</span></div>
  <div class="layer"><span>Supplying the context that makes a good answer possible</span><span class="rank">yours</span></div>
  <div class="layer"><span>Judging what came back</span><span class="rank">yours</span></div>
  <div class="layer untrusted"><span>Typing the characters</span><span class="rank">cheap now</span></div>
</div>

* The bottom row got cheap. **The other three did not.**

---

<!-- Speaker notes: ~0:43. PREDICT beat 3, the honest one. The concept is
that the productivity effect is real, modest, and depends on the task more
than on the tool — and that perceived and measured speed come apart.

The wrong answer to expect is a large single number, usually "10x". The
faulty model is that a tool has a fixed speed-up, absorbed from marketing.
Controlled studies find smaller and highly task-dependent effects, and
some find experienced developers on familiar code get SLOWER while feeling
faster — the 2025 METR randomised trial of experienced open-source
developers is the best-known example. The perception gap is the finding
worth remembering. -->

## Predict: how much faster does this make you?

* 10× faster
* Roughly 2× faster
* It depends enormously on the task
* Sometimes **slower** — while feeling faster

---

<!-- Speaker notes: ~0:47. The honest answer: the last two options are both
right, and "feels faster than it is" is the one that changes behaviour,
because it means your own sense of the tool's value is not reliable
evidence.

Say plainly that headline productivity numbers in vendor material are
marketing; measured effects are real but modest and task-dependent. This
buys credibility for everything else in the lecture, including the
mechanism in part 2. -->

## Honestly: it depends

- Large gains on **boilerplate and unfamiliar territory**
- Small or negative on **code you know well**
- Debugging is the hardest to measure and the easiest to lose time on

<div class="callout">

The uncomfortable finding: developers often report feeling faster on tasks
where measurement says they were not. **Perceived** speed and **actual**
speed come apart.

</div>

---

<!-- Speaker notes: ~0:50. The model is not the whole product. ChatGPT and
Claude add training, system instructions, retrieval, citations, and refusal
behaviour around the predictor. These layers can make an unsupported answer
less likely, but they do not turn generated text into verified fact.

OpenAI's public material says hallucinations remain a problem and describes
search and deep research as reducing, not eliminating, errors. Anthropic's
guidance recommends allowing uncertainty, grounding in supplied documents,
using direct quotes, and verifying with citations. Keep the distinction
between a useful signal and a guarantee explicit. -->

## What ChatGPT and Claude add

| Product layer | How it fights hallucination | What it cannot promise |
|---|---|---|
| **ChatGPT** | Search or deep research can add current sources and citations | A source can be weak, misread, or cited for a claim it does not support |
| **Claude** | Uncertainty training, document grounding, quotes, and citations can make gaps visible | It can still answer fluently when the evidence is missing |

<div class="callout">

Both products are trying to **change the odds**, not replace the check.

</div>

* Retrieval adds evidence to the context; it does not change the predictor
* A refusal or an **I don't know** is useful behaviour, not proof that the
  system knows its own limits

---

<!-- Speaker notes: ~0:52. This is the practical prompt to leave the room
with. The important move is not just "be honest"; it is to define what counts
as evidence and what to do when evidence is absent. Cite the source, then
check that the source really supports the claim. A model can follow this
instruction and still fail, so verification remains outside the answer. -->

## Ask for "I don't know" properly

<p class="prompt good">Answer only from the evidence provided or from sources you can cite. If the evidence is insufficient, say "I don't know" or "I don't have enough information." Separate verified facts from inferences. Do not fill gaps with plausible details.</p>

* **Give it a boundary:** use only this document, these sources, or a named
  tool
* **Give it an escape:** say what to do when the evidence is insufficient
* **Give it a check:** cite the source, quote the supporting passage, or run
  the test

<div class="callout">

You can make **"I don't know" more likely**. You cannot make it a guarantee.

</div>

---

<!-- Speaker notes: ~0:51. The bridge to part 2. Part 1 has given a model
of WHAT the tool does; these four questions are ones that model cannot
answer, and every one of them bites students in the first fortnight. Part
2 answers all four with one more level of mechanism: tokens, the context
window, frozen weights, and a ranked list of next tokens.

Nothing is revealed here. The slide exists so the room goes into the break
holding questions rather than conclusions. -->

## Four things part 1 cannot explain

* Why did it write `read_excel_fast` instead of saying "that does not
  exist"?

* Why does the **same prompt** give a different answer tomorrow?

* What exactly can it see — and why not the file beside the one you
  opened?

* Why does asking again **in a fresh conversation** change the answer?

<span class="kicker">// part 2 is one mechanism behind all four</span>

---

<!-- Speaker notes: ~0:55. Break. Part 2 answers one question: how does
"predict the next token" actually work — tokens in, a ranked list out, one
picked, over a context that is finite and starts empty — and what does
that let you do about it. The habits that follow are the point: show it
the file, put the decision in the ask, and open a fresh conversation when
you want a check rather than a continuation. -->

<!-- _class: lead -->

<span class="kicker">// break</span>

## Ten minutes

Part 2 answers: how does "predict the next token" actually work — and what
does that let you do about it?

---

<!-- Speaker notes: ~1:05. Part 2 opens one level down: what the model
actually sees. Text is chopped into TOKENS — pieces of words, punctuation,
runs of spaces — and every token becomes a number before the model sees
it. It does not read letter by letter, and it does not read code as code;
a line of Python is a sequence of pieces, the same as a line of prose.

Two consequences pay off part 1. Counting letters and doing arithmetic are
hard because the units it works in are not letters or digits. And
"conventional" is what it is good at because training was, at bottom, one
job: learn from an enormous amount of text which pieces usually follow
which. The split shown is illustrative — different tools cut text
differently, and the exact boundaries are not the point. -->

## What it actually sees: tokens

<div class="tokens">
  <span class="tok">def</span><span class="tok"> calculate</span><span class="tok">_</span><span class="tok">median</span><span class="tok">(</span><span class="tok">numbers</span><span class="tok">):</span><span class="tok next">?</span>
</div>

<div class="legend">one illustrative split — tools cut text differently; the dashed box is the piece it is about to predict</div>

* Text is cut into **tokens** — pieces of words, punctuation, runs of
  spaces — and each becomes a number

* It does not read letter by letter, and it does not read your code *as
  code*: a line of Python is a sequence of pieces, like a line of prose

* Training was, at bottom, one job: learn from an enormous amount of text
  which pieces usually follow which

<span class="kicker">// why counting letters is hard, and why "conventional" is easy</span>

---

<!-- Speaker notes: ~1:07. One step of the loop, and the two facts to
carry out of it. First: nothing inside the network changes between steps
— the same fixed numbers score every candidate every time; only the
sequence grows, by one token, and the whole sequence is fed back in.
Second: there is no step labelled "check". Correctness is not computed
anywhere; a token is chosen because it is likely given everything before
it, and that is the entire criterion.

This is the HOW behind part 1's "plausible is the target", and it is the
slide to teach from if a student asks why the tool cannot simply verify
its own answer: verification is not a stage in the loop, so it only
happens if you make it part of the context — a test, a document, a direct
question. -->

## One step of the loop

<div class="flow">
  <div class="step"><span class="n">01</span>Everything so far, as tokens</div>
  <div class="step"><span class="n">02</span>Score <strong>every</strong> possible next token</div>
  <div class="step"><span class="n">03</span>Pick one — usually a likely one</div>
  <div class="step"><span class="n">04</span>Append it, feed it all back in</div>
</div>

* The network is **fixed**. Between steps, only the sequence grows

* There is no step labelled "check". Likely, given everything before it,
  is the **entire** criterion

* So a reply is built one piece at a time, each piece committed before the
  next is chosen

---

<!-- Speaker notes: ~1:09. The context window: the complete list of what
the model can see and — the half students need — what it cannot. The
context is the instructions the tool adds, the conversation so far
INCLUDING its own earlier replies, whatever files were attached or pasted,
and nothing else. It is finite; what does not fit is not seen.

The concept that fixes the commonest complaint: the model does not know a
file exists because the file is in the same folder. "It can see the repo"
is false unless the tool put the file into the context. The lab's DIY on
explaining a file with and without it open is this slide as an exercise.
And its own earlier replies being context is the seed of the
fresh-conversation predict that follows. -->

## The context window: all it can see

<div class="stack">
  <div class="layer top"><span>Instructions the tool adds before you type anything</span><span class="rank">always in</span></div>
  <div class="layer"><span>The conversation so far — <strong>including its own replies</strong></span><span class="rank">in</span></div>
  <div class="layer"><span>Files you attached or pasted, or the tool chose to include</span><span class="rank">in, if put there</span></div>
  <div class="layer untrusted"><span>The rest of your repo, the docs, the internet, yesterday's chat</span><span class="rank">not in</span></div>
</div>

* It is **finite**. What does not fit is not seen

* Nothing outside it exists. "It can see the repo" is false unless the
  tool put the file in

---

<!-- Speaker notes: ~1:11. PREDICT beat 4: does the tool learn from being
used? The concept under test is that the network is fixed and the context
starts empty, so nothing said in one conversation reaches the next unless
something puts it there.

The wrong answer to expect is (a), "it follows the convention — I told it
yesterday". The faulty model is a colleague: someone who learns your
preferences by working with you. The tool is not one. The weights were set
once, in training; typing at it changes the context and nothing else; and
a new conversation is a new, empty context. If a tool does appear to
remember, in practice it is re-inserting saved text into the context —
which is worth knowing, because that text can be read, edited, and
deleted. -->

## Predict: does it remember?

Yesterday you told it, in a long conversation, that your team names
booleans `is_…` and never uses single-letter variables.

Today, in a **new** conversation, you ask for a function.

* It follows your convention — it learned it yesterday
* It follows the convention only if something put it in today's context
* It asks you what conventions to use

---

<!-- Speaker notes: ~1:13. The reveal: no. The concept is the split the
table draws — what was fixed in training versus what you change every
message — and it explains two of part 1's failure modes at once. "Recent"
fails because the training snapshot has a cutoff and the weights do not
move. "Your conventions" fails because they are not in the snapshot and
not in today's context.

The practical consequence is the habit to build: anything you want it to
know every time — conventions, decisions, the shape of the project — has
to be written down somewhere the tool puts into the context each time.
Whether that is a pasted note or a standing instructions file, it is
context, and it is yours to maintain. -->

## Frozen weights, live context

| Fixed at training | Changed by you, every message |
|---|---|
| What it knows, up to a cutoff | What it can **see** right now |
| How it writes; what counts as "typical" | The question, and how it is framed |
| Nothing you type changes it | Everything you type changes it |

* "It learned that yesterday" is never true. **It was in the context
  yesterday**

* Anything it must know every time has to be written down where the tool
  will put it in — every time

---

<!-- Speaker notes: ~1:15. The honest refinement of part 1's headline. "It
does not look things up" is true of the model; the PRODUCT around it may
add tools — a search, a file read, a test run — and the students' own
tools do. The concept is what a tool result is: text that gets pasted into
the context and then predicted over, exactly like anything else there. The
mechanism did not change; the context got a new ingredient.

Why it matters: a looked-up fact can still be misread, quoted wrongly, or
outvoted by what was "typical", because the step after the lookup is still
prediction. So a tool that searches has raised the odds, not removed the
job of checking. This also sets up the "explain a file" predict — the file
has to actually be in the context. -->

## When it does look things up

<div class="flow">
  <div class="step"><span class="n">01</span>The tool runs a search, reads a file, runs a test</div>
  <div class="step"><span class="n">02</span>The result is <strong>pasted into the context</strong></div>
  <div class="step"><span class="n">03</span>Prediction continues — over the new text</div>
</div>

* Retrieval changes **what is in the context**. It does not change the
  mechanism

* A looked-up fact can still be misread, misquoted, or outvoted by
  "typical" — the step after the lookup is still prediction

<span class="kicker">// a tool that can search has raised the odds, not removed the check</span>

---

<!-- Speaker notes: ~1:17. The ranked list, and with it the HOW behind
predict 1. After "write a function that uses read_excel_fast()", the
candidates for the next piece are ranked by how often such a request has
been followed by each kind of text. Code that uses the named function is
the overwhelming pattern; "that does not exist" is a rare continuation of
a request phrased as if it exists. The request PRESUPPOSED the function,
and the ranking inherited the presupposition.

Two further consequences. Sampling: the pick is usually a likely
candidate, not always the top one, so the same prompt gives different
answers on different runs — that is not a malfunction. Stability: when
the wrong answer is the top candidate, sampling keeps landing on it, so
the same fiction comes back again and again — different in detail, same
in kind. -->

## The ranked list

<p class="prompt">Write a function that loads a spreadsheet using
pandas.read_excel_fast()</p>

<div class="stack">
  <div class="layer top"><span><code>def load_sheet(path):</code> — code that uses the function named</span><span class="rank">most likely</span></div>
  <div class="layer"><span>"Here's a function that…" — prose, then the same code</span><span class="rank">likely</span></div>
  <div class="layer rare"><span>"pandas has no <code>read_excel_fast</code>; did you mean…"</span><span class="rank">rare</span></div>
</div>

* The request **presupposed** the function. The ranking inherited it

* The pick is usually likely, not always top: same prompt, different
  answers — and often the same fiction again

---

<!-- Speaker notes: ~1:19. PREDICT beat 5: same knowledge, different
question. The concept under test is that the question shapes the ranked
list — "write code using X" presupposes X, "does X exist?" invites a
factual answer — and that a fresh conversation removes its own earlier
code from the context, so there is nothing to stay consistent with.

The wrong answer to expect is "it insists the function exists — it just
wrote it". The faulty model is that the tool holds beliefs and defends
them across conversations. It holds no belief; it has a context. In the
SAME conversation the wrong answer is more likely, because the code it
wrote is now context and continuing consistently is the plausible pattern
— which is why "fresh" is in the question. The second-commonest wrong
answer, "it cannot know", comes from thinking the first answer showed it
lacked the knowledge; it did not, it showed it was never asked. The lab's
DIY on hallucination ends with exactly this step. -->

## Predict: fresh conversation, direct question

It has just written `pd.read_excel_fast(...)` for you.

You open a **new** conversation and ask:

<p class="prompt">Does pandas.read_excel_fast actually exist?</p>

* It insists it exists — it just used it
* It says no, and names the real function
* It says it cannot know without checking

---

<!-- Speaker notes: ~1:21. The reveal: usually the truth, and the line to
land is the lab's — it had the information; nothing in the first prompt
made it check. The knowledge of the real pandas API was in the weights
both times. What changed is the context: a direct factual question ranks
a factual answer at the top, and a fresh conversation contains no code of
its own to stay consistent with.

The two habits that follow are the useful output of this slide. Ask for a
check as a check, not buried inside a request that assumes the answer.
And ask it in a fresh conversation, because in the one that produced the
code, the code is now context and "yes, that's right" is the plausible
continuation of its own work. -->

## Usually: the truth

<p class="reply">No — pandas has read_excel(), but there is no
read_excel_fast(). Did you mean read_excel()?</p>

* Same weights, same knowledge, **different question** — the ranking
  followed the question

* In the conversation that wrote the code, the code is now context, and
  agreeing with itself is the plausible continuation

<div class="callout">

It had the information. **Nothing in the first prompt made it check.**
Ask for a check as a check — and ask in a fresh conversation.

</div>

---

<!-- Speaker notes: ~1:23. PREDICT beat 6, and the second worked case —
different in kind from part 1's: an EXPLAIN task rather than a write task,
and a context failure rather than a knowledge failure. The concept under
test is that a filename in the prompt is context like any other, and a
description of what such a file typically does is a more plausible
continuation than "I cannot see it".

The wrong answer to expect is (a), "it says it cannot see the file". The
faulty model is that the tool has a sense of what it has and has not read
— a boundary it can report. It does not; it has a context, and the context
contains a filename, so the top-ranked continuation is what files with
that name usually do. If a student's tool does say it cannot see the file,
that is the better behaviour and the fix is identical: put the file in the
context. The lab's DIY on explaining a file with and without it open is
this predict, run for real. -->

## Predict: explain a file it cannot see

You have a file called `backup.py`. You have **not** opened it, attached
it, or pasted it.

<p class="prompt">Explain what backup.py does.</p>

* It says it cannot see the file
* It asks you to paste it
* It explains, fluently, what a file called that usually does

---

<!-- Speaker notes: ~1:25. The reveal: a fluent description of a typical
backup script, and the concept is the TELL — "typically", "usually", "a
script like this" are the words a predictor produces when the context has
a name and no content. They are the honest part of the answer, and
students read straight past them.

Note what is and is not wrong here. Nothing in the reply is false about
backup scripts in general; none of it is known to be true about this one.
That is the characteristic shape of a context failure: generic, hedged,
and confident about the category rather than the instance. The next slide
puts the file in and the answer changes completely. -->

## A plausible guess

<p class="reply">backup.py is typically a script that copies important
files or directories to a backup location — usually a timestamped folder
or an archive — and may compress them. It will likely use shutil or
zipfile, and may accept the source and destination paths as arguments.</p>

* Nothing here is false about backup scripts **in general**

* Nothing here is known to be true about **this one**

<div class="callout">

The tell: *typically, usually, likely, may*. Those are the words of a
guess from a filename. They are the honest part of the answer.

</div>

---

<!-- Speaker notes: ~1:27. Same question with the file in the context, and
the answer is now specific, checkable against the code on the slide, and
different in the one way that matters: the file deletes, it does not copy.
The concept is the lab's line — the model was not smarter the second time,
it could see more — and the practical test that follows from it: if you
can check the explanation against the code in front of you, you gave it
the code; if you cannot, it is guessing.

Note the change in vocabulary: no "typically", no "usually". Specific
names, specific numbers, specific behaviour. That shift is the fastest way
to tell the two situations apart in the lab. -->

## Same question, file in the conversation

```python
import time
from pathlib import Path

KEEP_DAYS = 30

def prune(folder):
    cutoff = time.time() - KEEP_DAYS * 86400
    for path in Path(folder).glob("*.zip"):
        if path.stat().st_mtime < cutoff:
            path.unlink()
```

<p class="reply">It deletes every .zip in the given folder whose modified
time is older than 30 days. Despite the name, it never creates a backup.</p>

* Not smarter. **It could see more** — and now you can check it

---

<!-- Speaker notes: ~1:29. Why "explain" is the safer ask, which is the
lab's closing point and the one students least expect: an explanation is
checked against code that is in front of you, right now, by reading;
generated code is checked against a spec you may never have written down,
by running it, later. The mechanism is the same in both, so the difference
is entirely in how cheap the check is.

The second point is the deeper one and connects to "what the job becomes":
an explanation leaves you understanding the code, and understanding is one
of the things that did not get cheap. Asking it to write leaves you a file
you must now understand anyway. -->

## Why "explain" is the safer ask

| Ask it to **explain** | Ask it to **write** |
|---|---|
| Checked against code **in front of you** | Checked against a spec you may not have written |
| Checked by **reading**, now | Checked by **running**, later |
| Wrong answers caught while you hold the context | Wrong answers surface when something breaks |
| Leaves you **understanding** | Leaves you a **file** — to understand anyway |

* Same mechanism both times. The difference is how cheap the **check** is

---

<!-- Speaker notes: ~1:31. The one activity: seven to eight minutes on
their own laptops with whatever assistant they have. The concept it makes
visible is two things from the two hours at once. Sampling — an identical
ask in two fresh conversations gives two answers, because a ranked list
was sampled, not a stored function retrieved. And silent decisions — an
empty list and an even-length list are both decisions the ask left open,
and neither answer will say it made them.

If a pair of answers comes out identical, the second point still holds and
is the one to debrief on. Students without an assistant to hand can pair
up; the comparison is the exercise, not the typing. The debrief slide
carries the wording that brings the decisions back into the prompt. -->

## Try it now: the same ask, twice

<p class="prompt">Write a Python function calculate_median(numbers) that
returns the median of a list of numbers.</p>

- Ask it in a **fresh** conversation. Keep the answer
- Open **another** fresh conversation and ask exactly the same thing
- Put the two side by side

* **Notice:** empty list — exception, `None`, or silence? Even count — the
  mean of the middle two, or one of them? Neither answer told you it had
  decided

* If the two differ at all, that is **sampling**: there was no single
  answer in there to retrieve

<span class="kicker">// seven minutes, on your own laptop, with whatever assistant you have</span>

---

<!-- Speaker notes: ~1:39. Debrief, and the payoff is part 1's lesson
arriving from the other direction: the email validator showed that an
unspecified decision gets made silently; the median function shows the
same thing on the hook's own example, and the fix is identical — put the
decision in the ask. Two different answers, if they appeared, are the
ranked list being sampled, and neither is "the" answer the tool
retrieved.

The characteristic mistake in the debrief is to judge the two answers on
style — variable names, a sort versus a selection trick — rather than on
behaviour at the edges. The edges are where the silent decisions live, and
where any difference between the two runs is most likely to show. -->

## What you should have seen

* Two fluent answers, possibly different — a ranked list sampled twice,
  not a stored function found twice

* The empty list handled **somehow**, and the even count handled
  **somehow**, without either answer saying it chose

- The fix is part 1's skill on part 2's mechanism: make the decision, and
  put it in the context

<p class="prompt good">Write a Python function calculate_median(numbers) that
returns the median of a list of numbers. Raise ValueError on an empty list.
For an even count, return the mean of the two middle values.</p>

---

<!-- Speaker notes: ~1:41. Back to the hook, now answerable in full, and
better asked of the room than restated. "How did it know?" — the signature
was in the context, and a body has followed a line like that many times in
its training text, so a body is the top of the ranked list. "Why
confidently wrong?" — likely is the whole criterion, "I don't know" is
rarely near the top, and it could not see anything you did not put in
front of it.

The concept to make explicit: both halves of the question have the same
answer, which is the claim the lecture opened with. If a student can give
both halves in their own words, the model has landed. -->

## The question, answered

<!-- no-parse -->
```python
def calculate_median(numbers):
```

* **How did it know?** The signature is context. A body has followed a
  line like that many times in its training text, so a body tops the
  ranked list

* **Why confidently wrong?** Likely is the whole criterion; "I don't know"
  is rarely near the top; and it cannot see what you did not show it

<div class="callout">

One mechanism. Both halves of the question.

</div>

---

<!-- Speaker notes: ~1:43. Common mistakes on the asking side, in the order
students meet them. The first three are part 1's; the fourth is part 2's,
and it is the one the frozen-weights slide exists to prevent — the context
starts empty every time, so a convention told once is a convention told to
nobody.

The last is the important one: an assistant asked to solve a problem does
not stop to ask whether the problem is worth solving, because "should I?"
is never the plausible continuation of "do this". -->

## Common mistakes: asking

* Believing it **looked something up**

* Giving it a vague ask, then blaming the tool for guessing

- Not showing it the code it needs to see — it sees the conversation, and
  nothing else
- Expecting it to remember what you told it in another conversation
- Letting it answer a question you should have questioned

---

<!-- Speaker notes: ~1:44. Common mistakes on the reading side. Each one is
a mechanism from part 2 misread as something else: fluency read as
correctness; hedge words read as facts about your code; a hallucination
read as a bug rather than the loop working normally; a different second
answer read as a fault rather than sampling; and its own earlier code read
as an independent opinion rather than as context it will continue.

The last is the practical one. In the conversation that wrote the code,
"is this right?" is answered by the plausible continuation of its own
work. A fresh conversation, given the code as data, is a different
input. -->

## Common mistakes: reading what comes back

* Accepting the first answer because it is **fluent**

* Reading *typically* and *usually* as a description of **your** code

- Treating a hallucination as a bug in the tool — it is the loop working
  normally, and your job is to notice
- Reading a different second answer as a malfunction — that is sampling
- Asking "is this right?" in the conversation that wrote it — it will
  continue its own work, not review it

---

<!-- Speaker notes: ~1:45. The honest limits of the lecture's own model,
stated so nobody over-applies it. "Predict the next token" describes the
model; the tools students use wrap it in things that put more into the
context — searches, file reads, test runs, and generated "thinking" that
is itself more text in the context before the answer. Every one of those
raises the odds of a right answer, and none of them is a verification
step, because the step after each of them is still prediction.

The claim to leave in place is the modest one: the mechanism explains the
behaviour well enough to predict it, and it says nothing about what the
tools will be able to do in a year's time. What it says about YOUR job —
decide, supply, judge — does not move. -->

## Where this picture is a simplification

- "Predict the next token" describes the **model**. The tools around it
  add searches, file reads, test runs — each puts more into the context
- Some tools generate their reasoning before the answer. That reasoning is
  **more text in the context**: it raises the odds; it is not a check
- The mechanism predicts the behaviour. It says nothing about what the
  tools will be able to do in a year's time

<div class="callout">

What it says about **your** job — decide, supply the context, judge what
came back — does not move.

</div>

---

<!-- Speaker notes: ~1:47. Summary and close. The first four lines are part
1's model at the level of WHAT; the last two are part 2's HOW. The useful
test of the two hours is whether a student can now explain the hook's
completion in their own words — both halves, one mechanism — and say what
they would change about a prompt, and when they would open a fresh
conversation. Leave the callout up for questions. -->

<!-- _class: dense -->

## Summary

- It **predicts plausible text**. It does not retrieve, and it does not
  verify
- Brilliance and hallucination are the **same mechanism**
- Four shapes — completion, chat, edit, agent — told apart by what each
  may touch; the products change yearly
- Good at conventional, weak at novel, recent, or specific to you
- Under the bonnet: tokens in, a **ranked list** out, one picked, repeat —
  over a finite context, with weights that never change
- The context is the only thing you steer: what it can see, how the ask
  is framed, and whether the conversation is fresh

<div class="callout">

The typing got cheap. Deciding what should exist, and judging what came
back, did not.

</div>
