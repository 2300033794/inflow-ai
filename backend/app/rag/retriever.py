from typing import List, Dict, Any

from app.core.config import TOP_K
from app.core.logging import logger
from app.rag.embedder import embed_query
from app.rag.vector_store import load_index, similarity_search


def retrieve(query: str, top_k: int = TOP_K) -> List[Dict[str, Any]]:
    """Retrieve the top-k most relevant chunks for a query."""
    index, metadata = load_index()
    if index is None:
        logger.warning("No index available. Returning empty results.")
        return []
    query_embedding = embed_query(query)
    results = similarity_search(index, metadata, query_embedding, top_k=top_k)
    logger.info(f"Retrieved {len(results)} chunks for query: '{query[:60]}...'")
    return results
