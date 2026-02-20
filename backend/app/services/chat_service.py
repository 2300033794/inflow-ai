from typing import Dict, Any

from app.rag.generator import generate_answer
from app.core.logging import logger


async def process_chat(query: str) -> Dict[str, Any]:
    """Process a chat query and return the answer with sources."""
    logger.info(f"Processing chat query: '{query[:80]}'")
    result = generate_answer(query)
    return result
