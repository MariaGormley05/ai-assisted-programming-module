---
title: Retrieval and Grounding
topic: rag
type: lecture
source: authored
marp: true
theme: aiap
paginate: true
transition: fade
---

<!-- _class: lead -->

<span class="kicker">// giving it what it does not know</span>

# Retrieval and Grounding

---

## A problem you cannot prompt your way out of

Your company has 40,000 internal documents.

A user asks a question whose answer is in one of them.

* The model has never seen any of them

* How do you get it to answer **correctly**?

---

## The one idea

<div class="callout">

You do not teach the model your documents. You **find the relevant piece
and put it in the prompt.**

</div>

* No retraining. No fine-tuning

* The model is the reasoning engine; **you** supply the facts

---

## Two hours, two halves

- **Part 1 — the decision, then the pipeline**
  - Do you even need retrieval? Long context versus retrieval
  - How retrieval works: chunk, embed, search
  - Grounding and citation, and what they fix
  - Where it goes wrong
- **Part 2 — the mechanism**
  - How a few hundred numbers hold meaning
  - Why chunk size and overlap change what comes back
  - How the hybrid fits together, a second worked case, and you try it

---

## First: do you need it at all?

* When RAG became popular, context windows held a **few thousand** tokens

* Retrieval was the only way to work with anything larger

- Today's windows hold **hundreds of thousands** to millions

<div class="callout">

For a lot of problems, the correct architecture is now **paste the whole
thing in** — when the whole thing fits, and is what the question is about.
No chunking, no embeddings, no database to maintain.

</div>

---

## Predict: five short documents, conversational questions

You have five documents, a few thousand words in total. Users ask open
questions about them.

* Chunk, embed, and build a vector database
* Paste all five into the prompt
* Fine-tune a model on them
* Summarise each, then discard the originals

---

## It depends — and here is on what

| Situation | Reach for |
|---|---|
| Small corpus, conversational questions | **Long context** — just paste it |
| Too large to fit, or thousands of documents | **Retrieval** |
| You must cite which source said it | **Retrieval** gives it free — a labelled full context can too |
| Data changes constantly | **Retrieval**, or live search |
| Cost matters at scale | **Retrieval** — crossover ≈ a couple of thousand pages, as a rule of thumb |

---

## Long context is not free either

- **Lost in the middle** — attention is less reliable in the middle of a
  very long input than at either end
- **Dilution** — marginally relevant text competes with the relevant part
- Cost and latency scale with everything you send

<div class="callout">

Adding more context can make an answer **worse**. More tokens is not more
understanding.

</div>

---

## Worked case: the 40,000 documents

<div class="flow">
  <div class="step"><span class="n">01</span>Scope: which documents does <strong>this question</strong> need?</div>
  <div class="step"><span class="n">02</span>Size: does that subset fit the window?</div>
  <div class="step"><span class="n">03</span>Fits? Paste it. Doesn't? Retrieve</div>
  <div class="step"><span class="n">04</span>Need citation or freshness? Retrieve anyway</div>
</div>

* 40,000 documents at a page each is far past the crossover → **retrieval**

* But a question about the leave policy needs **one handbook** — which fits

<div class="callout">

Size the corpus a **question** needs, not the corpus the company owns.

</div>

---

## How retrieval works

<div class="flow">
  <div class="step"><span class="n">01</span>Split documents into chunks</div>
  <div class="step"><span class="n">02</span>Embed each chunk as a vector</div>
  <div class="step"><span class="n">03</span>Embed the question too</div>
  <div class="step"><span class="n">04</span>Find the nearest chunks</div>
  <div class="step"><span class="n">05</span>Put them in the prompt</div>
</div>

* Only the **last** step involves the model

* Steps 1–4 are ordinary information retrieval

---

## Embeddings: meaning as coordinates

* A vector of numbers representing **what a piece of text means**

* Similar meanings land **near each other**, whatever words they used

| Query | Keyword search finds | Embedding search finds |
|---|---|---|
| "car maintenance" | documents containing "car" | "vehicle servicing", "auto repair" |
| "how do I quit" | "quit" | "resignation process", "leaving the company" |

---

## Predict: which chunk size retrieves best?

You split a manual into chunks. Which works best?

