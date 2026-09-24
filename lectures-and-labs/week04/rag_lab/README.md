# AIAP Retrieval Lab

Build a retrieval pipeline by hand — chunk, embed, search, ground — and
then find out whether this corpus needed one at all. Both halves matter.
Building infrastructure a problem does not need is a commoner and more
expensive mistake than the reverse.

## What you'll learn

- Split documents into chunks and turn them into embeddings
- Search by meaning rather than by keyword, and see the difference
- Ground an answer in retrieved text, with a citation
- Measure how chunk size changes what comes back
- Decide, with evidence, when long context beats retrieval outright

## Table of Contents

1. [Chunking and embeddings](#1-chunking-and-embeddings)
2. [Retrieval](#2-retrieval)
3. [Grounding the answer](#3-grounding-the-answer)
4. [Measuring what you built](#4-measuring-what-you-built)
5. [Did you need any of this?](#5-did-you-need-any-of-this)
6. [Common mistakes](#common-mistakes)
7. [Summary](#summary)

## Getting started

1. Open a Codespace on **your own copy** of the module repo.
2. Move into this lab and install its dependencies:

   ```bash
   cd lectures-and-labs/week04/rag_lab
   pip install -r requirements.txt
   ```

3. Check the install. The embedding model downloads on first use (about
   90 MB) and needs no key:

   ```bash
   python check_setup.py
   ```

4. Sections 3 to 5 send the retrieved text to a hosted model, and that
   needs an **API key**. The default is the Gemini API's free tier: create
   a key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
   (a Google account is all it takes), copy `.env.example` to `.env` in
   this folder, and put the key in `LLM_API_KEY`. **Never commit it** —
   `.env` is gitignored and the repo's safety audit will reject it.
   Sections 1 and 2 (chunking, embeddings, retrieval) need no key at all,
   so you can start without one. Any OpenAI-compatible provider works:
   change the base URL and model name in `.env`, nothing in the code.

`data/` holds five short documents about programming topics. They are the
whole corpus, and their size becomes the point in section 5.

---

## 1. Chunking and embeddings

A model cannot search your documents. It can only read what you put in the
prompt. So the first job is turning documents into pieces small enough to
select from, and into numbers you can compare.

### DIY 1: Chunk the corpus

Work in `part2_embeddings.py`.

1. Load all five files from `data/`.
2. Split each into chunks of roughly **200 words**, with about **40 words
   of overlap** between neighbours.
3. Print how many chunks you produced and the length of the shortest and
   longest.
4. Print chunk 0 and chunk 1 and confirm you can see the overlap.

**Expected output**

```text
Loaded 5 documents
Produced 14 chunks (200 words, 40 overlap)
  shortest: 72 words
  longest:  200 words
Overlap check: chunk 1 begins "in half, eliminating the half..." -- those words also sit inside chunk 0: True
```

<details><summary>Hint</summary>

Overlap exists so that a fact sitting on a chunk boundary is not cut in
half. Without it, a sentence split across two chunks may be retrievable
from neither.

Split on words rather than characters — a chunk that ends mid-word embeds
badly and reads worse when it reaches the prompt.

</details>

### DIY 2: Embed and store

1. Embed every chunk and store the vectors alongside their text.
2. Print the dimensionality of one vector.
3. Embed the phrase `"what is a variable"` and print its first five
   numbers.
4. Confirm the query vector has the **same** dimensionality as the chunk
   vectors.

**Expected output**

```text
Embedded 14 chunks
Vector dimensionality: 384
Query vector (first 5): [0.021, -0.114, 0.087, 0.043, -0.009]
Dimensions match: True
```

<details><summary>Hint</summary>

Step 4 is not busywork. Comparing vectors of different dimensionality is
meaningless, and mixing two embedding models in one index is a genuine
and confusing bug — everything "works" and the results are nonsense.

Use the same model for chunks and queries, always.

</details>

---

## 2. Retrieval

### DIY 3: Find the nearest chunks

Work in `part3_retrieval.py`.

1. Complete `semantic_search(query, collection, model, top_k=3)` so it
   returns the `top_k` closest chunks, each with its similarity score and
   the file it came from.
2. Run it for `"what is a variable"`.
3. Run it for `"how do I store a value under a name"` — **different
   words, same meaning**.
4. Compare the two result sets.

**Expected output**

```text
Query: "what is a variable"
  0.81  introduction_to_programming.txt  "A variable is a named location..."
  0.64  data_structures_basics.txt       "Variables can hold references..."

Query: "how do I store a value under a name"
  0.78  introduction_to_programming.txt  "A variable is a named location..."
```

<details><summary>Hint</summary>

Step 3 is the whole justification for embeddings. The second query shares
almost no words with the text it should find — keyword search would return
nothing useful, and meaning-based search returns the same top chunk.

If the two result sets are completely different, check you are embedding
the query with the same model as the chunks.

</details>

### DIY 4: Break it on purpose

1. Search for something **not** in the corpus at all — `"how do I bake
   sourdough"`.
2. Look at what comes back and at the scores.
3. Record what the system does when it has no good answer.

**What you should have**

The returned chunks and their scores, and one sentence on what a retrieval
system does when nothing is relevant.

<details><summary>Hint</summary>

It still returns chunks. Nearest-neighbour search always has a nearest
neighbour — there is no built-in notion of "nothing here is relevant".

The scores are the only signal, which is why a **score threshold** matters
and why the next section has to give the model permission to say it does
not know.

</details>

---

## 3. Grounding the answer

### DIY 5: Answer from retrieved text only

Work in `part4_generation.py`.

1. Build a prompt containing the retrieved chunks and the question.
2. Instruct the model to answer **only** from that context, and to say
   "I don't know" if the answer is not there.
3. Ask a question the corpus answers.
4. Ask the sourdough question again and confirm it declines.
5. Make the answer print **which document** it came from.

**Expected output**

```text
Q: What is a variable?
A: A variable is a named location in memory used to store a value.
   [source: introduction_to_programming.txt]

Q: How do I bake sourdough?
A: I don't know — the provided context does not cover this.
```

<details><summary>Hint</summary>

Step 2's permission is load-bearing. "I don't know" is a rare continuation
in training data, so without explicit permission the most plausible
completion is a confident answer from training — which is precisely the
failure grounding is supposed to prevent.

If it still answers the sourdough question, make the instruction blunter
and put it *after* the context rather than before.

</details>

---

## 4. Measuring what you built

Everything so far had one setting. Now find out whether it was a good one.

### DIY 6: Change the chunk size and measure

Work in `part5_experiments.py`, recording results in `results.md`.

1. Rebuild the index at **50 words**, **200 words**, and **800 words**
   per chunk — part 2 takes the size as an argument. Hold the overlap
   fixed, so you change one thing at a time (left to itself it shrinks
   with small chunks):

   ```bash
   python part2_embeddings.py --chunk-words 50 --overlap-words 20
   ```

2. After each rebuild, run `part3_retrieval.py` and read what comes back
   for its three queries.
3. Record for each size: was the right chunk retrieved, and how much
   irrelevant text came with it?
4. Write one sentence explaining what goes wrong at each extreme.

**What you should have**

A filled table in `results.md`:

```text
| Chunk size | Right chunk found? | Noise | Notes |
|------------|--------------------|-------|-------|
| 50 words   |                    |       |       |
| 200 words  |                    |       |       |
| 800 words  |                    |       |       |
```

<details><summary>Hint</summary>

At 50 words you should see chunks that have lost their own subject — a
fragment saying "it must be declared before use" is useless when you
cannot tell what "it" is.

At 800 you should see the right answer arriving buried in a page of
unrelated text, which costs tokens and dilutes the model's attention.

There is no universally correct size. The answer depends on your
documents, which is why measuring is the skill.

</details>

---

## 5. Did you need any of this?

You have built a working retrieval pipeline. Now find out whether this
problem justified one.

### DIY 7: Skip retrieval entirely

1. Concatenate **all five** documents in `data/` into one string.
2. Count roughly how many tokens that is (words ÷ 0.75 is close enough).
3. Send the whole thing as context with the same questions — **no
   retrieval step at all**. `part5_experiments.py` does exactly this, with
   the same grounding rules your RAG prompt uses, once your part 4 works.
4. Compare each answer with your RAG answer for the same question.
5. Record the comparison in `results.md`.

**What you should have**

```text
## Long context vs retrieval

Whole corpus size: ................. [approx tokens]
Question asked: .................... [your question]
  RAG answer: ...................... [response]
  Whole-corpus answer: ............. [response]
Which was better? .................. [RAG / long context / no difference]
At what corpus size would this flip? [your reasoning]
```

<details><summary>Hint</summary>

**Long context should win on this corpus**, and that is the expected
result, not a failure of your pipeline. Five short documents fit
comfortably in a modern context window, and retrieval can only lose
information that reading everything would have had.

The last line is the real question. Retrieval earns its place on scale,
on cost, on freshness, and when you must cite a source. None of those
apply to five files that fit in the prompt.

</details>

---

## Common mistakes

- **Building a pipeline for a corpus that fits in the prompt.** Ask first.
- **Embedding queries with a different model** from the chunks — silent
  and baffling.
- **Assuming retrieval means relevance.** Nearest-neighbour always returns
  something; the score is your only signal.
- **Forgetting to permit "I don't know"**, then blaming the model for
  making something up.
- **Never measuring chunk size**, so you never learn whether your one
  setting was any good.
- Blaming the model when the retrieval step returned the wrong chunks —
  most "the AI is wrong" reports here are search bugs.

## Summary

- You do not teach a model your documents. You **find the relevant piece
  and put it in the prompt**.
- Embeddings retrieve by **meaning**, so wording that shares no words
  still matches.
- Grounding needs explicit permission to say **"I don't know"**.
- Chunk size is a real parameter with failures at both extremes.
  **Measure it.**
- Retrieval earns its place on **scale, cost, freshness and citation** —
  and on a corpus this size, it does not.
