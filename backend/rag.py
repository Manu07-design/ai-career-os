import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# EMBEDDING MODEL
# --------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# These will temporarily store our resume knowledge
chunks = []
index = None


# --------------------------------------------------
# CHUNKING
# --------------------------------------------------

def chunk_text(text, chunk_size=500, overlap=100):

    text = text.strip()

    if not text:
        return []

    text_chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        text_chunks.append(chunk)

        start += chunk_size - overlap

    return text_chunks


# --------------------------------------------------
# BUILD VECTOR INDEX
# --------------------------------------------------

def build_vector_store(text):

    global chunks
    global index

    # Step 1: Split resume
    chunks = chunk_text(text)

    if not chunks:
        raise ValueError("Cannot build vector store from empty text.")

    # Step 2: Convert chunks into embeddings
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    # Step 3: Determine embedding dimension
    dimension = embeddings.shape[1]

    # Step 4: Create FAISS index
    index = faiss.IndexFlatIP(dimension)

    # Step 5: Store vectors
    index.add(embeddings)

    return {
        "chunks": len(chunks),
        "embedding_dimension": dimension,
        "vectors_stored": index.ntotal
    }


# --------------------------------------------------
# SEMANTIC RETRIEVAL
# --------------------------------------------------

def retrieve_chunks(query, top_k=3):

    if index is None or not chunks:
        raise ValueError(
            "Vector store has not been created yet."
        )

    # Convert question into embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    # Don't request more chunks than we have
    k = min(top_k, len(chunks))

    # Search FAISS
    scores, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for score, chunk_index in zip(
        scores[0],
        indices[0]
    ):

        results.append({
            "chunk": chunks[int(chunk_index)],
            "score": float(score)
        })

    return results