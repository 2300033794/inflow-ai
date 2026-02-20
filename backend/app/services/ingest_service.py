from typing import Dict, Any

from app.rag.ingestion import run_ingestion
from app.core.logging import logger


async def trigger_ingestion() -> Dict[str, Any]:
    """Trigger the document ingestion pipeline."""
    logger.info("Triggering ingestion pipeline via service layer")
    return run_ingestion()
