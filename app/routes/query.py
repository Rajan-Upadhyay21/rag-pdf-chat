from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_chain import generate_rag_answer

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    result = generate_rag_answer(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }