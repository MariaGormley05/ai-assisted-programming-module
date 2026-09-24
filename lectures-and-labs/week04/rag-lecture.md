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

<!-- Speaker notes: ~0:01. Title. This deck teaches the DECISION before
the pipeline: retrieve, or don't. Most retrieval lectures teach the
pipeline and stop; this one starts from whether a problem needs the
infrastructure at all, because building infrastructure a problem does not
need is a commoner and costlier mistake than the reverse.

Part 1 is the decision and the shape of the pipeline. Part 2 is the
mechanism under it: how a few hundred numbers hold meaning, why chunk
size and overlap change what comes back, and how bounded retrieval and
long-context reasoning fit together. -->

<!-- _class: lead -->

<span class="kicker">// giving it what it does not know</span>

# Retrieval and Grounding

---

<!-- Speaker notes: ~0:02. The hook: a question whose answer is in a
document the model has never seen. The instinct to dislodge is that the
model must be TAUGHT the document, by retraining or fine-tuning. That
instinct dissolves the moment they remember the context window: the model
can read anything you put in front of it. Do not reveal yet; let the room
commit to "train it". -->

## A problem you cannot prompt your way out of

Your company has 40,000 internal documents.

A user asks a question whose answer is in one of them.

* The model has never seen any of them

* How do you get it to answer **correctly**?

---

<!-- Speaker notes: ~0:04. The idea, and the whole two hours in one
sentence: you do not teach the model your documents, you find the relevant
piece and put it in the prompt. It reframes the problem from "teach the
model" to "put the right text in front of it".

The misconception this kills: that answering from private data requires
training. It does not. Training is expensive, slow, and does not update;
retrieval is cheap, instant, and always current. The model is the
reasoning engine and you supply the facts. -->

## The one idea

<div class="callout">

You do not teach the model your documents. You **find the relevant piece
and put it in the prompt.**

</div>

* No retraining. No fine-tuning

* The model is the reasoning engine; **you** supply the facts

---

<!-- Speaker notes: ~0:05. Agenda, naming both halves. Part 1 is the
decision and the shape: whether you need retrieval at all, then chunk,
embed, search, ground, and where it goes wrong. Part 2 is the mechanism
behind each of those: how meaning becomes coordinates, why chunk size and
overlap change what comes back, how bounded retrieval and long-context
reasoning fit together, a second worked case, and a short exercise on
their own laptops. The decision section is what distinguishes this from a
standard pipeline tour. -->

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

<!-- Speaker notes: ~0:07. The decision, and the part most retrieval
lectures skip. Retrieval was invented for a constraint: when it became
popular, context windows held a few thousand tokens and retrieval was the
ONLY way to work with a large document. Windows now hold hundreds of
thousands to millions of tokens, so for many problems the correct
architecture is to paste the whole thing in, with no chunking, no
embeddings and no database to maintain. The misconception here is that
retrieval is a best practice rather than a workaround for a limit that
has largely lifted. -->

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

<!-- Speaker notes: ~0:09. PREDICT beat 1: the decision applied to a small
corpus. Five documents of a few thousand words fit comfortably in a modern
window, and retrieval can only LOSE information a full read would have
had.

The wrong answer to expect is "chunk, embed, and build a vector database":
students have been told RAG is what you do with documents, so they reach
for it reflexively. The faulty model is that RAG is a best practice rather
than a trade-off against a constraint that has largely lifted. A minority
pick "fine-tune", which is the training misconception from the opening
slide surfacing again. -->

## Predict: five short documents, conversational questions

You have five documents, a few thousand words in total. Users ask open
questions about them.

* Chunk, embed, and build a vector database
* Paste all five into the prompt
* Fine-tune a model on them
* Summarise each, then discard the originals

---

<!-- Speaker notes: ~0:12. The reveal and the decision table. This is a
trade-off table, not a ranking: long context wins on a small corpus with
conversational questions; retrieval wins on scale, on freshness, and on
cost at scale. Citation is not retrieval's alone — a full context whose
documents are labelled can be cited too — but retrieval hands you the
source of every answer for free, which is why the row leans that way. The
cost crossover is a rule of thumb, not a constant: around a couple of
thousand pages when this deck was written, and it moves with token
prices, prompt caching and how often the corpus is asked. Quote it as an
order of magnitude, so they have a number to reason with rather than a
vibe.

