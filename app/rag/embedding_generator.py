
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional


# Model configuration
MODEL_NAME = "all-MiniLM-L6-v2"

# Load the model only once
_model: Optional[SentenceTransformer] = None


def get_embedding_model() -> SentenceTransformer:
    """
    Load and reuse the sentence transformer model.
    """

    global _model

    if _model is None:
        print(f"Loading embedding model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)
        print("Embedding model loaded successfully!")

    return _model


def generate_embeddings(
    chunks: List[Dict]
) -> List[Dict]:
    """
    Generate embeddings for document chunks.
    """

    if not chunks:
        return []

    model = get_embedding_model()

    texts = [
        chunk["text"]
        for chunk in chunks
        if chunk.get("text", "").strip()
    ]

    if not texts:
        return []

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    embedded_chunks = []
    embedding_index = 0

    for chunk in chunks:

        if not chunk.get("text", "").strip():
            continue

        embedded_chunk = chunk.copy()

        embedded_chunk["embedding"] = (
            embeddings[embedding_index].tolist()
        )

        embedded_chunk["embedding_dimension"] = len(
            embedded_chunk["embedding"]
        )

        embedded_chunks.append(embedded_chunk)

        embedding_index += 1

    return embedded_chunks


def get_embedding_dimension() -> int:
    """
    Return the embedding vector dimension.
    """

    model = get_embedding_model()

    return model.get_embedding_dimension()

def generate_query_embedding(query: str) -> list:
    """
    Convert a user's question into an embedding vector.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    model = get_embedding_model()

    embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding.tolist()

