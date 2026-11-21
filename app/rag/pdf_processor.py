
from pypdf import PdfReader
from pathlib import Path


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF document.
    """

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    reader = PdfReader(str(pdf_path))

    extracted_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        extracted_text.append(
            f"\n--- Page {page_number} ---\n{text}"
        )

    return "\n".join(extracted_text)
