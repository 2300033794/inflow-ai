import json
import os
from typing import List, Dict, Any

import faiss
import numpy as np

from app.core.config import VECTOR_DB_PATH
from app.core.logging import logger

INDEX_FILE = "index.faiss"
METADATA_FILE = "metadata.json"


def _get_paths(store_path: str = VECTOR_DB_PATH):
    os.makedirs(store_path, exist_ok=True)
    return (
        os.path.join(store_path, INDEX_FILE),
        os.path.join(store_path, METADATA_FILE),
    )


def create_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """Create a FAISS flat L2 index from embeddings."""
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    logger.info(f"FAISS index created with {index.ntotal} vectors (dim={dim})")
    return index


def save_index(index: faiss.IndexFlatL2, metadata: List[Dict[str, Any]], store_path: str = VECTOR_DB_PATH) -> None:
    """Persist FAISS index and metadata to disk."""
    idx_path, meta_path = _get_paths(store_path)
    faiss.write_index(index, idx_path)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False)
    logger.info(f"Index saved to {idx_path}, metadata to {meta_path}")


def load_index(store_path: str = VECTOR_DB_PATH):
    """Load FAISS index and metadata from disk. Returns (index, metadata) or (None, [])."""
    idx_path, meta_path = _get_paths(store_path)
    if not os.path.exists(idx_path) or not os.path.exists(meta_path):
        logger.warning("Vector store not found. Run /ingest first.")
        return None, []
    index = faiss.read_index(idx_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    logger.info(f"Index loaded: {index.ntotal} vectors, {len(metadata)} metadata records")
    return index, metadata


def similarity_search(
    index: faiss.IndexFlatL2,
    metadata: List[Dict[str, Any]],
    query_embedding: np.ndarray,
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """Return top-k most similar chunks for a query embedding."""
    query_vec = query_embedding.reshape(1, -1).astype("float32")
    distances, indices = index.search(query_vec, min(top_k, index.ntotal))
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0:
            continue
        record = dict(metadata[idx])
        record["score"] = float(dist)
        results.append(record)
    return results
