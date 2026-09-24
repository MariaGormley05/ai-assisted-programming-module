"""
Part 2: Document Processing & Embeddings -- RAG Lab

In this part, you will:
1. Load documents from the data directory
2. Split each one into overlapping chunks of WORDS
3. Generate vector embeddings
4. Store the chunks, their embeddings and the file each came from in ChromaDB

Run it as:   python part2_embeddings.py

DIY 6 rebuilds the index at other chunk sizes (each run replaces the index):
             python part2_embeddings.py --chunk-words 50
             python part2_embeddings.py --chunk-words 800

Estimated time: 30 minutes
"""

import argparse
import os

import chromadb
from sentence_transformers import SentenceTransformer

DEFAULT_CHUNK_WORDS = 200
DEFAULT_OVERLAP_WORDS = 40
COLLECTION = "cs_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_documents(data_dir="data"):
    """
    Load all .txt files from the data directory.

    Args:
        data_dir: Path to directory containing text files

    Returns:
        List of (filename, content) tuples, sorted by filename
    """
    documents = []

    # TODO: Exercise 2.1
    # Use sorted(os.listdir(data_dir)) to get the files in a stable order
    # Keep only the .txt files
    # Read each file and append a (filename, content) tuple to documents
    #
    # Hints:
    # - Use os.path.join() to create full file paths
    # - Use .endswith('.txt') to filter for text files
    # - Use 'with open(filepath, 'r', encoding='utf-8')' to read files
    #
    # GitHub Copilot Prompt: "Read all text files from a directory and return a sorted list of (filename, content) tuples"

    # YOUR CODE HERE
    pass  # Remove this line when you add your code

    return documents


def chunk_text(text, chunk_words=DEFAULT_CHUNK_WORDS, overlap_words=DEFAULT_OVERLAP_WORDS):
    """
    Split text into overlapping chunks of roughly chunk_words WORDS.

    Args:
        text: The full document text
        chunk_words: Words per chunk (default 200)
        overlap_words: Words shared between neighbouring chunks (default 40)

    Returns:
        List of text chunks (strings)
    """
    chunks = []

    # TODO: Exercise 2.2
    # Split on words, not characters: a chunk that ends mid-word embeds
    # badly and reads worse when it reaches the prompt.
    #
    # Algorithm:
    # 1. words = text.split()
    # 2. start = 0; step = chunk_words - overlap_words
    # 3. Take words[start:start + chunk_words], join them with spaces, append
    # 4. If that slice reached the end of the words, stop
    # 5. Otherwise move start forward by step and repeat
    #
    # The overlap is why a fact sitting on a chunk boundary is still
    # retrievable from at least one chunk.
    #
    # GitHub Copilot Prompt: "Split text into overlapping chunks of N words with M words of overlap"

    # YOUR CODE HERE
    pass  # Remove this line when you add your code

    return chunks


def generate_embeddings(chunks, model_name=EMBEDDING_MODEL):
    """
    Generate vector embeddings for text chunks.

    Args:
        chunks: List of text chunks
        model_name: Name of the sentence-transformer model

    Returns:
        numpy array of embedding vectors, one row per chunk
    """
    print(f"Loading embedding model: {model_name}...")

    # TODO: Exercise 2.3
    # 1. Load the SentenceTransformer model using model_name
    # 2. Use model.encode() to generate embeddings for all chunks
    # 3. Return the embeddings
    #
    # Note: model.encode() takes a list of strings and returns all embeddings at once
    #
    # GitHub Copilot Prompt: "Use sentence-transformers to encode a list of text chunks"

    # YOUR CODE HERE
    pass  # Remove this line when you add your code


