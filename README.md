# RAG PDF Chat Project

An AI-powered PDF chatbot built with Python, FastAPI, Hugging Face, and ChromaDB. This project allows users to upload PDF documents, process them into semantic chunks, store embeddings in a vector database, and ask natural language questions to receive document-grounded answers.

## Features

- Upload PDF documents through FastAPI
- Extract text page by page from PDFs
- Split text into smaller semantic chunks
- Generate embeddings using Hugging Face models
- Store embeddings in ChromaDB
- Perform semantic search over uploaded PDFs
- Generate concise answers from retrieved context
- Return source references with page number and chunk ID
- Prevent duplicate storage for the same PDF

## Tech Stack

- Python
- FastAPI
- Hugging Face Transformers
- Sentence Transformers
- ChromaDB
- LangChain
- PyPDF

## Project Structure

```bash
rag-pdf-chat/
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── upload.py
│   │   └── query.py
│   ├── services/
│   │   ├── pdf_loader.py
│   │   ├── text_splitter.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── rag_chain.py
│   ├── models/
│   └── utils/
├── data/
│   ├── uploads/
│   └── chroma_db/
├── requirements.txt
├── .env
└── README.md