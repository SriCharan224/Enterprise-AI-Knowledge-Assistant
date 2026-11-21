
from fastmcp import FastMCP
from app.rag.retrieval import retrieve_documents
from app.core.chroma_store import get_collection_count
from app.rag.answer_generator import generate_answer

mcp = FastMCP(
    name="Enterprise AI Knowledge Assistant"
)


@mcp.tool()
def health_check() -> str:
    """Check whether the MCP server is running."""
    return "Enterprise AI Knowledge Assistant MCP server is running."
@mcp.tool()
def search_documents(query: str, top_k: int = 3) -> list:
    """Search for relevant information in uploaded documents."""
    return retrieve_documents(query=query, top_k=top_k)
@mcp.tool()
def get_document_count() -> int:
    """Get the total number of document chunks stored."""
    return get_collection_count()
@mcp.tool()
def ask_knowledge_base(query: str, top_k: int = 3) -> str:
    """Answer a question using information from uploaded documents."""
    results = retrieve_documents(query=query, top_k=top_k)

    if not results:
        return "I could not find relevant information in your documents."

    context = "\n\n".join(result["text"] for result in results)

    return generate_answer(query=query, context=context)


if __name__ == "__main__":
    mcp.run()
