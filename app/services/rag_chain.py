from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from app.services.vector_store import load_chroma_vectorstore

_tokenizer = None
_model = None


def get_generator():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        model_name = "google/flan-t5-base"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    return _tokenizer, _model


def format_sources(results):
    formatted_sources = []

    for doc in results:
        formatted_sources.append({
            "source": doc.metadata.get("source", "Unknown"),
            "page_number": doc.metadata.get("page_number", "N/A"),
            "chunk_id": doc.metadata.get("chunk_id", "N/A")
        })

    return formatted_sources


def generate_rag_answer(question: str, k: int = 3):
    vectorstore = load_chroma_vectorstore()
    results = vectorstore.similarity_search(question, k=k)

    if not results:
        return {
            "answer": "I could not find relevant information in the uploaded PDF.",
            "sources": []
        }

    context_parts = [doc.page_content for doc in results]
    context = "\n\n".join(context_parts)
    sources = format_sources(results)

    prompt = f"""
You are a helpful AI assistant.

Answer the question only from the provided context.
Do not add outside knowledge.
Keep the answer clear, natural, and concise.
If the answer is not present in the context, say:
"The answer is not available in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    tokenizer, model = get_generator()

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=180
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "answer": answer.strip(),
        "sources": sources
    }