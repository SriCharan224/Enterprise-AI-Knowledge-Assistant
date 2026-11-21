
from typing import List, Dict


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Dict]:

    """
    Split extracted document text into overlapping chunks.
    """

    if not text or not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be non-negative "
            "and smaller than chunk_size"
        )

    chunks = []

    start = 0
    text_length = len(text)
    chunk_index = 0

    while start < text_length:

        end = min(start + chunk_size, text_length)

        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "chunk_id": chunk_index,
                "text": chunk,
                "start_index": start,
                "end_index": end
            })

            chunk_index += 1

        if end == text_length:
            break

        start = end - chunk_overlap

    return chunks