def store_in_chromadb(chunks, embeddings, sources, collection_name=COLLECTION):
    """
    Store chunks, their embeddings and the file each came from in ChromaDB.

    Args:
        chunks: List of text chunks
        embeddings: Embedding vectors, one per chunk
        sources: List of filenames, one per chunk, in the same order
        collection_name: Name for the ChromaDB collection

    Returns:
        ChromaDB collection object
    """
    # TODO: Exercise 2.4
    # 1. client = chromadb.PersistentClient(path="./chroma_db")
    # 2. Delete the collection if it already exists (wrap in try/except),
    #    so every run starts fresh -- DIY 6 depends on that
    # 3. collection = client.create_collection(name=collection_name)
    # 4. collection.add(
    #        documents=chunks,
    #        embeddings=embeddings.tolist(),
    #        metadatas=[{"source": s} for s in sources],
    #        ids=[f"chunk_{i}" for i in range(len(chunks))]
    #    )
    #
    # The metadata is what lets part 3 show where a hit came from and part 4
    # say which document an answer used. Drop it and citation is impossible.
    #
    # GitHub Copilot Prompt: "Store text chunks, embeddings and per-chunk metadata in a ChromaDB collection"

    # YOUR CODE HERE
    pass  # Remove this line when you add your code


def main():
    """Run the complete Part 2 pipeline."""
    parser = argparse.ArgumentParser(description="Build the chunk index for the RAG lab.")
    parser.add_argument("--chunk-words", type=int, default=DEFAULT_CHUNK_WORDS,
                        help=f"words per chunk (default {DEFAULT_CHUNK_WORDS})")
    parser.add_argument("--overlap-words", type=int, default=None,
                        help=f"words shared between neighbours (default {DEFAULT_OVERLAP_WORDS}, "
                             f"or a fifth of --chunk-words when that is smaller)")
    args = parser.parse_args()
    overlap = (args.overlap_words if args.overlap_words is not None
               else min(DEFAULT_OVERLAP_WORDS, args.chunk_words // 5))

    print("=" * 70)
    print("Part 2: Document Processing & Embeddings")
    print("=" * 70)
    print()

    # Step 1: Load documents
    documents = load_documents("data")
    if not documents:
        print("No documents loaded. Check your load_documents() function.")
        return
    print(f"Loaded {len(documents)} documents")
    for filename, _ in documents:
        print(f"   - {filename}")
    print()

    # Step 2: Chunk documents, remembering which file each chunk came from
    all_chunks = []
    sources = []
    for filename, content in documents:
        chunks = chunk_text(content, chunk_words=args.chunk_words, overlap_words=overlap)
        all_chunks.extend(chunks)
        sources.extend([filename] * len(chunks))

    if not all_chunks:
        print("No chunks created. Check your chunk_text() function.")
        return

    lengths = [len(c.split()) for c in all_chunks]
    print(f"Produced {len(all_chunks)} chunks ({args.chunk_words} words, {overlap} overlap)")
    print(f"  shortest: {min(lengths)} words")
    print(f"  longest:  {max(lengths)} words")
    if len(all_chunks) > 1:
        opening = " ".join(all_chunks[1].split()[:5])
        print(f'Overlap check: chunk 1 begins "{opening}..." -- those words also sit '
              f'inside chunk 0: {opening in all_chunks[0]}')
    print()

    # Step 3: Generate embeddings
    embeddings = generate_embeddings(all_chunks)
    if embeddings is None:
        print("No embeddings generated. Check your generate_embeddings() function.")
        return
    print(f"Embedded {len(embeddings)} chunks")
    print(f"Vector dimensionality: {len(embeddings[0])}")

    query_vector = SentenceTransformer(EMBEDDING_MODEL).encode("what is a variable")
    print(f"Query vector (first 5): {[round(float(x), 3) for x in query_vector[:5]]}")
    print(f"Dimensions match: {len(query_vector) == len(embeddings[0])}")
    print()

    # Step 4: Store in ChromaDB
    collection = store_in_chromadb(all_chunks, embeddings, sources)
    if collection is None:
        print("Failed to create collection. Check your store_in_chromadb() function.")
        return
    print(f"Stored {collection.count()} chunks in ./chroma_db (collection '{COLLECTION}')")
    print()

    print("=" * 70)
    print("Part 2 complete. Next: python part3_retrieval.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
