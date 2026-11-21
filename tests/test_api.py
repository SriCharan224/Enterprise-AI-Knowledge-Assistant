
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)


# Test 1: Health check endpoint
def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200


# Test 2: Root endpoint
def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200


# Test 3: Document count endpoint
def test_document_count():
    response = client.get("/documents/count")

    assert response.status_code == 200


# Test 4: Document count response structure
def test_document_count_response():
    response = client.get("/documents/count")

    data = response.json()

    assert "total_stored_chunks" in data
    assert isinstance(data["total_stored_chunks"], int)


# Test 5: Document search endpoint
def test_document_search():
    response = client.post(
        "/documents/search",
        params={
            "query": "What is this document about?",
            "top_k": 3
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "query" in data
    assert "total_results" in data
    assert "results" in data


# Test 6: Empty search query
def test_empty_search_query():
    response = client.post(
        "/documents/search",
        params={
            "query": "",
            "top_k": 3
        }
    )

    assert response.status_code in [200, 422, 500]
from pathlib import Path


def test_pdf_upload():
    pdf_files = list(Path("data/documents").glob("*.pdf"))

    assert pdf_files, "No sample PDF found in data/documents"

    pdf_path = pdf_files[0]

    with open(pdf_path, "rb") as pdf:
        response = client.post(
            "/documents/upload",
            files={
                "file": (
                    pdf_path.name,
                    pdf,
                    "application/pdf"
                )
            }
        )

    assert response.status_code == 200
def test_ai_chat(monkeypatch):
    import app.api.main as main

    # Mock document retrieval
    monkeypatch.setattr(
        main,
        "retrieve_documents",
        lambda query, top_k: [
            {
                "text": "The company was founded in 2020.",
                "filename": "sample.pdf",
                "distance": 0.1
            }
        ]
    )

    # Mock AI answer generation
    monkeypatch.setattr(
        main,
        "generate_answer",
        lambda query, context: "The company was founded in 2020."
    )

    response = client.post(
        "/chat",
        params={
            "query": "When was the company founded?",
            "top_k": 3
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data
    assert data["answer"] == "The company was founded in 2020."