* One sentence per chunk — maximum precision
* One paragraph per chunk
* One page per chunk
* The whole document as one chunk

---

## A paragraph, usually — and here is why

* **Too small:** *"It must be replaced every 12 months."* Replaced —
  what? The chunk lost its own subject

* **Too large:** one relevant sentence arrives with a page of noise

- Overlap between chunks stops a fact being split down the middle

<div class="callout">

There is no universally correct chunk size. It depends on your documents,
and the only way to know is to **measure**.

</div>

---

## Grounding

* The answer is anchored to text you supplied, not to what the model
  half-remembers

* You can **show which text** — the citation

<p class="prompt">Answer using ONLY the context below. If the context does
not contain the answer, say "I don't know".
&#10;
Context: {retrieved chunks}
Question: {question}</p>

---

## What a citation actually is

* Every chunk carries a **label** from the moment it is cut: which document, where

* The label goes into the prompt **beside** the chunk

* The model is asked to repeat the label it used — nothing more

<p class="reply">A variable is like a labeled box that stores information.
[source: introduction_to_programming.txt]</p>

<div class="callout">

The model does not know where text came from. It **copies the label you
attached** — so a citation with no label behind it is an invention.

</div>

---

## Predict: does retrieval eliminate hallucination?

* Yes — the answer comes from real documents now
* No, but it reduces it a lot
* No difference
* It makes it worse

---

## It reduces it. It does not remove it.

- It can **misread** a retrieved chunk
- It can **blend** two chunks into a claim neither made
- If retrieval returns nothing useful, it may answer from training anyway

<div class="callout">

"I don't know" is a rare continuation in training data. If you want it,
you have to **explicitly permit it** — and then check that it does.

</div>

---

## Where it goes wrong

| Failure | Symptom |
|---|---|
| Bad retrieval | Confident answers from irrelevant chunks |
| Chunks too small | Fragments with no context |
| Stale index | Correct answers to last month's question |
| No citation | Nobody can check anything |
| Everything embedded | Slow, expensive, no better |

<span class="kicker">// most "the AI is wrong" reports here are search bugs</span>

---

## What most real systems do now

<div class="flow">
  <div class="step"><span class="n">01</span>Retrieve a generous, bounded set</div>
  <div class="step"><span class="n">02</span>Let a long-context model read all of it</div>
  <div class="step"><span class="n">03</span>Answer with citations</div>
</div>

* Hybrid, not either/or

<div class="callout">

**Agentic retrieval:** your coding assistant does not embed your repo — it
*greps and reads files on demand.* Same problem, solved with search.

</div>

---

<!-- _class: lead -->

<span class="kicker">// break</span>

## Ten minutes

Part 2 answers: *how* can a few hundred numbers hold meaning — and why
does that decide what comes back?

---

## Meaning as coordinates, literally

