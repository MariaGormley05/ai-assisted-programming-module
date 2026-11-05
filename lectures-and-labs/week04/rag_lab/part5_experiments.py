"""
Part 5: Experiments -- RAG Lab

Four experiments, in the order the README's DIY 6 and DIY 7 want them:

1. top-k: how much context each k retrieves            (no key needed)
2. chunk size: how to rebuild the index at 50/200/800   (no key needed)
3. long context versus retrieval: the same questions answered from the
   retrieved chunks and from the WHOLE corpus            (key needed)
4. hallucination: a question the corpus cannot answer, asked with no
   context, with the whole corpus, and with retrieval    (key needed)

Run it as:   python part5_experiments.py

Estimated time: 20 minutes
"""

import os

import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from part2_embeddings import load_documents
from part4_generation import GROUNDING_RULES, call_llm, initialize_llm, rag_query

COLLECTION = "cs_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# The same three questions for every experiment, so the answers compare.
QUESTIONS = [
    "What is a variable?",
    "How do linked lists work?",
    "What is HTML?",
]
OUT_OF_CORPUS = "How do I bake sourdough?"


def approx_tokens(text):
    """Words / 0.75 is close enough for English prose."""
    return int(len(text.split()) / 0.75)


def whole_corpus_prompt(question, documents):
    """The same grounding rules as the RAG prompt, over every document at once."""
    labelled = "\n\n".join(f"[source: {name}]\n{text}" for name, text in documents)
    return f"{GROUNDING_RULES}\n\nCONTEXT:\n{labelled}\n\nQUESTION: {question}\n\nANSWER:"


def query_with_whole_corpus(question, llm_client, documents, max_tokens=300):
    """No retrieval step: the model reads everything, labelled by file."""
    return call_llm(llm_client, whole_corpus_prompt(question, documents), max_tokens=max_tokens)


def query_without_context(question, llm_client, max_tokens=300):
    """No context at all: whatever the model believes from training."""
    return call_llm(llm_client, f"Answer this question briefly: {question}", max_tokens=max_tokens)


def show(label, text):
    print(f"  {label}")
    for line in str(text or "(nothing came back - check call_llm and rag_query)").splitlines():
        print(f"     {line}")


def topk_experiment(collection, model):
    print("Experiment 1: how much context does each top-k retrieve?")
    print("-" * 70)
    question = QUESTIONS[0]
    query_embedding = model.encode(question)
    for k in (1, 3, 5):
        results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=k)
        texts = results["documents"][0]
        sources = [m["source"] for m in results["metadatas"][0]]
        words = sum(len(t.split()) for t in texts)
        print(f"  top_k={k}: {len(texts)} chunks, ~{int(words / 0.75)} tokens, from "
              f"{', '.join(dict.fromkeys(sources))}")
    print("  More chunks means more context and more tokens - and past some k, more noise.")
    print()


def chunk_size_note():
    print("Experiment 2: chunk size (DIY 6)")
    print("-" * 70)
    print("  The index is rebuilt by part 2. Run each of these, then part 3, and")
    print("  record in results.md whether the right chunk came back and how much")
    print("  unrelated text came with it:")
    print("     python part2_embeddings.py --chunk-words 50 --overlap-words 20")
    print("     python part2_embeddings.py --chunk-words 200 --overlap-words 20")
    print("     python part2_embeddings.py --chunk-words 800 --overlap-words 20")
    print("  Rebuild at 200 when you are done, so parts 4 and 5 use the setting")
    print("  the README expects.")
    print()


def long_context_vs_retrieval(collection, model, llm_client, documents):
    print("Experiment 3: long context versus retrieval (DIY 7)")
    print("-" * 70)
    corpus = "\n\n".join(text for _, text in documents)
    print(f"  Whole corpus: {len(documents)} documents, ~{approx_tokens(corpus)} tokens - "
          f"it fits in one prompt.")
    print()
    for question in QUESTIONS:
        print(f"Q: {question}")
        rag = rag_query(question, collection, model, llm_client, top_k=3)
        show("RAG (retrieved chunks):", rag.get("answer") if rag else None)
        if rag and rag.get("sources"):
            print(f"     retrieved from: {', '.join(rag['sources'])}")
        show("Whole corpus (no retrieval):", query_with_whole_corpus(question, llm_client, documents))
        print()


def hallucination_test(collection, model, llm_client, documents):
    print("Experiment 4: a question the corpus cannot answer")
    print("-" * 70)
    print(f"Q: {OUT_OF_CORPUS}")
    show("No context at all:", query_without_context(OUT_OF_CORPUS, llm_client))
    show("Whole corpus:", query_with_whole_corpus(OUT_OF_CORPUS, llm_client, documents))
    rag = rag_query(OUT_OF_CORPUS, collection, model, llm_client, top_k=3)
    show("RAG:", rag.get("answer") if rag else None)
    print()
    print("  With no context the model answers from training, confidently. With")
    print("  either kind of grounding it should decline - the permission to say")
    print("  'I don't know' is doing the work, not the retrieval step.")
    print()


def main():
    print("=" * 70)
    print("Part 5: Experiments")
    print("=" * 70)
    print()

    if not os.path.exists("./chroma_db"):
        print("Index not found. Run part2_embeddings.py first.")
        return

    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name=COLLECTION)
    documents = load_documents("data")
    if not documents:
        print("load_documents() returned nothing - finish part 2 first.")
        return

    topk_experiment(collection, model)
    chunk_size_note()

    load_dotenv()
    llm_client = initialize_llm()
    if llm_client is None:
        print("Experiments 3 and 4 need a hosted model and there is no LLM_API_KEY in .env.")
        print("  1. Create a free key at https://aistudio.google.com/apikey")
        print("  2. Copy .env.example to .env in this folder")
        print("  3. Put the key in LLM_API_KEY (leave the base URL and model as they are)")
        return

    long_context_vs_retrieval(collection, model, llm_client, documents)
    hallucination_test(collection, model, llm_client, documents)

    print("=" * 70)
    print("Record the comparison in results.md. The README says what to look for.")
    print("=" * 70)


if __name__ == "__main__":
    main()
