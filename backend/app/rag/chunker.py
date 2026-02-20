from typing import List, Dict, Any

from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP
from app.core.logging import logger


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping token-approximate chunks using word boundaries."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def chunk_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Chunk all documents and return a flat list of chunk records."""
    chunks = []
    for doc in documents:
        doc_chunks = split_into_chunks(doc["text"])
        for idx, chunk_text in enumerate(doc_chunks):
            chunks.append({
                "source": doc["source"],
                "chunk_id": idx,
                "text": chunk_text,
            })
    logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
    return chunks
