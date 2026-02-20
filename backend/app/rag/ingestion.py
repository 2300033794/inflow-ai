from typing import List, Dict, Any

import numpy as np

from app.core.config import DATA_PATH, VECTOR_DB_PATH
from app.core.logging import logger
from app.rag.loader import load_documents
from app.rag.chunker import chunk_documents
from app.rag.embedder import embed_texts
from app.rag.vector_store import create_index, save_index


def run_ingestion(data_path: str = DATA_PATH, store_path: str = VECTOR_DB_PATH) -> Dict[str, Any]:
    """Full ingestion pipeline: load → chunk → embed → store."""
    logger.info("Starting ingestion pipeline...")

    documents = load_documents(data_path)
    if not documents:
        logger.warning("No documents found to ingest.")
        return {"status": "warning", "message": "No documents found.", "chunks_ingested": 0}

    chunks = chunk_documents(documents)
    if not chunks:
        logger.warning("No chunks created.")
        return {"status": "warning", "message": "No chunks created.", "chunks_ingested": 0}

    texts = [chunk["text"] for chunk in chunks]
    logger.info(f"Generating embeddings for {len(texts)} chunks...")
    embeddings: np.ndarray = embed_texts(texts)

    index = create_index(embeddings)
    save_index(index, chunks, store_path=store_path)

    logger.info(f"Ingestion complete. {len(chunks)} chunks stored.")
    return {
        "status": "success",
        "documents_loaded": len(documents),
        "chunks_ingested": len(chunks),
    }
