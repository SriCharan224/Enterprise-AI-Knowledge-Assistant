
from pathlib import Path
import uuid
import chromadb


# Persistent database directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma"

CHROMA_DIR.mkdir(parents=True, exist_ok=True)


# Initialize ChromaDB
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


# Create or retrieve collection
collection = client.get_or_create_collection(
    name="enterprise_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def store_embeddings(chunks, embeddings, filename):
    """
    Store document chunks and their embeddings in ChromaDB.
    """

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks and embeddings must match"
        )

    if not chunks:
        raise ValueError("No document chunks to store")

    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]

    metadatas = [
        {
            "filename": filename,
            "chunk_index": index
        }
        for index in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=[
            [float(value) for value in embedding]
            for embedding in embeddings
        ],
        metadatas=metadatas
    )

    return {
        "stored_chunks": len(chunks),
        "collection": "enterprise_knowledge"
    }


def get_collection_count():
    """
    Return total stored document chunks.
    """

    return collection.count()
# --------------------------------------------------
# Search Similar Documents
# --------------------------------------------------

def search_similar_chunks(query_embedding, top_k=3):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    return results