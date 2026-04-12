RAG PDF Chat — Retrieval-Augmented Generation for Intelligent Document Q&A

An end-to-end AI-powered document intelligence system that enables natural language interaction with PDF documents through semantic retrieval and context-grounded answer generation.


Overview
RAG PDF Chat is a production-grade, retrieval-augmented generation (RAG) pipeline built to bridge the gap between static document storage and dynamic, conversational AI. Rather than relying on a language model's parametric memory alone, this system grounds every response in evidence retrieved directly from user-uploaded PDFs — delivering accurate, traceable, and context-aware answers at scale.
The architecture follows a strict separation of concerns: document ingestion, semantic chunking, vector embedding, similarity-based retrieval, and response synthesis are each handled by dedicated, modular service layers. This design ensures maintainability, extensibility, and clean integration across the full retrieval-to-generation pipeline.
Whether querying a 200-page legal contract, a dense research paper, or a technical manual, RAG PDF Chat returns precise answers anchored to specific passages — complete with page-level source attribution and chunk traceability.

Key Features

PDF Ingestion via REST API — Upload documents programmatically through a FastAPI endpoint; files are validated, deduplicated, and routed to the processing pipeline automatically.
Page-Level Text Extraction — Leverages PyPDF to extract raw text content page by page, preserving document structure and enabling granular source attribution downstream.
Semantic Chunking — Long-form text is split into semantically coherent, overlapping chunks using a configurable splitter, optimized to preserve contextual continuity across chunk boundaries.
Dense Vector Embedding — Each chunk is transformed into a high-dimensional semantic embedding using state-of-the-art Sentence Transformer models from Hugging Face, capturing deep linguistic meaning beyond surface-level keyword matching.
Persistent Vector Storage with ChromaDB — Embeddings are indexed and persisted in ChromaDB, a high-performance vector database purpose-built for similarity search. Collections are organized per document for efficient, isolated retrieval.
Semantic Similarity Search — At query time, the user's question is embedded and matched against stored vectors using cosine similarity, surfacing the most contextually relevant passages regardless of exact wording.
Context-Grounded Answer Generation — Retrieved chunks are assembled into a structured prompt context and passed to a language model, which synthesizes a concise, faithful answer derived exclusively from document content.
Source Attribution & Traceability — Every response is accompanied by structured source metadata including the originating page number, chunk identifier, and relevance score — enabling full answer provenance tracking.
Duplicate Detection & Idempotent Ingestion — A document fingerprinting mechanism prevents redundant re-processing and duplicate vector entries when the same PDF is uploaded more than once.
Modular, Extensible Architecture — Each stage of the pipeline — loading, splitting, embedding, retrieval, and generation — is encapsulated as an independent service, making it straightforward to swap models, vector stores, or retrieval strategies without systemic refactoring.


System Architecture
The system is organized around a clean unidirectional data flow:
PDF Upload (FastAPI)
        │
        ▼
Text Extraction (PyPDF)          ← page-by-page parsing
        │
        ▼
Semantic Chunking (LangChain)    ← configurable chunk size + overlap
        │
        ▼
Embedding Generation             ← Sentence Transformers (Hugging Face)
        │
        ▼
Vector Indexing (ChromaDB)       ← persistent similarity index
        │
        ▼
Query Embedding                  ← same embedding model applied to query
        │
        ▼
Semantic Retrieval               ← cosine similarity search over index
        │
        ▼
Context Assembly + LLM Synthesis ← grounded answer generation
        │
        ▼
Structured Response              ← answer + page references + chunk IDs

Tech Stack
LayerTechnologyPurposeAPI FrameworkFastAPIHigh-performance async REST endpoints for upload and queryPDF ParsingPyPDFPage-level text extraction from PDF documentsChunking & OrchestrationLangChainText splitting, prompt templating, and chain orchestrationEmbedding ModelsHugging Face Transformers + Sentence TransformersDense semantic vector generationVector DatabaseChromaDBPersistent embedding storage and similarity retrievalLanguage ModelHugging Face Inference / OpenAI-compatibleContext-grounded answer synthesisRuntimePython 3.10+Core application runtime

