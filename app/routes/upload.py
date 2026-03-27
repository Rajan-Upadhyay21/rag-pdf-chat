import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_splitter import chunk_pdf_pages
from app.services.vector_store import store_chunks_in_chroma

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    pages_data = extract_text_from_pdf(file_path)
    chunks = chunk_pdf_pages(pages_data)
    store_result = store_chunks_in_chroma(chunks, file.filename)

    return {
        "message": "PDF processed successfully",
        "filename": file.filename,
        "total_pages": len(pages_data),
        "total_chunks": len(chunks),
        "storage_status": store_result["status"],
        "storage_message": store_result["message"]
    }