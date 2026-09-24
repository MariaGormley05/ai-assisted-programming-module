"""
Part 3: Retrieval -- RAG Lab

In this part, you will:
1. Implement semantic search over the chunks you stored in part 2
2. Show each hit with its score and the file it came from
3. Filter hits by a score threshold
4. Fit the winning chunks into a context window

Run it as:   python part3_retrieval.py

Estimated time: 35 minutes
"""

import chromadb
from sentence_transformers import SentenceTransformer

COLLECTION = "cs_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def semantic_search(query, collection, model, top_k=3):
    """
    Return the top_k chunks nearest in meaning to the query.

    Args:
        query: The question, as a string
        collection: ChromaDB collection from part 2
        model: SentenceTransformer model -- the SAME one part 2 used
        top_k: Number of results to return

    Returns:
        List of (chunk_text, source, similarity) tuples, best first.
        ChromaDB reports a DISTANCE (lower is closer); convert it with
        similarity = 1 / (1 + distance) so that higher means closer.
    """
    # TODO: Exercise 3.1
    # 1. query_embedding = model.encode(query)
    # 2. results = collection.query(
    #        query_embeddings=[query_embedding.tolist()],
    #        n_results=top_k
    #    )
    # 3. Pull out, for each hit:
    #      results['documents'][0]   -> the chunk texts
    #      results['metadatas'][0]   -> dicts with the 'source' filename
    #      results['distances'][0]   -> distances (lower = closer)
    # 4. Return [(text, source, 1 / (1 + distance)), ...]
    #
    # GitHub Copilot Prompt: "Query a ChromaDB collection with an embedding and return text, metadata source and similarity for the top k hits"

    # YOUR CODE HERE
    pass  # Remove this line when you add your code


def filter_by_relevance(results, min_similarity=0.5):
    """
    Keep only the hits whose similarity clears a threshold.

    Args:
        results: List of (chunk_text, source, similarity) tuples
        min_similarity: Lowest similarity worth keeping

    Returns:
        The filtered list, same tuple shape

    Nearest-neighbour search ALWAYS returns something (DIY 4). The score is
    the only signal that nothing relevant was found, and this threshold is
    where you act on it.
    """
    # TODO: Exercise 3.2
    # Return the tuples whose similarity >= min_similarity
    #
    # GitHub Copilot Prompt: "Filter a list of (text, source, score) tuples by a minimum score"

    # YOUR CODE HERE
    pass  # Remove this line when you add your code


def manage_context_window(results, max_tokens=1500):
    """
    Join chunk texts into one context string that fits a token budget.

    Args:
        results: List of (chunk_text, source, similarity) tuples, best first
        max_tokens: Approximate budget (4 characters is roughly 1 token)

    Returns:
        One string: the chunks that fit, each prefixed with its source and
        separated by a blank line and a rule
    """
    # TODO: Exercise 3.3
    # 1. Start with an empty list of pieces
    # 2. For each hit, build "[source: <file>]\n<text>"
    # 3. Add it only if the total length in characters // 4 stays within max_tokens
    # 4. Join the pieces with "\n\n---\n\n" and return the string
    #
    # GitHub Copilot Prompt: "Combine labelled text chunks with separators while staying within a token budget"

    # YOUR CODE HERE
    pass  # Remove this line when you add your code


def display_results(query, results):
    """Print hits the way the README shows them: score, source, preview."""
    print(f'Query: "{query}"')
    if not results:
        print("  no results -- check your semantic_search() function")
        return
    for text, source, similarity in results:
        preview = " ".join(text.split()[:6])
        print(f'  {similarity:.2f}  {source:<34} "{preview}..."')


def main():
    """Run retrieval against the index from part 2."""
    print("=" * 70)
    print("Part 3: Retrieval")
    print("=" * 70)
    print()

    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        collection = client.get_collection(name=COLLECTION)
    except Exception:
        print("Collection not found. Run part2_embeddings.py first.")
        return
    print(f"Connected to collection with {collection.count()} chunks")
    print()

    # DIY 3: same meaning, different words. DIY 4: nothing relevant at all.
    queries = [
        "what is a variable",
        "how do I store a value under a name",
        "how do I bake sourdough",
    ]

    for query in queries:
        results = semantic_search(query, collection, model, top_k=3)
        display_results(query, results)
        if results:
            kept = filter_by_relevance(results, min_similarity=0.5)
            if kept is not None:
                print(f"  kept after threshold 0.50: {len(kept)} of {len(results)}")
            context = manage_context_window(results, max_tokens=500)
            if context:
                print(f"  context window: ~{len(context) // 4} tokens")
        print()

    print("=" * 70)
    print("Part 3 complete. Next: python part4_generation.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