Students tend to read the table as "retrieval wins four rows to one" and
miss that the first row is the commonest situation they will actually
meet. -->

## It depends — and here is on what

| Situation | Reach for |
|---|---|
| Small corpus, conversational questions | **Long context** — just paste it |
| Too large to fit, or thousands of documents | **Retrieval** |
| You must cite which source said it | **Retrieval** gives it free — a labelled full context can too |
| Data changes constantly | **Retrieval**, or live search |
| Cost matters at scale | **Retrieval** — crossover ≈ a couple of thousand pages, as a rule of thumb |

---

<!-- Speaker notes: ~0:15. The honest limits of "just paste it", so nobody
leaves with the opposite oversimplification. Lost in the middle: models
attend less reliably to material in the middle of a very long context than
at either end. Dilution: marginally relevant text competes with the
relevant part, so adding text can make an answer WORSE. And cost and
latency scale with everything you send. The misconception is that more
tokens means more understanding; a long context is a budget, not a
superpower. -->

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

<!-- Speaker notes: ~0:18. Worked case 1: the opening problem run through
the decision table. 40,000 documents at even a page each is far past the
couple-of-thousand-page crossover, users need to know which document an
answer came from, and the set changes, so this is a retrieval problem on
three rows of the table.

The step students skip is the first one: scoping. A question about the
leave policy needs the handbook, not the 40,000; if the subset a question
actually needs fits the window, paste that subset. Size the corpus a
QUESTION needs, not the corpus the company owns. -->

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

<!-- Speaker notes: ~0:21. The pipeline, now that it has been earned. Five
steps: split into chunks, embed each chunk, embed the question, find the
nearest chunks, put them in the prompt. Only the LAST step involves the
model; steps 1 to 4 are ordinary information retrieval, which is why
retrieval-augmented generation is mostly a search problem wearing an AI
hat, and why most of its failures are search failures. The detail of each
step is part 2's job, and the lab's. -->

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

<!-- Speaker notes: ~0:24. Embeddings, intuition only; the mechanism comes
in part 2. An embedding puts MEANING in space: "car" and "automobile" land
near each other even though they share no letters, which is what keyword
search cannot do and why this works at all.

The misconception to watch for is that search means matching words; the
table's right-hand column is the whole point, and the lab's retrieval
exercise reproduces it with two phrasings of one question. -->

## Embeddings: meaning as coordinates

* A vector of numbers representing **what a piece of text means**

* Similar meanings land **near each other**, whatever words they used

| Query | Keyword search finds | Embedding search finds |
|---|---|---|
| "car maintenance" | documents containing "car" | "vehicle servicing", "auto repair" |
| "how do I quit" | "quit" | "resignation process", "leaving the company" |

---

<!-- Speaker notes: ~0:27. PREDICT beat 2: chunk size, the parameter
students get wrong most often in the lab.

The wrong answer to expect is "one sentence per chunk, maximum precision".
The faulty model treats retrieval as lookup, where a smaller unit is always
a sharper match. In fact a chunk that is too small loses the context that
makes it meaningful: a sentence saying "it must be replaced every 12
months" is useless when you cannot tell what "it" is. Too large and the
relevant sentence is diluted by a page of noise. There is a middle, and
finding it is empirical. -->

## Predict: which chunk size retrieves best?

You split a manual into chunks. Which works best?

* One sentence per chunk — maximum precision
* One paragraph per chunk
* One page per chunk
* The whole document as one chunk

---

<!-- Speaker notes: ~0:30. The reveal: roughly a paragraph, and more
importantly WHY both extremes fail. Too small and the chunk loses its own
subject (the pronoun example). Too large and one relevant sentence arrives
with a page of noise. Overlap between chunks stops a fact being split down
the middle.

Then the honest engineering point: there is no universally correct chunk
size, it depends on the documents, and the only way to know is to measure,
which is what the lab's experiment does at three sizes. Part 2 explains
the mechanism behind both failures. -->

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

