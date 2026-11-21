
from app.rag.embedding_generator import generate_query_embedding
from app.core.chroma_store import search_similar_chunks


def retrieve_documents(query: str, top_k: int = 3):
    """
    Retrieve relevant document chunks for a user query.
    """

    query_embedding = generate_query_embedding(query)

    results = search_similar_chunks(
        query_embedding=query_embedding,
        top_k=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved_chunks = []

    for document, metadata, distance in zip(
        documents, metadatas, distances
    ):
        retrieved_chunks.append({
            "text": document,
            "filename": metadata.get("filename"),
            "distance": distance
        })

    return retrieved_chunks
