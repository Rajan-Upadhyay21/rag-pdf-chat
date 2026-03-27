from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.query import router as query_router

app = FastAPI(
    title="RAG PDF Chat Project",
    description="Chat with PDF documents using RAG, FastAPI, ChromaDB, and Hugging Face",
    version="1.0.0"
)

app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(query_router, prefix="/api", tags=["Query"])


@app.get("/")
def home():
    return {"message": "RAG PDF Chat API is running successfully"}