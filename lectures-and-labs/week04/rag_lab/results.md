# RAG Lab - results

**Name:** _[Your name]_
**Date:** _[Date]_

Fill this in as you go. The README says what each section is for.

---

## Part 1: chunking and embeddings (DIY 1 and 2)

- Documents loaded: ___
- Chunks produced at 200 words: ___ (shortest ___ words, longest ___ words)
- Vector dimensionality: ___
- Did the query vector have the same dimensionality as the chunks? ___

_What did the overlap check show?_

---

## Part 2: retrieval (DIY 3 and 4)

**"what is a variable"** - top hit, score and source: ___

**"how do I store a value under a name"** - top hit, score and source: ___

_Same meaning, different words: did both queries find the same chunk?_

**"how do I bake sourdough"** - what came back, and with what scores: ___

_One sentence on what a retrieval system does when nothing is relevant:_

---

## Part 3: grounding (DIY 5)

**Q:** What is a variable?
**A:** ___
**Source it cited:** ___

**Q:** How do I bake sourdough?
**A:** ___ (did it decline?)

---

## Part 4: chunk size (DIY 6)

| Chunk size | Right chunk found? | Noise | Notes |
|------------|--------------------|-------|-------|
| 50 words   |                    |       |       |
| 200 words  |                    |       |       |
| 800 words  |                    |       |       |

_One sentence on what goes wrong at each extreme:_

---

## Part 5: long context versus retrieval (DIY 7)

```text
Whole corpus size: ................. [approx tokens]
Question asked: .................... [your question]
  RAG answer: ...................... [response]
  Whole-corpus answer: ............. [response]
Which was better? .................. [RAG / long context / no difference]
At what corpus size would this flip? [your reasoning]
```

Repeat for each of the three questions if the answers differed.

**The question the corpus cannot answer** (sourdough):

- No context: ___
- Whole corpus: ___
- RAG: ___

_Which of the three declined, and what made the difference?_

---

## Reflection

_When would you build retrieval, and when would you just paste everything?_

_What surprised you?_
