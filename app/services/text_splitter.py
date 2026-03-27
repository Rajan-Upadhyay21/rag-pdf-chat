from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_pdf_pages(pages_data, chunk_size=500, chunk_overlap=100):
    """
    Split extracted PDF page text into smaller chunks.
    Keeps page number metadata for each chunk.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunked_documents = []

    for page in pages_data:
        page_number = page["page_number"]
        text = page["text"]

        if not text.strip():
            continue

        chunks = splitter.split_text(text)

        for i, chunk in enumerate(chunks):
            chunked_documents.append({
                "page_number": page_number,
                "chunk_id": i + 1,
                "text": chunk
            })

    return chunked_documents