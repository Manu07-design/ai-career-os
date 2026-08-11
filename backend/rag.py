import faiss
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer


# --------------------------------------------------
# RESUME KNOWLEDGE STORAGE
# --------------------------------------------------

chunks = []
index = None
vectorizer = None


# --------------------------------------------------
# CHUNKING
# --------------------------------------------------

def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split resume text into overlapping chunks.

    Example:
        chunk 1 -> characters 0-500
        chunk 2 -> characters 400-900
        chunk 3 -> characters 800-1300

    The overlap helps preserve context between chunks.
    """

    text = text.strip()

    if not text:
        return []

    text_chunks = []

    start = 0
    step = chunk_size - overlap

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            text_chunks.append(chunk)

        start += step

    return text_chunks


# --------------------------------------------------
# BUILD VECTOR INDEX
# --------------------------------------------------

def build_vector_store(text):

    global chunks
    global index
    global vectorizer

    # Step 1: Split resume into chunks
    chunks = chunk_text(text)

    if not chunks:
        raise ValueError(
            "Cannot build vector store from empty text."
        )

    # Step 2: Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    # Step 3: Convert chunks into vectors
    embeddings = vectorizer.fit_transform(chunks)

    # Convert sparse matrix to dense float32
    embeddings = embeddings.toarray().astype("float32")

    # --------------------------------------------------
    # Normalize vectors
    # --------------------------------------------------

    faiss.normalize_L2(embeddings)

    # --------------------------------------------------
    # Create FAISS index
    # --------------------------------------------------

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    # --------------------------------------------------
    # Store vectors
    # --------------------------------------------------

    index.add(embeddings)

    return {
        "chunks": len(chunks),
        "embedding_dimension": dimension,
        "vectors_stored": index.ntotal,
        "embedding_model": "TF-IDF"
    }


# --------------------------------------------------
# RETRIEVAL
# --------------------------------------------------

def retrieve_chunks(query, top_k=3):

    if index is None or not chunks:
        raise ValueError(
            "Vector store has not been created yet."
        )

    if vectorizer is None:
        raise ValueError(
            "Vectorizer has not been created yet."
        )

    # --------------------------------------------------
    # Convert query into vector
    # --------------------------------------------------

    query_embedding = vectorizer.transform(
        [query]
    )

    query_embedding = (
        query_embedding
        .toarray()
        .astype("float32")
    )

    # Normalize query vector
    faiss.normalize_L2(query_embedding)

    # --------------------------------------------------
    # Don't request more chunks than available
    # --------------------------------------------------

    k = min(top_k, len(chunks))

    # --------------------------------------------------
    # Search FAISS
    # --------------------------------------------------

    scores, indices = index.search(
        query_embedding,
        k
    )

    # --------------------------------------------------
    # Build results
    # --------------------------------------------------

    results = []

    for score, chunk_index in zip(
        scores[0],
        indices[0]
    ):

        # Ignore invalid FAISS index
        if int(chunk_index) < 0:
            continue

        results.append({
            "chunk": chunks[int(chunk_index)],
            "score": float(score)
        })

    return results