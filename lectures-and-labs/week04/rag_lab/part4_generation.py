"""
Part 4: Generation -- RAG Lab

In this part, you will:
1. Connect to a hosted model through an OpenAI-compatible API
2. Build a grounded prompt from retrieved chunks
3. Complete the pipeline: retrieve, augment, generate
4. Return the answer together with the documents it came from

Run it as:   python part4_generation.py

Estimated time: 30 minutes
"""

import os

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

COLLECTION = "cs_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# The generation half talks to a hosted model through the OpenAI-compatible
# API that most providers now offer, so the provider is a setting, not code.
# .env supplies three values (see .env.example): the key, the base URL and
# the model name. The defaults point at the Gemini API's free tier.
DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEFAULT_MODEL = "gemini-3.5-flash-lite"

# The grounding instruction. The permission to say "I don't know" is
# load-bearing (see the README): without it the most plausible completion
# is a confident answer from training data, which is the failure grounding
# exists to prevent.
GROUNDING_RULES = (
    "Answer the question using ONLY the context below. "
    "If the context does not contain the answer, reply exactly: "
    "I don't know - the provided context does not cover this. "
    "Finish your answer with the document you used, in square brackets, "
    "like [source: introduction_to_programming.txt]."
)


def llm_settings():
    """Return (api_key, base_url, model) from .env, with the defaults above."""
    load_dotenv()
    return (os.getenv("LLM_API_KEY"),
            os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL),
            os.getenv("LLM_MODEL", DEFAULT_MODEL))


def initialize_llm():
    """
    Initialize the client for the hosted model.

    Returns:
        OpenAI client object, or None when no key is set
    """
    # TODO: Exercise 4.1
    # 1. Get the key, base URL and model name from llm_settings()
    # 2. If there is no key, return None -- the rest of the lab then runs
    #    retrieval only and skips generation
    # 3. Create and return an OpenAI client pointed at that base URL
    #
    # Usage:
    # api_key, base_url, model = llm_settings()
    # if not api_key:
    #     return None
    # client = OpenAI(api_key=api_key, base_url=base_url)
    #
    # GitHub Copilot Prompt: "Create an OpenAI client with a custom base_url from environment settings"

    # YOUR CODE HERE
    pass  # Remove this line when you add your code


def build_rag_prompt(query, context_chunks):
    """
    Build a grounded prompt from the retrieved chunks and the question.

    Args:
        query: The question
        context_chunks: List of (chunk_text, source) pairs, best first

    Returns:
        The prompt string
    """
    # TODO: Exercise 4.2
    # Build a prompt that:
    # 1. States GROUNDING_RULES
    # 2. Lists every chunk, each prefixed "[source: <file>]" so the model can
    #    say which document it used
    # 3. Puts the question after the context
    #
    # Template structure:
    #
    #   <GROUNDING_RULES>
    #
    #   CONTEXT:
    #   [source: <file>]
    #   <chunk text>
    #
    #   [source: <file>]
    #   <chunk text>
    #
    #   QUESTION: <query>
    #
    #   ANSWER:
    #
    # GitHub Copilot Prompt: "Build a RAG prompt with grounding rules, source-labelled context chunks and the question"

    # YOUR CODE HERE
    pass  # Remove this line when you add your code


def call_llm(client, prompt, max_tokens=500):
    """
    Call the hosted model with the given prompt.

    Args:
        client: OpenAI client (from initialize_llm)
        prompt: The formatted prompt
        max_tokens: Maximum tokens in the response

    Returns:
        Generated response text
    """
    # TODO: Part of Exercise 4.3
    # Call the chat completions API to generate a response
    #
    # Usage:
    # _, _, model = llm_settings()
    # response = client.chat.completions.create(
    #     model=model,
    #     max_tokens=max_tokens,
    #     messages=[
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    # return response.choices[0].message.content
    #
    # GitHub Copilot Prompt: "Call an OpenAI-compatible chat completions API with a prompt"

    # YOUR CODE HERE
    pass  # Remove this line when you add your code


def rag_query(question, collection, embedding_model, llm_client, top_k=3):
    """
    Complete RAG pipeline: retrieve, augment, generate.

    Args:
        question: The question
        collection: ChromaDB collection
        embedding_model: SentenceTransformer model -- the same one as part 2
        llm_client: OpenAI client, or None to retrieve without generating
        top_k: Number of chunks to retrieve

    Returns:
        dict with 'answer' (str or None), 'sources' (list of filenames,
        best first, no repeats) and 'context_used' (list of chunk texts)
    """
    # TODO: Exercise 4.3 - Complete RAG Pipeline
    #
    # Step 1: Retrieve
    # - query_embedding = embedding_model.encode(question)
    # - results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=top_k)
    # - texts = results['documents'][0]
    # - sources = [m['source'] for m in results['metadatas'][0]]
    #
    # Step 2: Augment
    # - prompt = build_rag_prompt(question, list(zip(texts, sources)))
    #
    # Step 3: Generate
    # - answer = call_llm(llm_client, prompt) if llm_client else None
    #
    # Step 4: Return
    # - {'answer': answer, 'sources': <sources without repeats>, 'context_used': texts}
    #
    # GitHub Copilot Prompt: "Implement a RAG pipeline: embed the question, query ChromaDB, build a prompt from the hits, call the model, return the answer with its sources"

    # YOUR CODE HERE
    pass  # Remove this line when you add your code


def test_rag_system():
    """Ask the questions DIY 5 names, and show the answer with its source."""
    print("=" * 70)
    print("Part 4: Generation")
    print("=" * 70)
    print()

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        collection = client.get_collection(name=COLLECTION)
        print(f"Found {collection.count()} chunks in the index")
    except Exception:
        print("Index not found. Run part2_embeddings.py first.")
        return

    llm_client = initialize_llm()
    if llm_client is None:
        print("No LLM_API_KEY in .env - retrieval will run, generation is skipped.")
        print("Copy .env.example to .env and add a free key (the README says where).")
    print()

    questions = [
        "What is a variable?",
        "How do linked lists work?",
        "How do I bake sourdough?",   # not in the corpus: the model must decline
    ]

    for question in questions:
        try:
            result = rag_query(question, collection, embedding_model, llm_client, top_k=3)
        except Exception as e:
            print(f"Error processing question: {e}")
            print("Check your implementation and try again")
            print()
            continue
        if not result:
            print(f"Q: {question}")
            print("   rag_query() returned nothing - check your implementation")
            print()
            continue
        print(f"Q: {question}")
        print(f"A: {result.get('answer') or '(no key set - retrieval only)'}")
        sources = result.get("sources") or []
        print(f"   retrieved from: {', '.join(sources) if sources else 'nothing'}")
        print()

    print("=" * 70)
    print("Part 4 complete. Next: python part5_experiments.py")
    print("=" * 70)


def interactive_mode():
    """Ask your own questions."""
    print("\n" + "=" * 70)
    print("Interactive mode - type a question, or 'quit'")
    print("=" * 70)

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name=COLLECTION)
    llm_client = initialize_llm()

    while True:
        question = input("\nQ: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue
        try:
            result = rag_query(question, collection, embedding_model, llm_client)
            if result:
                print(f"A: {result['answer']}")
                print(f"   retrieved from: {', '.join(result.get('sources') or [])}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    test_rag_system()

    # Uncomment for interactive mode:
    # interactive_mode()