Project Structure
bashrag-pdf-chat/
├── app/
│   ├── main.py                  # FastAPI application entry point, middleware, router registration
│   ├── routes/
│   │   ├── upload.py            # POST /upload — PDF ingestion, validation, and pipeline trigger
│   │   └── query.py             # POST /query — semantic search and answer generation endpoint
│   ├── services/
│   │   ├── pdf_loader.py        # Page-level text extraction using PyPDF
│   │   ├── text_splitter.py     # Configurable semantic chunking with overlap control
│   │   ├── embeddings.py        # Sentence Transformer embedding generation + caching
│   │   ├── vector_store.py      # ChromaDB collection management, upsert, and similarity search
│   │   └── rag_chain.py         # End-to-end RAG orchestration — retrieval, context assembly, generation
│   ├── models/                  # Pydantic request/response schemas for API validation
│   └── utils/                   # Shared utilities — hashing, logging, config loading
├── data/
│   ├── uploads/                 # Temporary storage for uploaded PDF files
│   └── chroma_db/               # Persistent ChromaDB vector index storage
├── requirements.txt             # Pinned Python dependencies
├── .env                         # Environment variables — API keys, model paths, config
└── README.md

Getting Started
Prerequisites

Python 3.10 or higher
pip package manager
(Optional) GPU with CUDA support for accelerated embedding generation

Installation
bash# Clone the repository
git clone https://github.com/Rajan-Upadhyay21/rag-pdf-chat.git
cd rag-pdf-chat

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
Configuration
Create a .env file in the root directory and configure the following variables:
envEMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./data/chroma_db
UPLOAD_DIR=./data/uploads
LLM_MODEL=your-model-name-or-api-endpoint
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=5
Running the Application
bash# Start the FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API documentation available at:
# http://localhost:8000/docs      (Swagger UI)
# http://localhost:8000/redoc     (ReDoc)

API Reference
Upload a PDF Document
httpPOST /upload
Content-Type: multipart/form-data
ParameterTypeDescriptionfileFilePDF document to ingest (multipart upload)
Response:
json{
  "status": "success",
  "document_id": "a3f9c2...",
  "pages_extracted": 42,
  "chunks_indexed": 187,
  "message": "Document successfully ingested and indexed."
}

Query a Document
httpPOST /query
Content-Type: application/json
json{
  "question": "What are the key findings in section 3?",
  "document_id": "a3f9c2...",
  "top_k": 5
}
Response:
json{
  "answer": "The key findings in section 3 indicate that...",
  "sources": [
    {
      "page": 14,
      "chunk_id": "a3f9c2_chunk_031",
      "relevance_score": 0.923,
      "excerpt": "The analysis reveals..."
    }
  ]
}

How RAG Works — Pipeline Deep Dive
Ingestion Phase:
When a PDF is uploaded, the system extracts raw text page by page, then applies a sliding-window chunking strategy that splits content into overlapping segments. Overlap is deliberately maintained to prevent contextual information from being severed at chunk boundaries. Each chunk is then encoded into a dense vector representation using a pre-trained Sentence Transformer model and persisted to ChromaDB under a document-scoped collection.
Retrieval Phase:
At query time, the natural language question undergoes the same embedding transformation as the document chunks — ensuring the query and document content exist in a shared semantic vector space. ChromaDB performs a cosine similarity search over the indexed embeddings, retrieving the top-K most semantically relevant chunks irrespective of exact keyword overlap.
Generation Phase:
The retrieved chunks are injected into a structured prompt template alongside the original question, forming a grounded context window. The language model synthesizes a response anchored exclusively to this retrieved context, substantially reducing hallucination and ensuring answer fidelity to the source document.

Roadmap

 Multi-document cross-retrieval — query across multiple indexed PDFs simultaneously
 Hybrid retrieval — combine dense semantic search with sparse BM25 keyword matching for improved recall
 Streaming response generation — token-by-token answer streaming via Server-Sent Events
 Conversational memory — multi-turn dialogue with session-scoped chat history
 Document metadata filtering — filter retrieval by author, date range, or custom tags
 Frontend interface — React-based chat UI with drag-and-drop PDF upload
 Docker Compose deployment — containerized multi-service setup for production environments


Author
Rajan M Upadhyay
MS Computer Science — Roosevelt University
LinkedIn · GitHub · rajanupadhyay2121@gmail.com
