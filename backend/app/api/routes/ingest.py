from fastapi import APIRouter, HTTPException

from app.services.ingest_service import trigger_ingestion
from app.core.logging import logger

router = APIRouter()


@router.post("/ingest")
async def ingest():
    """Trigger document ingestion: load, chunk, embed, and store documents."""
    try:
        result = await trigger_ingestion()
        return result
    except Exception as e:
        logger.error(f"Ingest endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Ingestion failed.")