| Text | Becomes |
|---|---|
| "what is a variable" | 384 numbers (the lab's model; the count is per model): 0.057, 0.04, −0.052, … |
| "A variable is like a labeled box…" | 384 numbers, pointing **almost the same way** |
| "Bubble sort compares neighbours…" | 384 numbers, pointing **somewhere else** |

* Trained so texts that **mean the same** produce arrows pointing the same way

* Nearness = the angle between two arrows, or a distance: **one score per pair**

- No single number means anything alone — the whole list is the meaning

---

## Predict: nothing in the corpus matches

The corpus is five documents about programming. You search for
*"how do I bake sourdough"* with k = 3.

* An empty result — nothing matched
* An error: no relevant chunks
* Three chunks anyway, with worse scores
* One chunk, flagged as a weak match

---

## There is always a nearest neighbour

* Search ranks **every** chunk by distance and returns the top k. Always

* "Relevant" is not a concept the search has — only **closer** and **further**

* The **score** is your only signal, and it is relative, not absolute

- So: set a **threshold**, calibrated on questions with known answers, and treat "nothing above the line" as the answer "nothing"

<div class="callout">

Check which way the score runs before you write a threshold. Some libraries
report a **distance** (lower is closer), others a **similarity** (higher is
closer). Get it backwards and the filter inverts — silently.

</div>

---

## Predict: two embedding models, same length

You embedded every chunk with one model. After an upgrade, queries are
embedded with a **newer** model — same dimensionality, 384 numbers.

* An error — the index rejects the query
* It works, slightly better — the newer model is smarter
* It runs, and the results are nonsense
* It works — meaning is meaning

---

## The space is private to the model

<div class="stack">
  <div class="layer top"><span>Same model for chunks <strong>and</strong> queries — always</span><span class="rank">rule</span></div>
  <div class="layer"><span>Change the model → re-embed <strong>everything</strong>; the old vectors live in a different space</span><span class="rank">cost</span></div>
  <div class="layer untrusted"><span>Mixed spaces: it runs, nothing errors, the results are nonsense</span><span class="rank">failure</span></div>
</div>

* Each model learns its **own axes**; the same length only means the arithmetic runs

* Record which model built the index — the bug looks like "search got worse", not like an error

---

## Where keyword search still wins

| Query looks like | Better tool | Why |
|---|---|---|
| "how do I quit" | **Meaning** search | Wording varies; the idea does not |
| ERR_4021, `max_attempts`, v3.2.1 | **Keyword** search | Exact string; meaning blurs the spelling |
| A name, a code, a path | **Keyword** search | There is only one right match |

* An embedding holds the **gist** of a chunk; the exact spelling is blurred

* Many real systems run **both** and merge the two rankings

---

## A chunk becomes one point

<div class="flow">
  <div class="step danger"><span class="n">too small</span>A precise arrow — at a sentence whose subject is "it"</div>
  <div class="step"><span class="n">about right</span>One topic per chunk: the arrow points at that topic</div>
  <div class="step danger"><span class="n">too large</span>Five topics in one chunk: the arrow points <strong>between</strong> them</div>
</div>

* One vector per chunk, so the vector is the chunk's **average** meaning

* A big chunk can contain the answer and still lose to a chunk that is **only** about it

* A tiny chunk is retrieved precisely — and arrives as a fragment the model cannot interpret

---

## Overlap, drawn

<div class="flow">
  <div class="step"><span class="n">chunk 1</span>words 1 – 200</div>
  <div class="step"><span class="n">chunk 2</span>words 161 – 360</div>
  <div class="step"><span class="n">chunk 3</span>words 321 – 520</div>
</div>

* Each chunk starts **40 words before** the previous one ended

* A fact straddling word 200 is cut in chunk 1 and **whole** in chunk 2

* Without overlap, a sentence split by a seam may be retrievable from **neither** side

- The price: those 40 words are embedded and stored twice — which is why overlap is a fraction of the chunk, not half of it

---

## How you would know

| Chunk size | Found? | What came with it | Answerable? |
|---|---|---|---|
| Small | yes, as a fragment | little | often **no** — "it" has no referent |
| Medium | yes | some | **yes** |
| Large | yes, buried | a page of noise | yes, at a cost — and diluted |

* A handful of questions with **known answers** — and the chunk each one lives in

* Rebuild at several sizes; fill the columns for each

<div class="callout">

Without that table, the chunk size is a **guess with a number on it**. With
it, it is an engineering decision.

</div>

---

## Predict: which question defeats top-3?

Same five programming documents, k = 3.

* "What is a variable?"
* "How can my code remember a number for later?"
* "Which topics do these five documents cover?"
* "How do I bake sourdough?"

---

## Local questions, global questions

| Question | Answer lives in | Top-3 retrieval |
|---|---|---|
| "What is a variable?" | one chunk | fine |
| "How can my code remember a number for later?" | one chunk, other words | fine — embeddings' job |
| "How do I bake sourdough?" | nowhere | fine — the threshold's job |
| "Which topics do these documents cover?" | **every document** | **cannot** — 3 chunks ≠ 5 docs |

* Top-k answers **local** questions. A **global** question needs the whole corpus

- On a corpus that fits the window, the global question is the strongest argument for pasting it

---

## The hybrid, mechanically

<div class="flow">
  <div class="step"><span class="n">01</span>Retrieve <strong>generously</strong>: a large k, cut by a threshold</div>
  <div class="step"><span class="n">02</span>Widen each hit to its section or document</div>
  <div class="step"><span class="n">03</span>One long-context read of the whole set</div>
  <div class="step"><span class="n">04</span>Answer, citing the labels that came along</div>
</div>

* **Bounded** keeps the read where attention is reliable, cost proportional, and the citation set checkable

* **Long-context** is where the joining happens: a fact in one document, a condition in another

- Retrieval finds the pieces. The read is what puts them together

---

## The index is a snapshot

* The vectors were computed **when you built the index**. Editing the document does not touch them

* A stale chunk looks **identical** to a fresh one — the model cannot tell

* Correct, confident answers to **last month's** question

- Re-chunk and re-embed what changed; put a version or date in the chunk's label
- For data that changes by the minute: no index — **search live** at question time

---

## Worked case: a question about a codebase

<p class="prompt">Where is the retry limit for outgoing HTTP requests configured?</p>

<div class="flow">
  <div class="step"><span class="n">01</span>Search the files for a literal: <strong>retry</strong></div>
  <div class="step"><span class="n">02</span>Read the file that matched — the whole file</div>
  <div class="step"><span class="n">03</span>Answer, citing <strong>file and line</strong></div>
</div>

* No index, no embeddings: retrieval is a **loop the agent runs at question time**

* Bounded search, widened read, cited answer — the hybrid in miniature

---

<!-- _class: dense -->

## When the word is not there

```python
# net/http_client.py
MAX_ATTEMPTS = 5          # nobody ever called it a "retry limit"
BACKOFF_SECONDS = 0.5
```

* Searching for **retry** finds nothing. A naive agent reports *there is no retry limit* — confidently wrong: the bad-retrieval failure in a different hat

* A good agent treats an empty search as a **signal**: try *attempt*, *backoff*; read where such a setting would live

<p class="reply">The retry limit is MAX_ATTEMPTS = 5 in net/http_client.py, line 2.
It is spelled "attempts", not "retry", which is why the first search missed it.</p>

---

<!-- _class: dense -->

## Try it now: ground an answer by hand

<p class="prompt">Answer ONLY from the context below. If the context does not contain
the answer, reply exactly: I don't know.
&#10;
Context: Loans last 21 days. An item can be renewed twice unless another
member has reserved it. A lost item is charged at its replacement cost
plus a handling fee.
&#10;
Q1: How many times can I renew a loan?
Q2: What is the handling fee for a lost item?</p>

- **Notice:** the context *mentions* a handling fee and never gives the amount. Does the answer to Q2 come from the context, get invented, or decline?
- Then delete the *If the context does not contain…* sentence and ask both again

---

## What the near miss shows

* Retrieval would have **found the right chunk** — the fee sentence is the closest text

* And the chunk still **does not contain the answer**

* Two different conditions. A grounded system must decline on the second even when the first succeeded

- The off-topic question is the easy test. The **near miss** is the real one — put several in your evaluation set
- If the permission line changed the behaviour, you saw the rare continuation live. If it did not, it still belongs there: behaviour you did not ask for is behaviour you cannot rely on

---

## Common mistakes: building it

* Building a pipeline for a corpus that would **fit in the prompt**

* Chunking without ever measuring whether the size works

- Embedding queries with a **different model** from the chunks — it runs, and the results are nonsense
- Writing a threshold without checking whether the score is a **distance or a similarity**
- Overlap of zero, then wondering why facts at chunk seams are never found

---

## Common mistakes: running it

* Blaming the model when retrieval returned the wrong chunks — look at what was retrieved **first**

* Forgetting the index goes stale

- Asking a **global** question of a top-k system, and reading three chunks as a summary
- Never testing a **near miss** — only the obviously off-topic question
- Having no set of questions with known answers to test against

<span class="kicker">// grounding reduces hallucination; it does not remove it</span>

---

<!-- _class: dense -->

## Summary

- You do not teach the model your data — you **put the right piece in the prompt**
- **Ask first whether you need retrieval.** Small corpus, conversational use → long context wins
- Retrieval earns its place on **scale, cost, freshness, citation**
- Chunk ≈ a paragraph, with overlap, and **measure** it — one arrow per chunk, in a space **private to the model** that made it
- There is **always a nearest neighbour** — the score and its threshold are the only signal
- Top-k answers **local** questions; the **hybrid** is bounded retrieval feeding one long, cited read
- Grounding reduces hallucination; it does not remove it — test the **near miss**

<div class="callout">

Building infrastructure a problem does not need is a commoner and more
expensive mistake than the reverse.

</div>
