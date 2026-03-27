from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str):
    """
    Extract text page by page from a PDF.
    Returns a list of dictionaries with page number and text.
    """
    reader = PdfReader(pdf_path)
    pages_data = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        pages_data.append({
            "page_number": page_number,
            "text": text.strip() if text else ""
        })

    return pages_data