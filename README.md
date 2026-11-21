
# 🤖 Enterprise AI Knowledge Assistant

An AI-powered enterprise document assistant built using Retrieval-Augmented Generation (RAG), FastAPI, ChromaDB, Google Gemini, MCP, and Streamlit.

The application allows users to upload PDF documents, retrieve relevant information using semantic search, and generate context-aware answers using an LLM.

## 🚀 Features

- PDF document upload and processing
- Automatic text extraction and chunking
- Semantic embeddings using Sentence Transformers
- Vector storage using ChromaDB
- Similarity-based document retrieval
- AI-powered question answering using Google Gemini
- FastAPI backend with REST endpoints
- MCP server with four tools
- Interactive Streamlit frontend
- Automated API testing using Pytest

## 🏗️ Architecture

```text
                 User
                  |
                  v
          Streamlit Frontend
                  |
                  v
             FastAPI
                  |
          +-------+-------+
          |               |
          v               v
     PDF Processing   AI Chat
          |               |
          v               v
     Text Chunking    Retrieval
          |               |
          v               v
     Embeddings      ChromaDB
          |               |
          +-------+-------+
                  |
                  v
             Google Gemini
                  |
                  v
             AI Answer
```

MCP Server exposes knowledge-base functionality through independent tools.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend API |
| Streamlit | Frontend interface |
| ChromaDB | Vector database |
| Sentence Transformers | Text embeddings |
| Google Gemini | AI answer generation |
| FastMCP | Model Context Protocol server |
| PyPDF | PDF text extraction |
| Pytest | Automated testing |

## 📂 Project Structure

```text
Enterprise_Ai_Knowledge_Assistant/
│
├── app/
│   ├── api/
│   │   └── main.py
│   ├── core/
│   │   └── chroma_store.py
│   ├── mcp/
│   │   └── server.py
│   └── rag/
│       ├── pdf_processor.py
│       ├── text_chunker.py
│       ├── embedding_generator.py
│       ├── retrieval.py
│       └── answer_generator.py
│
├── data/
│   ├── documents/
│   └── chroma/
│
├── frontend/
│   └── app.py
│
├── tests/
│   └── test_api.py
│
├── evaluation/
├── scripts/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Enterprise_Ai_Knowledge_Assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never commit your `.env` file to GitHub.

### 6. Start the FastAPI backend

```bash
python -m uvicorn app.api.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### 7. Start the Streamlit frontend

Open another terminal:

```bash
streamlit run frontend/app.py
```

### 8. Start the MCP server

Open another terminal:

```bash
python -m app.mcp.server
```

The MCP server uses STDIO transport and can be connected to an MCP-compatible client.

## 🔧 MCP Tools

The MCP server provides four tools:

| Tool | Description |
|---|---|
| health_check | Checks MCP server status |
| search_documents | Searches relevant document chunks |
| get_document_count | Returns stored document chunk count |
| ask_knowledge_base | Generates answers from document context |

## 🧪 Running Tests

Run automated tests using:

```bash
python -m pytest tests/ -v
```

The test suite covers API health, root endpoint, document count, document search, PDF upload, and AI chat behavior.

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| GEMINI_API_KEY | Google Gemini API key |

## 🎯 Project Objective

The goal of this project is to build an intelligent enterprise knowledge assistant that makes information stored in PDF documents searchable and accessible through natural-language questions.

## 👨‍💻 Author

**Your Name**

AI / Machine Learning Project

## 📌 Future Improvements

- Document duplicate detection
- User authentication and authorization
- Support for multiple document formats
- Advanced RAG evaluation
- Conversation history persistence
- Deployment to a cloud platform
