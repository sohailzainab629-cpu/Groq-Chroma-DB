
from typing import Dict, List

from .config import settings


def chunk_text(
    text: str,
    chunk_size: int,
    overlap: int,
) -> List[str]:

    if not text.strip():
        return []

    chunks: List[str] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        if end < text_length:
            search_start = max(
                start + int(chunk_size * 0.65),
                start,
            )

            candidate = text.rfind(
                "\n",
                search_start,
                end,
            )

            if candidate == -1:
                candidate = text.rfind(
                    " ",
                    search_start,
                    end,
                )

            if candidate > start:
                end = candidate

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = max(end - overlap, start + 1)

    return chunks


def chunk_documents(
    documents: List[Dict],
) -> List[Dict]:

    all_chunks: List[Dict] = []

    chunk_size = settings.chunk_size
    overlap = settings.chunk_overlap

    for document in documents:
        text = document.get("text", "")

        source = document.get(
            "source",
            "unknown",
        )

        page = document.get("page", 0)

        text_chunks = chunk_text(
            text=text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for index, chunk in enumerate(text_chunks):
            all_chunks.append(
                {
                    "text": chunk,
                    "source": source,
                    "page": page,
                    "chunk": index,
                }
            )

    return all_chunks