<!-- Speaker notes: ~0:33. Grounding: the payoff, and the reason retrieval
is worth the trouble even where long context would also work. Two
properties: the answer is anchored to text you supplied rather than to
what the model half-remembers, and you can SHOW which text.

The prompt on the slide is the shape every grounded system uses: restrict
the answer to the context, and explicitly permit "I don't know". The
permission line looks decorative and is not; the next predict beat is
about it. -->

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

<!-- Speaker notes: ~0:36. What a citation mechanically is: each chunk
carries a label (which document, and where in it) from the moment it is
cut, the label travels into the prompt beside the chunk, and the model is
asked to repeat the label it used. A citation is therefore only as good as
the labelling: the model does not "know" where text came from, it copies
the label you attached.

Citation is the property enterprises actually buy, because it turns "the
AI said" into something a person can check. Students often assume the
model can cite from memory; it cannot, and a citation with no label behind
it is an invention. -->

## What a citation actually is

* Every chunk carries a **label** from the moment it is cut: which document, where

* The label goes into the prompt **beside** the chunk

* The model is asked to repeat the label it used — nothing more

<p class="reply">A variable is a named location in memory used to store a value.
[source: introduction_to_programming.txt]</p>

<div class="callout">

The model does not know where text came from. It **copies the label you
attached** — so a citation with no label behind it is an invention.

</div>

---

<!-- Speaker notes: ~0:39. PREDICT beat 3, the honest one: does retrieval
eliminate hallucination?

The wrong answer to expect is "yes, the answer comes from real documents
now"; it is the claim every vendor makes. The faulty model is that a
hallucination is a missing-fact problem, so supplying the fact must cure
it. Retrieval reduces hallucination substantially and does not eliminate
it: the model can misread a retrieved chunk, blend two chunks, or fall
back on training data when retrieval returns nothing useful. "I don't
know" is a rare continuation in training data, so it needs explicit
permission, which is why the grounding prompt says it out loud. -->

## Predict: does retrieval eliminate hallucination?

* Yes — the answer comes from real documents now
* No, but it reduces it a lot
* No difference
* It makes it worse

---

<!-- Speaker notes: ~0:42. The reveal and the model-side failure modes,
stated specifically because vague warnings do not change behaviour:
misreading a chunk, blending two chunks into a claim neither made, and
answering from training when retrieval returned nothing useful.

The last is the important one: without explicit permission to say "I
don't know", the most plausible continuation of a question is a confident
answer. And permission is not enough on its own; you have to check that
the system actually declines, which is what the lab's off-topic question
is for. -->

## It reduces it. It does not remove it.

- It can **misread** a retrieved chunk
- It can **blend** two chunks into a claim neither made
- If retrieval returns nothing useful, it may answer from training anyway

<div class="callout">

"I don't know" is a rare continuation in training data. If you want it,
you have to **explicitly permit it** — and then check that it does.

</div>

---

<!-- Speaker notes: ~0:46. The operational failures, distinct from the
model failures on the previous slide. Retrieval quality is the one that
surprises people: if step 4 returns the wrong chunks, everything
downstream is confidently wrong, and the system looks like a model problem
when it is a search problem.

The misconception is that a wrong answer means a bad model; here it
usually means a bad search, and the fix is to look at what was retrieved
before touching the prompt. Part 2 puts a mechanism under each row. -->

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

<!-- Speaker notes: ~0:50. The shape most real systems now use, which
resolves the false either/or the lecture opened with: retrieve a generous,
bounded set, let a long-context model read all of it, answer with
citations. Hybrid, not either/or.

Also name agentic retrieval: a coding assistant does not maintain a vector
database of the repository, it searches and reads files on demand, which
is the same problem solved with keyword search instead of embeddings.
Part 2 explains HOW the two halves of the hybrid fit together and walks a
coding-assistant case. -->

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

<!-- Speaker notes: ~0:55. Break. Part 1 gave the decision and the shape
of the pipeline; part 2 explains the mechanism under it: how a list of a
few hundred numbers can hold meaning, why chunk size and overlap change
what comes back, and how bounded retrieval and long-context reasoning fit
together, followed by a second worked case and a short exercise on their
own laptops. Resume at about 1:05. -->

