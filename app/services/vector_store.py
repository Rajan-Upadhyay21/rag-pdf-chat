import os
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from app.services.embeddings import get_embedding_function

CHROMA_DIR = "data/chroma_db"
COLLECTION_NAME = "pdf_chunks"

os.makedirs(CHROMA_DIR, exist_ok=True)


def get_vectorstore():
    embedding_function = get_embedding_function()
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_function
    )


def store_chunks_in_chroma(chunks, filename: str):
    vectorstore = get_vectorstore()

    existing = vectorstore.get(where={"source": filename})

    if existing and existing.get("ids"):
        return {
            "status": "already_exists",
            "message": f"{filename} is already stored in ChromaDB."
        }

    documents = []
    ids = []

    for chunk in chunks:
        chunk_id = f"{filename}_page{chunk['page_number']}_chunk{chunk['chunk_id']}"
        ids.append(chunk_id)

        documents.append(
            Document(
                page_content=chunk["text"],
                metadata={
                    "source": filename,
                    "page_number": chunk["page_number"],
                    "chunk_id": chunk["chunk_id"]
                }
            )
        )

    vectorstore.add_documents(documents=documents, ids=ids)

    return {
        "status": "stored",
        "message": f"{filename} stored successfully in ChromaDB."
    }


def load_chroma_vectorstore():
    return get_vectorstore()