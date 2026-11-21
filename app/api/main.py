
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil

# RAG imports
from app.rag.text_chunker import chunk_text
from app.rag.retrieval import retrieve_documents
from app.rag.answer_generator import generate_answer
from app.rag.pdf_processor import extract_text_from_pdf
from app.rag.embedding_generator import (
    generate_embeddings,
    get_embedding_dimension
)

# ChromaDB import
from app.core.chroma_store import (
    store_embeddings,
    get_collection_count
)

# --------------------------------------------------
# Initialize FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Enterprise AI Knowledge Assistant",
    description="An intelligent RAG and MCP powered knowledge assistant",
    version="1.0.0"
)


# --------------------------------------------------
# Document storage directory
# --------------------------------------------------

DOCUMENT_DIR = Path("data/documents")
DOCUMENT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Enterprise AI Knowledge Assistant!",
        "status": "Running successfully"
    }


# --------------------------------------------------
# Health check endpoint
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "Enterprise AI Knowledge Assistant"
    }


# --------------------------------------------------
# About endpoint
# --------------------------------------------------

@app.get("/about")
def about():
    return {
        "project": "Enterprise AI Knowledge Assistant",
        "technology": [
            "Python",
            "FastAPI",
            "RAG",
            "ChromaDB",
            "MCP"
        ],
        "version": "1.0.0"
    }


# --------------------------------------------------
# PDF Upload and RAG Processing
# --------------------------------------------------

@app.post("/documents/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Validate file
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_path = DOCUMENT_DIR / Path(file.filename).name

    try:

        # Step 1: Save uploaded PDF
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 2: Extract text from PDF
        extracted_text = extract_text_from_pdf(
            str(file_path)
        )

        if not extracted_text or not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the PDF"
            )

        # Step 3: Split extracted text into chunks
        chunks = chunk_text(
            extracted_text,
            chunk_size=1000,
            chunk_overlap=200
        )

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks generated from PDF"
            )

        # Step 4: Generate embeddings
        embedded_chunks = generate_embeddings(chunks)

        if not embedded_chunks:
            raise HTTPException(
                status_code=400,
                detail="Embedding generation failed"
            )

        # Step 5: Get embedding dimension
        embedding_dimension = get_embedding_dimension()

        # Step 6: Extract document text
        document_chunks = [
            chunk["text"]
            for chunk in embedded_chunks
        ]

        # Step 7: Extract numerical embedding vectors
        embedding_vectors = [
            chunk["embedding"]
            for chunk in embedded_chunks
        ]

        # Step 8: Store embeddings in ChromaDB
        storage_result = store_embeddings(
            document_chunks,
            embedding_vectors,
            file.filename
        )

        # Step 9: Return successful response
        return {
            "message": "PDF processed and embeddings stored successfully",
            "filename": file.filename,
            "characters_extracted": len(extracted_text),
            "total_chunks": len(chunks),
            "embedded_chunks": len(embedded_chunks),
            "stored_chunks": storage_result["stored_chunks"],
            "embedding_dimension": embedding_dimension,
            "collection": storage_result["collection"]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        await file.close()
# --------------------------------------------------
# ChromaDB Collection Count
# --------------------------------------------------

@app.get("/documents/count")
def document_count():

    try:
        total_chunks = get_collection_count()

        return {
            "collection": "enterprise_knowledge",
            "total_stored_chunks": total_chunks,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.post("/documents/search")
def search_documents(query: str, top_k: int = 3):
    try:
        results = retrieve_documents(query=query, top_k=top_k)

        return {
            "query": query,
            "total_results": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/chat")
def chat_with_documents(query: str, top_k: int = 3):
    try:
        # Retrieve relevant document chunks
        results = retrieve_documents(query=query, top_k=top_k)

        if not results:
            return {
                "query": query,
                "answer": "I could not find relevant information in your documents.",
                "sources": []
            }

        # Combine retrieved chunks into context
        context = "\n\n".join(
            result["text"] for result in results
        )

        # Generate answer using Gemini
        answer = generate_answer(
            query=query,
            context=context
        )

        return {
            "query": query,
            "answer": answer,
            "sources": [
                result["filename"] for result in results
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))