<!-- _class: lead -->

<span class="kicker">// break</span>

## Ten minutes

Part 2 answers: *how* can a few hundred numbers hold meaning — and why
does that decide what comes back?

---

<!-- Speaker notes: ~1:05. Part 2 opens with the mechanism under "meaning
as coordinates". An embedding model reads a piece of text and outputs a
fixed-length list of numbers; the lab's model produces 384 of them. The
model was trained so that texts which mean the same thing produce lists
that point the same way, and unrelated texts point elsewhere. Nearness is
measured as the angle between two such arrows (cosine similarity) or as a
distance; some libraries report a similarity where higher is closer,
others a distance where lower is closer.

The misconception is that the numbers are word counts or keywords in
disguise. They are learned features, and no single number means anything
on its own. -->

## Meaning as coordinates, literally

| Text | Becomes |
|---|---|
| "what is a variable" | 384 numbers (the lab's model; the count is per model): 0.021, −0.114, 0.087, … |
| "A variable is a named location…" | 384 numbers, pointing **almost the same way** |
| "Bubble sort compares neighbours…" | 384 numbers, pointing **somewhere else** |

* Trained so texts that **mean the same** produce arrows pointing the same way

* Nearness = the angle between two arrows, or a distance: **one score per pair**

- No single number means anything alone — the whole list is the meaning

---

<!-- Speaker notes: ~1:08. PREDICT beat 4: what a nearest-neighbour search
returns when nothing in the corpus is relevant. The corpus is the lab's
five programming documents; the query is about baking.

The wrong answer to expect is "an empty result, nothing matched". The
faulty model is the search engine: keyword search returns zero hits when
no document contains the word, so students assume vector search has a
zero too. It does not. Nearest-neighbour search ranks every chunk by
distance and returns the top k, and there is always a nearest chunk;
relevance is not a concept the search has. A smaller group expects an
error, on the same faulty model that something in the system checks
relevance. The only signal is the score, which is why a threshold exists
and why grounding must permit "I don't know". -->

## Predict: nothing in the corpus matches

The corpus is five documents about programming. You search for
*"how do I bake sourdough"* with k = 3.

* An empty result — nothing matched
* An error: no relevant chunks
* Three chunks anyway, with worse scores
* One chunk, flagged as a weak match

---

<!-- Speaker notes: ~1:10. The reveal: three chunks come back, because
nearest-neighbour search always has a nearest neighbour; there is no
built-in notion of "nothing here is relevant". The score is the only
signal, and it is relative: a top score that looks respectable on an
on-topic query may be the same number a junk query gets. So a real system
sets a threshold, calibrated on questions with known answers, and treats
"nothing above the line" as the retrieval result "nothing", which is what
lets the model say "I don't know" instead of grounding in the
least-irrelevant chunk.

Check which direction the library's score runs before writing a
threshold: some report a distance (lower is closer), some a similarity
(higher is closer), and getting it backwards inverts the filter
silently. -->

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

<!-- Speaker notes: ~1:12. PREDICT beat 5: the vector space is private to
the model that produced it. Chunks were embedded with one model; after an
upgrade, queries are embedded with a different model that happens to
produce vectors of the same length.

The wrong answer to expect is "it works; an embedding is an embedding,
meaning is meaning". The faulty model is that the coordinates are
universal, like latitude and longitude, so any model's arrow for
"variable" points the same way. They are not: each model learns its own
axes, and the same dimensionality only means the arithmetic runs without
complaint. A second wrong answer is "an error", on the faulty model that
something type-checks the vectors; nothing does. The lab makes them
confirm dimensionality precisely because the failure is silent. -->

## Predict: two embedding models, same length

You embedded every chunk with one model. After an upgrade, queries are
embedded with a **newer** model — same dimensionality, 384 numbers.

* An error — the index rejects the query
* It works, slightly better — the newer model is smarter
* It runs, and the results are nonsense
* It works — meaning is meaning

---

<!-- Speaker notes: ~1:14. The reveal: it runs and the results are
nonsense. Each model learns its own axes, so a vector from one model is a
set of coordinates in a space the other model has never seen; comparing
them is arithmetic on unrelated numbers, and nothing in the pipeline
checks.

Consequences: one model for chunks AND queries, always; the index is tied
to the model that built it, so changing the model means re-embedding
everything; and record which model built an index, because the failure
looks like "the search got worse" rather than an error. This is the
commonest silent bug in a retrieval system. -->

## The space is private to the model

<div class="stack">
  <div class="layer top"><span>Same model for chunks <strong>and</strong> queries — always</span><span class="rank">rule</span></div>
  <div class="layer"><span>Change the model → re-embed <strong>everything</strong>; the old vectors live in a different space</span><span class="rank">cost</span></div>
  <div class="layer untrusted"><span>Mixed spaces: it runs, nothing errors, the results are nonsense</span><span class="rank">failure</span></div>
</div>

* Each model learns its **own axes**; the same length only means the arithmetic runs

* Record which model built the index — the bug looks like "search got worse", not like an error

---

<!-- Speaker notes: ~1:16. The honest counterpoint to part 1's embeddings
table: keyword search still wins on exact strings. An embedding captures
the gist of a chunk; the exact spelling of an error code, a function name,
a version string or a ticket number is blurred, so a query for one of them
can miss the chunk that contains it verbatim while a plain text match
finds it instantly. Many real systems run both a keyword search and a
vector search and merge the rankings.

This also sets up the second worked case: a coding assistant's search is
keyword search, and it inherits both the strength and the gap. -->

## Where keyword search still wins

| Query looks like | Better tool | Why |
|---|---|---|
| "how do I quit" | **Meaning** search | Wording varies; the idea does not |
| ERR_4021, `max_attempts`, v3.2.1 | **Keyword** search | Exact string; meaning blurs the spelling |
| A name, a code, a path | **Keyword** search | There is only one right match |

* An embedding holds the **gist** of a chunk; the exact spelling is blurred

* Many real systems run **both** and merge the two rankings

---

<!-- Speaker notes: ~1:18. The mechanism under part 1's "a paragraph,
usually". A chunk becomes ONE vector, so the vector is the average meaning
of everything in the chunk. A page-sized chunk about five things points in
a blurred, in-between direction, so a specific question lands closer to a
chunk that is only about that thing; that is why the too-large chunk fails
even when it contains the answer. A one-sentence chunk points precisely,
but at a sentence whose subject is a pronoun, so the vector is precise
about the wrong thing and the model receives a fragment it cannot
interpret.

The misconception is that a larger chunk is "safer" because it contains
more. It contains more and points less accurately. -->

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

<!-- Speaker notes: ~1:20. Overlap, mechanically. Chunks are cut every 200
words, and each chunk starts 40 words before the previous one ended, so
the 40 words at every seam appear in both neighbours; those are the lab's
own settings. A fact that straddles a seam is cut in half in one chunk and
whole in the next, so it is retrievable from at least one of them; without
overlap it may be retrievable from neither. The price is that overlapping
words are embedded and stored twice, which is why overlap is a fraction of
the chunk and not half of it.

Students often see overlap as duplication to be cleaned up. It is the
guarantee that no sentence is only ever seen cut. -->

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

<!-- Speaker notes: ~1:22. How you know a chunk size is right: you measure
it against questions with known answers. Write a handful of questions,
note the chunk each answer lives in, rebuild the index at several sizes,
and for each size record whether the right chunk came back and how much
irrelevant text came with it. That table is the difference between
engineering and guessing, and almost nobody builds it. The lab does
exactly this at three sizes; the slide sets up why, not the steps.

The misconception is that chunk size is a configuration default you
inherit. It is a parameter with failures at both ends, and only a
measurement tells you where your documents sit. -->

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

<!-- Speaker notes: ~1:24. PREDICT beat 6: which question top-k retrieval
cannot answer well, however good the embeddings are. The corpus is the
five programming documents, k = 3.

The wrong answer to expect is "how do I store a value under a name",
picked because it shares no words with the text that answers it. The
faulty model is still keyword matching: students have heard that
embeddings match meaning and not yet believed it. A second group picks
the sourdough question, on the model that hardness means distance from
the corpus; with a threshold that is the EASY case. The hard one is
"which topics do these documents cover", because the answer needs every
document and the search returns three chunks. Hardness is how much of the
corpus the answer needs, and no ranking fixes a question that needs all
of it. -->

## Predict: which question defeats top-3?

Same five programming documents, k = 3.

* "What is a variable?"
* "How do I store a value under a name?"
* "Which topics do these five documents cover?"
* "How do I bake sourdough?"

---

<!-- Speaker notes: ~1:26. The reveal: the global question. Top-k
retrieval answers LOCAL questions, where the answer lives in one place or
a few; a question about the whole corpus needs the whole corpus, and three
chunks cannot summarise five documents whatever their scores. The synonym
question is exactly what embeddings are for; the sourdough question is
what the threshold is for.

This is the structural limit that produces the hybrid: bounded retrieval
for local questions, and either a whole-corpus read or a two-stage summary
for global ones. When the corpus is small enough to paste, the global
question is the strongest argument for pasting it. -->

## Local questions, global questions

| Question | Answer lives in | Top-3 retrieval |
|---|---|---|
| "What is a variable?" | one chunk | fine |
| "How do I store a value under a name?" | one chunk, other words | fine — embeddings' job |
| "How do I bake sourdough?" | nowhere | fine — the threshold's job |
| "Which topics do these documents cover?" | **every document** | **cannot** — 3 chunks ≠ 5 docs |

* Top-k answers **local** questions. A **global** question needs the whole corpus

- On a corpus that fits the window, the global question is the strongest argument for pasting it

---

<!-- Speaker notes: ~1:28. How the hybrid's two halves fit together.
Retrieval is BOUNDED: a generous k with a threshold, so the set is bigger
than three chunks and never the whole corpus. Each hit is then widened to
its neighbourhood, typically the section or document it came from, so the
model sees whole thoughts rather than fragments. The long-context model
reads the union in one prompt, which is where cross-referencing happens:
joining a fact from one document to a condition in another, noticing that
two chunks disagree. Every piece keeps its label, so the answer can cite.

The bound is what keeps the read inside the range where attention is
reliable, keeps cost proportional to the question, and keeps the citation
set small enough to check. The long read is what single-chunk answers
never had. -->

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

<!-- Speaker notes: ~1:30. Freshness, mechanically. The index is a
snapshot: the vectors were computed when you built it, and editing a
document does not touch them. A stale chunk looks exactly like a fresh one
to the model, which is how a system gives a correct answer to last month's
question with full confidence. So: re-chunk and re-embed what changed,
carry a version or date in the chunk's label so the answer can say how old
its source is, and for anything that changes by the minute skip the index
and search live at question time.

The misconception is that retrieval is "always current" because it reads
real documents. It reads the documents as they were when indexed. -->

## The index is a snapshot

* The vectors were computed **when you built the index**. Editing the document does not touch them

* A stale chunk looks **identical** to a fresh one — the model cannot tell

* Correct, confident answers to **last month's** question

- Re-chunk and re-embed what changed; put a version or date in the chunk's label
- For data that changes by the minute: no index — **search live** at question time

---

<!-- Speaker notes: ~1:32. Worked case 2, different in kind from the
document corpus: a question about a codebase, answered by a coding
assistant that can run a search and read files. There is no index and no
embedding; retrieval is a LOOP the agent runs at question time: search for
a literal, read the file that matched, answer with a file and line as the
citation. This is the hybrid in miniature: a bounded search (the hits), a
widened read (the whole file), and a long-context answer with a citation.

The point for students is that agentic retrieval is retrieval, with
keyword search doing the job embeddings do in the pipeline, and inheriting
keyword search's strength: exact identifiers. -->

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

<!-- Speaker notes: ~1:34. The case continued, at the point where keyword
search fails: the code never uses the word "retry". A search for the
literal returns nothing, and a naive agent reports that there is no retry
limit, which is confidently wrong in exactly the way part 1's
bad-retrieval row describes. A good agent treats an empty search as a
signal and iterates: try the synonyms ("attempt", "backoff"), or read the
file where such a setting would plausibly live. Meaning search would
have found it first time; keyword search needs the right word.

The lesson is the mirror image of the embeddings table: every retrieval
method has a gap, and a system that iterates on its own retrieval closes
it. -->

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

<!-- Speaker notes: ~1:35. TRY IT NOW, five to eight minutes, on their own
laptops with whatever assistant they have; no code and no pipeline. They
ground an answer by hand: paste a three-sentence context and two
questions, one the context answers and one it only appears to. The
handling-fee question is the trap: the context mentions a fee, so the
nearest text is relevant, but the amount is not there. That is the gap
between "found the right chunk" and "the chunk contains the answer", and
it is where a grounded system must decline. Then they remove the
permission sentence and ask again.

The instruction to observe is deliberately neutral: watch whether the
second answer comes from the context, is invented, or is a decline, and
whether the permission line changes that. Do not tell them what will
happen; models differ, and the point is to look. -->

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

<!-- Speaker notes: ~1:41. Debrief, framed as mechanism rather than as a
prediction of what each model did. The handling-fee question is a near
miss: retrieval would have found the right chunk, because the fee sentence
is the closest text, and the chunk still does not contain the answer.
"Found the right chunk" and "the chunk answers the question" are different
conditions, and a grounded system has to decline on the second even when
the first succeeded. The obviously off-topic question is the easy test;
the near miss is the real one, and an evaluation set should contain
several.

If removing the permission line changed the behaviour, that is the "I
don't know is a rare continuation" point seen live. If it did not, the
instruction still belongs there, because behaviour you did not ask for is
behaviour you cannot rely on. -->

## What the near miss shows

* Retrieval would have **found the right chunk** — the fee sentence is the closest text

* And the chunk still **does not contain the answer**

* Two different conditions. A grounded system must decline on the second even when the first succeeded

- The off-topic question is the easy test. The **near miss** is the real one — put several in your evaluation set
- If the permission line changed the behaviour, you saw the rare continuation live. If it did not, it still belongs there: behaviour you did not ask for is behaviour you cannot rely on

---

<!-- Speaker notes: ~1:42. Common mistakes when building, extended with
part 2's mechanisms. The first is the one the whole lecture is arranged to
prevent: building a pipeline for a corpus that would fit in the prompt.
Then: chunking without measuring; mixing embedding models across chunks
and queries, which fails silently; reading the score in the wrong
direction when writing a threshold; and zero overlap. Each of these is a
search bug that will be reported as a model bug. -->

## Common mistakes: building it

* Building a pipeline for a corpus that would **fit in the prompt**

* Chunking without ever measuring whether the size works

- Embedding queries with a **different model** from the chunks — it runs, and the results are nonsense
- Writing a threshold without checking whether the score is a **distance or a similarity**
- Overlap of zero, then wondering why facts at chunk seams are never found

---

<!-- Speaker notes: ~1:43. Common mistakes when running it, and the honest
limits. Blaming the model when retrieval returned the wrong chunks;
forgetting the index goes stale; asking a global question of a top-k
system and treating the fragments it returns as a summary; testing only
the obviously off-topic question and never a near miss; and having no set
of questions with known answers, which is the difference between
engineering and guessing and the one almost nobody builds.

The limit to be honest about: grounding reduces hallucination and does
not remove it, and the near miss is where that shows. -->

## Common mistakes: running it

* Blaming the model when retrieval returned the wrong chunks — look at what was retrieved **first**

* Forgetting the index goes stale

- Asking a **global** question of a top-k system, and reading three chunks as a summary
- Never testing a **near miss** — only the obviously off-topic question
- Having no set of questions with known answers to test against

<span class="kicker">// grounding reduces hallucination; it does not remove it</span>

---

<!-- Speaker notes: ~1:45. Summary and close. Return to the opening
problem, 40,000 documents: they can now answer it, including the part
where they check whether 40,000 is really the number a question needs.
Part 1's takeaways are the decision and the shape; part 2's are the
mechanisms: one arrow per chunk in a space private to the model, always a
nearest neighbour so the score and its threshold are the only signal,
local versus global questions, and the hybrid as bounded retrieval feeding
one long read. Leave the callout up for questions. -->

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
